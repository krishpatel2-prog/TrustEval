"""Generate Figure 1: Evaluator Paradigm and Trade-offs (Page 1 Teaser) - Revised."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

# Publication typography setup (IEEE Conference style)
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 7.5,
    "axes.labelsize": 7.5,
    "axes.titlesize": 8.0,
    "xtick.labelsize": 6.8,
    "ytick.labelsize": 6.8,
    "legend.fontsize": 6.5,
    "figure.titlesize": 8.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

def make_fig1():
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir.parent
    data_path = Path("D:/Research/TrustEval/results/tables/ensemble_predictions_dices50.csv")

    df = pd.read_csv(data_path)

    # 3.5 in wide x 3.6 in high (standard IEEE single column teaser with proper spacing)
    fig = plt.figure(figsize=(3.5, 3.6), facecolor="white")
    gs = gridspec.GridSpec(4, 1, height_ratios=[1.15, 0.78, 0.78, 0.95], hspace=0.42,
                           left=0.03, right=0.97, top=0.96, bottom=0.06)

    # Colors
    c_qwen = "#1f77b4"     # Steel blue
    c_smol = "#d95f02"     # Amber / orange
    c_ens = "#2ca02c"      # Forest green
    c_human = "#4a4a4a"    # Charcoal gray

    # Panel 0: Empirical Distribution Strip Comparison
    ax0 = fig.add_subplot(gs[0])
    ax0.set_facecolor("#ffffff")
    for spine in ["top", "right", "left"]:
        ax0.spines[spine].set_visible(False)
    ax0.spines["bottom"].set_color("#888888")
    ax0.spines["bottom"].set_linewidth(0.6)

    # Plot horizontal jittered points
    np.random.seed(42)
    y_human = 3.0 + np.random.normal(0, 0.05, len(df))
    y_qwen = 2.0 + np.random.normal(0, 0.05, len(df))
    y_smol = 1.0 + np.random.normal(0, 0.05, len(df))
    y_ens = 0.0 + np.random.normal(0, 0.05, len(df))

    ax0.scatter(df["h_primary"], y_human, color=c_human, alpha=0.35, s=7, edgecolors="none")
    ax0.scatter(df["p_qwen"], y_qwen, color=c_qwen, alpha=0.35, s=7, edgecolors="none")
    ax0.scatter(df["p_smollm"], y_smol, color=c_smol, alpha=0.35, s=7, edgecolors="none")
    ax0.scatter(df["p_ensemble"], y_ens, color=c_ens, alpha=0.45, s=7, edgecolors="none")

    # Plot means
    means = [
        (df["h_primary"].mean(), 3.0, c_human),
        (df["p_qwen"].mean(), 2.0, c_qwen),
        (df["p_smollm"].mean(), 1.0, c_smol),
        (df["p_ensemble"].mean(), 0.0, c_ens),
    ]
    for m, y_pos, col in means:
        ax0.plot([m, m], [y_pos - 0.22, y_pos + 0.22], color=col, linewidth=1.8, solid_capstyle="round")

    ax0.set_yticks([0.0, 1.0, 2.0, 3.0])
    ax0.set_yticklabels(["Ensemble", "SmolLM2", "Qwen", "Human"], fontsize=6.8, fontweight="medium")
    ax0.set_xlim(-0.02, 1.02)
    ax0.set_xlabel("Predicted Probability $P(\\mathrm{unsafe})$ vs. Human Target $h_{\\mathrm{primary}}$", fontsize=6.8, labelpad=3)
    ax0.tick_params(axis="y", length=0, pad=2)
    ax0.tick_params(axis="x", labelsize=6.5, length=2)

    # Panel 1: Qwen Card
    ax1 = fig.add_subplot(gs[1])
    ax1.set_facecolor("#f4f7fb")
    for spine in ax1.spines.values():
        spine.set_color("#c2d4e7")
        spine.set_linewidth(0.6)
    ax1.text(0.03, 0.70, "A. Qwen2.5-0.5B: Highest Judge Ranking Acuity",
             fontsize=7.0, fontweight="bold", color=c_qwen, transform=ax1.transAxes)
    ax1.text(0.03, 0.22, "• AUROC: 0.7529, $\\rho$: 0.5680  |  Overprediction: $\\mu=0.751$ vs. $0.338$ (MAE: 0.4152)",
             fontsize=6.4, color="#1c2833", transform=ax1.transAxes)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Panel 2: SmolLM2 Card
    ax2 = fig.add_subplot(gs[2])
    ax2.set_facecolor("#fdf7f2")
    for spine in ax2.spines.values():
        spine.set_color("#fadbd8")
        spine.set_linewidth(0.6)
    ax2.text(0.03, 0.70, "B. SmolLM2-1.7B: Lowest Judge Absolute Error",
             fontsize=7.0, fontweight="bold", color=c_smol, transform=ax2.transAxes)
    ax2.text(0.03, 0.22, "• Lowest Judge MAE: 0.1734  |  Low Variance Anchor: $\\mu=0.253, \\sigma=0.028$ (AUROC: 0.6690)",
             fontsize=6.4, color="#1c2833", transform=ax2.transAxes)
    ax2.set_xticks([])
    ax2.set_yticks([])

    # Panel 3: Ensemble Card & Trade-off
    ax3 = fig.add_subplot(gs[3])
    ax3.set_facecolor("#f2f8f2")
    for spine in ax3.spines.values():
        spine.set_color("#c8e6c9")
        spine.set_linewidth(0.6)
    ax3.text(0.03, 0.72, "C. Two-Judge Ensemble: Peak Rank Concordance & Trade-Offs",
             fontsize=7.0, fontweight="bold", color=c_ens, transform=ax3.transAxes)
    ax3.text(0.03, 0.40, "• Highest Rank Correlation: Spearman $\\rho = 0.5903$, Pearson $r = 0.4992$",
             fontsize=6.4, color="#1b5e20", fontweight="medium", transform=ax3.transAxes)
    ax3.text(0.03, 0.12, "• MAE 0.2464 (-40.6% vs Qwen); Held-out baseline retains lower Soft MSE (0.0602)",
             fontsize=6.2, color="#333333", transform=ax3.transAxes)
    ax3.set_xticks([])
    ax3.set_yticks([])

    pdf_path = out_dir / "fig1_teaser.pdf"
    png_path = out_dir / "fig1_teaser.png"

    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Figure 1 successfully regenerated:\n  PDF: {pdf_path}\n  PNG: {png_path}")

if __name__ == "__main__":
    make_fig1()
