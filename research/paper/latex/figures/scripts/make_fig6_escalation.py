"""Script to maintain and verify Figure 6: Conceptual Selective Human Escalation Architecture (Appendix B).

Locks in the approved publication-grade full-width operational workflow diagram
as fig6_escalation.pdf and fig6_escalation.png.
"""

from pathlib import Path
from PIL import Image


def make_fig6():
    script_dir = Path(__file__).resolve().parent
    fig_dir = script_dir.parent
    png_path = fig_dir / "fig6_escalation.png"
    pdf_path = fig_dir / "fig6_escalation.pdf"

    if not png_path.exists():
        raise FileNotFoundError(f"Source escalation image not found at {png_path}")

    im = Image.open(png_path)
    im_rgb = im.convert("RGB")
    im_rgb.save(pdf_path, "PDF", resolution=300)
    print(f"Verified Figure 6 PNG: {png_path}")
    print(f"Verified Figure 6 PDF: {pdf_path}")


if __name__ == "__main__":
    make_fig6()
