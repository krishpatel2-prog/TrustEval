"""Preprocessing script: rater filtering, target generation, and stratified fold assignment."""

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from trusteval.utils.config import load_experiment_config
from trusteval.data.loader import load_raw_dices_csv
from trusteval.data.preprocessor import prepare_dices_350

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("prepare_data")


def main():
    config_path = PROJECT_ROOT / "configs" / "experiment.yaml"
    logger.info(f"Loading configuration from {config_path}...")
    config = load_experiment_config(config_path)

    d_cfg = config["dataset"]
    e_cfg = config["evaluation"]

    raw_path = PROJECT_ROOT / d_cfg["raw_file"]
    if not raw_path.is_file():
        logger.error(f"Raw data file not found at {raw_path}. Run 01_fetch_dices.py first.")
        return 1

    logger.info(f"Loading raw annotations from {raw_path}...")
    raw_df = load_raw_dices_csv(raw_path)
    logger.info(f"Loaded {len(raw_df)} annotation rows.")

    removed_raters = [str(r).strip() for r in d_cfg["removed_raters"]]
    n_splits = e_cfg["cv_folds"]
    seed = config["experiment"]["seed"]

    logger.info("Executing preprocessing pipeline...")
    conversations_df, targets_df, audit = prepare_dices_350(
        raw_df=raw_df,
        removed_rater_ids=removed_raters,
        n_splits=n_splits,
        seed=seed,
    )

    # Output paths
    proc_conv_path = PROJECT_ROOT / d_cfg["processed_conversations"]
    proc_targ_path = PROJECT_ROOT / d_cfg["processed_targets"]
    proc_conv_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to parquet (and csv backup for transparency)
    conversations_df.to_parquet(proc_conv_path, index=False)
    conversations_df.to_csv(proc_conv_path.with_suffix(".csv"), index=False)
    logger.info(f"Saved {len(conversations_df)} conversations to {proc_conv_path} and .csv")

    targets_df.to_parquet(proc_targ_path, index=False)
    targets_df.to_csv(proc_targ_path.with_suffix(".csv"), index=False)
    logger.info(f"Saved {len(targets_df)} targets to {proc_targ_path} and .csv")

    # Save audit record
    audit_file = PROJECT_ROOT / config["paths"]["results_tables"] / "data_preparation_audit.json"
    audit_file.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)
    logger.info(f"Saved audit log to {audit_file}:")
    logger.info(json.dumps(audit, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())

