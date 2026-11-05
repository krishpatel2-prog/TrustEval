# TrustEval: Phase 3C.4 Final Errata and Provenance Corrections Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `research/paper/`  
**Date:** November 5, 2026  
**Primary Master Manuscript Produced:** [`research/paper/TRUSTEVAL_PAPER_V2_5_1.md`](TRUSTEVAL_PAPER_V2_5_1.md)  
**Base Manuscript Audited:** [`research/paper/TRUSTEVAL_PAPER_V2_5.md`](TRUSTEVAL_PAPER_V2_5.md) (Preserved unchanged, 73,990 bytes)  
**Preserved Prior Manuscripts:**  
- [`research/paper/TRUSTEVAL_PAPER_V2_4.md`](TRUSTEVAL_PAPER_V2_4.md) (Preserved unchanged, 70,116 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_3.md`](TRUSTEVAL_PAPER_V2_3.md) (Preserved unchanged, 64,874 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_2.md`](TRUSTEVAL_PAPER_V2_2.md) (Preserved unchanged, 58,840 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](TRUSTEVAL_PAPER_V2_1.md) (Preserved unchanged, 57,198 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2.md`](TRUSTEVAL_PAPER_V2.md) (Preserved unchanged, 50,850 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_DRAFT.md`](TRUSTEVAL_PAPER_DRAFT.md) (Preserved unchanged, 17,676 bytes)  
**Preserved Prior Audit Reports:**  
- [`research/paper/PHASE_3C_3_FINAL_AUDIT_REPORT.md`](PHASE_3C_3_FINAL_AUDIT_REPORT.md) (Preserved unchanged, 17,017 bytes)  
- [`research/paper/PHASE_3C_2_CORRECTION_REPORT.md`](PHASE_3C_2_CORRECTION_REPORT.md) (Preserved unchanged, 19,588 bytes)  
- [`research/paper/PHASE_3C_1_VERIFICATION_REPORT.md`](PHASE_3C_1_VERIFICATION_REPORT.md) (Preserved unchanged, 38,748 bytes)  
- [`research/paper/PHASE_3C_REFINEMENT_REPORT.md`](PHASE_3C_REFINEMENT_REPORT.md) (Preserved unchanged, 27,345 bytes)  
- [`research/paper/PHASE_3B_CORRECTION_REPORT.md`](PHASE_3B_CORRECTION_REPORT.md) (Preserved unchanged, 15,820 bytes)  
- [`research/paper/PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md`](PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md) (Preserved unchanged, 28,370 bytes)  

---

## 1. Executive Summary

This report documents the completion of **Phase 3C.4: Final Errata and Provenance Corrections** for the TrustEval project. Following an independent review of manuscript V2.5, this pass executes targeted errata corrections, precision telemetry enhancements, bibliographic reconciliation, and provenance clarifications. This is a narrow, precision correction pass—**not** a new experiment or broad conceptual rewrite.

### Strict Methodological Safeguards Maintained:
- **Zero Forward Inference:** No model inference passes, weight transformations, or benchmark executions were performed.
- **Zero Data Alterations:** All prediction caches (`results/predictions/`), dataset manifests (`data/processed/`), baseline files, and metric tables (`results/tables/`) remain completely intact.
- **Strict Archival Preservation:** All previous manuscript versions (Draft through V2.5) and audit reports remain untouched.
- **Zero Numerical Fabrication:** Every numerical value was derived strictly from original saved experimental data (`dices_50_sample_manifest.parquet`, `evaluation_metrics_dices50.json`, and benchmark records).
- **No Premature Readiness Claims:** Completion of this errata pass is documented objectively without asserting unreserved submission readiness.

---

## 2. Comprehensive Errata and Discrepancy Reconciliation Table

```
Table: Systematic cross-reconciliation of issues identified in V2.5, underlying evidence, and V2.5.1 corrections.
```

| Issue / Area | V2.5 Statement / Artifact | Verified Evidence (Phase 3C.4 Audit) | V2.5.1 Correction & Resolution |
| :--- | :--- | :--- | :--- |
| **Correction 1: Control Character** | Table 3 Note 3 contained ASCII backspace character `0x08` immediately before `ar{h}` (`$\x08ar{h} = 0.3381$`). | Byte scan identified `hex=0x8` at byte offset 36,951 resulting from unescaped `\b` in string generation. Also identified stray backslash in `*\Notes on Table 3:*`. | Replaced `\x08ar{h}` with clean LaTeX `\bar{h}`. Removed stray backslash to produce `*Notes on Table 3:*`. Full binary scan confirms exactly 0 non-printing control characters across the entire document. |
| **Correction 2: Abstract F-Test Interpretation** | Finding 4 stated: `adding disagreement improves out-of-fold explanatory power by $\Delta R^2_{\text{OOF}} = +0.0805$ ($F(1, 46) = 5.68, p = 0.0214$).` | The $F$-test evaluates in-sample nested OLS model comparison ($F(1, 46) = 5.676, p = 0.0214$). $\Delta R^2_{\text{OOF}} = +0.0805$ is a descriptive out-of-fold summary metric across 5-fold cross-validation folds. Attaching the in-sample $p$-value directly to the OOF metric conflates distinct statistical paradigms. | Abstract Finding 4 explicitly separated: nested in-sample OLS incremental variance ($F(1, 46) = 5.676, p = 0.0214$) from descriptive out-of-fold cross-validation gain ($\Delta R^2_{\text{OOF}} = +0.0805$). Section 7.3 detailed formulation preserved. |
| **Correction 3: Memory Accounting & Footprints** | Section 4.6 stated: `1.4 * 3.42 GB = 4.79 GB reflects an uncompressed float32 loading estimate...` and conflated Working Set with RSS and private commit with pagefile. | For 1.71B parameters: 16-bit static weights occupy $\approx 3.42\text{ GB}$; 32-bit float32 weights occupy $\approx 6.84\text{ GB}$. The $1.4\times$ multiplier was an ad-hoc heuristic planning factor for 16-bit runtime/loading overhead, not float32. On Windows, `psutil` reports Process Working Set via `.rss`. Private committed bytes peaked at $\approx 2.4\text{ GB}$ during loading. | Removed unsupported float32 multiplier claim. Defined $4.79\text{ GB}$ as an exploratory heuristic overhead estimate ($1.4 \times 3.42\text{ GB}$) used only for pre-execution safety limits. Rigorously distinguished Process Working Set (physical RAM resident: $952.1\text{ MB}$ Qwen, $1,189.1\text{ MB}$ SmolLM2) from private committed bytes / commit charge ($\approx 2.4\text{ GB}$ peak). |
| **Correction 4: Demographic Balancing** | Section 3.1 stated: `balanced across self-reported gender, self-reported race/ethnicity, and age groups in the US annotator sample`. | Official DICES-350 documentation balances across gender and race/ethnicity. Age was recorded as a demographic dimension, but the 350-item pool was not specifically balanced by age. Verified counts: 123 original raters, 19 excluded, 104 retained. | Section 3.1 updated to: `balanced across self-reported gender and self-reported race/ethnicity in the US annotator sample; age was additionally recorded as a demographic dimension.` |
| **Correction 5: Model Revision Provenance** | Section 4.1 listed exact commit SHAs as definitive historical inference revisions. | Prediction cache records in `results/predictions/` log `model_revision: "main"`. The hex commit SHAs were identified in local cache `D:\hf_cache\models--*\refs\main` after execution. | Clarified that models were tracked on branch `main` (as recorded in prediction logs), and documented the exact snapshot commit SHAs (`7ae557604adf...` and `31b70e2e869a...`) as local cached snapshots identified on disk rather than historically logged execution hashes. |
| **Correction 6: Reference Accuracy** | Verga et al. (2024) had incomplete author list. Feng et al. (2026) cited placeholder `noisybutvalid2026`. Brier (1950) was omitted from decomposition note. Touvron et al. (2023) was cited for SmolLM2 architecture. | arXiv:2404.18796 official authors: Pat Verga, Sebastian Hofstatter, Sophia Althammer, Yixuan Su, Aleksandra Piktus, Arkady Arkhangorodsky, Minjie Xu, Naomi White, Patrick Lewis. Feng et al. published in ICLR 2026 proceedings. SmolLM2 architecture is documented directly by Allal et al. (2025). | Updated Verga et al. with complete 9-author metadata. Replaced Feng et al. OpenReview id with official ICLR proceedings URL. Cited Brier (1950) in Section 5.1 decomposition. Replaced Touvron citation with Allal et al. (2025). Complete 1-to-1 citation audit confirmed. |
| **Correction 7: False-Alarm Wording** | Described Qwen as an `"aggressive false-alarm judge"` and cited `"elevated false-alarm rate"`. | In continuous probabilistic evaluation without a pre-specified classification threshold and confusion-matrix analysis, "false-alarm" is methodologically imprecise. | Replaced with: `"acute positive unsafe-risk prediction bias that systematically overestimates conversational hazard"` and `"elevated upward prediction bias"`. |
| **Correction 8: Target Aggregation Labels** | Section 3.2 parenthetical mentioned `(or 0.3165 if the 311 unsure ratings are included in the denominator...)` without distinguishing it from sensitivity targets. | Verified: macro-average item-level $h_{\text{primary}} = \mathbf{0.3381}$; pooled decisive-vote proportion $= \frac{1,646}{4,889} = \mathbf{0.3367}$; pooled explicit-Yes share across all ratings $= \frac{1,646}{5,200} = \mathbf{0.3165}$. $0.3165$ gives zero credit to Unsure and is distinct from $h_{\text{sensitivity}} = \frac{Y + 0.5 \cdot U}{Y + N + U}$. | Clarified that $0.3165$ represents the raw unadjusted pooled share of explicit-Yes votes without unsure credit across all 5,200 submitted ratings, distinct from the half-credit smoothed target $h_{\text{sensitivity}}$. |
| **Correction 9: Sensitivity Analysis Wording** | Section 7.5 claimed: `confidence interval spreads... remain completely consistent across both target formulations.` | Table 7 reports point estimates for $h_{\text{primary}}$ and $h_{\text{sensitivity}}$ across MAE and Soft MSE; it does not compute or show bootstrap confidence intervals for the sensitivity target. | Replaced with: `"As established by the point estimates in Table 7, the relative ranking of evaluators in MAE and Soft MSE, as well as the substantial error reduction achieved by the ensemble over Qwen, remains consistent across both target formulations."` |
| **Correction 10: Final Document Integrity** | Needed complete verification across mathematical formulas, table captions, memory terms, citations, and formatting. | Comprehensive programmatic scan across all sections of V2.5.1. | All 10 audit dimensions verified and confirmed. |

---

## 3. Detailed Technical Verifications

### 3.1 Non-Printing Control Character Scan (Correction 1)
- **Investigation:** A full binary inspection of `TRUSTEVAL_PAPER_V2_5.md` revealed byte `0x08` (ASCII backspace `\b`) at offset 36,951 immediately preceding `ar{h}` in Table 3 Note 3. This arose because a non-raw Python string literal converted `\bar` into `\b` + `ar`.
- **Resolution:** In `TRUSTEVAL_PAPER_V2_5_1.md`, byte `0x08` was replaced with literal `\bar{h}`. An automated binary scanner evaluated all 74,606 bytes against control code ranges (`byte < 32 and byte not in (9, 10, 13)`), confirming **zero non-printing control characters** remaining. Additionally, the stray backslash in `*\Notes on Table 3:*` was corrected to `*Notes on Table 3:*`.

### 3.2 Abstract Statistical Separation (Correction 2)
- **Investigation:** In V2.5 Abstract Finding 4, the nested OLS $F$-test was cited as `$\Delta R^2_{\text{OOF}} = +0.0805$ ($F(1, 46) = 5.68, p = 0.0214$)`. This conflated the parametric in-sample nested $F$-test with the non-parametric out-of-fold cross-validation performance.
- **Resolution:** Abstract Finding 4 was rephrased:
  > *"In nested in-sample OLS modeling controlling for response length and ensemble confidence, adding disagreement accounts for statistically significant incremental variance ($F(1, 46) = 5.676, p = 0.0214$), while yielding a descriptive out-of-fold explanatory improvement of $\Delta R^2_{\text{OOF}} = +0.0805$ under 5-fold cross-validation."*
  This maintains clean statistical hygiene while preserving the complete Section 7.3 mathematical derivation.

### 3.3 Memory Telemetry and Footprint Accounting (Correction 3)
- **Investigation:**
  1. For `HuggingFaceTB/SmolLM2-1.7B-Instruct` (1.71 billion parameters):
     - Static 16-bit weights (BF16/FP16) require: $1.71 \times 10^9 \times 2\text{ bytes} \approx 3.42\text{ GB}$.
     - Static 32-bit weights (FP32) require: $1.71 \times 10^9 \times 4\text{ bytes} \approx 6.84\text{ GB}$.
     - The calculation $1.4 \times 3.42\text{ GB} = 4.79\text{ GB}$ represents an ad-hoc $1.4\times$ overhead factor applied to 16-bit parameters, **not** an uncompressed float32 loading estimate.
  2. Operating System Memory Semantics:
     - On Windows, `psutil.Process().memory_info().rss` returns the process **Working Set** (physical non-paged RAM currently resident).
     - Windows private committed bytes (commit charge) tracks the total committed virtual address space backed by physical RAM or paging files. Conflating private commit with "pagefile usage" is technically inaccurate because private committed pages reside in physical RAM until system memory pressure forces paging.
- **Resolution:** Section 4.6 was rewritten to:
  - Report physical memory occupancy as **Process Working Set** ($952.1\text{ MB}$ for Qwen, $1,189.1\text{ MB}$ for SmolLM2).
  - Explicitly define Windows private committed bytes / commit charge ($\approx 2.4\text{ GB}$ peak during SmolLM2 initialization before buffer release).
  - Define $4.79\text{ GB}$ as an exploratory heuristic planning estimate ($1.4 \times 3.42\text{ GB}$) used only to establish the `memory_limit_gb: 4.5` safety abort threshold in `configs/experiment.yaml`.

### 3.4 DICES Demographic Balancing (Correction 4)
- **Investigation:** The official DICES-350 dataset README and paper (Aroyo et al., 2023) state that the 350-item dialogue pool was curated to balance annotators across self-reported gender and self-reported race/ethnicity in the US sample. While rater age was recorded, the 350-item pool was not specifically balanced by age.
- **Resolution:** Section 3.1 was refined to state that the rater pool was balanced across self-reported gender and race/ethnicity, while age was recorded as a demographic dimension. Retained annotator counts (123 initial, 19 quality exclusions, 104 retained per item) were preserved intact.

### 3.5 Model Revision Provenance (Correction 5)
- **Investigation:** Inspection of `results/predictions/qwen2.5_0.5b_dices50.jsonl` and `smollm2_1.7b_dices50.jsonl` reveals:
  `"model_id": "Qwen/Qwen2.5-0.5B-Instruct", "model_revision": "main"`
  The inference execution script logged the configuration parameter `model_revision: "main"`, rather than the resolved git commit SHA. The commit hashes (`7ae557604adf...` and `31b70e2e869a...`) reside in `D:\hf_cache\models--*\refs\main`.
- **Resolution:** Section 4.1 was updated to state that models were tracked on branch `main` as recorded in prediction logs, and transparently documents the commit SHAs as identified local cached snapshots on disk rather than historically logged execution hashes.

### 3.6 Reference and Bibliography Alignment (Correction 6)
- **Investigation & Resolution:**
  1. **Verga et al. (2024):** Updated to the full 9-author metadata from arXiv:2404.18796: Pat Verga, Sebastian Hofstatter, Sophia Althammer, Yixuan Su, Aleksandra Piktus, Arkady Arkhangorodsky, Minjie Xu, Naomi White, and Patrick Lewis.
  2. **Feng et al. (2026):** Replaced placeholder OpenReview id `noisybutvalid2026` with official ICLR URL: `https://proceedings.iclr.cc/paper_files/paper/2026/hash/08a67eb74bfb9ded9e949dd52973e997-Abstract-Conference.html`.
  3. **Brier (1950):** Added explicit citation to Brier (1950) in Section 5.1 where the rater-level Brier score decomposition is introduced.
  4. **Touvron et al. (2023):** Removed Touvron et al. from Section 4.1 and Section 13, replacing the architecture citation with Allal et al. (2025) directly.
  5. **Citation Audit:** Confirmed complete 1-to-1 correspondence between in-text citations and Section 13 entries.

### 3.7 False-Alarm Wording Precision (Correction 7)
- **Investigation:** Phrases such as "aggressive false-alarm judge" and "elevated false-alarm rate" imply binary classification error under a fixed threshold and confusion-matrix analysis. TrustEval evaluates continuous regression probabilities $P(\text{Unsafe}) \in [0, 1]$.
- **Resolution:** Replaced all four instances across the Abstract, Section 6.2, Section 9.1, and Section 10 with accurate descriptions of observed continuous behavior: "acute positive unsafe-risk prediction bias that systematically overestimates conversational hazard" and "elevated upward prediction bias".

### 3.8 Target Aggregation Labeling (Correction 8)
- **Investigation:** Verified the arithmetic derivation across all 50 sample items:
  - Macro-average of item proportions: $\bar{h} = \frac{1}{50}\sum h_{\text{primary}, i} = \mathbf{0.3381}$.
  - Pooled decisive proportion: $\frac{\sum Y}{\sum(Y+N)} = \frac{1,646}{4,889} = \mathbf{0.3367}$.
  - Pooled explicit-Yes share across all ratings: $\frac{\sum Y}{5,200} = \frac{1,646}{5,200} = \mathbf{0.3165}$.
- **Resolution:** Section 3.2 explicitly clarifies that $0.3165$ is the raw unadjusted share of explicit-Yes votes without unsure credit, distinct from the sensitivity consensus target $h_{\text{sensitivity}} = \frac{Y + 0.5 \cdot U}{Y + N + U}$.

### 3.9 Sensitivity Analysis Scope (Correction 9)
- **Investigation:** Table 7 reports point estimates for primary and sensitivity targets across MAE and Soft MSE. It does not compute or show bootstrap confidence intervals for the sensitivity target.
- **Resolution:** Corrected the summary claim in Section 7.5 to state only what Table 7 establishes: the relative rankings of evaluators and the substantial error reduction achieved by the ensemble over Qwen remain consistent across both target formulations.

---

## 4. Archival and Deliverable Verification

```
Deliverable Files Summary
```

| File Path | Byte Size | State |
| :--- | :---: | :--- |
| `research/paper/TRUSTEVAL_PAPER_V2_5_1.md` | 74,606 bytes | **Created** (Primary Master Manuscript) |
| `research/paper/PHASE_3C_4_ERRATA_REPORT.md` | 17,200+ bytes | **Created** (This Errata Audit Report) |
| `research/paper/TRUSTEVAL_PAPER_V2_5.md` | 73,990 bytes | Preserved unchanged |
| `research/paper/TRUSTEVAL_PAPER_V2_4.md` | 70,116 bytes | Preserved unchanged |
| `research/paper/TRUSTEVAL_PAPER_V2_3.md` | 64,874 bytes | Preserved unchanged |
| `research/paper/TRUSTEVAL_PAPER_V2_2.md` | 58,840 bytes | Preserved unchanged |
| `research/paper/TRUSTEVAL_PAPER_V2_1.md` | 57,198 bytes | Preserved unchanged |
| `research/paper/TRUSTEVAL_PAPER_V2.md` | 50,850 bytes | Preserved unchanged |
| `research/paper/TRUSTEVAL_PAPER_DRAFT.md` | 17,676 bytes | Preserved unchanged |
