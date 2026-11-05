"""Disagreement predictive analysis for TrustEval ensemble error."""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold


def analyze_disagreement_predictive_power(
    df: pd.DataFrame,
    target_col: str = "h_primary",
    length_col: str = "response_char_length",
    n_splits: int = 5,
    seed: int = 20261103,
) -> Dict[str, float]:
    """Test whether judge disagreement predicts ensemble error beyond baseline features.

    Parameters
    ----------
    df : pd.DataFrame
        Ensemble dataframe containing:
        - `p_ensemble`
        - `disagreement`
        - `target_col` (e.g. 'h_primary')
        - `length_col` (e.g. 'response_char_length')
    target_col : str, default='h_primary'
        Human rating ground truth column.
    length_col : str, default='response_char_length'
        Response length control feature column.
    n_splits : int, default=5
        Number of cross-validation folds.
    seed : int, default=20261103
        Random seed for fold splitting.

    Returns
    -------
    Dict[str, float]
        Statistical test results and cross-validated predictive metrics.
    """
    clean = df.dropna(subset=["p_ensemble", "disagreement", target_col, length_col]).copy()
    n = len(clean)

    if n < 20:
        raise ValueError(f"Insufficient sample size for regression analysis (n={n}).")

    # Absolute ensemble error against human ratings
    clean["abs_error"] = np.abs(clean["p_ensemble"] - clean[target_col])

    # 1. Bivariate correlations between disagreement and error
    r_pearson, p_pearson = stats.pearsonr(clean["disagreement"], clean["abs_error"])
    rho_spearman, p_spearman = stats.spearmanr(clean["disagreement"], clean["abs_error"])

    # Feature sets
    X_base = clean[["p_ensemble", length_col]].values
    X_ext = clean[["p_ensemble", length_col, "disagreement"]].values
    y = clean["abs_error"].values

    # 2. In-sample Ordinary Least Squares (OLS)
    lr_base = LinearRegression().fit(X_base, y)
    r2_base_in = float(lr_base.score(X_base, y))

    lr_ext = LinearRegression().fit(X_ext, y)
    r2_ext_in = float(lr_ext.score(X_ext, y))
    delta_r2_in = r2_ext_in - r2_base_in

    # F-test for incremental R-squared
    p_base = X_base.shape[1]
    p_ext = X_ext.shape[1]
    df1 = p_ext - p_base  # 1
    df2 = n - p_ext - 1
    f_stat = ((r2_ext_in - r2_base_in) / df1) / ((1.0 - r2_ext_in) / df2) if r2_ext_in < 1.0 else 0.0
    f_pvalue = float(stats.f.sf(f_stat, df1, df2))

    # 3. 5-Fold Cross-Validation for Out-of-Fold Predictive Comparison
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    oof_pred_base = np.zeros(n)
    oof_pred_ext = np.zeros(n)

    for train_idx, test_idx in kf.split(X_base):
        m_b = LinearRegression().fit(X_base[train_idx], y[train_idx])
        oof_pred_base[test_idx] = m_b.predict(X_base[test_idx])

        m_e = LinearRegression().fit(X_ext[train_idx], y[train_idx])
        oof_pred_ext[test_idx] = m_e.predict(X_ext[test_idx])

    # Out-of-fold R^2
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2_base_oof = float(1.0 - (np.sum((y - oof_pred_base) ** 2) / ss_tot))
    r2_ext_oof = float(1.0 - (np.sum((y - oof_pred_ext) ** 2) / ss_tot))
    delta_r2_oof = r2_ext_oof - r2_base_oof

    return {
        "n_samples": n,
        "pearson_r": float(r_pearson),
        "pearson_pvalue": float(p_pearson),
        "spearman_rho": float(rho_spearman),
        "spearman_pvalue": float(p_spearman),
        "r2_baseline_in_sample": r2_base_in,
        "r2_extended_in_sample": r2_ext_in,
        "delta_r2_in_sample": delta_r2_in,
        "f_statistic": float(f_stat),
        "f_pvalue": f_pvalue,
        "r2_baseline_oof": r2_base_oof,
        "r2_extended_oof": r2_ext_oof,
        "delta_r2_oof": delta_r2_oof,
        "disagreement_coef": float(lr_ext.coef_[2]),
    }
