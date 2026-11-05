"""Sequential evaluation runner for the two-judge TrustEval panel.

Judges:
1. Qwen/Qwen2.5-0.5B-Instruct
2. HuggingFaceTB/SmolLM2-1.7B-Instruct

Features:
- Immediate append-only JSONL caching.
- Resumes automatically from existing predictions.
- Memory monitoring and periodic garbage collection every 25 items.
- Strict sequential model loading (never two models in RAM concurrently).
"""

import argparse
import gc
import json
import logging
from pathlib import Path
import shutil
import sys
import time
from typing import Any, Dict, Optional

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
from trusteval.utils.config import load_experiment_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("evaluate_judges")


def evaluate_single_judge(
    model_id: str,
    output_cache_path: Path,
    seed_cache_path: Path | None,
    conversations_df: pd.DataFrame,
    prompt_template: str,
    system_message: str,
    prompt_version: str,
    prompt_hash: str,
    threads: int = 4,
    limit: int | None = None,
) -> Dict[str, Any]:
    """Run sequential inference on conversations for a single judge."""
    logger.info("=" * 70)
    logger.info(f"Starting sequential evaluation: {model_id}")
    logger.info("=" * 70)

    # 1. Setup Cache and Seed from existing pilot if needed
    output_cache_path.parent.mkdir(parents=True, exist_ok=True)
    if seed_cache_path and seed_cache_path.is_file() and not output_cache_path.is_file():
        logger.info(f"Seeding cache {output_cache_path.name} from {seed_cache_path.name}...")
        shutil.copyfile(seed_cache_path, output_cache_path)

    cache = PredictionCache(output_cache_path)
    logger.info(f"Current cache holds {len(cache)} existing predictions.")

    # 2. Filter items needing evaluation
    items_to_eval = []
    scoring_method = "next_token_binary_softmax"
    from trusteval.judges.cache import generate_cache_key

    for row in conversations_df.itertuples():
        item_id = int(row.item_id)
        k = generate_cache_key(
            model_id=model_id,
            model_revision="main",
            prompt_hash=prompt_hash,
            item_id=item_id,
            scoring_method=scoring_method,
        )
        if not cache.contains(k):
            items_to_eval.append(row)

    logger.info(f"Items remaining to evaluate: {len(items_to_eval)} of {len(conversations_df)}.")

    if limit is not None and limit > 0:
        items_to_eval = items_to_eval[:limit]
        logger.info(f"Applying execution limit: evaluating {len(items_to_eval)} items.")

    if len(items_to_eval) == 0:
        logger.info(f"All target items already cached for {model_id}. Skipping inference.")
        return {"model_id": model_id, "status": "completed_cached", "items_evaluated": 0}

    # 3. Load Model
    gc.collect()
    init_rss = get_process_memory_mb()
    init_avail = get_system_available_ram_mb()
    logger.info(f"Pre-load Process RSS: {init_rss:.1f} MB | Available RAM: {init_avail:.1f} MB")

    t0_load = time.time()
    judge = HFJudge(
        model_id=model_id,
        revision="main",
        threads=threads,
        dtype=torch.bfloat16,
    )
    load_time = time.time() - t0_load
    logger.info(f"Model {model_id} loaded in {load_time:.2f}s.")

    # 4. Evaluate Sequentially
    latencies = []
    peak_rss = get_process_memory_mb()

    for idx, row in enumerate(items_to_eval, start=1):
        item_id = int(row.item_id)
        context = str(row.context)
        response = str(row.response)

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

        if idx % 5 == 0 or idx == len(items_to_eval):
            logger.info(
                f"[{idx}/{len(items_to_eval)}] item_id={item_id:3d} | latency={lat:.2f}s | "
                f"P(Yes)={rec['conditional_p_yes']:.4f} | mass={rec['mass_yes_no']:.4f} | "
                f"RSS={curr_rss:.1f} MB | AvailRAM={avail_ram:.1f} MB"
            )

        # Periodic memory cleanup every 5 items
        if idx % 5 == 0:
            gc.collect()

    # 5. Clean Unload
    logger.info(f"Unloading model {model_id}...")
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


def main() -> int:
    parser = argparse.ArgumentParser(description="TrustEval Two-Judge Inference Runner")
    parser.add_argument("--model", choices=["qwen", "smollm", "all"], default="all")
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

    conv_path = PROJECT_ROOT / config["dataset"]["processed_conversations"]
    df = pd.read_parquet(conv_path)
    logger.info(f"Loaded {len(df)} conversations from {conv_path.name}.")

    models = []
    if args.model in ["qwen", "all"]:
        models.append({
            "id": "Qwen/Qwen2.5-0.5B-Instruct",
            "cache": PROJECT_ROOT / "results" / "predictions" / "qwen2.5_0.5b_dices350.jsonl",
            "seed": PROJECT_ROOT / "results" / "predictions" / "qwen_3item_pilot.jsonl",
        })
    if args.model in ["smollm", "all"]:
        models.append({
            "id": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
            "cache": PROJECT_ROOT / "results" / "predictions" / "smollm2_1.7b_dices350.jsonl",
            "seed": PROJECT_ROOT / "results" / "predictions" / "smollm2_smoke.jsonl",
        })

    for m in models:
        evaluate_single_judge(
            model_id=m["id"],
            output_cache_path=m["cache"],
            seed_cache_path=m["seed"],
            conversations_df=df,
            prompt_template=prompt_template,
            system_message=system_message,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            threads=args.threads,
            limit=args.limit,
        )

    logger.info("Sequential judge evaluation run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
