"""Generate master inspection contact sheet for the complete TrustEval figure suite."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def make_master_contact_sheet():
    fig_dir = Path("D:/Research/TrustEval/research/paper/latex/figures")
    artifact_dir = Path(r"C:\Users\KRISH PATEL\.gemini\antigravity\brain\e724aff9-dfc6-4da9-aae5-a2666d4316b7")

    figures = [
        ("Figure 1: Evaluator Polarization & Trade-Off Frontier (Page 1 Teaser)", fig_dir / "fig1_tradeoff.png"),
        ("Figure 2: Evaluation Architecture & Construct Validity (Methodology)", fig_dir / "fig2_architecture.png"),
        ("Figure 3: Decile Reliability Diagram & Bin Occupancy (Calibration)", fig_dir / "fig3_reliability.png"),
        ("Figure 4: Disagreement as a Candidate Error Correlate (Error Modeling)", fig_dir / "fig4_disagreement.png"),
        ("Figure 6: Conceptual Selective Human Escalation Architecture (Appendix B)", fig_dir / "fig6_escalation.png"),
    ]

    loaded = []
    for title, fpath in figures:
        if not fpath.exists():
            print(f"Warning: {fpath} does not exist.")
            continue
        im = Image.open(fpath)
        loaded.append((title, im))

    sheet_w = 2300
    sheet_h = 3600
    sheet = Image.new("RGB", (sheet_w, sheet_h), color="#f8f9fa")
    draw = ImageDraw.Draw(sheet)

    # Top banner
    draw.rectangle([(0, 0), (sheet_w, 70)], fill="#1a365d")
    try:
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_label = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title

    draw.text((30, 20), "TrustEval — Master Research Figure Suite (Figures 1, 2, 3, 4, and 6)", fill="white", font=font_title)

    # Row 1: Fig 1 (left) and Fig 3 (right)
    target_w_half = 1040
    # Fig 1
    im1 = loaded[0][1]
    target_h1 = int(im1.size[1] * (target_w_half / im1.size[0]))
    im1_thumb = im1.resize((target_w_half, target_h1), Image.Resampling.LANCZOS)
    draw.rectangle([(40, 90), (40 + target_w_half + 20, 90 + target_h1 + 50)], fill="white", outline="#cccccc", width=1)
    draw.text((55, 100), loaded[0][0], fill="#111111", font=font_label)
    sheet.paste(im1_thumb, (50, 130))

    # Fig 3
    im3 = loaded[2][1]
    target_h3 = int(im3.size[1] * (target_w_half / im3.size[0]))
    im3_thumb = im3.resize((target_w_half, target_h3), Image.Resampling.LANCZOS)
    draw.rectangle([(1160, 90), (1160 + target_w_half + 20, 90 + target_h3 + 50)], fill="white", outline="#cccccc", width=1)
    draw.text((1175, 100), loaded[2][0], fill="#111111", font=font_label)
    sheet.paste(im3_thumb, (1170, 130))

    row1_max_h = max(target_h1, target_h3)

    # Row 2: Fig 2 (Full-Width Landscape)
    im2 = loaded[1][1]
    target_w_full = 2160
    target_h2 = int(im2.size[1] * (target_w_full / im2.size[0]))
    im2_thumb = im2.resize((target_w_full, target_h2), Image.Resampling.LANCZOS)
    y_row2 = 90 + row1_max_h + 80
    draw.rectangle([(40, y_row2), (40 + target_w_full + 20, y_row2 + target_h2 + 50)], fill="white", outline="#cccccc", width=1)
    draw.text((55, y_row2 + 10), loaded[1][0], fill="#111111", font=font_label)
    sheet.paste(im2_thumb, (50, y_row2 + 40))

    # Row 3: Fig 4 (Left) and Fig 6 (Right / Below)
    # Fig 4
    im4 = loaded[3][1]
    target_w4 = 1040
    target_h4 = int(im4.size[1] * (target_w4 / im4.size[0]))
    im4_thumb = im4.resize((target_w4, target_h4), Image.Resampling.LANCZOS)
    y_row3 = y_row2 + target_h2 + 80
    draw.rectangle([(40, y_row3), (40 + target_w4 + 20, y_row3 + target_h4 + 50)], fill="white", outline="#cccccc", width=1)
    draw.text((55, y_row3 + 10), loaded[3][0], fill="#111111", font=font_label)
    sheet.paste(im4_thumb, (50, y_row3 + 40))

    # Fig 6 (Right of Fig 4)
    im6 = loaded[4][1]
    target_w6 = 1040
    target_h6 = int(im6.size[1] * (target_w6 / im6.size[0]))
    im6_thumb = im6.resize((target_w6, target_h6), Image.Resampling.LANCZOS)
    draw.rectangle([(1160, y_row3), (1160 + target_w6 + 20, y_row3 + target_h6 + 50)], fill="white", outline="#cccccc", width=1)
    draw.text((1175, y_row3 + 10), loaded[4][0], fill="#111111", font=font_label)
    sheet.paste(im6_thumb, (1170, y_row3 + 40))

    out_sheet_png = fig_dir / "contact_sheet.png"
    out_artifact_png = artifact_dir / "contact_sheet.png"
    sheet.save(out_sheet_png, "PNG")
    sheet.save(out_artifact_png, "PNG")

    print(f"Master contact sheet saved to:\n  - {out_sheet_png}\n  - {out_artifact_png}")


if __name__ == "__main__":
    make_master_contact_sheet()
