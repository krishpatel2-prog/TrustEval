"""Milestone 2: Hardware benchmark pilot and probability extraction validator on 20 items."""

import gc
import json
import logging
import os
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
import psutil
import torch

# Ensure Hugging Face cache resides on D: drive where disk space is abundant
os.environ.setdefault("HF_HOME", "D:/hf_cache")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from trusteval.utils.config import load_experiment_config
from trusteval.judges.cache import PredictionCache
from trusteval.judges.hf_judge import (
    HFJudge,
    get_process_memory_mb,
    get_system_available_ram_mb,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("benchmark_hardware")


def select_20_pilot_items(conversations_df: pd.DataFrame) -> pd.DataFrame:
    """Select 20 representative items across response-length ranges without observing human safety outcomes.

    Parameters
    ----------
    conversations_df : pd.DataFrame
        Deduplicated conversations dataframe containing `item_id` and `response_char_length`.

    Returns
    -------
    pd.DataFrame
        20 selected conversations spanning the length distribution.
    """
    sorted_df = conversations_df.sort_values("response_char_length").reset_index(drop=True)
    # 20 evenly spaced percentiles across response length
    indices = np.linspace(0, len(sorted_df) - 1, 20, dtype=int)
    selected = sorted_df.iloc[indices].copy()
    logger.info(
        f"Selected 20 pilot items across response lengths ranging from "
        f"{selected['response_char_length'].min()} to {selected['response_char_length'].max()} characters."
    )
    return selected


def benchmark_model(
    model_cfg: dict,
    pilot_items: pd.DataFrame,
    prompt_template: str,
    system_message: str,
    prompt_version: str,
    prompt_hash: str,
    cache: PredictionCache,
    threads: int = 4,
) -> dict:
    """Benchmark a single model sequentially, profiling latency, RAM, and logit validity."""
    model_id = model_cfg["id"]
    family = model_cfg["family"]
    params = model_cfg["params"]

    logger.info(f"\n{'='*70}\nStarting benchmark for model: {model_id} ({family}, {params})\n{'='*70}")

    initial_ram_mb = get_process_memory_mb()
    initial_sys_avail_mb = get_system_available_ram_mb()

    # Step 1: Load model
    t_load_start = time.time()
    try:
        judge = HFJudge(
            model_id=model_id,
            revision=model_cfg.get("revision", "main"),
            threads=threads,
            dtype=torch.bfloat16,
        )
        load_duration_sec = time.time() - t_load_start
    except Exception as e:
        logger.error(f"Failed to load model {model_id}: {e}")
        return {
            "model_id": model_id,
            "status": "failed_loading",
            "error": str(e),
        }

    post_load_ram_mb = get_process_memory_mb()
    peak_ram_mb = post_load_ram_mb

    latencies = []
    masses = []
    non_finite_count = 0
    records = []

    # Step 2: Evaluate 20 items sequentially
    for idx, row in enumerate(pilot_items.itertuples(), start=1):
        item_id = int(row.item_id)
        context = str(row.context)
        response = str(row.response)

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

        latencies.append(rec["inference_duration_sec"])
        masses.append(rec["mass_yes_no"])

        if np.isnan(rec["logit_yes"]) or np.isnan(rec["logit_no"]):
            non_finite_count += 1

        curr_ram = get_process_memory_mb()
        if curr_ram > peak_ram_mb:
            peak_ram_mb = curr_ram

        records.append(rec)
        if idx % 5 == 0 or idx == len(pilot_items):
            logger.info(
                f"  [{idx}/20] item_id={item_id:3d} | latency={rec['inference_duration_sec']:.2f}s | "
                f"mass={rec['mass_yes_no']:.4f} | cond_p_yes={rec['conditional_p_yes']:.4f} | "
                f"RAM={curr_ram:.1f} MB"
            )

    # Step 3: Unload and release memory
    judge.unload()
    del judge
    gc.collect()

    final_ram_mb = get_process_memory_mb()
    logger.info(
        f"Benchmark finished for {model_id}. Unloaded. "
        f"Initial RAM: {initial_ram_mb:.1f} MB -> Peak: {peak_ram_mb:.1f} MB -> Final: {final_ram_mb:.1f} MB."
    )

    return {
        "model_id": model_id,
        "family": family,
        "parameters": params,
        "license": model_cfg.get("license", "unknown"),
        "status": "success",
        "load_duration_sec": float(load_duration_sec),
        "initial_process_ram_mb": float(initial_ram_mb),
        "post_load_process_ram_mb": float(post_load_ram_mb),
        "peak_process_ram_mb": float(peak_ram_mb),
        "net_ram_increase_mb": float(peak_ram_mb - initial_ram_mb),
        "final_process_ram_mb": float(final_ram_mb),
        "system_available_ram_start_mb": float(initial_sys_avail_mb),
        "items_evaluated": len(pilot_items),
        "latency_mean_sec": float(np.mean(latencies)),
        "latency_median_sec": float(np.median(latencies)),
        "latency_min_sec": float(np.min(latencies)),
        "latency_max_sec": float(np.max(latencies)),
        "total_inference_time_sec": float(np.sum(latencies)),
        "mass_yes_no_mean": float(np.mean(masses)),
        "mass_yes_no_median": float(np.median(masses)),
        "mass_yes_no_min": float(np.min(masses)),
        "mass_yes_no_max": float(np.max(masses)),
        "non_finite_logits_count": non_finite_count,
    }


def main():
    config_path = PROJECT_ROOT / "configs" / "experiment.yaml"
    logger.info(f"Loading configuration from {config_path}...")
    config = load_experiment_config(config_path)

    # Load prompt text and hash
    p_cfg = config["prompt"]
    prompt_file = PROJECT_ROOT / p_cfg["file"]
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read()
    prompt_version = p_cfg["version"]
    prompt_hash = p_cfg["sha256"]
    system_message = p_cfg["system_message"]

    # Load processed conversations
    conv_file = PROJECT_ROOT / config["dataset"]["processed_conversations"]
    if not conv_file.is_file():
        logger.error(f"Processed conversations not found at {conv_file}. Run scripts/02_prepare_data.py first.")
        return 1

    conversations_df = pd.read_parquet(conv_file)
    logger.info(f"Loaded {len(conversations_df)} conversations from {conv_file}.")

    # Deterministically select 20 items across response length
    pilot_items = select_20_pilot_items(conversations_df)

    # Initialize persistent cache
    cache_path = PROJECT_ROOT / "results" / "predictions" / "pilot_predictions.jsonl"
    cache = PredictionCache(cache_path)

    # Check HF authentication
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    has_hf_token = bool(hf_token and len(hf_token.strip()) > 0)
    logger.info(f"Hugging Face authentication token present in environment: {has_hf_token}")

    benchmark_results = []
    models_to_run = []

    # Check candidate models
    for m in config["models"]["primary_candidates"]:
        if m.get("gated", False) and not has_hf_token:
            logger.warning(
                f"Model {m['id']} is marked as gated and no HF_TOKEN is configured. "
                "Logging model as inaccessible without authentication."
            )
            benchmark_results.append({
                "model_id": m["id"],
                "family": m["family"],
                "parameters": m["params"],
                "status": "skipped_gated_no_auth",
                "notes": "Requires HF_TOKEN with accepted Meta community license.",
            })
        else:
            models_to_run.append(m)

    # If Llama was skipped, also include the fallback model for benchmarking
    if any(r.get("status") == "skipped_gated_no_auth" for r in benchmark_results):
        fallback = config["models"]["fallback_candidate"]
        logger.info(
            f"Including fallback candidate {fallback['id']} ({fallback['family']}) "
            "for sequential benchmark comparison."
        )
        models_to_run.append(fallback)

    # Run benchmarks sequentially
    threads = config["hardware"].get("torch_threads", 4)
    for model_cfg in models_to_run:
        res = benchmark_model(
            model_cfg=model_cfg,
            pilot_items=pilot_items,
            prompt_template=prompt_template,
            system_message=system_message,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            cache=cache,
            threads=threads,
        )
        benchmark_results.append(res)

    # Save benchmark summary table
    summary_path = PROJECT_ROOT / "results" / "tables" / "hardware_benchmark_pilot.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2)

    logger.info(f"\nHardware benchmark pilot completed! Summary saved to {summary_path}")
    print("\n" + json.dumps(benchmark_results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

