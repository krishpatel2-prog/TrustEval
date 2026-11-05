# TrustEval: Submission Readiness Checklist & Pre-Flight Audit

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\paper`  
**Date:** November 2026  
**Audited Artifact:** `research/paper/TRUSTEVAL_PAPER_V2_1.md`  

---

## 1. Overview and Checklist Structure

This checklist provides an actionable, itemized pre-submission protocol for the TrustEval manuscript. Items are structured across six operational domains and categorized by severity:
- **[CRITICAL]:** Flaws or ambiguities that could trigger immediate desk rejection or severe reviewer skepticism.
- **[MAJOR]:** Methodological or statistical omissions that must be resolved to ensure paper acceptance.
- **[MINOR]:** Formatting, presentation, and citation polishes that elevate review scores.
- **[OPTIONAL]:** Best-practice enhancements for long-term archival visibility.

---

## 2. Itemized Verification Checklist

### 2.1 Scientific Integrity & Target Formulations

| ID | Status | Severity | Check Description | Verification Evidence & Location | Required Pre-Flight Action |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **SCI-1** | PASS | [CRITICAL] | **Prompt Polarity Consistency:** Model $P(\text{Yes})$ strictly matches human unsafe consensus $h_{\text{primary}}$. | Verified in `safety_judge_v1.txt` (line 20): query asks *"Is the response unsafe?"*. $P(\text{Yes}) = P(\text{Unsafe})$. | None. Fully verified. |
| **SCI-2** | PASS | [CRITICAL] | **Soft Target Formulation:** Analytical decomposition between soft MSE and rater Brier score. | Documented in Section 5.1: $\text{BS}_{\text{rater}} = \text{MSE}_{\text{soft}} + \bar{\sigma}^2_{\text{human}}$ ($\bar{\sigma}^2 = 0.1772$). | None. Formula verified. |
| **SCI-3** | PASS | [MAJOR] | **Prevalence Bias Exposure:** Unpacking the SmolLM2 Low MAE Paradox. | Addressed in Section 6.2: shows SmolLM2 predictions collapse into $[0.20, 0.32]$, matched by blind constant baseline ($0.1983$). | None. Rigorously contextualized. |
| **SCI-4** | PASS | [MAJOR] | **Objective Ensemble Claims:** Balanced comparison without overstating superiority. | Section 6.3 heading updated to objective metric comparison; acknowledges SmolLM2 has lower MAE ($p=0.0425$). | Maintain objective framing in venue abstracts. |
| **SCI-5** | PASS | [MAJOR] | **Heuristic Disagreement Framing:** Disagreement framed as surrogate error proxy, not established epistemic uncertainty. | Section 1, 9, and Abstract updated. Speculative 60–70% resolution claims removed. | None. Accurately framed. |
| **SCI-6** | WARN | [CRITICAL] | **Pre-Registration Terminology:** Avoid unverified registry claims. | Internal filesystem timestamps prove protocol preceded manifest/inference, but no third-party registry DOI exists. | **ACTION:** Replace "pre-registered protocol" with **"pre-declared, protocol-defined experimental design"**, or register on OSF. |

---

### 2.2 Statistical Inference & Robustness

| ID | Status | Severity | Check Description | Verification Evidence & Location | Required Pre-Flight Action |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **STAT-1** | PASS | [MAJOR] | **Multiple Comparison Correction:** Holm-Bonferroni correction applied across all paired tests. | Table 3 reports both unadjusted and Holm-adjusted p-values ($m=6$). | None. Verified in `additional_statistical_reporting.json`. |
| **STAT-2** | WARN | [MAJOR] | **MAE Normality & Test Divergence:** Explicitly explain why Wilcoxon test diverges from $t$-test. | Shapiro-Wilk on MAE differences yields $W=0.8776, p < 10^{-4}$. Wilcoxon $p_{\text{Holm}} = 0.0843$ (n.s.); $t$-test $p_{\text{Holm}} = 0.0425$. | **ACTION:** Add brief note in Section 7.1 explaining that the MAE advantage of SmolLM2 is not robust under the non-parametric Wilcoxon test. |
| **STAT-3** | PASS | [MAJOR] | **AUROC Stratified Bootstrap:** Fixed class counts (11 pos, 39 neg) with paired difference CIs. | 2,000 iterations in `task-1576`. Paired difference CI $[-0.0524, +0.0443]$ symmetrically straddles zero. | None. Verified. |
| **STAT-4** | PASS | [MAJOR] | **Rater vs. Item Uncertainty Distinction:** Rater bootstrap holds conversations fixed. | Verified in `bootstrap.py`: item indices are fixed, 104 raters resampled with replacement. | None. Clearly explained in Table 5. |
| **STAT-5** | PASS | [MAJOR] | **Baseline Calibration Reconciliation:** Baseline ECE-10 explained as $0.0000$. | Explained in Section 5.3: all fold predictions fall in decile $[0.3, 0.4)$, matching sample accuracy ($0.3381$). | None. Clarified in text. |
| **STAT-6** | PASS | [MAJOR] | **Baseline Ranking Metric Reconciliation:** Spurious fold-pooled correlations omitted from Table 2. | Table 2 reports baseline AUROC as $0.5000$ (chance); rank correlations omitted. | Add asterisk footnote `*Theoretical chance discrimination`. |
| **STAT-7** | PASS | [MAJOR] | **Nested Regression vs. CV Clarification:** In-sample $F$-test cleanly separated from descriptive CV $R^2$. | Section 7.3 states CV $\Delta R^2_{\text{OOF}} = +0.0805$ is descriptive; $p = 0.0214$ belongs to in-sample $F$-test. | None. Accurately separated. |

---

### 2.3 Codebase, Artifacts & Reproducibility

| ID | Status | Severity | Check Description | Verification Evidence & Location | Required Pre-Flight Action |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **COD-1** | PASS | [CRITICAL] | **Sample Manifest Reproducibility:** Sample item IDs and seed recorded immutably. | `dices_50_sample_manifest.json` & `.parquet` verified (seed `20261103`, uniform random without replacement). | Include manifest in supplementary zip or anonymous repository. |
| **COD-2** | PASS | [CRITICAL] | **Prompt Hash Verification:** Full 64-character SHA-256 prompt hash documented. | Section 4.2 documents `15f18333a682867c36fc600aaa80898b6293f324fcabb240ba95f9279d2685df`. | Verified against `configs/experiment.yaml`. |
| **COD-3** | PASS | [CRITICAL] | **Prediction Cache Integrity:** Append-only JSONL files preserved with zero loss. | `qwen2.5_0.5b_dices50.jsonl` (50 items) & `smollm2_1.7b_dices50.jsonl` (50 items) verified intact. | None. Fully verified. |
| **COD-4** | PASS | [MAJOR] | **Probability Mass Statistics Reconciled:** Model adherence to binary decision space confirmed. | Qwen mean mass $= 0.9938$, SmolLM2 mean mass $= 0.9808$, combined minimum $= 0.9684$. | None. Reconciled in Section 4.3. |
| **COD-5** | PASS | [MAJOR] | **Hardware Resource Bounds Documented:** Peak RSS and sequential execution profile recorded. | Peak RSS $<1.2\text{ GB}$ (Qwen $952\text{ MB}$, SmolLM2 $1189\text{ MB}$); released to $<258\text{ MB}$. | Move micro-specs to appendix if page limits require. |

---

### 2.4 Visualizations, Tables & Citations

| ID | Status | Severity | Check Description | Verification Evidence & Location | Required Pre-Flight Action |
| :---: | :---: | :---: | :--- | :--- | :--- |
| **VIS-1** | PASS | [MAJOR] | **Figure Resolution & Quality:** PNG plots generated at 300 DPI publication standards. | Verified in `results/figures/`: all plots $\ge 1900\text{ px}$ width, 300 DPI, serif font. | Ensure high-res compilation in LaTeX. |
| **VIS-2** | PASS | [MAJOR] | **Figure Embedded Paths Portability:** Relative image links resolve properly. | `../../results/figures/...` verified relative to `research/paper/`. | Verify relative path mapping for target LaTeX build. |
| **VIS-3** | WARN | [MAJOR] | **Figure 3 Caption Precision:** Align caption with step-histogram code implementation. | Caption states "Kernel density estimation (KDE)", but plot code uses `ax.hist(..., histtype='step')`. | **ACTION:** Change caption to: *"Empirical step-density histograms comparing..."*. |
| **BIB-1** | PASS | [MAJOR] | **Bibliography Metadata Accuracy:** Verified identifiers, venues, and publication years. | All 26 entries verified in `references.bib` (Gordon 2021/2022, Allal 2025, Röttger 2022, etc.). | None. BibTeX updated. |
| **BIB-2** | WARN | [MINOR] | **In-Text Citation Coverage:** Ensure every entry in `references.bib` is cited in text. | Guo et al. (2017) and Chiang et al. (2023) exist in BibTeX but missing from body prose. | **ACTION:** Insert in-text citation for Guo (2017) in Section 5.1 and Chiang (2023) in Section 1. |

---

## 3. Venue-Specific Preparation Protocol

When preparing for the primary recommended target (**TrustNLP 2027 at COLING 2027**, Deadline: January 5, 2027) or secondary target (**TMLR**, Rolling):

### Phase A: Anonymization for Double-Blind Review
- [ ] Remove author names, affiliations, and explicit repository paths (`D:\Research\TrustEval`) from manuscript headers.
- [ ] Refer to prior project work in the third person (e.g., "Whose-Safety-Judge (2024) observed that..." rather than "In our earlier work...").
- [ ] Provide an anonymous GitHub repository or supplementary zip containing anonymized prediction caches and analysis scripts.

### Phase B: Format Mapping (Markdown to LaTeX)
- [ ] Use the official `coling2027.sty` / `acl.sty` or `tmlr.sty` LaTeX template.
- [ ] Convert KaTeX equation blocks (`$$...$$`) into standard `\begin{equation} ... \end{equation}` environments.
- [ ] Map Markdown tables (Tables 1–6) to `\begin{table*}[t] ... \end{table*}` with `booktabs` (`\toprule`, `\midrule`, `\bottomrule`).
- [ ] Include high-resolution PNG figures using `\includegraphics[width=\linewidth]{figures/...}`.

### Phase C: Page Budget Management
- **TrustNLP Short Paper Track:** Strictly 4 pages of main content + unlimited pages for references and appendices.
  - *Main Text (4 pages):* Sections 1, 3, 4, 6, 7 (key tables), and 11.
  - *Appendix:* Section 2 (extended literature), Section 4.5 (hardware specs), Section 7.4 (rater bootstrap details), Section 8 (figures), Section 9.2 (escalation flowchart).
- **TMLR Article:** Flexible page limit (typically 8–12 pages). The current full text of V2.1 fits naturally without aggressive condensation.

---

## 4. Concrete Pre-Flight Action Items

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                Immediate Pre-Submission Action Plan                             │
├──────┬──────────┬────────────────────────────────────────────────────────────────────────────────┤
│ Step │ Priority │ Action Item                                                                    │
├──────┼──────────┼────────────────────────────────────────────────────────────────────────────────┤
│  1   │ Critical │ Replace "pre-registered protocol" with "protocol-defined experimental design"  │
│      │          │ in Section 3.2 and Abstract (or deposit protocol on OSF).                      │
├──────┼──────────┼────────────────────────────────────────────────────────────────────────────────┤
│  2   │ Major    │ Update Figure 3 caption in Section 8.3: replace "Kernel density estimation"    │
│      │          │ with "Empirical step-density histograms".                                      │
├──────┼──────────┼────────────────────────────────────────────────────────────────────────────────┤
│  3   │ Major    │ Add sentence to Section 7.1 clarifying that the SmolLM2 MAE advantage is not   │
│      │          │ statistically significant under the non-parametric Wilcoxon test (p = 0.0843). │
├──────┼──────────┼────────────────────────────────────────────────────────────────────────────────┤
│  4   │ Minor    │ Add in-text citation for Guo et al. (2017) in Section 5.1 (ECE formula) and    │
│      │          │ Chiang et al. (2023) in Section 1 (chatbot preference judging).                │
├──────┼──────────┼────────────────────────────────────────────────────────────────────────────────┤
│  5   │ Minor    │ Add asterisk footnote to Table 2: "*Theoretical chance discrimination for      │
│      │          │ an uninformative constant predictor".                                          │
└──────┴──────────┴────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Summary Conclusion

The TrustEval project has successfully navigated from experimental execution to academic maturity. All experimental results are verified, caches are preserved, and findings are defensible. Upon executing the five concise action items above and importing into the target LaTeX style template, the manuscript will be fully prepared for formal peer-reviewed submission.
