# TrustEval: Phase 3C.2 Manuscript Correction and Scientific Reconciliation Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\paper`  
**Date:** November 4, 2026  
**Primary Master Manuscript:** [`research/paper/TRUSTEVAL_PAPER_V2_4.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_4.md)  
**Preserved Prior Manuscripts:**  
- [`research/paper/TRUSTEVAL_PAPER_V2_3.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_3.md) (Preserved unchanged, 64,874 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_2.md) (Preserved unchanged, 58,840 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_1.md) (Preserved unchanged, 57,198 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2.md) (Preserved unchanged, 50,850 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_DRAFT.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_DRAFT.md) (Preserved unchanged, 17,676 bytes)  
**Audit Source:** [`research/paper/PHASE_3C_1_VERIFICATION_REPORT.md`](file:///D:/Research/TrustEval/research/paper/PHASE_3C_1_VERIFICATION_REPORT.md)  

---

## 1. Executive Summary

This report documents the completion of **Phase 3C.2: Manuscript Correction and Scientific Reconciliation** for the TrustEval project. Incorporating findings from the Phase 3C.1 scientific verification audit, master manuscript [`TRUSTEVAL_PAPER_V2_4.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_4.md) resolves all identified editorial, construct-validity, statistical, baseline prevalence, and hardware telemetry discrepancies.

Strict methodological boundaries were maintained:
- **Zero Model Inference:** No additional forward passes or model evaluations were performed.
- **Zero Data Alterations:** All prediction caches (`results/predictions/`), dataset manifests (`data/processed/`), baseline files, and metric tables (`results/tables/`) remain completely pristine.
- **Preservation of Prior Drafts:** All previous manuscript versions (Draft, V2, V2.1, V2.2, V2.3) and reports (Phase 3C Refinement Report, Phase 3C.1 Verification Report) remain untouched.
- **Zero Fabrication:** Every statistical value was directly recomputed and verified against underlying JSON artifacts.

---

## 2. Comprehensive Discrepancy and Reconciliation Table

```
Table: Systematic cross-reconciliation of claims, findings, and corrections across manuscript versions.
```

| Area | Original V2.3 / Phase 3C Report Claim | Verified Empirical Finding (Phase 3C.1 Audit) | V2.4 Manuscript Correction |
| :--- | :--- | :--- | :--- |
| **Prompt Presentation** | Quoted prompt in `[INST] ... [/INST]` with 6-bullet unrendered category list in Section 4.2. | `configs/prompts/safety_judge_v1.txt` contains 4 numbered categories; `[INST]` was never passed; models use native ChatML templates (`<|im_start|>...`). | Section 4.2 presents exact contents of `safety_judge_v1.txt`; details ChatML serialization and confirmed logit extraction at position `-1` (assistant first response token). |
| **DICES Rubric Compatibility** | Claimed model prompt rubric directly matches DICES rater guidelines. | DICES $h_{\text{primary}}$ is derived from `Q_overall` (logical OR of Q2..Q6). Prompt rubric covers core concepts but omits regulated goods, relationship advice, and insensitive language, while adding illegal advice. | Section 4.3 adds explicit DICES category mapping table; transparently documents rubric divergence as a construct-validity limitation. |
| **Rater Exclusions** | Section 3.2 stated: `"rater IDs 0 through 18"`. | Excluded annotators are 19 specific 15-digit identifiers from official `removed_raters_350`. Retained annotators: exactly 104 across all 350 conversations. | Removed "rater IDs 0 through 18"; documented DICES post-annotation filtering; provided complete 19-ID list in Appendix A. |
| **Sample Prevalence** | Stale note in Phase 3C report cited sample prevalence as `0.2483` (bin `[0.2, 0.3)`). | $0.2483$ was an arithmetic mistake from $1 - \text{AUROC}_{\text{ens}} = 1 - 0.7517$. True sample mean $h_{\text{primary}} = \mathbf{0.3381}$ (bin `[0.3, 0.4)`). | All prevalence references corrected to $0.3381$. Baseline ECE $= 0.0000$ explained via single bin $[0.3, 0.4)$ matching mean prevalence. |
| **Baseline AUROC & Ranking** | Table 2 reported theoretical chance AUROC ($0.5000^*$) and omitted correlations, while text noted cross-validation pooling. | 5-fold cross-validation produces slight fold-to-fold variations ($0.3129$ to $0.3499$), yielding empirical OOF AUROC $= 0.3601$, $r = -0.2353$, $\rho = -0.1941$. | Table 3 reports empirical OOF AUROC ($0.3601^\dagger$) and correlations ($r = -0.2353^\dagger, \rho = -0.1941^\dagger$), explicitly explaining them as fold partitioning artifacts. Theoretical constant predictor ($0.5000$) kept as a separate reference row. |
| **SmolLM2 ECE** | Stale text in Phase 3C report cited SmolLM2 ECE as `0.0658`. | Primary metric JSON `evaluation_metrics_dices50.json` line 15 records ECE $= \mathbf{0.0850}$ ($0.085034$). | Table 3 and text confirmed at **0.0850**. |
| **Equivalence Phrasing** | Described SmolLM2 and Ensemble as "statistically equivalent" or "statistically indistinguishable" in Soft MSE and AUROC. | A failure to reject the null hypothesis ($p = 0.6425$, CI straddling zero) does not prove equivalence. | Replaced with: "No statistically significant difference was detected." |
| **Pairwise Sign Tests** | Sign test was evaluated only for SmolLM2 vs Ensemble; reported unadjusted $p = 0.0026$. | Evaluated sign tests across all three model pairs; applied Holm-Bonferroni correction ($m=3$). | Reported all 3 sign tests with exact unadjusted and Holm-adjusted p-values (Qwen vs Ens: $p_{\text{Holm}} = 3.49 \times 10^{-6}$; Qwen vs SmolLM: $p_{\text{Holm}} = 1.80 \times 10^{-4}$; SmolLM vs Ens: $p_{\text{Holm}} = 0.0026$). |
| **Power Calculation** | Section 10 stated $N \ge 146$ samples required for Spearman correlation without mathematical derivation. | Standard asymptotic normal approximation for bivariate correlation under Fisher's $z$-transformation: $N = \lceil 145.85 \rceil = 146$. | Documented exact Fisher $z$ power formula and assumptions; clarified that it serves as an approximate bivariate normal planning estimate rather than an exact guarantee across arbitrary non-normal Spearman distributions. |
| **Hardware Specification** | Phase 3C report mentioned `Intel Core i7-13700H, 32 GB RAM`. | Original inference execution logs confirm the physical platform was: `13th Gen Intel(R) Core(TM) i5-1335U (10 cores, 12 threads), 8.00 GB DDR4 RAM`. | Section 4.6 documents actual Intel Core i5-1335U, 8.00 GB RAM platform. Clarified $4.79\text{ GB}$ as early float32 uncompressed loading estimate. |
| **Sampling Terminology** | Described sample as "unbiased 50-conversation sample" that "eliminates selection bias". | A 50-item sample from an imbalanced dataset cannot guarantee population representativeness. | Replaced with: "fixed-seed simple random sample without replacement" (seed `20261103`); emphasized sample size limitation explicitly. |

---

## 3. Systematic Tracking of Master Corrections in V2.4

### Correction 1: Prompt Serialization and Native Chat Templates
- **Source Issue:** In V2.3 Section 4.2, the prompt template was presented inside `[INST] ... [/INST]` tags with an informal 6-point bullet list (`Hate speech`, `Harassment`, `Sexually explicit`, `Violence`, `Misinformation`, `Privacy`). This contradicted the actual frozen prompt file `configs/prompts/safety_judge_v1.txt`.
- **Applied Changes in V2.4:**
  - Section 4.2 now displays the **verbatim contents** of [`configs/prompts/safety_judge_v1.txt`](file:///D:/Research/TrustEval/configs/prompts/safety_judge_v1.txt) with its 4 structured, numbered categories.
  - Section 4.2 explains the exact serialization pipeline:
    `tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)`
  - Confirmed that both models implement **ChatML** formatting (`<|im_start|>system...<|im_end|>\n<|im_start|>user...<|im_end|>\n<|im_start|>assistant\n`).
  - Stated explicitly that neither model received literal `[INST]` or `[/INST]` markers.
  - Confirmed that logits are extracted at sequence index `-1` (`outputs.logits[0, -1]`), which corresponds to the first token generated by the assistant.
  - Preserved the frozen prompt SHA-256 hash (`15f18333a682867c36fc600aaa80898b6293f324fcabb240ba95f9279d2685df`).

### Correction 2: Construct Validity and DICES Rubric Compatibility
- **Source Issue:** Earlier drafts claimed that the model prompt rubric directly matched DICES safety guidelines. However, DICES contains specific sub-questions (e.g., regulated goods, relationship advice) that do not appear in `safety_judge_v1.txt`.
- **Applied Changes in V2.4:**
  - Added Section 4.3: **Construct Validity and DICES Rubric Compatibility**.
  - Documented that DICES human targets are derived from `Q_overall`, which is the exact deterministic logical OR of five sub-axes: Q2 (Harmful Content), Q3 (Unfair Bias), Q4 (Misinformation), Q5 (Political Affiliation), and Q6 (Policy Guidelines).
  - Added Table 2: A detailed category mapping table comparing raw DICES questions to TrustEval's 4 prompt categories.
  - Transparently identified omissions: relationship advice, insensitive language, and regulated goods (alcohol, tobacco, firearms).
  - Transparently identified additions: "illegal advice" was made explicit in Category 1.
  - Explicitly framed the rubric mismatch as a construct-validity limitation of automated safety evaluation.

### Correction 3: Rater Filtering and Annotator Metadata
- **Source Issue:** Section 3.2 previously described excluded raters as `"(removed_raters_350: rater IDs 0 through 18)"`.
- **Applied Changes in V2.4:**
  - Replaced `"rater IDs 0 through 18"` with the official `removed_raters_350` metadata.
  - Clarified that exclusions were applied by Google Research authors during post-annotation quality filtering.
  - Documented that each of the 350 conversations retains **exactly 104 annotators**, yielding 36,400 total ratings across the benchmark and 5,200 ratings across the 50-item sample.
  - Added Appendix A listing the complete 19 15-digit excluded rater IDs.
  - Removed any language calling annotators "independently verified individuals."

### Correction 4: Sample Prevalence and Baseline Metric Reconciliation
- **Source Issue:** In prior report notes, sample prevalence was erroneously cited as `0.2483` (bin `[0.2, 0.3)`). Furthermore, Table 2 reported theoretical chance AUROC ($0.5000^*$) without presenting the empirical out-of-fold AUROC ($0.3601$) or correlations ($r = -0.2353, \rho = -0.1941$).
- **Applied Changes in V2.4:**
  - Reconciled sample mean prevalence across the 50 items to **$0.3381$** ($0.3381175$).
  - Identified the origin of $0.2483$: an arithmetic subtraction artifact from $1 - \text{AUROC}_{\text{ens}} = 1 - 0.7517 = 0.2483$.
  - Section 5.4 and Table 3 report the 5-fold cross-validated out-of-fold baseline:
    - Mean: $0.338 \pm 0.014$ (Fold training means: $0.3319, 0.3469, 0.3129, 0.3490, 0.3499$)
    - MAE: $0.1983$
    - RMSE: $0.2454$
    - Soft MSE: $0.0602$
    - ECE-10: $0.0000^*$ (All predictions fall strictly into single decile bin $[0.3, 0.4)$, where mean prediction matches mean ground truth)
    - Empirical OOF AUROC: $0.3601^\dagger$
    - Empirical OOF Pearson $r$: $-0.2353^\dagger$ ($p = 0.100$)
    - Empirical OOF Spearman $\rho$: $-0.1941^\dagger$ ($p = 0.177$)
  - Added dagger ($^\dagger$) footnote explaining that negative correlations and sub-chance AUROC are artifacts of fold-partitioning noise across training splits, rather than genuine conversational anti-correlation.
  - Retained the Theoretical Constant Predictor ($0.3381$, MAE $0.1963$, RMSE $0.2417$, MSE $0.0584$, ECE $0.0000$, correlations `—`, AUROC $0.5000$) as an explicit separate reference row.
  - Confirmed SmolLM2 ECE as **`0.0850`** from `evaluation_metrics_dices50.json`.

### Correction 5: Statistical Language and Pairwise Sign Tests
- **Source Issue:** Prior drafts referred to non-significant differences as "statistically equivalent" or "statistically indistinguishable." Furthermore, the sign test was evaluated only for SmolLM2 vs Ensemble with an unadjusted p-value.
- **Applied Changes in V2.4:**
  - Replaced all instances of "statistically equivalent" and "statistically indistinguishable" with:
    `"No statistically significant difference was detected."`
  - Recomputed two-sided binomial sign tests across all three model pairs in MAE:
    1. **Qwen vs. Ensemble:** Ensemble better on 42 items; Qwen on 8 items (0 ties). Raw $p = 1.16 \times 10^{-6}$; Holm-adjusted $p_{\text{Holm}} = \mathbf{3.49 \times 10^{-6}}$ (rank 1, multiplier 3).
    2. **Qwen vs. SmolLM2:** SmolLM2 better on 39 items; Qwen on 11 items (0 ties). Raw $p = 9.02 \times 10^{-5}$; Holm-adjusted $p_{\text{Holm}} = \mathbf{1.80 \times 10^{-4}}$ (rank 2, multiplier 2).
    3. **SmolLM2 vs. Ensemble:** SmolLM2 better on 36 items; Ensemble on 14 items (0 ties). Raw $p = 0.00260$; Holm-adjusted $p_{\text{Holm}} = \mathbf{0.00260}$ (rank 3, multiplier 1).
  - Clearly distinguished parametric paired $t$-tests, Wilcoxon signed-rank tests, and sign tests in Section 7.1.

### Correction 6: Power Analysis Derivation and Assumptions
- **Source Issue:** The sample size planning estimate of $N \ge 146$ lacked explicit mathematical derivation and stated assumptions.
- **Applied Changes in V2.4:**
  - Section 10 now documents the exact formula based on Fisher's $z$-transformation:
    $$N \ge \left\lceil \left(\frac{z_{1-\alpha/2} + z_{1-\beta}}{\frac{1}{2}\ln\left(\frac{1+\rho}{1-\rho}\right)}\right)^2 + 3 \right\rceil$$
  - Stated assumptions: two-sided $\alpha = 0.05$ ($z = 1.95996$), target power $1-\beta = 0.80$ ($z = 0.84162$), target correlation $\rho = 0.2302$ (Fisher $z = 0.23440$), yielding $N = \lceil 145.85 \rceil = 146$.
  - Explicitly qualified that this calculation is an approximate bivariate normal planning estimate rather than an exact guarantee across arbitrary non-normal Spearman rank distributions.

### Correction 7: Hardware Specifications and Memory Telemetry
- **Source Issue:** The Phase 3C report mentioned an `Intel Core i7-13700H, 32 GB RAM` machine, conflicting with earlier logs.
- **Applied Changes in V2.4:**
  - Section 4.6 documents the primary host hardware verified from original logs:
    - **Processor:** 13th Gen Intel(R) Core(TM) i5-1335U (10 cores: 2 P-cores, 8 E-cores, 12 threads), 1.30 GHz base clock.
    - **Memory:** 8.00 GB DDR4 RAM (7.69 GB visible physical RAM; available host RAM: $\sim 600\text{--}800\text{ MB}$).
  - Reconciled memory scopes:
    - Process peak RSS (physical RAM / working set): Qwen $952.1\text{ MB}$, SmolLM2 $1,189.1\text{ MB}$ ($<1.2\text{ GB}$).
    - Post-unload RSS: $<258\text{ MB}$.
    - Private committed pagefile memory: $\approx 2.4\text{ GB}$ during weight loading.
    - Clarified the theoretical $4.79\text{ GB}$ value as an uncompressed float32 loading estimate from early Milestone 2 benchmarking that motivated the `memory_limit_gb: 4.5` safety abort limit.

### Correction 8: Sampling Terminology and Scope Boundaries
- **Source Issue:** Earlier drafts referred to the 50-item sample as "unbiased" and claimed that it "eliminated selection bias."
- **Applied Changes in V2.4:**
  - Replaced with: `"fixed-seed simple random sample without replacement (seed 20261103)"`.
  - Added explicit language in Abstract, Section 3.3, and Section 10 clarifying that a 50-item draw is an exploratory preliminary benchmark sample and does not eliminate sampling variance or guarantee full population representativeness.

---

## 4. Reconciliation of Stale Phase 3C Report Values

To maintain archival integrity, the previous Phase 3C report (`PHASE_3C_REFINEMENT_REPORT.md`) was **preserved completely unchanged**. The table below records the reconciliation of stale values identified in that report:

| Stale Phase 3C Report Entry | Context in Old Report | Reconciled Finding in Phase 3C.2 |
| :--- | :--- | :--- |
| **Prevalence: 0.2483** | Stated that baseline predictions matched empirical mean prevalence of 0.2483. | The empirical sample mean prevalence is **0.3381**. 0.2483 was an arithmetic subtraction artifact ($1 - 0.7517 = 0.2483$). |
| **Baseline Bin: [0.2, 0.3)** | Stated that baseline predictions fell into bin [0.2, 0.3). | Baseline fold predictions ($0.3129$ to $0.3499$) fall entirely into decile bin 3: **[0.3, 0.4)**. |
| **SmolLM2 ECE: 0.0658** | Stated that SmolLM2 achieved an ECE of 0.0658. | The verified ECE from `evaluation_metrics_dices50.json` is **0.0850** ($0.085034$). |
| **Hardware: i7-13700H / 32 GB** | Stated host hardware as Intel Core i7-13700H with 32 GB RAM. | Primary hardware verified from original logs is **13th Gen Intel Core i5-1335U with 8.00 GB RAM**. |

---

## 5. Verification Checklist for V2.4

```
[x] Deliverable 1 created: research/paper/TRUSTEVAL_PAPER_V2_4.md
[x] Deliverable 2 created: research/paper/PHASE_3C_2_CORRECTION_REPORT.md (this report)
[x] Prior manuscripts preserved completely unchanged (Draft, V2, V2.1, V2.2, V2.3)
[x] Prior reports preserved completely unchanged (Phase 3B, Phase 3C, Phase 3C.1)
[x] Correction 1: Misleading [INST] presentation replaced with exact safety_judge_v1.txt prompt and ChatML serialization explanation
[x] Correction 2: Construct validity and DICES rubric compatibility table added; subcategory omissions/additions documented
[x] Correction 3: "Rater IDs 0 through 18" replaced with official removed_raters_350 metadata; 19 IDs listed in Appendix A
[x] Correction 4: Sample mean prevalence reconciled to 0.3381; baseline ECE = 0.0000 explained via bin [0.3, 0.4); empirical OOF AUROC (0.3601) and correlations reported with fold-partitioning artifact explanation
[x] Correction 5: "Statistically equivalent" replaced with "No statistically significant difference was detected"; pairwise sign tests recomputed and Holm-corrected for all 3 pairs
[x] Correction 6: Fisher z power formula and assumptions documented for N >= 146 planning calculation
[x] Correction 7: Host hardware reconciled to Intel Core i5-1335U, 8.00 GB RAM; 4.79 GB explained as theoretical float32 loading estimate
[x] Correction 8: "Unbiased" and "eliminating selection bias" replaced with "fixed-seed simple random sample without replacement"
[x] Correction 9: Stale values from Phase 3C report documented and reconciled without altering the old report
[x] Correction 10: 100% numerical consistency verified across all tables, abstract, and text
[x] Zero model inference re-runs or prediction cache modifications
[x] Prompt SHA-256 hash (15f18333...) and protocol seed (20261103) confirmed identical
```

---

## 6. Strategic Conclusion

`TRUSTEVAL_PAPER_V2_4.md` represents the complete, reconciled master research manuscript for TrustEval. The paper eliminates all misleading prompt formatting presentations, grounds all baseline and prevalence metrics in empirical out-of-fold data, tempers statistical language to avoid overclaiming equivalence, and transparently acknowledges construct-validity boundaries.

The manuscript presents a rigorous, publication-grade defense of small open-weight LLM safety ensembling on consumer hardware.
