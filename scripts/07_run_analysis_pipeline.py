"""Master analysis pipeline for TrustEval (Phases 2, 3, 4, 5).

Executes:
1. Two-judge ensemble aggregation (Phase 2).
2. Human agreement, calibration, and rater cluster bootstrapping (Phase 3).
3. Judge disagreement predictive modeling and cross-validation (Phase 4).
4. Publication-quality figure generation (Phase 5).
"""

import json
import logging
from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

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
logger = logging.getLogger("analysis_pipeline")


def load_predictions_jsonl(path: Path) -> pd.DataFrame:
    """Load JSONL predictions into a pandas DataFrame."""
    if not path.is_file():
        raise FileNotFoundError(f"Predictions file not found: {path}")
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return pd.DataFrame(records)


def main() -> int:
    logger.info("=" * 70)
    logger.info("TrustEval Research Analysis Pipeline")
    logger.info("=" * 70)

    config_file = PROJECT_ROOT / "configs" / "experiment.yaml"
    config = load_experiment_config(config_file)

    # 1. Determine Prediction Sources (Full vs Pilot Fallback)
    qwen_full = PROJECT_ROOT / "results" / "predictions" / "qwen2.5_0.5b_dices350.jsonl"
    qwen_pilot = PROJECT_ROOT / "results" / "predictions" / "qwen_3item_pilot.jsonl"
    qwen_path = qwen_full if qwen_full.is_file() else qwen_pilot

    smollm_full = PROJECT_ROOT / "results" / "predictions" / "smollm2_1.7b_dices350.jsonl"
    smollm_smoke = PROJECT_ROOT / "results" / "predictions" / "smollm2_smoke.jsonl"
    smollm_path = smollm_full if smollm_full.is_file() else smollm_smoke

    logger.info(f"Loading Qwen predictions from: {qwen_path.name}")
    qwen_df = load_predictions_jsonl(qwen_path)
    logger.info(f"Loading SmolLM predictions from: {smollm_path.name}")
    smollm_df = load_predictions_jsonl(smollm_path)

    # 2. Load Processed Data
    conv_path = PROJECT_ROOT / config["dataset"]["processed_conversations"]
    tgt_path = PROJECT_ROOT / config["dataset"]["processed_targets"]
    conv_df = pd.read_parquet(conv_path)
    tgt_df = pd.read_parquet(tgt_path)

    # 3. Phase 2: Build Ensemble Table
    logger.info("Building two-judge ensemble and calculating disagreement...")
    ensemble_df = build_two_judge_ensemble(
        qwen_predictions=qwen_df,
        smollm_predictions=smollm_df,
        conversations=conv_df,
        human_targets=tgt_df,
    )

    ens_csv = PROJECT_ROOT / "results" / "tables" / "ensemble_predictions.csv"
    ens_parquet = PROJECT_ROOT / "results" / "tables" / "ensemble_predictions.parquet"
    ens_csv.parent.mkdir(parents=True, exist_ok=True)
    ensemble_df.to_csv(ens_csv, index=False)
    ensemble_df.to_parquet(ens_parquet, index=False)
    logger.info(f"Saved ensemble predictions ({len(ensemble_df)} items) to {ens_csv.name}")

    # 4. Phase 3: Evaluate Point Metrics
    logger.info("Calculating point evaluation metrics against human targets...")
    point_metrics = {}
    models = ["p_qwen", "p_smollm", "p_ensemble"]

    for m in models:
        clean = ensemble_df.dropna(subset=[m, "h_primary"])
        reg_m = calculate_regression_metrics(clean[m].values, clean["h_primary"].values)
        ece_m = calculate_expected_calibration_error(clean[m].values, clean["h_primary"].values, n_bins=10)
        point_metrics[m] = {
            "n_items": len(clean),
            **reg_m,
            **ece_m,
        }

    # 5. Rater-Level Cluster Bootstrapping (if full annotations available)
    raw_path = PROJECT_ROOT / config["dataset"]["raw_file"]
    if raw_path.is_file() and len(ensemble_df) >= 3:
        logger.info("Executing rater-level cluster bootstrap (1000 resamples)...")
        raw_df = pd.read_csv(raw_path)
        filtered_annos, _ = filter_raters(raw_df, config["dataset"]["removed_raters"])
        boot_results = bootstrap_raters_and_evaluate(
            raw_annotations_df=filtered_annos,
            predictions_df=ensemble_df,
            n_resamples=config["evaluation"]["bootstrap"].get("n_resamples", 1000),
            seed=config["evaluation"]["bootstrap"].get("seed", 20261103),
            confidence_level=config["evaluation"]["bootstrap"].get("confidence_level", 0.95),
        )
    else:
        boot_results = {}

    metrics_output = {
        "point_metrics": point_metrics,
        "rater_cluster_bootstrap": boot_results,
    }

    metrics_file = PROJECT_ROOT / "results" / "tables" / "human_agreement_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics_output, f, indent=2)
    logger.info(f"Saved human agreement metrics and bootstrap CIs to {metrics_file.name}")

    # 6. Phase 4: Disagreement Predictive Modeling (if sufficient items)
    if len(ensemble_df) >= 20:
        logger.info("Conducting cross-validated disagreement predictive analysis...")
        disagreement_results = analyze_disagreement_predictive_power(
            df=ensemble_df,
            target_col="h_primary",
            length_col="response_char_length",
            n_splits=5,
            seed=20261103,
        )
        dis_file = PROJECT_ROOT / "results" / "tables" / "disagreement_analysis.json"
        with open(dis_file, "w", encoding="utf-8") as f:
            json.dump(disagreement_results, f, indent=2)
        logger.info(f"Saved disagreement predictive analysis to {dis_file.name}")
    else:
        logger.info(f"Skipping disagreement regression (n={len(ensemble_df)} < 20). Requires full prediction set.")

    # 7. Phase 5: Publication Figures
    fig_dir = PROJECT_ROOT / "results" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    if len(ensemble_df) >= 3:
        logger.info("Generating publication figures...")
        f1 = plot_reliability_diagrams(ensemble_df, fig_dir / "figure1_reliability_diagrams.png")
        f3 = plot_distribution_alignment(ensemble_df, fig_dir / "figure3_distribution_alignment.png")
        logger.info(f"Generated Figure 1: {f1.name}")
        logger.info(f"Generated Figure 3: {f3.name}")

        if len(ensemble_df) >= 20:
            f2 = plot_disagreement_vs_error(ensemble_df, fig_dir / "figure2_disagreement_vs_error.png")
            logger.info(f"Generated Figure 2: {f2.name}")

    logger.info("=" * 70)
    logger.info("ANALYSIS PIPELINE COMPLETE")
    logger.info("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
