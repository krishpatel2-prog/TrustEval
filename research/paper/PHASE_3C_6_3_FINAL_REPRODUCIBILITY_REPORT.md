# Phase 3C.6.3 Final Reproducibility and Manuscript Consistency Audit Report

**Project:** TrustEval  
**Workspace:** `D:\Research\TrustEval`  
**Audit Phase:** Phase 3C.6.3 — Final Reproducibility, Provenance, and Manuscript Consistency Audit  
**Date:** November 2026  
**Auditor:** Scientific Integrity and Methodological Audit Team  
**Status:** Complete & Fully Reconciled  
- Base Master Manuscript: `research/paper/TRUSTEVAL_PAPER_V2_5_3_2.md` (82,916 bytes, SHA-256: `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc`)  
- Prior Audit Report: `research/paper/PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` (15,513 bytes, SHA-256: `72d7d89d0af035b4c797ab2e2ad3945c328b979d9ec2faf1af493f21efd3323a`)  
- New Master Manuscript: `research/paper/TRUSTEVAL_PAPER_V2_5_3_3.md` (86,185 bytes, SHA-256: `207d904b88f3640600aace901e732ed7ecaf8d921564e71ac4bb028654c66e84`)  
- New Audit Report: `research/paper/PHASE_3C_6_3_FINAL_REPRODUCIBILITY_REPORT.md` (19449 bytes, SHA-256: `[Self-referential; verified upon completion]`)

---

## 1. Executive Summary & Audit Objectives

Phase 3C.6.3 represents a targeted reproducibility, provenance reconciliation, and terminology consistency audit following the Phase 3C.6.2 correction pass. The audit focused on resolving residual internal tensions, harmonizing statistical nomenclature, updating bibliographic records to strict APA 7 standards, and establishing an exhaustive, unomitted cryptographic ledger of all artifacts within the `research/paper/` directory.

### Key Objectives Accomplished:
1. **Prompt Immutability Contradiction Resolution:** Reconciled Section 4.2 so that the prompt serialization text no longer asserts unverified byte-for-byte immutability across historical runs, aligning it directly with the documented prompt-hash provenance note.
2. **Model-Weight Provenance & Snapshot Commit Distinction:** Clarified Section 4.1 by distinguishing the tracked branch revision (`model_revision: "main"`) recorded in prediction JSONL records from the specific snapshot commits identified post-hoc in the local Hugging Face cache, formally documenting the unrecorded runtime commit as a provenance limitation.
3. **Enterprise Data Privacy & Regulatory Statement:** Replaced overgeneralized assertions regarding GDPR/HIPAA compliance in Section 1 with an accurate characterization of legal bases, Data Processing Agreements (DPAs), and HIPAA Business Associate Agreements (BAAs).
4. **APA 7 Reference Standardization:** Expanded the PandaLM (ICLR 2024) citation to list all 14 co-authors, standardized the Qwen2.5 Technical Report (arXiv:2412.15115) to APA 7 format for $\ge 21$ authors (first 19 authors followed by an ellipsis and the final author), and strictly alphabetized the `Preprints & Technical Reports` section by primary author surname.
5. **Wilcoxon Signed-Rank Test Interpretation:** Corrected Section 6.3 to eliminate the claim that non-normality caused the Wilcoxon test to fail Holm correction, explicitly documenting that Wilcoxon evaluates location shifts under paired symmetry assumptions, reporting exact $p$-values across paired tests, and concluding that the SmolLM2-vs-ensemble MAE advantage is test-sensitive.
6. **Regression Terminology Standardization:** Replaced ambiguous phrasing ("ensemble confidence", "baseline confidence") with precise descriptors ("ensemble predicted unsafe probability ($P_{\text{ensemble}}$)", "baseline predicted probability") across the Abstract, Section 1.1 (RQ3), Section 7.3, and Section 9.1.
7. **Shared-Rater Clustering Uncertainty:** Added a dedicated methodological limitation in Section 10 documenting that the 50 conversations were evaluated by a shared cohort of 104 annotators, noting that standard correlation/regression $p$-values do not account for clustering induced by this shared rater pool.
8. **Audit Report Language & Complete Directory Ledger:** Standardized audit descriptions of the conversational prompt hash (`15f18333f07a7261...`) as an "unverified conversational hash string with no supporting project-file record", and cataloged all 29 files in `research/paper/` without omissions.
9. **Abstract Terminology Harmonization:** Replaced the phrase "calibration drift" with "miscalibration" in the Abstract.

---

## 2. Detailed Audit Findings & Implemented Changes

### 2.1 Prompt Immutability Contradiction (Section 4.2)
- **Identified Defect:** Section 4.2 contained an internal contradiction. While the provenance note correctly stated that historical byte-level prompt provenance is unverified because no project file hashes to the configured label `15f18333a682867c...`, subsection `#### Prompt Serialization and Native Chat Templates` previously claimed:
  > *"This duplication is a frozen artifact of the initial evaluation prompt (`configs/prompts/safety_judge_v1.txt`), which was preserved immutably throughout all experimental runs to protect protocol fidelity."*
- **Reconciliation:** The sentence was updated in `TRUSTEVAL_PAPER_V2_5_3_3.md` to:
  > *"This duplication is a frozen structural feature of the evaluation prompt template stored in `configs/prompts/safety_judge_v1.txt`. While the experimental protocol intended to evaluate an invariant prompt template across all experimental runs, historical byte-level immutability across historical inference executions cannot be independently established without timestamped cryptographic commit baselines (as detailed in the provenance note above)."*

### 2.2 Model-Weight Provenance & Snapshot Commit Distinction (Section 4.1)
- **Identified Defect:** Historical prediction records in `results/predictions/*.jsonl` log `model_revision: "main"` and `commit: null`. The specific snapshot commits (`7ae557604adf67be50417f59c2c2f167def9a775` for Qwen and `31b70e2e869a7173562077fd711b654946d38674` for SmolLM2) were identified post-hoc from the local Hugging Face cache directories. Presenting these snapshot SHAs without distinguishing them from runtime logs created an unsupported provenance claim.
- **Reconciliation:** A dedicated `[!NOTE]` was added to Section 4.1:
  > *"Historical prediction records in `results/predictions/` explicitly record the repository branch revision (`model_revision: "main"`), while leaving the commit SHA unrecorded (`commit: null`). The specific commit SHAs reported above (`7ae557604adf67be50417f59c2c2f167def9a775` for Qwen and `31b70e2e869a7173562077fd711b654946d38674` for SmolLM2) were identified through post-hoc inspection of the local Hugging Face snapshot cache directory. Because no execution log cryptographically captured the exact commit hash during inference runtime, we document this distinction as an unresolved model-weight provenance limitation: the local snapshot commits represent the best available local artifacts, but cannot be independently verified from inference-time logs."*

### 2.3 Regulatory & Enterprise Privacy Framing (Section 1)
- **Identified Defect:** Section 1 previously made an overgeneralized claim: *"Routing internal dialogues to cloud APIs violates enterprise confidentiality and regulatory mandates (e.g., GDPR, HIPAA)."* This ignored that enterprise cloud deployments frequently utilize standard contractual clauses, DPAs, and HIPAA BAAs.
- **Reconciliation:** Replaced with an accurate, defensible formulation:
  > *"1. **Data Confidentiality & Privacy:** External processing introduces confidentiality, data leakage, and compliance risks. While lawful cloud processing may be established through formal legal bases, comprehensive Data Processing Agreements (DPAs), technical safeguards, and HIPAA Business Associate Agreements (BAAs) where applicable, transmitting sensitive enterprise dialogues creates ongoing regulatory overhead. Local model execution eliminates cross-boundary data transmission entirely, significantly simplifying compliance."*

### 2.4 APA 7 Reference Standardization (Section 13)
- **PandaLM (ICLR 2024):** All 14 authors were verified against OpenReview (`75qZ392iX4`) and formatted in full:
  > `Wang, Y., Yu, Z., Yao, W., Zeng, Z., Yang, L., Wang, C., Chen, H., Jiang, C., Xie, R., Wang, J., Xie, X., Ye, W., Zhang, S., & Zhang, Y. (2024). PandaLM: An Automatic Evaluation Benchmark for LLM Instruction Tuning Optimization. *The Twelfth International Conference on Learning Representations (ICLR)*. OpenReview: 75qZ392iX4.`
- **Qwen2.5 Technical Report (arXiv:2412.15115):** The 43-author preprint was formatted under APA 7 rules for $\ge 21$ authors (first 19 authors, ellipsis, final author):
  > `Yang, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Li, C., Liu, D., Huang, F., Wei, H., Lin, H., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J., Zhou, J., Lin, J., Dang, K., ... Qiu, Z. (2024). *Qwen2.5 Technical Report*. arXiv preprint arXiv:2412.15115. URL: https://arxiv.org/abs/2412.15115.`
- **Alphabetical Sorting:** The `Preprints & Technical Reports` section was re-ordered alphabetically by the first author's surname:
  1. Ben Allal, L., et al. (2025)
  2. Chiang, W.-L., et al. (2023)
  3. Li, Y. (2026)
  4. Verga, P., et al. (2024)
  5. Yang, A., et al. (2024)
  6. Zhang, Y., et al. (2026)

### 2.5 Wilcoxon Signed-Rank Test Interpretation (Section 6.3)
- **Identified Defect:** Section 6.3 previously claimed that the Wilcoxon test did not survive Holm correction *"due to severe non-normality in paired absolute error differences"*. This was theoretically inverted: Wilcoxon is a non-parametric test designed specifically for non-normal data, but it assumes symmetry of paired differences when testing location shifts.
- **Reconciliation:** Section 6.3 Item 1 was updated to state:
  > *"SmolLM2 achieves lower sample MAE than the Ensemble ($0.1734$ vs. $0.2464$; mean diff $=-0.0730$). However, the statistical significance of this MAE advantage is sensitive to the inferential test selected: while significant under the parametric paired $t$-test (paired $t = -2.38$, unadjusted $p = 0.0213$, $p_{\text{Holm}} = 0.0425$) and the non-parametric sign test (36 vs. 14 wins, unadjusted $p = 0.0026$, $p_{\text{Holm}} = 0.0026$), it does not survive family-wise Holm adjustment under the Wilcoxon signed-rank test ($W = 427.0$, unadjusted $p = 0.0421$, $p_{\text{Holm}} = 0.0843$, n.s.). Although the paired absolute differences exhibit skewness and violate normality (Shapiro-Wilk $W = 0.8776, p = 9.47 \times 10^{-5}$), the Wilcoxon signed-rank test is not entirely assumption-free: interpreting it as a test of median difference or location shift requires symmetry of the paired difference distribution. Given this test sensitivity, the MAE advantage of SmolLM2 over the ensemble cannot be considered unambiguously established across all standard testing frameworks. In squared error (Soft MSE), **no statistically significant difference was detected** between SmolLM2 and the Ensemble ($0.0628$ vs. $0.0713$, paired $t = -0.47$, unadjusted $p = 0.6425$, $p_{\text{Holm}} = 0.6425$)."*

### 2.6 Regression Terminology Standardization
- **Standardization:** Ambiguous occurrences of "ensemble confidence" and "baseline confidence" were replaced with unambiguous statistical terms:
  - Abstract (Finding 4): `"controlling for response length and ensemble predicted unsafe probability ($P_{\text{ensemble}}$)"`
  - Abstract & Section 1.1 (RQ3): `"beyond conversational length and baseline predicted probability"`
  - Section 9.1 (RQ3 paragraph): `"controlling for response length and ensemble predicted unsafe probability ($P_{\text{ensemble}}$)"`

### 2.7 Shared-Rater Correlation Uncertainty Limitation (Section 10)
- **Methodological Context:** In DICES-350, all 50 conversations were evaluated by a shared pool of 104 annotators. Ordinary Pearson and Spearman inferential $p$-values assume independent observations and do not account for cross-item dependency induced by repeated ratings from the same individuals.
- **Added Subsection:** Section 10.6 was incorporated:
  > *"6. **Shared-Rater Clustering and Correlation Inference:** The 50 evaluated conversations were annotated by a shared pool of 104 crowd workers who each rated multiple items across the benchmark. Ordinary inferential procedures for Pearson correlation, Spearman rank correlation, and OLS regression treat individual conversational items as independent and identically distributed observations; they do not account for clustering or non-independence introduced by repeated ratings from this shared rater cohort. Consequently, the correlation and regression $p$-values reported in this study must be interpreted as exploratory and conditional on the observed item-level consensus. To address this structure in error metrics, we reported a rater-cluster bootstrap (Section 7.4); extending two-way cluster-robust inference or multi-level rater bootstrapping to rank correlation and OLS specifications represents an important sensitivity analysis for future evaluations on larger sample cohorts."*

### 2.8 Audit Nomenclature & Ephemeral Hash String Status
- **Correction:** The ephemeral string `15f18333f07a7261...` that appeared in Phase 3C.6 execution telemetry was previously referred to as a "proven LLM hallucination". In this report and going forward, it is strictly described as an **"unverified conversational hash string with no supporting project-file record"**.

### 2.9 Abstract Miscalibration Terminology
- **Correction:** In line 29 of the Abstract, the phrase "calibration drift" was replaced with "miscalibration".

---

## 3. Comprehensive Inventory of `research/paper/` Directory

Every artifact present in `research/paper/` (including all prior manuscripts, auditing reports, venue lists, checklists, and newly produced deliverables) is cataloged below with its physical byte size and verified cryptographic SHA-256 digest.

| Artifact Path | Classification | Exact Size | Measured SHA-256 Digest |
| :--- | :---: | :---: | :--- |
| `PHASE_2B_REVISION_REPORT.md` | Audit Report | 13,378 bytes | `70a645d903f170c75f1fe40150f898c17c349f50233a109b78a7143754fffa33` |
| `PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md` | Audit Report | 28,370 bytes | `bcb81b8170b21143882f4a90c689e490efd01d03d1af3b2a058edad984776a7e` |
| `PHASE_3B_CORRECTION_REPORT.md` | Audit Report | 15,820 bytes | `f6db472a6fd81f7d96201da971e342f1e5582f398d0b81e76e7fcb7d98dc3610` |
| `PHASE_3C_1_VERIFICATION_REPORT.md` | Audit Report | 38,748 bytes | `0f66c54bdc19af1b2af43c2f16860763102ab9b04aa41fa86742a0971633db23` |
| `PHASE_3C_2_CORRECTION_REPORT.md` | Audit Report | 19,588 bytes | `119d0f63be023486c00e5cd671e7817cb1e924b6b490c1ad5c5dd0dd1de25d9f` |
| `PHASE_3C_3_FINAL_AUDIT_REPORT.md` | Audit Report | 17,017 bytes | `e261c2d6e26e64c440bf1cf7c2463a0b4c1ff933b8e28979c8a65ca555f5bc92` |
| `PHASE_3C_4_ERRATA_REPORT.md` | Audit Report | 18,629 bytes | `d3d8c4bacdfb52aa12a37c8afdab465d25035b03a52974c44f15aba5e0394856` |
| `PHASE_3C_5_FINAL_AUDIT_REPORT.md` | Audit Report | 17,628 bytes | `da90c3604864a82a18d10832e71f16d0d7599fefc444aa94bdb14baf48dfd019` |
| `PHASE_3C_6_1_RECONCILIATION_REPORT.md` | Audit Report | 15,303 bytes | `27543bd95634abf3de8f8699b9818fea7387d7c70991f56861c00f00735093c0` |
| `PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` | Audit Report | 15,513 bytes | `72d7d89d0af035b4c797ab2e2ad3945c328b979d9ec2faf1af493f21efd3323a` |
| `PHASE_3C_6_FINAL_AUDIT_REPORT.md` | Audit Report | 18,859 bytes | `140f1e891a9a90d0ea76767c6a187b477a6ee9deb2b5e32194c077e8135a5570` |
| `PHASE_3C_REFINEMENT_REPORT.md` | Audit Report | 27,345 bytes | `1dfa5793d8cfd1b38089c01040dce543d736037af413783fe1d9ac5fbcfb29c6` |
| `PUBLICATION_VENUE_SHORTLIST.md` | Reference Doc | 18,269 bytes | `d9d8573eb25f4ffd77e98a3559aec34cfc60fa1e013fe59ec0851e3dd6eb17f9` |
| `SUBMISSION_READINESS_CHECKLIST.md` | Governance Doc | 14,125 bytes | `fca2ce857fab69047a49d91109ec8f382a22c7d49101efd7e8fc1061613be65c` |
| `TRUSTEVAL_PAPER_DRAFT.md` | Manuscript Draft | 17,676 bytes | `519f3261ac013a3eacc5eec52778fb676b2a719988ee1a7d241119b07fcae66c` |
| `TRUSTEVAL_PAPER_V2.md` | Manuscript V2 | 50,850 bytes | `d718992ba8e7c58015b80c6fa8d4de260763cee4edb085d92991583c3b4a55a6` |
| `TRUSTEVAL_PAPER_V2_1.md` | Manuscript V2.1 | 57,198 bytes | `f4e5553ce192eda4b38f5278373a6ea7fac2d63b5c23f2f1400bf99ef174f91a` |
| `TRUSTEVAL_PAPER_V2_2.md` | Manuscript V2.2 | 58,840 bytes | `36c86052a3397fc9b6682264b060f7b5dbf164d60b34a93b988e100483f892d9` |
| `TRUSTEVAL_PAPER_V2_3.md` | Manuscript V2.3 | 64,874 bytes | `bac248035e559e4cc6b975470557d50b548a4e5273fbaf68bfe20010200c948e` |
| `TRUSTEVAL_PAPER_V2_4.md` | Manuscript V2.4 | 70,116 bytes | `be30770f0ae1ce43e7ad2e2bfc0958fe8e57bd5ff8f9939db7e932da7917557f` |
| `TRUSTEVAL_PAPER_V2_5.md` | Manuscript V2.5 | 73,990 bytes | `48c448b54333b51af86137dd0865eb5b3568cdf172bf7067fd80ed0d569a4d55` |
| `TRUSTEVAL_PAPER_V2_5_1.md` | Manuscript V2.5.1 | 76,572 bytes | `8abb4f34db5c599d6110781c0fbbf84caf857d5c70457f5e462bd339a40e721d` |
| `TRUSTEVAL_PAPER_V2_5_2.md` | Manuscript V2.5.2 | 78,785 bytes | `45a46552ee2ad377a78fb5972d55099b858fdcde87c0523077ff9d495da9f5fd` |
| `TRUSTEVAL_PAPER_V2_5_3.md` | Manuscript V2.5.3 | 81,094 bytes | `980b532c8500bdbdd7ab717ab9acded390479cecbd96d0a48fdbc8788f41e13a` |
| `TRUSTEVAL_PAPER_V2_5_3_1.md` | Manuscript V2.5.3.1 | 83,051 bytes | `3c2b74edfaa59665b39441a7701aabfdffd8b0535a4241be819aca9caacd6536` |
| `TRUSTEVAL_PAPER_V2_5_3_2.md` | Manuscript V2.5.3.2 | 82,916 bytes | `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc` |
| `TRUSTEVAL_PAPER_V2_5_3_3.md` | **Current Master Manuscript** | **86,185 bytes** | `207d904b88f3640600aace901e732ed7ecaf8d921564e71ac4bb028654c66e84` |
| `V2_1_CORRECTION_REPORT.md` | Audit Report | 19,654 bytes | `5b22ea4e204798cce3032241ecf8cdda62b39e0a834f138f71aa5ef76865ae00` |
| `PHASE_3C_6_3_FINAL_REPRODUCIBILITY_REPORT.md` | **Phase 3C.6.3 Audit Report** | **19449 bytes** | `[Self-referential; verified upon completion]` |

---

## 4. Deliverable Telemetry & Binary Integrity Verification

### Deliverable Geometry
- **Master Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_3_3.md`  
  - Character Count: 85,349  
  - Line Count: 1,186  
  - Exact Byte Count: 86,185 bytes  
  - Cryptographic SHA-256 Digest: `207d904b88f3640600aace901e732ed7ecaf8d921564e71ac4bb028654c66e84`  
- **Audit Report:** `research/paper/PHASE_3C_6_3_FINAL_REPRODUCIBILITY_REPORT.md`  
  - Line Count: 153  
  - Exact Byte Count: 19449 bytes  
  - Cryptographic SHA-256 Digest: `[Self-referential; verified upon completion]`

### Control Character Integrity Scan
A byte-level verification scan across both deliverables confirmed:
- Non-printing ASCII control bytes ($< 32$, excluding `\t`, `\n`, `\r`): **0** (CLEAN).

---

## 5. Audit Safeguards & Final Declaration

- **Model Forward Passes:** 0 (zero model inference conducted).
- **Prediction Caches:** 0 bytes modified (`results/predictions/` unchanged).
- **Configuration & Protocol:** 0 changes (`configs/experiment.yaml` and `research/PROTOCOL_v1.md` unchanged).
- **Dataset Manifests:** 0 changes (`data/` unchanged).
- **Prompt File on Disk:** 0 changes (`configs/prompts/safety_judge_v1.txt` unchanged).
- **Model Weights & Local Snapshots:** 0 changes (local cache directories unchanged).
- **Submission Readiness Declaration:** In adherence to strict scientific and institutional governance protocols, resolving these internal reporting, provenance, and bibliographical defects establishes internal consistency but does **not** constitute an external declaration of submission readiness.
