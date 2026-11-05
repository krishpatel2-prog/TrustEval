"""Three-item engineering smoke test for HuggingFaceTB/SmolLM2-1.7B-Instruct.

Validates:
1. Tokenizer token IDs for Yes/No in SmolLM2 vocabulary.
2. Chat template formatting.
3. Model CPU load behavior in bfloat16.
4. Deterministic next-token logit extraction on items [1, 2, 3].
5. Clean post-inference memory release.
"""

import gc
import json
import logging
from pathlib import Path
import sys
import time

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
logger = logging.getLogger("smollm2_smoke")


def main() -> int:
    logger.info("=" * 70)
    logger.info("SmolLM2-1.7B-Instruct: 3-Item Engineering Smoke Test")
    logger.info("=" * 70)

    # Telemetry
    initial_rss = get_process_memory_mb()
    initial_avail = get_system_available_ram_mb()
    logger.info(f"Initial Process RSS: {initial_rss:.1f} MB | Available RAM: {initial_avail:.1f} MB")

    # Config & Prompts
    config_file = PROJECT_ROOT / "configs" / "experiment.yaml"
    config = load_experiment_config(config_file)
    prompt_cfg = config["prompt"]
    prompt_file = PROJECT_ROOT / prompt_cfg["file"]
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read().strip()
    system_message = prompt_cfg["system_message"]
    prompt_version = prompt_cfg["version"]
    prompt_hash = prompt_cfg["sha256"]

    # Load Items [1, 2, 3]
    conv_path = PROJECT_ROOT / config["dataset"]["processed_conversations"]
    df = pd.read_parquet(conv_path)
    target_ids = [1, 2, 3]
    smoke_items = df[df["item_id"].isin(target_ids)].copy().sort_values("item_id")

    # Setup Cache
    cache_path = PROJECT_ROOT / "results" / "predictions" / "smollm2_smoke.jsonl"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache = PredictionCache(cache_path)

    # Initialize SmolLM2-1.7B
    model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    revision = "main"
    threads = config["hardware"].get("torch_threads", 4)
    model_dtype = torch.bfloat16

    logger.info(f"Initializing {model_id} (rev: {revision}, dtype: {model_dtype}, threads: {threads})...")
    t0_load = time.time()
    try:
        judge = HFJudge(
            model_id=model_id,
            revision=revision,
            threads=threads,
            dtype=model_dtype,
        )
    except Exception as e:
        logger.error(f"Failed to load {model_id}: {e}")
        return 1

    load_duration = time.time() - t0_load
    post_load_rss = get_process_memory_mb()
    post_load_avail = get_system_available_ram_mb()
    logger.info(
        f"Model loaded in {load_duration:.2f}s | "
        f"Post-load RSS: {post_load_rss:.1f} MB | "
        f"Available RAM: {post_load_avail:.1f} MB"
    )
    logger.info(f"SmolLM2 Token IDs: Yes={judge.yes_token_id}, No={judge.no_token_id}")

    # Evaluate Smoke Items
    results = []
    peak_rss = post_load_rss

    for idx, row in enumerate(smoke_items.itertuples(), start=1):
        item_id = int(row.item_id)
        context = str(row.context)
        response = str(row.response)

        curr_avail = get_system_available_ram_mb()
        if curr_avail < 150:
            logger.error(f"SAFETY ABORT: Available RAM dropped to {curr_avail:.1f} MB (< 150 MB)")
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
        if curr_rss > peak_rss:
            peak_rss = curr_rss

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
            "system_avail_ram_mb": curr_avail,
        }
        results.append(diag)
        logger.info(
            f"Item [{idx}/3] ID={item_id:2d} | Latency={rec['inference_duration_sec']:.2f}s | "
            f"Logit(Yes)={rec['logit_yes']:6.2f} | Logit(No)={rec['logit_no']:6.2f} | "
            f"P(Yes|Binary)={rec['conditional_p_yes']:.4f} | Mass={rec['mass_yes_no']:.4f} | "
            f"Top='{rec['top_token_text']}' | RSS={curr_rss:.1f} MB"
        )

    # Unload
    logger.info("Unloading SmolLM2 judge model...")
    judge.unload()
    del judge
    gc.collect()

    post_unload_rss = get_process_memory_mb()
    post_unload_avail = get_system_available_ram_mb()
    logger.info(
        f"Post-unload RSS: {post_unload_rss:.1f} MB (Peak was {peak_rss:.1f} MB) | "
        f"Available RAM: {post_unload_avail:.1f} MB"
    )

    # Summary
    summary = {
        "model_id": model_id,
        "revision": revision,
        "precision": str(model_dtype),
        "threads": threads,
        "load_duration_sec": load_duration,
        "peak_rss_mb": peak_rss,
        "post_unload_rss_mb": post_unload_rss,
        "items_evaluated": len(results),
        "mean_latency_sec": float(np.mean([d["latency_sec"] for d in results])),
        "mean_mass_yes_no": float(np.mean([d["mass_yes_no"] for d in results])),
        "results": results,
    }

    summary_path = PROJECT_ROOT / "results" / "tables" / "smollm2_smoke_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info("=" * 70)
    logger.info("SMOLLM2-1.7B SMOKE TEST COMPLETE")
    logger.info("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
