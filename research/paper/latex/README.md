# TrustEval LaTeX Publication Project

This directory contains the modular LaTeX source code for the academic publication:

**TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges**

## Directory Layout

```
latex/
├── main.tex                    # Primary document root (IEEEtran conference class)
├── references.bib              # Verified BibTeX bibliography (26 entries)
├── Makefile                    # Standard compilation and cleanup recipes
├── README.md                   # This project guide
├── PHASE2A_SETUP_REPORT.md     # Phase 2A setup report and asset inventory
├── sections/                   # Modular text sections (01 to 08)
│   ├── 01_introduction.tex
│   ├── 02_related_work.tex
│   ├── 03_dataset_methodology.tex
│   ├── 04_experimental_setup.tex
│   ├── 05_results.tex
│   ├── 06_disagreement_analysis.tex
│   ├── 07_discussion.tex
│   └── 08_conclusion.tex
├── tables/                     # Modular standalone table files (booktabs format)
├── figures/                    # Vector PDF and PNG figure assets
│   └── scripts/                # Standalone Python scripts for figure generation
├── appendices/                 # Supplementary appendices (A and B)
│   ├── appendix_a.tex
│   └── appendix_b.tex
└── build/                      # Build outputs and compilation logs
```

## Compilation Requirements

- **Class:** `IEEEtran.cls` (IEEE Conference Two-Column Format).
- **Engine:** `pdflatex` or `latexmk`.
- **BibTeX:** `bibtex`.

## Compilation Commands

```bash
# Standard 4-pass compilation
pdflatex -output-directory=build main.tex
bibtex build/main
pdflatex -output-directory=build main.tex
pdflatex -output-directory=build main.tex
```
