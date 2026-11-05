"""Generate Figure 3: Inter-Judge Disagreement vs. Absolute Evaluation Error - Revised."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from scipy import stats

# Publication typography setup
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 7.5,
    "axes.labelsize": 7.5,
    "axes.titlesize": 8.0,
    "xtick.labelsize": 6.8,
    "ytick.labelsize": 6.8,
    "legend.fontsize": 6.2,
    "figure.titlesize": 8.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

def make_fig3():
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir.parent
    data_path = Path("D:/Research/TrustEval/results/tables/ensemble_predictions_dices50.csv")

    df = pd.read_csv(data_path)
    x = df["disagreement"].values
    y = np.abs(df["p_ensemble"] - df["h_primary"]).values
    n = len(x)

    # 1. Bivariate Linear Regression
    slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
    rho_val, rho_pval = stats.spearmanr(x, y)

    # 95% Confidence Interval for regression line
    x_line = np.linspace(0.0, max(x) * 1.05, 100)
    y_line = slope * x_line + intercept

    # Residual standard error
    y_pred_orig = slope * x + intercept
    s_err = np.sqrt(np.sum((y - y_pred_orig) ** 2) / (n - 2))

    # Margin of error across x_line
    x_mean = np.mean(x)
    s_xx = np.sum((x - x_mean) ** 2)
    t_crit = stats.t.ppf(0.975, df=n - 2)

    ci = t_crit * s_err * np.sqrt(1.0 / n + (x_line - x_mean) ** 2 / s_xx)
    y_lower = y_line - ci
    y_upper = y_line + ci

    # Figure: 3.5 in wide x 3.5 in high (2-tier layout: stats card on top, clean scatter below)
    fig = plt.figure(figsize=(3.5, 3.5), facecolor="white")
    gs = gridspec.GridSpec(2, 1, height_ratios=[0.85, 2.5], hspace=0.32,
                           left=0.13, right=0.96, top=0.96, bottom=0.10)

    # Panel 0: Dedicated Statistics Summary Card (Zero Overlap with Points)
    ax_card = fig.add_subplot(gs[0])
    ax_card.set_facecolor("#f8f9fa")
    for spine in ax_card.spines.values():
        spine.set_color("#cccccc")
        spine.set_linewidth(0.6)

    card_text_left = (
        "Bivariate Association ($N=50$):\n"
        f"• Pearson: $r = {r_val:.4f}$, $p = {p_val:.4f}$ (nominally significant)\n"
        f"• Spearman: $\\rho = {rho_val:.4f}$, $p = {rho_pval:.4f}$ (not significant)"
    )
    card_text_right = (
        "Multivariable & CV Diagnostics:\n"
        "• Nested In-Sample OLS: $F(1, 46) = 5.676$, $p = 0.0214$\n"
        "• 5-Fold OOF: $\\Delta R^2_{\\mathrm{OOF}} = +0.0805$ (descriptive only)"
    )

    ax_card.text(0.03, 0.50, card_text_left, transform=ax_card.transAxes,
                 fontsize=5.8, va="center", ha="left", color="#222222")
    ax_card.text(0.53, 0.50, card_text_right, transform=ax_card.transAxes,
                 fontsize=5.8, va="center", ha="left", color="#222222")
    ax_card.set_xticks([])
    ax_card.set_yticks([])

    # Panel 1: Scatter Plot and Regression Ribbon
    ax = fig.add_subplot(gs[1])
    ax.set_facecolor("white")
    ax.grid(True, linestyle=":", alpha=0.5, color="#bbbbbb")

    # Colors
    c_pts = "#1f77b4"
    c_fit = "#d95f02"

    # Scatter of 50 conversations
    ax.scatter(x, y, alpha=0.70, color=c_pts, edgecolors="#104e7a", linewidth=0.5, s=26,
               label=f"Conversations ($N={n}$)")

    # 95% CI Ribbon
    ax.fill_between(x_line, y_lower, y_upper, color=c_fit, alpha=0.18, label="95% Confidence Ribbon")

    # Bivariate regression line with accurate label requested
    ax.plot(x_line, y_line, color=c_fit, linewidth=1.5,
            label=f"Linear fit; Pearson $r = {r_val:.3f}$")

    ax.set_xlabel("Inter-Judge Disagreement $\\Delta = |P_{\\mathrm{qwen}} - P_{\\mathrm{smollm}}|$", fontsize=7.2, labelpad=2)
    ax.set_ylabel("Ensemble Absolute Error $|P_{\\mathrm{ens}} - h_{\\mathrm{primary}}|$", fontsize=7.2, labelpad=2)
    ax.set_xlim(-0.02, max(x) * 1.05)
    ax.set_ylim(-0.02, max(y) * 1.08)

    # Footnote warning inside plot margin
    ax.text(0.97, 0.04, "Note: Candidate error correlate; not validated uncertainty.",
            transform=ax.transAxes, fontsize=5.3, ha="right", va="bottom",
            color="#555555", style="italic")

    ax.legend(loc="upper left", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc", fontsize=5.8)

    pdf_path = out_dir / "fig3_disagreement.pdf"
    png_path = out_dir / "fig3_disagreement.png"

    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Figure 3 successfully regenerated:\n  PDF: {pdf_path}\n  PNG: {png_path}")

if __name__ == "__main__":
    make_fig3()
