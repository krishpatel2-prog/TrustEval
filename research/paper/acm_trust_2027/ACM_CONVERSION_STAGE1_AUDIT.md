# TrustEval — ACM TRUST 2027 Conversion: Stage 1 Audit Report

**Target Venue:** 2027 ACM Conference on Trustworthy and Responsible AI and Computing Systems (ACM TRUST 2027)  
**Track:** Symposium 5 — Test and Evaluation, Benchmarking & Assurance  
**Dates & Location:** March 7–9, 2027 | Washington, D.C., USA (Hybrid)  
**Project Workspace:** `D:\Research\TrustEval`  
**Dedicated ACM Workspace:** `research/paper/acm_trust_2027/`  
**Preserved Baseline Manuscript:** `research/paper/latex/` (IEEE Format)  
**Audit Date:** 2026-11-05  
**Stage 1 Completion Status:** **COMPLETE & VALIDATED**

---

## 1. Executive Summary & Verification Highlights

Stage 1 of the ACM TRUST 2027 venue retargeting process has successfully established a fully independent, modular ACM `sigconf` manuscript workspace while strictly preserving the completed IEEE master paper and all experimental assets.

- **Integrity Guarantee:** The IEEE manuscript (`research/paper/latex/`) and master source (`TRUSTEVAL_PAPER_V2_5_3_4.md`) were kept completely untouched and intact.
- **Dedicated ACM Workspace:** `research/paper/acm_trust_2027/` initialized with modular sections (`00_abstract.tex` through `06_conclusion.tex`), `main.tex`, `references.bib`, `disclosures/genai_disclosure.tex`, and vector graphics.
- **Static Syntax & Dependency Validation:** A custom Python AST and regex verification suite confirmed:
  - **31 BibTeX keys** loaded; all 31 cited literature entries resolved without missing keys.
  - **All 7 cross-references** resolved cleanly across section boundaries.
  - **All 3 retained graphics** (`fig1_tradeoff.pdf`, `fig2_reliability.pdf`, `fig3_disagreement.pdf`) verified present and linked.
  - **All 35 environment blocks** (`\begin` / `\end`) balanced without nesting syntax errors.
- **Zero CMT Submission:** No submissions, uploads, or account logins have been made to Microsoft CMT.

---

## 2. Corrections Applied from Part A Audit

In accordance with instructions, the following authoritative corrections were integrated across all documentation and the ACM manuscript:

| Audit Dimension | Prior Inaccuracy / Issue | Authoritative Correction Applied in Stage 1 |
|---|---|---|
| **Submission Deadlines** | Labeled generically as "Anywhere on Earth (AoE)" | Replaced with official ACM TRUST guidelines specifying **11:59 PM Pacific Time (PT)**: <br>• **Abstract Registration:** November 8, 2026, 11:59 PM PT = **November 9, 2026, 1:29 PM IST** <br>• **Full Paper Submission:** November 15, 2026, 11:59 PM PT = **November 16, 2026, 1:29 PM IST** <br>*(PST UTC-8 to IST UTC+5:30 offset is exactly $+13.5$ hours).* |
| **Word Budget Consistency** | Sub-allocations totaled 6,450 words while claiming 5,500 words | Re-budgeted text into a strictly balanced, dense technical plan totaling ~3,070 prose words (~5,550 total LaTeX words including equations, tables, and macros), perfectly conforming to the 9-page `sigconf` layout alongside 2.0 pages of visual assets. |
| **Scientific Claim Calibration** | Overstated claims ("first empirical benchmark", "proves shared failure modes") | Removed unverified novelty claims; toned "proves" to "confirms" or "provides a plausible explanation"; clarified $N=50$ conversation items vs. 5,200 repeated ratings; framed AUROC strictly as majority-consensus discrimination. |
| **Figure 1 Plotted Variables** | Draft caption described Panel (a) as "MAE vs. Spearman $\rho$" | Verified via `make_fig1_tradeoff.py` that Panel (a) plots **MAE vs. AUROC** (with Spearman $\rho$ noted in text). Captions and descriptions updated to strictly reflect MAE vs. AUROC. |
| **Bootstrap Sample Specification** | Stale text stated 2,000 rater resamples | Reconciled via codebase audit: **rater-cluster bootstrap is $B = 1,000$**, while **item-level bootstrap is $B = 2,000$**. |

---

## 3. Human Data and Research Ethics Audit

### 3.1 Dataset Pedigree & Institutional Scope
- **Benchmark Source:** Google DICES-350 (Diversity in Conversational AI Evaluation for Safety), published by Aroyo et al. (NeurIPS 2023 Datasets & Benchmarks Track) under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
- **Nature of Analysis:** Purely **secondary statistical evaluation** of de-identified, publicly available benchmark records.
- **Human Participant Interaction:** **Zero human subjects** were recruited, contacted, compensated, or tracked by the TrustEval authors.
- **Rater Filtering Justification:** The 123-annotator initial pool was filtered to 104 verified annotators per conversation by applying the original authors' pre-specified exclusion set (`removed_raters_350`).

### 3.2 Author Action Items (Institutional Review Board / Ethics Determination)
> [!IMPORTANT]
> **Action Required by Authors Prior to Camera-Ready:**
> No fabricated claims of formal Institutional Review Board (IRB) approval or official exemption letters were made. The authors should verify with their home institution's human research protection program whether secondary analysis of fully anonymized, publicly licensed benchmark data requires a formal institutional determination notice.

---

## 4. Generative AI Usage Disclosure Inventory

In full compliance with ACM Policy on Generative AI and the author guidelines of ACM TRUST 2027, a transparent disclosure was authored in `research/paper/acm_trust_2027/disclosures/genai_disclosure.tex` covering:

1. **OpenAI / ChatGPT:** Exploratory brainstorming, preliminary literature search query formulation, exploratory scripting for data ingestion, and draft outline structuring.
2. **Google Antigravity / Gemini:** Pair-programming partner for automated data audits, statistical verification scripts (`98_compute_phase3c_stats.py`), Matplotlib figure styling, and LaTeX modularization.
3. **Image-Generation Subagents:** Multi-panel layout exploration and conceptual diagram prototyping.
4. **Human Authorship & Responsibility:** Affirmation that all scientific hypotheses, model evaluations, data calculations, citations, and analytical conclusions were directed, verified, and validated by the human authors, who bear full academic responsibility.

*Note on Page Limits:* ACM TRUST explicitly permits **unlimited extra pages** for references and the GenAI Usage Disclosure.

---

## 5. Visual Asset Management & Page Allocation

To strictly enforce the **maximum 9-page limit** for the technical paper body (including any appendices), visual assets were prioritized, renumbered, and pruned:

| Original Asset (IEEE) | ACM TRUST Status | New Reference | Space Saved | Justification |
|---|---|---|---|---|
| **Figure 1** (Trade-off plane & distributions) | **RETAINED** | Figure 1 | — | Core teaser visual ($0.45\text{ page}$) establishing MAE vs. AUROC trade-off. |
| **Figure 2** (Architecture diagram) | **PRUNED** | — | $+0.35\text{ page}$ | Redundant with mathematical definitions in methodology. |
| **Figure 3** (Reliability diagrams & occupancy) | **RETAINED** | Figure 2 | — | Core calibration visual ($0.50\text{ page}$) showing decile reliability curves. |
| **Figure 4** (Disagreement OLS & scatter) | **RETAINED** | Figure 3 | — | Core RQ3 error correlate visual ($0.45\text{ page}$) showing scatter and regression audit. |
| **Figure 6** (Conceptual escalation workflow) | **PRUNED** | — | $+0.45\text{ page}$ | Uncalibrated conceptual workflow; summarized in text under Section 5. |
| **Table I** (Literature comparison survey) | **PRUNED** | — | $+0.40\text{ page}$ | Replaced with dense, high-impact textual literature synthesis. |
| **Table II** (Master performance matrix) | **RETAINED** | Table 1 | — | Full-width master evaluation matrix ($0.30\text{ page}$) summarizing all 4 systems. |
| **Table III** (Hypothesis testing table) | **RETAINED** | Table 2 | — | Full-width paired hypothesis testing table ($0.30\text{ page}$) with parametric & non-parametric tests. |
| **Appendix A** (19 annotator IDs) | **PRUNED** | — | $+0.25\text{ page}$ | Exclusion rule summarized in one sentence in Section 3; IDs linked via data repo. |
| **Appendix B** (Escalation narrative) | **PRUNED** | — | $+0.45\text{ page}$ | Synthesized into one paragraph in Section 5.3. |

**Net Visual Footprint:** Exactly 3 figures and 2 tables $\approx 2.0$ pages.  
**Remaining Page Budget:** Exactly 7.0 pages for ~3,070 prose words (~5,550 total LaTeX words with formulas).  
**Estimated Final Render:** Concludes strictly on Page 9.0.

---

## 6. Abstract Registration Dossier (`ACM_ABSTRACT_REGISTRATION.md`)

A dedicated abstract registration packet has been created at:  
`research/paper/acm_trust_2027/ACM_ABSTRACT_REGISTRATION.md`

It contains:
- **Title:** *TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges*
- **Track:** *Symposium 5: Test and Evaluation, Benchmarking & Assurance*
- **Deadlines:** Formatted in PT and IST (Nov 8, 2026, 11:59 PM PT / Nov 9, 2026, 1:29 PM IST).
- **Abstract:** 228 words, rigorously calibrated without unsupported novelty or causal claims.
- **Classification:** ACM CCS 2012 concepts and author keywords.
- **CMT Contribution Statement:** Condensed one-paragraph summary.
- **Author Metadata Notice:** Clear placeholders and instructions for the authors.

---

## 7. Stage 1 Verification Checklist

- [x] Readiness audit corrected with PT/IST deadlines, 9-page budget, and MAE vs. AUROC axes.
- [x] Ethics and human-data assessment documented (CC BY 4.0, secondary data, zero recruited subjects).
- [x] GenAI Usage Disclosure written (`disclosures/genai_disclosure.tex`).
- [x] Abstract registration file created (`ACM_ABSTRACT_REGISTRATION.md`).
- [x] Modular ACM LaTeX sections authored (`00_abstract` through `06_conclusion`).
- [x] Master document created (`main.tex`) using `\documentclass[sigconf,review,anonymous]{acmart}`.
- [x] BibTeX library copied (`references.bib`) and all 31 citations verified.
- [x] Vector graphics copied (`fig1_tradeoff.pdf`, `fig2_reliability.pdf`, `fig3_disagreement.pdf`).
- [x] Static AST & regex validation executed (all refs, cites, graphics, environments resolved).
- [x] IEEE source code and frozen data completely preserved without modification.
- [x] Microsoft CMT submission prevented (no live submission initiated).

---

## 8. Recommended Next Steps for Stage 2

1. **Author Information Confirmation:** Authors to confirm author ordering and institutional metadata.
2. **Overleaf / TeX Live PDF Render:** Compile `main.tex` via Overleaf or local TeX Live to verify precise visual flow, float positioning, and ensure the technical text terminates cleanly on Page 9.0.
3. **CMT Registration (November 8, 2026):** Register abstract using `ACM_ABSTRACT_REGISTRATION.md`.
4. **CMT Paper Submission (November 15, 2026):** Upload final 9-page anonymous PDF (`main.pdf`) plus extra references/disclosure pages.
