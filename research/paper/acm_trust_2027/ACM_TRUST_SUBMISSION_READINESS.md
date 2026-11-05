# ACM TRUST 2027 Venue Retargeting & Submission Readiness Audit (Corrected)
**Target Track:** Symposium 5 — Test and Evaluation, Benchmarking & Assurance  
**Target Venue:** 2027 ACM Conference on Trustworthy and Responsible AI and Computing Systems (ACM TRUST 2027)  
**Location & Dates:** Washington, D.C., USA | March 7–9, 2027 (Hybrid)  
**Project Workspace:** `D:\Research\TrustEval`  
**Dedicated ACM Workspace:** `research/paper/acm_trust_2027/`  
**Date of Audit:** 2026-11-05 (Stage 1 Reconciliation)  

---

## 1. Official Venue Requirements and Deadline Verification

The official author guidelines and call-for-papers have been audited. Critical deadlines are established as follows:

| Milestone | Official Deadline (Pacific Time) | Equivalent India Standard Time (IST) | Notes & Guidelines |
|---|---|---|---|
| **Abstract Registration** | **November 8, 2026, 11:59 PM PT** | **November 9, 2026, 1:29 PM IST** | Mandatory initial registration on Microsoft CMT. *(Note: US Daylight Saving Time ends Nov 1, 2026; Pacific Time is PST = UTC-8; IST is UTC+5:30. Offset is +13.5 hours).* |
| **Full Paper Submission** | **November 15, 2026, 11:59 PM PT** | **November 16, 2026, 1:29 PM IST** | Complete PDF upload on Microsoft CMT. |
| **Notification of Acceptance** | January 15, 2027 | January 16, 2027 | Peer-review decisions announced. |
| **Camera-Ready Deadline** | February 10, 2027 | February 11, 2027 | Final proceedings version. |
| **Conference Dates** | March 7–9, 2027 | March 7–9, 2027 | Washington, D.C., USA (Hybrid). |

*Correction Note:* Deadlines are strictly governed by Pacific Time (PT), **not Anywhere on Earth (AoE)**. 11:59 PM PT corresponds to 1:29 PM IST on the following calendar day.

### Core Formatting Requirements
- **Template:** Official ACM `sigconf` two-column format (`\documentclass[sigconf,review,anonymous]{acmart}`).
- **Page Ceiling:** **Strictly maximum 9 pages for the complete technical paper, including appendices**.
- **Permitted Extra Pages:** References and the mandatory GenAI Usage Disclosure have **unlimited additional pages** and do not count against the 9-page limit.
- **Review Model:** Double-Blind peer review. Author identities, affiliations, and identifying self-citations must be omitted or written in the third person.
- **Track Selection:** **Symposium 5: Test and Evaluation, Benchmarking & Assurance** covers evaluation benchmarks, stress-testing, reproducibility, dataset integrity, and validation/verification pipelines.

---

## 2. Existing Manuscript Density and Word Budget Reconciliation

A line-by-line audit of the completed IEEE source (`research/paper/latex/`) establishes the exact baseline:

### 2.1 Itemized Word and Component Inventory
- **Abstract:** 199 words (0 equations)
- **Section I (Introduction):** 1,432 words (0 equations; Figure 1)
- **Section II (Related Work):** 1,412 words (0 equations; Table I)
- **Section III (Dataset & Ground Truth):** 1,232 words (7 equations)
- **Section IV (Methodology & Setup):** 1,882 words (10 equations; Figure 2)
- **Section V (Results):** 2,861 words (3 equations; Tables II & III; Figures 3 & 4)
- **Section VI (Discussion):** 1,599 words (0 equations)
- **Section VII (Limitations & Ethics):** 948 words (0 equations)
- **Section VIII (Conclusion):** 399 words (0 equations)
- **Main Text Total:** **11,964 words** (20 equations)
- **Appendix A (Annotator Protocol):** 182 words (19 annotator IDs)
- **Appendix B (Escalation Architecture):** 405 words (Figure 6)
- **Appendices Total:** **587 words**
- **Combined Manuscript Words:** **12,551 words**
- **Visuals Footprint:** 5 figures + 3 tables $\approx 3.9$ pages of non-text area.
- **References Footprint:** 31 verified entries $\approx 1.3$ pages (exempt from 9-page limit).

### 2.2 Reconciled Nine-Page Budget & Layout Allocation
In ACM `sigconf`, standard body text formats at approximately $800$ to $850$ words per full text page. Retaining 3 single-column figures and 2 compact tables consumes approximately **$2.0$ pages**. The remaining **$7.0$ pages** accommodate approximately **$5,200$ to $5,500$ words**.

The reconciled allocation plan is structured as follows:

| Section Target | Scope & Content | Visual / Table Assets | Target Words | Est. Pages |
|---|---|---|---|---|
| **Front Matter & Sec. 1** | Title, Abstract, Motivation, RQ1–RQ3, Contributions | Figure 1 (single-col capability trade-off plane) | ~750 words | 1.2 pages |
| **Sec. 2: Related Work** | Dense textual synthesis across 5 pillars (prunes Table I) | None | ~550 words | 0.7 page |
| **Sec. 3: Methodology** | DICES-350, 104 raters, soft targets, prompt, CPU setup | Core mathematical equations | ~1,400 words | 1.8 pages |
| **Sec. 4: Results** | Master evaluation matrix, decile calibration, hypothesis tests, disagreement OLS | Table 1 (perf matrix), Table 2 (paired tests), Figure 2 (rel), Figure 3 (disagree) | ~1,450 words | 3.1 pages |
| **Sec. 5: Discussion** | Ranking/calibration decoupling, disagreement limits, edge auditing, limitations | Textual synthesis | ~1,100 words | 1.7 pages |
| **Sec. 6: Conclusion** | Summary of contributions, candidate correlate, future work | None | ~300 words | 0.5 page |
| **Technical Body Total** | **Strict 9-Page Maximum** | **3 Figures, 2 Tables** | **~5,550 words** | **9.0 pages** |
| *Extra Pages (Unconstrained)* | References (31 verified entries) + GenAI Usage Disclosure | None | ~1,100 words | Pages 10–11 |

*Note on Authoritative Length:* The final rendered PDF page count—not raw word count—is the sole authoritative measure. Layout adjustments (padding, float placement, table spacing) must ensure that Section 6 concludes strictly before or at page 9.0.

---

## 3. Scientific Claim Auditing and Empirical Precision

All claims have been reviewed to enforce strict empirical calibration:

1. **Elimination of Unsupported Novelty Claims:** Removed all phrasing declaring TrustEval the "first rigorous empirical benchmark" or claiming "unprecedented characterization". The study is described as an *exploratory empirical investigation* into sub-2B open-weight safety judges.
2. **Replacement of Causal Terminology:** Replaced occurrences of "proves" or "guarantees" with appropriately qualified language. Specifically:
   - Low disagreement ($\Delta < 0.20$) does *not* "prove" shared failure modes; shared pretraining heuristics are presented as a *plausible explanation* for observed high-error counterexamples.
   - The DICES construct reduction is described as *confirming* logical equivalence, not "proving" infallible ground truth.
3. **Independent Sample Unit Clarification:** Clarified that the $5,200$ ratings reflect **104 repeated-measures crowd evaluations across $N=50$ conversational items**, *not* $5,200$ independent conversational samples. $N=50$ is explicitly maintained as the conversation-level sample size.
4. **SmolLM2 Inductive Behavior:** Described SmolLM2's observed low-score concentration ($\bar{P}=0.2531$, $s=0.0279$) as an empirical low-variance clustering near benchmark prevalence, without speculating on unverified internal causal mechanisms.
5. **AUROC Metric Framing:** Majority-label AUROC ($0.7529$ for Qwen, $0.7517$ for Ensemble, $0.6690$ for SmolLM2) is defined strictly as *majority-consensus discrimination* on the $11$ positive and $39$ negative majority partitions ($429$ evaluation pairs), not direct proof of generalized hazard detection across arbitrary domains.

---

## 4. Figure 1 Technical Verification

Inspection of `make_fig1_tradeoff.py` and the source PDF `fig1_tradeoff.pdf` verifies its actual plotted quantities:
- **Panel (a) Capability Trade-Off Plane:**
  - **X-axis:** Mean Absolute Error (MAE; lower is better), spanning $[0.14, 0.46]$.
  - **Y-axis:** **AUROC (higher is better)**, spanning $[0.62, 0.80]$.
  - *Data Coordinates Plotted:*
    - SmolLM2-1.7B: $\text{MAE} = 0.1734$, $\text{AUROC} = 0.6690$
    - Two-Judge Ensemble: $\text{MAE} = 0.2464$, $\text{AUROC} = 0.7517$
    - Qwen2.5-0.5B: $\text{MAE} = 0.4152$, $\text{AUROC} = 0.7529$
  - *Contextual Reference Note:* Held-out prevalence baseline ($\text{MAE}=0.1983, \text{RMSE}=0.2454, \text{Soft MSE}=0.0602$) documented as a constant prediction excluded from AUROC scatter.
- **Panel (b) Empirical Prediction Distributions (N = 50 conversations):**
  - Four beeswarm vertical strips plotting individual conversation scores with sample means:
    - Human Consensus ($h_{\text{primary}}$): $\mu = 0.3381$
    - Qwen2.5-0.5B: $\mu = 0.7509$
    - SmolLM2-1.7B: $\mu = 0.2531$
    - Two-Judge Ensemble: $\mu = 0.5020$
- *Correction:* In earlier draft text, Panel (a) was mistakenly referenced as "MAE vs. Spearman $\rho$". The actual figure plots **MAE vs. AUROC**. All text, captions, and references must reflect **MAE vs. AUROC**.

---

## 5. Visual Asset Retention and Pruning Plan

To strictly satisfy the 9-page ceiling, visual assets are prioritized as follows:

| Asset | Original Location | ACM TRUST Recommendation | Justification & Footprint |
|---|---|---|---|
| **Figure 1** | Section I | **RETAIN (Figure 1)** | Core single-column teaser visual ($0.45\text{ page}$) plotting MAE vs. AUROC and beeswarm distributions. |
| **Figure 2** | Section IV | **PRUNE** | Full-width architecture schematic ($0.35\text{ page}$). Redundant with mathematical definitions in methodology. |
| **Figure 3** | Section V | **RETAIN (Figure 2)** | Core empirical calibration visual ($0.50\text{ page}$) showing decile reliability curves and bin occupancy. |
| **Figure 4** | Section V | **RETAIN (Figure 3)** | Core RQ3 error correlate visual ($0.45\text{ page}$) showing scatter plot, OLS fit, and regression audit tables. |
| **Figure 6** | Appendix B | **PRUNE** | Full-width conceptual diagram ($0.45\text{ page}$). Uncalibrated conceptual workflow; inappropriate under 9-page limit. |
| **Table I** | Section II | **PRUNE** | Full-width survey matrix ($0.40\text{ page}$). Replaced with dense textual literature synthesis. |
| **Table II** | Section V | **RETAIN (Table 1)** | Full-width master performance matrix ($0.30\text{ page}$) summarizing all 4 systems across 9 metrics. |
| **Table III** | Section V | **RETAIN (Table 2)** | Full-width paired hypothesis testing table ($0.30\text{ page}$) with parametric, Wilcoxon, sign, and bootstrap tests. |
| **Appendix A** | Appendices | **PRUNE** | 19 15-digit annotator IDs summarized in one sentence in Section 3; full listing linked via data repository. |
| **Appendix B** | Appendices | **PRUNE** | Conceptual escalation proposal summarized in one paragraph in Section 5. |

---

## 6. Research Ethics and Human Data Assessment

### 6.1 Secondary Analysis of Public Benchmark Data
- **Dataset Origin:** Google DICES-350 (Diversity in Conversational AI Evaluation for Safety), published by Aroyo et al. (NeurIPS 2023 Datasets & Benchmarks Track) under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
- **Human Participant Context:** Google Research recruited crowd workers via an established supplier to evaluate adversarial user-chatbot dialogues across safety sub-dimensions. The released dataset is public and anonymized.
- **TrustEval Research Scope:** Our investigation constitutes **purely secondary statistical analysis** of released, de-identified public benchmark records.
- **Participant Interaction:** **Zero human subjects were recruited, contacted, compensated, or tracked** by the TrustEval authors.
- **Rater Filtering Context:** The 123 initial annotator pool was reduced to 104 verified raters per item by applying the original dataset authors' pre-specified post-annotation exclusion set (`removed_raters_350`).
- **Institutional Ethics Determination:** No claims of formal Institutional Review Board (IRB) approval or official exemption determinations are fabricated. Authors must confirm with their home institution whether secondary analysis of fully anonymized, publicly licensed benchmark data requires formal institutional documentation prior to camera-ready publication.

---

## 7. Generative AI Usage Disclosure Audit

An accurate inventory of generative AI assistance across the project lifecycle has been conducted:

1. **OpenAI / ChatGPT Assistance:** Used in early exploratory phases for high-level research ideation, initial analysis script scaffolding, exploratory hypothesis framing, and draft review.
2. **Google Antigravity / Gemini Assistance:** Used as an interactive pair-programming environment for executing deterministic data audits, refactoring evaluation scripts (`98_compute_phase3c_stats.py`), generating Matplotlib publication figures, verifying token continuations, and performing LaTeX modularization.
3. **Image-Generation Subagents:** Utilized in Phase 2B to explore visual prototyping and layout concepts for conceptual diagrams (e.g., Figure 6).
4. **Boundary of Machine vs. Human Responsibility:** Generative AI tools served strictly as coding, drafting, and typesetting assistants. All experimental hypotheses, deterministic model evaluations, statistical calculations, and final manuscript claims were directed, reviewed, and validated by the human authors, who bear full academic responsibility.

---

## 8. Publication Cost & Open Access Terms (ACM Open / APC)

ACM operates under a mandatory Open Access publishing model:
1. **ACM Open Institutional Agreements:** If the corresponding author's institution is an active ACM Open subscriber, the Article Processing Charge (APC) is **$0.00** (fully covered).
2. **Geographic Waivers:** Authors affiliated with institutions in countries eligible under EIFL or Research4Life receive an automatic **100% APC waiver**. Authors in World Bank lower-middle-income economies receive an automatic **50% discount**.
3. **Financial Hardship Waivers (FHW):** Authors lacking institutional funding or geographic waivers may apply for a hardship waiver through ACM's eRights system *after* paper acceptance.
4. **Submission Fees:** **Zero fees are due at submission or during review.**

---

## 9. Final Go / No-Go Recommendation

### **VERDICT: GO (SUBMIT TO ACM TRUST 2027)**
TrustEval is scientifically complete, reproducible, and precisely aligned with the assurance and benchmarking objectives of **Symposium 5**. Condensing the manuscript to the strict 9-page ceiling using the 3-figure, 2-table plan preserves all essential scientific findings while eliminating redundant survey matrices and uncalibrated conceptual schematics.
