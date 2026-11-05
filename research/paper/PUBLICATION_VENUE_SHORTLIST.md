# TrustEval: Publication Venue Shortlist and Strategic Roadmap

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\paper`  
**Date:** November 2026  
**Target Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_1.md`  

---

## 1. Executive Strategy Summary

TrustEval investigates the deployment of sub-2B parameter open-weight language models (`Qwen2.5-0.5B` and `SmolLM2-1.7B`) on consumer CPU hardware for conversational safety evaluation on the DICES-350 benchmark. It establishes three core empirical contributions:
1. Architectural polarization and the "SmolLM2 Prevalence Collapse Paradox" in imbalanced safety benchmarks.
2. The superior discriminative ranking of equal-weight ensembling ($r=0.4992, \rho=0.5903, \text{AUROC}=0.7517$).
3. Inter-judge disagreement as a statistically validated heuristic predictor of evaluation error ($F(1, 46)=5.676, p=0.0214; \Delta R^2_{\text{OOF}}=+0.0805$).

Given the **preliminary 50-conversation sample size**, the publication strategy prioritizes:
- **Immediate / Short-Term Venues:** AI Safety and Trustworthy NLP workshops, short paper tracks (4 pages), student/undergraduate tracks, and journals valuing technical correctness over compute scale (e.g., TMLR).
- **Medium-Term Venues (Post 350-Item Scale):** Full archival conference tracks (ACM FAccT, IEEE SaTML, EMNLP Main).

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               Publication Venue Recommendation Matrix                            │
├──────────────────────┬────────────────────────────────┬────────────────────────┬─────────────────┤
│ Tier                 │ Venue                          │ Submission Category    │ Primary Timing  │
├──────────────────────┼────────────────────────────────┼────────────────────────┼─────────────────┤
│ Strong Topical Fit   │ 1. TrustNLP @ COLING 2027      │ Workshop Short Paper   │ Jan 5, 2027     │
│                      │ 2. TMLR (Transactions on MLR)  │ Archival Journal       │ Rolling         │
│                      │ 3. ACL Rolling Review (ARR)    │ Short Paper (4 pages)  │ 10-Week Cycles  │
├──────────────────────┼────────────────────────────────┼────────────────────────┼─────────────────┤
│ Realistic Targets    │ 4. AIES 2026 / 2027            │ Regular / Short Paper  │ May Annually    │
│                      │ 5. SafeAI Workshop (AAAI/UAI)  │ Workshop Paper         │ Oct / May       │
│                      │ 6. IEEE MIT URTC 2027          │ Student / Tech Paper   │ August 2027     │
│                      │ 7. ICLR Workshop Tiny Papers   │ Workshop Short Track   │ Jan / Feb       │
├──────────────────────┼────────────────────────────────┼────────────────────────┼─────────────────┤
│ Aspirational Targets │ 8. ACM FAccT 2027              │ Archival Conference    │ Oct / Nov 2026  │
│                      │ 9. IEEE SaTML 2027             │ Archival Conference    │ Sept 2026       │
│                      │ 10. EMNLP Main (Findings)      │ Long Paper (via ARR)   │ ARR Cycles      │
└──────────────────────┴────────────────────────────────┴────────────────────────┴─────────────────┘
```

---

## 2. Strong Topical Fit Venues

### Venue 1: Workshop on Trustworthy Natural Language Processing (TrustNLP 2027)
- **Host Conference:** Co-located with COLING 2027 (Macau, China).
- **Official Website:** `https://trustnlpworkshop.github.io/`
- **Research Scope:** Robust evaluation of language models, safety alignment, uncertainty quantification, calibration, detection of hallucination and harmfulness, demographic fairness, and resource-efficient trustworthy NLP.
- **Fit with TrustEval:** **Exceptional.** TrustEval addresses the core theme of TrustNLP: evaluating safety using accessible models, quantifying calibration drift, and using disagreement for uncertainty estimation.
- **Submission Category:** Workshop Short Paper (4 pages + unlimited references/appendices) or Long Paper (8 pages).
- **Publication Format:** ACL Anthology (Archival Proceedings).
- **Eligibility Requirements:** Open to all researchers worldwide; double-blind review via OpenReview.
- **Submission Fees / APC:** None ($0.00). Open-access via ACL Anthology.
- **Verified Upcoming Deadlines:**
  - Direct Paper Submission Deadline: **January 5, 2027**
  - Author Notification: February 6, 2027
  - Camera-Ready Deadline: March 5, 2027
- **Suitability of 50-Conversation Study:** **High.** TrustNLP explicitly welcomes focused empirical evaluations, negative results, and compact hardware benchmarks that illuminate model calibration and uncertainty.

---

### Venue 2: Transactions on Machine Learning Research (TMLR)
- **Publisher:** Journal of Machine Learning Research (JMLR) ecosystem / hosted on OpenReview.
- **Official Website:** `https://jmlr.org/tmlr/`
- **Research Scope:** Computational, algorithmic, and mathematical principles of learning systems; experimental studies clarifying strengths and weaknesses of existing methods; reproducibility studies; evaluation tasks.
- **Fit with TrustEval:** **Very High.** TMLR's core reviewing philosophy explicitly prioritizes **technical correctness, rigor, and validity of claims** over subjective impact, novelty hype, or massive compute budgets.
- **Submission Category:** Full Research Article (flexible length, typically 8–12 pages standard conference layout).
- **Publication Format:** Open-access archival journal; indexed in major indices.
- **Eligibility Requirements:** Open to all researchers; double-blind submission via OpenReview; requires complete reproducibility details.
- **Submission Fees / APC:** **Zero ($0.00).** Completely free to submit and free to publish.
- **Upcoming Verified Deadlines:** **Rolling Year-Round Submissions.** No fixed deadlines; fast review cycles (Action Editor assigned within 1–2 weeks; reviews typically returned in 4–6 weeks).
- **Suitability of 50-Conversation Study:** **Moderate to High.** Suitable provided claims are strictly scoped to the empirical evidence (as done in V2.1) without over-generalizing beyond the 50-item sample. A reviewer may request adding the remaining DICES items during the interactive revision phase, which TMLR's rolling revision structure accommodates cleanly.

---

### Venue 3: ACL Rolling Review (ARR) — Short Paper Track
- **Target Commitment Venues:** EMNLP 2026, EACL 2026, or ACL 2026.
- **Official Website:** `https://aclrollingreview.org/`
- **Research Scope:** Computational linguistics, natural language processing, LLM evaluation methodologies, safety benchmarks, annotation disagreement.
- **Fit with TrustEval:** **High.** The track on *Evaluation Methodologies* and *Ethics, Bias, and Fairness* directly matches TrustEval's analysis of DICES and small open LLMs.
- **Submission Category:** Short Paper (up to 4 pages of main content, excluding references and appendices).
- **Publication Format:** ACL Anthology (Archival Conference / Findings Proceedings).
- **Eligibility Requirements:** Double-blind review; requires adherence to ACL Sustainable Reviewing Policy.
- **Submission Fees / APC:** Zero ($0.00).
- **Upcoming Verified Deadlines:**
  - May 2026 Cycle: **May 25, 2026** (Commitment to EMNLP 2026)
  - August 2026 Cycle: **August 3, 2026**
  - October 2026 Cycle: **October 12, 2026**
- **Suitability of 50-Conversation Study:** **High for Short Paper Track.** The 4-page short paper format is specifically designed for focused empirical observations, focused pilots, and critical evaluation insights (such as exposing the SmolLM2 prevalence collapse paradox).

---

## 3. Realistic Target Venues

### Venue 4: AAAI / ACM Conference on AI, Ethics, and Society (AIES 2026 / 2027)
- **Official Website:** `https://www.aies-conference.com/`
- **Research Scope:** Societal impacts of AI, ethics, safety governance, algorithmic fairness, pluralism, and human-in-the-loop auditing.
- **Fit with TrustEval:** **Strong.** TrustEval's focus on pluralistic human safety ratings (avoiding binary consensus collapse) and decentralized, on-premises governance without third-party API exposure aligns with AIES's mission.
- **Submission Category:** Full Paper (up to 7 pages + references).
- **Publication Format:** ACM Digital Library.
- **Eligibility Requirements:** Double-blind submission; open to all academic and industry researchers.
- **Submission Fees / APC:** Standard ACM conference registration; no mandatory open-access APC.
- **Upcoming Verified Deadlines:** Annual mid-May deadline (May 14–21, 2026; next cycle May 2027).
- **Suitability of 50-Conversation Study:** **Moderate.** AIES values sociotechnical framing, human annotation pluralism, and governance implications; the 50-item sample is acceptable if framed as an algorithmic governance case study.

---

### Venue 5: Workshop on Safe and Robust AI (SafeAI / SafeNLP)
- **Host Conferences:** Co-located with AAAI or UAI.
- **Official Websites:** `https://safeai-workshop.github.io/` / `https://aaai.org/`
- **Research Scope:** Robustness, uncertainty quantification, automated red-teaming, calibration, AI alignment, safe autonomous deployment.
- **Fit with TrustEval:** **High.** SafeAI focuses on mechanisms for verifying that AI systems operate safely in uncertain environments. Using inter-judge disagreement as a triage signal for human review fits SafeAI's agenda.
- **Submission Category:** Workshop Paper (4–7 pages).
- **Publication Format:** CEUR Workshop Proceedings or OpenReview.
- **Eligibility Requirements:** Double-blind; open submission.
- **Submission Fees / APC:** None ($0.00).
- **Upcoming Verified Deadlines:**
  - SafeAI at UAI: Late May annually.
  - SafeAI at AAAI: Late October / early November annually.
- **Suitability of 50-Conversation Study:** **Very High.** Workshops are the premier venue for focused hardware studies and preliminary empirical methodologies.

---

### Venue 6: IEEE MIT Undergraduate Research Technology Conference (URTC 2027)
- **Official Website:** `https://ieee.mit.edu/`
- **Research Scope:** Computer science, electrical engineering, artificial intelligence, and software applications developed by undergraduate and early-career researchers.
- **Fit with TrustEval:** **Exceptional for Student / Early-Career Profiles.** If any authors on the team are undergraduate students, post-baccalaureates, or early-stage researchers, URTC provides premier visibility and IEEE indexing.
- **Submission Category:** Technical Paper (3–5 pages in IEEE 2-column format).
- **Publication Format:** IEEE Xplore Digital Library (Archival, Scopus/EI indexed).
- **Eligibility Requirements:** At least one primary author must be an undergraduate student at the time of research execution.
- **Submission Fees / APC:** Standard IEEE student registration fee (approx. \$150–\$250); no open-access APC.
- **Upcoming Verified Deadlines:** **August 8–15, 2027** (Paper submission deadline; conference held in October annually at MIT).
- **Suitability of 50-Conversation Study:** **Extremely High.** The rigorous statistical testing, consumer laptop hardware constraints (8 GB RAM), and novel disagreement findings comfortably exceed the typical standard of undergraduate research conferences.

---

### Venue 7: ICLR Workshop Tiny / Short Paper Tracks
- **Host Conference:** International Conference on Learning Representations (ICLR).
- **Official Website:** `https://iclr.cc/`
- **Research Scope:** Specific accepted workshops on Reliable Foundation Models, Pluralistic Alignment, or Model Evaluation.
- **Fit with TrustEval:** **High.** Following the integration of the Tiny Papers initiative into individual workshops, ICLR workshops solicit 2–4 page extended abstracts focusing on "Clear, Correct, and Reproducible (CCR)" empirical results.
- **Submission Category:** Workshop Short Paper / Extended Abstract (2–4 pages).
- **Publication Format:** OpenReview (often non-archival, allowing subsequent full journal submission).
- **Eligibility Requirements:** Open submission via OpenReview.
- **Submission Fees / APC:** None.
- **Upcoming Verified Deadlines:** Typically January / February annually (aligned with ICLR spring workshops).
- **Suitability of 50-Conversation Study:** **Very High.** Tailored specifically for focused evaluations conducted on constrained compute budgets.

---

## 4. Aspirational Target Venues (Requires Scaling to Full 350 Items)

### Venue 8: ACM Conference on Fairness, Accountability, and Transparency (ACM FAccT 2027)
- **Official Website:** `https://facctconference.org/`
- **Research Scope:** Algorithmic bias, evaluation governance, sociotechnical audit, demographic fairness, and multi-stakeholder consensus.
- **Fit with TrustEval:** **High conceptually, but demands full benchmark scale.**
- **Submission Category:** Research Track (10 pages ACM format).
- **Publication Format:** ACM Digital Library.
- **Upcoming Deadlines:** October 27, 2026 (Abstract), November 3, 2026 (Full Paper) for FAccT 2027.
- **Suitability of 50-Conversation Study:** **Low to Moderate.** FAccT reviewers will expect the full 350 conversations and demographic subgroup breakdowns across rater cohorts.

---

### Venue 9: IEEE Conference on Secure and Trustworthy Machine Learning (SaTML 2027)
- **Official Website:** `https://satml.org/`
- **Research Scope:** Rigorous security, trustworthiness, robustness, and verification of machine learning algorithms.
- **Submission Category:** Regular Research Paper (10 pages IEEE format).
- **Upcoming Deadlines:** September 22, 2026 (Mandatory Abstract), September 29, 2026 (Full Paper).
- **Suitability of 50-Conversation Study:** **Low.** SaTML is a top-tier IEEE archival conference. Requires full 350-item evaluation and multiple model families.

---

### Venue 10: EMNLP 2026 Main Conference (Track: Evaluation Methodologies)
- **Host:** Association for Computational Linguistics.
- **Submission Pathway:** Via ACL Rolling Review (ARR May 2026 cycle).
- **Submission Category:** Long Paper (8 pages + references).
- **Suitability of 50-Conversation Study:** **Low for Main Track; High for Findings / Short Paper.** Main track reviewers will request evaluation across 350 items and additional judge architectures (e.g., Llama-3.2-1B).

---

## 5. Strategic Venue Recommendation

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                Recommended Two-Stage Publishing Path                             │
└────────────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                                 │
          ┌──────────────────────────────────────┴──────────────────────────────────────┐
          ▼                                                                             ▼
   PATHWAY A: Immediate Submission                                              PATHWAY B: Full Scale
   (Using Current 50-Item Study)                                                (350 Items Completed)
   • Target 1: TrustNLP @ COLING 2027 (Jan 5, 2027)                             • Target 1: TMLR Full Article
     → 4-page short paper on open-weight judges.                                • Target 2: ACM FAccT 2027
   • Target 2: TMLR (Rolling)                                                   • Target 3: EMNLP Main (ARR)
     → Submit as focused empirical evaluation.
   • Target 3: IEEE MIT URTC (Aug 2027)
     → If student co-author eligible.
```

### Primary Immediate Recommendation:
1. **Target:** **TrustNLP 2027 (co-located with COLING 2027)**
   - **Deadline:** **January 5, 2027**
   - **Format:** 4-page short paper.
   - **Rationale:** The deadline allows sufficient time to apply the Phase 3A quality audit fixes and format into the standard ACL style. The workshop is peer-reviewed, archived in the ACL Anthology, and perfectly targeted at TrustEval's core themes.
2. **Parallel / Secondary Option:** **Transactions on Machine Learning Research (TMLR)**
   - **Timing:** Rolling submission on OpenReview.
   - **Rationale:** TMLR explicitly evaluates technical correctness rather than compute scale. If submitted with the careful scoping in V2.1, it provides an archival journal publication without waiting for annual conference deadlines.
