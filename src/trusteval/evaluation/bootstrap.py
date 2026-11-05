"""Cluster bootstrap inference accounting for rater-level dependence in DICES-350."""

import logging
from typing import Callable, Dict, List, Tuple
import numpy as np
import pandas as pd

from .metrics import calculate_regression_metrics, calculate_expected_calibration_error

logger = logging.getLogger(__name__)


def bootstrap_raters_and_evaluate(
    raw_annotations_df: pd.DataFrame,
    predictions_df: pd.DataFrame,
    n_resamples: int = 1000,
    seed: int = 20261103,
    confidence_level: float = 0.95,
) -> Dict[str, Dict[str, float]]:
    """Perform cluster bootstrap by resampling raters with replacement.

    Accounts for the shared-rater structure of DICES annotations.

    Parameters
    ----------
    raw_annotations_df : pd.DataFrame
        Filtered annotations containing `rater_id`, `item_id`, and `Q_overall`.
    predictions_df : pd.DataFrame
        Model/ensemble predictions indexed by `item_id`, containing:
        `p_qwen`, `p_smollm`, and `p_ensemble`.
    n_resamples : int, default=1000
        Number of bootstrap iterations.
    seed : int, default=20261103
        Random seed for reproducibility.
    confidence_level : float, default=0.95
        Coverage level for confidence intervals.

    Returns
    -------
    Dict[str, Dict[str, float]]
        Nested dictionary of metrics and their 95% bootstrap confidence intervals.
    """
    rng = np.random.default_rng(seed)

    # Unique raters
    raters = np.array(sorted(raw_annotations_df["rater_id"].unique()))
    n_raters = len(raters)
    logger.info(f"Running rater cluster bootstrap over {n_raters} unique raters ({n_resamples} iterations)...")

    # Group annotations by rater for O(1) sampling lookup
    rater_groups = {
        r_id: grp[["item_id", "Q_overall"]].copy()
        for r_id, grp in raw_annotations_df.groupby("rater_id")
    }

    judge_keys = [k for k in ["p_qwen", "p_smollm", "p_ensemble"] if k in predictions_df.columns]

    boot_metrics: Dict[str, Dict[str, List[float]]] = {
        jk: {"mae": [], "rmse": [], "brier": [], "ece": []} for jk in judge_keys
    }

    item_order = predictions_df["item_id"].values

    for b in range(n_resamples):
        # Sample raters with replacement
        sampled_rater_indices = rng.integers(0, n_raters, size=n_raters)
        sampled_raters = raters[sampled_rater_indices]

        # Aggregate annotations from sampled raters
        sampled_annos = pd.concat([rater_groups[r] for r in sampled_raters], ignore_index=True)

        # Compute conversation-level h_primary
        # Y / (Y + N)
        counts = sampled_annos.groupby(["item_id", "Q_overall"]).size().unstack(fill_value=0)
        col_y = "Yes" if "Yes" in counts.columns else None
        col_n = "No" if "No" in counts.columns else None

        if col_y is None and col_n is None:
            continue

        c_yes = counts[col_y] if col_y in counts.columns else pd.Series(0, index=counts.index)
        c_no = counts[col_n] if col_n in counts.columns else pd.Series(0, index=counts.index)
        denom = c_yes + c_no

        # Handle zero valid votes gracefully
        h_boot = np.where(denom > 0, c_yes / np.maximum(denom, 1), 0.5)
        h_boot_series = pd.Series(h_boot, index=counts.index)

        # Align with predictions item_id order
        aligned_h = h_boot_series.reindex(item_order).fillna(0.5).values

        for jk in judge_keys:
            preds = predictions_df[jk].values
            reg_m = calculate_regression_metrics(preds, aligned_h)
            ece_m = calculate_expected_calibration_error(preds, aligned_h, n_bins=10)

            boot_metrics[jk]["mae"].append(reg_m["mae"])
            boot_metrics[jk]["rmse"].append(reg_m["rmse"])
            boot_metrics[jk]["brier"].append(reg_m["brier_score"])
            boot_metrics[jk]["ece"].append(ece_m["ece"])

    # Compute percentiles
    alpha = (1.0 - confidence_level) / 2.0
    q_low = alpha * 100
    q_high = (1.0 - alpha) * 100

    results: Dict[str, Dict[str, float]] = {}
    for jk in judge_keys:
        results[jk] = {}
        for m_name, vals in boot_metrics[jk].items():
            arr = np.array(vals)
            results[jk][f"{m_name}_mean"] = float(np.mean(arr))
            results[jk][f"{m_name}_ci_lower"] = float(np.percentile(arr, q_low))
            results[jk][f"{m_name}_ci_upper"] = float(np.percentile(arr, q_high))
            results[jk][f"{m_name}_std"] = float(np.std(arr))

    return results
