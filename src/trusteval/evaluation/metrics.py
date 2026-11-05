"""Performance, calibration, and alignment metrics for safety judge evaluation."""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def calculate_regression_metrics(predictions: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
    """Calculate standard error metrics between predicted probabilities and human targets.

    Parameters
    ----------
    predictions : np.ndarray
        Model predicted probabilities in [0, 1].
    targets : np.ndarray
        Human safety proportions in [0, 1].

    Returns
    -------
    Dict[str, float]
        Dictionary with 'mae', 'rmse', and 'brier_score'.
    """
    p = np.asarray(predictions, dtype=np.float64)
    y = np.asarray(targets, dtype=np.float64)

    if len(p) != len(y):
        raise ValueError(f"Length mismatch: {len(p)} predictions vs {len(y)} targets.")

    residuals = p - y
    mae = float(np.mean(np.abs(residuals)))
    mse = float(np.mean(residuals ** 2))
    rmse = float(np.sqrt(mse))

    return {
        "mae": mae,
        "rmse": rmse,
        "brier_score": mse,
    }


def calculate_expected_calibration_error(
    predictions: np.ndarray,
    targets: np.ndarray,
    n_bins: int = 10,
) -> Dict[str, float]:
    """Calculate Expected Calibration Error (ECE) and Maximum Calibration Error (MCE).

    Parameters
    ----------
    predictions : np.ndarray
        Model predicted probabilities in [0, 1].
    targets : np.ndarray
        Human ground truth proportions in [0, 1].
    n_bins : int, default=10
        Number of equal-width bins over [0, 1].

    Returns
    -------
    Dict[str, float]
        Dictionary with 'ece', 'mce', and 'n_populated_bins'.
    """
    p = np.asarray(predictions, dtype=np.float64)
    y = np.asarray(targets, dtype=np.float64)
    n = len(p)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    # Right-inclusive on the last bin
    bin_indices = np.digitize(p, bin_edges[1:-1])

    ece = 0.0
    mce = 0.0
    populated = 0

    for b in range(n_bins):
        mask = bin_indices == b
        bin_count = int(np.sum(mask))
        if bin_count == 0:
            continue

        populated += 1
        bin_conf = float(np.mean(p[mask]))
        bin_acc = float(np.mean(y[mask]))
        abs_diff = abs(bin_acc - bin_conf)

        ece += (bin_count / n) * abs_diff
        if abs_diff > mce:
            mce = abs_diff

    return {
        "ece": float(ece),
        "mce": float(mce),
        "n_populated_bins": populated,
    }


def compute_reliability_curve(
    predictions: np.ndarray,
    targets: np.ndarray,
    n_bins: int = 10,
) -> List[Dict[str, float]]:
    """Generate reliability curve bin-level diagnostics.

    Parameters
    ----------
    predictions : np.ndarray
        Model predicted probabilities in [0, 1].
    targets : np.ndarray
        Human ground truth proportions in [0, 1].
    n_bins : int, default=10
        Number of bins.

    Returns
    -------
    List[Dict[str, float]]
        List of bin records with 'bin_start', 'bin_end', 'mean_confidence',
        'mean_target', 'count'.
    """
    p = np.asarray(predictions, dtype=np.float64)
    y = np.asarray(targets, dtype=np.float64)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_indices = np.digitize(p, bin_edges[1:-1])

    bins = []
    for b in range(n_bins):
        mask = bin_indices == b
        count = int(np.sum(mask))
        if count > 0:
            mean_conf = float(np.mean(p[mask]))
            mean_target = float(np.mean(y[mask]))
        else:
            mean_conf = float(0.5 * (bin_edges[b] + bin_edges[b + 1]))
            mean_target = np.nan

        bins.append({
            "bin": b,
            "bin_start": float(bin_edges[b]),
            "bin_end": float(bin_edges[b + 1]),
            "mean_confidence": mean_conf,
            "mean_target": mean_target,
            "count": count,
        })

    return bins
