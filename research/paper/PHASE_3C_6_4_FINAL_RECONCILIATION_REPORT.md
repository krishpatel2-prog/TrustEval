# Phase 3C.6.4 Final Numerical, Bibliographic and Integrity Reconciliation Report

**Project:** TrustEval  
**Workspace:** `D:\Research\TrustEval`  
**Audit Phase:** Phase 3C.6.4 — Final Numerical, Bibliographic and Integrity Reconciliation  
**Date:** November 2026  
**Auditor:** Scientific Integrity and Methodological Audit Team  
**Status:** Complete & Fully Reconciled  
- Base Master Manuscript: `research/paper/TRUSTEVAL_PAPER_V2_5_3_3.md` (86,185 bytes, SHA-256: `207d904b88f3640600aace901e732ed7ecaf8d921564e71ac4bb028654c66e84`)  
- Prior Audit Report: `research/paper/PHASE_3C_6_3_FINAL_REPRODUCIBILITY_REPORT.md` (19,449 bytes, SHA-256: `76406ee755787283b75a963211448ab5ab4412b4766b2155b2a872272581794a`)  
- New Master Manuscript: `research/paper/TRUSTEVAL_PAPER_V2_5_3_4.md` (87,014 bytes, SHA-256: `eaab250fba8f2ee175e43195de97251377b23c6eb7950d2f360a237b448a179a`)  
- New Audit Report: `research/paper/PHASE_3C_6_4_FINAL_RECONCILIATION_REPORT.md` (24899 bytes, SHA-256: `[Self-referential; verified upon completion]`)

---

## 1. Executive Summary & Audit Objectives

Phase 3C.6.4 constitutes the final numerical, bibliographic, and telemetry reconciliation of the TrustEval study. This phase resolved an arithmetic discrepancy in the rater-level Brier score decomposition, rectified overgeneralized claims regarding local-inference privacy and compliance, standardized Qwen2.5 authorship to reflect official title-page group attribution (`Qwen Team`), finished consolidating all references into a single APA 7th edition alphabetized list in sentence case, harmonized regression terminology across the Abstract and Research Questions, and documented a rigorous before-and-after cryptographic telemetry analysis.

### Strict Methodological Safeguards:
- **Zero Forward Passes & Zero Inference:** No model inference was executed.
- **Zero Modifications to Data or Predictions:** `data/` and `results/predictions/` remain 100% untouched.
- **Zero Changes to Protocol or Configuration:** `configs/experiment.yaml` and `research/PROTOCOL_v1.md` remain intact.
- **Target Vector Verification:** Read-only verification was performed on the existing frozen target vector `h_primary`.
- **Preservation of Prior Files:** All 29 previously existing files in `research/paper/` remain byte-for-byte intact.
- **Submission Readiness Declaration:** In strict compliance with institutional guidelines, completing this audit resolves methodological and bibliographic issues but does **not** constitute an external declaration of submission readiness.

---

## 2. Numerical Reconciliation: Brier Score Decomposition Arithmetic

### 2.1 The Arithmetic Conflict
Previous drafts of the manuscript reported:
- Sample mean human target: $\bar{h}_{\text{primary}} = 0.3381$ ($0.33811754$)
- Population standard deviation: $\text{SD}_{\text{pop}}(h) = 0.2417$ (Population variance $\text{Var}_{\text{pop}}(h) = 0.05841830$)
- Mean within-item binomial rater variance: $\bar{\sigma}^2_{\text{human}} = 0.1772$

These three values cannot mathematically describe the same target vector. For any discrete set of proportions $h_i$, the sample mean of within-item binomial variances satisfies the exact algebraic identity:
$$\frac{1}{N}\sum_{i=1}^N h_i(1 - h_i) = \bar{h}(1 - \bar{h}) - \text{Var}_{\text{pop}}(h)$$

Substituting the reported mean and population variance into the identity:
$$\bar{h}(1 - \bar{h}) = 0.33811754 \times (1 - 0.33811754) = 0.22379407$$
$$\bar{\sigma}^2_{\text{human}} = 0.22379407 - 0.05841830 = \mathbf{0.16537577} \approx \mathbf{0.1654}$$

If $\bar{\sigma}^2_{\text{human}}$ were $0.1772$, the population variance would have to be:
$$\text{Var}_{\text{pop}}(h) = 0.22379407 - 0.1772 = 0.04659407 \implies \text{SD}_{\text{pop}}(h) = \sqrt{0.04659407} = 0.21585660 \neq 0.2417$$

### 2.2 Direct Read-Only Verification on Frozen Target Vector
A direct calculation was executed on the frozen 50-item target vector $h_{\text{primary}}$ from `results/tables/ensemble_predictions_dices50.csv` and `data/processed/dices_350_targets.csv`:
- **Sample Size ($N$):** 50 items
- **Mean $\bar{h}_{\text{primary}}$:** $0.3381175351471969$ (rounds to $0.3381$)
- **Population Variance (ddof=0):** $0.058418299799827586$ (rounds to $0.0584$)
- **Population Standard Deviation (ddof=0):** $0.24169877906151613$ (rounds to $0.2417$)
- **Sample Variance (ddof=1):** $0.05961050999982407$ (rounds to $0.0596$)
- **Sample Standard Deviation (ddof=1):** $0.24415263668415313$ (rounds to $0.2442$)
- **Mean Within-Item Binomial Variance $\frac{1}{N}\sum h_i(1-h_i)$:** $\mathbf{0.1653757677733534}$ (rounds to $\mathbf{0.1654}$)
- **Algebraic Brier Decomposition Check:** $0.22379406757318096 - 0.058418299799827586 = \mathbf{0.1653757677733534}$ (holds identically).

### 2.3 Diagnostic Conclusion & Manuscript Erratum
- The reported mean human target ($0.3381$) and population standard deviation ($0.2417$) are mathematically correct.
- The reported mean within-item binomial variance of **$0.1772$ was an erroneous historical value** (likely originating from an un-filtered calculation or a 350-item benchmark aggregate where within-item variance is $\approx 0.1787$).
- On the frozen 50-item sample, the true within-item binomial variance is $\mathbf{0.1654}$ ($0.16537577$).
- Consequently, the rater-level Brier score decomposition for the Two-Judge Ensemble resolves to:
  $$\text{BS}_{\text{rater}}(\text{Ensemble}) = \text{MSE}_{\text{soft}} + \bar{\sigma}^2_{\text{human}} = 0.0713 + 0.1654 = \mathbf{0.2367}$$
- Section 5.1 of `TRUSTEVAL_PAPER_V2_5_3_4.md` was updated with an explicit explanatory note reconciling this identity and documenting the erratum.

---

## 3. Local-Inference Privacy & Regulatory Framing Corrections

### 3.1 Defect in Prior Text
Section 1 previously made an absolute claim:
> *"Local model execution eliminates cross-boundary data transmission entirely, significantly simplifying compliance."*

Similarly, Abstract Finding 5 claimed local inference enabled auditing *"without transmitting conversational data to external third-party APIs"*.

These formulations failed to account for:
1. Surrounding pipeline transmission (e.g., if data ingestion, pre-processing, logging, or metric aggregation pipelines transmit data across network boundaries).
2. Compliance reality: executing models locally does not automatically guarantee GDPR, HIPAA, or statutory compliance, which depends on organizational data governance, access controls, audit logs, and security controls.

### 3.2 Implemented Corrections
- **Abstract (Finding 5):**
  > *"Deterministic next-token logit scoring executes locally on consumer CPU hardware within a bounded memory envelope ($<1.2\text{ GB}$ peak resident set size), demonstrating the technical feasibility of on-premises, decentralized safety auditing that avoids sending evaluated conversational data to external third-party model inference APIs, provided the surrounding data pipeline also operates locally."*
- **Section 1 (Item 1):**
  > *"1. **Data Confidentiality & Privacy:** External processing introduces confidentiality, data leakage, and compliance risks. While lawful cloud processing may be established through formal legal bases, comprehensive Data Processing Agreements (DPAs), technical safeguards, and HIPAA Business Associate Agreements (BAAs) where applicable, transmitting sensitive enterprise dialogues creates ongoing regulatory overhead. Local model inference avoids sending evaluated conversations to external third-party model inference APIs, provided the surrounding data pipeline also operates within an on-premises or secure local boundary; however, local execution does not automatically guarantee regulatory compliance, which depends on broader organizational data governance and system-level security controls."*

---

## 4. Qwen2.5 Authorship & Reference Reconciliation

### 4.1 Group Author vs. Individual Author Analysis
- **Source Inspection:** The official PDF title page of arXiv:2412.15115 designates the author as **Qwen Team** (Alibaba Group), with individual contributors listed subordinate to the group moniker.
- **APA 7 Standard (Section 9.11, Group Authors):** Under APA 7th edition rules, when a work's title page credits a group or corporate entity as the author, the work is cited under the group author's name. It should not be forced into an artificial 43-person individual author string that obscures the official title-page group attribution.
- **Reconciliation:**
  - Bibliographic Entry:
    > `Qwen Team. (2024). *Qwen2.5 technical report*. arXiv preprint arXiv:2412.15115. URL: https://arxiv.org/abs/2412.15115.`
  - In-Text Citations: Standardized to `(Qwen Team, 2024)` across Section 1 (line 73) and Section 2.2 (line 121), replacing `(Yang et al., 2024)`.

---

## 5. APA 7 Reference Standardization

### 5.1 Consolidating Reference Subsections
Under strict APA 7 guidelines, reference lists are not partitioned by document genre (e.g., "Peer-Reviewed Conference Papers", "Preprints", "Software Repositories"). Section 13 has been consolidated into a **single, unified alphabetical list**.

### 5.2 Sentence Case for Work Titles
All work titles (journal articles, conference papers, preprints, and repositories) have been converted to sentence case in accordance with APA 7 Section 9.19 (capitalizing only the first word of the title, the first word after a colon/em-dash, and proper nouns such as DICES, LLM, LLMs, AI, PandaLM, SafetyBench, MT-Bench, Chatbot Arena, SmolLM2, Qwen2.5, GPT-4).

### 5.3 Complete Author Lists & Alphabetical Verification
- **PandaLM (ICLR 2024):** All 14 verified co-authors are listed in full.
- **Qwen2.5:** Listed under `Qwen Team` and alphabetized under `Q`.
- **Zhang Entries:** `Zhang, Y.` (2026) is sorted before `Zhang, Z.` (2024).
- **In-Text Cross-Verification:** Every in-text citation in `TRUSTEVAL_PAPER_V2_5_3_4.md` was verified to match an entry in the consolidated bibliography.

---

## 6. Regression Terminology Standardization

### 6.1 Elimination of "Baseline Predicted Probability"
In Phase 3C.6.3, the phrase "baseline confidence" was replaced with "baseline predicted probability". However, in nested OLS modeling, the baseline predictor is $P_{\text{ensemble}}$ (the ensemble predicted unsafe probability). Phrasing this as "baseline predicted probability" created ambiguity regarding whether a separate baseline model's predictions were used as a covariate.

### 6.2 Standardized Formulation
Terminology has been harmonized across the manuscript to use **"ensemble predicted unsafe probability ($P_{\text{ensemble}})$"**:
- **Abstract line 33:**
  > *"...predicting ensemble error beyond conversational length and ensemble predicted unsafe probability ($P_{\text{ensemble}}$)."*
- **Section 1.1 RQ3 (line 95):**
  > *"...predicting uncertainty beyond response length and ensemble predicted unsafe probability ($P_{\text{ensemble}}$)?"*
- **Abstract Finding 4 (line 45) & Section 9.1:** Maintained consistent phrasing:
  > *"In nested in-sample OLS modeling controlling for response length and ensemble predicted unsafe probability ($P_{\text{ensemble}}$), adding disagreement accounts for nominally significant incremental variance..."*

---

## 7. Archival Integrity & Cryptographic Telemetry Ledger

### 7.1 Telemetry Analysis for 27 Pre-3C.6.3 Artifacts
We examine historical cryptographic hashes recorded in earlier audit reports versus current physical files on disk:
- **Recorded in Phase 3C.6.2 (Table 6.2):** 22 prior files had their full 64-character SHA-256 digests recorded in execution telemetry. All 22 files match their recorded digests **100% identically**, establishing cryptographically verifiable preservation.
- **Unrecorded in Phase 3C.6.2:** Five files (`PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` [self-referential in 3C.6.2], `PHASE_3C_REFINEMENT_REPORT.md`, `PUBLICATION_VENUE_SHORTLIST.md`, `SUBMISSION_READINESS_CHECKLIST.md`, and `V2_1_CORRECTION_REPORT.md`) were omitted from Table 6.2 in Phase 3C.6.2. In adherence to rigorous reporting standards:
  > **Methodological Note:** Because SHA-256 digests for these 5 files were not recorded in Table 6.2 of Phase 3C.6.2, their historical byte-for-byte preservation prior to Phase 3C.6.3 cannot be independently established from that telemetry table alone. However, their physical digests were recorded in Phase 3C.6.3 and confirmed 100% unchanged in Phase 3C.6.4.

| File Path | Classification | Pre-3C.6.3 Recorded SHA-256 | Current Phase 3C.6.4 SHA-256 | Telemetry Verification Status |
| :--- | :---: | :--- | :--- | :---: |
| `TRUSTEVAL_PAPER_DRAFT.md` | Draft | `519f3261ac013a3eacc5eec52778fb676b2a719988ee1a7d241119b07fcae66c` | `519f3261ac013a3eacc5eec52778fb676b2a719988ee1a7d241119b07fcae66c` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2.md` | V2 | `d718992ba8e7c58015b80c6fa8d4de260763cee4edb085d92991583c3b4a55a6` | `d718992ba8e7c58015b80c6fa8d4de260763cee4edb085d92991583c3b4a55a6` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_1.md` | V2.1 | `f4e5553ce192eda4b38f5278373a6ea7fac2d63b5c23f2f1400bf99ef174f91a` | `f4e5553ce192eda4b38f5278373a6ea7fac2d63b5c23f2f1400bf99ef174f91a` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_2.md` | V2.2 | `36c86052a3397fc9b6682264b060f7b5dbf164d60b34a93b988e100483f892d9` | `36c86052a3397fc9b6682264b060f7b5dbf164d60b34a93b988e100483f892d9` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_3.md` | V2.3 | `bac248035e559e4cc6b975470557d50b548a4e5273fbaf68bfe20010200c948e` | `bac248035e559e4cc6b975470557d50b548a4e5273fbaf68bfe20010200c948e` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_4.md` | V2.4 | `be30770f0ae1ce43e7ad2e2bfc0958fe8e57bd5ff8f9939db7e932da7917557f` | `be30770f0ae1ce43e7ad2e2bfc0958fe8e57bd5ff8f9939db7e932da7917557f` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_5.md` | V2.5 | `48c448b54333b51af86137dd0865eb5b3568cdf172bf7067fd80ed0d569a4d55` | `48c448b54333b51af86137dd0865eb5b3568cdf172bf7067fd80ed0d569a4d55` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_5_1.md` | V2.5.1 | `8abb4f34db5c599d6110781c0fbbf84caf857d5c70457f5e462bd339a40e721d` | `8abb4f34db5c599d6110781c0fbbf84caf857d5c70457f5e462bd339a40e721d` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_5_2.md` | V2.5.2 | `45a46552ee2ad377a78fb5972d55099b858fdcde87c0523077ff9d495da9f5fd` | `45a46552ee2ad377a78fb5972d55099b858fdcde87c0523077ff9d495da9f5fd` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_5_3.md` | V2.5.3 | `980b532c8500bdbdd7ab717ab9acded390479cecbd96d0a48fdbc8788f41e13a` | `980b532c8500bdbdd7ab717ab9acded390479cecbd96d0a48fdbc8788f41e13a` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_5_3_1.md` | V2.5.3.1 | `3c2b74edfaa59665b39441a7701aabfdffd8b0535a4241be819aca9caacd6536` | `3c2b74edfaa59665b39441a7701aabfdffd8b0535a4241be819aca9caacd6536` | **Verified Match** |
| `TRUSTEVAL_PAPER_V2_5_3_2.md` | V2.5.3.2 | `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc` | `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc` | **Verified Match** |
| `PHASE_2B_REVISION_REPORT.md` | Report | `70a645d903f170c75f1fe40150f898c17c349f50233a109b78a7143754fffa33` | `70a645d903f170c75f1fe40150f898c17c349f50233a109b78a7143754fffa33` | **Verified Match** |
| `PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md` | Report | `bcb81b8170b21143882f4a90c689e490efd01d03d1af3b2a058edad984776a7e` | `bcb81b8170b21143882f4a90c689e490efd01d03d1af3b2a058edad984776a7e` | **Verified Match** |
| `PHASE_3B_CORRECTION_REPORT.md` | Report | `f6db472a6fd81f7d96201da971e342f1e5582f398d0b81e76e7fcb7d98dc3610` | `f6db472a6fd81f7d96201da971e342f1e5582f398d0b81e76e7fcb7d98dc3610` | **Verified Match** |
| `PHASE_3C_1_VERIFICATION_REPORT.md` | Report | `0f66c54bdc19af1b2af43c2f16860763102ab9b04aa41fa86742a0971633db23` | `0f66c54bdc19af1b2af43c2f16860763102ab9b04aa41fa86742a0971633db23` | **Verified Match** |
| `PHASE_3C_2_CORRECTION_REPORT.md` | Report | `119d0f63be023486c00e5cd671e7817cb1e924b6b490c1ad5c5dd0dd1de25d9f` | `119d0f63be023486c00e5cd671e7817cb1e924b6b490c1ad5c5dd0dd1de25d9f` | **Verified Match** |
| `PHASE_3C_3_FINAL_AUDIT_REPORT.md` | Report | `e261c2d6e26e64c440bf1cf7c2463a0b4c1ff933b8e28979c8a65ca555f5bc92` | `e261c2d6e26e64c440bf1cf7c2463a0b4c1ff933b8e28979c8a65ca555f5bc92` | **Verified Match** |
| `PHASE_3C_4_ERRATA_REPORT.md` | Report | `d3d8c4bacdfb52aa12a37c8afdab465d25035b03a52974c44f15aba5e0394856` | `d3d8c4bacdfb52aa12a37c8afdab465d25035b03a52974c44f15aba5e0394856` | **Verified Match** |
| `PHASE_3C_5_FINAL_AUDIT_REPORT.md` | Report | `da90c3604864a82a18d10832e71f16d0d7599fefc444aa94bdb14baf48dfd019` | `da90c3604864a82a18d10832e71f16d0d7599fefc444aa94bdb14baf48dfd019` | **Verified Match** |
| `PHASE_3C_6_FINAL_AUDIT_REPORT.md` | Report | `140f1e891a9a90d0ea76767c6a187b477a6ee9deb2b5e32194c077e8135a5570` | `140f1e891a9a90d0ea76767c6a187b477a6ee9deb2b5e32194c077e8135a5570` | **Verified Match** |
| `PHASE_3C_6_1_RECONCILIATION_REPORT.md` | Report | `27543bd95634abf3de8f8699b9818fea7387d7c70991f56861c00f00735093c0` | `27543bd95634abf3de8f8699b9818fea7387d7c70991f56861c00f00735093c0` | **Verified Match** |
| `PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` | Report | *Unrecorded in 3C.6.2* | `72d7d89d0af035b4c797ab2e2ad3945c328b979d9ec2faf1af493f21efd3323a` | Established in 3C.6.3 |
| `PHASE_3C_REFINEMENT_REPORT.md` | Report | *Unrecorded in 3C.6.2* | `1dfa5793d8cfd1b38089c01040dce543d736037af413783fe1d9ac5fbcfb29c6` | Established in 3C.6.3 |
| `PUBLICATION_VENUE_SHORTLIST.md` | Ref Doc | *Unrecorded in 3C.6.2* | `d9d8573eb25f4ffd77e98a3559aec34cfc60fa1e013fe59ec0851e3dd6eb17f9` | Established in 3C.6.3 |
| `SUBMISSION_READINESS_CHECKLIST.md` | Gov Doc | *Unrecorded in 3C.6.2* | `fca2ce857fab69047a49d91109ec8f382a22c7d49101efd7e8fc1061613be65c` | Established in 3C.6.3 |
| `V2_1_CORRECTION_REPORT.md` | Report | *Unrecorded in 3C.6.2* | `5b22ea4e204798cce3032241ecf8cdda62b39e0a834f138f71aa5ef76865ae00` | Established in 3C.6.3 |

---

### 7.2 Complete 31-File Physical Inventory of `research/paper/`

All 31 artifacts currently present in `research/paper/` are inventoried below with exact byte sizes and SHA-256 digests:

| # | Artifact Path | Classification | Exact Size | Measured SHA-256 Digest |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `PHASE_2B_REVISION_REPORT.md` | Audit Report | 13,378 bytes | `70a645d903f170c75f1fe40150f898c17c349f50233a109b78a7143754fffa33` |
| 2 | `PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md` | Audit Report | 28,370 bytes | `bcb81b8170b21143882f4a90c689e490efd01d03d1af3b2a058edad984776a7e` |
| 3 | `PHASE_3B_CORRECTION_REPORT.md` | Audit Report | 15,820 bytes | `f6db472a6fd81f7d96201da971e342f1e5582f398d0b81e76e7fcb7d98dc3610` |
| 4 | `PHASE_3C_1_VERIFICATION_REPORT.md` | Audit Report | 38,748 bytes | `0f66c54bdc19af1b2af43c2f16860763102ab9b04aa41fa86742a0971633db23` |
| 5 | `PHASE_3C_2_CORRECTION_REPORT.md` | Audit Report | 19,588 bytes | `119d0f63be023486c00e5cd671e7817cb1e924b6b490c1ad5c5dd0dd1de25d9f` |
| 6 | `PHASE_3C_3_FINAL_AUDIT_REPORT.md` | Audit Report | 17,017 bytes | `e261c2d6e26e64c440bf1cf7c2463a0b4c1ff933b8e28979c8a65ca555f5bc92` |
| 7 | `PHASE_3C_4_ERRATA_REPORT.md` | Audit Report | 18,629 bytes | `d3d8c4bacdfb52aa12a37c8afdab465d25035b03a52974c44f15aba5e0394856` |
| 8 | `PHASE_3C_5_FINAL_AUDIT_REPORT.md` | Audit Report | 17,628 bytes | `da90c3604864a82a18d10832e71f16d0d7599fefc444aa94bdb14baf48dfd019` |
| 9 | `PHASE_3C_6_1_RECONCILIATION_REPORT.md` | Audit Report | 15,303 bytes | `27543bd95634abf3de8f8699b9818fea7387d7c70991f56861c00f00735093c0` |
| 10 | `PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` | Audit Report | 15,513 bytes | `72d7d89d0af035b4c797ab2e2ad3945c328b979d9ec2faf1af493f21efd3323a` |
| 11 | `PHASE_3C_6_3_FINAL_REPRODUCIBILITY_REPORT.md` | Audit Report | 19,449 bytes | `76406ee755787283b75a963211448ab5ab4412b4766b2155b2a872272581794a` |
| 12 | `PHASE_3C_6_FINAL_AUDIT_REPORT.md` | Audit Report | 18,859 bytes | `140f1e891a9a90d0ea76767c6a187b477a6ee9deb2b5e32194c077e8135a5570` |
| 13 | `PHASE_3C_REFINEMENT_REPORT.md` | Audit Report | 27,345 bytes | `1dfa5793d8cfd1b38089c01040dce543d736037af413783fe1d9ac5fbcfb29c6` |
| 14 | `PUBLICATION_VENUE_SHORTLIST.md` | Reference Doc | 18,269 bytes | `d9d8573eb25f4ffd77e98a3559aec34cfc60fa1e013fe59ec0851e3dd6eb17f9` |
| 15 | `SUBMISSION_READINESS_CHECKLIST.md` | Governance Doc | 14,125 bytes | `fca2ce857fab69047a49d91109ec8f382a22c7d49101efd7e8fc1061613be65c` |
| 16 | `TRUSTEVAL_PAPER_DRAFT.md` | Manuscript Draft | 17,676 bytes | `519f3261ac013a3eacc5eec52778fb676b2a719988ee1a7d241119b07fcae66c` |
| 17 | `TRUSTEVAL_PAPER_V2.md` | Manuscript V2 | 50,850 bytes | `d718992ba8e7c58015b80c6fa8d4de260763cee4edb085d92991583c3b4a55a6` |
| 18 | `TRUSTEVAL_PAPER_V2_1.md` | Manuscript V2.1 | 57,198 bytes | `f4e5553ce192eda4b38f5278373a6ea7fac2d63b5c23f2f1400bf99ef174f91a` |
| 19 | `TRUSTEVAL_PAPER_V2_2.md` | Manuscript V2.2 | 58,840 bytes | `36c86052a3397fc9b6682264b060f7b5dbf164d60b34a93b988e100483f892d9` |
| 20 | `TRUSTEVAL_PAPER_V2_3.md` | Manuscript V2.3 | 64,874 bytes | `bac248035e559e4cc6b975470557d50b548a4e5273fbaf68bfe20010200c948e` |
| 21 | `TRUSTEVAL_PAPER_V2_4.md` | Manuscript V2.4 | 70,116 bytes | `be30770f0ae1ce43e7ad2e2bfc0958fe8e57bd5ff8f9939db7e932da7917557f` |
| 22 | `TRUSTEVAL_PAPER_V2_5.md` | Manuscript V2.5 | 73,990 bytes | `48c448b54333b51af86137dd0865eb5b3568cdf172bf7067fd80ed0d569a4d55` |
| 23 | `TRUSTEVAL_PAPER_V2_5_1.md` | Manuscript V2.5.1 | 76,572 bytes | `8abb4f34db5c599d6110781c0fbbf84caf857d5c70457f5e462bd339a40e721d` |
| 24 | `TRUSTEVAL_PAPER_V2_5_2.md` | Manuscript V2.5.2 | 78,785 bytes | `45a46552ee2ad377a78fb5972d55099b858fdcde87c0523077ff9d495da9f5fd` |
| 25 | `TRUSTEVAL_PAPER_V2_5_3.md` | Manuscript V2.5.3 | 81,094 bytes | `980b532c8500bdbdd7ab717ab9acded390479cecbd96d0a48fdbc8788f41e13a` |
| 26 | `TRUSTEVAL_PAPER_V2_5_3_1.md` | Manuscript V2.5.3.1 | 83,051 bytes | `3c2b74edfaa59665b39441a7701aabfdffd8b0535a4241be819aca9caacd6536` |
| 27 | `TRUSTEVAL_PAPER_V2_5_3_2.md` | Manuscript V2.5.3.2 | 82,916 bytes | `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc` |
| 28 | `TRUSTEVAL_PAPER_V2_5_3_3.md` | Manuscript V2.5.3.3 | 86,185 bytes | `207d904b88f3640600aace901e732ed7ecaf8d921564e71ac4bb028654c66e84` |
| 29 | `TRUSTEVAL_PAPER_V2_5_3_4.md` | **Current Master Manuscript** | **87,014 bytes** | `eaab250fba8f2ee175e43195de97251377b23c6eb7950d2f360a237b448a179a` |
| 30 | `V2_1_CORRECTION_REPORT.md` | Audit Report | 19,654 bytes | `5b22ea4e204798cce3032241ecf8cdda62b39e0a834f138f71aa5ef76865ae00` |
| 31 | `PHASE_3C_6_4_FINAL_RECONCILIATION_REPORT.md` | **Phase 3C.6.4 Audit Report** | **24899 bytes** | `[Self-referential; verified upon completion]` |

---

## 8. Deliverable Telemetry & Verification Scans

### Deliverable Geometry
- **Master Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_3_4.md`  
  - Line Count: 1,176  
  - Exact Byte Count: 87,014 bytes  
  - Cryptographic SHA-256 Digest: `eaab250fba8f2ee175e43195de97251377b23c6eb7950d2f360a237b448a179a`  
- **Audit Report:** `research/paper/PHASE_3C_6_4_FINAL_RECONCILIATION_REPORT.md`  
  - Line Count: 239  
  - Exact Byte Count: 24899 bytes  
  - Cryptographic SHA-256 Digest: `[Self-referential; verified upon completion]`

### Control Character Integrity Scan
A byte-level verification scan across both deliverables confirmed:
- Non-printing ASCII control bytes ($< 32$, excluding `\t`, `\n`, `\r`): **0** (CLEAN).

---

## 9. Remaining Study Limitations

In accordance with transparent reporting, the following methodological boundaries remain:
1. **Sample Size ($N=50$):** Modest sample size limits power for fine-grained demographic subgroup stratification; 11 positive-class items result in wide marginal AUROC confidence intervals.
2. **Model Weight Provenance Limitation:** Historical prediction records logged branch `main` and commit `null`. While local cached snapshot commits were identified post-hoc (`7ae557604adf...` for Qwen and `31b70e2e869a...` for SmolLM2), no runtime execution log independently captured the commit SHA.
3. **Prompt Immutability Verification:** Although the study intended to evaluate an invariant prompt template, historical byte-level immutability cannot be proven without timestamped cryptographic commit baselines.
4. **Shared-Rater Non-Independence:** All 50 conversations were annotated by a shared cohort of 104 raters. Ordinary correlation and regression inferential $p$-values do not adjust for cross-item dependency induced by repeated ratings from this shared pool and are exploratory and conditional on sample consensus.
5. **No Intermediate Chain-of-Thought:** Direct next-token logit extraction provides deterministic probability estimates but restricts the models from generating intermediate reasoning tokens.
6. **Hardware Latency Bounds:** BF16 software execution on consumer x86 CPU hardware required $\approx 135\text{ s/item}$ for SmolLM2-1.7B, indicating that high-throughput deployment requires quantization (e.g., INT4) or hardware acceleration.
