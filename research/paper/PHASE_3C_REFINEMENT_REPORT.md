# TrustEval: Phase 3C Final Scientific Refinement Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\paper`  
**Date:** November 2026  
**Primary Master Manuscript:** [`research/paper/TRUSTEVAL_PAPER_V2_3.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_3.md)  
**Preserved Prior Manuscripts:**  
- [`research/paper/TRUSTEVAL_PAPER_V2_2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_2.md) (Unchanged, 58,840 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_1.md) (Unchanged, 57,198 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2.md) (Unchanged, 50,850 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_DRAFT.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_DRAFT.md) (Unchanged, 17,676 bytes)  

---

## 1. Executive Summary

This report documents the completion of **Phase 3C: Final Scientific Refinement** for the TrustEval project. Following the Phase 3A independent publication-readiness audit and the Phase 3B initial correction pass, Phase 3C addresses eleven targeted scientific, statistical, citation, and tabular refinements to elevate the manuscript to a rigorous, publication-grade academic artifact: [`TRUSTEVAL_PAPER_V2_3.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_3.md) (64,874 bytes).

All original raw prediction caches (`results/predictions/`), baseline outputs, and metric tables remain strictly untouched. To provide full statistical depth for Phase 3C without touching frozen data, diagnostic script [`scripts/98_compute_phase3c_stats.py`](file:///D:/Research/TrustEval/scripts/98_compute_phase3c_stats.py) was executed to calculate paired effect sizes (Cohen's $d_z$), non-parametric sign tests, and bootstrap confidence intervals, storing verified values in [`results/diagnostics/phase_3c_statistical_refinements.json`](file:///D:/Research/TrustEval/results/diagnostics/phase_3c_statistical_refinements.json).

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 Summary of Phase 3C Refinements                                        │
├──────────────────────────┬─────────────────────────────────────────────────────────────────────────────┤
│ 1. Table 2 Highlighting  │ Disentangled overall best vs. model-specific best; marked Constant Baseline │
│                          │ lowest RMSE (0.2454) & Soft MSE (0.0602), SmolLM2 lowest MAE (0.1734),      │
│                          │ Ensemble highest Pearson (0.4992) & Spearman (0.5903), Qwen AUROC (0.7529).│
│                          │ Added footnote explaining Baseline ECE = 0.0000* as degenerate artifact.    │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 2. SmolLM2 Nuanced View  │ Balanced severe probability compression ([0.201, 0.316]) against positive   │
│                          │ monotonic rank correlation (Spearman rho = 0.3929, p = 0.0048).             │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 3. Logit Probability Mass│ Decoupled conditional Yes/No probability, full-vocabulary mass coverage     │
│                          │ (M > 0.9684), and generative formatting compliance in Section 4.3.         │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 4. Metric Categorization │ Structured Section 5.1 into 3 distinct categories: Prediction Approximation │
│                          │ Error (MAE/RMSE/MSE), Calibration (ECE-10), and Discrimination/Ranking.     │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 5. Paired Significance   │ Added Shapiro-Wilk (W = 0.8776), paired t-test (p_Holm = 0.0425), Wilcoxon  │
│                          │ (p_Holm = 0.0843), sign test (p = 0.0026), Cohen's dz, & paired CIs.       │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 6. CV & Length Metrics   │ Explicitly recorded KFold seed (20261103) and character count definition     │
│                          │ (len(response)) for regression experiments.                                 │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 7. Balanced Conclusions  │ Moderated ensemble mean prediction to 0.502; highlighted that Qwen AUROC    │
│                          │ edge is statistically indistinguishable from 0 under bootstrap CI.          │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 8. Environment Specs     │ Documented Python 3.12.7, PyTorch 2.13.0+cpu, Transformers 5.13.1, Apache   │
│                          │ 2.0 / CC BY 4.0 licenses, and physical RSS (<1.2 GB) vs. committed pagefile.│
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 9. Citation Updates      │ Updated DICES title to official NeurIPS title; updated Qian et al. to       │
│                          │ official published ICML 2026 proceedings (PMLR 306).                        │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 10. Abstract & Conclusion│ Removed speculative "60-70% automation" claim; positioned routing pipeline  │
│                          │ as a conceptual architecture for future empirical validation.               │
├──────────────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ 11. Author & Ethics      │ Added standard double-blind placeholder notice and ethics statement.        │
└──────────────────────────┴─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Systematic Tracking of Master Refinements in V2.3

### Refinement 1: Table 2 Results Presentation & Baseline ECE Footnote
- **Issue:** In prior versions, Table 2 bolded SmolLM2's MAE and Ensemble's correlation metrics, but did not clearly distinguish between the constant baseline's statistical minimums in RMSE/Soft MSE and model-specific metrics. Furthermore, the baseline's ECE of `0.0000` appeared to imply optimal calibration rather than an artifact of single-bin grouping.
- **Resolution in V2.3:**
  - Table 2 bolding was systematically clarified:
    * Lowest MAE: **0.1734** (SmolLM2-1.7B)
    * Lowest RMSE: **0.2454** (Constant Baseline)
    * Lowest Soft Target MSE: **0.0602** (Constant Baseline; model lowest is **0.0628** for SmolLM2)
    * Lowest ECE-10: **0.0000\*** (Constant Baseline artifact; model lowest is **0.0658** for SmolLM2)
    * Highest Pearson $r$: **0.4992** (Two-Judge Ensemble)
    * Highest Spearman $\rho$: **0.5903** (Two-Judge Ensemble)
    * Highest AUROC: **0.7529** (Qwen2.5-0.5B; Ensemble is comparable at 0.7517)
  - Table 2 Notes expanded:
    `"*(Note: In Table 2, Pearson and Spearman correlations for the constant baseline are omitted as constant predictions carry zero item-level ranking variance; AUROC is reported at its theoretical chance level of 0.5000* [Theoretical chance discrimination for an uninformative predictor]. The Constant Baseline ECE of 0.0000* is a mathematical artifact of all predictions falling into a single bin [0.2, 0.3) matching the empirical mean prevalence (0.2483), not evidence of informative probability calibration. Bold values indicate the top performance within each column. For RMSE and Soft MSE, the constant baseline achieves the lowest overall error, while SmolLM2 achieves the lowest error among predictive models.)"`

### Refinement 2: Nuanced Interpretation of SmolLM2-1.7B
- **Issue:** The manuscript previously risked presenting SmolLM2 either as a failed model (due to extreme probability compression $[0.201, 0.316]$ and AUROC $0.6690$) or as superior (due to low MAE).
- **Resolution in V2.3:**
  - Section 6.2, 6.3, and 7.1 now balance these two realities:
    1. **Failure of Dynamic Range:** SmolLM2 fails to produce confident binary judgements, compressing all outputs into a narrow window around the dataset prior ($[0.201, 0.316]$), which allows it to minimize linear distance to $h_{\text{primary}}$.
    2. **Retention of Monotonic Signal:** Despite range compression, SmolLM2 achieves a **statistically significant positive Spearman rank correlation** with human consensus ($\rho = \mathbf{0.3929}, p = \mathbf{0.0048}$), demonstrating that its internal logits correctly order safer vs. more harmful conversations. It is not an unguided constant-prevalence predictor.

### Refinement 3: Decoupling Probability Mass, Conditional Probability, and Generation Compliance
- **Issue:** Section 4.3 previously conflated the conditional softmax over `Yes`/`No` tokens with the total vocabulary probability mass and multi-token generative instruction compliance.
- **Resolution in V2.3:**
  - Section 4.3 was rewritten to establish three formal distinctions:
    1. **Full-Vocabulary Probability Mass ($M$):** $M = P_{\mathcal{M}}(\text{"Yes"} \mid x) + P_{\mathcal{M}}(\text{"No"} \mid x)$. In our audit, $M > 0.9684$ across all 50 items for both models, demonstrating that the next-token probability mass is almost entirely captured by the binary decision tokens.
    2. **Conditional Target Probability ($P$):** $P = \frac{P_{\mathcal{M}}(\text{"Yes"} \mid x)}{P_{\mathcal{M}}(\text{"Yes"} \mid x) + P_{\mathcal{M}}(\text{"No"} \mid x)}$, isolating relative belief.
    3. **Generative Formatting Compliance:** Direct logit interrogation bypasses multi-token autoregressive generation entirely. Thus, high probability mass $M$ does *not* prove that the model would adhere to strict single-token formatting during unconstrained autoregressive decoding.

### Refinement 4: Rigorous Three-Way Metric Categorization
- **Issue:** In earlier drafts, MAE and Soft Target MSE were occasionally described colloquially as "calibration errors."
- **Resolution in V2.3:**
  - Section 5.1 cleanly partitions evaluation into three distinct mathematical dimensions:
    1. **Prediction Approximation Error:** MAE, RMSE, and Soft-Target MSE ($\text{MSE}_{\text{soft}} = \text{RMSE}^2$). Measures absolute and squared deviations from the continuous human consensus target $h_{\text{primary}} \in [0, 1]$.
    2. **Probability Calibration:** ECE-10 (Expected Calibration Error partitioned into $M=10$ uniform bins). Measures grouping alignment between binned confidence and empirical safety rate.
    3. **Discrimination and Ranking:** Pearson linear correlation ($r$), Spearman monotonic rank correlation ($\rho$), and AUROC (binarized at $h_{\text{primary}} \ge 0.5$). Measures relative ordering capacity independent of scale.

### Refinement 5: Exhaustive Paired Statistical Significance & Robustness
- **Issue:** Evaluator comparisons required formal test statistics, normality diagnostics, effect sizes, and non-parametric verification.
- **Resolution in V2.3:**
  - Section 6.3 and Section 7.1 were expanded with exact values from [`phase_3c_statistical_refinements.json`](file:///D:/Research/TrustEval/results/diagnostics/phase_3c_statistical_refinements.json):
    * **Normality Check:** Shapiro-Wilk test on paired MAE differences ($|P_{\text{smollm}} - h| - |P_{\text{ensemble}} - h|$) yields $W = 0.8776, p = 9.47 \times 10^{-5}$ (violating normality, positive skewness $+0.7425$).
    * **Parametric Paired $t$-test:** $t = -2.380, p_{\text{unadj}} = 0.0213, p_{\text{Holm}} = 0.0425$; Cohen's $d_z = -0.337$.
    * **Non-Parametric Wilcoxon Signed-Rank Test:** $W = 427.0, Z = -2.032, r = -0.287, p_{\text{unadj}} = 0.0421, p_{\text{Holm}} = 0.0843$ (fails to reach significance under Holm correction at $\alpha = 0.05$).
    * **Two-Sided Sign Test:** SmolLM2 achieves lower absolute error on 36 conversations, Ensemble achieves lower error on 14, with 0 ties ($p = 0.00260$).
    * **Paired Item Bootstrap 95% CI (2,000 resamples):** $[-0.1298, -0.0101]$.
    * **Paired Rater-Cluster Bootstrap 95% CI (1,000 resamples):** $[-0.0935, -0.0355]$.
    * **Squared Error (Soft MSE) Equivalence:** In Soft MSE, SmolLM2 vs. Ensemble yields paired $t = -0.467, p = 0.6425, d_z = -0.066$; paired item bootstrap 95% CI $[-0.0414, +0.0290]$; paired rater bootstrap 95% CI $[-0.0256, +0.0091]$ (straddles zero).
    * **Qwen vs. Ensemble Significance:** Qwen suffers massive error relative to the ensemble: MAE difference $+0.1688$ ($t = 6.730, p_{\text{Holm}} = 1.04 \times 10^{-7}, d_z = 0.952$; Wilcoxon $p_{\text{Holm}} = 1.07 \times 10^{-5}$); Soft MSE difference $+0.1489$ ($t = 7.742, p_{\text{Holm}} = 2.85 \times 10^{-9}, d_z = 1.095$).

### Refinement 6: Cross-Validation & Metric Reproducibility Parameters
- **Issue:** Section 6.4 (Disagreement Analysis) described 5-fold cross-validation and response length controls without explicitly stating the random seed and the exact metric unit for length.
- **Resolution in V2.3:**
  - Section 6.4 explicitly states:
    `"Using 5-fold cross-validation with a fixed random seed (seed 20261103) and controlling for conversational response length defined strictly as character count (len(response)), adding ensemble disagreement to the baseline length predictor..."`

### Refinement 7: Balanced Interpretations & Neutrality
- **Issue:** Prior phrasing overstated ensemble uniformity or single-model supremacy.
- **Resolution in V2.3:**
  - **Qwen AUROC vs. Ensemble AUROC:** Section 6.2 and 7.1 emphasize that while Qwen achieves a higher point AUROC ($0.7529$ vs. $0.7517$), the paired item-level difference is $-0.0012$ with a 95% bootstrap confidence interval of $[-0.0524, +0.0443]$, confirming that the two models have statistically indistinguishable discriminative capacity.
  - **Ensemble Mean Calibration:** Clarified that the ensemble's mean prediction is $0.502$ (moderating Qwen's $0.751$ positive bias, but still above the empirical sample prevalence of $0.248$).
  - **Disagreement Routing:** Clarified that ensemble disagreement ($\Delta_{\text{ens}}$) serves as an informative *heuristic routing signal* ($\Delta R^2_{\text{OOF}} = +0.0805, F(1,46) = 5.68, p = 0.0214$) rather than a standalone safety detector.

### Refinement 8: Operational Environment & Licensing Specifications
- **Issue:** System specifications required exact versioning, license declarations, and precise memory accounting.
- **Resolution in V2.3:**
  - Section 3.1 and 3.3 document:
    * Python 3.12.7 (64-bit AMD64)
    * PyTorch 2.13.0+cpu
    * Hugging Face Transformers 5.13.1
    * Hardware: Intel Core i7-13700H (14 cores / 20 threads), 32 GB RAM, Windows 11
    * Open-source licenses: DICES dataset (CC BY 4.0), Qwen2.5-0.5B (Apache 2.0), SmolLM2-1.7B (Apache 2.0).
    * Memory dynamics: Process physical resident set size (RSS) peaked at $952.1\text{ MB}$ for Qwen and $1,189.1\text{ MB}$ for SmolLM2 (under the $1.2\text{ GB}$ physical threshold). Virtual committed pagefile memory temporarily reached $\approx 2.4\text{ GB}$ during initial PyTorch tensor weight deserialization before settling.

### Refinement 9: Bibliography & Citation Updates
- **Issue:** DICES was listed with an informal workshop title, and Qian et al. (LLM-as-a-Jury) was cited as an arXiv preprint rather than its final published ICML 2026 proceedings version.
- **Resolution in V2.3:**
  - Updated [`research/literature/references.bib`](file:///D:/Research/TrustEval/research/literature/references.bib):
    * DICES: `"DICES Dataset: Diversity in Conversational AI Evaluation for Safety"`, NeurIPS 2023 Datasets and Benchmarks Track.
    * Qian et al.: `"LLM-as-a-Jury: Evaluating Conversational AI with Committee of Language Models"`, *Proceedings of the 43rd International Conference on Machine Learning (ICML 2026)*, PMLR 306, authors: Mengjie Qian, Guangzhi Sun, Mark Gales, and Kate Knill.
  - Table 1 was updated to reflect Qian et al. as a published conference paper (`Conf`).

### Refinement 10: De-escalation of Speculative Operational Claims
- **Issue:** Earlier drafts claimed a selective escalation routing policy would "automate 60-70% of evaluation volume."
- **Resolution in V2.3:**
  - Abstract and Section 7.2 removed the unsupported 60-70% figure.
  - Phrased strictly as an architectural proposal:
    `"We outline a selective escalation architecture wherein low-disagreement items are routed to small local ensembles and high-disagreement items are escalated to frontier models or human moderators, proposing this two-tier topology as an empirical hypothesis for future multi-tier benchmarking."`

### Refinement 11: Double-Blind Authorship Notice & Ethics Declaration
- **Issue:** The manuscript required formal anonymization placeholders and an ethical impact statement.
- **Resolution in V2.3:**
  - Added formal header: `Anonymous Authors (Paper under double-blind peer review)`.
  - Added Section 11: **Ethical Considerations and Responsible AI**, addressing rater diversity, demographic representation, and risks of deploying small LLM judges in safety-critical automated moderation pipelines.

---

## 3. Comprehensive Numerical Consistency Verification

Every numerical figure presented in `TRUSTEVAL_PAPER_V2_3.md` was cross-referenced across the primary experimental artifacts:

| Metric / Analysis | Result File Source | JSON Artifact Value | V2.3 Value | Verification Status |
| :--- | :--- | :---: | :---: | :---: |
| **Qwen MAE ($h_{\text{primary}}$)** | `evaluation_metrics_dices50.json` | $0.41521166$ | $0.4152$ | **VERIFIED EXACT** |
| **SmolLM2 MAE ($h_{\text{primary}}$)**| `evaluation_metrics_dices50.json` | $0.17344791$ | $0.1734$ | **VERIFIED EXACT** |
| **Ensemble MAE ($h_{\text{primary}}$)**| `evaluation_metrics_dices50.json` | $0.24641665$ | $0.2464$ | **VERIFIED EXACT** |
| **Baseline MAE ($h_{\text{primary}}$)**| `predictive_discrimination_audit.json`| $0.19827784$ | $0.1983$ | **VERIFIED EXACT** |
| **Qwen RMSE** | `evaluation_metrics_dices50.json` | $0.46925940$ | $0.4693$ | **VERIFIED EXACT** |
| **SmolLM2 RMSE** | `evaluation_metrics_dices50.json` | $0.25050568$ | $0.2505$ | **VERIFIED EXACT** |
| **Ensemble RMSE** | `evaluation_metrics_dices50.json` | $0.26693805$ | $0.2669$ | **VERIFIED EXACT** |
| **Baseline RMSE** | `predictive_discrimination_audit.json`| $0.24543207$ | $0.2454$ | **VERIFIED EXACT** |
| **Qwen Soft MSE** | `evaluation_metrics_dices50.json` | $0.22020439$ | $0.2202$ | **VERIFIED EXACT** |
| **SmolLM2 Soft MSE** | `evaluation_metrics_dices50.json` | $0.06275310$ | $0.0628$ | **VERIFIED EXACT** |
| **Ensemble Soft MSE** | `evaluation_metrics_dices50.json` | $0.07125592$ | $0.0713$ | **VERIFIED EXACT** |
| **Baseline Soft MSE** | `predictive_discrimination_audit.json`| $0.06023690$ | $0.0602$ | **VERIFIED EXACT** |
| **SmolLM2 Spearman $\rho$** | `predictive_discrimination_audit.json`| $0.39294977$ ($p=0.00478$) | $0.3929$ ($p=0.0048$) | **VERIFIED EXACT** |
| **Ensemble Pearson $r$** | `predictive_discrimination_audit.json`| $0.49915146$ ($p=2.24\times 10^{-4}$) | $0.4992$ ($p=2.2\times 10^{-4}$) | **VERIFIED EXACT** |
| **Ensemble Spearman $\rho$** | `predictive_discrimination_audit.json`| $0.59026712$ ($p=6.43\times 10^{-6}$) | $0.5903$ ($p=6.4\times 10^{-6}$) | **VERIFIED EXACT** |
| **Qwen AUROC point** | `additional_statistical_reporting.json`| $0.75291375$ | $0.7529$ | **VERIFIED EXACT** |
| **Ensemble AUROC point** | `additional_statistical_reporting.json`| $0.75174825$ | $0.7517$ | **VERIFIED EXACT** |
| **AUROC Difference** | `additional_statistical_reporting.json`| $-0.00116550$ | $-0.0012$ | **VERIFIED EXACT** |
| **AUROC Diff 95% Bootstrap CI** | `additional_statistical_reporting.json`| $[-0.05244755, +0.04428904]$ | $[-0.0524, +0.0443]$ | **VERIFIED EXACT** |
| **SmolLM2 vs Ens MAE diff** | `phase_3c_statistical_refinements.json`| $-0.07296874$ | $-0.0730$ | **VERIFIED EXACT** |
| **SmolLM2 vs Ens Cohen's $d_z$**| `phase_3c_statistical_refinements.json`| $-0.33656956$ | $-0.337$ | **VERIFIED EXACT** |
| **Paired $t$-test $p_{\text{Holm}}$** | `phase_3c_statistical_refinements.json`| $0.04250629$ | $0.0425$ | **VERIFIED EXACT** |
| **Wilcoxon $p_{\text{Holm}}$** | `phase_3c_statistical_refinements.json`| $0.08428987$ | $0.0843$ | **VERIFIED EXACT** |
| **Sign test $p$-value** | `phase_3c_statistical_refinements.json`| $0.00260217$ | $0.0026$ | **VERIFIED EXACT** |
| **SmolLM2 vs Ens Rater CI (MAE)**| `phase_3c_statistical_refinements.json`| $[-0.09351633, -0.03549491]$ | $[-0.0935, -0.0355]$ | **VERIFIED EXACT** |
| **Disagreement OLS $F(1,46)$** | `disagreement_cv_dices50.json` | $5.67595861$ ($p=0.021388$) | $5.6760$ ($p=0.0214$) | **VERIFIED EXACT** |
| **Disagreement 5-Fold OOF $\Delta R^2$**| `disagreement_cv_dices50.json` | $+0.08048989$ | $+0.0805$ | **VERIFIED EXACT** |
| **All Table 5 Rater Bootstrap CIs**| `bootstrap_ci_dices50.json` | Matches all 12 entries | Matches all 12 entries | **VERIFIED EXACT** |

---

## 4. Integrity and Preservation Verification

1. **Prior Drafts Preserved:**
   - `TRUSTEVAL_PAPER_DRAFT.md`: 17,676 bytes (MD5 verified identical)
   - `TRUSTEVAL_PAPER_V2.md`: 50,850 bytes (MD5 verified identical)
   - `TRUSTEVAL_PAPER_V2_1.md`: 57,198 bytes (MD5 verified identical)
   - `TRUSTEVAL_PAPER_V2_2.md`: 58,840 bytes (MD5 verified identical)
2. **Experimental Result Caches:**
   - `results/predictions/qwen2.5_0.5b_dices50.jsonl`: Untouched
   - `results/predictions/smollm2_1.7b_dices50.jsonl`: Untouched
   - `results/tables/evaluation_metrics_dices50.json`: Untouched
   - `results/tables/bootstrap_ci_dices50.json`: Untouched
   - `results/tables/disagreement_cv_dices50.json`: Untouched
   - `results/diagnostics/predictive_discrimination_audit.json`: Untouched
3. **No New Model Downloads or Heavy Inference Runs:**
   - Zero model inference was executed; all analyses derived from existing verified predictions and dedicated diagnostic scripts.

---

## 5. Phase 3C Completion Checklist

```
[x] Deliverable 1 created: research/paper/TRUSTEVAL_PAPER_V2_3.md (64,874 bytes)
[x] Deliverable 2 created: research/paper/PHASE_3C_REFINEMENT_REPORT.md (this report)
[x] Refinement 1: Table 2 highlighting, overall vs. model distinctions, and Baseline ECE = 0.0000* explained
[x] Refinement 2: SmolLM2-1.7B dynamic range compression balanced with positive rank correlation (rho = 0.3929, p = 0.0048)
[x] Refinement 3: Probability mass (M > 0.9684), conditional probability, and generative compliance decoupled
[x] Refinement 4: Metrics partitioned into Prediction Error, Calibration, and Discrimination/Ranking
[x] Refinement 5: Exhaustive paired statistical tests documented (Shapiro-Wilk, paired t, Wilcoxon, sign test, Cohen's dz, bootstrap CIs)
[x] Refinement 6: Cross-validation seed (20261103) and response length unit (character count) specified
[x] Refinement 7: Balanced interpretations (Qwen AUROC bootstrap difference straddles 0, disagreement as routing heuristic)
[x] Refinement 8: Operating environment, framework versions, open licenses, and RSS vs. virtual memory detailed
[x] Refinement 9: References updated (DICES official title, Qian et al. ICML 2026 published proceedings PMLR 306)
[x] Refinement 10: Speculative 60-70% automation claim removed; selective escalation framed as proposed architecture
[x] Refinement 11: Double-blind authorship placeholder and Section 11 Ethics Considerations added
[x] 100% numerical consistency verified against JSON result artifacts
[x] All prior manuscripts and prediction caches preserved without modification
```

---

## 6. Conclusion & Recommendation

The TrustEval project now possesses a rigorous, mathematically verified, and methodologically sound academic manuscript in [`TRUSTEVAL_PAPER_V2_3.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_3.md). The manuscript makes no inflated claims, documents both the strengths and distinct failure modes of small sub-2B open-weight LLMs, and presents reproducible statistical evidence for ensemble reliability and disagreement-based routing on consumer hardware.

The paper is ready for venue conversion (e.g., TrustNLP 2027 / COLING 2027 LaTeX style or TMLR OpenReview formatting).
