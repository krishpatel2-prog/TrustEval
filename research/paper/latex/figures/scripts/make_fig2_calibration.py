"""Generate Figure 2: Reliability and Calibration Diagrams - Revised."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

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

def compute_bins(p, y, n_bins=10):
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

def make_fig2():
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir.parent
    data_path = Path("D:/Research/TrustEval/results/tables/ensemble_predictions_dices50.csv")

    df = pd.read_csv(data_path)

    # Colors matching academic visual system
    c_qwen = "#1f77b4"     # Steel blue
    c_smol = "#d95f02"     # Amber / orange
    c_ens = "#2ca02c"      # Forest green
    c_base = "#7570b3"     # Purple

    # Figure: 3.5 in wide x 3.8 in high
    fig = plt.figure(figsize=(3.5, 3.8), facecolor="white")
    gs = gridspec.GridSpec(2, 1, height_ratios=[2.2, 0.95], hspace=0.42,
                           left=0.13, right=0.96, top=0.95, bottom=0.10)

    # Subplot 1: Calibration Curves
    ax0 = fig.add_subplot(gs[0])
    ax0.set_facecolor("white")
    ax0.grid(True, linestyle=":", alpha=0.5, color="#bbbbbb")

    # Perfect calibration diagonal
    ax0.plot([0, 1], [0, 1], "k--", linewidth=1.0, alpha=0.6, label="Perfect Calibration ($y = x$)")

    # 1. Qwen bins (8 populated bins)
    qwen_bins = compute_bins(df["p_qwen"].values, df["h_primary"].values, n_bins=10)
    q_x = [b["mean_confidence"] for b in qwen_bins if b["count"] > 0]
    q_y = [b["mean_target"] for b in qwen_bins if b["count"] > 0]
    ax0.plot(q_x, q_y, marker="o", markersize=4, linewidth=1.4, color=c_qwen,
             label="Qwen2.5-0.5B (ECE = 0.413, 8 bins)")

    # 2. SmolLM2 bins (2 populated bins)
    smol_bins = compute_bins(df["p_smollm"].values, df["h_primary"].values, n_bins=10)
    s_x = [b["mean_confidence"] for b in smol_bins if b["count"] > 0]
    s_y = [b["mean_target"] for b in smol_bins if b["count"] > 0]
    ax0.plot(s_x, s_y, marker="s", markersize=4.5, linewidth=1.4, color=c_smol,
             label="SmolLM2-1.7B (ECE = 0.085, 2 bins)")

    # 3. Ensemble bins (6 populated bins)
    ens_bins = compute_bins(df["p_ensemble"].values, df["h_primary"].values, n_bins=10)
    e_x = [b["mean_confidence"] for b in ens_bins if b["count"] > 0]
    e_y = [b["mean_target"] for b in ens_bins if b["count"] > 0]
    ax0.plot(e_x, e_y, marker="^", markersize=4.5, linewidth=1.6, color=c_ens,
             label="Two-Judge Ensemble (ECE = 0.164, 6 bins)")

    # 4. Prevalence Baseline: SINGLE-BIN ISOLATED POINT
    mean_h = df["h_primary"].mean()
    ax0.scatter([mean_h], [mean_h], marker="*", s=120, color=c_base, edgecolors="#222222",
                linewidth=0.8, zorder=5, label="Prevalence Baseline ($0.0000^*$, 1 bin)")

    # Legend placed in EMPTY upper-left region to strictly avoid covering observations
    ax0.legend(loc="upper left", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc", fontsize=5.8)

    # Footnote / annotation explicitly explaining coarse single-bin baseline
    ax0.text(0.97, 0.05,
             "Note: The baseline occupies one calibration bin;\n"
             "ECE = 0.0000 is a coarse one-bin aggregation\n"
             "result and does not establish reliable calibration.",
             transform=ax0.transAxes, fontsize=5.4, ha="right", va="bottom",
             bbox=dict(boxstyle="round,pad=0.25", facecolor="#fbf9fd", edgecolor=c_base, lw=0.5))

    ax0.set_xlim(-0.02, 1.02)
    ax0.set_ylim(-0.02, 1.02)
    ax0.set_xlabel("Mean Predicted Probability (Decile Bins)", fontsize=7.2, labelpad=2)
    ax0.set_ylabel("Empirical Human Target ($h_{\\mathrm{primary}}$)", fontsize=7.2, labelpad=2)

    # Subplot 2: Decile Sample Occupancy Panel
    ax1 = fig.add_subplot(gs[1])
    ax1.set_facecolor("white")
    ax1.grid(True, linestyle=":", alpha=0.4, color="#bbbbbb", axis="y")

    bin_centers = np.arange(10)
    w = 0.22

    q_counts = [b["count"] for b in qwen_bins]
    s_counts = [b["count"] for b in smol_bins]
    e_counts = [b["count"] for b in ens_bins]

    ax1.bar(bin_centers - w, q_counts, width=w, color=c_qwen, alpha=0.85, label="Qwen (8 bins)")
    ax1.bar(bin_centers, s_counts, width=w, color=c_smol, alpha=0.85, label="SmolLM2 (2 bins)")
    ax1.bar(bin_centers + w, e_counts, width=w, color=c_ens, alpha=0.85, label="Ensemble (6 bins)")

    ax1.set_xlim(-0.6, 9.6)
    ax1.set_xticks(bin_centers)
    ax1.set_xticklabels([f"{i/10:.1f}" for i in range(10)], fontsize=6.2)
    ax1.set_xlabel("Calibration Bin Starting Probability", fontsize=6.8, labelpad=1)
    ax1.set_ylabel("Count ($N=50$)", fontsize=6.8, labelpad=2)
    ax1.legend(loc="upper right", frameon=True, framealpha=0.9, facecolor="white", edgecolor="#cccccc", fontsize=5.5, ncol=3)

    pdf_path = out_dir / "fig2_calibration.pdf"
    png_path = out_dir / "fig2_calibration.png"

    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Figure 2 successfully regenerated:\n  PDF: {pdf_path}\n  PNG: {png_path}")

if __name__ == "__main__":
    make_fig2()
