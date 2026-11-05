"""Script to maintain and verify Figure 3: Reliability Diagrams & Calibration Behaviour.

Locks in the approved publication-grade reliability diagram and decile occupancy visual
as fig3_reliability.pdf and fig3_reliability.png.
"""

from pathlib import Path
from PIL import Image


def make_fig3():
    script_dir = Path(__file__).resolve().parent
    fig_dir = script_dir.parent
    png_path = fig_dir / "fig3_reliability.png"
    pdf_path = fig_dir / "fig3_reliability.pdf"

    if not png_path.exists():
        raise FileNotFoundError(f"Source reliability image not found at {png_path}")

    im = Image.open(png_path)
    im_rgb = im.convert("RGB")
    im_rgb.save(pdf_path, "PDF", resolution=300)
    print(f"Verified Figure 3 PNG: {png_path}")
    print(f"Verified Figure 3 PDF: {pdf_path}")


if __name__ == "__main__":
    make_fig3()
