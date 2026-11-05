# Phase 3C.6 Final Terminology, Calibration, and Reference Audit Report

**Project:** TrustEval: Empirical Evaluation of LLM Judges for Conversational Safety  
**Workspace:** `D:\Research\TrustEval`  
**Date:** 2026-11-05  
**Audit Phase:** Phase 3C.6 — Final Terminology, Calibration, and Reference Corrections  
**Base Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_2.md`  
**New Deliverable Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_3.md`  
**Audit Report Deliverable:** `research/paper/PHASE_3C_6_FINAL_AUDIT_REPORT.md`  

---

## 1. Executive Summary & Audit Objectives

Phase 3C.6 was executed as a focused, surgical refinement pass on `research/paper/TRUSTEVAL_PAPER_V2_5_2.md` to resolve residual terminological inaccuracies, calibrate metric naming conventions, remove anthropomorphic interpretative phrasing, refine statistical descriptions, audit memory guard runtime behavior, and correct bibliographic references.

### Strict Safeguard Compliance

| Safeguard Requirement | Verification Result | Evidence |
| :--- | :---: | :--- |
| Zero model inference or forward passes | **COMPLIANT** | No model was initialized or queried during this pass. |
| Zero modification to prediction caches (`results/predictions/`) | **COMPLIANT** | Hashes and timestamps of all `.npz` and `.json` cache files are unchanged. |
| Zero modification to raw/processed data (`data/`) | **COMPLIANT** | `data/processed/dices_50_benchmark.csv` and sample manifests are preserved intact. |
| Zero modification to experiment config (`configs/experiment.yaml`) | **COMPLIANT** | Experiment configuration file is unmodified. |
| Zero modification to protocol (`research/PROTOCOL_v1.md`) | **COMPLIANT** | Protocol document is preserved unchanged. |
| Preservation of prior manuscripts & reports | **COMPLIANT** | Draft, V2, V2.1, V2.2, V2.3, V2.4, V2.5, V2.5.1, V2.5.2 and all previous audit reports remain unchanged. |
| Exact file size accounting | **COMPLIANT** | Exact byte counts and line counts are empirically measured and recorded. |

---

## 2. Comprehensive Correction Audit Matrix

The following table documents every manuscript correction executed in the transition from V2.5.2 to V2.5.3:

| Item # | Target Category / Section | V2.5.2 Original Text | Verified Empirical Evidence | V2.5.3 Corrected Text |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Dataset Expansion**<br>(Section 3.1) | `Diverse Conversations Experts and Non-Experts (DICES)` | Official NeurIPS 2023 DICES publication title confirms expansion. | `Diversity in Conversational AI Evaluation for Safety (DICES)` |
| **2** | **Calibration Metric Naming**<br>(Abstract, Sec 5.2, Table 3, Table 3 Note 1, Sec 5.4) | `Expected Calibration Error (ECE-10)`<br>`$\text{ECE} = \sum ... \text{acc}(B_m)$` | Primary target $h_{\text{primary}} \in [0, 1]$ is continuous human consensus proportion, not binary ground truth $y \in \{0, 1\}$. | Renamed to `Soft-Target Expected Calibration Error (Soft-Target ECE-10)`. Explicitly defined with continuous consensus mean $\text{acc}(B_m)$. |
| **3** | **SmolLM2 Non-Anthropomorphic Phrasing**<br>(Abstract, RQ2, Sec 6.2, Sec 9.1) | "confirming that it senses relative conversational hazard..."<br>"suppressing single-model pathological upward prediction bias"<br>"suffer from severe polarization"<br>"tempering Qwen's extreme upward prediction bias" | Models do not "sense" or have "pathological" states; they produce low-variance probability distributions with monotonic rank correlation. | "demonstrating a positive monotonic association with human consensus rankings in this sample..."<br>"tempering single-model large positive mean-prediction bias"<br>"exhibit divergent prediction profiles"<br>"tempering Qwen's large positive mean-prediction bias" |
| **4** | **RQ3 Descriptive OOF Performance**<br>(Section 7.3, Table 5 Note) | Subheading: `- **Out-of-Fold Generalization:**`<br>Note: "...statistical significance is established by the nested in-sample F-test." | Out-of-fold $R^2$ (+0.0805) is descriptive summary metric on $N=50$; $F$-test evaluates in-sample OLS fit, not out-of-fold generalization. | Subheading: `- **Descriptive Out-of-Fold Performance:**`<br>Note: explicitly clarifies $F$-test evaluates in-sample OLS fit and larger cohorts are required to test OOF generalizability. |
| **5** | **Exploratory Correlation p-Values**<br>(Abstract, Sec 5.3, Sec 7.3, Fig 2, Sec 9.1, Sec 10, Sec 12) | Unqualified $p$-values: `($r = 0.3125, p = 0.0271$)`<br>`$\rho = 0.2302 (p = 0.1078)$` | Bivariate correlations on $N=50$ are exploratory linear/monotonic tests without family-wise error rate control. | Explicitly qualified as `unadjusted nominal $p = 0.0271$` and added formal interpretive callout in Section 5.3 noting exploratory nature. |
| **6** | **Brier Decomposition Scope**<br>(Section 5.1 Callout Box) | "...against individual binary rater decisions $y_{i, j} \in \{0, 1\}$... establishing an irreducible human disagreement floor on rater-level binary scoring." | Individual binary decisions $y_{i, j}$ exclude "Unsure" raters; $\bar{\sigma}^2_{\text{human}} = 0.1772$ is empirical sample variance across decisive ratings, not a universal error floor. | Clarified decisive binary decisions (excluding "Unsure"), and stated $\bar{\sigma}^2_{\text{human}}$ reflects empirical annotator disagreement across these sample items rather than an objective universal floor. |
| **7** | **Memory Guard Runtime Control Flow**<br>(Section 4.6) | V2.5.2 claimed pre-emptive GC at 300 MB pre-load, 80 MB during inference, and hard abort at 50 MB, noting `memory_limit_gb: 4.5` as declarative ceiling. | Inspection of `scripts/08_run_50_experiment.py` lines 139–216 confirms: pre-load < 300 MB only calls `gc.collect()` and never aborts; inference loop sleeps 2s at < 80 MB and aborts at < 50 MB available system RAM; `memory_limit_gb: 4.5` is completely unused. | Replaced Section 4.6 text with exact three-part runtime control flow breakdown documenting precise behavior and lack of pre-load abort. |
| **8** | **Bibliography: SmolLM2 Reference**<br>(References) | Cited Hugging Face blog post with 6 authors: `Allal, L. B., Lozhkov, A., Bakouch, E., Gallé, G., von Werra, L., & Wolf, T. (2025). SmolLM2: When Small Language Models Go Big.` | Official publication is arXiv:2502.02737 with 10 authors: Allal, Lozhkov, Bakouch, Blazquez, Tunstall, Piqueres, Marafioti, Zakka, von Werra, & Wolf. | Updated reference entry to official arXiv preprint with all 10 authors, exact title, and arXiv URL. |
| **9** | **Bibliography: Qian et al. (2026)**<br>(References) | Missing PMLR page numbers: `PMLR 306.` | Official ICML 2026 proceedings volume 306 page range is `100995–101013`. | Updated reference entry to `PMLR 306, 100995–101013`. |
| **10** | **File Size & Line Accounting**<br>(Audit Report & Records) | V2.5.1 errata report contained approximate size note (`19,000+ bytes`). | Exact filesystem inspection reveals byte-exact measurements. | Measured and recorded exact byte and line counts for both deliverables; performed control-character scan. |

---

## 3. Deep-Dive Audit: Memory Guard Runtime Control Flow

### Source Code Inspection: `scripts/08_run_50_experiment.py`

Inspection of lines 139–216 of `scripts/08_run_50_experiment.py` and `src/trusteval/judges/hf_judge.py` reveals the exact runtime memory management architecture:

1. **Pre-Load Branch (Lines 141–151):**
   ```python
   pre_avail = psutil.virtual_memory().available / (1024 * 1024)
   logger.info("Host RAM available pre-load: %.1f MB", pre_avail)
   if pre_avail < 300.0:
       logger.warning("Low available RAM pre-load (%.1f MB < 300.0 MB). Pre-emptively running GC...", pre_avail)
       gc.collect()
   ```
   *Findings:* If available system RAM is below 300 MB, `gc.collect()` is invoked. Crucially, the script **does not re-poll available memory** after garbage collection, nor does it contain a conditional abort branch before initializing the model. Consequently, if host RAM remains below 300 MB after garbage collection, model loading proceeds anyway, creating an unmitigated risk of host OOM crash if weights exceed available RAM.

2. **Inference Loop Guard (Lines 185–205):**
   ```python
   avail_ram = psutil.virtual_memory().available / (1024 * 1024)
   if avail_ram < 80.0:
       logger.warning("Available host RAM degraded below 80MB (%.1f MB). Running GC and pausing 2s...", avail_ram)
       gc.collect()
       time.sleep(2.0)
       avail_ram = psutil.virtual_memory().available / (1024 * 1024)
       if avail_ram < 50.0:
           raise RuntimeError(f"CRITICAL: Available host RAM below 50MB ({avail_ram:.1f} MB). Aborting inference.")
   ```
   *Findings:* The active inference monitor checks **system available RAM** (`psutil.virtual_memory().available`), not the Python process Working Set / RSS. The 50 MB threshold is an emergency system-level threshold designed to prevent host kernel freeze, rather than a process memory quota.

3. **Declarative Configuration Audit (`configs/experiment.yaml`):**
   ```yaml
   hardware:
     memory_limit_gb: 4.5
   ```
   *Findings:* Neither `scripts/08_run_50_experiment.py` nor `src/trusteval/judges/hf_judge.py` reads, parses, or enforces `memory_limit_gb`. This parameter was an exploratory planning calculation ($1.4 \times 3.42\text{ GB} = 4.79\text{ GB}$ 16-bit footprint heuristic) and remained completely dead code in execution.

Manuscript Section 4.6 in V2.5.3 now documents these three facts with exact technical precision.

---

## 4. Calibration & Metric Terminology Audit

### Soft-Target ECE-10 vs. Conventional ECE

In conventional binary classification calibration (Guo et al., 2017), Expected Calibration Error evaluates whether predicted probabilities correspond to empirical binary 0/1 accuracy across $M$ probability bins:
$$\text{ECE}_{\text{binary}} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|, \quad \text{where } \text{acc}(B_m) = \frac{1}{|B_m|}\sum_{i \in B_m} \mathbf{1}[y_i = 1]$$

In conversational safety evaluation with continuous annotator consensus:
- Primary target: $h_{\text{primary}, i} = \frac{R_{\text{unsafe}, i}}{R_{\text{unsafe}, i} + R_{\text{safe}, i}} \in [0, 1]$
- Empirical bin accuracy is replaced by the mean human consensus proportion:
  $$\text{acc}(B_m) = \frac{1}{|B_m|}\sum_{i \in B_m} h_{\text{primary}, i}$$
- Predicted confidence: $\text{conf}(B_m) = \frac{1}{|B_m|}\sum_{i \in B_m} p_i$

To prevent reader confusion with binary-label calibration, V2.5.3 adopts the explicit naming convention **Soft-Target Expected Calibration Error (Soft-Target ECE-10)** across the Abstract, Section 5.2, Section 5.4, Table 3 heading, and Table 3 footnotes.

### Brier Score Rater Decomposition Scope

The mathematical equivalence callout in Section 5.1 decomposes rater-level scoring:
$$\text{BS}_{\text{rater}} = \text{MSE}_{\text{soft}} + \bar{\sigma}^2_{\text{human}}$$
Audit verification notes:
1. Individual binary decisions $y_{i, j} \in \{0, 1\}$ apply strictly to decisive ratings, excluding annotators who responded "Unsure" (matching $h_{\text{primary}}$).
2. The term $\bar{\sigma}^2_{\text{human}} = 0.1772$ (derived from benchmark records) represents the sample mean of within-item decisive binomial variances. V2.5.3 clarifies that this value reflects empirical annotator disagreement across this specific sample of 50 conversations rather than an objective or universal lower bound across all possible conversational safety evaluations.

---

## 5. Statistical Interpretation & Significance Disclaimers

### Exploratory Bivariate Correlations

The bivariate correlations between human annotator disagreement $\sigma_{\text{human}}$ and ensemble absolute error $|p_{\text{ensemble}} - h_{\text{primary}}|$ are:
- Pearson correlation: $r = 0.3125$ ($p = 0.0271$)
- Spearman rank correlation: $\rho = 0.2302$ ($p = 0.1078$)

In V2.5.3, these tests are explicitly characterized across all sections (Abstract, Section 5.3, Section 7.3, Figure 2 caption, Section 9.1, Section 10, Section 12) as:
> **Unadjusted nominal / exploratory tests** without family-wise error rate control.

Furthermore, a designated GitHub alert callout was inserted into Section 5.3 explicitly instructing readers on this statistical interpretation.

### Out-of-Fold Cross-Validation Terminology

In Section 7.3 and Table 5:
- The subheading was corrected from `- **Out-of-Fold Generalization:**` to `- **Descriptive Out-of-Fold Performance:**`.
- The Table 5 caption note was updated to clarify that while the nested in-sample $F$-test evaluates the incremental linear fit of annotator disagreement, the out-of-fold cross-validation $R^2$ improvement (+0.0805 absolute) is purely a descriptive summary on this 50-item sample. Establishing genuine out-of-sample generalizability requires independent evaluation on larger cohorts.

---

## 6. Non-Anthropomorphic SmolLM2 Interpretive Language

To adhere to rigorous scientific reporting standards, all anthropomorphic language regarding model behavior was eliminated:

1. **Abstract:** Replaced "confirming that it senses relative conversational hazard rather than blindly guessing prevalence" with "demonstrating a positive monotonic association with human consensus rankings in this sample rather than an invariant prevalence prediction."
2. **RQ2 Formulation:** Replaced "suppressing single-model pathological upward prediction bias" with "tempering single-model large positive mean-prediction bias."
3. **Section 6.2:** Replaced "it genuinely senses relative dialogue risk, but its output probabilities are heavily compressed..." with "its outputs maintain a positive monotonic association with human consensus rankings in this sample, although its prediction scores are compressed into a narrow, low-variance range."
4. **Section 9.1:** Replaced "suffer from severe polarization" with "exhibit divergent prediction profiles."
5. **Section 9.1:** Replaced "tempering Qwen's extreme upward prediction bias" with "tempering Qwen's large positive mean-prediction bias."

---

## 7. Bibliographic Metadata Verification

1. **SmolLM2 Citation:**
   - *Previous (V2.5.2):* Hugging Face Blog Post, 6 authors.
   - *Corrected (V2.5.3):* Allal, L. B., Lozhkov, A., Bakouch, E., Blazquez, G. M., Tunstall, L., Piqueres, A., Marafioti, A., Zakka, C., von Werra, L., & Wolf, T. (2025). SmolLM2: When Smol Goes Big -- Data-Centric Training of a Small Language Model. *arXiv preprint arXiv:2502.02737*. URL: `https://arxiv.org/abs/2502.02737`.
2. **Qian et al. (2026) ICML Citation:**
   - *Previous (V2.5.2):* `PMLR 306.` (missing pages).
   - *Corrected (V2.5.3):* `PMLR 306, 100995–101013.`
3. **DICES Dataset Title:**
   - *Previous (V2.5.2):* `Diverse Conversations Experts and Non-Experts (DICES)`
   - *Corrected (V2.5.3):* `Diversity in Conversational AI Evaluation for Safety (DICES)` (Aroyo et al., NeurIPS 2023).

---

## 8. Artifact Verification & Image Resolution Audit

### Figure Resolution Check

All figure references in `TRUSTEVAL_PAPER_V2_5_3.md` use relative paths resolving directly from the project root. Their existence on disk was verified:

| Figure Markdown Path | Local Filesystem Path | File Size | Dimensions | Status |
| :--- | :--- | :---: | :---: | :---: |
| `results/figures/reliability_diagrams_dices50.png` | `D:\Research\TrustEval\results\figures\reliability_diagrams_dices50.png` | 352,650 bytes | $4155 \times 1311$ px | **VERIFIED** |
| `results/figures/disagreement_vs_error_dices50.png` | `D:\Research\TrustEval\results\figures\disagreement_vs_error_dices50.png` | 175,628 bytes | $1910 \times 1461$ px | **VERIFIED** |
| `results/figures/distribution_alignment_dices50.png` | `D:\Research\TrustEval\results\figures\distribution_alignment_dices50.png` | 126,687 bytes | $2061 \times 1311$ px | **VERIFIED** |

### Control Character Scan

A byte-level inspection was executed across `TRUSTEVAL_PAPER_V2_5_3.md` scanning for non-printing ASCII control characters (byte value $< 32$, excluding `\t`, `\n`, `\r`):
- Non-printing control bytes detected: **0**
- ASCII Backspace (`\x08`): **0**
- NUL bytes (`\x00`): **0**

---

## 9. Deliverable Accounting & Archival Preservation

### Exact Deliverable Metrics

| File Path | Character Count | Line Count | Exact Byte Size |
| :--- | :---: | :---: | :---: |
| `research/paper/TRUSTEVAL_PAPER_V2_5_3.md` | 79,126 | 1,172 | 81,094 bytes |
| `research/paper/PHASE_3C_6_FINAL_AUDIT_REPORT.md` | 18618 | 224 | 18859 bytes |

### Complete Archival Ledger

All previous manuscript drafts, correction passes, and audit reports in `D:\Research\TrustEval\research\paper` have been preserved unchanged:

| File Name | File Type | Exact Size (Bytes) | Integrity Status |
| :--- | :---: | :---: | :---: |
| `TRUSTEVAL_PAPER_DRAFT.md` | Initial Draft | 17,676 | Unmodified |
| `TRUSTEVAL_PAPER_V2.md` | V2 Manuscript | 50,850 | Unmodified |
| `TRUSTEVAL_PAPER_V2_1.md` | V2.1 Manuscript | 57,198 | Unmodified |
| `TRUSTEVAL_PAPER_V2_2.md` | V2.2 Manuscript | 58,840 | Unmodified |
| `TRUSTEVAL_PAPER_V2_3.md` | V2.3 Manuscript | 64,874 | Unmodified |
| `TRUSTEVAL_PAPER_V2_4.md` | V2.4 Manuscript | 70,116 | Unmodified |
| `TRUSTEVAL_PAPER_V2_5.md` | V2.5 Manuscript | 73,990 | Unmodified |
| `TRUSTEVAL_PAPER_V2_5_1.md` | V2.5.1 Manuscript | 76,572 | Unmodified |
| `TRUSTEVAL_PAPER_V2_5_2.md` | V2.5.2 Manuscript | 78,785 | Unmodified |
| `TRUSTEVAL_PAPER_V2_5_3.md` | **V2.5.3 Master Manuscript** | **81,094** | **Created (Phase 3C.6)** |
| `V2_1_CORRECTION_REPORT.md` | Report | 19,654 | Unmodified |
| `PHASE_2B_REVISION_REPORT.md` | Report | 13,378 | Unmodified |
| `PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md` | Report | 28,370 | Unmodified |
| `PHASE_3B_CORRECTION_REPORT.md` | Report | 15,820 | Unmodified |
| `PHASE_3C_REFINEMENT_REPORT.md` | Report | 27,345 | Unmodified |
| `PHASE_3C_1_VERIFICATION_REPORT.md` | Report | 38,748 | Unmodified |
| `PHASE_3C_2_CORRECTION_REPORT.md` | Report | 19,588 | Unmodified |
| `PHASE_3C_3_FINAL_AUDIT_REPORT.md` | Report | 17,017 | Unmodified |
| `PHASE_3C_4_ERRATA_REPORT.md` | Report | 18,629 | Unmodified |
| `PHASE_3C_5_FINAL_AUDIT_REPORT.md` | Report | 17,628 | Unmodified |
| `PHASE_3C_6_FINAL_AUDIT_REPORT.md` | **Phase 3C.6 Audit Report** | **18859** | **Created (Phase 3C.6)** |

---

## 10. Audit Conclusion

The Phase 3C.6 refinement pass is complete. All 10 specific correction requirements have been verified and applied without altering any numerical results, experimental data, prediction caches, configurations, or protocols. `TRUSTEVAL_PAPER_V2_5_3.md` stands as the current master manuscript for TrustEval.
