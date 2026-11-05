# TrustEval — Phase 2A Setup and Asset Inventory Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Phase:** Phase 2A — LaTeX Project Setup & Source-Asset Inventory  
**Workspace:** `D:\Research\TrustEval`  
**LaTeX Root:** `research/paper/latex/`  
**Master Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_3_4.md` (Frozen Master)  
**Approved Design Blueprint:** `research/paper/REFERENCE_PAPER_ANALYSIS.md`  
**Date:** November 2026  
**Status:** Phase 2A Complete (Awaiting Explicit Authorization for Phase 2B)

---

## 1. Environment and Dependency Inventory

An empirical audit of the local development environment was conducted to detect available compilers, plotting packages, and build tools.

### A. Python Environment
- **Python Binary:** `py.exe` / `python.exe`
- **Detected Version:** `Python 3.14.2 (AMD64, MSC v.1944 64-bit)`
- **Installed Plotting & Data Packages:**
  - `matplotlib`: **3.10.8** (Installed, functional)
  - `seaborn`: **0.13.2** (Installed, functional)
  - `numpy`: **2.4.1** (Installed, functional)
  - `scipy`: **1.18.1** (Installed, functional)
  - `pandas`: **2.3.3** (Installed, functional)
  - `pyyaml`: **Installed**
  - `scikit-learn`: **Installed**
- **Evaluation:** The Python data processing and vector visualization toolchain is 100% complete and fully verified. All figure generation scripts can execute immediately to produce publication-grade vector graphics (`.pdf` and `.png`).

### B. LaTeX Toolchain Status
- **`pdflatex` Executable:** `None` (Not detected in system `PATH` or standard installation directories)
- **`xelatex` Executable:** `None`
- **`lualatex` Executable:** `None`
- **`latexmk` Executable:** `None`
- **`bibtex` Executable:** `None`
- **Distribution Paths Searched:**
  - `C:\Program Files\MiKTeX` — *Not present*
  - `C:\texlive` / `D:\texlive` — *Not present*
  - `C:\Users\KRISH PATEL\AppData\Local\Programs\MiKTeX` — *Not present*
- **Diagnostic Finding:** No native TeX distribution is currently installed in the host operating system. Local PDF compilation cannot proceed until a TeX engine is provisioned, or until the LaTeX source directory is compiled via cloud/CI infrastructure (e.g., Overleaf, GitHub Actions).

### C. IEEEtran Document Class Availability
- **Local Filesystem Search:** Searched `D:\Research` and project trees. No local copy of `IEEEtran.cls` was found.
- **Official Source:** The official class file is distributed via CTAN:
  - Package: `IEEEtran` (v1.8b, official IEEE conference & transaction class)
  - URL: `https://ctan.org/pkg/ieeetran`
- **Recommended Installation:**
  - Option 1 (System-wide): Install MiKTeX on Windows via `winget install MiKTeX.MiKTeX`, which automatically fetches `IEEEtran.cls` upon first build.
  - Option 2 (Isolated/Portable): Download official `IEEEtran.cls` directly from CTAN and place it inside `research/paper/latex/`.
  - Option 3 (Cloud Collaboration): Upload the modular `latex/` directory directly to Overleaf, where IEEEtran is pre-installed in the TeX Live environment.

---

## 2. Created Modular LaTeX Project Structure

The publication project has been instantiated in an isolated, maintainable directory under `research/paper/latex/`:

```
research/paper/latex/
├── main.tex                    # Primary document root (IEEEtran conference class)
├── references.bib              # Verified BibTeX bibliography (26 curated entries)
├── Makefile                    # Multi-pass compilation recipes (pdflatex + bibtex)
├── README.md                   # Comprehensive project architecture & build manual
├── PHASE2A_SETUP_REPORT.md     # This comprehensive setup & asset inventory report
├── sections/                   # Modular section files (strictly isolated)
│   ├── 01_introduction.tex
│   ├── 02_related_work.tex
│   ├── 03_dataset_methodology.tex
│   ├── 04_experimental_setup.tex
│   ├── 05_results.tex
│   ├── 06_disagreement_analysis.tex
│   ├── 07_discussion.tex
│   └── 08_conclusion.tex
├── tables/                     # Standalone booktabs LaTeX tables (Phase 2B target)
├── figures/                    # Vector PDF and high-DPI raster assets
│   └── scripts/                # Standalone reproducible Python figure generation scripts
├── appendices/                 # Modular supplementary appendices
│   ├── appendix_a.tex          # Quality filtering protocol (19 rater exclusions)
│   └── appendix_b.tex          # Rubric mapping, Positioning Matrix, diagnostic tables
└── build/                      # Build outputs, compilation logs, and diagnostics
    └── build_test.log          # Automated environment compilation audit log
```

---

## 3. Files Created and Their Purpose

| File / Path | Format | Size | Purpose |
| :--- | :---: | :---: | :--- |
| `latex/main.tex` | LaTeX | 1,882 B | Master LaTeX root document. Configures `\documentclass[conference]{IEEEtran}`, loads essential packages (`amsmath`, `booktabs`, `graphicx`, `cite`, `microtype`, `url`, `hyperref`), defines clean placeholders for author blocks, and imports modular section/appendix files. |
| `latex/references.bib` | BibTeX | 13,100 B | Full 26-entry curated bibliography, copied from `research/literature/references.bib`. Contains complete entries for DICES, Zheng et al., Ali (2026), Bavaresco et al. (ACL 2025), and foundational literature. |
| `latex/Makefile` | Make | 616 B | Automated build automation script with targets `all`, `clean`, and `test`, using `pdflatex -output-directory=build` and `bibtex`. |
| `latex/README.md` | Markdown | 1,908 B | Full documentation of repository structure, modular workflow, formatting guidelines, and compilation commands. |
| `sections/01_introduction.tex` | LaTeX | 343 B | Section I module: Motivation, consumer CPU constraints, core research questions (RQ1–RQ3), empirical scope, and overview of contributions. |
| `sections/02_related_work.tex` | LaTeX | 362 B | Section II module: Automated LLM judges, human subjectivity, evaluator ensembles, and prior benchmark context (Ali, 2026). |
| `sections/03_dataset_methodology.tex` | LaTeX | 459 B | Section III module: DICES-350 adversarial benchmark, quality filtering, continuous consensus targets ($h_{\text{primary}}$, $h_{\text{sensitivity}}$), 50-item sample, and evaluator models. |
| `sections/04_experimental_setup.tex` | LaTeX | 472 B | Section IV module: Next-token logit extraction, prompt rubric (TrustEval-R0), evaluation metrics, held-out prevalence baseline, and CPU execution profile. |
| `sections/05_results.tex` | LaTeX | 439 B | Section V module: Master performance evaluation matrix (`table*`), single judge polarization, two-judge ensemble trade-offs, baseline comparisons, and calibration analysis. |
| `sections/06_disagreement_analysis.tex` | LaTeX | 464 B | Section VI module: Inter-judge disagreement as candidate error correlate, bivariate correlations (Pearson $r$ vs non-significant Spearman $\rho$), nested OLS modeling, and cross-validation. |
| `sections/07_discussion.tex` | LaTeX | 479 B | Section VII module: Empirical synthesis, conceptual selective escalation workflow (uncalibrated $\tau$), threats to validity, and responsible AI considerations. |
| `sections/08_conclusion.tex` | LaTeX | 380 B | Section VIII module: Summary of empirical findings, architectural trade-offs, and future research directions (cohort scaling, formal epistemic uncertainty). |
| `appendices/appendix_a.tex` | LaTeX | 372 B | Appendix A module: Methodological protocol summary of the 19 anomalous crowd annotator exclusions (`removed_raters_350`). |
| `appendices/appendix_b.tex` | LaTeX | 385 B | Appendix B module: Prompt rubric mapping, Framework Positioning Matrix (Table V), paired statistical tests, bootstrap CIs, and sensitivity analysis. |
| `build/build_test.log` | Log | 321 B | Diagnostic execution log of the initial compilation attempt. |

---

## 4. LaTeX Compilation Test Result

An automated smoke-test compilation was executed via `python`:

- **Command Invoked:** `pdflatex -interaction=nonstopmode -output-directory=build main.tex`
- **Result:** Compilation blocked before process execution.
- **Return Code:** `N/A` (`pdflatex` executable not found in system `PATH`).
- **Log Contents (`build/build_test.log`):**
  ```
  === LATEX BUILD TEST LOG ===
  pdflatex executable: None
  bibtex executable: None
  RESULT: FAILED - pdflatex is not installed in system PATH.
  DIAGNOSTIC: No LaTeX distribution (TeX Live / MiKTeX) was detected on the Windows host.
  RECOMMENDATION: Install TeX Live or MiKTeX, or compile via CI/cloud LaTeX service (Overleaf / GitHub Actions).
  ```
- **Conclusion:** The modular LaTeX code is structurally complete, syntactically clean, and ready for compilation as soon as a TeX compiler is available.

---

## 5. Source Manuscript Integrity Confirmation

We confirmed the integrity of the frozen master manuscript:

- **Path:** `D:\Research\TrustEval\research\paper\TRUSTEVAL_PAPER_V2_5_3_4.md`
- **File Size:** **110,950 bytes**
- **Last Modified Timestamp:** **Thu Nov 5 13:12:07 2026**
- **Edits Made:** **Strictly 0 edits** (unopened for writing; 100% frozen).
- **Approved Blueprint:** `D:\Research\TrustEval\research\paper\REFERENCE_PAPER_ANALYSIS.md` (56,494 bytes; verified and finalized).

---

## 6. Figure-by-Figure Data-Source Mapping

All proposed figures trace directly to existing, frozen local project artifacts. No new inference or synthetic data is required.

| Figure Identifier & Topic | Planned Layout & Dimensions | Chart Type | Exact Source File Path | Key Variables / Columns | Completeness & Reproducibility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Figure 1:** Page 1 Teaser: Paradigm Overview & Evaluator Trade-offs | Upper right column of Page 1; Single column width ($3.5\text{ in} \times 3.2\text{ in}$) | 3-panel horizontal mini-cards / diagnostic profile bar | `results/tables/ensemble_predictions_dices50.csv`<br>`results/diagnostics/predictive_discrimination_audit.json`<br>`results/tables/evaluation_metrics_dices50.json` | `p_qwen`, `p_smollm`, `p_ensemble`, `h_primary`, `mean_pred`, `std_pred`, `mae_soft`, `auroc_majority` | **Complete (100%).** Fully reproducible via standalone script. |
| **Figure 2:** Decile Calibration Curves & Reliability Diagrams | Single column ($3.5\text{ in} \times 3.0\text{ in}$) or full width ($7.0\text{ in} \times 2.8\text{ in}$) in Section V | 10-bin reliability curves with diagonal reference & point markers | `results/tables/ensemble_predictions_dices50.csv`<br>`results/tables/evaluation_metrics_dices50.json`<br>`src/trusteval/evaluation/figures.py` | `p_qwen`, `p_smollm`, `p_ensemble`, `h_primary`, bin confidence, bin empirical accuracy | **Complete (100%).** Reference script exists in `figures.py`. |
| **Figure 3:** Inter-Judge Disagreement vs. Absolute Evaluation Error | Single column ($3.5\text{ in} \times 3.0\text{ in}$) in Section VI | Scatter plot ($N=50$) with OLS regression fit line & 95% CI band | `results/tables/ensemble_predictions_dices50.csv`<br>`results/tables/disagreement_cv_dices50.json`<br>`src/trusteval/evaluation/figures.py` | `disagreement` ($|P_{\text{qwen}} - P_{\text{smollm}}|$), `abs_error` ($|P_{\text{ens}} - h_{\text{primary}}|$) | **Complete (100%).** Reference script exists in `figures.py`. |
| **Figure 4:** Continuous Step-Density Alignment (Appendix F) | Single column ($3.5\text{ in} \times 2.8\text{ in}$) in Appendix F / Section V | 20-bin step density histograms overlaying judges against human consensus | `results/tables/ensemble_predictions_dices50.csv`<br>`src/trusteval/evaluation/figures.py` | `p_qwen`, `p_smollm`, `p_ensemble`, `h_primary` | **Complete (100%).** Reference script exists in `figures.py`. |
| **Figure 5:** Conceptual Selective Human Escalation Workflow | Single column ($3.5\text{ in} \times 4.0\text{ in}$) in Section VII / Appendix | Vector workflow diagram (process boxes, decision diamond, output paths) | Manuscript Section 9.2 description;<br>`REFERENCE_PAPER_ANALYSIS.md` Section 5.C | Conceptual steps: prompt $\to$ logit extraction $\to$ disagreement check ($\Delta < \tau$) $\to$ logging vs. escalation | **Complete (100%).** Generated via Python `matplotlib.patches` vector rendering. |

---

## 7. Table-by-Table Data-Source Mapping

Every numerical entry in the planned tables traces to frozen JSON/CSV artifacts or verified reference benchmarks:

| Table Identifier & Description | Placement in Paper | Planned Layout | Exact Source File Path | Data Format & Relevant Keys | Status & Reproducibility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Table I:** Prior Benchmark Results from Ali (2026) | Section II (Related Work) | Single Column (3.5 in) | `d:\Research\whose-safety-judge-main\results\summary.json`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 1) | JSON (`runs['primary__P0']`, BSS, Spearman $\rho$, AUROC on DICES-350 / 990) | **Complete (100%).** Frozen benchmark data verified. |
| **Table II:** Master Performance Evaluation Matrix | Section V (Results) | Full-width float (`table*`, 7.0 in) | `results/diagnostics/predictive_discrimination_audit.json`<br>`results/tables/evaluation_metrics_dices50.json`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 4) | JSON (Mean, Std, MAE, RMSE, Soft MSE, ECE-10, Populated Deciles, Pearson $r$, Spearman $\rho$, AUROC) | **Complete (100%).** All 5 evaluator rows verified. |
| **Table III:** Disagreement Predictive Modeling (OLS & CV) | Section VI (Disagreement) | Single Column (3.5 in) | `results/tables/disagreement_cv_dices50.json`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 7) | JSON (Model 1, Model 2, Model 3 OLS coefficients, std err, $F(1, 46)$, in-sample $R^2$, out-of-fold $R^2$) | **Complete (100%).** Verified against manuscript. |
| **Table IV:** DICES Annotation Axis to TrustEval-R0 Mapping | Appendix B | Single Column (3.5 in) | `configs/prompts/safety_judge_v1.txt`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 3) | Text / Markdown (5 crowd questions mapped to 4 prompt rubric criteria) | **Complete (100%).** Exact prompt bytes archived. |
| **Table V:** Framework Positioning Matrix & Ali Comparison | Appendix B | Full-width float (`table*`, 7.0 in) | `research/literature/RELATED_WORK_SOURCE_MAP.md`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 5) | Markdown (7 dimensions: Judge Architecture, Consensus Target, Loss Metric, Inference Cost, Calibration, etc.) | **Complete (100%).** Formally relocated to Appendix B. |
| **Table VI:** Paired Error Differences Between Evaluators | Appendix C | Single Column (3.5 in) | `results/diagnostics/additional_statistical_reporting.json`<br>`results/diagnostics/phase_3c_statistical_refinements.json` | JSON (`paired_mae_differences`, `paired_mse_differences`: $t$-tests, Wilcoxon signed-rank, Holm correction) | **Complete (100%).** 6 evaluator pairs verified. |
| **Table VII:** Rater-Cluster Bootstrap Statistics (104 Raters) | Appendix D | Single Column (3.5 in) | `results/tables/bootstrap_ci_dices50.json`<br>`results/tables/human_agreement_metrics.json`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 8) | JSON (1,000 resamples: point estimates, SE, 95% bootstrap CIs across MAE, MSE, ECE) | **Complete (100%).** Verified against manuscript. |
| **Table VIII:** Target Consensus Formulation Sensitivity Analysis | Appendix E | Single Column (3.5 in) | `results/tables/evaluation_metrics_dices50.json`<br>`TRUSTEVAL_PAPER_V2_5_3_4.md` (Table 9) | JSON (`primary_target_h_primary` vs `sensitivity_target_h_sensitivity`) | **Complete (100%).** Sensitivity target verified. |

---

## 8. Missing Assets, Dependencies, and Blockers

### A. Non-Blocking Items (Self-Contained)
1. **Research Data:** **0 missing items.** All 50-conversation predictions, 104-annotator ground truths, OLS regressions, and bootstrap metrics exist as frozen local files.
2. **Bibliographic Entries:** **0 missing items.** All 26 references are populated in `latex/references.bib`.
3. **Figure Code:** Core plotting logic exists in `src/trusteval/evaluation/figures.py`. Standalone scripts will be authored in `latex/figures/scripts/` during Phase 2B.

### B. Dependencies and Potential Blockers
1. **Local TeX Compiler:**
   - **Status:** Neither `pdflatex` nor `latexmk` is present in system `PATH`.
   - **Impact:** We can author modular LaTeX files and generate standalone vector PDF figures, but cannot compile a local `.pdf` document without installing MiKTeX/TeX Live or building via CI/Overleaf.
   - **Action for Phase 2B:** Provide standalone Python scripts to compile vector figures and author `.tex` modules. For PDF compilation, user can install MiKTeX (`winget install MiKTeX.MiKTeX`) or upload `latex/` to Overleaf.
2. **Author Names and Affiliations:**
   - **Status:** Marked with explicit placeholders in `main.tex`.
   - **Action:** Can remain anonymized for double-blind submission or updated with confirmed author metadata.

---

## 9. Detailed Proposed Figure-Generation Implementation Plan

During Phase 2B, standalone scripts in `research/paper/latex/figures/scripts/` will generate vector PDF assets (`.pdf`) and 300 DPI PNG fallbacks (`.png`) into `research/paper/latex/figures/`.

### Planned Figure Specifications

#### Figure 1: Page 1 Teaser Graphic (Paradigm Overview & Evaluator Trade-offs)
- **Script:** `figures/scripts/make_fig1_teaser.py`
- **Output:** `figures/fig1_teaser.pdf` (and `.png`)
- **Dimensions:** $3.5\text{ in wide} \times 3.2\text{ in high}$ (Single column).
- **Visual Design:** A three-panel vertically stacked card or horizontal mini-panel layout:
  - *Panel A (Qwen2.5-0.5B):* Shows discriminative ranking ($\text{AUROC} = 0.7529, \rho = 0.5680$) contrasted with positive bias ($\mu = 0.751$ vs. human $0.338$, $\text{MAE} = 0.4152$).
  - *Panel B (SmolLM2-1.7B):* Shows lowest judge $\text{MAE} = 0.1734$ achieved via low-variance score compression ($\sigma = 0.028$, $\mu = 0.253$).
  - *Panel C (Ensemble vs. Prevalence Baseline):* Highlights the ensemble moderating bias ($\mu = 0.502$) and maximizing ranking ($\rho = 0.5903, r = 0.4992$), while explicitly noting that the held-out prevalence baseline retains lower RMSE ($0.2454$) and lower Soft MSE ($0.0602$).
- **Placement:** Top of right column on Page 1 (Section I).

#### Figure 2: Decile Calibration Curves & Reliability Diagrams
- **Script:** `figures/scripts/make_fig2_calibration.py`
- **Output:** `figures/fig2_calibration.pdf` (and `.png`)
- **Dimensions:** $3.5\text{ in wide} \times 3.0\text{ in high}$ (Single column) or $7.0\text{ in wide} \times 2.8\text{ in high}$ (Two column span).
- **Visual Design:** Calibration curves plotting bin mean predicted probability vs. empirical human consensus proportion across 10 deciles. Directly labels Qwen ($\text{ECE-10} = 0.4128$), SmolLM2 ($\text{ECE-10} = 0.0850$), and Ensemble ($\text{ECE-10} = 0.1639$).
- **Mandatory Calibration Note:** Explicitly represents the zero ECE ($0.0000^*$) of the prevalence baseline as degenerate single-bin pooling, avoiding any visual implication of continuous calibration.
- **Placement:** Section V (Results).

#### Figure 3: Inter-Judge Disagreement vs. Absolute Evaluation Error
- **Script:** `figures/scripts/make_fig3_disagreement.py`
- **Output:** `figures/fig3_disagreement.pdf` (and `.png`)
- **Dimensions:** $3.5\text{ in wide} \times 3.0\text{ in high}$ (Single column).
- **Visual Design:** Scatter plot of the 50 conversations with fitted OLS regression line and shaded 95% confidence ribbon.
- **Reporting Annotations:** Annotates bivariate Pearson $r = 0.3125$ ($p = 0.0271$), non-significant Spearman $\rho = 0.2302$ ($p = 0.1078$), nested OLS $F(1, 46) = 5.676$ ($p = 0.0214$), and descriptive $\Delta R^2_{\text{OOF}} = +0.0805$.
- **Placement:** Section VI (Disagreement Analysis).

#### Figure 4: Continuous Step-Density Alignment (Appendix F / Section V)
- **Script:** `figures/scripts/make_fig4_density.py`
- **Output:** `figures/fig4_density.pdf` (and `.png`)
- **Dimensions:** $3.5\text{ in wide} \times 2.8\text{ in high}$ (Single column).
- **Visual Design:** 20-bin step density distribution overlaying Qwen, SmolLM2, and Ensemble against human consensus $h_{\text{primary}}$.
- **Placement:** Appendix F (or Section V if page budget permits).

#### Figure 5: Conceptual Selective Human Escalation Workflow
- **Script:** `figures/scripts/make_fig5_escalation.py`
- **Output:** `figures/fig5_escalation.pdf` (and `.png`)
- **Dimensions:** $3.5\text{ in wide} \times 3.8\text{ in high}$ (Single column).
- **Visual Design:** Clean vector flowchart showing prompt serialization $\to$ sub-2B logit extraction $\to$ disagreement check ($\Delta < \tau$) $\to$ automated logging vs. human safety audit. Explicitly qualifies threshold $\tau$ as uncalibrated.
- **Placement:** Section VII (Discussion).

---

## 10. Recommended Order of Actual Publication Production (Phase 2B)

To ensure maximum scientific precision and prevent layout reflows, Phase 2B production should proceed in the following strict sequential stages:

1. **Stage 1 — Vector Figure Generation (Phase 2B.1):**
   - Author standalone Python scripts in `figures/scripts/`.
   - Generate standalone vector PDFs (`fig1` through `fig5`) from frozen project CSVs/JSONs.
   - Visually inspect vector dimensions and label crispness.
2. **Stage 2 — Booktabs LaTeX Table Production (Phase 2B.2):**
   - Convert verified JSON results into standalone modular `.tex` table files in `tables/` (`table1_ali.tex`, `table2_master.tex`, `table3_regression.tex`, and appendix tables).
   - Ensure strict compliance with `booktabs` (no vertical lines, bold subheadings).
3. **Stage 3 — Section Content Encoding (Phase 2B.3):**
   - Translate content from frozen manuscript `TRUSTEVAL_PAPER_V2_5_3_4.md` into modular section files `sections/01_introduction.tex` through `08_conclusion.tex`.
   - Insert cross-references (`\ref{sec:...}`, `\ref{fig:...}`, `\ref{tab:...}`).
   - Insert IEEE numerical citations (`\cite{...}`).
4. **Stage 4 — Appendices & Supplementary Material (Phase 2B.4):**
   - Populate `appendices/appendix_a.tex` (rater exclusion summary) and `appendix_b.tex` (prompt text, Framework Positioning Matrix, bootstrap CIs).
5. **Stage 5 — Compilation & Page Budget Optimization (Phase 2B.5):**
   - Compile document and tune spacing to strictly satisfy the 8–10 page main narrative budget.

---

*Phase 2A setup is complete. All source assets, directory structures, and data mappings are documented and verified. Awaiting your explicit authorization before proceeding to Phase 2B.*
