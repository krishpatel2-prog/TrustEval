"""Generate Figure 5: Conceptual Selective Human Escalation Workflow (Full-Width Horizontal) - Revised."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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

def make_fig5():
    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir.parent

    # Full-width 2-column IEEE figure: 7.0 in wide x 2.8 in high
    fig, ax = plt.subplots(figsize=(7.0, 2.8), facecolor="white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Colors matching academic visual system
    c_blue = "#1f77b4"
    c_orange = "#d95f02"
    c_green = "#2ca02c"
    c_red = "#c53030"
    c_dark = "#2d3748"
    c_border = "#888888"

    # Helper for boxes
    def draw_box(x, y, w, h, body, title=None, bg="#f8f9fa", border="#888888",
                 title_col="#222222", body_col="#333333", shape="rect", r_size=1.2):
        if shape == "rect":
            p = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.4,rounding_size={r_size}",
                                       facecolor=bg, edgecolor=border, linewidth=0.8, zorder=2)
            ax.add_patch(p)
        elif shape == "diamond":
            pts = np.array([[x + w/2, y + h], [x + w, y + h/2], [x + w/2, y], [x, y + h/2]])
            p = patches.Polygon(pts, closed=True, facecolor=bg, edgecolor=border, linewidth=0.9, zorder=2)
            ax.add_patch(p)

        cx, cy = x + w / 2, y + h / 2
        if title:
            ax.text(cx, cy + h * 0.22, title, ha="center", va="center",
                    fontsize=6.2, fontweight="bold", color=title_col, zorder=3)
            ax.text(cx, cy - h * 0.18, body, ha="center", va="center",
                    fontsize=5.4, color=body_col, zorder=3)
        else:
            ax.text(cx, cy, body, ha="center", va="center",
                    fontsize=5.8, fontweight="medium", color=title_col, zorder=3)

    # Helper for arrows
    def draw_arrow(x1, y1, x2, y2, label=None, label_side="top", col="#555555"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=0.9, mutation_scale=7, shrinkA=0, shrinkB=0), zorder=1)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dy = 2.2 if label_side == "top" else -2.2
            ax.text(mx, my + dy, label, ha="center", va="center",
                    fontsize=5.4, fontweight="bold", color=col, zorder=3)

    # --- PROCESS PIPELINE (Horizontal Flow: Steps 1 to 6) ---

    # 1. Incoming User Conversation
    draw_box(1.0, 36.0, 13.0, 44.0,
             "Multi-Turn Dialog\nUser Query &\nAssistant Turns",
             title="1. Incoming\nConversation",
             bg="#f7fafc", border="#cbd5e0", title_col=c_dark)

    draw_arrow(14.0, 58.0, 17.5, 58.0)

    # 2. Prompt Serialization
    draw_box(17.5, 36.0, 13.5, 44.0,
             "Standardized\nTrustEval-R0\nPrompt Rubric\n(CPU <1.2 GB)",
             title="2. Prompt\nSerialization",
             bg="#edf2f7", border="#a0aec0", title_col=c_dark)

    # Split arrows to two judges
    draw_arrow(31.0, 66.0, 34.5, 71.0)
    draw_arrow(31.0, 50.0, 34.5, 45.0)

    # 3. Independent Judge Scoring (Step 3)
    # Judge 1 (Qwen)
    draw_box(34.5, 59.0, 15.0, 24.0,
             "Qwen2.5-0.5B\nInstruct (0.5B)\nLogit Extract:\n$P_{\\mathrm{qwen}} \\in [0, 1]$",
             title="3a. Judge 1",
             bg="#ebf8ff", border=c_blue, title_col=c_blue, body_col="#2c5282")

    # Judge 2 (SmolLM2)
    draw_box(34.5, 33.0, 15.0, 24.0,
             "SmolLM2-1.7B\nInstruct (1.7B)\nLogit Extract:\n$P_{\\mathrm{smollm}} \\in [0, 1]$",
             title="3b. Judge 2",
             bg="#fffaf0", border=c_orange, title_col=c_orange, body_col="#9c4221")

    # Merge arrows to Step 4
    draw_arrow(49.5, 71.0, 53.0, 64.0)
    draw_arrow(49.5, 45.0, 53.0, 52.0)

    # 4. Disagreement and Prediction Extraction (Step 4)
    eq_text = (
        "Ensemble Target:\n"
        "$P_{\\mathrm{ens}} = \\frac{1}{2}(P_{\\mathrm{qwen}} + P_{\\mathrm{smollm}})$\n\n"
        "Disagreement Metric:\n"
        "$\\Delta = |P_{\\mathrm{qwen}} - P_{\\mathrm{smollm}}|$"
    )
    draw_box(53.0, 34.0, 17.5, 48.0,
             eq_text,
             title="4. Disagreement &\nPrediction Extraction",
             bg="#f0fff4", border=c_green, title_col=c_green, body_col="#22543d")

    draw_arrow(70.5, 58.0, 73.5, 58.0)

    # 5. Conceptual Threshold Decision (Step 5: Diamond)
    draw_box(73.5, 39.0, 12.0, 38.0, "", shape="diamond", bg="#fff5f5", border=c_red)
    ax.text(79.5, 59.5, "5. Decision", ha="center", va="center",
            fontsize=5.6, fontweight="bold", color=c_red, zorder=3)
    ax.text(79.5, 54.0, "$\\Delta < \\tau$ ?", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=c_red, zorder=3)

    # Branch True: Automated Logging (Step 6a)
    draw_arrow(84.0, 68.0, 87.5, 72.0, label="Yes (Agreed)", label_side="top", col=c_green)
    draw_box(87.5, 59.0, 11.8, 24.0,
             "Deploy $P_{\\mathrm{ens}}$\nAuto-archive\nZero latency",
             title="6a. Tier 1\nAuto Audit",
             bg="#f0fff4", border=c_green, title_col=c_green, body_col="#22543d")

    # Branch False: Human Review (Step 6b)
    draw_arrow(84.0, 48.0, 87.5, 44.0, label="No (High $\\Delta$)", label_side="bottom", col=c_red)
    draw_box(87.5, 33.0, 11.8, 24.0,
             "Route dialogue\nto human safety\nexpert team",
             title="6b. Tier 2\nHuman Review",
             bg="#fff5f5", border=c_red, title_col=c_red, body_col="#742a2a")

    # --- BOTTOM MANDATORY QUALIFICATIONS BANNER ---
    callout_box = patches.FancyBboxPatch((1.0, 1.5), 98.0, 27.0, boxstyle="round,pad=0.3,rounding_size=1.0",
                                         facecolor="#fffaf0", edgecolor="#dd6b20", linewidth=0.8, zorder=2)
    ax.add_patch(callout_box)

    warn_title = "MANDATORY METHODOLOGICAL QUALIFICATIONS (Conceptual Operational Proposal — Unvalidated Architecture):"
    warn_text = (
        "• Threshold $\\tau$ is an uncalibrated conceptual parameter not empirically optimized in this study.\n"
        "• Low inter-judge disagreement does NOT guarantee evaluation correctness; correlated small-model failure modes remain.\n"
        "• Independent out-of-domain validation on held-out safety cohorts is required prior to institutional deployment.\n"
        "• Illustrative operational proposal only: this workflow has not been implemented or empirically validated as a production pipeline."
    )
    ax.text(3.0, 24.0, warn_title, ha="left", va="center", fontsize=5.6, fontweight="bold", color="#9c4221", zorder=3)
    ax.text(3.0, 12.0, warn_text, ha="left", va="center", fontsize=5.1, color="#7b341e", zorder=3)

    pdf_path = out_dir / "fig5_escalation.pdf"
    png_path = out_dir / "fig5_escalation.png"

    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Figure 5 successfully regenerated:\n  PDF: {pdf_path}\n  PNG: {png_path}")

if __name__ == "__main__":
    make_fig5()
