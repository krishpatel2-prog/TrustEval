"""Phase 3C Statistical Analysis & Verification Script for TrustEval."""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import torch
import transformers

PROJECT_ROOT = Path("D:/Research/TrustEval")
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# 1. Environment specs
env_info = {
    "python_version": sys.version,
    "pytorch_version": torch.__version__,
    "transformers_version": transformers.__version__,
    "platform": sys.platform,
}

# 2. Load dataset
ens_df = pd.read_csv(PROJECT_ROOT / "results/tables/ensemble_predictions_dices50.csv")
h_prim = ens_df["h_primary"].values

err_q = np.abs(ens_df["p_qwen"].values - h_prim)
err_s = np.abs(ens_df["p_smollm"].values - h_prim)
err_e = np.abs(ens_df["p_ensemble"].values - h_prim)

sq_err_q = (ens_df["p_qwen"].values - h_prim) ** 2
sq_err_s = (ens_df["p_smollm"].values - h_prim) ** 2
sq_err_e = (ens_df["p_ensemble"].values - h_prim) ** 2

# Paired MAE difference: SmolLM2 - Ensemble
diff_mae_se = err_s - err_e
diff_mae_qe = err_q - err_e
diff_mae_qs = err_q - err_s

diff_mse_se = sq_err_s - sq_err_e
diff_mse_qe = sq_err_q - sq_err_e
diff_mse_qs = sq_err_q - sq_err_s

# Sign test
n_pos_se = int(np.sum(diff_mae_se > 0))
n_neg_se = int(np.sum(diff_mae_se < 0))
n_zero_se = int(np.sum(diff_mae_se == 0))
n_total_se = n_pos_se + n_neg_se
# Binomial test against p=0.5
sign_test_p_se = float(stats.binomtest(min(n_pos_se, n_neg_se), n_total_se, 0.5).pvalue)

# Effect sizes: Cohen's d_z = mean(diff) / std(diff, ddof=1)
def cohens_dz(diff):
    return float(np.mean(diff) / np.std(diff, ddof=1))

# Wilcoxon effect size r = Z / sqrt(N)
def wilcoxon_r(w_stat, n):
    # Mean of W = n*(n+1)/4, variance = n*(n+1)*(2n+1)/24
    mean_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0
    z = (w_stat - mean_w) / np.sqrt(var_w)
    return float(z / np.sqrt(n)), float(z)

w_se, p_w_se = stats.wilcoxon(diff_mae_se, zero_method="wilcox")
r_w_se, z_w_se = wilcoxon_r(w_se, len(diff_mae_se))

w_qe, p_w_qe = stats.wilcoxon(diff_mae_qe, zero_method="wilcox")
r_w_qe, z_w_qe = wilcoxon_r(w_qe, len(diff_mae_qe))

# Paired bootstrap for MAE difference (2,000 resamples)
rng = np.random.default_rng(20261103)
n_boot = 2000
boot_diff_se = []
boot_diff_qe = []
boot_diff_mse_se = []
boot_diff_mse_qe = []

for _ in range(n_boot):
    b_idx = rng.integers(0, len(ens_df), size=len(ens_df))
    boot_diff_se.append(np.mean(diff_mae_se[b_idx]))
    boot_diff_qe.append(np.mean(diff_mae_qe[b_idx]))
    boot_diff_mse_se.append(np.mean(diff_mse_se[b_idx]))
    boot_diff_mse_qe.append(np.mean(diff_mse_qe[b_idx]))

def boot_ci(arr):
    return [float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))]

# 3. Rater-Cluster Bootstrap Paired Differences
# Run rater bootstrap and record paired differences across same replicates
config_file = PROJECT_ROOT / "configs/experiment.yaml"
import yaml
with open(config_file, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

raw_path = PROJECT_ROOT / cfg["dataset"]["raw_file"]
raw_df = pd.read_csv(raw_path)
removed_raters = set(str(r).strip() for r in cfg["dataset"]["removed_raters"])
raw_df["rater_id"] = raw_df["rater_id"].astype(str).str.strip()
raw_df = raw_df[~raw_df["rater_id"].isin(removed_raters)].copy()

sampled_item_ids = set(ens_df["item_id"].tolist())
raw_df_50 = raw_df[raw_df["item_id"].isin(sampled_item_ids)].copy()

raters = np.array(sorted(raw_df_50["rater_id"].unique()))
n_raters = len(raters)
rater_groups = {
    r_id: grp[["item_id", "Q_overall"]].copy()
    for r_id, grp in raw_df_50.groupby("rater_id")
}
item_order = ens_df["item_id"].values

p_q = ens_df["p_qwen"].values
p_s = ens_df["p_smollm"].values
p_e = ens_df["p_ensemble"].values

rater_boot_diff_mae_qe = []
rater_boot_diff_mae_se = []
rater_boot_diff_mse_qe = []
rater_boot_diff_mse_se = []

rng_rater = np.random.default_rng(cfg["experiment"]["seed"])
for b in range(1000):
    s_idx = rng_rater.integers(0, n_raters, size=n_raters)
    s_raters = raters[s_idx]
    s_annos = pd.concat([rater_groups[r] for r in s_raters], ignore_index=True)
    counts = s_annos.groupby(["item_id", "Q_overall"]).size().unstack(fill_value=0)
    col_y = "Yes" if "Yes" in counts.columns else None
    col_n = "No" if "No" in counts.columns else None
    if col_y is None and col_n is None:
        continue
    c_yes = counts[col_y] if col_y in counts.columns else pd.Series(0, index=counts.index)
    c_no = counts[col_n] if col_n in counts.columns else pd.Series(0, index=counts.index)
    denom = c_yes + c_no
    h_boot = np.where(denom > 0, c_yes / np.maximum(denom, 1), 0.5)
    h_boot_series = pd.Series(h_boot, index=counts.index)
    aligned_h = h_boot_series.reindex(item_order).fillna(0.5).values

    mae_q = np.mean(np.abs(p_q - aligned_h))
    mae_s = np.mean(np.abs(p_s - aligned_h))
    mae_e = np.mean(np.abs(p_e - aligned_h))

    mse_q = np.mean((p_q - aligned_h) ** 2)
    mse_s = np.mean((p_s - aligned_h) ** 2)
    mse_e = np.mean((p_e - aligned_h) ** 2)

    rater_boot_diff_mae_qe.append(mae_q - mae_e)
    rater_boot_diff_mae_se.append(mae_s - mae_e)
    rater_boot_diff_mse_qe.append(mse_q - mse_e)
    rater_boot_diff_mse_se.append(mse_s - mse_e)

out_data = {
    "environment": env_info,
    "smollm_vs_ensemble_mae": {
        "mean_diff": float(np.mean(diff_mae_se)),
        "cohens_dz": cohens_dz(diff_mae_se),
        "t_stat": float(stats.ttest_rel(err_s, err_e).statistic),
        "t_pval_unadj": float(stats.ttest_rel(err_s, err_e).pvalue),
        "t_pval_holm_m6": float(stats.ttest_rel(err_s, err_e).pvalue * 2),
        "wilcoxon_stat": float(w_se),
        "wilcoxon_z": z_w_se,
        "wilcoxon_r": r_w_se,
        "wilcoxon_pval_unadj": float(p_w_se),
        "wilcoxon_pval_holm_m6": float(p_w_se * 2),
        "sign_test": {
            "n_smollm_better": n_neg_se,
            "n_ensemble_better": n_pos_se,
            "n_ties": n_zero_se,
            "pvalue": sign_test_p_se,
        },
        "item_bootstrap_2000_95ci": boot_ci(boot_diff_se),
        "rater_bootstrap_1000_mean": float(np.mean(rater_boot_diff_mae_se)),
        "rater_bootstrap_1000_95ci": boot_ci(rater_boot_diff_mae_se),
    },
    "qwen_vs_ensemble_mae": {
        "mean_diff": float(np.mean(diff_mae_qe)),
        "cohens_dz": cohens_dz(diff_mae_qe),
        "t_stat": float(stats.ttest_rel(err_q, err_e).statistic),
        "t_pval_unadj": float(stats.ttest_rel(err_q, err_e).pvalue),
        "t_pval_holm_m6": float(stats.ttest_rel(err_q, err_e).pvalue * 6),
        "wilcoxon_stat": float(w_qe),
        "wilcoxon_z": z_w_qe,
        "wilcoxon_r": r_w_qe,
        "wilcoxon_pval_unadj": float(p_w_qe),
        "wilcoxon_pval_holm_m6": float(p_w_qe * 5),
        "item_bootstrap_2000_95ci": boot_ci(boot_diff_qe),
        "rater_bootstrap_1000_mean": float(np.mean(rater_boot_diff_mae_qe)),
        "rater_bootstrap_1000_95ci": boot_ci(rater_boot_diff_mae_qe),
    },
    "smollm_vs_ensemble_mse": {
        "mean_diff": float(np.mean(diff_mse_se)),
        "cohens_dz": cohens_dz(diff_mse_se),
        "t_stat": float(stats.ttest_rel(sq_err_s, sq_err_e).statistic),
        "t_pval_unadj": float(stats.ttest_rel(sq_err_s, sq_err_e).pvalue),
        "t_pval_holm_m6": float(stats.ttest_rel(sq_err_s, sq_err_e).pvalue * 1),
        "item_bootstrap_2000_95ci": boot_ci(boot_diff_mse_se),
        "rater_bootstrap_1000_mean": float(np.mean(rater_boot_diff_mse_se)),
        "rater_bootstrap_1000_95ci": boot_ci(rater_boot_diff_mse_se),
    },
    "qwen_vs_ensemble_mse": {
        "mean_diff": float(np.mean(diff_mse_qe)),
        "cohens_dz": cohens_dz(diff_mse_qe),
        "t_stat": float(stats.ttest_rel(sq_err_q, sq_err_e).statistic),
        "t_pval_unadj": float(stats.ttest_rel(sq_err_q, sq_err_e).pvalue),
        "t_pval_holm_m6": float(stats.ttest_rel(sq_err_q, sq_err_e).pvalue * 6),
        "item_bootstrap_2000_95ci": boot_ci(boot_diff_mse_qe),
        "rater_bootstrap_1000_mean": float(np.mean(rater_boot_diff_mse_qe)),
        "rater_bootstrap_1000_95ci": boot_ci(rater_boot_diff_mse_qe),
    },
}

out_file = PROJECT_ROOT / "results/diagnostics/phase_3c_statistical_refinements.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out_data, f, indent=2)

print("Saved Phase 3C statistical refinements to", out_file)
print(json.dumps(out_data, indent=2))
