# Research Paper Reconnaissance and Visual Design Analysis

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Phase:** Phase 1.2 — Final Blueprint Integrity Check Complete  
**Working Directory:** `D:\Research\TrustEval\research\paper`  
**Document:** `research/paper/REFERENCE_PAPER_ANALYSIS.md`  
**Base Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_3_4.md`  
**Status:** Phase 1.2 — Final Blueprint Integrity Check Complete (Awaiting Authorization for Phase 2)  
**Date:** November 2026  

---

## Executive Summary

Before transitioning TrustEval from our frozen master markdown manuscript (`TRUSTEVAL_PAPER_V2_5_3_4.md`) into a camera-ready, publication-grade academic document, we conducted an empirical reconnaissance of published peer-reviewed research papers, verified preprints, and official academic formatting templates:
- **Peer-Reviewed Conference Papers:** NeurIPS 2023 (Zheng et al.; Aroyo et al.), ICLR 2025 (Tan et al.), ICML 2026 (Schwinn et al.), ACL 2025 (Bavaresco et al.), and IEEE SaTML 2024 (Debenedetti et al.).
- **Supplementary Methodological Preprints:** Verga et al. (arXiv:2404.18796).
- **Official Formatting Baseline:** IEEE Conference LaTeX specification (`IEEEtran.cls` and `IEEEtran_HOWTO.pdf`).

All reference papers were downloaded, verified against official proceeding records, and visually inspected page-by-page. We analyzed their layout geometry, column structures, first-page visual density, teaser graphic usage, diagram conventions, mathematical typography, tabular styling (`booktabs`), and bibliographic mechanics.

Following Phase 1 review feedback, this document incorporates **Phase 1.1 corrections**:
1. Accurately designating paper publication statuses (correcting Verga et al. to an arXiv preprint, removing unverified Oral tags, and adding the ACL 2025 peer-reviewed benchmark by Bavaresco et al.).
2. Recalibrating visual asset narratives (ensuring the Page 1 teaser and Figure 3 accurately reflect empirical trade-offs, exploratory status, and unadjusted nominal statistics rather than universal superiority or validated uncertainty).
3. Qualifying the selective escalation diagram as an optional conceptual workflow with uncalibrated threshold $\tau$.
4. Streamlining the paper structure into an 8-section organization.
5. Establishing a strict prioritization of main-body tables vs. appendix placements.

---

## 1. Reference Paper Sources and Empirical Visual Inspection

Each paper was analyzed across 14 standardized dimensions with exact PDF page citations and verified repository URLs.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  Reconnaissance Paper Roster                                     │
├─────────────────────────┬─────────────────────────┬──────────────────────┬───────────────────────┤
│ Short Identifier        │ Publication Status      │ Format Paradigm      │ Total Verified Pages  │
├─────────────────────────┼─────────────────────────┼──────────────────────┼───────────────────────┤
│ 1. Zheng et al. (2023)  │ NeurIPS 2023 (Main)     │ 1-Column NeurIPS     │ 29 pages (10 core)    │
│ 2. Aroyo et al. (2023)  │ NeurIPS 2023 (D&B Track)│ 1-Column NeurIPS     │ 22 pages (10 core)    │
│ 3. Tan et al. (2025)    │ ICLR 2025 (Conference) │ 1-Column ICLR        │ 27 pages (11 core)    │
│ 4. Bavaresco et al.(2025│ ACL 2025 (Vol. 2)       │ 2-Column ACL         │ 18 pages (5 core)     │
│ 5. Schwinn et al. (2026)│ ICML 2026 (PMLR 306)    │ 2-Column ICML        │ 26 pages (9 core)     │
│ 6. Debenedetti (2024)   │ IEEE SaTML 2024         │ 2-Column IEEEtran    │ 17 pages (13 core)    │
│ [Supp] Verga et al.(2024│ arXiv Preprint (2404)   │ 2-Column Pre-print   │ 17 pages (6 core)     │
└─────────────────────────┴─────────────────────────┴──────────────────────┴───────────────────────┘
```

---

### Reference Paper 1: Zheng et al. (NeurIPS 2023)

1. **Title and Authors:**  
   *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.*  
   Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica (UC Berkeley, UCSD, CMU, Stanford, MBZUAI).
2. **Venue and Year:**  
   Thirty-seventh Conference on Neural Information Processing Systems (NeurIPS 2023), Advances in Neural Information Processing Systems 36, Main Conference Track.
3. **Source URLs:**  
   - Official Proceedings: `https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Conference.html`  
   - Accessible PDF: `https://arxiv.org/pdf/2306.05685.pdf` (Verified size: 1,580,141 bytes).
4. **Total Page Count:**  
   29 pages total: 10 pages main body (Title through Section 7 Conclusion, pp. 1–10); References pp. 10–13; Appendices pp. 14–29.
5. **Number of Columns:**  
   1 column (single-column format standard to NeurIPS LaTeX style `neurips_2023.sty`).
6. **Overall Layout and Typography:**  
   - Page dimensions: US Letter ($8.5 \times 11.0$ inches; $612 \times 792$ pt).  
   - Text block width: 5.5 inches ($396$ pt); side margins: 1.5 inches.  
   - Primary typeface: Times Roman, 10pt with 13pt baseline skip.
7. **Section and Subsection Organization:**  
   Numbered hierarchically with Arabic numerals: `1 Introduction`, `2 MT-Bench and Chatbot Arena`, `3 LLM as a Judge` (`3.1 Evaluation Formats`, `3.2 Benchmarks and Models`, `3.3 Limitations of LLM-as-a-Judge`), `4 Agreement Evaluation`, `5 Mitigations`, `6 Discussion`, `7 Conclusion`.
8. **Abstract and Introduction Presentation (PDF p. 1):**  
   - Centered 14pt bold title followed by an author block with numbered superscripts matching institutional affiliations.
   - Abstract is centered, 10pt, indented by an additional 0.5 inches on both left and right margins, with bold centered heading `Abstract`.
   - Introduction begins immediately below the abstract on Page 1 without a teaser figure.
9. **Number and Types of Figures:**  
   - 41 figures total (4 in main body, 37 in appendix).
   - Figure 1 (PDF p. 2): Multi-turn conversational dialogue cards comparing Assistant A (LLaMA-13B) and Assistant B (Vicuna-13B) with color-tinted background frames, followed by a highlighted GPT-4 judgment card.
   - Figure 2 (PDF p. 8): Scatter and line plots comparing win rate difference against human-judge agreement.
   - Figures 3 & 4 (PDF pp. 7–8): Horizontal stacked bar charts of model win rates under different judges.
10. **Number and Types of Tables:**  
    - 36 tables total (6 in main body).
    - Table 1 (PDF p. 3): Multi-turn sample prompts from MT-Bench.
    - Table 2 (PDF p. 5): Position bias percentage and consistency metrics across judges.
    - Tables 5 & 6 (PDF p. 8): Agreement matrices using percent agreement and Cohen’s $\kappa$ across pairwise and single-answer judges.
    - Strict adherence to `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) with zero vertical grid lines.
11. **Diagram and Architecture Styles:**  
    - High-contrast card callouts for prompt and dialogue serialization. Vector boxes use light gray and light blue fills (`#f0f4f8`) with rounded corners and clean sans-serif mono fonts for input prompts.
12. **Equations and Technical Explanations:**  
    - Numbered display equations for Cohen's $\kappa$ and Bradley-Terry win-rate estimation models.
13. **Citation and Bibliography Formatting:**  
    - Author-year natural citations using `natbib` (e.g., `Chiang et al. (2023)` or `(Zheng et al., 2023)`).
    - 4 pages of references (pp. 10–13), unbulleted, alphabetized by primary author surname with hanging indents.
14. **Overall Visual Quality:**  
    - High readability; whitespace balance; conversational callout blocks make qualitative examples immediately digestible.

---

### Reference Paper 2: Aroyo et al. (NeurIPS 2023 Datasets & Benchmarks Track)

1. **Title and Authors:**  
   *DICES Dataset: Diversity in Conversational AI Evaluation for Safety.*  
   Lora Aroyo, Alex S. Taylor, Mark Díaz, Christopher M. Homan, Alicia Parrish, Greg Serapio-García, Vinodkumar Prabhakaran, Ding Wang (Google Research, City University of London, University of Cambridge).
2. **Venue and Year:**  
   Thirty-seventh Conference on Neural Information Processing Systems (NeurIPS 2023) Track on Datasets and Benchmarks.
3. **Source URLs:**  
   - Official Proceedings: `https://proceedings.neurips.cc/paper_files/paper/2023/hash/a74b697bce4cac6c91896372abaa8863-Abstract-Datasets_and_Benchmarks.html`  
   - Accessible PDF: `https://arxiv.org/pdf/2306.11247.pdf` (Verified size: 606,317 bytes).
4. **Total Page Count:**  
   22 pages total: 10 pages main body (Sections 1–6, pp. 1–10); References pp. 10–13; Appendices & Datasheet pp. 14–22.
5. **Number of Columns:**  
   1 column (NeurIPS Datasets and Benchmarks Track template).
6. **Overall Layout and Typography:**  
   - Page dimensions: US Letter ($8.5 \times 11.0$ inches; $612 \times 792$ pt).  
   - Typography: Times Roman 10pt on 13pt leading; section headers bold 12pt.
7. **Section and Subsection Organization:**  
   `1 Introduction`, `2 Related Work`, `3 Data Collection Methodology` (`3.1 Conversational AI System and Dialogues`, `3.2 Safety Annotation Task and Criteria`, `3.3 Rater Demographics and Recruitment`), `4 DICES Dataset` (`4.1 DICES-350`, `4.2 DICES-990`, `4.3 Quality Checks`), `5 Discussion and Limitations`, `6 Statement of Ethics`.
8. **Abstract and Introduction Presentation (PDF p. 1):**  
   - Abstract focuses on the premise that safety is culturally situated and that forced binary consensus erases marginalized viewpoints.
   - Section 1 concludes with a concise, bolded 4-point bulleted list of dataset contributions.
9. **Number and Types of Figures:**  
   - 10 figures total (5 in main body).
   - Figure 1 (PDF p. 5): Demographic breakdown plots of annotators along race, gender, and age brackets.
   - Figure 2 (PDF p. 6): High-resolution raster screenshot of the crowd annotator web interface showing `Q_overall` and the 5 specific sub-axes.
   - Figure 3 (PDF p. 7): Dual bar charts showing conversational topic distributions and degree of harm distributions.
   - Figure 4 (PDF p. 8): Within-group inter-rater reliability (IRR) and negentropy metrics plotted across demographic groups.
10. **Number and Types of Tables:**  
    - 5 tables total. Table 1 (PDF p. 7): Summary breakdown of item counts, rater counts, ratings per item, and overall label shares across DICES-350 and DICES-990. Table 2 (PDF p. 8): Annotator demographic breakdown across US Census racial categories and gender.
11. **Diagram and Illustration Styles:**  
    - Clean categorical bar charts generated with Python Seaborn using muted, accessible color palettes. Rater interface screenshots are framed with light gray borders to separate UI text from paper prose.
12. **Equations and Technical Explanations:**  
    - Formal mathematical definitions of Inter-Rater Reliability (Krippendorff's $\alpha$), plurality consensus size, and negentropy.
13. **Citation Formatting:**  
    - Author-year APA-style via `natbib`.
14. **Visual Quality & Takeaway for TrustEval:**  
    - Directly relevant as the foundational benchmark evaluated in our research. Demonstrates that rater demographic breakdowns and annotator UI definitions must be clearly grounded and visually documented.

---

### Reference Paper 3: Tan et al. (ICLR 2025)

1. **Title and Authors:**  
   *JudgeBench: A Benchmark for Evaluating LLM-Based Judges.*  
   Sijun Tan, Siyuan Zhuang, Kyle Montgomery, William Y. Tang, Alejandro Cuadron, Chenguang Wang, Raluca Ada Popa, Ion Stoica (UC Berkeley, Washington University in St. Louis).
2. **Venue and Year:**  
   The Thirteenth International Conference on Learning Representations (ICLR 2025), Singapore.
3. **Source URLs:**  
   - Official OpenReview: `https://openreview.net/forum?id=jN7g2C3p5w`  
   - Accessible PDF: `https://arxiv.org/pdf/2410.12784.pdf` (Verified size: 1,079,243 bytes).
4. **Total Page Count:**  
   27 pages total: 11 pages main body (Sections 1–6, pp. 1–11); References pp. 11–13; Appendices pp. 14–27.
5. **Number of Columns:**  
   1 column (ICLR style `iclr2025_conference.sty`).
6. **Overall Layout and Typography:**  
   - US Letter ($8.5 \times 11.0$ inches); Computer Modern / Times Roman font hierarchy.  
   - Section headers styled in bold uppercase small caps (`1 INTRODUCTION`, `2 RELATED WORK`, `3 JUDGEBENCH`).
7. **Section Organization:**  
   `1 Introduction`, `2 Related Work`, `3 JudgeBench` (`3.1 Overview`, `3.2 Data Sourcing`, `3.3 Transformation Pipeline`, `3.4 Quality Control`), `4 Evaluation` (`4.1 Evaluated Judges`, `4.2 Primary Benchmark Results`, `4.3 Capability Breakdown`), `5 Analysis and Discussion`, `6 Conclusion`.
8. **Abstract and Introduction Presentation (PDF p. 1):**  
   - Features bold all-caps header `ABSTRACT` centered above text.
   - Introduction uses bold opening phrases for key paragraphs to guide reader scanning.
9. **Number and Types of Figures:**  
   - 7 figures total.
   - Figure 1 (PDF p. 2): Conceptual architecture diagram contrasting crowdsourced human preference benchmarks against objective correctness verification.
   - Figure 2 (PDF p. 4): Overview diagram of the JudgeBench generation pipeline (Sourcing $\to$ Perturbation $\to$ Verification $\to$ Pairing) using vector boxes with directional arrows and color coding.
   - Figure 3 (PDF p. 9): Benchmark radar charts comparing judge performance across Math, Coding, Logic, and Knowledge.
10. **Number and Types of Tables:**  
    - 16 tables total.
    - Table 1 (PDF p. 7): Master benchmarking matrix reporting overall accuracy, capability breakdowns, and agreement for 20+ judges (GPT-4o, Claude 3.5 Sonnet, Llama-3-70B, Qwen-2.5-72B). Top scores bolded, second-best underlined.
    - Table 2 (PDF p. 7): Evaluating Arena-Hard judge variants across model backbones.
11. **Diagram and Illustration Styles:**  
    - Vector diagrams created in Figma/Illustrator. Clear visual icons represent input questions, LLM evaluators, and validation gates.
12. **Equations and Technical Notation:**  
    - Formal specification of pairwise evaluation accuracy, length-normalized scoring, and position-bias adjustment.
13. **Citation Formatting:**  
    - Author-year in-text citations; extensive bibliography spanning 3 full pages.
14. **Visual Quality & Takeaway for TrustEval:**  
    - Demonstrates how to design a master evaluation table that reports multiple metric dimensions cleanly.

---

### Reference Paper 4: Bavaresco et al. (ACL 2025)

1. **Title and Authors:**  
   *LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks.*  
   Anna Bavaresco, Raffaella Bernardi, Leonardo Bertolazzi, Desmond Elliott, Raquel Fernández, Albert Gatt, Esam Ghaleb, Mario Giulianelli, Michael Hanna, Alexander Koller, André F. T. Martins, Philipp Mondorf, Vera Neplenbroek, Sandro Pezzelle, Barbara Plank, David Schlangen, Alessandro Suglia, Aditya K Surikuchi, Ece Takmaz, Alberto Testoni (University of Amsterdam, University of Trento, University of Copenhagen, Utrecht, MPI, ETH Zürich, Saarland, Lisbon/Unbabel, LMU Munich/MCML, Potsdam, Heriot-Watt, Amsterdam UMC).
2. **Venue and Official Publication Citation:**  
   *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, 2025, pages 238–255.
3. **Source URLs:**  
   - Official ACL Anthology: `https://aclanthology.org/2025.acl-short.20/`  
   - Official DOI: `10.18653/v1/2025.acl-short.20`  
   - Accessible PDF: `https://arxiv.org/pdf/2406.18403.pdf` (Verified size: 821,777 bytes).
4. **Total Page Count:**  
   18 pages total: **5 pages main body** (Title through Section 5 Conclusion, pp. 1–5); References pp. 5–8; Appendices pp. 9–18.
5. **Number of Columns:**  
   **2 columns** (official ACL format `acl.sty`).
6. **Overall Layout and Typography:**  
   - Page dimensions: A4 ($8.27 \times 11.69$ inches; $595.3 \times 841.9$ pt).  
   - Margins: 2.5 cm top/bottom, 2.0 cm left/right.  
   - Column width: 3.03 inches ($218$ pt); inter-column gutter: 0.24 inches ($17$ pt).  
   - Primary typeface: Times Roman 10pt on 11pt baseline skip.
7. **Section Organization:**  
   `1 Introduction`, `2 JUDGE-BENCH: Benchmark Collection`, `3 Experimental Setup`, `4 Results & Analysis` (`4.1 Overall Performance`, `4.2 What Influences Model-Human Alignment?`), `5 Conclusion & Takeaways`.
8. **Abstract and Introduction Presentation (PDF p. 1):**  
   - Full-width title and multi-institution author block across both columns.
   - Abstract confined to the left column of Page 1.
   - Introduction begins immediately on Page 1 below the abstract, cleanly motivating the paper's core research question.
9. **Number and Types of Figures:**  
   - 6 figures total (2 in main body).
   - Figure 1 (PDF p. 3): Comprehensive horizontal boxplot distribution showing correlation ($\rho$) between LLM judge scores and human ratings across 20 evaluation tasks, grouped by model family.
   - Figure 2 (PDF p. 4): Interaction plot showing how model-human correlation shifts as a function of task complexity and human expertise level.
10. **Number and Types of Tables:**  
    - 8 tables total (1 master table in main body, 7 in appendix).
    - Table 1 (PDF p. 2): Master overview of the 20 NLP datasets included in JUDGE-BENCH, detailing domain, linguistic property, rater count, and target metric.
11. **Diagram and Illustration Styles:**  
    - High-density Seaborn boxplots with clearly demarcated baseline markers (chance level, median human agreement).
12. **Equations and Technical Explanations:**  
    - Clear specification of Pearson $r$, Spearman $\rho$, and Kendall $\tau$ rank alignments across continuous and ordinal rater distributions.
13. **Citation Formatting:**  
    - Author-year in-text citations using standard ACL style (`\citep{...}`, `\citet{...}`).
14. **Visual Quality & Key Takeaway for TrustEval:**  
    - **Crucial Peer-Reviewed 2-Column Model.** Bavaresco et al. proves that a highly rigorous empirical evaluation of LLM judges across human datasets can be communicated with exceptional clarity and density within a **5-page main body** in a 2-column format.

---

### Reference Paper 5: Schwinn et al. (ICML 2026)

1. **Title and Authors:**  
   *A Coin Flip for Safety: LLM Judges Fail to Reliably Measure Adversarial Robustness.*  
   Leo Schwinn, Moritz Ladenburger, Tim Beyer, Mehrnaz Mofakhami, Gauthier Gidel, Stephan Günnemann (Technical University of Munich, Mila, Université de Montréal).
2. **Venue and Year:**  
   Forty-third International Conference on Machine Learning (ICML 2026), Vienna, Austria (PMLR Volume 306).
3. **Source URLs:**  
   - Official PMLR Proceedings: `https://proceedings.mlr.press/v306/schwinn26a.html`  
   - Accessible PDF: `https://arxiv.org/pdf/2603.06594.pdf` (Verified size: 1,521,171 bytes).
4. **Total Page Count:**  
   26 pages total: **9 pages main body** (Title through Section 5 Conclusion, pp. 1–9); References pp. 9–11; Appendices pp. 12–26.
5. **Number of Columns:**  
   **2 columns** (standard ICML format `icml2026.sty`).
6. **Overall Layout and Typography:**  
   - US Letter ($8.5 \times 11.0$ inches; $612 \times 792$ pt).  
   - Column width: 3.25 inches ($234$ pt); inter-column gutter: 0.25 inches ($18$ pt).  
   - Primary typeface: Times Roman 10pt with 11.5pt leading.
7. **Section Organization:**  
   `1. Introduction`, `2. Related Work`, `3. Method` (`3.1 Failure Taxonomy`, `3.2 JudgeStressTest (JST)`, `3.3 ReliableBench`), `4. Results` (`4.1 Judge Accuracy on Adversarial Distributions`, `4.2 Leave-One-Out Generalization`, `4.3 Robustness Evaluation Audit`), `5. Conclusion`.
8. **Abstract and Teaser Presentation (PDF p. 1):**  
   - Left column contains abstract and introduction.
   - **Teaser Figure 1 is placed in the upper right column of Page 1!**  
     Figure 1 shows a high-impact bar chart contrasting reported Attack Success Rates (ASR) from standard LLM judges against true human ground truth, visually proving that judges underestimate or overestimate robustness by up to 40 percentage points ("a coin flip").
9. **Number and Types of Figures:**  
   - 41 figures total (5 in main body, 36 in appendix).
   - Figure 1 (PDF p. 1): Teaser bar chart of ASR inflation.
   - Figure 2 (PDF p. 4): Failure breakdown across semantic categories and response lengths.
   - Figure 3 (PDF p. 6): Calibration curves and ECE distributions across judge families.
   - Figure 4 (PDF p. 7): Leave-one-out cross-validation accuracy trajectories.
10. **Number and Types of Tables:**  
    - Table 1 (PDF p. 8): Leave-one-out accuracy evaluation (`Acc@k`) across 7 frontier and open judges.
11. **Diagram Styles:**  
    - Modern color scheme featuring red/salmon for attack failures and slate blue for robust baselines.
12. **Equations and Technical Explanations:**  
    - Explicit formulation of empirical ASR, false positive/negative risk, and leave-one-out accuracy metrics.
13. **Citation Formatting:**  
    - Author-year in-text citations; comprehensive bibliography.
14. **Visual Quality & Key Takeaway for TrustEval:**  
    - Substantively our closest sibling paper in AI safety evaluation failure modes. Demonstrates how to combine calibration diagnostics, reliability diagrams, and failure mode analysis into a high-density, 2-column conference format.

---

### Reference Paper 6: Debenedetti et al. (IEEE SaTML 2024) & Official IEEE Format

1. **Title and Authors:**  
   *Evading Black-box Classifiers Without Breaking Eggs.*  
   Edoardo Debenedetti, Nicholas Carlini, Florian Tramèr (ETH Zurich, Google DeepMind).
2. **Venue and Year:**  
   IEEE Conference on Secure and Trustworthy Machine Learning (IEEE SaTML 2024), Toronto, Canada.
3. **Source URLs:**  
   - Official IEEE / SaTML: `https://satml.org/2024-program/`  
   - Accessible PDF: `https://arxiv.org/pdf/2306.02895.pdf` (Verified size: 1,390,138 bytes).  
   - Formatting Baseline: Official IEEEtran class specification (`IEEEtran_HOWTO.pdf`, CTAN).
4. **Total Page Count:**  
   17 pages total: 13 pages main body (Sections I–VII, pp. 1–13); References pp. 13–15; Appendices pp. 15–17.
5. **Number of Columns:**  
   **2 columns** (official `\documentclass[conference]{IEEEtran}`).
6. **Overall Layout and Typography:**  
   - Page dimensions: US Letter ($8.5 \times 11.0$ inches; $612 \times 792$ pt).  
   - Margins: Top 0.75 in, bottom 1.0 in, side margins 0.625 in.  
   - Column width: 3.5 inches ($252$ pt); inter-column gutter: 0.25 inches ($18$ pt).  
   - Primary typeface: Times Roman 10pt with tight leading.
7. **Section Organization:**  
   Numbered with **Roman numerals** in small caps: `I. INTRODUCTION`, `II. DECISION-BASED ATTACKS`, `III. ASYMMETRIC QUERY COSTS`, `IV. STEALTHY DECISION-BASED ATTACKS`, `V. EVALUATION`, `VI. DEFENSES`, `VII. CONCLUSION`.  
   Subsections are formatted with italicized capital letters: `A. Threat Model`, `B. Evaluation Metrics`.
8. **Abstract and Front Matter Presentation (PDF p. 1):**  
   - Title centered in 18pt or 24pt bold.
   - Author block arranged in multi-column affiliations (`\and`).
   - Abstract begins with bold run-in heading and em-dash: **Abstract**—*Decision-based evasion attacks repeatedly query...*
   - Includes official **Index Terms** block: **Index Terms**—*Security, threat models, black-box adversarial attacks, machine learning.*
   - **Teaser Figure on Page 1:** `Fig. 1: Existing decision-based attacks (left) make many...` placed at the bottom of the right column on Page 1.
9. **Number and Types of Figures:**  
   - 12 figures total.
   - Fig. 1 (PDF p. 1): Conceptual comparison between standard vs. stealthy query trajectories.
   - Fig. 2 (PDF p. 6): Geometric diagram of boundary search trajectories in input space.
   - Figs. 3–6 (PDF pp. 8–10): Multi-panel grid plots showing median adversarial distance as a function of query budget.
10. **Number and Types of Tables:**  
    - Uses Roman numeral centered table headers (`TABLE I`, `TABLE II`) in small caps positioned *above* the table.
11. **Diagram and Architecture Styles:**  
    - High-precision geometric and algorithmic diagrams with vector annotations.
12. **Equations and Technical Explanations:**  
    - Centered display equations numbered consecutively with parenthesized numerals `(1)`, `(2)`.
13. **Citation and Bibliography Formatting:**  
    - **Numerical bracket style:** `[1]`, `[2]–[5]`.
    - Bibliography entries are numbered `[1]`, `[2]` with authors listed by initials and surname, titles in quotation marks or italics, followed by venue and year.
14. **Visual Quality & Key Takeaway for TrustEval:**  
    - Gold standard for formal engineering and computer society venues. Clean, dense, highly structured, and instantly recognizable.

---

### Supplementary Methodological Reference: Verga et al. (arXiv:2404.18796)

- **Title:** *Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models*  
- **Authors:** Pat Verga, Sebastian Hofstätter, Sophia Althammer, Yixuan Su, Aleksandra Piktus, Arkady Arkhangorodsky, Minjie Xu, Naomi White, Patrick Lewis (Cohere).  
- **Publication Status:** **arXiv preprint (arXiv:2404.18796)**. (Accurately corrected; retained as a supplementary methodological reference on multi-model jury aggregation).  
- **Layout & Structure:** 2 columns, A4, 17 pages (6 pages core narrative, pp. 1–6). Demonstrates Page 1 teaser placement and jury pooling formulas.

---

## 2. Updated Comparative Matrix Across Reference Papers

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      Comparative Visual and Structural Matrix                                                    │
├───────────────────┬──────────────┬────────────┬─────────────┬──────────────┬─────────────┬────────────────┬───────────────────┬──────────────────┤
│ Paper             │ Venue/Status │ Columns    │ Core Pages  │ Teaser on P1 │ Figure Type │ Table Style    │ Citation Format   │ Primary Strength │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ Zheng et al.      │ NeurIPS 2023 │ 1 Column   │ 10 pages    │ No           │ Dialogue Box│ booktabs       │ Author-Year       │ Qualitative      │
│ (2023)            │ Main Track   │ (5.5 in)   │             │              │ + Win-rates │ (no verticals) │ (Chiang, 2023)    │ callout boxes    │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ Aroyo et al.      │ NeurIPS D&B  │ 1 Column   │ 10 pages    │ No           │ Demographics│ booktabs       │ Author-Year       │ Demographic & IRR│
│ (2023)            │ 2023         │ (5.5 in)   │             │              │ + UI screen │ (no verticals) │ (Aroyo, 2023)     │ breakdown charts │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ Tan et al.        │ ICLR 2025    │ 1 Column   │ 11 pages    │ No           │ Pipeline +  │ Master Matrix  │ Author-Year       │ Multi-domain     │
│ (2025)            │ Conference   │ (5.5 in)   │             │              │ Radars      │ (multi-column) │ (Tan, 2025)       │ benchmark tables │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ Bavaresco et al.  │ ACL 2025     │ 2 Columns  │ **5 pages** │ No           │ Boxplots +  │ Dataset Matrix │ Author-Year       │ High-density     │
│ (2025)            │ Vol. 2 Short │ (3.03 in)  │             │              │ Interaction │ (booktabs)     │ (Bavaresco, 2025) │ 20-task audit    │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ Schwinn et al.    │ ICML 2026    │ 2 Columns  │ 9 pages     │ **Yes**      │ ASR bar +   │ Leave-One-Out  │ Author-Year       │ Calibration &    │
│ (2026)            │ (PMLR 306)   │ (3.25 in)  │             │ (Top Right)  │ Reliability │ Acc@k          │ (Schwinn, 2026)   │ diagnostic plots │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ Debenedetti et al.│ IEEE SaTML   │ 2 Columns  │ 13 pages    │ **Yes**      │ Geometric   │ Roman Centered │ Numerical [1]     │ Formal IEEEtran  │
│ (2024)            │ 2024         │ (3.5 in)   │             │ (Bottom R)   │ + Trajectory│ (TABLE I)      │ (IEEE Standard)   │ layout rigor     │
├───────────────────┼──────────────┼────────────┼─────────────┼──────────────┼─────────────┼────────────────┼───────────────────┼──────────────────┤
│ [Supp] Verga et al│ arXiv:2404   │ 2 Columns  │ 6 pages     │ **Yes**      │ Rank Shifts │ Compact        │ Author-Year       │ Jury panels &    │
│ (2024)            │ Preprint     │ (3.03 in)  │             │ (Top Right)  │ + Accuracy  │ (Cohen's k)    │ (Verga, 2024)     │ prompt variance  │
└───────────────────┴──────────────┴────────────┴─────────────┴──────────────┴─────────────┴────────────────┴───────────────────┴──────────────────┘
```

---

## 3. Synthesis of Publication Best Practices

From our visual inspection of these top-tier publications, five universal principles guide our production specification:

1. **The Page 1 Teaser as a Structural Conceptual Hook:**  
   In competitive two-column formats (Schwinn et al., Debenedetti et al.), modern papers place a conceptual or empirical figure on Page 1. This must present a balanced, scientifically precise visual summary of the problem and trade-offs rather than claiming universal victory.
2. **Strict Elimination of Vertical Table Lines:**  
   Every top-tier publication across NeurIPS, ICML, ICLR, ACL, and IEEE completely eschews vertical grid lines in tables, using `booktabs` horizontal rules (`\toprule`, `\midrule`, `\bottomrule`) with subtle sub-headers.
3. **Multi-Column Span vs. Single-Column Placement:**  
   In 2-column papers, large master evaluation tables and multi-panel diagnostic plots use the starred float environment (`\begin{table*}` and `\begin{figure*}`) to span both columns cleanly across the top or bottom of a page. Smaller focused plots and correlation tables fit neatly within a single column.
4. **Direct Plot Annotation Over Complex Legends:**  
   Papers with the highest visual clarity (Bavaresco et al., Schwinn et al.) label curves and distributions directly inside the plot canvas rather than forcing the reader's eye to alternate between a distant multi-color legend box and the curves.
5. **Decoupled Main Body and Reproducibility Appendices:**  
   Leading conference papers strictly observe an 8- to 10-page main narrative budget that contains all critical claims, tables, and figures, while placing prompt serializations, hyperparameter listings, and extended diagnostic plots into an unconstrained appendix.

---

## 4. TrustEval Manuscript Analysis & Empirical Source of Truth

We conducted a complete re-read of the frozen TrustEval manuscript (`TRUSTEVAL_PAPER_V2_5_3_4.md`) to establish the exact empirical boundary conditions for publication:

- **Research Core:**
  - **RQ1 (Representation Error):** Sub-2B models approximate continuous safety consensus ($h_{\text{primary}} \in [0, 1]$), but exhibit stark polarization: Qwen2.5-0.5B overpredicts hazard ($\mu = 0.751$ vs. human $0.338$, $\text{ECE-10} = 0.4128$), while SmolLM2-1.7B collapses into a low-variance band near prevalence ($\mu = 0.253, \sigma = 0.028, \text{MAE} = 0.1734$).
  - **RQ2 (Discriminative Ranking vs. Calibration):** Ensembling Qwen and SmolLM2 achieves the highest rank alignment ($r = 0.4992, \rho = 0.5903$), matches Qwen's strong AUROC ($0.7517$ vs. $0.7529$), cuts Qwen's MAE by $40.6\%$ and Soft MSE by $67.6\%$, and expands calibration coverage to 6 bins, while moderating positive prediction bias ($\mu = 0.502$). Crucially, **the ensemble does not achieve universal superiority**: SmolLM2 retains lower MAE ($0.1734$ vs. $0.2464$), and the held-out prevalence baseline retains lower RMSE ($0.2454$) and lower Soft MSE ($0.0602$).
  - **RQ3 (Disagreement as a Candidate Error Correlate):** Inter-judge disagreement ($\Delta = |P_{\text{qwen}} - P_{\text{smollm}}|$) exhibits a nominally significant Pearson correlation with ensemble evaluation error ($r = 0.3125, p = 0.0271$), but its Spearman correlation is not statistically significant ($\rho = 0.2302, p = 0.1078$). In nested OLS modeling controlling for response length and ensemble prediction, adding disagreement accounts for nominally significant incremental in-sample variance ($F(1, 46) = 5.676, p = 0.0214$). 5-fold cross-validation yields a descriptive out-of-fold $\Delta R^2_{\text{OOF}} = +0.0805$ (from $0.0298$ to $0.1103$). This out-of-fold gain is purely descriptive on an exploratory $N=50$ sample.
- **Benchmark Scope:** The 50-conversation sample from DICES-350 ($N=50$ drawn via simple random sampling without replacement with fixed seed `20261103`, not stratified; 104 annotators per item, 5,200 submitted ratings, 4,889 decisive ratings).
- **Hardware Profile:** Consumer x86 laptop CPU, BF16 weights with FP32 logit upcasting, resident memory envelope $<1.2$ GB peak RAM, zero cloud API dependencies.
- **Prior Reference Baseline:** *Whose Safety Does an LLM Judge Reflect?* (Ali, 2026; 1,340 conversations across DICES-350 and DICES-990).

---

## 5. Phase 1.2 — Final Production Blueprint and Implementation Specifications

Following Phase 1.1 design review, this section specifies the finalized, corrected production plan for TrustEval.

### A. Primary Working Publication Format

1. **Document Class Baseline: IEEE Conference Two-Column Format (`IEEEtran.cls`)**
   - **Provisional Primary Working Format:** `\documentclass[conference]{IEEEtran}`.
   - **Rationale:** The IEEE two-column format provides maximum visual structure, high information density, and strict typographical conventions (Times 10pt, 3.5-inch column width, small-caps Roman headings, and numerical bracket citations `[1]`).
   - **Citation & Reference Ordering:** In accordance with official IEEEtran conference standards, citations are numbered consecutively in the order of their first appearance in the text using numerical brackets (`[1]`, `[2]`, `[3]`, ...). The References section is organized strictly in citation order (chronological appearance in text), strictly non-alphabetical.
   - **Venue Adaptability:** We do not promise zero-disruption drop-in conversion to ACL. Any future venue-specific submission (e.g., ACL/EMNLP or TMLR) will be migrated into that venue's official template using dedicated layout scripts rather than forced dual-compilation hacks.
   - **Page Length Target:** **8 to 10 pages for the core narrative** (Sections I through VIII, inclusive of primary figures and tables), followed by References and unconstrained Appendices.

---

### B. Streamlined 8-Section Paper Structure

To avoid unnecessary narrative fragmentation while preserving all technical details from the master manuscript, the paper is organized into eight cohesive sections:

```
Section I: Introduction
  ├── Motivation: API data-leakage / cost vulnerabilities vs. local consumer CPU auditing
  ├── Core Research Questions (RQ1, RQ2, RQ3)
  ├── Explicit Summary of Contributions & Empirical Boundaries (N=50 exploratory draw)
  └── Candidate Teaser Figure 1 (Upper Right Column of Page 1)

Section II: Related Work
  ├── Automated LLM Judges & Robustness Auditing (Zheng, Tan, Schwinn, Bavaresco)
  ├── Human Subjectivity & Annotator Disagreement in Safety (Gordon, Davani, Aroyo)
  ├── Evaluator Ensembles, Juries, and Uncertainty (Lakshminarayanan, Verga, Qian)
  ├── Prior Reference Benchmark: Whose Safety Does an LLM Judge Reflect? (Ali, 2026)
  └── Framework Positioning Matrix [Relocated to Appendix B Table V to preserve main narrative budget]

Section III: Dataset and Methodology
  ├── DICES-350 Adversarial Benchmark & Quality Filtering (104 retained annotators)
  ├── Ground-Truth Continuous Consensus Targets: Primary (h_primary) and Sensitivity (h_sensitivity)
  ├── 50-Conversation Sample Manifest & Statistical Properties (78% safe majority)
  └── Evaluated Sub-2B Judge Architectures: Qwen2.5-0.5B-Instruct vs. SmolLM2-1.7B-Instruct

Section IV: Experimental Setup
  ├── Architectural Diversity Rationale & Prior Baseline Context (Ali, 2026)
  ├── Deterministic Next-Token Logit Scoring & Vocabulary Target Extraction (Yes / No)
  ├── Standardized Prompt Rubric (TrustEval-R0) & Construct Validity Mapping
  ├── Evaluation Metrics: MAE, RMSE, Soft MSE, Soft-Target ECE-10, Pearson r, Spearman rho, AUROC
  ├── Held-Out 5-Fold Cross-Validated Prevalence Baseline Formulation
  └── Consumer Hardware Execution Profile (<1.2 GB peak RSS on CPU, BF16 weights, FP32 logits)

Section V: Results and Comparative Analysis
  ├── Master Evaluation Performance Matrix (Full-Width Table)
  ├── Single Judge Profiles: Qwen Ranking Acuity vs. SmolLM2 Prevalence Anchoring
  ├── Two-Judge Ensemble Performance: Error Reduction, Decile Coverage, and Ranking Concordance
  ├── Nuanced Acknowledgment of Baselines: SmolLM2 lowest MAE, prevalence baseline lowest RMSE/MSE
  ├── Comparative Synthesis with Ali (2026) & Metric Incommensurability Warning (BSS vs. Soft MSE)
  └── Candidate Figure 2: Decile Calibration Curves & Reliability Diagrams

Section VI: Disagreement Analysis (Disagreement as a Candidate Error Correlate)
  ├── Inter-Judge Disagreement (Delta = |P_qwen - P_smollm|) as Candidate Error Correlate
  ├── Correlation Analysis: Pearson r = 0.3125 (nominal p = 0.0271) vs. Spearman rho = 0.2302 (p = 0.1078, n.s.)
  ├── Nested OLS In-Sample Hypothesis Testing (F(1, 46) = 5.676, nominal p = 0.0214)
  ├── Descriptive 5-Fold Out-of-Fold Evaluation (Delta R^2_OOF = +0.0805, purely descriptive)
  └── Candidate Figure 3: Disagreement vs. Absolute Error Scatter with OLS Trendline

Section VII: Discussion, Limitations and Ethical Considerations
  ├── Synthesis of Empirical Findings across RQ1, RQ2, and RQ3
  ├── Optional Candidate Figure 5: Conceptual Selective Human Escalation Architecture (Uncalibrated tau)
  ├── Threats to Validity: N=50 exploratory draw, construct validity, CPU latency, binary token pair scoring
  └── Responsible AI & Ethical Considerations (bias preservation vs. amplification)

Section VIII: Conclusion
  ├── Summary of Findings: Complementary small models, ensembling trade-offs, exploratory disagreement
  └── Future Work: Scaling to complete DICES cohort (N=350), formal epistemic uncertainty modeling

References (IEEE Numerical Bracket Style [1], ordered strictly by first appearance/citation in text, non-alphabetical)

Appendices
  ├── Appendix A: Crowd Annotator Exclusion and Quality Filtering Protocol (Manuscript Protocol Summary)
  ├── Appendix B: Framework Positioning Matrix, Complete TrustEval-R0 Prompt Text & DICES Rubric Mapping
  ├── Appendix C: Paired Error Difference Tests with Multiple Comparison Correction (Table)
  ├── Appendix D: Rater-Cluster Bootstrap Analysis across 104 Crowd Annotators (Table)
  ├── Appendix E: Target Formulation Sensitivity Analysis: Primary vs. Sensitivity Consensus (Table)
  └── Appendix F: Continuous Step-Density Alignment (Candidate Figure 4) & Diagnostic Residuals
```

---

### C. Corrected Visual Asset Specifications

#### 1. Candidate Figure 1: Page 1 Teaser Graphic (Revised Narrative)
- **Title/Caption:** *Fig. 1: Evaluator polarization, ensembling trade-offs, and ranking concordance in sub-2B LLM safety judges on DICES-350 ($N=50$).*  
- **Visual Design:** A three-panel horizontal or two-tier card layout placed in the upper right column of Page 1:
  1. *Qwen2.5-0.5B-Instruct:* Highlights strong discriminative ranking ($\text{AUROC} = 0.7529, \rho = 0.5680$), but illustrates severe positive prediction bias ($\mu = 0.751$ vs. human $0.338$, $\text{MAE} = 0.4152$).
  2. *SmolLM2-1.7B-Instruct:* Highlights lowest observed judge $\text{MAE} = 0.1734$ via extreme score compression ($\mu = 0.253, \sigma = 0.028$, populating 2 deciles).
  3. *Two-Judge Ensemble vs. Prevalence Baseline:* Shows the ensemble achieving highest Pearson ($r = 0.4992$) and Spearman ($\rho = 0.5903$) correlations and reducing Qwen's MAE by $40.6\%$ ($0.4152 \to 0.2464$); explicitly contrasts this with the 5-fold held-out prevalence baseline achieving lower RMSE ($0.2454$) and lower Soft MSE ($0.0602$) than the ensemble ($0.2669$ and $0.0713$).
- **Core Message:** **Communicates complementary evaluator behaviour and a ranking-oriented ensemble trade-off.** Strictly avoids any implication of universal ensemble superiority.

#### 2. Candidate Figure 2: Decile Calibration Curves & Reliability Diagrams
- **Title/Caption:** *Fig. 2: Reliability diagrams showing empirical human unsafe consensus proportion against predicted probability across 10 calibration deciles on the 50-conversation sample from DICES-350 (simple random sample without replacement).*  
- **Mandatory Calibration Note:** Explicitly describe the zero ECE ($0.0000^*$) of the prevalence baseline as degenerate single-bin calibration resulting from prevalence pooling into a single point/bin, not evidence of superior or perfect calibration. Visualizations must not depict or imply that the baseline possesses perfect calibration across the probability continuum.  
- **Source:** Manuscript Section 8.1; verified result matrix.

#### 3. Candidate Figure 3: Disagreement vs. Evaluation Error (Revised & Qualified)
- **Title/Caption:** *Fig. 3: Exploratory analysis of inter-judge disagreement ($\Delta = |P_{\text{qwen}} - P_{\text{smollm}}|$) as candidate error correlate versus absolute ensemble evaluation error across 50 DICES conversations ($N=50$).*  
- **Visual Design:** Scatter plot of the 50 conversations with fitted OLS regression line and shaded $95\%$ confidence ribbon.  
- **Mandatory Reporting in Figure & Caption:**  
  - Explicitly states: Pearson $r = 0.3125$ (unadjusted nominal $p = 0.0271$).  
  - Explicitly states: Spearman $\rho = 0.2302$ (unadjusted $p = 0.1078$, **not statistically significant**).  
  - Explicitly notes: In-sample OLS incremental $F$-test yields $F(1, 46) = 5.676$ (nominal $p = 0.0214$).  
  - Explicitly notes: Out-of-fold cross-validation $\Delta R^2_{\text{OOF}} = +0.0805$ is purely descriptive on this exploratory sample.  
  - **Explicit Methodological Designation:** Strictly designates disagreement as a candidate error correlate, preserving the formal distinction between exploratory bivariate correlation, nested in-sample OLS, and descriptive cross-validation without presenting disagreement as a validated epistemic uncertainty measure.

#### 4. Candidate Figure 4: Continuous Step-Density Distribution Alignment (Appendix / Secondary)
- **Title/Caption:** *Fig. 4: Step-density distributions of predicted probabilities ($P_{\text{unsafe}}$) for Qwen, SmolLM2, and Ensemble against empirical human consensus ($h_{\text{primary}}$).*  
- **Placement:** Recommended for Appendix or Section V depending on page constraints.

#### 5. Candidate Figure 5: Conceptual Selective Escalation Workflow (Revised as Optional Conceptual Application)
- **Title/Caption:** *Fig. 5: Conceptual two-tier selective human escalation workflow for on-premises safety auditing (uncalibrated operational proposal).*  
- **Visual Design:** Vector flowchart showing prompt serialization $\to$ sub-2B logit extraction $\to$ disagreement check ($\Delta < \tau$) $\to$ automated logging vs. human review.  
- **Mandatory Caption & Text Qualifications:**  
  - Explicitly states that this is an **unvalidated conceptual operational proposal**, not an experimentally validated deployment architecture.  
  - Notes that threshold $\tau$ has not been calibrated or empirically validated in this study.  
  - Emphasizes that low disagreement does not guarantee correct evaluation (both models may fail simultaneously).  
  - Explains that institutional deployment requires independent validation on separate hold-out data.

---

### D. Table Prioritization: Main Body vs. Appendix

To prevent cognitive overload and maintain strict conference page budgets, tables are divided into essential main-body tables and appendix tables:

#### Main-Body Tables (Strictly Sequenced in Order of Appearance)
1. **Table I: Prior Benchmark Results from Ali (2026) (Single Column in Section II):**  
   Reports BSS, Spearman $\rho$, and AUROC across Qwen2.5-0.5B, Qwen2.5-1.5B, and SmolLM2-1.7B on DICES-350 and DICES-990 under prompts P0, P1, and P2. Provides essential baseline context. (Source: Manuscript Table 1).
2. **Table II: Master Performance Evaluation Matrix (Full-Width Starred Table `table*` in Section V):**  
   Reports Mean Prediction ($\mu \pm \sigma$), MAE, RMSE, Soft MSE, Soft-Target ECE-10, Populated Deciles, Pearson $r$, Spearman $\rho$, and AUROC across Qwen2.5-0.5B, SmolLM2-1.7B, Two-Judge Ensemble, 5-Fold Held-Out Baseline, and In-Sample Constant Reference. Includes explanatory notes on baseline degenerate single-bin calibration ($0.0000^*$) and held-out prevalence advantage. (Source: Manuscript Table 4).
3. **Table III: Disagreement Predictive Modeling under OLS and 5-Fold Cross-Validation (Single Column in Section VI):**  
   Reports nested OLS coefficients, standard errors, $t$-statistics, nominal $p$-values, incremental $F$-tests, and cross-validated out-of-fold $R^2$ across Model 1 (Length), Model 2 (Length + $P_{\text{ens}}$), and Model 3 (Length + $P_{\text{ens}} + \Delta$). (Source: Manuscript Table 7).

#### Appendix Tables and Narrative Inventories
- **Appendix A: Crowd Annotator Quality Filtering & Exclusion Protocol:** Concise methodological summary of the 19 anomalous crowd annotator exclusions pre-identified by the DICES dataset creators (`removed_raters_350`) based on quality-filter criteria, retaining 104 annotators per item without exposing individual 15-digit identifiers.
- **Table IV (Appendix B): DICES Annotation Axis to TrustEval-R0 Prompt Mapping:** Operational alignment between the 5 crowd questions and the 4 prompt rubric categories. (Source: Manuscript Table 3).
- **Table V (Appendix B): Systematic Framework Positioning Matrix & Methodological Comparison between Ali (2026) and TrustEval:** 7-dimension comparison table with Metric Incommensurability Warning and systematic literature positioning. (Source: Manuscript Table 5).
- **Table VI (Appendix C): Paired Error Differences Between Evaluators:** Parametric $t$-tests, Wilcoxon signed-rank tests, and two-sided sign tests with Holm correction across all 6 pairs. (Source: Manuscript Table 6).
- **Table VII (Appendix D): Rater-Cluster Bootstrap Statistics (104 Raters, 1,000 Resamples):** Standard errors, $95\%$ bootstrap CIs, and paired bootstrap differences. (Source: Manuscript Table 8).
- **Table VIII (Appendix E): Target Consensus Formulation Sensitivity Analysis:** Evaluating primary consensus $h_{\text{primary}}$ vs. smoothed unsure-credit consensus $h_{\text{sensitivity}}$. (Source: Manuscript Table 9).

---

### E. Rigorous Implementation Standards

1. **Direct Data Generation:** All chart curves, calibration bins, regression lines, and confidence ribbons will be generated directly from frozen saved project artifacts (`results/predictions/`, `data/processed/`) via standalone, fully reproducible Python scripts (`matplotlib` / `seaborn`).
2. **Vector Graphic Production:** All figures and diagrams will be compiled to standalone vector PDFs (`.pdf`) using standard vector primitives to ensure crisp typography and zero rasterization artifacts.
3. **Zero Fabricated Content:** No synthetic data points, decorative AI-generated imagery, unsupported annotations, or invented author affiliations will be introduced. Every numerical claim and statistic in the paper will trace directly to the verified master manuscript.

---

## 6. Status and Next Steps

Phase 1.2 — Final Blueprint Integrity Check Complete.

We await your formal authorization of this revised blueprint. Upon receiving your approval, we will proceed to **Phase 2**, creating the modular LaTeX repository, compiling verified vector figures from project data, and generating the camera-ready research paper.

---

## 7. Final Phase 1.2 Verification Summary

This verification summary confirms that all Phase 1.2 integrity corrections have been systematically applied to `REFERENCE_PAPER_ANALYSIS.md`:

1. **Mathematical Text and Syntax Cleanliness:**
   - Exact control characters (ASCII < 32 excluding newline and carriage return): **0**.
   - Unintended tab characters: **0** (all 29 historical tabs resolved into standard LaTeX backslash expressions `\text`, `\toprule`, `\to`, and `\tau`).
   - Broken math fragments / split lines (`\rho`): **0** orphaned fragments (all 9 occurrences restored cleanly).
   - Verified valid LaTeX symbols: `\rho`, `\tau`, `\mu`, `\sigma`, `\Delta`, `\text{...}`, `\toprule`, `\midrule`, `\bottomrule`.

2. **Bibliographic and Reference Metadata:**
   - Bavaresco et al. (ACL 2025): Verified against official ACL Anthology entry (`https://aclanthology.org/2025.acl-short.20/`, DOI `10.18653/v1/2025.acl-short.20`), published in *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)*, 2025, pages 238–255.
   - IEEE Reference Order: Confirmed numerical bracket citations (`[1]`, `[2]`, `[3]`, ...) ordered strictly in the sequential order of their first appearance in the text, explicitly non-alphabetical.

3. **Dataset Terminology:**
   - Legacy shorthand label occurrences in document body: **0** (eliminated all legacy shorthand references). Replaced throughout with `"the 50-conversation sample from DICES-350"`, explicitly documenting simple random sampling without replacement (not stratified) with fixed seed `20261103`.

4. **Crowd Annotator Privacy:**
   - 15-digit annotator IDs: **0** published. Appendix A is specified as a concise methodological summary of the 19 anomalous rater exclusions and quality criteria documented by the original dataset authors.

5. **Table Architecture and Framework Positioning:**
   - Framework Positioning Matrix explicitly relocated to Appendix B (Table V) to strictly preserve the 8–10 page main narrative budget.
   - Main-body tables strictly numbered in sequential text order: Table I (Ali Prior Baseline, Section II), Table II (Master Performance Matrix, Section V), Table III (Disagreement Regression Modeling, Section VI).

6. **RQ3 Disagreement and Calibration Qualifications:**
   - RQ3 strictly designated as `"Disagreement as a Candidate Error Correlate"`, preserving formal statistical distinctions across Pearson $r$, Spearman $\rho$, nested OLS, and descriptive cross-validation without asserting validated uncertainty.
   - Figure 2 explicitly documents the zero ECE ($0.0000^*$) of the prevalence baseline as a degenerate single-bin pooling artifact, prohibiting any visual implication of perfect calibration.
