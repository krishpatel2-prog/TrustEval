# Phase 4 Quality Audit & Verification Report: Discussion, Limitations, Ethics & Conclusion

**Paper Title:** *TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges*  
**Workspace:** `D:\Research\TrustEval`  
**LaTeX Target Directory:** `research/paper/latex/sections/`  
**Audit Date:** 2026-11-05  
**Quality Gate Status:** **PASSED — ALL SCIENTIFIC, ETHICAL & CONSISTENCY CRITERIA SATISFIED**

---

## 1. Executive Summary

Phase 4 completes the substantive body of the TrustEval IEEE research paper, delivering:
1. **Section VI — Discussion** (`sections/06_discussion.tex`): Provides a comprehensive synthesis of empirical results answering RQ1–RQ3, decouples correlation from calibration and pointwise error, analyzes the boundaries and failure modes of inter-judge disagreement, establishes edge deployment feasibility vs. readiness, and integrates findings with 5 literature pillars.
2. **Section VII — Limitations and Ethical Considerations** (`sections/07_limitations_ethics.tex`): Transparently documents dataset/sample constraints ($N=50$), human ground-truth subjectivities, evaluator modeling choices (sub-2B scope, fixed prompt, single-token extraction), statistical power limitations, and responsible AI governance principles.
3. **Section VIII — Conclusion and Future Work** (`sections/08_conclusion.tex`): Succinctly synthesizes primary empirical contributions without overstating ensemble capabilities, frames disagreement as an exploratory candidate error correlate, and outlines five grounded future directions.
4. **Appendix B Integration** (`appendices/appendix_b.tex`): Integrates Figure 6 (*Conceptual Selective Human Escalation Architecture*) with explicit disclaimers confirming its uncalibrated, conceptual status.
5. **Phase 3 Micro-Corrections**: Executed narrow, verified corrections to Table II (sample SD $s = 0.0144$ for prevalence baseline), Table III (exact Holm step-down values), and Shapiro-Wilk phrasing in Section V.
6. **Master LaTeX Synchronization** (`main.tex`): Updated to input `sections/06_discussion`, `sections/07_limitations_ethics`, and `sections/08_conclusion` sequentially.

---

## 2. Files Inspected and Created

### Authoritative Files Inspected
- `main.tex`
- `sections/01_introduction.tex`
- `sections/02_related_work.tex`
- `sections/03_dataset_ground_truth.tex`
- `sections/04_methodology_experimental_setup.tex`
- `sections/05_results.tex`
- `references.bib` (31 verified entries)
- `appendices/appendix_a.tex` & `appendices/appendix_b.tex`
- `figures/fig6_escalation.pdf` & `figures/fig6_escalation.png`
- `PHASE1_QUALITY_REVIEW.md`, `PHASE2_METHODOLOGY_AUDIT.md`, `PHASE2_NUMERICAL_RECONCILIATION.md`, `PHASE3_RESULTS_AUDIT.md`
- `results/tables/ensemble_predictions_dices50.csv`
- `results/tables/disagreement_cv_dices50.json`
- `results/diagnostics/phase_3c_statistical_refinements.json`
- `results/diagnostics/predictive_discrimination_audit.json`

### Section Files Created / Updated
- [`sections/06_discussion.tex`](file:///D:/Research/TrustEval/research/paper/latex/sections/06_discussion.tex) (New, complete)
- [`sections/07_limitations_ethics.tex`](file:///D:/Research/TrustEval/research/paper/latex/sections/07_limitations_ethics.tex) (New, complete)
- [`sections/08_conclusion.tex`](file:///D:/Research/TrustEval/research/paper/latex/sections/08_conclusion.tex) (New, complete)
- [`appendices/appendix_b.tex`](file:///D:/Research/TrustEval/research/paper/latex/appendices/appendix_b.tex) (Updated with Figure 6 integration & disclaimers)
- [`sections/05_results.tex`](file:///D:/Research/TrustEval/research/paper/latex/sections/05_results.tex) (Micro-corrections applied)
- [`main.tex`](file:///D:/Research/TrustEval/research/paper/latex/main.tex) (Updated modular inputs)

---

## 3. Research-Question Coverage Audit

The Discussion directly answers the three core research questions formulated in Section I:

| Research Question | Section I Formulation | Empirical Finding (Section V) | Discussion Synthesis (Section VI) |
|---|---|---|---|
| **RQ1: Representation Fidelity & Ensembling Trade-offs** | Can compact sub-2B models approximate continuous human soft consensus, and does an equal-weight ensemble improve representation fidelity? | Qwen overpredicts ($\bar{P}=0.751$, $\text{MAE}=0.4152$); SmolLM2 collapses ($\bar{P}=0.253$, $\text{MAE}=0.1734$). Ensemble cuts Qwen MAE by $40.6\%$ ($0.2464$) and Soft MSE by $67.6\%$ ($0.0713$), moderating to $\bar{P}=0.502$. | Section~\ref{subsec:disc_ensemble_tradeoff} explains bias cancellation. Emphasizes that ensemble is not universally dominant: SmolLM2 has lowest MAE via prevalence anchoring, and prevalence baseline has lowest Soft MSE ($0.0602$). |
| **RQ2: Pointwise Error vs. Ordinal Ranking Acuity** | Does lower pointwise error translate to superior ordinal ranking and majority-label discrimination? | SmolLM2 has lowest MAE but weaker rank correlation ($\rho=0.3929$) and AUROC ($0.6690$). Qwen has high MAE but strong ranking ($\rho=0.5680$, $\text{AUROC}=0.7529$). Ensemble achieves highest rank correlation ($\rho=0.5903$) and matches Qwen AUROC ($0.7517$). | Section~\ref{subsec:disc_correlation_ranking_calibration} explicitly decouples pointwise error from rank sensitivity. Explains why variance collapse minimizes loss without safety discernment. |
| **RQ3: Inter-Judge Disagreement as Error Signal** | Can inter-judge disagreement ($\Delta$) between diverse small models serve as an informative proxy for ensemble prediction error? | Pearson $r=0.3125$ ($p=0.0271$); Spearman $\rho=0.2302$ ($p=0.1078$); Nested OLS $\Delta R^2_{\text{in}}=+0.1039$, $F=5.676$ ($p=0.0214$); 5-fold CV $\Delta R^2_{\text{OOF}}=+0.0805$. | Section~\ref{subsec:disc_disagreement_implications} qualifies $\Delta$ as an exploratory candidate error correlate. Highlights non-significant Spearman ranking and proves that low $\Delta < 0.20$ does not guarantee safety due to shared blind spots. |

---

## 4. Claim-to-Evidence Consistency

Every interpretive claim made in Sections VI–VIII strictly matches experimental data:
1. **Ensemble Non-Dominance:** The manuscript repeatedly and explicitly acknowledges that the ensemble does NOT dominate every metric. SmolLM2 achieves lower sample MAE ($0.1734$ vs $0.2464$), the prevalence baseline achieves lower Soft MSE ($0.0602$ vs $0.0713$), and Qwen achieves nominally higher AUROC ($0.7529$ vs $0.7517$).
2. **Disagreement Status:** Inter-judge disagreement $\Delta$ is never described as "validated uncertainty", "calibrated confidence", or an "escalation trigger". It is strictly framed as an empirical *candidate error correlate*.
3. **ECE Interpretation:** The manuscript explicitly warns against comparing scalar ECE across models with sparse, non-uniform bin occupancy (SmolLM2 occupies 2 bins; prevalence baseline occupies 1 bin).
4. **Feasibility vs. Readiness:** The text explicitly decouples demonstrated CPU feasibility ($<1.2\text{ GB}$ RSS, BF16 weights, FP32 logits, zero cloud APIs) from production readiness. Autonomous safety governance is explicitly discouraged.

---

## 5. Citation and BibTeX Key Audit

A comprehensive programmatic audit of all `.tex` files was performed against `references.bib`:
- **Total BibTeX Entries in `references.bib`:** 31
- **Total Unique Citations in Manuscript:** 31
- **Missing Citations:** **0** (All `\cite{...}` tags resolve cleanly)
- **Unused BibTeX Entries:** **0** (Every single reference is cited in the text)
- **1-to-1 Literature Synthesis:** Section VI-E connects findings to literature across all 5 key thematic areas:
  1. *LLM-as-a-judge reliability:* Zheng et al.~\cite{zheng2023judging}, Wang et al.~\cite{wang2023pandalm}, Tan et al.~\cite{tan2025judgebench}, Bavaresco et al.~\cite{bavaresco2025llms}, Debenedetti et al.~\cite{debenedetti2024evading}.
  2. *Reference benchmark reconciliation:* Ali~\cite{ali2026whose}, Aroyo et al.~\cite{aroyo2023dices}.
  3. *Human subjectivity & soft targets:* Basile et al.~\cite{basile2021we}, Gordon et al.~\cite{gordon2021disagreement,gordon2022jury}, Davani et al.~\cite{davani2022dealing}, Rottger et al.~\cite{rottger2022two}.
  4. *Ensembles & calibration:* Lakshminarayanan et al.~\cite{lakshminarayanan2017simple}, Ovadia et al.~\cite{ovadia2019can}, Guo et al.~\cite{guo2017calibration}, Brier~\cite{brier1950verification}, Kuhn et al.~\cite{kuhn2023semantic}, Malinin \& Gales~\cite{malinin2018predictive}.
  5. *Small models & multi-agent juries:* Yang et al.~\cite{yang2024qwen25}, Ben Allal et al.~\cite{allal2025smollm2}, Laddha et al.~\cite{laddha2026slmjury}, Zhang et al.~\cite{zhang2026can}, Schwinn et al.~\cite{schwinn2026coin}.

---

## 6. Limitations and Ethical Claims Verification

The Limitations and Ethical Considerations section (Section VII) includes candid, specific disclosures:
- **Sample Constraints:** Documented $N=50$ sample drawn via simple random sampling without replacement; noted majority class imbalance (11 unsafe vs 39 safe; 429 evaluation pairs) and wider AUROC confidence intervals.
- **Spearman Power Planning:** Included formal Fisher $z$-transformation power calculation demonstrating that detecting $\rho=0.2302$ with $80\%$ power requires $N \ge 146$ items, explaining the lack of statistical significance under monotonic evaluation.
- **Ground Truth Properties:** Noted that human consensus excludes 311 Unsure votes in the primary target, and that half-weighting in the sensitivity target ($h_{\text{sensitivity}}$) is a modeling heuristic.
- **Annotator Clustering:** Acknowledged that 104 raters evaluate multiple items, introducing cluster dependence.
- **Evaluator Scope:** Noted evaluation is limited to two sub-2B models, a single prompt (`TrustEval-R0`), and next-token probability extraction without multi-step chain-of-thought reasoning.
- **Ethical Integrity:** Confirmed no claims of institutional review board (IRB) exemption, HIPAA/GDPR compliance, or clinical validation are made; all empirical analyses derive from publicly released benchmark artifacts.

---

## 7. Figure 6 and Appendix B Integration

- **Placement:** Integrated into [`appendices/appendix_b.tex`](file:///D:/Research/TrustEval/research/paper/latex/appendices/appendix_b.tex) as Figure~\ref{fig:escalation_workflow}, referencing [`figures/fig6_escalation.pdf`](file:///D:/Research/TrustEval/research/paper/latex/figures/fig6_escalation.pdf).
- **Critical Constraints Maintained:**
  1. Labeled explicitly as a *conceptual selective human escalation workflow*, not an operational or deployed production system.
  2. Documented that the escalation threshold $\tau$ is uncalibrated and conceptual.
  3. Re-emphasized that low disagreement ($\Delta < \tau$) does not guarantee safety correctness due to shared failure modes.
  4. Explicitly stated that empirical out-of-domain validation and utility cost-benefit calibration are mandatory prior to any deployment.

---

## 8. Phase 3 Micro-Corrections Applied

The following targeted micro-corrections were implemented in Section V (`sections/05_results.tex`), Table II, Table III, and the Phase 3 audit:

1. **Prevalence Baseline Standard Deviation (Check A):**
   - Recomputation from 50 OOF predictions: Population SD ($\text{ddof}=0$) $\sigma = 0.014215 \approx \mathbf{0.0142}$; Sample SD ($\text{ddof}=1$) $s = 0.014359 \approx \mathbf{0.0144}$.
   - Table II updated from `$0.3398 \pm 0.0142$` to `$0.3398 \pm 0.0144$` to strictly match the sample standard deviation ($s$) convention used across all other rows, with population SD $\sigma = 0.0142$ documented in the table footnote.
2. **Paired-Test Wording (Check B):**
   - Refined Section V-E wording: *"A Shapiro-Wilk test on the paired MAE differences provides strong empirical evidence of departure from normality ($W=0.8776$, $p=9.47\times 10^{-5}$), which urges caution when interpreting parametric $t$-test inferences and motivates non-parametric validation."*
3. **Holm-Bonferroni Step-Down Multipliers (Check C):**
   - In Table III, adjusted $p$-values were verified against exact Holm step-down multipliers ($m=6$):
     - Rank 1 (Qwen vs Ens MSE): $t$-test $p_{\text{adj}} = 2.85 \times 10^{-9}$ ($\times 6$); Wilcoxon $p_{\text{adj}} = 1.85 \times 10^{-8}$ ($\times 6$).
     - Rank 2 (Qwen vs Ens MAE): $t$-test $p_{\text{adj}} = 8.69 \times 10^{-8}$ ($\times 5$); Wilcoxon $p_{\text{adj}} = 1.07 \times 10^{-5}$ ($\times 5$).
     - Rank 3 (Qwen vs Smol MAE for $t$, MSE for Wilcoxon): $t$-test $p_{\text{adj}} = 1.15 \times 10^{-4}$ ($\times 4$); Wilcoxon $p_{\text{adj}} = 4.76 \times 10^{-4}$ ($\times 4$).
     - Rank 4 (Qwen vs Smol MSE for $t$, MAE for Wilcoxon): $t$-test $p_{\text{adj}} = 1.98 \times 10^{-4}$ ($\times 3$); Wilcoxon $p_{\text{adj}} = 5.51 \times 10^{-4}$ ($\times 3$).
     - Rank 5 (SmolLM vs Ens MAE): $t$-test $p_{\text{adj}} = \mathbf{0.0425}$ ($\times 2$); Wilcoxon $p_{\text{adj}} = \mathbf{0.0843}$ ($\times 2$, non-significant).
     - Rank 6 (SmolLM vs Ens MSE): $t$-test $p_{\text{adj}} = 0.6425$ ($\times 1$); Wilcoxon $p_{\text{adj}} = 0.1139$ ($\times 1$).

---

## 9. Updated Master Document Integration

[`main.tex`](file:///D:/Research/TrustEval/research/paper/latex/main.tex) lines 39–48 now read:
```latex
% Modular Sections
\input{sections/01_introduction}
\input{sections/02_related_work}
\input{sections/03_dataset_ground_truth}
\input{sections/04_methodology_experimental_setup}
\input{sections/05_results}
\input{sections/06_discussion}
\input{sections/07_limitations_ethics}
\input{sections/08_conclusion}
```

---

## 10. Unresolved Issues

- **Status:** **NONE**. All sections, references, figures, statistical checks, and ethical disclosures are fully synchronized and validated against source evidence.
