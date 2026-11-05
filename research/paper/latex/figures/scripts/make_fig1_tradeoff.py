"""Generate Figure 1: Evaluator Polarization & Ensemble Trade-Off Frontier.

Restrained, publication-grade academic figure designed for IEEE Conference
single-column width (3.5 in). Implements verified empirical coordinates,
offset annotations, deterministic beeswarm stacking, and non-overlapping elements.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd


# Set IEEE Conference typography standards
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 7.0,
    "axes.labelsize": 7.0,
    "axes.titlesize": 7.5,
    "xtick.labelsize": 6.2,
    "ytick.labelsize": 6.2,
    "legend.fontsize": 6.0,
    "figure.titlesize": 7.8,
    "mathtext.fontset": "dejavuserif",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def beeswarm_vertical(x_vals, max_y=0.22, step=0.038, radius=0.010):
    """Compute deterministic vertical offsets for repeated or overlapping points.
    
    The original x-coordinates are never modified; displacement is purely visual.
    """
    n = len(x_vals)
    y_offsets = np.zeros(n)
    order = np.argsort(x_vals)

    for idx, orig_idx in enumerate(order):
        cand_y = 0.0
        placed_indices = order[:idx]
        while True:
            collision = False
            for p_idx in placed_indices:
                dx = abs(x_vals[orig_idx] - x_vals[p_idx])
                dy = abs(cand_y - y_offsets[p_idx])
                if dx < radius and dy < step * 0.95:
                    collision = True
                    break
            if not collision:
                y_offsets[orig_idx] = cand_y
                break
            cand_y = -cand_y if cand_y > 0 else -cand_y + step
            if abs(cand_y) > max_y:
                y_offsets[orig_idx] = np.clip(cand_y, -max_y, max_y)
                break
    return y_offsets


def make_fig1():
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir.parent
    data_path = Path("D:/Research/TrustEval/results/tables/ensemble_predictions_dices50.csv")

    df = pd.read_csv(data_path)

    # Palette
    c_qwen = "#1f77b4"     # Steel blue
    c_smol = "#d95f02"     # Amber orange
    c_ens = "#2ca02c"      # Forest green
    c_human = "#4a4a4a"    # Dark charcoal

    # Exact IEEE single-column width: 3.5 in wide by 4.0 in high
    fig = plt.figure(figsize=(3.5, 4.0), facecolor="white")

    # GridSpec: Panel A (top) and Panel B (bottom 4 strips)
    outer_gs = gridspec.GridSpec(
        2, 1,
        height_ratios=[1.15, 1.05],
        hspace=0.48,
        left=0.16, right=0.96, top=0.94, bottom=0.08
    )

    # ==========================================
    # PANEL A: Capability Trade-Off Plane
    # ==========================================
    ax_a = fig.add_subplot(outer_gs[0])
    ax_a.set_facecolor("#ffffff")
    ax_a.set_title("(a) Capability Trade-Off", fontsize=7.6, fontweight="bold", pad=5, loc="center")

    # Axis limits & ticks
    ax_a.set_xlim(0.14, 0.46)
    ax_a.set_ylim(0.62, 0.80)
    ax_a.set_xticks([0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45])
    ax_a.set_yticks([0.65, 0.70, 0.75, 0.80])

    ax_a.set_xlabel("Mean Absolute Error (MAE; lower is better)", fontsize=6.8, labelpad=2.5)
    ax_a.set_ylabel("AUROC (higher is better)", fontsize=6.8, labelpad=3.5)

    # Minimal light grid
    ax_a.grid(True, linestyle="-", linewidth=0.4, color="#eeeeee", alpha=0.9, zorder=0)

    # Verified coordinates:
    # SmolLM2: (0.1734, 0.6690)
    # Ensemble: (0.2464, 0.7517)
    # Qwen: (0.4152, 0.7529)
    models = [
        {
            "name": "SmolLM2-1.7B", "mae": 0.1734, "auroc": 0.6690, "color": c_smol,
            "xytext": (10, 2), "ha": "left", "va": "center"
        },
        {
            "name": "Two-Judge Ensemble", "mae": 0.2464, "auroc": 0.7517, "color": c_ens,
            "xytext": (0, 7), "ha": "center", "va": "bottom"
        },
        {
            "name": "Qwen2.5-0.5B", "mae": 0.4152, "auroc": 0.7529, "color": c_qwen,
            "xytext": (0, 7), "ha": "center", "va": "bottom"
        },
    ]

    annotations_a = []
    for m in models:
        # Scatter marker
        ax_a.scatter(
            m["mae"], m["auroc"],
            color=m["color"], s=38, zorder=4,
            edgecolors="#111111", linewidth=0.6
        )
        # Direct annotation using point offsets
        label_text = f"{m['name']}\n({m['mae']:.3f}, {m['auroc']:.3f})"
        ann = ax_a.annotate(
            label_text,
            xy=(m["mae"], m["auroc"]),
            xytext=m["xytext"],
            textcoords="offset points",
            ha=m["ha"], va=m["va"],
            fontsize=6.2, fontweight="bold",
            color="#111111", zorder=5
        )
        annotations_a.append(ann)

    # Prevalence Baseline Note (placed cleanly outside the plotting region, beneath Panel A)
    baseline_text = (
        "Contextual Baseline (held-out prevalence): MAE = 0.1983, RMSE = 0.2454, Soft MSE = 0.0602\n"
        "[Constant prediction; non-ranking baseline excluded from AUROC scatter]"
    )
    ax_a.text(
        0.50, -0.28,
        baseline_text,
        transform=ax_a.transAxes,
        fontsize=5.2, ha="center", va="top",
        color="#555555", fontstyle="italic"
    )

    # Spine styling for Panel A
    for spine in ax_a.spines.values():
        spine.set_color("#888888")
        spine.set_linewidth(0.5)

    # ==========================================
    # PANEL B: Empirical Prediction Distributions
    # ==========================================
    gs_b = gridspec.GridSpecFromSubplotSpec(
        4, 1, subplot_spec=outer_gs[1],
        hspace=0.20
    )

    strips_data = [
        {
            "label": "Human Target\n" + r"($h_{\mathrm{primary}}$)",
            "vals": df["h_primary"].values,
            "mean": 0.3381,
            "color": c_human,
        },
        {
            "label": "Qwen2.5-0.5B",
            "vals": df["p_qwen"].values,
            "mean": 0.7509,
            "color": c_qwen,
        },
        {
            "label": "SmolLM2-1.7B",
            "vals": df["p_smollm"].values,
            "mean": 0.2531,
            "color": c_smol,
        },
        {
            "label": "Two-Judge\nEnsemble",
            "vals": df["p_ensemble"].values,
            "mean": 0.5020,
            "color": c_ens,
        },
    ]

    axes_b = []
    for idx, s in enumerate(strips_data):
        ax = fig.add_subplot(gs_b[idx])
        axes_b.append(ax)
        ax.set_facecolor("#ffffff")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(-0.30, 0.30)

        # Subtle vertical grid lines at deciles
        for x_tick in [0.2, 0.4, 0.6, 0.8]:
            ax.axvline(x_tick, color="#f2f2f2", lw=0.5, zorder=0)

        # Deterministic vertical beeswarm offsets (original x-coordinates NEVER modified)
        y_jit = beeswarm_vertical(s["vals"])

        # Scatter plot of actual 50 observations
        ax.scatter(
            s["vals"], y_jit,
            color=s["color"], s=16, alpha=0.65,
            edgecolors=s["color"], linewidth=0.3, zorder=3
        )

        # Thin vertical mean marker
        ax.plot([s["mean"], s["mean"]], [-0.24, 0.24], color="#111111", lw=0.9, zorder=4)

        # Exactly one mean label per strip
        ax.text(
            s["mean"], 0.26,
            rf"$\mu = {s['mean']:.3f}$",
            fontsize=5.2, ha="center", va="bottom",
            color="#111111", zorder=5
        )

        # Y-axis label (model name)
        ax.set_ylabel(s["label"], fontsize=6.0, rotation=0, ha="right", va="center", labelpad=5)
        ax.set_yticks([])

        # Spine styling
        for spine in ax.spines.values():
            spine.set_color("#888888")
            spine.set_linewidth(0.5)

        # X-ticks and label on bottom strip only
        if idx == 3:
            ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_xticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"])
            ax.set_xlabel(r"Judge unsafe probability ($P_{\mathrm{unsafe}}$) | Human consensus ($h_{\mathrm{primary}}$)",
                          fontsize=6.6, labelpad=3)
        else:
            ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
            ax.set_xticklabels([])

    # Subpanel Title for Panel B (placed above top strip)
    axes_b[0].set_title("(b) Empirical Prediction Distributions (N = 50 conversations)",
                        fontsize=7.6, fontweight="bold", pad=6, loc="center")

    # Output paths
    pdf_path = out_dir / "fig1_tradeoff.pdf"
    png_path = out_dir / "fig1_tradeoff.png"

    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    fig.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Generated Figure 1 PDF: {pdf_path}")
    print(f"Generated Figure 1 PNG: {png_path}")


if __name__ == "__main__":
    make_fig1()
