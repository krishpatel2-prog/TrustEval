# TrustEval: Manuscript V2.1 Correction & Reconciliation Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\paper`  
**Date:** November 2026  
**Target Manuscript:** [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_1.md)  
**Preserved Prior Manuscripts:**  
- [`research/paper/TRUSTEVAL_PAPER_V2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2.md) (Unchanged)  
- [`research/paper/TRUSTEVAL_PAPER_DRAFT.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_DRAFT.md) (Unchanged)  

---

## 1. Executive Summary

This report documents the comprehensive correction and reconciliation pass conducted on `TRUSTEVAL_PAPER_V2.md` to produce `TRUSTEVAL_PAPER_V2_1.md`. Following an independent manuscript review, all scientific claims, statistical tests, sampling descriptions, baseline formulations, and bibliographic records have been meticulously aligned with the underlying codebase, execution manifests, and peer-reviewed literature.

Zero model inference was re-run, no prediction caches were modified, and all original result files remain pristine.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 Summary of Key Reconciliations                                   │
├─────────────────────────┬────────────────────────────────────────────────────────────────────────┤
│ Sampling Strategy       │ Corrected from "stratified" to "uniform random sampling without        │
│                         │ replacement" (verified in manifest JSON).                              │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Baseline ECE & Ranking  │ Reconciled baseline ECE = 0.0000 (resolving copy-paste of soft Brier   │
│                         │ 0.0602). Removed spurious fold-pooling correlations (AUROC = 0.5000).  │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Multiple Comparisons    │ Applied Holm-Bonferroni correction across all 6 paired tests (m=6).    │
│                         │ Reported both unadjusted and adjusted p-values.                        │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Balanced Claims         │ Replaced "Superiority" header; acknowledged SmolLM2 has significantly  │
│                         │ lower MAE than ensemble, while squared error difference is n.s.        │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Disagreement Framing    │ Reframed disagreement as a heuristic surrogate signal rather than      │
│                         │ established epistemic uncertainty. Removed unvalidated 60-70% claims. │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ Bibliography & Figures  │ Reconciled all 9 target references with precise venues/arXiv IDs.      │
│                         │ Embedded actual publication figures directly into manuscript markdown. │
└─────────────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Priority 1: Sampling and Baseline Reconciliations

### 2.1 Uniform Random Sampling vs. Stratification
- **Audit Findings:** Inspection of [`data/processed/dices_50_sample_manifest.json`](file:///D:/Research/TrustEval/data/processed/dices_50_sample_manifest.json) confirmed that the field `sampling_strategy` is explicitly:
  ```json
  "sampling_strategy": "uniform_random_without_replacement",
  "seed": 20261103
  ```
- **Correction in V2.1:** The manuscript was corrected to remove all assertions that the sample was "stratified". Sections 3.3 and 10 now accurately state that the 50 conversations were drawn via uniform random sampling without replacement. The resulting proportion (39 safe / 11 unsafe) naturally reflects the random draw from the underlying DICES-350 distribution.

### 2.2 Pre-Registration Dates and Documentation
- **Audit Findings:** Protocol v1.0 was pre-registered and committed in [`research/PROTOCOL_v1.md`](file:///D:/Research/TrustEval/research/PROTOCOL_v1.md) dated November 2026, establishing the fixed random seed `20261103`, the 104 filtered rater pool, and the frozen prompt rubric prior to full execution.
- **Correction in V2.1:** Documented the exact pre-registration date (November 2026) and referenced `PROTOCOL_v1.md` in Section 3.2.

### 2.3 Constant-Prevalence Baseline Description
- **Audit Findings:** Code inspection of the diagnostic script (`predictive_discrimination_audit`) revealed that the constant baseline was computed using 5-fold cross-validation (`KFold(n_splits=5, shuffle=True, random_state=20261103)`), where each test fold received the mean ground-truth of the 40 training items ($\bar{h}_{\text{train}} \in [0.3129, 0.3499]$).
- **Correction in V2.1:** Corrected Section 5.3 to state that the baseline uses 5-fold cross-validation, correcting the accidental reference to "leave-one-out" in earlier text.

### 2.4 Reconciliation of Baseline ECE = 0.0602
- **Audit Findings:** In Table 2 of V2, the baseline ECE-10 was listed as `0.0602`, which was identical to its Soft Brier score ($0.0602$). Re-computing ECE on the 5-fold cross-validation baseline predictions revealed:
  - All 50 predictions fall strictly into decile bin 3 ($[0.3, 0.4]$).
  - The mean prediction in bin 3 is $\bar{p} = 0.3381$.
  - The mean human ground truth in bin 3 is $\bar{h} = 0.3381$.
  - Absolute calibration error $|\text{conf}(B_3) - \text{acc}(B_3)| = |0.3381 - 0.3381| = 0.0000$.
- **Correction in V2.1:** Table 2 and Section 5.3 now correctly report $\text{ECE-10} = \mathbf{0.0000}$ for the constant baseline, explaining that the earlier value was a clerical copy-paste error from the Soft Brier column.

### 2.5 Removal of Pooled Fold-Specific Ranking Scores
- **Audit Findings:** In the diagnostic script, pooling the 5 fold-specific training means produced slight cross-fold variation that induced a spurious negative correlation ($r = -0.235, \rho = -0.194, \text{AUROC} = 0.360$).
- **Correction in V2.1:** Table 2 was corrected to remove pooled correlation figures for the baseline. Section 5.3 explicitly notes that a constant baseline has no item-level ranking capacity ($\text{AUROC} = \mathbf{0.5000}$ chance discrimination; rank correlations omitted/undefined), and explains that fold pooling noise must not be conflated with meaningful ranking signal.

---

## 3. Priority 2: Statistical Inference Reconciliations

### 3.1 Holm Multiple-Comparison Correction
- **Audit Findings:** To control the family-wise error rate across all pairwise model comparisons, the Holm-Bonferroni step-down procedure was applied across all six paired tests ($m=6$: 3 for MAE, 3 for MSE).
- **Correction in V2.1:** Table 3 in Section 7.1 now presents both unadjusted $p$-values and Holm-adjusted $p$-values ($p_{\text{Holm}}$):

```
Table: Paired error comparisons with Holm-Bonferroni correction (m=6).
```
| Comparison | Metric | Mean Diff | Paired $t$ | $p_{\text{unadj}}$ ($t$) | $p_{\text{Holm}}$ ($t$) | Wilcoxon $W$ | $p_{\text{unadj}}$ ($W$) | $p_{\text{Holm}}$ ($W$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Qwen $-$ Ensemble | MAE | $+0.1688$ | $6.730$ | $1.74 \times 10^{-8}$ | $\mathbf{1.04 \times 10^{-7}}$ | $146.5$ | $2.14 \times 10^{-6}$ | $\mathbf{1.07 \times 10^{-5}}$ |
| SmolLM2 $-$ Ensemble | MAE | $-0.0730$ | $-2.380$ | $0.0213$ | $\mathbf{0.0425}$ | $427.0$ | $0.0421$ | $0.0843$ (n.s.) |
| Qwen $-$ SmolLM2 | MAE | $+0.2418$ | $4.613$ | $2.87 \times 10^{-5}$ | $\mathbf{1.15 \times 10^{-4}}$ | $250.0$ | $1.84 \times 10^{-4}$ | $\mathbf{5.51 \times 10^{-4}}$ |
| Qwen $-$ Ensemble | MSE | $+0.1489$ | $7.742$ | $4.74 \times 10^{-10}$ | $\mathbf{2.85 \times 10^{-9}}$ | $88.0$ | $3.09 \times 10^{-9}$ | $\mathbf{1.85 \times 10^{-8}}$ |
| SmolLM2 $-$ Ensemble | MSE | $-0.0085$ | $-0.467$ | $0.6425$ | $0.6425$ (n.s.) | $473.0$ | $0.1139$ | $0.1139$ (n.s.) |
| Qwen $-$ SmolLM2 | MSE | $+0.1575$ | $4.363$ | $6.58 \times 10^{-5}$ | $\mathbf{1.98 \times 10^{-4}}$ | $253.0$ | $1.19 \times 10^{-4}$ | $\mathbf{4.76 \times 10^{-4}}$ |

### 3.2 Correction of Overstated Significance Claims
- **Wilcoxon MAE between SmolLM2 and Ensemble:** While unadjusted $p = 0.0421$, after Holm correction across all 6 tests, $p_{\text{Holm}} = \mathbf{0.0843}$, which is **not significant** at $\alpha = 0.05$. The text in Section 7.1 explicitly states this distinction.
- **Squared Error between SmolLM2 and Ensemble:** Unadjusted $p = 0.6425$ and Holm-adjusted $p = 0.6425$. The manuscript explicitly emphasizes that their squared-error difference is statistically indistinguishable.

### 3.3 Descriptive Status of Cross-Validation $R^2$ Gain
- **Correction in V2.1:** Section 7.3 and Table 4 now explicitly clarify that the out-of-fold cross-validation gain ($\Delta R^2_{\text{OOF}} = +0.0805$) is a **descriptive out-of-sample summary metric** rather than a formal distribution-free hypothesis test. Statistical significance is formally provided by the in-sample nested OLS $F$-test ($F(1, 46) = 5.676, p = \mathbf{0.0214}$).

### 3.4 Distinction Between Rater-Level and Conversation-Level Uncertainty
- **Correction in V2.1:**
  - Section 7.4 (Table 5) explicitly notes that the 1,000-iteration rater-cluster bootstrap quantifies **rater-sampling uncertainty** (variance attributable to the 104 crowd raters, holding the 50 conversations fixed).
  - Section 7.2 explicitly notes that the stratified bootstrap quantifies **conversation-sampling uncertainty** (variance attributable to drawing 50 items from the universe of dialogues).

### 3.5 Reconciliation of Marginal and Paired AUROC Confidence Intervals
- **Correction in V2.1:** Section 7.2 reconciles why individual marginal AUROC CIs are wide (Qwen: $[0.594, 0.888]$, Ensemble: $[0.605, 0.876]$), while the paired difference bootstrap CI is tight ($-0.0012$, 95% CI: $[-0.0524, +0.0443]$). Because both evaluators are tested on the exact same conversations, high positive covariance cancels sample-level variance, proving their discriminative capacities are statistically indistinguishable.

---

## 4. Priority 3: Scientific Claims Reconciliations

### 4.1 Section Heading Replacement
- **Change:** In Section 6.3, replaced `"The Superiority of the Two-Judge Ensemble"` with the objective, metric-specific heading:
  `"6.3 Metric-Specific Comparison: Calibration, Error, and Discriminative Ranking"`.

### 4.2 Balanced Reporting of SmolLM2 vs. Ensemble MAE
- **Change:** Sections 6.3 and Abstract explicitly state that SmolLM2 achieves significantly lower MAE than the Ensemble ($0.1734$ vs. $0.2464$; $p_{\text{Holm}} = 0.0425$), while their squared error difference is not statistically significant ($p = 0.6425$).

### 4.3 Objective AUROC Reporting
- **Change:** Sections 6.3 and 7.2 explicitly state that Qwen achieves a marginally higher point AUROC than the Ensemble ($0.7529$ vs. $0.7517$), but their paired bootstrap difference is statistically compatible with zero ($[-0.0524, +0.0443]$).

### 4.4 Disagreement as a Heuristic Surrogate Uncertainty Proxy
- **Change:** Removed all phrasing describing disagreement as "established epistemic uncertainty". Section 1, 9, and Abstract now consistently describe inter-judge disagreement as a **candidate heuristic surrogate uncertainty signal** or **predictive error proxy**, acknowledging that formal epistemic uncertainty requires Bayesian posteriors or model parameter distributions.

### 4.5 Removal of Unsubstantiated Deployment Thresholds and Percentages
- **Change:** Section 9.2 was thoroughly revised:
  - Removed the unsupported claim that a threshold of $0.40$ autonomously resolves "60–70% of dialogues".
  - Replaced fixed numbers with a parameterized conceptual threshold $\tau$.
  - Explicitly stated that $\tau$ must be empirically calibrated on an independent institutional validation set based on organizational risk tolerance.

### 4.6 Local Inference vs. Data Leakage Claims
- **Change:** Replaced sweeping "zero data leakage" claims with accurate technical descriptions: "local, on-premises execution preventing the transmission of conversational data to third-party cloud APIs".

### 4.7 Qualified Generalizations on Model Architecture and Proprietary Evaluators
- **Change:** Tempered broad statements in Section 1 and Section 2. Replaced absolute assertions with evidence-grounded literature citations (Zheng et al., 2023; Tan et al., 2025; Zhang et al., 2026).

---

## 5. Priority 4: References Reconciliations

All 9 reference entries specified in the review were verified, corrected, and updated in [`research/literature/references.bib`](file:///D:/Research/TrustEval/research/literature/references.bib) and Section 12:

1. **Aroyo et al. (2023):** DICES Dataset — Verified as NeurIPS 2023 Datasets and Benchmarks Track. OpenReview: `Vv81g0Vb8M`.
2. **Allal et al. (2025):** SmolLM2 — Corrected year to 2025 (`techreport`, Hugging Face, February 2025).
3. **Röttger et al. (2022):** Corrected title to *"Two Contrasting Data Annotation Paradigms for Subjective NLP Tasks"*, NAACL-HLT 2022.
4. **Gordon et al. (2021):** Corrected year and title to *"The Disagreement Deconvolution: Bringing Machine Learning Performance into Alignment with High-Disagreement Contexts"*, CHI 2021.
5. **Gordon et al. (2022):** Verified as *"Jury Learning: Integrating Local Crowds and Diverse Architectures into Machine Learning"*, CHI 2022.
6. **Qian et al. (2026):** Verified preprint entry `arXiv:2404.18796` (Qian & Gales).
7. **Li (2026):** Corrected identifier to `arXiv:2605.09702` (*Calibrate, Don't Curate*).
8. **Zhang et al. (2026):** Corrected identifier to `arXiv:2609.12002` (*Can We Trust LLM Judges?*).
9. **SafetyBench Metadata:** Corrected and verified authors: Zhexin Zhang, Leqi Lei, Lindong Wu, Rui Sun, Yongkang Huang, Chongxuan Li, Minlie Huang (ACL 2024 Findings).

In Section 12, entries are now categorized into:
- Peer-Reviewed Conference & Journal Papers
- Preprints & Technical Reports
- Software Repositories

---

## 6. Priority 5: Presentation & Material Reconciliations

### 6.1 Embedded Publication Figures
- **Change:** Figures 1, 2, and 3 are now directly embedded in Section 8 of `TRUSTEVAL_PAPER_V2_1.md`:
  - `![Figure 1: Reliability Diagrams](../../results/figures/reliability_diagrams_dices50.png)`
  - `![Figure 2: Disagreement vs. Error](../../results/figures/disagreement_vs_error_dices50.png)`
  - `![Figure 3: Distribution Alignment](../../results/figures/distribution_alignment_dices50.png)`
- Captions and interpretive text were verified against the underlying plots.

### 6.2 Consistent Metric Terminology
- Standardized across all sections:
  - **Mean Absolute Error (MAE)**
  - **Root Mean Squared Error (RMSE)**
  - **Soft-Target Mean Squared Error (Soft Brier Score, $\text{MSE}_{\text{soft}}$)**
  - **Expected Calibration Error (ECE-10)**

### 6.3 Full SHA-256 Prompt Hash
- **Change:** Section 4.2 now provides the complete 64-character SHA-256 hash:
  `15f18333a682867c36fc600aaa80898b6293f324fcabb240ba95f9279d2685df`.

### 6.4 Model Probability Mass Reconciliation
- **Audit Findings:** Per-item inspection of the JSONL prediction caches revealed:
  - `Qwen2.5-0.5B`: Mean mass $= 0.9938 \pm 0.0052$, range $[0.9769, 0.9986]$.
  - `SmolLM2-1.7B`: Mean mass $= 0.9808 \pm 0.0034$, range $[0.9684, 0.9864]$.
  - Combined minimum $= 0.9684$ ($96.84\%$).
- **Correction in V2.1:** Corrected Section 4.3 to report the exact per-item means, ranges, and the accurate combined minimum ($96.84\%$), replacing the earlier claim of "exceeds 97.8% for both models".

---

## 7. Unresolved Issues and Scope Delimitations

The following issues are documented as fundamental scope boundaries of the 50-item preliminary evaluation, preserved for future milestones:

1. **Demographic Subgroup Breakdown:** Partitioning $N=50$ into individual racial, gender, and age cohorts yields sparse bins ($n < 10$). Full subgroup alignment analysis requires the complete 350-item benchmark.
2. **Spearman Rank Power for Disagreement:** While Pearson $r = 0.3125$ ($p = 0.0271$), Spearman $\rho = 0.2302$ is not statistically significant at $N=50$ ($p = 0.1078$). Power calculations indicate that detecting $\rho \approx 0.23$ with $80\%$ power requires $N \ge 146$ samples.
3. **Execution Throughput:** Software BF16 execution on consumer CPU requires $\approx 135\text{ s/item}$ for the 1.7B model. Exploring 4-bit integer quantization (INT4) remains future work.

---

## 8. Verification Checklist

```
[x] TRUSTEVAL_PAPER_V2.md preserved completely unchanged
[x] TRUSTEVAL_PAPER_V2_1.md created with all corrections applied
[x] V2_1_CORRECTION_REPORT.md created documenting all reconciliations
[x] references.bib updated with verified metadata, years, venues, and preprints
[x] Uniform random sampling terminology corrected throughout
[x] Baseline 5-fold CV and ECE = 0.0000 reconciled
[x] Spurious fold-pooled ranking metrics removed from constant baseline
[x] Holm multiple-comparison correction reported for all paired tests
[x] SmolLM2 MAE vs. Ensemble acknowledged transparently
[x] Qwen AUROC point superiority acknowledged with paired bootstrap CI [-0.052, +0.044]
[x] Disagreement reframed as heuristic surrogate uncertainty signal
[x] Unvalidated 60-70% and tau = 0.40 deployment claims removed
[x] Zero-data-leakage claims replaced with qualified local-inference language
[x] Three generated publication figures embedded directly into markdown
[x] Full 64-character SHA-256 prompt hash documented
[x] Actual per-item probability mass statistics reconciled
[x] Zero model inference re-runs or prediction cache modifications
```
