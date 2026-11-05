# TrustEval — Research Figure Strategy & Visual Design Blueprint

## Executive Overview

This document establishes the authoritative, literature-grounded visual communication strategy for the TrustEval academic manuscript (*TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges*). Drawing upon empirical visual reconnaissance of published papers in top-tier machine learning and AI safety venues (NeurIPS, ICML, ICLR, ACL, IEEE SaTML), this blueprint structures a **hypothesis-driven visual pipeline** where every figure serves as direct evidence for a core research question (RQ1: Representation Error; RQ2: Discriminative Ranking vs. Calibration; RQ3: Disagreement as an Error Correlate; and Methodological Construct Validity).

Following the Phase 2B.1 scientific audit, this revised blueprint resolves key methodological, distributional, and architectural requirements:
1. **Trade-Off Frontier Refinement (Figure 1):** The held-out prevalence baseline is removed from the AUROC-vs-MAE plane due to non-interpretable ranking mechanics under constant prediction; baseline error is communicated via separate contextual reference lines/notes. The ensemble is presented as an observed empirical compromise rather than an objectively optimal solver. The lower distribution panel replaces smoothed violin curves with data-faithful raw observation strips/empirical CDFs, reflecting Qwen's actual skewed distribution (28/50 items in $[0.8, 1.0]$, not bimodal).
2. **Evaluation Architecture & Construct Validity (Figure 2):** Formulates the complete data pipeline from DICES-350 ($N=350$) through a fixed-seed simple random sample ($N=50$, seed `20261103`) splitting into two parallel paths: (a) Human reference path with 104 retained raters per item evaluating overall safety ($Q_{\text{overall}}$, synthesizing 5 safety sub-axes) aggregated into continuous $h_{\text{primary}}$, and (b) Judge path executing zero-shot ChatML prompts (`TrustEval-R0`) on consumer CPU (<1.2 GB RAM) with FP32 logit upcast, converging at the evaluation/comparison stage.
3. **Disagreement Statistics Decoupling (Figure 4):** Strictly separates Pearson $r$, Spearman $\rho$, nested OLS $F$-tests, and cross-validated $\Delta R^2_{\text{OOF}}$ rather than combining them into a single-axis forest plot.
4. **Metric Discrepancy Resolution:** Establishes **SmolLM2-1.7B Spearman $\rho = 0.3929$ ($p = 0.0048$)** as the canonical verified value on TrustEval's 50-item evaluation sample (Table 4), clarifying that $\rho = 0.26$ derives from Ali (2026)'s prior full-dataset pilot benchmark.
5. **Reconsideration of Appendix Figure 5:** Demonstrates that a 20-bin step density with $N=50$ introduces severe binning artifacts and duplicates Figure 1's observation strips; provides a clear recommendation to prune it for publication economy while maintaining full conditional specifications.
6. **Final Numbering & Sequential Implementation Sequence:** Formally aligns all figure numbers (1 through 6), filenames, script mappings, output paths, and execution order.

---

## 1. Literature-Inspired Visual Design Principles

Our visual audit of landmark papers in automated evaluation and AI safety reveals six universal design principles that govern publication-grade scientific graphics:

### Principle 1: The Teaser as an Empirical Demonstration, Not a Scorecard
- **Literature Precedent:** Schwinn et al. (ICML 2026, Fig. 1) placed a high-impact empirical graphic on Page 1 demonstrating that standard safety judges deviate by up to 40% from human ground truth. Debenedetti et al. (IEEE SaTML 2024, Fig. 1) placed a geometric search diagram on Page 1 contrasting naive vs. stealthy boundary exploration.
- **Application to TrustEval (Figure 1):** Page 1 must not feature static text cards or tabular scorecards. Instead, it displays a dual-panel empirical graphic:
  - Upper Panel: A 2D **Capability Trade-Off Plane** plotting Discriminative Ranking (AUROC) against Mean Absolute Error (MAE), visually proving why sub-2B models require ensembling: Qwen2.5-0.5B achieves high ranking acuity (AUROC 0.7529) but high error (MAE 0.4152); SmolLM2-1.7B achieves low error (MAE 0.1734) but weak discrimination (AUROC 0.6690); the Two-Judge Ensemble bridges this gap (AUROC 0.7517, MAE 0.2464).
  - Lower Panel: Raw observation strips or empirical cumulative distribution functions (eCDFs) displaying the empirical distribution of predictions across all 50 items.

### Principle 2: Exposing Degeneracy in Calibration Metrics
- **Literature Precedent:** Guo et al. (ICML 2017, Fig. 1) established reliability diagrams with decile sample occupancy histograms. Schwinn et al. (ICML 2026, Fig. 3) emphasized that low ECE can be deceptive when predictions collapse to a single bin.
- **Application to TrustEval (Figure 3):** ECE cannot be interpreted in isolation. SmolLM2 populates only 2 decile bins, and the constant prevalence baseline achieves an ostensible ECE $= 0.0000^*$ purely by falling entirely into decile bin $[0.3, 0.4)$. The reliability diagram must couple decile calibration curves with sample occupancy bars and isolate the degenerate baseline as a discrete point at $(0.338, 0.338)$, accompanied by explicit non-calibration footnotes.

### Principle 3: Structural Separation of Exploratory vs. Multivariable Modeling
- **Literature Precedent:** Bavaresco et al. (ACL 2025, Fig. 1–2) cleanly isolated exploratory bivariate scatter plots from nested linear models and random-effects structures.
- **Application to TrustEval (Figure 4):** Inter-judge disagreement ($\Delta$) is an exploratory heuristic, not a validated uncertainty measure. Figure 4 must isolate the primary bivariate scatter ($y = \text{Ensemble MAE Error}$, $x = \Delta$, $r = 0.3125, p = 0.0271$) and report Spearman rank correlation ($\rho = 0.2302, p = 0.1078$, not statistically significant) alongside nested OLS statistics ($F(1, 46) = 5.676, p = 0.0214$) and out-of-fold cross-validation ($\Delta R^2_{\text{OOF}} = +0.0805$) in distinct, clearly labeled cards—never combined into a single-axis forest plot.

### Principle 4: Decoupling Conceptual Workflow from Empirical Findings
- **Literature Precedent:** Tan et al. (ICLR 2025, Fig. 1–2) strictly distinguished their empirical benchmark evaluations from their proposed operational agent architecture. Verga et al. (arXiv 2024, Fig. 1) presented jury routing as a workflow diagram separate from empirical agreement tables.
- **Application to TrustEval (Figure 6):** The two-tier selective escalation workflow is a conceptual operational proposal with an uncalibrated threshold $\tau$, not a validated empirical finding. Placing a full-width conceptual flowchart in the empirical core would dilute scientific credibility and waste space under an 8–10 page budget. It belongs in **Appendix B** (or Section VII as an operational discussion).

### Principle 5: Construct Validity & Traceability to Raw Human Data
- **Literature Precedent:** Aroyo et al. (NeurIPS 2023 D&B, Fig. 2) provided exhaustive schematic illustrations showing crowd annotator question breakdowns and their transformation into continuous benchmark targets.
- **Application to TrustEval (Figure 2):** Top venues demand construct validity. Section III/IV must feature a dedicated architecture diagram detailing how 104 quality-filtered raters evaluating $Q_{\text{overall}}$ aggregate into $h_{\text{primary}} = Y / (Y + N)$, and how zero-shot prompt templates map to consumer CPU causal forward inference (<1.2 GB RAM, FP32 logit upcast).

### Principle 6: Strict Typographic and Geometric Restraint
- **Literature Precedent:** IEEE SaTML (Debenedetti et al., 2024) enforces strict single-column ($3.50\text{ in}$) and full-width ($7.00\text{ in}$) grid alignment with serif typography matching the master document.
- **Application to TrustEval:** All figures must be generated as dual-format assets (vector `.pdf` with embedded TrueType fonts and $300\text{ DPI}$ `.png`) adhering to IEEE column widths and Computer Modern / Times Roman serif typography.

---

## 2. Critical Audit of Candidate Figures & Proposed Evolution

```
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| Figure   | Initial Concept (Phase 2B.1)| Scientific Audit & Corrections | Final Fate      | Paper Placement     |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| FIG. 1   | 3 text cards + strip plot   | Text-heavy dashboard layout;   | Major Redesign  | Main Body: Page 1   |
| (Teaser) | showing summary statistics  | baseline plotted on AUROC plane| (Empirical      | (Section I)         |
|          |                             | was uninterpretable; Qwen was  | Trade-Off Plane |                     |
|          |                             | incorrectly assumed bimodal    | + Raw Strips)   |                     |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| FIG. 2   | Missing from initial draft  | Top reviewers demand construct | New Figure      | Main Body: Page 3   |
| (Arch.)  | (system architecture was    | validity and exact rater/CPU   | (Evaluation     | (Section III/IV)    |
|          | purely textual)             | pipeline verification          | Architecture)   |                     |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| FIG. 3   | 10-bin reliability curves   | High scientific value; upper   | Retain & Refine | Main Body: Page 5   |
| (Calib.) | + sample occupancy bars     | legend and callout card clean; | (Maintain ECE   | (Section V)         |
|          |                             | isolates degenerate baseline   | qualification)  |                     |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| FIG. 4   | Scatter of 50 items + OLS   | Critical separation required:  | Retain & Polish | Main Body: Page 7   |
| (Disagr.)| fit ribbon + combined stats | do NOT combine r, rho, F, and  | (Distinct Stats | (Section VI)        |
|          |                             | R^2 into a shared forest plot  | Cards)          |                     |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| FIG. 5   | 20-bin empirical step       | For N=50, 20 bins cause severe | Prune / Keep    | Appendix F          |
| (Density)| density overlay across      | binning noise; largely repeats | as Conditional  | (Diagnostics)       |
|          | evaluators and target       | Fig. 1 distribution strips     | Appendix Asset  |                     |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
| FIG. 6   | Full-width 6-step           | Uncalibrated conceptual        | Move to         | Appendix B          |
| (Flow)   | operational workflow for    | proposal; must not displace    | Appendix B      | (Operational        |
|          | selective human escalation  | empirical space in main body   | (Full Width)    | Framework)          |
+----------+-----------------------------+--------------------------------+-----------------+---------------------+
```

---

## 3. Approved Research Visual Inventory

The approved visual inventory aligns strictly with the primary IEEE two-column paper budget (8–10 pages), prioritizing empirical proof in the main body and isolating conceptual workflows and secondary diagnostics in appendices:

```
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| ID       | Figure Title & Scientific Objective                    | Format      | Width     | Paper Placement    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| FIG. 1   | Evaluator Polarization & Trade-Off Frontier            | Empirical   | 3.5 in    | Main Body: Page 1  |
| (Teaser) | Demonstrates the AUROC vs. MAE capability plane and    | Teaser      | (1 col)   | (Section I)        |
|          | empirical prediction distribution strips (N=50).       |             |           |                    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| FIG. 2   | Evaluation Architecture & Construct Validity           | System /    | 3.5 in    | Main Body: Page 3  |
| (Arch.)  | Two-path pipeline: DICES 104-rater continuous consensus| Methodology | (1 col)   | (Section III/IV)   |
|          | aggregation and zero-shot CPU inference (<1.2 GB RAM). |             |           |                    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| FIG. 3   | Reliability Diagrams & Sample Occupancy                | Statistical | 3.5 in    | Main Body: Page 5  |
| (Calib.) | Decile calibration curves exposing SmolLM2 compression | Calibration | (1 col)   | (Section V)        |
|          | and the degenerate single-bin baseline (0.0000*).      |             |           |                    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| FIG. 4   | Disagreement Analysis as an Error Correlate            | Statistical | 3.5 in    | Main Body: Page 7  |
| (Disagr.)| Bivariate scatter of 50 items with OLS fit, 95% CI     | Regression  | (1 col)   | (Section VI)       |
|          | ribbon, and distinct Pearson, Spearman, and OLS cards. |             |           |                    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| FIG. 5   | Distribution Diagnostics Across Evaluators             | Diagnostic  | 3.5 in    | Appendix F         |
| (Density)| 20-bin empirical step density overlay (conditional:    | Empirical   | (1 col)   | (Diagnostics)      |
|          | recommended for pruning due to Fig. 1 redundancy).     |             |           |                    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
| FIG. 6   | Conceptual Escalation Architecture                     | Conceptual  | 7.0 in    | Appendix B         |
| (Flow)   | Full-width 6-step operational workflow for two-tier    | Workflow    | (2 col)   | (or Section VII)   |
|          | CPU auditing with uncalibrated threshold tau.          |             |           |                    |
+----------+--------------------------------------------------------+-------------+-----------+--------------------+
```

---

## 4. Detailed Design Specifications for Approved Figures

### FIG. 1: Evaluator Polarization & Trade-Off Frontier (Page 1 Teaser)
- **Primary Scientific Purpose:** Immediately establish the core empirical tension of RQ1 and RQ2 on Page 1: compact sub-2B judges exhibit opposing failure modes that motivate ensembling, while framing the ensemble accurately as an observed trade-off rather than an objectively optimal solver.
- **Visual Composition (Two-Tier Single-Column Layout, $3.5\text{ in} \times 3.6\text{ in}$):**
  - **Upper Panel (The Capability Trade-Off Plane):** A 2D scatter space plotting **Discriminative Ranking (AUROC)** on the $Y$-axis ($[0.55, 0.82]$) against **Mean Absolute Error (MAE)** on the inverted $X$-axis ($[0.45, 0.15]$, where rightward indicates lower error).
    - **Constituent Observations (Three Judges Only):**
      - *Qwen2.5-0.5B:* Plotted at $(0.4152, 0.7529)$ in Steel Blue (`#1f77b4`). Strong ranking sensitivity but severe approximation error.
      - *SmolLM2-1.7B:* Plotted at $(0.1734, 0.6690)$ in Amber Orange (`#d95f02`). Low point prediction error but weak discrimination.
      - *Two-Judge Ensemble:* Plotted at $(0.2464, 0.7517)$ in Forest Green (`#2ca02c`). Cuts Qwen's MAE by $40.6\%$ while matching its AUROC.
    - **Exclusion of Prevalence Baseline as an Ordinary Scatter Point:** The 5-fold out-of-fold prevalence baseline ($0.338 \pm 0.014$) produces constant predictions within each validation fold; its ostensible AUROC ($0.3601$) and ranking correlations are artifacts of fold partitioning noise rather than meaningful ranking behavior, and its coordinates fall far outside the interpretable AUROC range. Therefore, the baseline is **not** plotted as a fourth point on the scatter plane.
    - **Communicating Baseline Error Performance:** The baseline's verified error metrics ($\text{MAE} = 0.1983$, $\text{RMSE} = 0.2454$, $\text{Soft MSE} = \mathbf{0.0602}$) are communicated via a dedicated vertical reference line or contextual benchmark note along the MAE axis.
    - **Trade-Off Boundary:** A clean dashed curve connects the non-dominated points, illustrating the empirical Pareto trade-off between discrimination and calibration without claiming mathematical optimality.
  - **Lower Panel (Empirical Observation Strips):**
    - Raw observation strips (jittered rug plot / dot plot) or empirical CDF (eCDF) curves showing the exact 50 conversation predictions against human targets ($h_{\text{primary}}$).
    - **Rejection of Automatic Smoothing / Violin Curves:** With $N=50$, kernel density estimation introduces spurious smoothing artifacts (e.g., probability mass outside $[0, 1]$ or fictitious modes). Raw observation strips faithfully expose:
      - *Qwen2.5-0.5B Skew:* Heavily concentrated in $[0.80, 1.00]$ (28 out of 50 items; $\mu = 0.751, \sigma = 0.188$), with a long, sparse left tail down to $0.165$. **Direct data verification confirms Qwen is NOT bimodal**; it is unimodal and strongly left-skewed (hyper-cautious).
      - *SmolLM2-1.7B Collapse:* Severe variance collapse ($\mu = 0.253, \sigma = 0.028$), taking on only 6 distinct discrete values across all 50 items ($0.245$ and $0.269$ account for 33/50 items).
      - *Ensemble Centering:* Centered distribution ($\mu = 0.502, \sigma = 0.098$, range $[0.194, 0.634]$).
      - *Human Ground Truth ($h_{\text{primary}}$):* Broad consensus spread ($\mu = 0.338, \sigma = 0.244$, range $[0.039, 0.952]$).
- **Required Evidence:** `results/tables/ensemble_predictions_dices50.csv`, `results/tables/evaluation_metrics_dices50.json`.
- **Literature Inspiration:** Schwinn et al. (ICML 2026, Fig. 1); Debenedetti et al. (IEEE SaTML 2024, Fig. 1).
- **Placement:** Page 1, Upper Right Column (Section I). **Priority: Essential.**

---

### FIG. 2: Evaluation Architecture & Construct Validity
- **Primary Scientific Purpose:** Establish complete construct validity, operational reproducibility, and on-premises feasibility for Section III & IV. Explicitly shows the sampling, rater filtering, target aggregation, zero-shot prompt compilation, and CPU causal inference converging at evaluation.
- **Visual Composition (Vertical Single-Column Flowchart, $3.5\text{ in} \times 3.8\text{ in}$):**
  - **Stage 1: Source & Sampling Pipeline:**
    - Source: Full DICES-350 dataset ($N=350$ multi-turn adversarial dialogues).
    - Sampling: Fixed-seed simple random sample without replacement ($N=50$ conversations, seed `20261103`, manifest verified at `data/processed/dices_50_sample_manifest.parquet`).
    - Explicitly splits into two parallel evaluation paths:
  - **Stage 2A: Human Reference Path (Construct Ground Truth):**
    - 123 initial crowd raters $\to$ Protocol quality filter removing 19 author-flagged raters $\to$ **Exactly 104 retained annotators** per conversation ($5,200$ total ratings across 50 items).
    - Raters evaluate overall conversation safety ($Q_{\text{overall}} \in \{\text{Yes}, \text{No}, \text{Unsure}\}$), which synthesizes 5 underlying safety dimensions: Q2 (Harmful Content), Q3 (Unfair Bias), Q4 (Misinformation), Q5 (Political Topics), and Q6 (Policy Guidelines).
    - Verified decisive vote aggregation:
      $$h_{\text{primary}, i} = \frac{Y_i}{Y_i + N_i} \in [0, 1] \quad (\bar{h} = 0.3381)$$
  - **Stage 2B: Judge Path (Local Consumer CPU Execution):**
    - Unlabeled multi-turn dialogue $\to$ Standardized zero-shot prompt template (`TrustEval-R0`, `safety_judge_v1.txt`).
    - Native ChatML compilation (`<|im_start|>system...<|im_start|>user...<|im_start|>assistant\n`).
    - Parallel execution on consumer CPU (<1.2 GB RAM, BF16 weights, FP32 logit upcast):
      - *Qwen2.5-0.5B-Instruct* (0.49B params, vocab 151,936; target tokens `Yes`: 9454, `No`: 2753).
      - *SmolLM2-1.7B-Instruct* (1.71B params, vocab 49,152; target tokens `Yes`: 10539, `No`: 5230).
    - Deterministic single-forward-pass logit extraction at sequence index `-1` (assistant first token position):
      $$P(\text{Unsafe}) = \frac{\exp(z_{\text{Yes}})}{\exp(z_{\text{Yes}}) + \exp(z_{\text{No}})}$$
    - Ensemble averaging ($P_{\text{ens}} = 0.5(P_{\text{qwen}} + P_{\text{smol}})$) and absolute disagreement ($\Delta = |P_{\text{qwen}} - P_{\text{smol}}|$).
  - **Stage 3: Convergence & Evaluation Stage:**
    - Both paths converge to compare $P_{\text{model}}$ against $h_{\text{primary}}$ across:
      - Point Approximation Error (MAE, RMSE, Soft MSE)
      - Calibration (Soft-Target ECE-10, reliability diagrams)
      - Ranking & Discrimination (Pearson $r$, Spearman $\rho$, AUROC)
      - Error Covariance & Disagreement Correlation ($\Delta$)
- **Required Evidence:** `scripts/02_prepare_data.py`, `src/trusteval/data/preprocessor.py`, `data/processed/dices_50_sample_manifest.json`, `configs/prompts/safety_judge_v1.txt`.
- **Literature Inspiration:** Aroyo et al. (NeurIPS 2023 D&B, Fig. 2); Tan et al. (ICLR 2025, Fig. 1–2).
- **Placement:** Section III/IV, Single Column ($3.5\text{ in}$). **Priority: Essential.**

---

### FIG. 3: Reliability Diagrams & Sample Occupancy
- **Primary Scientific Purpose:** Directly answer RQ2 regarding model calibration. Exposes the reality behind Brier and ECE scores by contrasting reliability curves with decile sample occupancy.
- **Visual Composition (Two-Tier Single-Column Layout, $3.5\text{ in} \times 3.8\text{ in}$):**
  - **Upper Panel (Calibration Curves):**
    - Diagonal dashed line of perfect calibration ($y = x$).
    - Qwen curve (8 populated bins): shows severe overconfidence ($P > \text{Target}$).
    - SmolLM2 curve (2 populated bins): confined strictly to $[0.2, 0.4]$.
    - Ensemble curve (6 populated bins): moderated slope tracking closer to diagonal.
    - Prevalence Baseline: rendered as an **isolated purple star** at $(0.338, 0.338)$ rather than a continuous curve.
    - Unblocked legend positioned in the upper-left quadrant ($x < 0.45, y > 0.55$).
    - Explanatory footnote: *"Note: The baseline occupies one calibration bin; ECE = 0.0000* is a coarse one-bin aggregation artifact and does not establish reliable calibration."*
  - **Lower Panel (Decile Sample Occupancy):**
    - Grouped bar chart displaying the count of items falling into each decile bin $[0.0, 0.1), \dots, [0.9, 1.0]$.
    - Visually proves SmolLM2's failure of coverage (all 50 items concentrated in 2 bins) vs. Qwen's broad 8-bin coverage.
- **Required Evidence:** `results/tables/ensemble_predictions_dices50.csv`, `results/tables/evaluation_metrics_dices50.json`.
- **Literature Inspiration:** Guo et al. (ICML 2017, Fig. 1); Schwinn et al. (ICML 2026, Fig. 3).
- **Placement:** Section V, Single Column ($3.5\text{ in}$). **Priority: Essential.**

---

### FIG. 4: Disagreement Analysis as an Error Correlate
- **Primary Scientific Purpose:** Directly evaluate RQ3: does inter-judge disagreement ($\Delta = |P_{\text{qwen}} - P_{\text{smol}}|$) reliably track ensemble prediction error ($|P_{\text{ens}} - h_{\text{primary}}|$)?
- **Visual Composition (Single-Column Bivariate Scatter + Statistical Cards, $3.5\text{ in} \times 3.5\text{ in}$):**
  - **Main Scatter Panel:**
    - 50 semi-transparent scatter points plotting Ensemble Absolute Error ($Y$-axis, $[0.0, 0.6]$) against Inter-Judge Disagreement $\Delta$ ($X$-axis, $[0.0, 0.8]$).
    - Ordinary Least Squares (OLS) regression line with shaded 95% bootstrap confidence ribbon.
  - **Strict Statistical Decoupling (No Shared Forest Plot):**
    - In accordance with audit instructions, correlation coefficients ($r, \rho$), regression $F$-statistics, and out-of-fold $\Delta R^2$ represent distinct statistical quantities and **must not be combined on a single shared effect axis**.
    - Instead, they are presented in cleanly partitioned summary cards:
      - **Bivariate Correlation Card:**
        - Pearson $r = 0.3125$ ($p = 0.0271$, unadjusted nominal significance).
        - Spearman $\rho = 0.2302$ ($p = 0.1078$, not statistically significant; demonstrates monotonic ranking relationship is fragile).
      - **Nested In-Sample OLS Card:**
        - Controlled for response character length: $F(1, 46) = 5.676$ ($p = 0.0214$).
      - **Out-of-Fold Cross-Validation Card:**
        - 5-fold cross-validation incremental gain: $\Delta R^2_{\text{OOF}} = +0.0805$ (clearly designated as descriptive out-of-fold performance).
  - **Mandatory Scientific Qualification:** Card footnote: *"Disagreement exhibits moderate linear correlation with error but is non-significant under monotonic ranking (Spearman rho = 0.2302, p = 0.108); it serves as a preliminary heuristic, not a validated confidence metric."*
- **Required Evidence:** `results/tables/ensemble_predictions_dices50.csv`, `results/tables/disagreement_cv_dices50.json`, Manuscript Section 7.3 & Table 7.
- **Literature Inspiration:** Bavaresco et al. (ACL 2025, Fig. 1–2); Zheng et al. (NeurIPS 2023, Fig. 2).
- **Placement:** Section VI, Single Column ($3.5\text{ in}$). **Priority: Essential.**

---

### FIG. 5: Distribution Diagnostics Across Evaluators (Reconsidered & Conditional)
- **Scientific Role & Redundancy Assessment:**
  - Figure 1 already features an empirical prediction-distribution component (raw observation strips / eCDF).
  - With a sample size of $N=50$, a 20-bin histogram (bin width 0.05) has an expected occupancy of only 2.5 items per bin. For SmolLM2, all 50 items fall into just 2 adjacent bins ($[0.20, 0.25]$ and $[0.25, 0.30]$). For Qwen, 28 items fall into $[0.80, 1.00]$, leaving 22 items sparsely scattered across the remaining 16 bins.
  - Consequently, a 20-bin step density exhibits severe binning noise without revealing information not already visible in Figure 1's raw observation strips.
  - **Explicit Recommendation:** **Prune / remove Figure 5** from the manuscript visual inventory to prevent visual repetition and preserve manuscript brevity.
  - **Conditional Specification (If Retained by Author Direction):**
    - If retained as an appendix diagnostic in **Appendix F**, it displays pure step densities (un-smoothed histograms with `histtype='step'`) comparing Qwen, SmolLM2, Ensemble, and Human Target $h_{\text{primary}}$, highlighting that empirical distributions do not match normal or kernel-smoothed approximations.
- **Placement:** Appendix F (Methodological Diagnostics), Single Column ($3.5\text{ in}$). **Status: Conditional / Recommended for Omission.**

---

### FIG. 6: Conceptual Escalation Architecture
- **Primary Scientific Purpose:** Provide a clear, practical system diagram illustrating how a resource-constrained enterprise can operationalize a two-tier safety auditing pipeline using compact local models.
- **Visual Composition (Full-Width Double-Column Layout, $7.0\text{ in} \times 2.6\text{ in}$):**
  - Six horizontal workflow stages:
    1. *Input Ingestion:* Multi-turn dialogue stream.
    2. *Local CPU Inference:* Zero-shot ChatML prompt on Qwen2.5-0.5B and SmolLM2-1.7B (<1.2 GB RAM, 0 cloud API calls).
    3. *Ensemble Aggregation & Metric Extraction:* $P_{\text{ens}}$ and Disagreement $\Delta$.
    4. *Decision & Disagreement Triage:* Fast automated routing if $\Delta \le \tau$; routing to escalation if $\Delta > \tau$.
    5. *Human-in-the-Loop Arbitration:* Flagged ambiguous items routed to expert review.
    6. *Continuous Audit Log:* Storing decisions and annotator feedback.
  - **Mandatory Operational Qualification Banner:**
    - *"Conceptual Operational Framework: The threshold tau is uncalibrated and requires task-specific empirical tuning. This workflow illustrates a potential deployment pattern and was not evaluated as an automated production system in this study."*
- **Required Evidence:** Manuscript Section 9.2, `results/tables/disagreement_cv_dices50.json`.
- **Literature Inspiration:** Verga et al. (arXiv 2024, Fig. 1); Tan et al. (ICLR 2025, Fig. 1).
- **Placement:** Appendix B (or Section VII Operational Discussion), Double Column ($7.0\text{ in}$). **Priority: Secondary (Appendix).**

---

## 5. Literature Reference Mapping

```
+----------+-----------------------------+---------------------------+---------------------------------------------+
| Visual   | Literature Reference        | Specific Paper Element    | Exact Visual Concept Adopted                |
+----------+-----------------------------+---------------------------+---------------------------------------------+
| FIG. 1   | Schwinn et al. (ICML 2026)  | Fig. 1 (PDF p. 1)         | Upper-right Page 1 teaser displaying        |
| (Teaser) | Debenedetti (IEEE SaTML 24) | Fig. 1 (PDF p. 1)         | capability trade-off plane and raw strips.  |
+----------+-----------------------------+---------------------------+---------------------------------------------+
| FIG. 2   | Aroyo et al. (NeurIPS 2023) | Fig. 2 (PDF p. 4)         | Parallel data flow: crowd rater aggregation |
| (Arch.)  | Tan et al. (ICLR 2025)      | Fig. 2 (PDF p. 4)         | vs. deterministic CPU logit extraction.     |
+----------+-----------------------------+---------------------------+---------------------------------------------+
| FIG. 3   | Guo et al. (ICML 2017)      | Fig. 1 (PDF p. 2)         | Reliability diagram paired with decile      |
| (Calib.) | Schwinn et al. (ICML 2026)  | Fig. 3 (PDF p. 6)         | occupancy; discrete degenerate baseline.    |
+----------+-----------------------------+---------------------------+---------------------------------------------+
| FIG. 4   | Bavaresco et al. (ACL 2025) | Fig. 1 & 2 (PDF pp. 3-4)  | Bivariate scatter with distinct statistical |
| (Disagr.)| Zheng et al. (NeurIPS 2023) | Fig. 2 (PDF p. 8)         | cards; separation of correlation and OLS.   |
+----------+-----------------------------+---------------------------+---------------------------------------------+
| FIG. 5   | Bavaresco et al. (ACL 2025) | Fig. 1 (PDF p. 3)         | Pure step-density comparison across bins    |
| (Density)|                             |                           | without kernel density estimation.          |
+----------+-----------------------------+---------------------------+---------------------------------------------+
| FIG. 6   | Verga et al. (arXiv 2024)   | Fig. 1 (PDF p. 1)         | Multi-tier model routing and selective      |
| (Flow)   | Tan et al. (ICLR 2025)      | Fig. 1 (PDF p. 2)         | escalation with threshold qualification.    |
+----------+-----------------------------+---------------------------+---------------------------------------------+
```

---

## 6. Scientific Visual Language & Styling System

All figures adhere to the following unified design system:

### A. Restrained Colorblind-Accessible Palette
Derived from Okabe-Ito and Tableau Color Blind palettes with strict semantic entity binding:
- **Qwen2.5-0.5B-Instruct:** `#1f77b4` (Steel Blue)
- **SmolLM2-1.7B-Instruct:** `#d95f02` (Amber Orange)
- **Two-Judge Ensemble:** `#2ca02c` (Forest Green)
- **Prevalence Baseline:** `#7570b3` (Muted Purple)
- **Human Ground Truth ($h_{\text{primary}}$):** `#4a4a4a` (Dark Charcoal)
- **Regression Fit & Accents:** `#333333` (Charcoal) with `#1f77b4` / `#2ca02c` confidence fills.

### B. Typography & Mathematical Typesetting
- **Font Family:** Computer Modern / Times Roman Serif (`plt.rcParams['font.family'] = 'serif'`), perfectly matching `IEEEtran.cls`.
- **Size Hierarchy:**
  - Panel Titles / Major Headings: $8.0\text{ pt}$ to $8.5\text{ pt}$, bold.
  - Axis Labels & Table Headers: $7.2\text{ pt}$ to $7.5\text{ pt}$, medium.
  - Tick Labels & Callout Text: $6.5\text{ pt}$ to $6.8\text{ pt}$.
  - Footnotes & Technical Notes: $5.2\text{ pt}$ to $5.8\text{ pt}$.
- **Mathematical Rigor:** Rendered via native mathtext: $\rho$, $\tau$, $\Delta$, $\mu$, $\sigma$, $P_{\text{ens}}$, $h_{\text{primary}}$.

### C. Geometry & Output Mechanics
- **Single-Column Width:** Exactly $3.50\text{ in}$ ($252\text{ pt}$). Heights: $3.2\text{ in}$ to $3.8\text{ in}$.
- **Full-Width Width:** Exactly $7.00\text{ in}$ ($516\text{ pt}$). Height: $2.60\text{ in}$.
- **Dual Export Pipeline:** Standalone Python scripts export both vector `.pdf` (`pdf.fonttype=42`) and $300\text{ DPI}$ `.png` with identical bounding boxes (`bbox_inches='tight'`).

---

## 7. Metric Discrepancy Resolution & Scientific Integrity Requirements

### Canonical Metric Discrepancy Resolution
- **Issue:** Recent preliminary draft text reported SmolLM2 Spearman $\rho = 0.2608$, whereas the frozen master manuscript reports $\rho = 0.3929$.
- **Audit Findings:**
  - In `results/tables/evaluation_metrics_dices50.json` and Table 4 of [`research/paper/TRUSTEVAL_PAPER_V2_5_3_4.md`](TRUSTEVAL_PAPER_V2_5_3_4.md), the canonical verified metric across the 50 DICES conversations evaluated in TrustEval is:
    $$\mathbf{\text{SmolLM2-1.7B Spearman } \rho = 0.3929 \quad (p = 0.0048)}$$
  - The value $\rho = 0.26$ ($[0.16, 0.36]$) originates from Ali (2026)'s prior benchmark on the full DICES-350 cohort ($N=350$), as reported in Section 2.2 / Table 1.
  - **Resolution:** All figures, captions, and blueprint specifications shall use the canonical 50-item evaluation result **$\rho = 0.3929$ ($p = 0.0048$)** consistently.

### Non-Negotiable Verification Gates
1. **Sample Verification:** All plots must use the frozen 50-conversation sample from `ensemble_predictions_dices50.csv` (seed `20261103`, exactly 104 raters per item). Zero synthetic points.
2. **Exact Numerical Values:**
   - Qwen2.5-0.5B: $\text{MAE} = 0.4152$, $\text{AUROC} = 0.7529$, $\text{Spearman } \rho = 0.5680$, $\text{Mean} = 0.7509 \pm 0.1884$.
   - SmolLM2-1.7B: $\text{MAE} = 0.1734$, $\text{AUROC} = 0.6690$, $\mathbf{\text{Spearman } \rho = 0.3929}$, $\text{Mean} = 0.2531 \pm 0.0279$.
   - Two-Judge Ensemble: $\text{MAE} = 0.2464$ ($-40.6\%$ vs Qwen), $\text{AUROC} = 0.7517$, $\text{Spearman } \rho = 0.5903$, $\text{Pearson } r = 0.4992$.
   - Prevalence Baseline: $\text{RMSE} = 0.2454$, $\text{Soft MSE} = \mathbf{0.0602}$, $\text{ECE} = 0.0000^*$ (1 bin).
   - Disagreement: Pearson $r = 0.3125$ ($p = 0.0271$); Spearman $\rho = 0.2302$ ($p = 0.1078$, not sig.); nested OLS $F(1, 46) = 5.676$ ($p = 0.0214$); 5-fold cross-validation $\Delta R^2_{\text{OOF}} = +0.0805$ (purely descriptive).
3. **Prohibited Claims:**
   - Do NOT draw a continuous calibration line for the baseline.
   - Do NOT claim the ensemble is objectively optimal; present it as an observed empirical compromise.
   - Do NOT claim Qwen is bimodal; it is unimodal and left-skewed into $[0.8, 1.0]$.
   - Do NOT present disagreement as a validated uncertainty measure.
   - Do NOT present the escalation workflow as an empirical production system.

---

## 8. Final Figure Numbering & Implementation Sequence

In accordance with Section 6 of the audit instructions, the final figure numbering, script mappings, output filenames, and implementation sequence are strictly unified:

```
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| Fig # | Figure Title & Scientific Role                                 | Script Name                | Output Path (.pdf & .png)   | Manuscript Anchor   |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| FIG. 1| Evaluator Polarization & Trade-Off Frontier                    | `make_fig1_tradeoff.py`    | `figures/fig1_tradeoff.*`   | Section I (Page 1)  |
|       | (AUROC vs. MAE capability plane + raw observation strips)      |                            |                             |                     |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| FIG. 2| Evaluation Architecture & Construct Validity                   | `make_fig2_architecture.py`| `figures/fig2_architecture.*`| Section III/IV      |
|       | (Two-path pipeline: 104-rater aggregation & CPU inference flow)|                            |                             |                     |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| FIG. 3| Reliability Diagrams & Sample Occupancy                        | `make_fig3_reliability.py` | `figures/fig3_reliability.*`| Section V (Calib.)  |
|       | (Decile calibration curves + decile occupancy + baseline star) |                            |                             |                     |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| FIG. 4| Disagreement Analysis as an Error Correlate                    | `make_fig4_disagreement.py`| `figures/fig4_disagreement.*`| Section VI (Disagr.)|
|       | (Bivariate scatter + OLS ribbon + partitioned stats cards)     |                            |                             |                     |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| FIG. 5| Distribution Diagnostics Across Evaluators                     | `make_fig5_distribution.py`| `figures/fig5_distribution.*`| Appendix F (Diag.)  |
|       | (20-bin empirical step density; conditional upon retention)    |                            |                             |                     |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
| FIG. 6| Conceptual Escalation Architecture                             | `make_fig6_escalation.py`  | `figures/fig6_escalation.*` | Appendix B (Flow)   |
|       | (Full-width 6-step selective escalation workflow)              |                            |                             |                     |
+-------+----------------------------------------------------------------+----------------------------+-----------------------------+---------------------+
```

### Sequential Implementation Execution Plan
Upon authorization, implementation will proceed strictly **one figure at a time** following the final numbering:
1. **Step 1 — Figure 1:** Implement `make_fig1_tradeoff.py` (AUROC vs. MAE scatter with Pareto boundary + 50-item raw observation strips).
2. **Step 2 — Figure 2:** Implement `make_fig2_architecture.py` (Two-path evaluation architecture: 104-rater continuous consensus aggregation + zero-shot CPU inference pipeline).
3. **Step 3 — Figure 3:** Refine `make_fig3_reliability.py` (Reliability curves with unblocked legend, decile occupancy subpanel, and degenerate baseline star).
4. **Step 4 — Figure 4:** Refine `make_fig4_disagreement.py` (Bivariate scatter with OLS ribbon and strictly partitioned statistical cards for $r$, $\rho$, $F$, and $\Delta R^2_{\text{OOF}}$).
5. **Step 5 — Figure 5 (Conditional):** If retained, implement `make_fig5_distribution.py` (Appendix F step density); otherwise omit to maintain publication economy.
6. **Step 6 — Figure 6:** Refine `make_fig6_escalation.py` (Appendix B full-width 6-step escalation workflow with threshold qualification banner).
