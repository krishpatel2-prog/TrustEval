# TrustEval — Complete Research Paper (Full-Length IEEE Manuscript)

**Title:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Format:** Full-Length IEEE Conference / Journal Double-Column Specification  
**Workspace:** `D:\Research\TrustEval\research\paper\final_full_manuscript\`  
**Archive:** `TrustEval_Full_Manuscript_Overleaf.zip`

---

## 1. Project Structure

This directory contains the complete, self-contained, unabridged research paper:

```
final_full_manuscript/
├── main.tex                    # Master LaTeX entry point
├── IEEEtran.cls                # Official IEEE Transactions/Conference Document Class (v1.8b)
├── references.bib              # Complete BibTeX bibliography (31 verified entries)
├── sections/                   # Core manuscript sections
│   ├── 00_abstract.tex         # Complete empirical abstract (199 words) & IEEE keywords
│   ├── 01_introduction.tex     # Section I: Introduction, RQ1–RQ3, Contributions, Figure 1
│   ├── 02_related_work.tex     # Section II: Literature Review & Table I
│   ├── 03_dataset_ground_truth.tex # Section III: DICES-350, Rater Filtering, h_primary
│   ├── 04_methodology_experimental_setup.tex # Section IV: Models, ChatML, Logits, Metrics, Figure 2
│   ├── 05_results.tex          # Section V: Table II, Figure 3, Table III, Figure 4, OLS
│   ├── 06_discussion.tex       # Section VI: Operational Trade-offs, Calibration Decoupling
│   ├── 07_limitations_ethics.tex # Section VII: Limitations, Power, Threats, Ethics
│   └── 08_conclusion.tex       # Section VIII: Conclusion & Future Directions
├── appendices/                 # Complete unabridged appendices
│   ├── appendix_a.tex          # Appendix A: 19 Excluded Annotator IDs Protocol
│   └── appendix_b.tex          # Appendix B: Conceptual Selective Escalation & Figure 6
├── figures/                    # Vector and raster publication assets
│   ├── fig1_tradeoff.pdf       # Figure 1: Trade-off Plane & Beeswarm Distributions
│   ├── fig2_architecture.pdf   # Figure 2: Research Architecture & Validity Schematic
│   ├── fig3_reliability.pdf    # Figure 3: Decile Reliability & Bin Occupancy Histograms
│   ├── fig4_disagreement.pdf   # Figure 4: Disagreement vs. Error Scatter & OLS Audit
│   └── fig6_escalation.pdf     # Figure 6: Conceptual Selective Escalation Workflow
├── TrustEval_Full_Manuscript_Overleaf.zip # One-click upload archive for Overleaf
├── MANUSCRIPT_ASSEMBLY_REPORT.md # Comprehensive assembly and scientific verification audit
└── README.md                   # This instruction guide
```

---

## 2. Compilation Instructions

### Option A: Overleaf (Recommended, One-Click)
1. Log in to [Overleaf](https://www.overleaf.com).
2. Click **New Project** $\to$ **Upload Project**.
3. Select `TrustEval_Full_Manuscript_Overleaf.zip`.
4. Ensure the root document is set to `main.tex`.
5. Click **Recompile**. Overleaf natively renders the complete two-column PDF with all figures, tables, math, citations, and appendices.

### Option B: Local TeX Live / MacTeX / MiKTeX
From the command line in this directory, run:
```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```
Or simply:
```bash
latexmk -pdf main
```
The output file will be `main.pdf`.
