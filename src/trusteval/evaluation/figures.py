"""Publication-quality figure generation for TrustEval research paper."""

from pathlib import Path
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .metrics import compute_reliability_curve

# Publication style defaults
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
})


def plot_reliability_diagrams(
    ensemble_df: pd.DataFrame,
    output_path: Path | str,
    target_col: str = "h_primary",
    n_bins: int = 10,
) -> Path:
    """Generate side-by-side reliability diagrams comparing Qwen, SmolLM2, and Ensemble."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)

    models = [
        ("p_qwen", "Qwen2.5-0.5B-Instruct", "#1f77b4", axes[0]),
        ("p_smollm", "SmolLM2-1.7B-Instruct", "#ff7f0e", axes[1]),
        ("p_ensemble", "Two-Judge Ensemble (Equal Weight)", "#2ca02c", axes[2]),
    ]

    for col, title, color, ax in models:
        clean = ensemble_df.dropna(subset=[col, target_col])
        bins = compute_reliability_curve(clean[col].values, clean[target_col].values, n_bins=n_bins)

        confs = [b["mean_confidence"] for b in bins if not np.isnan(b["mean_target"])]
        accs = [b["mean_target"] for b in bins if not np.isnan(b["mean_target"])]

        # Diagonal reference
        ax.plot([0, 1], [0, 1], "k--", alpha=0.6, label="Perfect Calibration")
        ax.plot(confs, accs, marker="o", color=color, linewidth=2, label=f"Observed ({title.split()[0]})")

        ax.set_title(title, pad=10)
        ax.set_xlabel("Mean Predicted Probability")
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="upper left", frameon=True)

    axes[0].set_ylabel(f"Empirical Human Target ({target_col})")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    return out_file


def plot_disagreement_vs_error(
    ensemble_df: pd.DataFrame,
    output_path: Path | str,
    target_col: str = "h_primary",
) -> Path:
    """Generate scatter plot and regression line for judge disagreement vs absolute error."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    clean = ensemble_df.dropna(subset=["disagreement", "p_ensemble", target_col]).copy()
    clean["abs_error"] = np.abs(clean["p_ensemble"] - clean[target_col])

    x = clean["disagreement"].values
    y = clean["abs_error"].values

    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
    x_line = np.linspace(0, max(x) * 1.05, 100)
    y_line = slope * x_line + intercept

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.scatter(x, y, alpha=0.55, color="#1f77b4", edgecolors="none", s=35, label="Conversations")
    ax.plot(
        x_line,
        y_line,
        color="#d62728",
        linewidth=2,
        label=f"OLS Fit (r = {r_val:.3f}, p = {p_val:.3g})",
    )

    ax.set_xlabel("Judge Disagreement |P(Qwen) - P(SmolLM)|")
    ax.set_ylabel(f"Ensemble Absolute Error |P_ensemble - {target_col}|")
    ax.set_title("Disagreement vs. Evaluation Error", pad=10)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    return out_file


def plot_distribution_alignment(
    ensemble_df: pd.DataFrame,
    output_path: Path | str,
    target_col: str = "h_primary",
) -> Path:
    """Generate density histograms comparing model predictions against human rating distributions."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 4.5))

    clean = ensemble_df.dropna(subset=["p_qwen", "p_smollm", "p_ensemble", target_col])
    bins = np.linspace(0, 1, 21)

    ax.hist(clean[target_col], bins=bins, alpha=0.35, color="gray", density=True, label=f"Human Ground Truth ({target_col})")
    ax.hist(clean["p_qwen"], bins=bins, histtype="step", linewidth=1.8, color="#1f77b4", density=True, label="Qwen2.5-0.5B")
    ax.hist(clean["p_smollm"], bins=bins, histtype="step", linewidth=1.8, color="#ff7f0e", density=True, label="SmolLM2-1.7B")
    ax.hist(clean["p_ensemble"], bins=bins, histtype="step", linewidth=2.2, color="#2ca02c", density=True, label="Ensemble")

    ax.set_xlabel("Safety Rating Probability (Unsafe)")
    ax.set_ylabel("Empirical Density")
    ax.set_title("Distribution Alignment: AI Judges vs. Human Ratings", pad=10)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper center", frameon=True)

    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    return out_file
