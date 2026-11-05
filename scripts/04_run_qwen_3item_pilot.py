"""Minimal 3-Item Engineering Smoke Test for Qwen2.5-0.5B-Instruct on CPU.

Validates:
1. Exact CPU memory behavior (RSS, available RAM).
2. Deterministic next-token logit extraction (Yes/No).
3. Chat template formatting and single-token IDs.
4. Clean post-inference memory release (unload).
"""

import gc
import json
import logging
import os
from pathlib import Path
import sys
import time

import numpy as np
import pandas as pd
import psutil
import torch

# Add src to Python path
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
logger = logging.getLogger("qwen_pilot")


def main() -> int:
    logger.info("=" * 70)
    logger.info("TrustEval: Qwen2.5-0.5B 3-Item Engineering Smoke Test")
    logger.info("=" * 70)

    # 1. System and CPU Telemetry
    vm = psutil.virtual_memory()
    initial_rss_mb = get_process_memory_mb()
    initial_avail_mb = get_system_available_ram_mb()
    logger.info(f"System Physical RAM: {vm.total / (1024**3):.2f} GB")
    logger.info(f"Initial Available RAM: {initial_avail_mb:.1f} MB ({vm.percent}% utilized)")
    logger.info(f"Initial Process RSS: {initial_rss_mb:.1f} MB")
    logger.info(f"PyTorch Version: {torch.__version__}")

    # 2. Load Configuration and Prompt
    config_file = PROJECT_ROOT / "configs" / "experiment.yaml"
    config = load_experiment_config(config_file)
    prompt_cfg = config["prompt"]
    prompt_file = PROJECT_ROOT / prompt_cfg["file"]
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read().strip()
    system_message = prompt_cfg["system_message"]
    prompt_version = prompt_cfg["version"]
    prompt_hash = prompt_cfg["sha256"]

    # 3. Load Processed Conversations and select items [1, 2, 3]
    conv_path = PROJECT_ROOT / config["dataset"]["processed_conversations"]
    df = pd.read_parquet(conv_path)
    target_ids = [1, 2, 3]
    pilot_items = df[df["item_id"].isin(target_ids)].copy().sort_values("item_id")

    if len(pilot_items) != 3:
        logger.error(f"Expected 3 items with IDs {target_ids}, found {len(pilot_items)}")
        return 1

    logger.info(f"Selected {len(pilot_items)} distinct items: {pilot_items['item_id'].tolist()}")

    # 4. Initialize Prediction Cache
    cache_path = PROJECT_ROOT / "results" / "predictions" / "qwen_3item_pilot.jsonl"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache = PredictionCache(cache_path)

    # 5. Load Model with Memory Tracking
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    revision = "main"
    threads = config["hardware"].get("torch_threads", 4)
    model_dtype = torch.bfloat16

    logger.info(f"Loading {model_id} (rev: {revision}, dtype: {model_dtype}, threads: {threads})...")
    t0_load = time.time()
    judge = HFJudge(
        model_id=model_id,
        revision=revision,
        threads=threads,
        dtype=model_dtype,
    )
    load_duration = time.time() - t0_load

    post_load_rss_mb = get_process_memory_mb()
    post_load_avail_mb = get_system_available_ram_mb()
    net_load_rss_mb = post_load_rss_mb - initial_rss_mb

    logger.info(
        f"Model loaded in {load_duration:.2f}s | "
        f"Post-load RSS: {post_load_rss_mb:.1f} MB (Net: +{net_load_rss_mb:.1f} MB) | "
        f"Available RAM: {post_load_avail_mb:.1f} MB"
    )
    logger.info(f"Token IDs confirmed: Yes={judge.yes_token_id}, No={judge.no_token_id}")

    # 6. Run Inference on 3 Items
    item_diagnostics = []
    peak_rss_mb = post_load_rss_mb

    for idx, row in enumerate(pilot_items.itertuples(), start=1):
        item_id = int(row.item_id)
        context = str(row.context)
        response = str(row.response)

        curr_avail_mb = get_system_available_ram_mb()
        if curr_avail_mb < 200:
            logger.error(f"SAFETY ABORT: Available RAM dropped to {curr_avail_mb:.1f} MB (< 200 MB)")
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

        curr_rss = get_process_memory_mb()
        if curr_rss > peak_rss_mb:
            peak_rss_mb = curr_rss

        diag = {
            "item_id": item_id,
            "latency_sec": rec["inference_duration_sec"],
            "logit_yes": rec["logit_yes"],
            "logit_no": rec["logit_no"],
            "logit_diff": rec["logit_yes"] - rec["logit_no"],
            "mass_yes_no": rec["mass_yes_no"],
            "conditional_p_yes": rec["conditional_p_yes"],
            "conditional_p_no": rec["conditional_p_no"],
            "top_token_text": rec["top_token_text"],
            "precision": rec["precision"],
            "process_rss_mb": curr_rss,
            "system_avail_ram_mb": curr_avail_mb,
        }
        item_diagnostics.append(diag)
        logger.info(
            f"Item [{idx}/3] ID={item_id:2d} | Latency={rec['inference_duration_sec']:.2f}s | "
            f"Logit(Yes)={rec['logit_yes']:6.2f} | Logit(No)={rec['logit_no']:6.2f} | "
            f"P(Yes|Binary)={rec['conditional_p_yes']:.4f} | Mass={rec['mass_yes_no']:.4f} | "
            f"Top='{rec['top_token_text']}' | RSS={curr_rss:.1f} MB"
        )

    # 7. Unload and Measure Memory Release
    logger.info("Unloading judge model...")
    judge.unload()
    del judge
    gc.collect()

    post_unload_rss_mb = get_process_memory_mb()
    post_unload_avail_mb = get_system_available_ram_mb()
    freed_rss_mb = peak_rss_mb - post_unload_rss_mb

    logger.info(
        f"Post-unload RSS: {post_unload_rss_mb:.1f} MB (Freed: {freed_rss_mb:.1f} MB) | "
        f"Available RAM: {post_unload_avail_mb:.1f} MB"
    )

    # 8. Save Summary JSON
    summary = {
        "model_id": model_id,
        "revision": revision,
        "precision": str(model_dtype),
        "threads": threads,
        "load_duration_sec": load_duration,
        "initial_rss_mb": initial_rss_mb,
        "post_load_rss_mb": post_load_rss_mb,
        "peak_rss_mb": peak_rss_mb,
        "post_unload_rss_mb": post_unload_rss_mb,
        "memory_freed_mb": freed_rss_mb,
        "initial_avail_ram_mb": initial_avail_mb,
        "final_avail_ram_mb": post_unload_avail_mb,
        "items_evaluated": len(item_diagnostics),
        "mean_latency_sec": float(np.mean([d["latency_sec"] for d in item_diagnostics])),
        "mean_mass_yes_no": float(np.mean([d["mass_yes_no"] for d in item_diagnostics])),
        "item_results": item_diagnostics,
    }

    summary_file = PROJECT_ROOT / "results" / "tables" / "qwen_3item_pilot_summary.json"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Pilot summary saved to {summary_file}")
    logger.info("=" * 70)
    logger.info("QWEN2.5-0.5B PILOT SUCCESSFUL")
    logger.info("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
