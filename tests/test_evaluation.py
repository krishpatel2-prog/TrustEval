"""Unit tests for TrustEval evaluation, ensembling, calibration, and disagreement modules."""

import numpy as np
import pandas as pd
import pytest

from trusteval.evaluation.ensemble import build_two_judge_ensemble
from trusteval.evaluation.metrics import (
    calculate_regression_metrics,
    calculate_expected_calibration_error,
    compute_reliability_curve,
)
from trusteval.evaluation.disagreement import analyze_disagreement_predictive_power
from trusteval.evaluation.bootstrap import bootstrap_raters_and_evaluate


def test_build_two_judge_ensemble():
    q_df = pd.DataFrame({
        "item_id": [1, 2, 3],
        "conditional_p_yes": [0.8, 0.4, 0.9],
    })
    s_df = pd.DataFrame({
        "item_id": [1, 2, 3],
        "conditional_p_yes": [0.2, 0.6, 0.3],
    })
    conv_df = pd.DataFrame({
        "item_id": [1, 2, 3],
        "response_char_length": [100, 200, 300],
    })
    tgt_df = pd.DataFrame({
        "item_id": [1, 2, 3],
        "h_primary": [0.5, 0.5, 0.6],
    })

    ens = build_two_judge_ensemble(q_df, s_df, conversations=conv_df, human_targets=tgt_df)
    assert len(ens) == 3
    assert np.allclose(ens["p_ensemble"], [0.5, 0.5, 0.6])
    assert np.allclose(ens["disagreement"], [0.6, 0.2, 0.6])
    assert "response_char_length" in ens.columns
    assert "h_primary" in ens.columns


def test_calculate_regression_metrics():
    preds = np.array([0.5, 0.8, 0.2])
    tgts = np.array([0.5, 0.6, 0.4])
    m = calculate_regression_metrics(preds, tgts)
    # Residuals: [0.0, 0.2, -0.2]
    # MAE: (0 + 0.2 + 0.2) / 3 = 0.4 / 3 = 0.133333
    # MSE: (0 + 0.04 + 0.04) / 3 = 0.08 / 3 = 0.0266667
    assert pytest.approx(m["mae"], abs=1e-5) == 0.4 / 3.0
    assert pytest.approx(m["brier_score"], abs=1e-5) == 0.08 / 3.0
    assert pytest.approx(m["rmse"], abs=1e-5) == np.sqrt(0.08 / 3.0)


def test_calculate_expected_calibration_error():
    # Perfectly calibrated
    preds = np.array([0.1, 0.1, 0.9, 0.9])
    tgts = np.array([0.1, 0.1, 0.9, 0.9])
    ece_m = calculate_expected_calibration_error(preds, tgts, n_bins=10)
    assert pytest.approx(ece_m["ece"], abs=1e-5) == 0.0
    assert pytest.approx(ece_m["mce"], abs=1e-5) == 0.0


def test_compute_reliability_curve():
    preds = np.array([0.05, 0.15, 0.85, 0.95])
    tgts = np.array([0.1, 0.2, 0.8, 0.9])
    bins = compute_reliability_curve(preds, tgts, n_bins=10)
    assert len(bins) == 10
    assert bins[0]["count"] == 1
    assert bins[1]["count"] == 1


def test_analyze_disagreement_predictive_power():
    rng = np.random.default_rng(42)
    n = 100
    p_ens = rng.uniform(0.1, 0.9, size=n)
    disagree = rng.uniform(0.0, 0.8, size=n)
    length = rng.integers(50, 500, size=n)
    # True error depends positively on disagreement
    abs_err = 0.05 + 0.3 * disagree + 0.02 * p_ens + rng.normal(0, 0.02, size=n)
    # Back-calculate target
    h_prim = np.clip(p_ens + abs_err, 0.0, 1.0)

    df = pd.DataFrame({
        "p_ensemble": p_ens,
        "disagreement": disagree,
        "response_char_length": length,
        "h_primary": h_prim,
    })

    res = analyze_disagreement_predictive_power(df, n_splits=5)
    assert res["n_samples"] == 100
    assert res["pearson_r"] > 0.0
    assert res["delta_r2_in_sample"] > 0.0
    assert "delta_r2_oof" in res


def test_bootstrap_raters_and_evaluate():
    # Synthetic annotations across 5 raters and 4 items
    annos = []
    raters = ["r1", "r2", "r3", "r4", "r5"]
    for r in raters:
        for itm in [1, 2, 3, 4]:
            annos.append({
                "rater_id": r,
                "item_id": itm,
                "Q_overall": "Yes" if (itm % 2 == 0) else "No",
            })
    annos_df = pd.DataFrame(annos)

    preds_df = pd.DataFrame({
        "item_id": [1, 2, 3, 4],
        "p_qwen": [0.2, 0.8, 0.3, 0.7],
        "p_smollm": [0.1, 0.9, 0.2, 0.8],
        "p_ensemble": [0.15, 0.85, 0.25, 0.75],
    })

    boot_res = bootstrap_raters_and_evaluate(
        annos_df,
        preds_df,
        n_resamples=50,
        seed=42,
    )

    assert "p_qwen" in boot_res
    assert "p_ensemble" in boot_res
    assert "mae_mean" in boot_res["p_ensemble"]
    assert "mae_ci_lower" in boot_res["p_ensemble"]
    assert "mae_ci_upper" in boot_res["p_ensemble"]
    assert boot_res["p_ensemble"]["mae_ci_lower"] <= boot_res["p_ensemble"]["mae_ci_upper"]
