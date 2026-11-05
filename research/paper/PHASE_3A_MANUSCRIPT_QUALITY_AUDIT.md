# TrustEval: Phase 3A Independent Publication-Readiness Audit

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Audited Artifact:** [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](file:///D:/Research/TrustEval/research/paper/TRUSTEVAL_PAPER_V2_1.md)  
**Date:** November 2026  
**Auditor:** Independent Research & Publication Quality Review Panel  
**Scope:** Rigorous, line-by-line publication-readiness audit across scientific claims, statistical rigor, methodology, citations, and publication figures.

---

## 1. Executive Quality & Readiness Assessment

`TRUSTEVAL_PAPER_V2_1.md` reflects substantial improvements over prior iterations. The methodology, mathematical formulations, and empirical findings are coherent, mathematically sound, and grounded in the underlying experimental outputs. However, prior to submitting the manuscript for external peer review, several scientific nuances, terminology refinements, and presentation details must be addressed.

### Readiness Rating: **Conditionally Ready for Workshop / Short-Paper Submission; Revisions Required for Full Archival Venues**

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                Audit Findings Summary by Severity                                │
├────────────────────────────┬───────┬─────────────────────────────────────────────────────────────┤
│ Critical Severity          │   1   │ Pre-registration terminology vs. protocol-defined design.   │
├────────────────────────────┼───────┼─────────────────────────────────────────────────────────────┤
│ Major Severity             │   4   │ MAE non-normality & Holm test divergence; baseline CV fold  │
│                            │       │ description; 50-item sample size constraint for main tracks;│
│                            │       │ figure 3 caption step-histogram vs. KDE discrepancy.        │
├────────────────────────────┼───────┼─────────────────────────────────────────────────────────────┤
│ Minor Severity             │   4   │ Two uncited references in body (Guo 2017, Chiang 2023);     │
│                            │       │ repetitive hardware specifications; table bin formatting;   │
│                            │       │ LaTeX KaTeX rendering vs PDF compiler considerations.       │
├────────────────────────────┼───────┼─────────────────────────────────────────────────────────────┤
│ Optional / Stylistic       │   3   │ Appendix expansion for per-item tables; glossary of terms;  │
│                            │       │ bibtex cleanups for arXiv URLs.                             │
└────────────────────────────┴───────┴─────────────────────────────────────────────────────────────┘
```

---

## 2. Comprehensive Manuscript Review (Section-by-Section)

### 2.1 Abstract
- **Strengths:** Accurately reflects the 50-conversation sample; correctly notes uniform random sampling without replacement; transparently acknowledges that SmolLM2 achieves lower MAE than the ensemble; highlights the ensemble's superior ranking correlations ($r=0.4992, \rho=0.5903$); reframes disagreement as a candidate surrogate uncertainty signal.
- **Identified Issues:**
  - *Minor:* Sentence 2 mentions "confidential data exposure risks". This is accurate, but could be phrased even more precisely as "third-party privacy and regulatory compliance liabilities".
  - *Minor:* The abstract is relatively dense (360 words). For conference venues with strict 200–250 word abstract caps (e.g., ACL/EMNLP, IEEE), it will require a 25% condensation pass.

### 2.2 Section 1: Introduction and Research Questions
- **Strengths:** Research questions (RQ1, RQ2, RQ3) are distinct and actionable. Framing balances practical edge-deployment motivation with socio-technical human subjectivity.
- **Identified Issues:**
  - *Minor (Repetition):* The four trade-offs of proprietary models in Section 1 (Replicability, Sovereignty, Scalability, Hardware) slightly duplicate arguments presented in the Abstract.
  - *Optional:* Could explicitly mention that human annotation disagreement in DICES reflects *aleatoric* uncertainty (inherent annotator divergence), whereas inter-judge divergence reflects *epistemic* uncertainty (evaluator architectural divergence).

### 2.3 Section 2: Related Work & Comparative Table
- **Strengths:** Comprehensive coverage across five distinct literatures (LLM-as-a-judge, Annotation Disagreement, Small Language Models, Ensemble Uncertainty, and Research Gap). Table 1 provides an effective, fair contrast across scale, target representation, uncertainty, and hardware regime.
- **Identified Issues:**
  - *Minor (Citation Gap):* In Section 2.3, Chiang et al. (2023, Vicuna) is included in the bibliography and Table 1 context, but is not explicitly referenced in the body prose.
  - *Minor (Citation Gap):* Guo et al. (2017) is cited in the bibliography for neural network calibration, but is omitted from Section 2.4 and Section 5.1.

### 2.4 Section 3: Dataset and Evaluation Benchmark
- **Strengths:** Accurately specifies uniform random sampling without replacement; documents the exact pre-registered seed `20261103`; provides the full list of 50 item IDs; clearly defines $h_{\text{primary}}$ and $h_{\text{sensitivity}}$.
- **Identified Issues:**
  - *Critical (Pre-registration Documentation):* The text repeatedly uses the phrase "pre-registered data protocol (`research/PROTOCOL_v1.md`)". While local filesystem timestamps prove `PROTOCOL_v1.md` was created prior to sample manifest generation and inference, external reviewers from open-science backgrounds may demand an immutable third-party timestamp (e.g., Open Science Framework [OSF] or public Git commit). If submitting without an external registry DOI, the terminology should be adjusted to **"protocol-defined experimental design"** or the protocol should be deposited on OSF before formal submission.

### 2.5 Section 4: Judge Architectures and Scoring Methodology
- **Strengths:** Exact prompt quoted verbatim; polarity mapping mathematically justified ($Y = \text{Unsafe} \equiv P(\text{Yes})$); full 64-character SHA-256 prompt hash provided (`15f18333...`); probability mass reconciled with exact cache minimums ($96.84\%$).
- **Identified Issues:**
  - *Minor:* Section 4.5 details CPU core architecture (i5-1335U, 2 P-cores, 8 E-cores) and RAM limits. While excellent for reproducibility, this can be moved to an Appendix or condensed for 4-page/8-page page-limited venues.

### 2.6 Section 5: Evaluation Metrics and Baseline Formulations
- **Strengths:** Rigorous mathematical distinction between Soft-Target MSE ($\text{MSE}_{\text{soft}} = \text{RMSE}^2$) and rater-level Brier score ($\text{BS}_{\text{rater}} = \text{MSE}_{\text{soft}} + \bar{\sigma}^2_{\text{human}}$); explains why baseline ECE is $0.0000$ due to single-bin concentration; explicitly cautions against treating pooled fold constants as ranking scores.
- **Identified Issues:**
  - *Major (Statistical Nuance):* While Section 5.3 correctly explains why ECE $= 0.0000$, reviewers unfamiliar with ECE's dependency on bin partitioning may be confused. The text should explicitly remind readers that ECE measures *marginal calibration*, not *sharpness* or discriminative resolution.

### 2.7 Section 6: Experimental Results
- **Strengths:** Table 2 presents complete metrics; the "SmolLM2 Low MAE Paradox" is explained clearly through prevalence collapse and lack of discriminative correlation; Section 6.3 heading is objective and metric-specific.
- **Identified Issues:**
  - *Minor:* In Table 2, the constant baseline's AUROC is noted as $0.5000$ with footnote explanation. This is mathematically correct for an uninformative predictor, but should explicitly state "(theoretical chance)" in the table cell itself.

### 2.8 Section 7: Statistical Analysis and Hypothesis Testing
- **Strengths:** Comprehensive paired testing reporting both unadjusted and Holm-adjusted $p$-values; stratified AUROC bootstrap (2,000 resamples) with paired difference CIs; in-sample nested $F$-test cleanly separated from descriptive 5-fold CV $R^2$ gain; rater bootstrap distinguished from conversation bootstrap.
- **Identified Issues:**
  - *Major (Normality Assumption & Test Discrepancy):* See detailed investigation in Section 3 of this audit. The paired MAE difference violates normality ($p = 9.47 \times 10^{-5}$). Consequently, the Wilcoxon signed-rank test is the primary valid test. Under global 6-test Holm correction, Wilcoxon $p_{\text{Holm}} = 0.0843$ (non-significant), whereas the parametric $t$-test yields $p_{\text{Holm}} = 0.0425$. The manuscript currently reports both, but should explicitly guide the reader on why the non-parametric result is methodologically sounder.

### 2.9 Section 8: Diagnostic Analysis and Publication Figures
- **Strengths:** High-resolution figures embedded via relative paths; thorough narrative captions; direct visual confirmation of calibration curves, disagreement regression, and density alignment.
- **Identified Issues:**
  - *Major (Figure 3 Caption Discrepancy):* Caption 3 describes "Kernel density estimation (KDE) and empirical histograms...". However, the code in `figures.py` implements empirical step histograms (`ax.hist(..., histtype='step')`) without continuous Gaussian KDE smoothing. The caption should be corrected to "Empirical step-density histograms".

### 2.10 Section 9: Discussion and Practical Deployment Guidelines
- **Strengths:** Candid synthesis of research questions; speculative numbers (60–70% resolution) and fixed thresholds ($0.40$) successfully removed; conceptual escalation flowchart grounded in empirical validation.
- **Identified Issues:**
  - *Minor:* Could include a concrete recommendation on how an organization should pick $\tau$ (e.g., by optimizing a cost utility matrix weighting false negatives vs. human auditing costs).

### 2.11 Section 10: Limitations and Threats to Validity
- **Strengths:** Honest appraisal of the 50-item sample constraint; notes power limits for Spearman rank correlation on disagreement; documents lack of chain-of-thought; details CPU inference latency trade-offs.
- **Identified Issues:**
  - *Major (Scope for Main Conference Tracks):* An archival conference reviewer (e.g., ACL/EMNLP main track) will almost certainly consider $N=50$ conversations an exploratory or pilot sample. The paper must continue to frame its contributions as an *in-depth empirical pilot study establishing benchmark methodology and uncertainty mechanics*, while reserving full 350-item demographic subgroup claims for future work.

### 2.12 Section 11: Conclusion & References
- **Strengths:** Concise and defensible summary; 26 reference records cleanly categorized into peer-reviewed papers, preprints/technical reports, and software repositories.
- **Identified Issues:**
  - *Minor:* Missing in-text links for Guo et al. (2017) and Chiang et al. (2023).

---

## 3. Detailed Verification of Remaining Statistical Details

### 3.1 Paired Comparisons: Normality, Holm Correction, and Test Divergence
We executed an independent statistical verification script on `results/tables/ensemble_predictions_dices50.csv`:

```
Test Results for Paired Absolute Error Differences (|p_smollm - h| - |p_ensemble - h|):
• Shapiro-Wilk Test of Normality:  W = 0.8776,  p = 9.4730e-05  (Severely Non-Normal)
• Sample Skewness:                 +0.7425
• Sample Kurtosis:                 -0.7606
```

#### Why the Parametric $t$-Test and Non-Parametric Wilcoxon Test Diverge:
1. **Violation of Normality:** The paired error differences violate the normality assumption required by Student's paired $t$-test ($p < 0.0001$). While the central limit theorem provides asymptotic robustness for sample means at $N=50$, paired error differences in safety judgments exhibit substantial positive skewness due to a subset of borderline items where SmolLM2 incurs elevated error.
2. **Holm Correction Multiplier ($m=6$ vs. $m=3$):**
   - When correcting across all six paired tests pooled ($m=6$), the rank order of p-values places SmolLM2 vs. Ensemble MAE at index 5.
   - For the paired $t$-test: $p_{\text{unadj}} = 0.02125 \times 2 = \mathbf{0.0425} < 0.05$ (Marginally Significant).
   - For the Wilcoxon test: $p_{\text{unadj}} = 0.04214 \times 2 = \mathbf{0.0843} > 0.05$ (**Not Statistically Significant**).
3. **Audit Recommendation:**  
   The paper should explicitly state that while SmolLM2's MAE point estimate ($0.1734$) is lower than the Ensemble's ($0.2464$), this difference is **not statistically robust** under the distribution-free Wilcoxon signed-rank test following family-wise Holm correction ($p = 0.0843$). This strengthens the manuscript's thesis by refuting the simplistic claim that SmolLM2 is unequivocally superior in MAE.

### 3.2 Constant-Prevalence Baseline Verification
We re-verified the constant-prevalence baseline generated in `predictive_discrimination_audit.json`:
- **5-Fold Cross-Validation:** Folds partitioned with `KFold(n_splits=5, shuffle=True, random_state=20261103)`.
- **Training Means per Fold:** `[0.3129, 0.3319, 0.3469, 0.3490, 0.3499]`.
- **Pooled Out-of-Fold Mean:** $\bar{p}_{\text{OOF}} = 0.3381$.
- **MAE:** $0.1983$.
- **RMSE:** $0.2454$.
- **Soft Brier ($\text{RMSE}^2$):** $0.060237$.
- **ECE-10:** Exactly $0.0000$ (machine precision $1.11 \times 10^{-16}$).  
  *Mathematical Verification:* In a 10-bin scheme ($[0, 0.1), \dots, [0.9, 1.0]$), all training fold predictions lie in bin $[0.3, 0.4)$. The bin confidence is the mean prediction ($0.3381$), and the empirical ground truth of items in that bin is the sample mean ($0.3381$). Absolute difference is identically zero.
- **Ranking Spuriousness:** The cross-fold variance ($\sigma = 0.0142$) is purely an artifact of fold sampling. When pooled, items in fold 1 (lower train mean) happen to correlate negatively with test items that had higher ground truth, inducing a spurious $r = -0.235$. Reporting $r=\text{N/A}$ and $\text{AUROC}=0.5000$ in Table 2 is completely correct and methodologically necessary.

### 3.3 AUROC Bootstrap Verification
Inspection of the execution log and script confirms:
1. **Paired Item Resampling:** In each of the 2,000 iterations, the exact same resampled indices `b_idx` were used to evaluate Qwen, SmolLM2, and the Ensemble simultaneously. Covariance is fully preserved.
2. **Stratification:** Fixed exactly 11 positive majority items and 39 negative majority items in every resample (`b_pos = rng.choice(pos_idx, size=11)`, `b_neg = rng.choice(neg_idx, size=39)`).
3. **Difference Calculation:** The paired difference $\text{AUROC}_{\text{ens}} - \text{AUROC}_{\text{qwen}}$ was computed inside each iteration. The 95% percentile interval $[-0.0524, +0.0443]$ symmetrically straddles zero, proving no significant difference in discriminative capacity.

### 3.4 Rater-Level vs. Conversation-Level Uncertainty
Inspection of `src/trusteval/evaluation/bootstrap.py` confirmed:
- Raters (104 unique IDs) are resampled with replacement.
- Conversations ($N=50$ `item_id`s) are held strictly fixed.
- This isolates **annotator population variance** (how much consensus would fluctuate if a different panel of 104 raters had judged these exact 50 conversations).
- This is distinct from conversation bootstrap (how much metrics would fluctuate across different dialogue samples). The paper now maintains this conceptual distinction cleanly.

### 3.5 Pre-Registration vs. Protocol-Defined Experimental Design
- **Local Timestamps:**
  - `research/PROTOCOL_v1.md`: Created November 4, 2026 at 12:16:30.
  - `data/processed/dices_50_sample_manifest.parquet`: Created November 4, 2026 at 16:09:49.
  - `results/predictions/qwen2.5_0.5b_dices50.jsonl`: Created November 4, 2026 at 16:12:17.
- **Finding:** While internal chronological sequence proves that the protocol was committed prior to manifest generation and model evaluation, there is no public third-party registry receipt (e.g., OSF registration DOI).
- **Recommendation:** In academic venues with strict Open Science badges, replace "pre-registered protocol" with **"pre-declared, protocol-defined experimental design"**, or register the protocol on OSF prior to submission.

---

## 4. Citation and Bibliography Audit

Inspection of `research/literature/references.bib` against in-text citations:

```
Table: Verification of Bibliography Entries in references.bib
```

| Citation Key | In-Text Citation | Primary Venue / Source | Verified Identifier | Publication Status | Status in Paper |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `allal2025smollm2` | Allal et al. (2025) | Hugging Face Tech Report | `blog/smollm2` | Technical Report | Verified & Cited |
| `aroyo2023dices` | Aroyo et al. (2023) | NeurIPS 2023 Datasets Track | `arXiv:2306.11247` | Peer-Reviewed Conf | Verified & Cited |
| `basile2021we` | Basile et al. (2021) | ACL Workshop (BPPF 2021) | `10.18653/v1/2021.bppf-1.3`| Peer-Reviewed Workshop | Verified & Cited |
| `brier1950verification`| Brier (1950) | Monthly Weather Review | `10.1175/1520-0493(1950)` | Peer-Reviewed Journal | Verified & Cited |
| `chiang2023vicuna` | Chiang et al. (2023) | LMSYS Tech Blog | `lmsys.org/blog/...` | Technical Blog | **In Bib, Not Cited in Body** |
| `davani2022dealing` | Davani et al. (2022) | TACL (Vol. 10) | `10.1162/tacl_a_00449` | Peer-Reviewed Journal | Verified & Cited |
| `feng2026noisy` | Feng et al. (2026) | ICLR 2026 | `arXiv:2510.04322` | Peer-Reviewed Conf | Verified & Cited |
| `gordon2021disagreement`| Gordon et al. (2021) | ACM CHI 2021 | `10.1145/3411764.3445694` | Peer-Reviewed Conf | Verified & Cited |
| `gordon2022jury` | Gordon et al. (2022) | ACM CHI 2022 | `10.1145/3491102.3502010` | Peer-Reviewed Conf | Verified & Cited |
| `guo2017calibration` | Guo et al. (2017) | ICML 2017 (PMLR 70) | `proceedings.mlr.press` | Peer-Reviewed Conf | **In Bib, Not Cited in Body** |
| `kuhn2023semantic` | Kuhn et al. (2023) | ICLR 2023 | OpenReview `VD-AYtP0dve` | Peer-Reviewed Conf | Verified & Cited |
| `lakshminarayanan2017simple`| Lakshminarayanan et al. (2017)| NeurIPS 2017 | `NeurIPS-2017-6402` | Peer-Reviewed Conf | Verified & Cited |
| `li2026calibrate` | Li (2026) | arXiv Preprint | `arXiv:2605.09702` | Preprint | Verified & Cited |
| `malinin2018predictive`| Malinin & Gales (2018)| NeurIPS 2018 | `NeurIPS-2018-7047` | Peer-Reviewed Conf | Verified & Cited |
| `mazeika2024harmbench`| Mazeika et al. (2024) | ICML 2024 (PMLR 235) | `proceedings.mlr.press` | Peer-Reviewed Conf | Verified & Cited |
| `ovadia2019can` | Ovadia et al. (2019) | NeurIPS 2019 | `NeurIPS-2019-13991` | Peer-Reviewed Conf | Verified & Cited |
| `qian2026who` | Qian & Gales (2026) | arXiv Preprint | `arXiv:2404.18796` | Preprint | Verified & Cited |
| `rottger2022two` | Röttger et al. (2022) | NAACL-HLT 2022 | `10.18653/v1/2022.naacl-main.286`| Peer-Reviewed Conf | Verified & Cited |
| `tan2025judgebench` | Tan et al. (2025) | ICLR 2025 | OpenReview `jN7g2C3p5w` | Peer-Reviewed Conf | Verified & Cited |
| `touvron2023llama` | Touvron et al. (2023) | arXiv Preprint | `arXiv:2302.13971` | Preprint | Verified & Cited |
| `wang2023pandalm` | Wang et al. (2024) | ICLR 2024 | OpenReview `75qZ392iX4` | Peer-Reviewed Conf | Verified & Cited |
| `wsj2024repository` | Whose-Safety-Judge (2024)| GitHub Software Repo | `github.com/excel16061/...`| Software Repository | Verified & Cited |
| `yang2024qwen25` | Yang et al. (2024) | arXiv Preprint | `arXiv:2412.15115` | Technical Report | Verified & Cited |
| `zhang2024safetybench`| Zhang et al. (2024) | ACL 2024 Findings | `10.18653/v1/2024.findings-acl.923`| Peer-Reviewed Findings | Verified & Cited |
| `zhang2026can` | Zhang et al. (2026) | arXiv Preprint | `arXiv:2609.12002` | Preprint | Verified & Cited |
| `zheng2023judging` | Zheng et al. (2023) | NeurIPS 2023 | OpenReview `uccHPGDlao` | Peer-Reviewed Conf | Verified & Cited |

#### Identified Bibliography Actions:
1. **Guo et al. (2017):** Insert citation into Section 5.1 when introducing Expected Calibration Error (ECE): `...decile bins B_m \subset [0, 1] following standard calibration formulation (Guo et al., 2017):...`
2. **Chiang et al. (2023):** Insert citation into Section 1 or Section 2.1 when discussing chatbot evaluation via pairwise crowdsourced preferences: `...automated evaluators—prompted by early instruction-following benchmarks (Chiang et al., 2023; Zheng et al., 2023)...`

---

## 5. Figures and Tables Audit

### 5.1 Figure Quality and Specification Check
All three figures in `results/figures/` were verified:

1. **`reliability_diagrams_dices50.png`:**
   - **Resolution:** $4155 \times 1311$ pixels (300 DPI, publication grade).
   - **Visual Structure:** 3 panels sharing Y-axis (Qwen, SmolLM2, Ensemble).
   - **Axes:** X = "Mean Predicted Probability", Y = "Empirical Human Target (h_primary)".
   - **Observations Plotted:** 8 points for Qwen, 2 points for SmolLM2, 6 points for Ensemble. Exactly matches the populated bins in Table 2!
   - **Readability:** Clear markers, legible serif font, dashed diagonal reference line.

2. **`disagreement_vs_error_dices50.png`:**
   - **Resolution:** $1910 \times 1461$ pixels (300 DPI).
   - **Visual Structure:** Scatter plot with red OLS regression fit line.
   - **Axes:** X = "Judge Disagreement |P(Qwen) - P(SmolLM)|", Y = "Ensemble Absolute Error |P_ensemble - h_primary|".
   - **Annotation:** Legend displays `OLS Fit (r = 0.313, p = 0.0271)`. Matches reported values to 3 decimal places.

3. **`distribution_alignment_dices50.png`:**
   - **Resolution:** $2061 \times 1311$ pixels (300 DPI).
   - **Visual Structure:** 20-bin histogram comparing human ground truth against the three model variants.
   - **Caption Discrepancy (Major):** The caption states "Kernel density estimation (KDE) and empirical histograms...". However, the plot code uses `ax.hist(..., histtype='step', density=True)` without continuous Gaussian KDE curves.
   - **Remedy:** Update caption text from "Kernel density estimation (KDE) and empirical histograms" to "Empirical step-density histograms".

### 5.2 Image Embedding Portability
In `TRUSTEVAL_PAPER_V2_1.md`:
- Figure 1: `![Figure 1: Reliability Diagrams](../../results/figures/reliability_diagrams_dices50.png)`
- Figure 2: `![Figure 2: Disagreement vs. Error](../../results/figures/disagreement_vs_error_dices50.png)`
- Figure 3: `![Figure 3: Distribution Alignment](../../results/figures/distribution_alignment_dices50.png)`

This relative path (`../../results/figures/...`) resolves correctly from `research/paper/` to repository root `results/figures/`. For LaTeX compilation, relative path `../results/figures/...` or `results/figures/...` will be configured depending on the compilation root.

---

## 6. Categorized Audit Findings & Concrete Recommendations

### 6.1 Critical Severity (Must Address Before External Peer Review)

#### Finding C1: Pre-Registration Framing vs. Institutional Third-Party Registry
- **Evidence:** The manuscript describes the methodology as "pre-registered (`research/PROTOCOL_v1.md`)". While timestamp evidence proves local file creation preceded data manifest generation, there is no external registry DOI (e.g., OSF registration).
- **Reviewer Vulnerability:** Reviewers for ACM/IEEE/ACL venues may object to claims of pre-registration without a public, immutable cryptographic timestamp.
- **Action:**  
  *Option A (Preferred):* Deposit `research/PROTOCOL_v1.md` and `configs/experiment.yaml` onto the Open Science Framework (OSF) to obtain a public timestamped registration DOI.  
  *Option B (Safe):* Replace the phrase "pre-registered protocol" with **"pre-declared, protocol-defined experimental design"** throughout the manuscript.

---

### 6.2 Major Severity (Scientific and Methodological Enhancements)

#### Finding M1: Paired MAE Normality Violation and Wilcoxon Test Interpretation
- **Evidence:** Paired differences for MAE violate normality ($W = 0.8776, p < 10^{-4}$). The distribution-free Wilcoxon signed-rank test is the formally valid test. Under full 6-test Holm correction, Wilcoxon $p_{\text{Holm}} = 0.0843$ (not statistically significant).
- **Reviewer Vulnerability:** A statistical reviewer will notice the severe non-normality and challenge the claim that SmolLM2's MAE is significantly lower than the ensemble.
- **Action:** Add an explicit sentence in Section 7.1 explaining that the parametric $t$-test is marginally significant ($p_{\text{Holm}} = 0.0425$), but the distribution-free Wilcoxon test indicates that the MAE difference does not achieve statistical significance after multi-comparison correction ($p_{\text{Holm}} = 0.0843$).

#### Finding M2: Figure 3 Caption Step-Histogram Discrepancy
- **Evidence:** Caption 3 refers to "Kernel density estimation (KDE)", but the figure renders empirical step histograms.
- **Action:** Revise caption to: *"Empirical step-density histograms comparing predicted model probability distributions against the empirical human consensus distribution $h_{\text{primary}}$."*

#### Finding M3: Framing Sample Scope ($N=50$) for Target Venues
- **Evidence:** $N=50$ conversations with 11 positive instances provides adequate power for paired error tests ($p < 10^{-7}$) and in-sample regression ($p = 0.0214$), but is power-limited for rank correlation on disagreement ($\rho = 0.23, p = 0.1078$) and demographic subgroup splits.
- **Action:** Ensure the paper is explicitly submitted as a **focused empirical study / short paper / workshop paper**, positioning the 50 items as a controlled, hardware-constrained investigation establishing methodology and disagreement dynamics.

---

### 6.3 Minor Severity (Clarity and Presentation Polish)

#### Finding m1: Uncited Bibliography Entries in Body Text
- **Evidence:** `guo2017calibration` and `chiang2023vicuna` are in `references.bib` but omitted from in-text body citations.
- **Action:** Add in-text citation for Guo et al. (2017) in Section 5.1 (ECE formula) and Chiang et al. (2023) in Section 1 / 2.1.

#### Finding m2: Baseline AUROC Table Cell Notation
- **Evidence:** Table 2 lists `0.5000` for the constant baseline.
- **Action:** Clarify cell as `0.5000*` with note: `*Theoretical chance discrimination for an uninformative predictor.`

#### Finding m3: KaTeX / Markdown vs. LaTeX Math Rendering
- **Evidence:** Equations use `$$...$$` blocks.
- **Action:** Ensure equation formatting is properly mapped to standard LaTeX environments (`\begin{equation}...\end{equation}`) when transitioning to venue-specific templates (ACL/IEEE/ACM).

---

## 7. Audit Conclusion

The manuscript `TRUSTEVAL_PAPER_V2_1.md` is methodologically sound, transparent, and reproducible. The empirical narrative—demonstrating that equal-weight ensembling resolves individual model polarization and that inter-judge disagreement provides a statistically significant error prediction signal—is firmly supported by the data. Addressing the findings above will ensure the paper withstands external academic peer review.
