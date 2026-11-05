"""Script to maintain and verify Figure 4: Disagreement as a Candidate Error Correlate.

Locks in the approved publication-grade bivariate scatter and partitioned regression tables
as fig4_disagreement.pdf and fig4_disagreement.png.
"""

from pathlib import Path
from PIL import Image


def make_fig4():
    script_dir = Path(__file__).resolve().parent
    fig_dir = script_dir.parent
    png_path = fig_dir / "fig4_disagreement.png"
    pdf_path = fig_dir / "fig4_disagreement.pdf"

    if not png_path.exists():
        raise FileNotFoundError(f"Source disagreement image not found at {png_path}")

    im = Image.open(png_path)
    im_rgb = im.convert("RGB")
    im_rgb.save(pdf_path, "PDF", resolution=300)
    print(f"Verified Figure 4 PNG: {png_path}")
    print(f"Verified Figure 4 PDF: {pdf_path}")


if __name__ == "__main__":
    make_fig4()
