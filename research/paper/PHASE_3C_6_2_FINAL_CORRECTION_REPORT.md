# Phase 3C.6.2 Final Correction and Disambiguation Audit Report

**Project:** TrustEval: Empirical Evaluation of LLM Judges for Conversational Safety  
**Workspace:** `D:\Research\TrustEval`  
**Date:** 2026-11-05  
**Audit Phase:** Phase 3C.6.2 — Final Provenance, Terminology, and Reference Corrections  
**Base Deliverables:**
- Master Manuscript: `research/paper/TRUSTEVAL_PAPER_V2_5_3_1.md` (83,051 bytes, SHA-256: `3c2b74edfaa59665b39441a7701aabfdffd8b0535a4241be819aca9caacd6536`)
- Prior Report: `research/paper/PHASE_3C_6_1_RECONCILIATION_REPORT.md` (15,303 bytes, SHA-256: `27543bd95634abf3de8f8699b9818fea7387d7c70991f56861c00f00735093c0`)

**New Deliverables:**
1. Master Manuscript: `research/paper/TRUSTEVAL_PAPER_V2_5_3_2.md`
2. Correction Report: `research/paper/PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md`

---

## 1. Executive Summary & Audit Objectives

Phase 3C.6.2 was conducted to resolve residual methodological inaccuracies identified during critical re-examination of Phase 3C.6.1 deliverables. Specifically, this audit resolves:
1. **Prompt-Hash Provenance:** Retracts unsupported assertions that the configured hash is a verified digest of historical prompt bytes, and clearly labels it as a configured/recorded label.
2. **APA 7 SmolLM2 Reference:** Formats the SmolLM2 bibliography entry in strict compliance with APA 7th edition rules for $\ge 21$ authors (first 19 authors, ellipsis, final author, no ampersand).
3. **Statistical Terminology Disambiguation:** Rigorously disambiguates within-item binary-rating variance, rating standard deviation, and proportion standard error, retracting the erroneous formula and Section 3.3 attribution in the Phase 3C.6.1 report.
4. **Significance & Inference Wording:** Renames Section 6.2 sub-heading to "Nominally Significant Monotonic Ranking" and clearly separates the in-sample nominal nested OLS $F$-test from descriptive cross-validation out-of-fold performance.
5. **Archival Accounting & Git Reality:** Transparently accounts for the absence of Git version control in the workspace, replacing claims of unverified historical byte identity with measured cryptographic baselines.
6. **Strict Safeguards:** Confirms zero forward inference passes, zero prediction-cache changes, zero configuration/protocol modifications, and declines premature claims of submission readiness.

---

## 2. Prompt-Hash Provenance Corrections

### 2.1 The Two Hashes
- **Current Filesystem SHA-256:** `3d610cf27d316c9caeb41e75fa4874a545aa540684fa67c8b2da3bf19205df9d`  
  Calculated directly on the raw bytes of `configs/prompts/safety_judge_v1.txt` (1,127 bytes, 22 lines).
- **Configured & Recorded Hash Label:** `15f18333a682867c36fc600aaa80898b6293f324fcabb240ba95f9279d2685df`  
  Defined in `configs/experiment.yaml` (line 80) and stamped into all output prediction records (`results/predictions/*.jsonl`).

### 2.2 Execution Runtime Mechanics
Inspection of `scripts/08_run_50_experiment.py` (lines 388–395) confirms that during benchmark execution, the script:
1. Read the prompt template text from `configs/prompts/safety_judge_v1.txt`.
2. Extracted `prompt_hash = prompt_cfg["sha256"]` directly from `configs/experiment.yaml`.
3. Stamped this configuration string directly into output prediction metadata.

The execution script **did not compute a dynamic SHA-256 digest** of the prompt file at runtime.

### 2.3 Retractions & Provenance Status
- **Retraction of Verified Historical Digest Claim:** We retract any claim that `15f18333a682867c...` is a verified SHA-256 hash of historical prompt bytes. It is an administratively configured string label.
- **Retraction of Speculative Formatting Causes:** We retract the assertion that the difference between the two hashes definitely originated from a trailing newline or line-ending shift. Because no historical prompt file exists that independently hashes to `15f18333a682867c...`, historical byte-level prompt provenance remains unverified.
- **Chat Hallucination Status:** The hash `15f18333f07a7261...` was an ungrounded LLM transcription hallucination in conversational audit chat with zero presence in any file.
- **Manuscript Corrections Applied:**
  - Manuscript header (line 15): Updated from `(SHA-256: ...)` to `(Configured Prompt-Hash Label: 15f18333a682867c36fc600aaa80898b6293f324fcabb240ba95f9279d2685df)`.
  - Section 4.2 introductory sentence: Updated to call it a "configured prompt-hash label".
  - Section 4.2 Note: Completely rewritten to explicitly document that historical byte provenance remains unverified and to avoid speculative formatting claims.
  - Zero modifications were made to the current prompt file, configuration, predictions, or experimental protocol.

---

## 3. APA 7 SmolLM2 Reference Formatting

The official preprint record for SmolLM2 ([arXiv:2502.02737](https://arxiv.org/abs/2502.02737)) contains 22 authors. Under APA 7th edition section 9.8 (Works with 21 or more authors):
- List the first 19 authors.
- Insert an ellipsis (`...`).
- Include the final author's name (`Wolf, T.`).
- Do not place an ampersand (`&`) before the final author.

### 3.1 Metadata Documentation (Full 22 Authors)
For complete archival documentation, all 22 official co-authors are recorded in official order:
1. Loubna Ben Allal (`Ben Allal, L.`)
2. Anton Lozhkov (`Lozhkov, A.`)
3. Elie Bakouch (`Bakouch, E.`)
4. Gabriel Martín Blázquez (`Martín Blázquez, G.`)
5. Guilherme Penedo (`Penedo, G.`)
6. Lewis Tunstall (`Tunstall, L.`)
7. Andrés Marafioti (`Marafioti, A.`)
8. Hynek Kydlíček (`Kydlíček, H.`)
9. Agustín Piqueres Lajarín (`Piqueres Lajarín, A.`)
10. Vaibhav Srivastav (`Srivastav, V.`)
11. Joshua Lochner (`Lochner, J.`)
12. Caleb Fahlgren (`Fahlgren, C.`)
13. Xuan-Son Nguyen (`Nguyen, X.-S.`)
14. Clémentine Fourrier (`Fourrier, C.`)
15. Ben Burtenshaw (`Burtenshaw, B.`)
16. Hugo Larcher (`Larcher, H.`)
17. Haojun Zhao (`Zhao, H.`)
18. Cyril Zakka (`Zakka, C.`)
19. Mathieu Morlon (`Morlon, M.`)
20. Colin Raffel (`Raffel, C.`)
21. Leandro von Werra (`von Werra, L.`)
22. Thomas Wolf (`Wolf, T.`)

### 3.2 Corrected APA 7 Bibliography Entry
In `TRUSTEVAL_PAPER_V2_5_3_2.md`, the bibliography entry in References is formatted strictly per APA 7:
> Ben Allal, L., Lozhkov, A., Bakouch, E., Martín Blázquez, G., Penedo, G., Tunstall, L., Marafioti, A., Kydlíček, H., Piqueres Lajarín, A., Srivastav, V., Lochner, J., Fahlgren, C., Nguyen, X.-S., Fourrier, C., Burtenshaw, B., Larcher, H., Zhao, H., Zakka, C., Morlon, M., ... Wolf, T. (2025). SmolLM2: When Smol Goes Big -- Data-Centric Training of a Small Language Model. *arXiv preprint arXiv:2502.02737*. URL: `https://arxiv.org/abs/2502.02737`.

In-text citations retain `Ben Allal et al. (2025)` (Sections 1.1, 2.3, 4.1).

---

## 4. Human Disagreement, Rating Variance, and Standard Error Disambiguation

Section 5 of `PHASE_3C_6_1_RECONCILIATION_REPORT.md` contained a mathematical and conceptual error by presenting $\sqrt{\frac{h_i(1 - h_i)}{K_i}}$ as "human annotator disagreement" and claiming it was analyzed in Section 3.3.

### 4.1 Mathematical Disambiguation
For a conversation item $i$ evaluated by $K_i$ annotators with continuous consensus proportion $h_i \in [0, 1]$:
1. **Within-Item Binary-Rating Variance ($h_i(1 - h_i)$):**
   Under a Bernoulli model of decisive binary ratings $y_{i, j} \in \{0, 1\}$, the population variance of individual ratings on item $i$ is:
   $$\sigma^2_i = h_i(1 - h_i)$$
   Its sample mean across the 50 conversations is $\bar{\sigma}^2_{\text{human}} = \frac{1}{N}\sum_{i=1}^N h_i(1 - h_i) = 0.1772$.
2. **Individual Rating Standard Deviation ($\sqrt{h_i(1 - h_i)}$):**
   The standard deviation of an individual binary decision on item $i$ is $\sigma_i = \sqrt{h_i(1 - h_i)}$.
3. **Binomial Standard Error of the Estimated Proportion ($\sqrt{\frac{h_i(1 - h_i)}{K_i}}$):**
   Under independent binomial sampling, the standard error of the sample mean consensus estimator $\hat{h}_i$ across $K_i$ ratings is $\text{SE}(\hat{h}_i) = \sqrt{\frac{h_i(1 - h_i)}{K_i}}$. This measures estimator sampling uncertainty, **not** rater variance or disagreement.

### 4.2 Retraction of Section 3.3 Attribution & Disambiguation from $\Delta$
- Section 3.3 documents the 50-conversation sample manifest and sampling protocol; it **does not** analyze binomial standard errors.
- Crucially, none of these human-rater variance or sampling statistics represent **inter-judge model disagreement**:
  $$\Delta = |P_{\text{qwen}} - P_{\text{smollm}}|$$
  which is the sole predictor evaluated in RQ3 and Section 7.3 against ensemble absolute error $\epsilon = |P_{\text{ensemble}} - h_{\text{primary}}|$.
- The manuscript's Brier score decomposition in Section 5.1 ($\text{BS}_{\text{rater}} = \text{MSE}_{\text{soft}} + \bar{\sigma}^2_{\text{human}}$) is fully preserved.

---

## 5. Statistical Significance Wording & Inference Disambiguation

### 5.1 Section 6.2 Sub-Heading Correction
The sub-heading in Section 6.2 was corrected:
- *Previous:* `- **Significant Monotonic Ranking:**`
- *Corrected:* `- **Nominally Significant Monotonic Ranking:**`
- Linear correlation $r = 0.2743$ is explicitly described as falling just short of nominal significance ($p = 0.0539$), while Spearman $\rho = 0.3929$ ($p = 0.0048$) is explicitly designated as nominally significant under an unadjusted test.

### 5.2 Nested OLS $F$-Test vs. Out-of-Fold Generalization
To avoid conflating in-sample linear fit with out-of-fold cross-validation performance:
1. **In-Sample $F$-Test ($F(1, 46) = 5.676, p = 0.0214$):**
   Explicitly designated across the Abstract, Section 7.3, Section 9.1, and Section 12 as an **unadjusted nominal test of in-sample incremental linear fit**. It evaluates whether adding $\Delta$ reduces residual sum of squares in-sample after controlling for response length and confidence.
2. **Out-of-Fold Gain ($\Delta R^2_{\text{OOF}} = +0.0805$):**
   Explicitly documented as a **purely descriptive summary metric** on this 50-item sample. The out-of-fold $R^2$ gain was **not** statistically tested for significance.
3. Language asserting proven generalizability or causal error prediction was systematically removed.

---

## 6. Archival Preservation & Git Reality Accounting

### 6.1 Absence of Git Version Control
Inspection of `D:\Research\TrustEval` confirms:
- Exit code 128: `fatal: not a git repository (or any of the parent directories): .git`.
- In the absence of Git commit histories or cryptographic tag baselines from early developmental phases, claiming byte-for-byte historical invariance for earlier drafts solely from file sizes is epistemologically unsound.

### 6.2 Verified Present Artifact Ledger
We distinguish between:
1. **Historical Files Found in Workspace:** Documented as found with their current physical byte sizes and cryptographic SHA-256 digests.
2. **Phase 3C.6.1 to Phase 3C.6.2 Transition:** Verified by immediate pre- and post-generation cryptographic hashing.

| File Name | File Role | Exact Size | Measured SHA-256 Digest |
| :--- | :---: | :---: | :--- |
| `TRUSTEVAL_PAPER_DRAFT.md` | Initial Draft | 17,676 bytes | `519f3261ac013a3eacc5eec52778fb676b2a719988ee1a7d241119b07fcae66c` |
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
| `TRUSTEVAL_PAPER_V2_5_3_2.md` | **Current Master Manuscript** | **82,916 bytes** | `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc` |
| `PHASE_2B_REVISION_REPORT.md` | Report | 13,378 bytes | `70a645d903f170c75f1fe40150f898c17c349f50233a109b78a7143754fffa33` |
| `PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md` | Report | 28,370 bytes | `bcb81b8170b21143882f4a90c689e490efd01d03d1af3b2a058edad984776a7e` |
| `PHASE_3B_CORRECTION_REPORT.md` | Report | 15,820 bytes | `f6db472a6fd81f7d96201da971e342f1e5582f398d0b81e76e7fcb7d98dc3610` |
| `PHASE_3C_1_VERIFICATION_REPORT.md` | Report | 38,748 bytes | `0f66c54bdc19af1b2af43c2f16860763102ab9b04aa41fa86742a0971633db23` |
| `PHASE_3C_2_CORRECTION_REPORT.md` | Report | 19,588 bytes | `119d0f63be023486c00e5cd671e7817cb1e924b6b490c1ad5c5dd0dd1de25d9f` |
| `PHASE_3C_3_FINAL_AUDIT_REPORT.md` | Report | 17,017 bytes | `e261c2d6e26e64c440bf1cf7c2463a0b4c1ff933b8e28979c8a65ca555f5bc92` |
| `PHASE_3C_4_ERRATA_REPORT.md` | Report | 18,629 bytes | `d3d8c4bacdfb52aa12a37c8afdab465d25035b03a52974c44f15aba5e0394856` |
| `PHASE_3C_5_FINAL_AUDIT_REPORT.md` | Report | 17,628 bytes | `da90c3604864a82a18d10832e71f16d0d7599fefc444aa94bdb14baf48dfd019` |
| `PHASE_3C_6_FINAL_AUDIT_REPORT.md` | Report | 18,859 bytes | `140f1e891a9a90d0ea76767c6a187b477a6ee9deb2b5e32194c077e8135a5570` |
| `PHASE_3C_6_1_RECONCILIATION_REPORT.md` | Report | 15,303 bytes | `27543bd95634abf3de8f8699b9818fea7387d7c70991f56861c00f00735093c0` |
| `PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` | **Phase 3C.6.2 Report** | **15513 bytes** | `[Self-referential; documented in execution telemetry]` |

---

## 7. Deliverable Metrics & Binary Integrity Scan

### Deliverable Geometry

| Deliverable Path | Chars | Lines | Exact Bytes | SHA-256 Digest |
| :--- | :---: | :---: | :---: | :--- |
| `research/paper/TRUSTEVAL_PAPER_V2_5_3_2.md` | 82,115 | 1,177 | **82,916** | `5ac78534a71ac19d0344a20c1fa45362316baf33b09b90b4f852fbbb38d314fc` |
| `research/paper/PHASE_3C_6_2_FINAL_CORRECTION_REPORT.md` | 15491 | 202 | **15513** | `[Self-referential; documented in execution telemetry]` |

### Control Character Scan
Byte-level verification scans across both files confirmed:
- Non-printing ASCII control bytes ($< 32$, excluding `\t`, `\n`, `\r`): **0** (CLEAN).

---

## 8. Audit Safeguards & Final Declaration

- **Forward Passes:** 0 (zero model inference conducted).
- **Prediction Caches:** 0 bytes modified (`results/predictions/` unchanged).
- **Configuration & Protocol:** 0 changes (`configs/experiment.yaml` and `research/PROTOCOL_v1.md` unchanged).
- **Dataset Manifests:** 0 changes (`data/` unchanged).
- **Prompt File on Disk:** 0 changes (`configs/prompts/safety_judge_v1.txt` unchanged).
- **Submission Readiness Declaration:** In accordance with rigorous scientific evaluation standards, completing this internal correction pass resolves methodological and documentation defects but does **not** constitute an external declaration of submission readiness.
