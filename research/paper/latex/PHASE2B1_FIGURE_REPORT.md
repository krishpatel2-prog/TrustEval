# TrustEval — Phase 2B.1 Scientific Figure Generation & Revision Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Phase:** Phase 2B.1 — Scientific Figure Generation & Targeted Visual Revisions  
**Date:** November 2026  
**Status:** Visual Revisions Complete (Awaiting Final Visual Review and Approval for Phase 2B.2)  
**Frozen Master Manuscript:** `research/paper/TRUSTEVAL_PAPER_V2_5_3_4.md` (Strictly Untouched)  
**Approved Design Blueprint:** `research/paper/REFERENCE_PAPER_ANALYSIS.md`  

---

## 1. Executive Summary & Integrity Confirmation

Following our first visual inspection of the generated research figures, targeted visual and layout revisions were performed across the figure generation scripts. 

- **Scientific & Numerical Integrity:** Strictly preserved. No changes were made to the underlying 50-conversation sample (`ensemble_predictions_dices50.csv`), prediction probabilities, statistical calculations, regression parameters, or evaluation metrics.
- **Master Manuscript Integrity:** `TRUSTEVAL_PAPER_V2_5_3_4.md` remains completely unmodified (110,950 bytes, last modified Thu Nov 5 13:12:07 2026).
- **Deliverables:** All five figures were regenerated as native vector PDFs (`.pdf`) and 300 DPI raster images (`.png`). The composite review sheet was updated at `figures/contact_sheet.png` (2300 × 3100 px) and `figures/contact_sheet.html`.

---

## 2. Summary of Targeted Revisions Applied

### Figure 1: Evaluator Paradigm & Trade-offs (Page 1 Teaser)
- **Reduced Text Volume:** Streamlined card descriptions from multi-line paragraphs into concise, punchy bulleted metrics.
- **Improved Spacing:** Expanded figure height from $3.4\text{ in}$ to $3.6\text{ in}$ and increased vertical grid spacing (`hspace=0.42`), ensuring ample separation between the top distribution plot and the cards below.
- **Unobscured X-Axis Label:** Calibrated label padding and bottom margins so that *"Predicted Probability $P(\mathrm{unsafe})$ vs. Human Target $h_{\mathrm{primary}}$"* renders crisply without clipping.
- **Precise Comparative Framing:**
  - *Qwen2.5-0.5B:* Highest judge AUROC ($0.7529$), strong ranking ($\rho = 0.5680$), but substantial overprediction ($\mu = 0.751$ vs. $0.338$) and high MAE ($0.4152$).
  - *SmolLM2-1.7B:* Lowest judge MAE ($0.1734$), low-variance anchor near prevalence ($\mu = 0.253, \sigma = 0.028$, $\text{AUROC} = 0.6690$).
  - *Two-Judge Ensemble:* Highest rank concordance ($\rho = 0.5903, r = 0.4992$), moderating bias ($\text{MAE} = 0.2464$, $-40.6\%$ vs Qwen), but explicitly contrasting with the held-out prevalence baseline retaining lower Soft MSE (**0.0602**).
- **Corrected Metric Precision:** Updated baseline Soft MSE display from $0.060$ to exact **$0.0602$**.

### Figure 2: Reliability and Decile Calibration
- **Unblocked Plotted Observations:** Relocated the legend from the crowded lower-right quadrant to the **upper-left region** ($x \in [0, 0.45], y \in [0.55, 1.0]$), which contains strictly zero data points. Plotted observations for Qwen, SmolLM2, and Ensemble now have 100% unobstructed visibility.
- **Degenerate Baseline Footnote:** Added the exact required methodological note:
  > *"Note: The baseline occupies one calibration bin; ECE = 0.0000 is a coarse one-bin aggregation result and does not establish reliable calibration."*
- **Single-Bin Visual Representation:** Maintained the baseline as an isolated distinct point marker (purple star) at $(0.338, 0.338)$ rather than a continuous curve.
- **Bin Occupancy Readability:** Cleaned spacing and tick styling on the lower decile occupancy bar chart ($3.5\text{ in} \times 3.8\text{ in}$).

### Figure 3: Inter-Judge Disagreement vs. Evaluation Error
- **Separated Statistical Summary Card:** Created a clean two-tier layout placing the statistical summary in a dedicated structured card *above* the scatter plot (`hspace=0.32`), completely eliminating any overlap with the 50 conversation points.
- **Accurate Linear Fit Label:** Updated the regression line label to *"Linear fit; Pearson $r = 0.313$"* as requested, strictly avoiding conflation of the bivariate OLS fit with correlation statistics.
- **Clear Statistical Distinctions:**
  - Bivariate Pearson: $r = 0.3125$, $p = 0.0271$ (nominally significant).
  - Bivariate Spearman: $\rho = 0.2302$, $p = 0.1078$ (**not statistically significant**).
  - Nested In-Sample OLS: $F(1, 46) = 5.676$, $p = 0.0214$.
  - 5-Fold Cross-Validation: $\Delta R^2_{\mathrm{OOF}} = +0.0805$ (**descriptive only** on $N=50$).
- **Methodological Disclaimer:** Preserved explicit footnote: *"Note: Candidate error correlate; not validated uncertainty."*

### Figure 4: Prediction Distribution Alignment (Appendix F)
- **Empirical Preservation:** Retained the true 20-bin empirical step density histogram without artificial kernel smoothing.
- **Layout & Spacing Refinement:** Set $Y$-axis limit to $18.0$ and aligned the single-column legend to the top-right corner to prevent any vertical crowding over the SmolLM2 peak ($\approx 15.5$ at $P \approx 0.25$).

### Figure 5: Conceptual Selective Human Escalation Workflow
- **Full-Width Horizontal Architecture:** Completely redesigned from a cramped single-column vertical layout into a spacious, full-width, two-column IEEE figure ($7.0\text{ in}$ wide $\times 2.8\text{ in}$ high).
- **Explicit 6-Step Process Numbering:**
  1. *1. Incoming Conversation:* Unlabeled multi-turn dialogue input.
  2. *2. Prompt Serialization:* Standardized TrustEval-R0 formatting (<1.2 GB CPU RAM).
  3. *3. Independent Judge Scoring:* Parallel branches for Judge 1 (Qwen2.5-0.5B $\to P_{\mathrm{qwen}}$) and Judge 2 (SmolLM2-1.7B $\to P_{\mathrm{smollm}}$).
  4. *4. Disagreement & Prediction Extraction:* Clearly rendered mathematical equations:
     $$P_{\mathrm{ens}} = \frac{1}{2}(P_{\mathrm{qwen}} + P_{\mathrm{smollm}})$$
     $$\Delta = |P_{\mathrm{qwen}} - P_{\mathrm{smollm}}|$$
  5. *5. Decision Diamond:* Large, legible threshold decision check ($\Delta < \tau$ ?).
  6. *6. Illustrative Routing Outcomes:* Visually distinct branches for **6a. Tier 1 Auto Audit** (Green, $P_{\mathrm{ens}}$ archived) vs. **6b. Tier 2 Human Review** (Red, flagged for safety expert team).
- **Prominent Methodological Banner:** Spanning the entire bottom width of the figure, explicitly emphasizing that:
  - Threshold $\tau$ is uncalibrated in this study.
  - Low disagreement does not guarantee correctness (models may fail jointly).
  - Independent out-of-domain validation is required before deployment.
  - The workflow is an illustrative conceptual proposal, not an implemented production pipeline.

---

## 3. Revised Figure Inventory and Specifications

| Figure Identifier | Script Path | Output Assets (PDF & PNG) | Physical Dimensions | Pixel Resolution (300 DPI) | Recommended Placement |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Figure 1** (Teaser) | `figures/scripts/make_fig1_teaser.py` | `fig1_teaser.pdf`<br>`fig1_teaser.png` | $3.5\text{ in} \times 3.6\text{ in}$ | $1488 \times 1032\text{ px}$ | **Main Body:** Page 1 (Top Right Column) |
| **Figure 2** (Calibration) | `figures/scripts/make_fig2_calibration.py` | `fig2_calibration.pdf`<br>`fig2_calibration.png` | $3.5\text{ in} \times 3.8\text{ in}$ | $1055 \times 1114\text{ px}$ | **Main Body:** Section V (Results) |
| **Figure 3** (Disagreement) | `figures/scripts/make_fig3_disagreement.py` | `fig3_disagreement.pdf`<br>`fig3_disagreement.png` | $3.5\text{ in} \times 3.5\text{ in}$ | $1292 \times 1063\text{ px}$ | **Main Body:** Section VI (Disagreement) |
| **Figure 4** (Step Density) | `figures/scripts/make_fig4_density.py` | `fig4_density.pdf`<br>`fig4_density.png` | $3.5\text{ in} \times 2.9\text{ in}$ | $1032 \times 853\text{ px}$ | **Appendix:** Appendix F (Diagnostic Residuals) |
| **Figure 5** (Workflow) | `figures/scripts/make_fig5_escalation.py` | `fig5_escalation.pdf`<br>`fig5_escalation.png` | $7.0\text{ in} \times 2.8\text{ in}$ | $1687 \times 706\text{ px}$ | **Main / Appendix:** Section VII / Appendix B (`figure*`) |
| **Contact Sheet** | `figures/scripts/make_contact_sheet.py` | `contact_sheet.png`<br>`contact_sheet.html` | $7.7\text{ in} \times 10.3\text{ in}$ | $2300 \times 3100\text{ px}$ | **Audit / Review Artifact** |

---

## 4. Preservation of Verified Numerical Source Data

| Statistic / Metric | Verified Ground Truth | Reported in Revised Figures | Integrity Status |
| :--- | :---: | :---: | :---: |
| Qwen2.5-0.5B MAE | $0.4152$ | Fig 1: $0.4152$ | **IDENTICAL** |
| Qwen2.5-0.5B AUROC | $0.7529$ | Fig 1: $0.7529$ | **IDENTICAL** |
| Qwen2.5-0.5B Spearman $\rho$ | $0.5680$ | Fig 1: $0.5680$ | **IDENTICAL** |
| Qwen2.5-0.5B Mean Pred ($\mu$) | $0.751$ | Fig 1: $0.751$ | **IDENTICAL** |
| SmolLM2-1.7B MAE | $0.1734$ | Fig 1: $0.1734$ | **IDENTICAL** |
| SmolLM2-1.7B AUROC | $0.6690$ | Fig 1: $0.6690$ | **IDENTICAL** |
| SmolLM2-1.7B Mean Pred ($\mu$) | $0.253$ | Fig 1: $0.253$ | **IDENTICAL** |
| SmolLM2-1.7B Pred Std ($\sigma$) | $0.028$ | Fig 1: $0.028$ | **IDENTICAL** |
| Ensemble MAE | $0.2464$ | Fig 1: $0.2464$ ($-40.6\%$ vs Qwen) | **IDENTICAL** |
| Ensemble AUROC | $0.7517$ | Fig 1: $0.7517$ | **IDENTICAL** |
| Ensemble Spearman $\rho$ | $0.5903$ | Fig 1: $0.5903$ | **IDENTICAL** |
| Ensemble Pearson $r$ | $0.4992$ | Fig 1: $0.4992$ | **IDENTICAL** |
| Held-Out Prevalence Baseline Soft MSE | **$0.0602$** | Fig 1: **$0.0602$** | **EXACT MATCH** |
| Disagreement Pearson $r$ | $0.3125$ ($p=0.0271$) | Fig 3: $r=0.3125, p=0.0271$ | **IDENTICAL** |
| Disagreement Spearman $\rho$ | $0.2302$ ($p=0.1078$) | Fig 3: $\rho=0.2302, p=0.1078$ (n.s.) | **IDENTICAL** |
| Nested In-Sample OLS $F$-Test | $F(1, 46) = 5.676$ ($p=0.0214$) | Fig 3: $F(1, 46)=5.676, p=0.0214$ | **IDENTICAL** |
| 5-Fold Cross-Validation $\Delta R^2_{\mathrm{OOF}}$ | $+0.0805$ (descriptive) | Fig 3: $\Delta R^2_{\mathrm{OOF}}=+0.0805$ (descriptive) | **IDENTICAL** |
| Degenerate Prevalence Baseline ECE | $0.0000^*$ (1 bin) | Fig 2: $0.0000^*$ (1 bin, isolated star) | **IDENTICAL** |

---

*Phase 2B.1 visual revisions are complete. The updated figures and composite contact sheet are ready for visual review. We are stopped and await your explicit approval before Phase 2B.2.*
