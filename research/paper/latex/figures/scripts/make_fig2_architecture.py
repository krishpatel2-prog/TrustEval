"""Script to maintain Figure 2: Evaluation Architecture & Construct Validity.

Locks in the approved publication-grade methodology architecture diagram
as fig2_architecture.pdf and fig2_architecture.png.
"""

from pathlib import Path
from PIL import Image


def make_fig2():
    script_dir = Path(__file__).resolve().parent
    fig_dir = script_dir.parent
    png_path = fig_dir / "fig2_architecture.png"
    pdf_path = fig_dir / "fig2_architecture.pdf"

    if not png_path.exists():
        raise FileNotFoundError(f"Source architecture image not found at {png_path}")

    im = Image.open(png_path)
    im_rgb = im.convert("RGB")
    im_rgb.save(pdf_path, "PDF", resolution=300)
    print(f"Verified Figure 2 PNG: {png_path}")
    print(f"Verified Figure 2 PDF: {pdf_path}")


if __name__ == "__main__":
    make_fig2()
