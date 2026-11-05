# TrustEval: Phase 3B Final Publication Corrections Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\paper`  
**Date:** November 2026  
**Primary Master Manuscript:** [`research/paper/TRUSTEVAL_PAPER_V2_2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_2.md)  
**Preserved Prior Manuscripts:**  
- [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_1.md) (Unchanged)  
- [`research/paper/TRUSTEVAL_PAPER_V2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2.md) (Unchanged)  
- [`research/paper/TRUSTEVAL_PAPER_DRAFT.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_DRAFT.md) (Unchanged)  

---

## 1. Executive Summary

This report documents the execution and verification of **Phase 3B: Final Publication Corrections** for the TrustEval project. Following the Phase 3A independent publication-readiness audit, all six required corrections have been incorporated into the master manuscript `TRUSTEVAL_PAPER_V2_2.md`. 

Zero model inference was re-run, no prediction caches were altered, and all underlying experimental result files remain pristine.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               Summary of Phase 3B Master Corrections                             │
├─────────────────────────┬────────────────────────────────────────────────────────────────────────┤
│ 1. Protocol Terminology │ Replaced "pre-registered protocol" with "protocol-defined             │
│                         │ experimental design" (avoiding unverified registry claims).            │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 2. Paired Test Analysis │ Documented MAE non-normality (Shapiro-Wilk W = 0.8776, p < 1e-4);       │
│                         │ explained t-test (p_Holm = 0.0425) vs. Wilcoxon (p_Holm = 0.0843)     │
│                         │ discrepancy; emphasized that MAE advantage is not non-parametrically  │
│                         │ robust while squared errors are statistically indistinguishable.       │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 3. Figure 3 Caption     │ Corrected caption from "Kernel density estimation" to "Empirical       │
│                         │ step-density histograms" matching the exact ax.hist(..., step) code.   │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 4. Calibration Citation │ Added Guo et al. (2017) citation when defining ECE-10 in Section 5.1.  │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 5. Chatbot Evaluation   │ Added Chiang et al. (2023, Vicuna) citations in Section 1 and 2.1.     │
├─────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 6. Baseline Footnote    │ Added theoretical chance-discrimination footnote (*) to Table 2 AUROC. │
└─────────────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Systematic Tracking of Master Corrections

### Correction 1: Protocol-Defined Experimental Design
- **Source Issue:** In V2.1, Section 3.2 referred to the methodology as a "pre-registered data protocol". While filesystem timestamps confirm protocol creation preceded data manifest sampling and model inference, no external registry timestamp (e.g., OSF registration DOI) exists.
- **Applied Changes in V2.2:**
  - Section 3.2: Replaced `"Consistent with our pre-registered data protocol..."` with:
    `"Consistent with our protocol-defined experimental design (research/PROTOCOL_v1.md, established November 2026):"`
  - Section 3.2 Item 1: Replaced `"pre-registered filter"` with `"protocol-defined filter"`.
  - Section 3.3: Replaced `"pre-registered seed"` with `"fixed seed 20261103"`.

### Correction 2: Paired Comparisons, Normality, and Test Discrepancy
- **Source Issue:** In V2.1, the text noted that SmolLM2 had significantly lower MAE than the ensemble under a paired $t$-test ($p_{\text{Holm}} = 0.0425$), but did not fully unpack the statistical implications of the Wilcoxon test ($p_{\text{Holm}} = 0.0843$) or test normality assumptions.
- **Applied Changes in V2.2:**
  - **Abstract (Finding 2):** Explicitly states:
    `"...SmolLM2-1.7B achieves significantly lower Mean Absolute Error than the Two-Judge Ensemble under a parametric paired t-test (MAE = 0.1734 vs. 0.2464; paired t = -2.38, unadjusted p = 0.0213, Holm-adjusted p = 0.0425). However, paired MAE differences violate normality (Shapiro-Wilk W = 0.8776, p = 9.47e-5), and under the non-parametric Wilcoxon signed-rank test, this difference does not survive multiple-comparison correction (W = 427.0, unadjusted p = 0.0421, Holm-adjusted p = 0.0843). In squared error (Soft Brier score), SmolLM2 and the Ensemble are statistically indistinguishable (MSE = 0.0628 vs. 0.0713; paired t = -0.47, unadjusted p = 0.6425, Holm-adjusted p = 0.6425)."`
  - **Section 6.3 Item 1:** Updated to reflect the test discrepancy cautiously.
  - **Section 7.1:** Added subsection `"Methodological Interpretation of Paired Test Results"` detailing:
    1. The Shapiro-Wilk normality test on paired differences ($W = 0.8776, p = 9.47 \times 10^{-5}$, skewness $= +0.7425$).
    2. Why the non-parametric Wilcoxon test is methodologically superior given the positive skewness.
    3. The conclusion that SmolLM2's sample MAE advantage is not statistically robust under non-parametric testing ($p_{\text{Holm}} = 0.0843$), while squared errors are statistically equivalent ($p_{\text{Holm}} = 0.6425$) and the ensemble delivers vastly superior discriminative ranking ($r = 0.4992, \rho = 0.5903$).

### Correction 3: Figure 3 Caption Alignment
- **Source Issue:** Figure 3's caption previously referred to "Kernel density estimation (KDE)", whereas the code in `figures.py` implements empirical step histograms (`ax.hist(..., histtype='step', density=True)`).
- **Applied Changes in V2.2:**
  - Section 8.3 caption updated to:
    `*Figure 3: Empirical step-density histograms comparing predicted model probability distributions against the empirical human consensus distribution h_primary. Human consensus exhibits a bimodal structure with peaks at low and high risk. Qwen shifts heavily rightward (\mu = 0.751), while SmolLM2 collapses into an ultra-narrow spike near 0.25. The Two-Judge Ensemble yields an intermediate distribution centered at 0.50 with coverage across both regimes.*`

### Correction 4: Guo et al. (2017) Calibration Citation
- **Source Issue:** Guo et al. (2017) was present in `references.bib` but lacked an in-text citation in the body.
- **Applied Changes in V2.2:**
  - Section 5.1 Item 4: Added explicit citation:
    `"Following the standard calibration framework for neural networks (Guo et al., 2017), ECE is computed by partitioning predictions into M=10 equally spaced decile bins B_m \subset [0, 1]:..."`

### Correction 5: Chiang et al. (2023) Chatbot Evaluation Citation
- **Source Issue:** Chiang et al. (2023, Vicuna) was present in `references.bib` but lacked an in-text citation in the body.
- **Applied Changes in V2.2:**
  - Section 1: Added citation when introducing automated evaluators:
    `"...automated evaluators—popularized by conversational benchmarks (Chiang et al., 2023; Zheng et al., 2023)—termed LLM-as-a-judge are routinely employed..."`
  - Section 2.1: Added citation in the opening sentence of Related Work:
    `"The paradigm of using language models to evaluate conversational interactions was pioneered with Vicuna (Chiang et al., 2023) and formalized by Zheng et al. (2023) with MT-Bench and Chatbot Arena..."`

### Correction 6: Constant Baseline Chance-Discrimination Footnote in Table 2
- **Source Issue:** Table 2 listed `0.5000` for the constant baseline's AUROC without an immediate visual indicator distinguishing theoretical chance performance from empirical ranking ability.
- **Applied Changes in V2.2:**
  - Table 2 cell updated to: `0.5000*`
  - Table 2 note updated to:
    `"*(Note: In Table 2, Pearson and Spearman correlations for the constant baseline are omitted as constant predictions carry no item-level ranking information; AUROC is reported at its theoretical chance level of 0.5000* [*Theoretical chance discrimination for an uninformative predictor carrying zero ranking ability].)"`

---

## 3. Comprehensive Verification of Internal Consistency

The numerical values in `TRUSTEVAL_PAPER_V2_2.md` were cross-verified against all 5 underlying JSON result artifacts:

```
Table: Cross-Verification of V2.2 Manuscript Tables against Result Artifacts
```

| Metric / Analysis | Result File Source | JSON Artifact Value | V2.2 Manuscript Value | Match Status |
| :--- | :--- | :---: | :---: | :---: |
| **Qwen MAE ($h_{\text{primary}}$)** | `evaluation_metrics_dices50.json` | $0.41521166$ | $0.4152$ | **EXACT** |
| **SmolLM2 MAE ($h_{\text{primary}}$)**| `evaluation_metrics_dices50.json` | $0.17344791$ | $0.1734$ | **EXACT** |
| **Ensemble MAE ($h_{\text{primary}}$)**| `evaluation_metrics_dices50.json` | $0.24641665$ | $0.2464$ | **EXACT** |
| **Baseline MAE ($h_{\text{primary}}$)**| `predictive_discrimination_audit.json`| $0.19827784$ | $0.1983$ | **EXACT** |
| **Qwen Soft Brier** | `evaluation_metrics_dices50.json` | $0.22020439$ | $0.2202$ | **EXACT** |
| **SmolLM2 Soft Brier** | `evaluation_metrics_dices50.json` | $0.06275310$ | $0.0628$ | **EXACT** |
| **Ensemble Soft Brier** | `evaluation_metrics_dices50.json` | $0.07125592$ | $0.0713$ | **EXACT** |
| **Baseline Soft Brier** | `predictive_discrimination_audit.json`| $0.06023690$ | $0.0602$ | **EXACT** |
| **Baseline ECE-10** | `predictive_discrimination_audit.json`| $0.0000$ | $0.0000$ | **EXACT** |
| **Ensemble Pearson $r$** | `predictive_discrimination_audit.json`| $0.49915146$ ($p=2.24\times 10^{-4}$) | $0.4992$ ($p=2.2\times 10^{-4}$) | **EXACT** |
| **Ensemble Spearman $\rho$** | `predictive_discrimination_audit.json`| $0.59026712$ ($p=6.43\times 10^{-6}$) | $0.5903$ ($p=6.4\times 10^{-6}$) | **EXACT** |
| **Qwen AUROC point** | `additional_statistical_reporting.json`| $0.75291375$ | $0.7529$ | **EXACT** |
| **Ensemble AUROC point** | `additional_statistical_reporting.json`| $0.75174825$ | $0.7517$ | **EXACT** |
| **Ensemble $-$ Qwen AUROC Diff** | `additional_statistical_reporting.json`| $-0.00116550$ | $-0.0012$ | **EXACT** |
| **AUROC Diff 95% Bootstrap CI** | `additional_statistical_reporting.json`| $[-0.05244755, +0.04428904]$ | $[-0.0524, +0.0443]$ | **EXACT** |
| **Paired $t$-test (SmolLM - Ens)** | `additional_statistical_reporting.json`| $t = -2.3799, p = 0.02125$ | $t = -2.380, p = 0.0213$ | **EXACT** |
| **Paired Wilcoxon (SmolLM - Ens)**| `additional_statistical_reporting.json`| $W = 427.0, p = 0.04214$ | $W = 427.0, p = 0.0421$ | **EXACT** |
| **Disagreement OLS $F$-statistic**| `disagreement_cv_dices50.json` | $F(1, 46) = 5.67596, p = 0.021388$ | $F(1, 46) = 5.6760, p = 0.0214$ | **EXACT** |
| **Disagreement 5-Fold OOF $\Delta R^2$**| `disagreement_cv_dices50.json` | $+0.08048989$ | $+0.0805$ | **EXACT** |
| **Rater Bootstrap 95% CIs** | `bootstrap_ci_dices50.json` | Matches Table 5 across all 12 cells | Matches Table 5 | **EXACT** |
| **Bibliography Citation Check** | `references.bib` | 26 verified entries | All 26 cited in body / Table 1 | **EXACT** |

---

## 4. Unresolved Issues and Scope Delimitations

As established in the Phase 3A audit, the following items are acknowledged as fundamental scope boundaries of this study, transparently documented in Section 10:

1. **Subgroup Demographic Alignment:** Partitioning the 50 conversations into racial, gender, and age cohorts yields sparse cell counts ($n < 10$). Complete demographic alignment analysis is reserved for the full 350-item benchmark.
2. **Spearman Rank Power for Disagreement:** While Pearson $r = 0.3125$ ($p = 0.0271$), Spearman $\rho = 0.2302$ did not reach significance at $N=50$ ($p = 0.1078$). Power calculations indicate that detecting $\rho \approx 0.23$ at $\alpha = 0.05$ with $80\%$ power requires $N \ge 146$ samples.
3. **Execution Throughput:** Software BF16 execution on consumer laptop CPU requires $\approx 135\text{ s/item}$ for the 1.7B model. Exploring 4-bit integer quantization (INT4) remains future work.

---

## 5. Verification Checklist

```
[x] TRUSTEVAL_PAPER_V2.md preserved completely unchanged (50,850 bytes)
[x] TRUSTEVAL_PAPER_V2_1.md preserved completely unchanged (57,198 bytes)
[x] TRUSTEVAL_PAPER_V2_2.md created with all six master corrections applied (58,564 bytes)
[x] PHASE_3B_CORRECTION_REPORT.md created (this report)
[x] Pre-registration language replaced with protocol-defined design
[x] Paired t-test (p_Holm = 0.0425) vs. Wilcoxon (p_Holm = 0.0843) fully explained
[x] Shapiro-Wilk non-normality (W = 0.8776, p = 9.47e-5) documented
[x] Figure 3 caption corrected to "Empirical step-density histograms"
[x] Guo et al. (2017) calibration citation added to Section 5.1
[x] Chiang et al. (2023) Vicuna citation added to Section 1 and Section 2.1
[x] Theoretical chance-discrimination footnote (*) added to Table 2 AUROC
[x] Complete numerical consistency verified across all 5 JSON result files
[x] Complete citation coverage verified across all 26 entries in references.bib
[x] Three publication figures verified embedded and high-resolution (300 DPI)
[x] Zero model inference re-runs or prediction cache modifications
```

---

## 6. Strategic Conclusion

`TRUSTEVAL_PAPER_V2_2.md` represents the complete, verified master research manuscript for TrustEval. The paper presents a rigorous, scientifically cautious defense of small open-weight LLM safety ensembling on consumer hardware. 

The manuscript is ready for venue formatting (e.g., standard ACL style for **TrustNLP 2027 at COLING 2027**, or TMLR OpenReview style) and author team review.
