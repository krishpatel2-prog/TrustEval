"""Generate Figure 4: Prediction Distribution Alignment (Appendix F) - Revised."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
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

def make_fig4():
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir.parent
    data_path = Path("D:/Research/TrustEval/results/tables/ensemble_predictions_dices50.csv")

    df = pd.read_csv(data_path)

    # 3.5 in wide x 2.9 in high (single column appendix format)
    fig, ax = plt.subplots(figsize=(3.5, 2.9), facecolor="white")
    ax.grid(True, linestyle=":", alpha=0.5, color="#bbbbbb")

    # Colors
    c_qwen = "#1f77b4"     # Steel blue
    c_smol = "#d95f02"     # Amber / orange
    c_ens = "#2ca02c"      # Forest green
    c_human = "#4a4a4a"    # Charcoal / gray

    # 20 empirical bins spanning [0, 1] without artificial smoothing
    bins = np.linspace(0.0, 1.0, 21)

    # Empirical step density histograms
    ax.hist(df["h_primary"], bins=bins, density=True, alpha=0.25, color=c_human,
            edgecolor=c_human, linewidth=0.8, label="Human Target $h_{\\mathrm{primary}}$ (Ground Truth)")
    ax.hist(df["p_qwen"], bins=bins, density=True, histtype="step", linewidth=1.5,
            color=c_qwen, label="Qwen2.5-0.5B ($\\mu=0.751, \\sigma=0.186$)")
    ax.hist(df["p_smollm"], bins=bins, density=True, histtype="step", linewidth=1.5,
            color=c_smol, label="SmolLM2-1.7B ($\\mu=0.253, \\sigma=0.028$)")
    ax.hist(df["p_ensemble"], bins=bins, density=True, histtype="step", linewidth=1.8,
            color=c_ens, label="Two-Judge Ensemble ($\\mu=0.502, \\sigma=0.097$)")

    ax.set_xlabel("Safety Rating Probability $P(\\mathrm{unsafe})$", fontsize=7.2, labelpad=2)
    ax.set_ylabel("Empirical Step Density ($N=50$)", fontsize=7.2, labelpad=2)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 18.0)

    # Clean 2-column legend to prevent any vertical crowding
    ax.legend(loc="upper right", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc",
              fontsize=5.6, ncol=1)

    plt.tight_layout()

    pdf_path = out_dir / "fig4_density.pdf"
    png_path = out_dir / "fig4_density.png"

    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Figure 4 successfully regenerated:\n  PDF: {pdf_path}\n  PNG: {png_path}")

if __name__ == "__main__":
    make_fig4()
