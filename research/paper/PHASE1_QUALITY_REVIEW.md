# TrustEval — Phase 1 Quality Review and Scientific Audit Report

**Document:** `research/paper/PHASE1_QUALITY_REVIEW.md`  
**Phase:** Phase 1 — Scientific Quality Review & Corrections  
**Target Manuscripts Audited:**  
- `research/paper/latex/sections/01_introduction.tex`  
- `research/paper/latex/sections/02_related_work.tex`  
- `research/paper/latex/references.bib`  
- `research/paper/FINAL_MANUSCRIPT_SOURCE_AUDIT.md`  
- `research/paper/latex/main.tex`  
- `research/paper/VISUAL_DESIGN_BLUEPRINT.md`  
**Date:** November 2026  
**Status:** Verification & Scientific Corrections Complete  

---

## Executive Summary

In accordance with pre-submission quality standards, this document presents an exhaustive scientific and academic review of the initial drafts of **Section I (Introduction)** and **Section II (Related Work)**, along with their associated bibliography and visual assets. 

Every substantive claim was audited against raw experimental results (`results/tables/`, `results/diagnostics/`) and peer-reviewed literature. Identified inconsistencies—including Figure 1's column geometry, overclaimed regulatory/privacy guarantees, uncalibrated uncertainty phrasing, and bibliographic ordering—have been rigorously corrected in the LaTeX source files.

---

## 1. Scientific Claim Audit

Every substantive assertion in Sections I and II was categorized under one of four evidential categories:
- **[EXP] Directly supported by TrustEval experimental evidence** (audited against raw data).
- **[LIT] Supported by an external cited publication** (verified against proceedings/DOIs).
- **[INT] Reasonable contextual interpretation** (standard academic framing).
- **[CORR] Unsupported or overclaimed as originally written** (corrected and qualified).

### 1.1 Special Focus Audit Areas

| Focus Area | Original Draft Formulation | Evidential Status | Scientific Correction Applied |
| :--- | :--- | :--- | :--- |
| **Privacy & GDPR/HIPAA** | *"Local on-premises execution guarantees that conversational data never traverses external network perimeters."* | **[CORR]** Overclaimed. Local inference prevents external API calls, but organizational compliance depends on end-to-end data pipeline governance. | Qualified: *"Local model inference avoids sending evaluated dialogue data to third-party model APIs, ensuring conversational data remains within internal boundaries, though institutional regulatory compliance ultimately depends on broader system-level security controls."* |
| **Cloud Dependency & API Cost** | *"Continuous offline auditing of millions of dialogue turns incurs substantial API expenditures..."* | **[INT]** Supported by industry cost realities and literature~\cite{debenedetti2024evading}. | Retained with measured academic language. |
| **Logit Obfuscation & Uncertainty** | *"Black-Box Opacity and Epistemic Blindness: Commercial APIs restrict or obfuscate token logits..."* | **[CORR]** Rhetorical phrasing ("epistemic blindness") without operational grounding. | Neutralized: *"Logit Obfuscation and Uncertainty Blindness: Commercial model APIs frequently restrict or withhold raw next-token logit distributions, preventing downstream systems from extracting continuous probability estimates..."* |
| **Adversarial Vulnerability** | References to adversarial collapse and "coin flip" failure modes. | **[LIT]** Supported by Schwinn et al.~\cite{schwinn2026coin} on adversarial distributions. | Clarified that TrustEval evaluates static conversational dialogues containing adversarial and borderline queries from DICES-350, rather than running active red-teaming/jailbreak algorithms. |
| **Epistemic Uncertainty vs. Disagreement** | *"unlocks disagreement as a localized uncertainty signal"* / *"valid surrogate signal for evaluation uncertainty"* | **[CORR]** Disagreement ($\Delta$) has nominal linear correlation ($r=0.3125, p=0.0271$) and descriptive $\Delta R^2_{\text{OOF}} = +0.0805$, but non-significant monotonic correlation ($\rho=0.2302, p=0.1078$). Not a proven uncertainty metric. | Replaced across all occurrences with: *"exploratory candidate error correlate"*, *"preliminary candidate correlate"*, or *"candidate uncertainty heuristic"*. |
| **Novelty & Ensembling Superiority** | *"An unweighted ensemble navigates this Pareto frontier, substantially outperforming both individual constituents..."* | **[CORR]** The ensemble does *not* universally dominate: SmolLM2 achieves lower MAE ($0.1734$ vs. $0.2464$), and the prevalence baseline achieves lower Soft MSE ($0.0602$ vs. $0.0713$). | Corrected: *"The Two-Judge Ensemble provides an empirical compromise, cutting Qwen's MAE by 40.6% while capturing the highest rank correlation ($\rho = 0.5903$)... The ensemble does not universally dominate: SmolLM2 achieves lower sample MAE, and a 5-fold held-out prevalence baseline achieves lower squared error."* |
| **SmolLM2 Significance Sensitivity** | Reporting SmolLM2's lowest MAE without test qualification. | **[EXP / CORR]** Paired $t$-test is significant ($p=0.0213$), but absolute differences violate normality ($W=0.8776, p < 10^{-4}$); Wilcoxon signed-rank test after Holm correction is non-significant ($W=427.0, p_{\text{adj}}=0.0843$). | Explicitly reported the non-parametric Wilcoxon Holm-adjusted test sensitivity in Contribution 2. |
| **Sub-2B Reliability Bounds** | Claiming general SLM reliability without qualification. | **[EXP]** Measured on 50-item sample with Qwen2.5-0.5B and SmolLM2-1.7B. | Bounded strictly to the investigated architectures and sample context. |

---

## 2. Reference Metadata and Support Audit

All 31 citations appearing in the text were audited against official digital libraries (IEEE Xplore, ACM DL, ACL Anthology, PMLR, OpenReview, and arXiv).

Every entry in `research/paper/latex/references.bib` now matches the **exact order of first appearance `[1]` through `[31]`** in the manuscript:

| IEEE # | Citation Key | Primary Author & Short Title | Venue & Publication Status | Identifier (DOI / arXiv) | Specific Claim Supported in Text |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **[1]** | `chiang2023vicuna` | W.-L. Chiang et al., *Vicuna* | LMSYS Blog 2023 **[Technical Blog]** | `lmsys.org/blog/2023-03-30-vicuna/` | Emergence of LLM-as-a-judge evaluation |
| **[2]** | `zheng2023judging` | L. Zheng et al., *Judging LLM-as-a-Judge* | NeurIPS 2023 **[Peer-Reviewed Conf.]** | `arXiv:2306.05685` | Formalization of MT-Bench / Chatbot Arena |
| **[3]** | `wang2023pandalm` | Y. Wang et al., *PandaLM* | ICLR 2024 **[Peer-Reviewed Conf.]** | `openreview.net/forum?id=75qZ392iX4` | Automated instruction tuning evaluation |
| **[4]** | `zhang2024safetybench`| Z. Zhang et al., *SafetyBench* | ACL 2024 Findings **[Peer-Reviewed]** | `10.18653/v1/2024.findings-acl.923` | Multiple-choice LLM safety evaluation |
| **[5]** | `mazeika2024harmbench`| M. Mazeika et al., *HarmBench* | ICML 2024 **[Peer-Reviewed Conf.]** | `proceedings.mlr.press/v235/mazeika24a.html` | Automated red-teaming safety benchmarks |
| **[6]** | `touvron2023llama` | H. Touvron et al., *LLaMA* | arXiv 2023 **[Preprint]** | `arXiv:2302.13971` | Large open foundation model baselines |
| **[7]** | `tan2025judgebench` | S. Tan et al., *JudgeBench* | ICLR 2025 **[Peer-Reviewed Conf.]** | `arXiv:2410.12781` | Biases and failure modes in LLM judges |
| **[8]** | `bavaresco2025llms` | A. Bavaresco et al., *LLMs instead of Judges?*| ACL 2025 Short **[Peer-Reviewed Conf.]** | `10.18653/v1/2025.acl-short.20` | Degradation of LLM judges on subjective NLP |
| **[9]** | `debenedetti2024evading`| E. Debenedetti et al., *Evading Classifiers* | IEEE SaTML 2024 **[Peer-Reviewed Conf.]** | `10.1109/SaTML54575.2024.00010` | Black-box vulnerabilities & privacy risks |
| **[10]**| `yang2024qwen25` | A. Yang et al., *Qwen2.5 Tech Report* | arXiv 2024 **[Preprint / Tech Report]** | `arXiv:2412.15115` | Sub-2B open-weight model architectures |
| **[11]**| `allal2025smollm2` | L. B. Allal et al., *SmolLM2* | Hugging Face 2025 **[Tech Report]** | `huggingface.co/blog/smollm2` | Sub-2B compact open-weight models |
| **[12]**| `schwinn2026coin` | L. Schwinn et al., *A Coin Flip for Safety* | ICML 2026 **[Peer-Reviewed Conf.]** | `proceedings.mlr.press/v306/schwinn26a.html` | Safety judges collapsing to chance levels |
| **[13]**| `aroyo2023dices` | L. Aroyo et al., *DICES Dataset* | NeurIPS 2023 D&B **[Peer-Reviewed]** | `arXiv:2306.11247` | Multi-annotator safety evaluation benchmark |
| **[14]**| `davani2022dealing` | A. M. Davani et al., *Dealing with Disagreements*| TACL 2022 **[Peer-Reviewed Journal]** | `10.1162/tacl_a_00449` | Modeling non-majority annotator variance |
| **[15]**| `rottger2022two` | P. Röttger et al., *Two Contrasting Paradigms* | NAACL-HLT 2022 **[Peer-Reviewed Conf.]** | `10.18653/v1/2022.naacl-main.286` | Preserving annotation perspectives in NLP |
| **[16]**| `lakshminarayanan2017simple`| B. Lakshminarayanan et al., *Deep Ensembles*| NeurIPS 2017 **[Peer-Reviewed Conf.]** | `proceedings.neurips.cc/paper/2017/hash/9ef...` | Deep ensembling for predictive uncertainty |
| **[17]**| `ovadia2019can` | Y. Ovadia et al., *Can You Trust Uncertainty?*| NeurIPS 2019 **[Peer-Reviewed Conf.]** | `proceedings.neurips.cc/paper/2019/hash/855...` | Predictive uncertainty under dataset shift |
| **[18]**| `verga2024replacing` | P. Verga et al., *Replacing Judges with Juries*| arXiv 2024 **[Preprint — Explicitly Noted]** | `arXiv:2404.18796` | Multi-judge panels mitigating individual bias |
| **[19]**| `qian2026who` | M. Qian et al., *LLM-as-a-Jury* | ICML 2026 **[Peer-Reviewed Conf.]** | `proceedings.mlr.press/v306/qian26i.html` | Voting panels of models for evaluation |
| **[20]**| `basile2021we` | V. Basile et al., *We Need to Consider Disagreement*| ACL Workshop 2021 **[Peer-Reviewed]** | `10.18653/v1/2021.bppf-1.3` | Annotator disagreement in NLP benchmarks |
| **[21]**| `gordon2021disagreement`| M. L. Gordon et al., *Disagreement Deconvolution*| ACM CHI 2021 **[Peer-Reviewed Conf.]** | `10.1145/3411764.3445694` | Aligning ML models with high disagreement |
| **[22]**| `gordon2022jury` | M. L. Gordon et al., *Jury Learning* | ACM CHI 2022 **[Peer-Reviewed Conf.]** | `10.1145/3491102.3502010` | Architecture modeling diverse annotators |
| **[23]**| `brier1950verification`| G. W. Brier, *Verification of Forecasts* | MWR 1950 **[Peer-Reviewed Journal]** | `10.1175/1520-0493(1950)078<0001:VOFEIT>...` | Probabilistic calibration and Brier score |
| **[24]**| `guo2017calibration` | C. Guo et al., *Calibration of Modern Neural Nets*| ICML 2017 **[Peer-Reviewed Conf.]** | `proceedings.mlr.press/v70/guo17a.html` | Neural net miscalibration and ECE formulation |
| **[25]**| `kuhn2023semantic` | L. Kuhn et al., *Semantic Uncertainty* | ICLR 2023 **[Peer-Reviewed Conf.]** | `openreview.net/forum?id=VD-AYtP0dve` | Dispersion across stochastic generations |
| **[26]**| `malinin2018predictive`| A. Malinin & M. Gales, *Predictive Uncertainty*| NeurIPS 2018 **[Peer-Reviewed Conf.]** | `proceedings.neurips.cc/paper/2018/hash/3ea...` | Prior networks for predictive uncertainty |
| **[27]**| `li2026calibrate` | Y. Li, *Calibrate, Don't Curate* | arXiv 2026 **[Preprint — Explicitly Noted]** | `arXiv:2605.09702` | Population estimation from noisy LLM judges |
| **[28]**| `feng2026noisy` | C. Feng et al., *Noisy but Valid* | ICLR 2026 **[Peer-Reviewed Conf.]** | `arXiv:2510.04322` | Statistical estimation with imperfect judges |
| **[29]**| `zhang2026can` | Y. Zhang et al., *Can We Trust LLM Judges?* | arXiv 2026 **[Preprint — Explicitly Noted]** | `arXiv:2609.12002` | Capability-dependent bias in LLM evaluators |
| **[30]**| `laddha2026slmjury` | A. Laddha et al., *SLMJury* | arXiv 2026 **[Preprint — Explicitly Noted]** | `arXiv:2602.04321` | SLM panels on discrete NLP tasks |
| **[31]**| `ali2026whose` | S. O. Ali, *Whose Safety Does an LLM Judge Reflect?*| Benchmark Repo 2026 **[Reference Software]** | `github.com/excel16061/whose-safety-judge` | Prior single-judge baseline on full DICES |

*Note:* All entries have been cleaned of duplicate aliases (`ali2026`, `wsj2024repository`). Every entry is cited in the narrative, and the numerical citations appear sequentially in the text without gaps or out-of-order jumps.

---

## 3. Detailed Corrections Made

1. **Figure 1 Placement and Geometry Corrected:**
   - Modified `01_introduction.tex` from `\begin{figure*}[t] ... \includegraphics[width=\textwidth]` (2-column span) to `\begin{figure}[t] ... \includegraphics[width=\columnwidth]` (single-column, $3.5\text{ in}$ width), aligning strictly with `make_fig1_tradeoff.py` and `VISUAL_DESIGN_BLUEPRINT.md`.
   - Updated Figure 1 caption to clearly state both panels, single-model polarizations, ensembling trade-offs, and the baseline reality check.
2. **Corrected TrustEval Positioning and Qualified Claims:**
   - Rewrote Contribution 3 and Section 2.6 to remove claims of "universal superiority" or "unlocking disagreement as a localized uncertainty signal".
   - Explicitly stated that ensembling is an observed empirical compromise: it reduces Qwen's MAE by $40.6\%$ and achieves top rank correlation ($\rho = 0.5903$), but does not beat SmolLM2 in MAE ($0.1734$) or the prevalence baseline in Soft MSE ($0.0602$).
   - Qualified disagreement ($\Delta$) as an "exploratory candidate error correlate" supported by nominal in-sample regression ($F=5.676, p=0.0214$) and descriptive $\Delta R^2_{\text{OOF}} = +0.0805$, while documenting non-significance under Spearman rank correlation ($\rho=0.2302, p=0.1078$).
3. **Table I (tab:framework_comparison) Alignment:**
   - Modified the "Uncertainty Signal" entry for TrustEval to "Candidate Correlate ($\Delta$)" to avoid conveying that disagreement is already an established operational uncertainty metric.
4. **Bibliography Ordering and Deduplication:**
   - Consolidated duplicate entries for Ali's reference benchmark (`ali2026whose`).
   - Integrated `touvron2023llama` into Section I, achieving a complete 31-entry bibliography where BibTeX entries are arranged in the exact order of first citation.
5. **Source Audit Synchronization:**
   - Updated `FINAL_MANUSCRIPT_SOURCE_AUDIT.md` Section 4 to reflect Figure 1's single-column specification ($3.5\text{ in}$), Figure 5's pruning decision, and the 31-reference sequence.

---

## 4. Final Figure Inventory & Layout Consistency Checks

| Figure ID | Canonical Title | Layout Width | Primary Section Anchor | Generator Script | File Assets (.pdf & .png) | Status & Verification |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- |
| **Fig. 1** | Evaluator Polarization & Trade-Off Frontier | Single-Col ($3.5\text{ in}$) | Section I (Page 1) | `make_fig1_tradeoff.py` | `figures/fig1_tradeoff.*` | **Approved & Synchronized** (`width=\columnwidth`) |
| **Fig. 2** | Evaluation Architecture & Construct Validity | Full-Width ($7.0\text{ in}$) | Section III / IV | `make_fig2_architecture.py` | `figures/fig2_architecture.*` | **Approved & Locked** (`\begin{figure*}`) |
| **Fig. 3** | Reliability Diagrams & Sample Occupancy | Single-Col ($3.5\text{ in}$) | Section V | `make_fig3_reliability.py` | `figures/fig3_reliability.*` | **Approved & Locked** (Dual-panel calib. & deciles) |
| **Fig. 4** | Disagreement Analysis as an Error Correlate | Single-Col ($3.5\text{ in}$) | Section VI | `make_fig4_disagreement.py` | `figures/fig4_disagreement.*` | **Approved & Locked** (Scatter + statistical cards) |
| **Fig. 5** | Distribution Diagnostics Across Evaluators | Single-Col ($3.5\text{ in}$) | Appendix F (Conditional) | `make_fig5_density.py` | Optional / Diagnostic | **Pruned for Brevity** (avoids $N=50$ binning noise) |
| **Fig. 6** | Conceptual Selective Escalation Architecture | Full-Width ($7.0\text{ in}$) | Appendix B | `make_fig6_escalation.py` | `figures/fig6_escalation.*` | **Approved & Locked** (Qualified banner for $\tau$) |

---

## 5. Remaining Unresolved Issues & Methodological Boundaries

The following methodological boundaries remain active and will guide Phase 2 (Sections III & IV) and subsequent sections:
1. **Exploratory Sample Scope:** Findings are grounded in an exploratory random sample of 50 conversations ($5,200$ ratings) from DICES-350. Text must continue to frame observations as sample-level empirical findings rather than universal properties of small models.
2. **Prevalence Baseline Reality:** Section V (Results) must explicitly analyze why the 5-fold held-out prevalence baseline achieves lower Soft MSE ($0.0602$) than all models, discussing quadratic loss penalties for polarized predictions.
3. **Out-of-Fold Disagreement Modeling:** The reported incremental out-of-fold gain ($\Delta R^2_{\text{OOF}} = +0.0805$) across 5 folds is descriptive and was not subjected to out-of-sample inferential hypothesis testing; it will be framed as an encouraging exploratory signal.
4. **Conceptual Escalation Workflow:** In Appendix B, Figure 6 and accompanying text will strictly qualify the escalation threshold $\tau$ as uncalibrated and illustrative.
5. **Local Compilation Bounds:** Because no TeX distribution (`pdflatex`, `latexmk`) is installed on the host OS, LaTeX source files have been verified for syntax and key resolution using automated Python scripts, without claiming local PDF compilation.

---

## Conclusion and Gate Approval

Phase 1 quality review and scientific corrections are complete. All identified issues have been remediated. Sections I and II, `references.bib`, and `FINAL_MANUSCRIPT_SOURCE_AUDIT.md` are aligned with empirical reality and publication standards.

We await your authorization before proceeding to **Phase 2 (Sections III & IV: Dataset, Methodology, and Experimental Setup)**.
