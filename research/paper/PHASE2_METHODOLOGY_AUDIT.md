# TrustEval — Phase 2 Methodology and Implementation Audit Report

**Document:** `research/paper/PHASE2_METHODOLOGY_AUDIT.md`  
**Phase:** Phase 2 — Dataset, Ground Truth, Methodology, and Experimental Setup  
**Target Manuscripts Audited:**  
- `research/paper/latex/sections/03_dataset_ground_truth.tex`  
- `research/paper/latex/sections/04_methodology_experimental_setup.tex`  
- `research/paper/latex/main.tex`  
- `research/paper/latex/references.bib`  
**Date:** November 2026  
**Status:** Verification & End-to-End Traceability Complete  

---

## Executive Summary

This methodology audit establishes end-to-end mathematical, procedural, and empirical traceability for **Section III (Dataset and Ground Truth Formulation)** and **Section IV (Methodology and Experimental Setup)** of the TrustEval academic manuscript.

Every formula, data filtering step, model checkpoint, tokenizer ID, scoring calculation, metric definition, and figure asset was audited against raw code in `src/trusteval/`, configuration files in `configs/`, execution scripts in `scripts/`, and validated artifacts under `results/`.

---

## 1. Methodological Claim-to-Implementation Mapping

| Methodological Dimension | Manuscript Assertion | Implementation File & Function / Artifact | Audit Verification Details |
| :--- | :--- | :--- | :--- |
| **Benchmark Source** | Google DICES-350 ($N=350$) pinned to Git commit `b5596d9` | `configs/experiment.yaml` (lines 8–18)<br>`data/raw/diverse_safety_adversarial_dialog_350.csv` | Official CC BY 4.0 dataset containing 350 multi-turn dialogues across diverse safety categories. |
| **Evaluation Sample** | Simple random sample of $N=50$ dialogues without replacement | `data/processed/dices_50_sample_manifest.json`<br>`scripts/sample_dices50.py` | Governed by fixed random seed `20261103`. Unstratified, exploratory sample capturing $h_{\text{primary}} \in [0.0392, 0.9519]$. |
| **Initial Rater Pool** | 123 crowd annotators recruited by Google Research | `data/raw/diverse_safety_adversarial_dialog_350.csv`<br>`src/trusteval/data/preprocessor.py:filter_raters` | Audited raw column `rater_id.nunique() == 123`. |
| **Rater Exclusions** | Exactly 19 anomalous raters removed based on `removed_raters_350` | `configs/experiment.yaml` (lines 19–38)<br>`src/trusteval/data/preprocessor.py:filter_raters` | Excludes 19 author-flagged rater IDs failing attention/completion time criteria. |
| **Retained Rater Pool** | Exactly 104 annotators per conversation | `results/diagnostics/data_preparation_audit.json` $\to$ `remaining_raters` | Exactly 104 retained annotators per item across all 50 conversations. |
| **Total Evaluation Ratings** | 5,200 individual crowd ratings ($50 \times 104$) | `data_preparation_audit.json` $\to$ `remaining_rows` | $5,200$ total ratings: $4,889$ decisive ($94.02\%$) and $311$ unsure ($5.98\%$). |
| **Decisive Ratings Split** | 1,646 Unsafe (Yes) vs. 3,243 Safe (No) votes | `results/tables/ensemble_predictions_dices50.csv`<br>`data_preparation_audit.json` | $1,646 + 3,243 = 4,889$ decisive judgments. |
| **Construct Validity of $Q_{\text{overall}}$**| $Q_{\text{overall}} = \text{``Yes''} \iff \bigvee_{k=2}^6 (q_k = \text{``Yes''})$ | Verified across all 43,050 raw rows in `data/raw/diverse_safety_adversarial_dialog_350.csv` | Exactly $100\%$ precision and recall (14,064 matching rows, 0 mismatches). Hierarchical deterministic reduction. |

---

## 2. Ground-Truth Target Formulations

| Target Formulation | Mathematical Definition | Implementation File & Line | Empirical Sample Distribution ($N=50$) |
| :--- | :--- | :--- | :--- |
| **Primary Human Target ($h_{\text{primary}}$)** | $h_{\text{primary}, i} = \frac{Y_i}{Y_i + N_i}$ | `src/trusteval/data/preprocessor.py`<br>lines 94–96 (`valid_denom = y + n`) | $\bar{h}_{\text{primary}} = 0.3381$, $s = 0.2442$, $\sigma = 0.2417$<br>$\min = 0.0392$, $\max = 0.9519$<br>Pooled micro-average $= 1,646 / 4,889 = 0.336674$. |
| **Sensitivity Target ($h_{\text{sensitivity}}$)** | $h_{\text{sensitivity}, i} = \frac{Y_i + 0.5 U_i}{Y_i + N_i + U_i}$ | `src/trusteval/data/preprocessor.py`<br>lines 96–97 (`all_denom = y + n + u`) | $\bar{h}_{\text{sensitivity}} = 0.3464$, $\sigma = 0.2378$<br>Delta vs. primary: $+0.0083$ ($+0.83\%$), sensitivity analysis for Unsure partial weighting. |
| **Majority Consensus Label ($y_{\text{majority}}$)**| $y_{\text{majority}, i} = \mathbf{1}(h_{\text{primary}, i} \ge 0.5)$ | `src/trusteval/data/preprocessor.py`<br>line 99 (`np.where(h_primary >= 0.5, 1, 0)`) | 11 items majority-unsafe ($y=1$), 39 items majority-safe ($y=0$). Forms 429 concordant/discordant evaluation pairs for AUROC. |

---

## 3. Model Configuration and Inference Protocol Mapping

| Component | Specification | Implementation File & Code Location | Operational Parameters & Memory Footprint |
| :--- | :--- | :--- | :--- |
| **Judge 1** | `Qwen/Qwen2.5-0.5B-Instruct` | `configs/experiment.yaml` (lines 42–49)<br>`src/trusteval/judges/hf_judge.py` | 0.49B parameters, vocab 151,936, Apache 2.0 license. Net process RSS increase: $0.9\text{ GB}$. |
| **Judge 2** | `HuggingFaceTB/SmolLM2-1.7B-Instruct` | `configs/experiment.yaml` (lines 50–57)<br>`src/trusteval/judges/hf_judge.py` | 1.71B parameters, vocab 49,152, Apache 2.0 license. Net process RSS increase: $1.1\text{ GB}$. |
| **Prompt Protocol** | `TrustEval-R0` | `configs/prompts/safety_judge_v1.txt`<br>Hash: `15f18333a682867c...` | Standardized zero-shot prompt with context, response, 4 hazard criteria, and forced single-word Yes/No question. |
| **Prompt Serialization** | Native ChatML format | `src/trusteval/judges/hf_judge.py`<br>lines 198–200 (`apply_chat_template`) | Constructs `<\|im_start\|>system...<\|im_end\|><\|im_start\|>user...<\|im_end\|><\|im_start\|>assistant\n`. |
| **Inference Mode** | Causal next-token forward pass (no generation) | `src/trusteval/judges/hf_judge.py`<br>lines 207–210 (`torch.inference_mode()`) | Single forward pass per dialogue. Strictly 0 autoregressive token generation. |
| **Logit Location & Cast** | Index $-1$, FP32 upcast | `src/trusteval/judges/hf_judge.py`<br>line 209 (`.logits[0, -1].to(torch.float32)`) | Next-token prediction position; upcast from BF16 to FP32 guarantees numerical stability under exponentiation. |
| **Qwen Token IDs** | Yes: `9454`, No: `2753` | `results/predictions/pilot_predictions.jsonl`<br>`src/trusteval/judges/hf_judge.py` | Audited single-token encoding in Qwen tokenizer vocabulary. |
| **SmolLM2 Token IDs** | Yes: `10539`, No: `5230` | `results/predictions/pilot_predictions.jsonl`<br>`src/trusteval/judges/hf_judge.py` | Audited single-token encoding in SmolLM2 tokenizer vocabulary. |
| **Probability Formula** | $P(\text{Unsafe}) = \frac{\exp(z_{\text{Yes}} - m)}{\exp(z_{\text{Yes}} - m) + \exp(z_{\text{No}} - m)}$ | `src/trusteval/judges/hf_judge.py`<br>lines 76–82 (`calculate_binary_softmax_probabilities`) | Numerically stable binary softmax with $m = \max(z_{\text{Yes}}, z_{\text{No}})$. Yes+No mass exceeds $99.5\%$ of full vocabulary. |
| **Ensemble Formula** | $P_{\text{ens}} = 0.5(P_{\text{qwen}} + P_{\text{smol}})$ | `src/trusteval/evaluation/ensemble.py`<br>line 43 (`build_two_judge_ensemble`) | Simple unweighted linear average. |
| **Disagreement Formula**| $\Delta = \|P_{\text{qwen}} - P_{\text{smol}}\|$ | `src/trusteval/evaluation/ensemble.py`<br>line 44 (`build_two_judge_ensemble`) | Absolute probability gap; treated as exploratory candidate error correlate. |
| **Hardware Envelope** | Pure laptop x86 CPU inference | `src/trusteval/judges/hf_judge.py`<br>lines 119–122 (`torch.set_num_threads(4)`) | Pure CPU execution, 4 threads, $<1.2\text{ GB}$ peak resident set size, 0 external network dependencies. |

---

## 4. Metric Definitions and Evaluation Pipeline

| Evaluation Dimension | Metric & Mathematical Definition | Implementation File & Function | Empirical Benchmark Role |
| :--- | :--- | :--- | :--- |
| **Point Error (MAE)** | $\text{MAE} = \frac{1}{N}\sum \|P_i - h_{\text{primary}, i}\|$ | `src/trusteval/evaluation/metrics.py`<br>line 30 (`calculate_regression_metrics`) | Primary linear prediction error metric. |
| **Point Error (RMSE)** | $\text{RMSE} = \sqrt{\frac{1}{N}\sum (P_i - h_{\text{primary}, i})^2}$ | `src/trusteval/evaluation/metrics.py`<br>line 32 (`calculate_regression_metrics`) | Root mean squared prediction error. |
| **Soft MSE / Brier** | $\text{Soft MSE} = \frac{1}{N}\sum (P_i - h_{\text{primary}, i})^2$ | `src/trusteval/evaluation/metrics.py`<br>line 31 (`calculate_regression_metrics`) | Continuous Brier score against soft human consensus. |
| **Soft ECE-10** | $\sum_{k=1}^{10} \frac{N_k}{N} \|\bar{p}_k - \bar{h}_k\|$ | `src/trusteval/evaluation/metrics.py`<br>lines 41–94 (`calculate_expected_calibration_error`) | 10 equal-width bins $[b/10, (b+1)/10]$; unpopulated bins contribute 0. Populated bins tracked to expose variance collapse. |
| **Linear Association ($r$)**| Pearson product-moment correlation | `results/diagnostics/predictive_discrimination_audit.json` | Linear correlation between model probabilities and continuous human target. |
| **Monotonic Ranking ($\rho$)**| Spearman rank-order correlation | `results/diagnostics/predictive_discrimination_audit.json` | Monotonic ordering acuity across the 50 conversations. Canonical SmolLM2 $\rho = 0.3929$ ($p=0.0048$). |
| **Binary AUROC** | Mann-Whitney $U$ statistic vs. $y_{\text{majority}} = \mathbf{1}(h \ge 0.5)$ | `results/diagnostics/predictive_discrimination_audit.json`<br>`auroc_majority` | Evaluated against binary majority label (11 unsafe, 39 safe; 429 total pairs). |
| **Held-Out Baseline (OOF)** | 5-fold cross-validated out-of-fold mean prevalence | `scripts/08_run_50_experiment.py`<br>`results/tables/evaluation_metrics_dices50.json` | 5 stratified folds (seed `20261103`). Out-of-fold predictions ($\mu=0.3398$) fall into $[0.3, 0.4)$, yielding single-bin $\text{ECE} = 0.0017$. |
| **In-Sample Constant Reference**| Assigns sample mean $0.3381$ everywhere | Master manuscript Table 4 footnote | Degenerate one-bin artifact yielding $\text{ECE} = 0.0000$ (strictly distinguished from OOF baseline). |
| **Statistical Tests** | Paired $t$-test, sign test, Wilcoxon signed-rank test, Holm correction | `scripts/98_compute_phase3c_stats.py`<br>`results/tables/evaluation_metrics_dices50.json` | Reports parametric, non-parametric, and family-wise Holm-adjusted $p$-values. |
| **Rater-Cluster Bootstrap** | 1,000 resamples over 104 annotator IDs (2,000 resamples for item-level bootstrap) | `scripts/98_compute_phase3c_stats.py`<br>`src/trusteval/evaluation/bootstrap.py` | Generates 95% confidence intervals accounting for crowd annotation variance. |
| **Disagreement OLS & OOF** | Nested OLS ($F$-test) & 5-fold cross-validation ($\Delta R^2_{\text{OOF}}$) | `results/tables/disagreement_cv_dices50.json` | Nested OLS: $F(1, 46) = 5.676, p = 0.0214$; 5-fold cross-validation: descriptive $\Delta R^2_{\text{OOF}} = +0.0805$. |

---

## 5. Figure 2 Asset and Layout Verification

| Figure Property | Value / Specification | Verification Source |
| :--- | :--- | :--- |
| **Figure Number** | **Figure 2** | `VISUAL_DESIGN_BLUEPRINT.md` (Table line 96) |
| **Title** | *TrustEval Evaluation Architecture and Construct Validity* | `make_fig2_architecture.py` |
| **Vector PDF Asset** | `research/paper/latex/figures/fig2_architecture.pdf` | Verified file exists (90,808 bytes). |
| **Publication Raster** | `research/paper/latex/figures/fig2_architecture.png` | Verified file exists (496,021 bytes, 300 DPI). |
| **Generator Script** | `research/paper/latex/figures/scripts/make_fig2_architecture.py` | Reproducible script generating vector PDF from approved architecture master. |
| **Layout Placement** | Full-Width Double Column (`\begin{figure*}[t]`, `width=\textwidth`) | Placed at top of Section IV in `sections/04_methodology_experimental_setup.tex`. |
| **Diagram Workflow Content** | 1. Google DICES-350 ($N=350$) $\to$ Simple random sample ($N=50$, seed `20261103`).<br>2. **Path A:** 123 raters $\to$ 19 excluded $\to$ 104 retained, $5,200$ total ratings ($4,889$ decisive), $h_{\text{primary}} = \frac{Y}{Y+N}$ (macro mean $0.3381$).<br>3. **Path B:** `TrustEval-R0` in native ChatML $\to$ parallel Qwen2.5-0.5B + SmolLM2-1.7B on CPU ($<1.2\text{ GB}$ RSS, BF16 weights, FP32 logits) $\to$ logit extraction $\to$ $P_{\text{ens}}$ and $\Delta$.<br>4. **Convergence:** Evaluation across Point Error, Calibration, Ranking Discrimination, and Disagreement-Error Association. | Matches all specifications in `make_fig2_architecture.py` and master architecture diagram. |

---

## 6. Verification and Approval Confirmation

All methodological descriptions in Sections III and IV have been verified against raw code and data artifacts. All mathematical definitions, parameter counts, token IDs, precision handling, and cross-validation procedures are reproducible and consistent with the established scientific facts.

Phase 2 deliverables are complete and submitted for review.
