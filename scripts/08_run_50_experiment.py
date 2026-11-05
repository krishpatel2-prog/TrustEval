"""Fifty-Conversation Experiment Runner & Analysis Pipeline for TrustEval.

Manages:
1. 50-item sample inference for Qwen2.5-0.5B-Instruct.
2. 50-item sample inference for SmolLM2-1.7B-Instruct.
3. Equal-weight two-judge ensemble generation.
4. Evaluation pipeline: MAE, RMSE, Brier, ECE, rater cluster bootstrap,
   5-fold CV disagreement predictive modeling, and publication figure generation.
"""

import argparse
import gc
import json
import logging
from pathlib import Path
import shutil
import sys
import time
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import psutil
import torch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from trusteval.judges.cache import PredictionCache
from trusteval.judges.hf_judge import (
    HFJudge,
    get_process_memory_mb,
    get_system_available_ram_mb,
)
from trusteval.evaluation.ensemble import build_two_judge_ensemble
from trusteval.evaluation.metrics import (
    calculate_regression_metrics,
    calculate_expected_calibration_error,
)
from trusteval.evaluation.bootstrap import bootstrap_raters_and_evaluate
from trusteval.evaluation.disagreement import analyze_disagreement_predictive_power
from trusteval.evaluation.figures import (
    plot_reliability_diagrams,
    plot_disagreement_vs_error,
    plot_distribution_alignment,
)
from trusteval.data.preprocessor import filter_raters
from trusteval.utils.config import load_experiment_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("dices50_experiment")


def seed_cache_from_sources(
    target_cache_path: Path,
    source_paths: List[Path],
    target_item_ids: set,
) -> int:
    """Populate target cache with matching records from prior prediction files."""
    if target_cache_path.is_file() and target_cache_path.stat().st_size > 0:
        return 0

    target_cache_path.parent.mkdir(parents=True, exist_ok=True)
    seeded_records = {}

    for src in source_paths:
        if not src.is_file():
            continue
        with open(src, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                    iid = rec.get("item_id")
                    if iid in target_item_ids and iid not in seeded_records:
                        seeded_records[iid] = line.strip()
                except json.JSONDecodeError:
                    pass

    if seeded_records:
        with open(target_cache_path, "w", encoding="utf-8") as f:
            for iid in sorted(seeded_records.keys()):
                f.write(seeded_records[iid] + "\n")
        logger.info(f"Seeded {len(seeded_records)} existing predictions into {target_cache_path.name}")
    return len(seeded_records)


def run_judge_inference(
    model_id: str,
    output_cache_path: Path,
    seed_sources: List[Path],
    conversations_df: pd.DataFrame,
    prompt_template: str,
    system_message: str,
    prompt_version: str,
    prompt_hash: str,
    threads: int = 4,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Run sequential inference on the 50 conversations for a single judge."""
    logger.info("=" * 70)
    logger.info(f"Starting 50-Item Sequential Evaluation: {model_id}")
    logger.info("=" * 70)

    target_item_ids = set(conversations_df["item_id"].tolist())

    # Seed cache from existing prior runs if empty
    seed_cache_from_sources(output_cache_path, seed_sources, target_item_ids)

    cache = PredictionCache(output_cache_path)
    logger.info(f"Current cache holds {len(cache)} existing predictions.")

    # Filter to remaining items
    cached_item_ids = {int(rec["item_id"]) for rec in cache._entries.values()}
    items_to_eval = [
        row for row in conversations_df.itertuples()
        if int(row.item_id) not in cached_item_ids
    ]
    logger.info(f"Items remaining to evaluate: {len(items_to_eval)} of {len(conversations_df)}.")

    if not items_to_eval:
        logger.info(f"All {len(conversations_df)} items are already cached for {model_id}.")
        return {
            "model_id": model_id,
            "status": "already_complete",
            "items_evaluated": 0,
            "total_cached": len(cache),
        }

    if limit is not None and limit < len(items_to_eval):
        logger.info(f"Applying execution limit: evaluating {limit} items.")
        items_to_eval = items_to_eval[:limit]

    # Check RAM before loading
    pre_rss = get_process_memory_mb()
    pre_avail = get_system_available_ram_mb()
    logger.info(f"Pre-load Process RSS: {pre_rss:.1f} MB | Available RAM: {pre_avail:.1f} MB")

    if pre_avail < 300.0:
        logger.warning(f"Low system memory before load ({pre_avail:.1f} MB). Running pre-emptive GC...")
        gc.collect()

    t0_load = time.time()
    judge = HFJudge(
        model_id=model_id,
        revision="main",
        threads=threads,
        dtype=torch.bfloat16,
    )
    load_time = time.time() - t0_load
    logger.info(f"Model {model_id} loaded in {load_time:.2f}s.")

    latencies = []
    peak_rss = get_process_memory_mb()

    for idx, row in enumerate(items_to_eval, start=1):
        item_id = int(row.item_id)
        context = str(row.context)
        response = str(row.response)

        # Dynamic Memory Safety Guard
        avail_ram = get_system_available_ram_mb()
        if avail_ram < 80.0:
            gc.collect()
            time.sleep(2.0)
            avail_ram = get_system_available_ram_mb()
            if avail_ram < 50.0:
                logger.error(
                    f"SAFETY ABORT: Available RAM dropped critically to {avail_ram:.1f} MB (< 50 MB)."
                )
                break

        rec = judge.evaluate_and_cache(
            item_id=item_id,
            context=context,
            response=response,
            prompt_template=prompt_template,
            system_message=system_message,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            cache=cache,
        )

        lat = rec["inference_duration_sec"]
        latencies.append(lat)
        curr_rss = get_process_memory_mb()
        if curr_rss > peak_rss:
            peak_rss = curr_rss

        logger.info(
            f"[{idx}/{len(items_to_eval)}] item_id={item_id:3d} | latency={lat:.2f}s | "
            f"P(Yes)={rec['conditional_p_yes']:.4f} | mass={rec['mass_yes_no']:.4f} | "
            f"RSS={curr_rss:.1f} MB | AvailRAM={avail_ram:.1f} MB"
        )

        if idx % 5 == 0:
            gc.collect()

    # Clean Unload
    logger.info(f"Unloading model {model_id} from memory...")
    judge.unload()
    del judge
    gc.collect()

    final_rss = get_process_memory_mb()
    final_avail = get_system_available_ram_mb()
    logger.info(
        f"Evaluation finished for {model_id}. "
        f"Peak RSS: {peak_rss:.1f} MB -> Final RSS: {final_rss:.1f} MB | "
        f"Final Available RAM: {final_avail:.1f} MB"
    )

    return {
        "model_id": model_id,
        "status": "success",
        "items_evaluated": len(latencies),
        "mean_latency_sec": float(np.mean(latencies)) if latencies else 0.0,
        "peak_rss_mb": peak_rss,
        "total_cached": len(cache),
    }


def run_evaluation_pipeline(
    manifest_df: pd.DataFrame,
    qwen_cache_path: Path,
    smollm_cache_path: Path,
    config: dict,
) -> Dict[str, Any]:
    """Execute complete TrustEval evaluation pipeline on the 50-item sample."""
    logger.info("=" * 70)
    logger.info("Running 50-Item TrustEval Analysis Pipeline")
    logger.info("=" * 70)

    # 1. Load Predictions
    def load_pred_df(path: Path) -> pd.DataFrame:
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        return pd.DataFrame(records)

    qwen_df = load_pred_df(qwen_cache_path)
    smollm_df = load_pred_df(smollm_cache_path)
    logger.info(f"Loaded {len(qwen_df)} Qwen predictions and {len(smollm_df)} SmolLM2 predictions.")

    # 2. Phase 2: Two-Judge Ensemble
    conv_df = manifest_df[["item_id", "context", "response", "response_char_length", "response_word_length"]].copy()
    tgt_df = manifest_df[[
        "item_id", "count_yes", "count_no", "count_unsure", "total_valid_votes",
        "total_all_votes", "h_primary", "h_sensitivity", "majority_label", "is_tie", "cv_fold"
    ]].copy()

    ensemble_df = build_two_judge_ensemble(
        qwen_predictions=qwen_df,
        smollm_predictions=smollm_df,
        conversations=conv_df,
        human_targets=tgt_df,
    )

    ens_csv = PROJECT_ROOT / "results" / "tables" / "ensemble_predictions_dices50.csv"
    ens_parquet = PROJECT_ROOT / "results" / "tables" / "ensemble_predictions_dices50.parquet"
    ens_csv.parent.mkdir(parents=True, exist_ok=True)
    ensemble_df.to_csv(ens_csv, index=False)
    ensemble_df.to_parquet(ens_parquet, index=False)
    logger.info(f"Saved 50-item ensemble predictions to {ens_csv.name}")

    # 3. Phase 3: Point Metrics
    models = {
        "Qwen2.5-0.5B": ensemble_df["p_qwen"].values,
        "SmolLM2-1.7B": ensemble_df["p_smollm"].values,
        "Ensemble (Mean)": ensemble_df["p_ensemble"].values,
    }

    metrics_primary = {}
    metrics_sensitivity = {}

    for name, preds in models.items():
        reg_p = calculate_regression_metrics(preds, ensemble_df["h_primary"].values)
        ece_p = calculate_expected_calibration_error(preds, ensemble_df["h_primary"].values)
        metrics_primary[name] = {**reg_p, **ece_p}

        reg_s = calculate_regression_metrics(preds, ensemble_df["h_sensitivity"].values)
        ece_s = calculate_expected_calibration_error(preds, ensemble_df["h_sensitivity"].values)
        metrics_sensitivity[name] = {**reg_s, **ece_s}

    metrics_summary = {
        "primary_target_h_primary": metrics_primary,
        "sensitivity_target_h_sensitivity": metrics_sensitivity,
    }

    metrics_json = PROJECT_ROOT / "results" / "tables" / "evaluation_metrics_dices50.json"
    with open(metrics_json, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)
    logger.info(f"Saved metrics summary to {metrics_json.name}")

    # 4. Rater Cluster Bootstrap
    raw_path = PROJECT_ROOT / config["dataset"]["raw_file"]
    raw_df = pd.read_csv(raw_path)
    removed_raters = set(str(r).strip() for r in config["dataset"]["removed_raters"])
    raw_df["rater_id"] = raw_df["rater_id"].astype(str).str.strip()
    raw_df = raw_df[~raw_df["rater_id"].isin(removed_raters)].copy()

    # Filter raw annotations to the 50 items
    sampled_item_ids = set(manifest_df["item_id"].tolist())
    raw_df_50 = raw_df[raw_df["item_id"].isin(sampled_item_ids)].copy()

    boot_pred_df = ensemble_df[["item_id", "p_qwen", "p_smollm", "p_ensemble"]].copy()

    logger.info("Executing rater cluster bootstrap on 50-item sample (1000 resamples)...")
    boot_ci = bootstrap_raters_and_evaluate(
        raw_annotations_df=raw_df_50,
        predictions_df=boot_pred_df,
        n_resamples=1000,
        seed=config["experiment"]["seed"],
        confidence_level=0.95,
    )

    boot_json = PROJECT_ROOT / "results" / "tables" / "bootstrap_ci_dices50.json"
    with open(boot_json, "w", encoding="utf-8") as f:
        json.dump(boot_ci, f, indent=2)
    logger.info(f"Saved bootstrap CIs to {boot_json.name}")

    # 5. Phase 4: Disagreement Predictive Power (5-Fold CV)
    logger.info("Analyzing disagreement predictive power via 5-fold CV...")
    disagreement_results = analyze_disagreement_predictive_power(
        df=ensemble_df,
        n_splits=5,
        seed=config["experiment"]["seed"],
    )

    disag_json = PROJECT_ROOT / "results" / "tables" / "disagreement_cv_dices50.json"
    with open(disag_json, "w", encoding="utf-8") as f:
        json.dump(disagreement_results, f, indent=2)
    logger.info(f"Saved disagreement CV results to {disag_json.name}")

    # 6. Phase 5: Figures
    fig_dir = PROJECT_ROOT / "results" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Reliability diagrams
    fig_rel = fig_dir / "reliability_diagrams_dices50.png"
    plot_reliability_diagrams(
        ensemble_df=ensemble_df,
        output_path=fig_rel,
    )
    logger.info(f"Generated {fig_rel.name}")

    # Disagreement vs Error
    fig_dis = fig_dir / "disagreement_vs_error_dices50.png"
    plot_disagreement_vs_error(
        ensemble_df=ensemble_df,
        output_path=fig_dis,
    )
    logger.info(f"Generated {fig_dis.name}")

    # Distribution Alignment
    fig_dist = fig_dir / "distribution_alignment_dices50.png"
    plot_distribution_alignment(
        ensemble_df=ensemble_df,
        output_path=fig_dist,
    )
    logger.info(f"Generated {fig_dist.name}")

    return {
        "status": "success",
        "sample_size": len(ensemble_df),
        "metrics": metrics_summary,
        "bootstrap_ci": boot_ci,
        "disagreement": disagreement_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="TrustEval 50-Item Experiment Runner")
    parser.add_argument("--step", choices=["qwen", "smollm", "evaluate", "all"], default="all")
    parser.add_argument("--limit", type=int, default=None, help="Max items to evaluate per judge")
    parser.add_argument("--threads", type=int, default=4, help="CPU threads for PyTorch")
    args = parser.parse_args()

    config_file = PROJECT_ROOT / "configs" / "experiment.yaml"
    config = load_experiment_config(config_file)
    prompt_cfg = config["prompt"]
    prompt_file = PROJECT_ROOT / prompt_cfg["file"]
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read().strip()
    system_message = prompt_cfg["system_message"]
    prompt_version = prompt_cfg["version"]
    prompt_hash = prompt_cfg["sha256"]

    manifest_parquet = PROJECT_ROOT / "data" / "processed" / "dices_50_sample_manifest.parquet"
    if not manifest_parquet.is_file():
        logger.error(f"Sample manifest not found at {manifest_parquet}!")
        return 1

    manifest_df = pd.read_parquet(manifest_parquet)
    logger.info(f"Loaded 50-item sample manifest ({len(manifest_df)} items).")

    qwen_cache = PROJECT_ROOT / "results" / "predictions" / "qwen2.5_0.5b_dices50.jsonl"
    smollm_cache = PROJECT_ROOT / "results" / "predictions" / "smollm2_1.7b_dices50.jsonl"

    qwen_sources = [
        PROJECT_ROOT / "results" / "predictions" / "qwen2.5_0.5b_dices350.jsonl",
        PROJECT_ROOT / "results" / "predictions" / "qwen_3item_pilot.jsonl",
    ]
    smollm_sources = [
        PROJECT_ROOT / "results" / "predictions" / "smollm2_1.7b_dices350.jsonl",
        PROJECT_ROOT / "results" / "predictions" / "smollm2_smoke.jsonl",
    ]

    # Step 1: Qwen
    if args.step in ["qwen", "all"]:
        run_judge_inference(
            model_id="Qwen/Qwen2.5-0.5B-Instruct",
            output_cache_path=qwen_cache,
            seed_sources=qwen_sources,
            conversations_df=manifest_df,
            prompt_template=prompt_template,
            system_message=system_message,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            threads=args.threads,
            limit=args.limit,
        )

    # Step 2: SmolLM2
    if args.step in ["smollm", "all"]:
        run_judge_inference(
            model_id="HuggingFaceTB/SmolLM2-1.7B-Instruct",
            output_cache_path=smollm_cache,
            seed_sources=smollm_sources,
            conversations_df=manifest_df,
            prompt_template=prompt_template,
            system_message=system_message,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            threads=args.threads,
            limit=args.limit,
        )

    # Step 3: Evaluation Pipeline
    if args.step in ["evaluate", "all"]:
        # Verify both caches have predictions
        if not qwen_cache.is_file() or not smollm_cache.is_file():
            logger.warning("One or both prediction caches do not exist yet. Cannot run evaluation.")
            return 0
        run_evaluation_pipeline(
            manifest_df=manifest_df,
            qwen_cache_path=qwen_cache,
            smollm_cache_path=smollm_cache,
            config=config,
        )

    logger.info("TrustEval 50-Item Experiment runner complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
