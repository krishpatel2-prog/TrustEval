# TrustEval — Complete Manuscript Assembly & Scientific Verification Report

**Document Title:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Format:** Full-Length IEEE Transactions/Conference Double-Column Specification  
**Assembly Workspace:** `D:\Research\TrustEval\research\paper\final_full_manuscript\`  
**Frozen Master Document:** `TRUSTEVAL_PAPER_V2_5_3_4.md`  
**Date of Assembly:** 2026-11-05  
**Assembly Status:** **COMPLETE, SELF-CONTAINED & FULLY VALIDATED**

---

## 1. Executive Summary & Purpose

In accordance with user authorization, we have prioritized and completed the full assembly of the **original, unabridged TrustEval research paper**. This is the full-length scientific manuscript representing all research conducted over the project's developmental lifecycle. It is completely independent of the separate 9-page ACM TRUST conversion workspace.

The assembled manuscript preserves the comprehensive research narrative across 8 major sections, 2 extensive appendices, 3 full-width/single-column tables, 5 publication figures, and 31 verified academic citations, totaling **12,572 words**.

---

## 2. Inventory of Assembled Manuscript Assets

### 2.1 Modular Textual Sections
Every section has been verified for narrative flow, logical continuity, and mathematical rigor:

| Section File | Title & Scope | Visual / Table Assets Included | Word Count |
|---|---|---|---|
| `sections/00_abstract.tex` | **Abstract & Keywords:** Problem formulation, empirical scope ($N=50$, 104 raters, 5,200 ratings), key results, and assurance disclaimers. | None | 199 words |
| `sections/01_introduction.tex` | **Section I — Introduction:** Motivation (privacy, cloud lock-in, latency), small open-weight judges, RQ1–RQ3, 6 concrete contributions, and paper roadmap. | **Figure 1** (Capability Trade-Off Plane & Prediction Distributions) | 1,433 words |
| `sections/02_related_work.tex` | **Section II — Related Work:** 5 literature pillars (LLM judges, crowdsourced disagreement, calibration, ensembles, Ali 2026 baseline), research gap. | **Table I** (Systematic Comparison of Automated LLM Evaluation Frameworks) | 1,412 words |
| `sections/03_dataset_ground_truth.tex` | **Section III — Dataset & Ground Truth:** Google DICES-350, rater exclusion ($123 \to 104$), 5,200 ratings, $h_{\text{primary}}$, $h_{\text{sensitivity}}$, and logical OR construct reduction. | Equations (1)–(7) | 1,232 words |
| `sections/04_methodology_experimental_setup.tex` | **Section IV — Methodology & Setup:** Qwen2.5-0.5B, SmolLM2-1.7B, TrustEval-R0 ChatML prompt, next-token logit scoring (token IDs), CPU profiling, metrics, 5-fold OOF prevalence baseline, paired test battery. | **Figure 2** (Evaluation Architecture & Construct Validity Schematic) | 1,902 words |
| `sections/05_results.tex` | **Section V — Experimental Results:** Point error, decile calibration, majority AUROC, paired hypothesis tests, disagreement bivariate & nested OLS regressions, out-of-fold CV. | **Table II** (Master Performance Matrix), **Figure 3** (Reliability & Occupancy), **Table III** (Paired Hypothesis Tests), **Figure 4** (Disagreement OLS) | 2,861 words |
| `sections/06_discussion.tex` | **Section VI — Discussion:** Ensemble trade-off, ranking vs. calibration decoupling, disagreement boundaries & shared failure modes, edge deployment implications, relationship to prior work. | None | 1,599 words |
| `sections/07_limitations_ethics.tex` | **Section VII — Limitations & Ethics:** Sample size constraints ($N=50$), construct validity, model specificity, statistical power for rank disagreement, ethical use & prohibition of autonomous gating. | None | 948 words |
| `sections/08_conclusion.tex` | **Section VIII — Conclusion & Future Work:** Summary of empirical findings, 5 prioritized future research directions. | None | 399 words |
| `appendices/appendix_a.tex` | **Appendix A — Crowd Annotator Quality Filtering:** Complete protocol and unabridged listing of all 19 excluded annotator IDs from `removed_raters_350`. | None | 182 words |
| `appendices/appendix_b.tex` | **Appendix B — Conceptual Selective Escalation:** Two-tier human escalation architecture, 5 operational stages, non-deployment disclaimers. | **Figure 6** (Conceptual Selective Human Escalation Architecture) | 405 words |
| **Combined Text Total** | **Full Complete Manuscript** | **5 Figures, 3 Tables, 2 Appendices** | **12,572 words** |

---

### 2.2 Figures Inventory & Verification
All figures are verified, rendered in high-resolution vector PDF (with 300 DPI PNG backups), and stored in `final_full_manuscript/figures/`:

1. **Figure 1 (`figures/fig1_tradeoff.pdf`):**  
   - *Caption & Content:* Evaluator polarization and the ensembling trade-off frontier ($N=50$). Panel (a) plots Mean Absolute Error (MAE, lower is better) vs. majority-consensus discrimination (AUROC, higher is better), with contextual prevalence baseline noted. Panel (b) plots single-model prediction distributions (beeswarm strips) showing Qwen's positive hazard bias ($\mu=0.751$), SmolLM2's variance collapse ($\sigma=0.039$), Ensemble ($\mu=0.502$), and human consensus ($\mu=0.338$).
2. **Figure 2 (`figures/fig2_architecture.pdf`):**  
   - *Caption & Content:* Full-width evaluation architecture and construct validity framework. Path A (Human Reference Construction via 104 raters) and Path B (Automated Judge Evaluation on CPU via ChatML next-token scoring), converging on error, calibration, and disagreement evaluation.
3. **Figure 3 (`figures/fig3_reliability.pdf`):**  
   - *Caption & Content:* Decile reliability diagrams and sample occupancy histograms. Panel (a) plots empirical calibration curves across 10 deciles (Qwen overpredicting in 8 bins, SmolLM2 underpredicting in 2 bins, Ensemble overpredicting in 6 bins, OOF prevalence baseline at $0.0017$). Panel (b) plots bin occupancy distributions.
4. **Figure 4 (`figures/fig4_disagreement.pdf`):**  
   - *Caption & Content:* Inter-judge disagreement ($\Delta$) as an empirical error correlate. Scatter plot with bivariate OLS fit ($\hat{E} = 0.1549 + 0.1829\Delta$, $95\%$ mean-prediction band), bivariate linear audit ($r=0.3125, p=0.0271$; $\rho=0.2302, p=0.1078$), nested in-sample OLS diagnostics ($F(1, 46)=5.676, p=0.0214, \Delta R^2_{\text{in}}=+0.1039$), and 5-fold cross-validation ($\Delta R^2_{\text{OOF}}=+0.0805$).
5. **Figure 6 (`figures/fig6_escalation.pdf`):**  
   - *Caption & Content:* Full-width conceptual selective human escalation architecture (Appendix B). 5-stage workflow illustrating local parallel execution, disagreement extraction, automated gating for low disagreement ($\Delta < \tau$), and human expert escalation for contested cases ($\Delta \ge \tau$), accompanied by explicit disclaimers regarding uncalibrated thresholds and shared failure modes.

*(Note on Figure 5: In accordance with `VISUAL_DESIGN_BLUEPRINT.md` and `PHASE2B1_FIGURE_REPORT.md`, Figure 5 [redundant distribution density curves] was merged into Figure 1 Panel (b) and Table II, preserving Figure 6 as the designated publication-grade operational schematic).*

---

### 2.3 Tables Inventory & Verification
All three master research tables are preserved in full detail:

1. **Table I (Section II):** Systematic Comparison of Automated LLM Evaluation Frameworks (comparing MT-Bench, PandaLM, HarmBench, Coin Flip for Safety, LLM-as-a-Jury, SLMJury, Ali 2026, and TrustEval across target models, target formulations, uncertainty signals, and hardware profiles).
2. **Table II (Section V):** Consolidated Evaluation Performance Matrix on Google DICES-350 ($N=50$), detailing mean predictions ($\bar{P} \pm s$), MAE, RMSE, Soft MSE, decile $\text{ECE}_{10}$, populated bins ($B_{\text{pop}}$), Pearson $r$, Spearman $\rho$, and majority AUROC across Qwen, SmolLM2, the Ensemble, and the 5-fold OOF prevalence baseline.
3. **Table III (Section V):** Paired Statistical Comparisons and Hypothesis Tests on Evaluator Errors ($N=50$), reporting mean differences, paired $t$-tests ($p_{\text{unadj}}, p_{\text{Holm}}$), Wilcoxon signed-rank tests ($W, p_{\text{unadj}}, p_{\text{Holm}}$), two-sided sign tests, 2,000-replicate item bootstrap 95% CIs, and 1,000-replicate rater-cluster bootstrap 95% CIs across all pairwise comparisons.

---

## 3. Scientific Integrity & Numerical Reconciliation Audit

Every quantitative figure and scientific claim across the assembled manuscript has been verified against the frozen experimental outputs (`results/tables/`, `results/diagnostics/`, and data manifests):

| Scientific Parameter | Verified Value | Manuscript Citation & Location | Verification Status |
|---|---|---|---|
| **Conversational Sample Size** | $N = 50$ dialogues | `sections/03_dataset_ground_truth.tex` | Confirmed via `dices_50_sample_manifest.json` (random seed `20261103`). |
| **Crowd Annotators per Item** | 104 retained raters | `sections/03_dataset_ground_truth.tex`, `appendices/appendix_a.tex` | Confirmed; 123 initial raters minus 19 in `removed_raters_350`. |
| **Total Evaluated Ratings** | 5,200 ratings | `sections/03_dataset_ground_truth.tex` | Confirmed; exactly $50 \times 104 = 5,200$ (4,889 decisive, 311 unsure). |
| **Primary Consensus Target** | $\bar{h}_{\text{primary}} = 0.3381$ | `sections/03_dataset_ground_truth.tex` | Confirmed; item macro mean ($s=0.2442$, range $[0.0392, 0.9519]$). |
| **Sensitivity Target** | $\bar{h}_{\text{sensitivity}} = 0.3464$ | `sections/03_dataset_ground_truth.tex` | Confirmed; item macro mean ($s=0.2378$, range $[0.0481, 0.9519]$). |
| **Qwen Token Continuation IDs** | Yes: 9454, No: 2753 | `sections/04_methodology_experimental_setup.tex` | Confirmed via tokenizer audit in `inference.py`. |
| **SmolLM2 Token Continuation IDs** | Yes: 10539, No: 5230 | `sections/04_methodology_experimental_setup.tex` | Confirmed via tokenizer audit in `inference.py`. |
| **Qwen Performance** | $\bar{P}=0.7509, \text{MAE}=0.4152, \text{Soft MSE}=0.2202, \text{AUROC}=0.7529$ | Table II, `sections/05_results.tex` | Confirmed via `ensemble_predictions_dices50.csv`. |
| **SmolLM2 Performance** | $\bar{P}=0.2531, \text{MAE}=0.1734, \text{Soft MSE}=0.0628, \text{AUROC}=0.6690$ | Table II, `sections/05_results.tex` | Confirmed via `ensemble_predictions_dices50.csv`. |
| **Two-Judge Ensemble Performance** | $\bar{P}=0.5020, \text{MAE}=0.2464, \text{Soft MSE}=0.0713, \text{AUROC}=0.7517$ | Table II, `sections/05_results.tex` | Confirmed; cuts Qwen MAE by $40.6\%$, Soft MSE by $67.6\%$. |
| **Prevalence Baseline Performance** | $\bar{P}=0.3398, \text{MAE}=0.1983, \text{Soft MSE}=0.0602, \text{ECE}=0.0017$ | Table II, `sections/05_results.tex` | Confirmed via 5-fold cross-validated out-of-fold scoring. |
| **Linear Association ($\Delta$ vs $E$)** | Pearson $r = 0.3125$ ($p = 0.0271$) | `sections/05_results.tex`, Figure 4 | Confirmed via `disagreement_cv_dices50.json`. |
| **Rank Association ($\Delta$ vs $E$)** | Spearman $\rho = 0.2302$ ($p = 0.1078$) | `sections/05_results.tex`, Figure 4 | Confirmed; non-significant rank association rigorously documented. |
| **Nested In-Sample OLS Gain** | $F(1, 46) = 5.676, p = 0.0214, \Delta R^2_{\text{in}} = +0.1039$ | `sections/05_results.tex`, Figure 4 | Confirmed via statsmodels regression audit. |
| **Cross-Validated OOF Gain** | $\Delta R^2_{\text{OOF}} = +0.0805$ ($0.0298 \to 0.1103$) | `sections/05_results.tex`, Figure 4 | Confirmed via 5-fold stratified CV. |
| **Bootstrap Specifications** | Rater: $B=1,000$; Item: $B=2,000$ | Table III, `sections/04_methodology_experimental_setup.tex` | Reconciled across text, table notes, and codebase. |

---

## 4. Citation and Bibliography Resolution

The BibTeX database (`references.bib`) contains 31 fully formatted, verified academic entries covering:
- **LLM-as-a-Judge & Capability Evaluation:** Chiang et al. (2023), Zheng et al. (2023), Wang et al. (2023), Tan et al. (2025), Bavaresco et al. (2025), Debenedetti et al. (2024).
- **Safety Benchmarks & Adversarial Auditing:** Zhang et al. (2024), Mazeika et al. (2024), Schwinn et al. (2026), Touvron et al. (2023).
- **Annotator Disagreement & Human-Centric AI:** Aroyo et al. (2023), Basile et al. (2021), Davani et al. (2022), Rottger et al. (2022), Gordon et al. (2021), Gordon et al. (2022).
- **Calibration, Uncertainty & Loss Functions:** Brier (1950), Guo et al. (2017), Ovadia et al. (2019), Malinin & Gales (2018), Kuhn et al. (2023).
- **Multi-Model Ensembles & Juries:** Lakshminarayanan et al. (2017), Verga et al. (2024), Qian et al. (2026), Li (2026), Feng et al. (2026), Zhang et al. (2026), Laddha et al. (2026).
- **Target Small Models & Direct Baseline:** Yang et al. (2024; Qwen2.5), Allal et al. (2025; SmolLM2), Ali (2026; reference benchmark).

A comprehensive static cross-reference and citation parse confirmed:
- **Total Citations in Text:** 31 unique cited keys.
- **Total Keys in BibTeX:** 31 entries.
- **Missing or Undefined Citations:** **0 (Zero)**.
- **Internal Cross-References:** 64 defined labels; **0 broken references**.

---

## 5. Compilation Tool Audit & Overleaf Packaging

### 5.1 Local Tool Assessment
A systematic scan of the host environment was performed for LaTeX engines:
```powershell
where.exe pdflatex; where.exe latexmk; where.exe xelatex; where.exe lualatex; where.exe tectonic
```
Result: None of the above binaries are installed on the local Windows system (only standard Python, Node.js, and IDE extensions exist).

### 5.2 Strict Adherence to User Instructions
In strict compliance with user instructions:
> *"If no local LaTeX compiler is available, do not pretend the PDF was generated. Prepare an Overleaf-ready project containing all required source files and assets, and clearly explain the remaining compilation blocker."*

We did not generate a simulated or fabricated PDF. Instead, we:
1. Sourced and bundled the official CTAN document class `IEEEtran.cls` (version 1.8b) directly into the project root, ensuring that the project does not depend on external class downloads.
2. Verified all file encodings (UTF-8) and path delimiters (forward slashes `/`).
3. Created a complete, production-grade Overleaf zip package:
   `D:\Research\TrustEval\research\paper\final_full_manuscript\TrustEval_Full_Manuscript_Overleaf.zip` (3.75 MB).
4. Authored clear step-by-step compilation instructions in `README.md`.

---

## 6. Final Quality Checklist

- [x] **Complete Research Narrative Assembled:** All 8 sections, 2 appendices, and abstract present in full detail without truncation or abbreviated summaries.
- [x] **No Imposed Page Limits:** The manuscript is formatted as a full-length IEEE research paper (12,572 words across ~15–16 rendered double-column pages); no 9-page ACM limit was applied.
- [x] **All Original Figures Present:** Figures 1, 2, 3, 4, and 6 verified present in vector PDF and 300 DPI PNG in `figures/`.
- [x] **All Original Tables Present:** Tables I, II, and III fully authored and populated with exact experimental numbers.
- [x] **Complete Appendices Included:** Appendix A (annotator filtering protocol and 19 excluded IDs) and Appendix B (conceptual selective escalation workflow and Figure 6) fully included.
- [x] **All Cross-References Validated:** 64 labels defined; 0 broken cross-references.
- [x] **All Citations Validated:** 31 literature keys cited; 0 missing BibTeX entries.
- [x] **Official Class File Bundled:** CTAN `IEEEtran.cls` (v1.8b) downloaded and verified in the project directory.
- [x] **One-Click Overleaf Archive Created:** `TrustEval_Full_Manuscript_Overleaf.zip` generated and verified.
- [x] **Original Research Preserved:** Baseline IEEE workspace, ACM TRUST workspace, `TRUSTEVAL_PAPER_V2_5_3_4.md`, and all experimental results preserved untouched.
- [x] **Zero Fabricated Claims:** Transparent disclosure that local compilation requires TeX Live/MiKTeX/Overleaf due to absent local TeX binaries.

---

## 7. Deliverable File Paths

- **Assembled Project Root:**  
  [`D:\Research\TrustEval\research\paper\final_full_manuscript\`](file:///D:/Research/TrustEval/research/paper/final_full_manuscript/)
- **Master LaTeX Entry Point:**  
  [`D:\Research\TrustEval\research\paper\final_full_manuscript\main.tex`](file:///D:/Research/TrustEval/research/paper/final_full_manuscript/main.tex)
- **Official IEEE Class File:**  
  [`D:\Research\TrustEval\research\paper\final_full_manuscript\IEEEtran.cls`](file:///D:/Research/TrustEval/research/paper/final_full_manuscript/IEEEtran.cls)
- **Complete Bibliography:**  
  [`D:\Research\TrustEval\research\paper\final_full_manuscript\references.bib`](file:///D:/Research/TrustEval/research/paper/final_full_manuscript/references.bib)
- **Overleaf One-Click Archive:**  
  [`D:\Research\TrustEval\research\paper\final_full_manuscript\TrustEval_Full_Manuscript_Overleaf.zip`](file:///D:/Research/TrustEval/research/paper/final_full_manuscript/TrustEval_Full_Manuscript_Overleaf.zip)
- **Assembly & Verification Audit:**  
  [`D:\Research\TrustEval\research\paper\final_full_manuscript\MANUSCRIPT_ASSEMBLY_REPORT.md`](file:///D:/Research/TrustEval/research/paper/final_full_manuscript/MANUSCRIPT_ASSEMBLY_REPORT.md)
