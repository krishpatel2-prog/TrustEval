# TrustEval: Phase 3C.5 Residual Manuscript Corrections and Final Artifact Verification Report

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `research/paper/`  
**Date:** November 5, 2026  
**Primary Master Manuscript Produced:** [`research/paper/TRUSTEVAL_PAPER_V2_5_2.md`](TRUSTEVAL_PAPER_V2_5_2.md)  
- **Exact File Size:** 78,785 bytes  
- **Exact Line Count:** 1,168 lines  
**Base Manuscript Audited:** [`research/paper/TRUSTEVAL_PAPER_V2_5_1.md`](TRUSTEVAL_PAPER_V2_5_1.md) (Preserved unchanged, 76,572 bytes, 1,170 lines)  
**Preserved Prior Manuscripts:**  
- [`research/paper/TRUSTEVAL_PAPER_V2_5.md`](TRUSTEVAL_PAPER_V2_5.md) (Preserved unchanged, 73,990 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_4.md`](TRUSTEVAL_PAPER_V2_4.md) (Preserved unchanged, 70,116 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_3.md`](TRUSTEVAL_PAPER_V2_3.md) (Preserved unchanged, 64,874 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_2.md`](TRUSTEVAL_PAPER_V2_2.md) (Preserved unchanged, 58,840 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2_1.md`](TRUSTEVAL_PAPER_V2_1.md) (Preserved unchanged, 57,198 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_V2.md`](TRUSTEVAL_PAPER_V2.md) (Preserved unchanged, 50,850 bytes)  
- [`research/paper/TRUSTEVAL_PAPER_DRAFT.md`](TRUSTEVAL_PAPER_DRAFT.md) (Preserved unchanged, 17,676 bytes)  
**Preserved Prior Audit Reports:**  
- [`research/paper/PHASE_3C_4_ERRATA_REPORT.md`](PHASE_3C_4_ERRATA_REPORT.md) (Preserved unchanged, 18,629 bytes)  
- [`research/paper/PHASE_3C_3_FINAL_AUDIT_REPORT.md`](PHASE_3C_3_FINAL_AUDIT_REPORT.md) (Preserved unchanged, 17,017 bytes)  
- [`research/paper/PHASE_3C_2_CORRECTION_REPORT.md`](PHASE_3C_2_CORRECTION_REPORT.md) (Preserved unchanged, 19,588 bytes)  
- [`research/paper/PHASE_3C_1_VERIFICATION_REPORT.md`](PHASE_3C_1_VERIFICATION_REPORT.md) (Preserved unchanged, 38,748 bytes)  
- [`research/paper/PHASE_3C_REFINEMENT_REPORT.md`](PHASE_3C_REFINEMENT_REPORT.md) (Preserved unchanged, 27,345 bytes)  
- [`research/paper/PHASE_3B_CORRECTION_REPORT.md`](PHASE_3B_CORRECTION_REPORT.md) (Preserved unchanged, 15,820 bytes)  
- [`research/paper/PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md`](PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md) (Preserved unchanged, 28,370 bytes)  

---

## 1. Executive Summary

This report documents the completion of **Phase 3C.5: Residual Manuscript Corrections and Final Artifact Verification** for the TrustEval project. Following independent manuscript review, this pass executes targeted residual corrections across statistical reporting, annotator sampling explanations, baseline ranking rules, mathematical error metric terminology, calibration/bias distinctions, memory guard audit findings, and bibliographic citations.

### Strict Methodological Boundaries Maintained:
- **Zero Forward Inference:** No model forward passes, weight downloads, or prompt evaluations were executed.
- **Zero Data Alterations:** All prediction caches (`results/predictions/`), dataset manifests (`data/processed/`), and numerical outputs (`results/tables/`) remain completely unmodified.
- **Zero Value Recalculation or Fabrication:** No experimental numbers were altered, invented, or retrofitted.
- **Preservation of Scope and Archival Integrity:** All prior manuscripts (Draft through V2.5.1) and all audit reports (Phase 2B through Phase 3C.4) were preserved unchanged.
- **Epistemic Modesty:** Completion of this errata and verification pass is documented factually without asserting automatic submission readiness.

---

## 2. Comprehensive Correction and Verification Table

```
Table: Systematic audit of Phase 3C.5 corrections, underlying evidence, and V2.5.2 resolutions.
```

| Correction Focus | V2.5.1 Text / State | Verified Empirical Evidence | V2.5.2 Final Resolution |
| :--- | :--- | :--- | :--- |
| **1. RQ3 Statistical Reporting** | Section 9.1 and Section 12 attached nested in-sample $F$-test to 5-fold cross-validation. Section 7.3 described $\Delta R^2$ as `(+8.05%)` and used "generalization gain". | In-sample nested OLS $F$-test ($F(1, 46) = 5.676, p = 0.0214$) evaluates in-sample variance explanation. Out-of-fold cross-validation shifts $R^2_{\text{OOF}}$ from $0.0298$ to $0.1103$, representing an absolute increase of $+0.0805$ ($8.05$ percentage points). | Abstract, Table 5, Section 7.3, Section 9.1, and Section 12 cleanly separate in-sample $F$-test from cross-validation. Replaced `(+8.05%)` with `an absolute increase of 8.05 percentage points in R²`. Replaced "generalization gain" with `"descriptive out-of-fold improvement on this sample"`. |
| **2. DICES Annotator Terminology & Sampling** | Used "104 demographic raters" in Abstract and Table 6. Section 7.4 stated: `"conversations in DICES-350 share overlapping subsets of human annotators"`. | The dataset pool consists of crowd annotators. Following the authors' post-annotation exclusions (`removed_raters_350`), the **exact same 104 retained annotators rated all 350 conversations**. The data structure is repeated-measures, not overlapping random subsets. | Replaced all instances with `"104 annotators"`. Section 7.4 rewritten to state that because the exact same 104 annotators rated all conversations, annotations share repeated annotator-level variance that cluster bootstrapping resamples over 1,000 iterations holding conversations fixed. |
| **3. Table 3 Highlighting & Baseline Interpretation** | Caption underlined best overall result without explicitly defining the status of the constant reference. Note 4 attributed held-out baseline squared error to `"78% sample class imbalance"`. | The in-sample sample-mean constant reference row evaluates on the same 50 targets without cross-validation ($\text{RMSE} = \sigma_{\text{pop}} = 0.2417$, $\text{MSE} = \sigma^2_{\text{pop}} = 0.0584$). It is an analytical reference excluded from competitive ranking. 78% class imbalance was an informal causal attribution. | Table 3 caption explicitly states that underlining applies to deployable evaluators and held-out baselines, while the constant reference is an analytical, non-held-out benchmark excluded from competitive ranking. Note 4 rewritten using precise sample-prevalence and target-distribution language. |
| **4. Error Metric Terminology** | Section 5.1, Section 6.2, and Section 9.1 collectively referred to MAE, RMSE, and MSE as "Euclidean distance". | MAE is $L_1$ norm (Manhattan distance); MSE is squared Euclidean distance ($L_2^2$); RMSE is Euclidean distance ($L_2$). Grouping all three as "Euclidean distance" is mathematically inaccurate. | Replaced with `"point prediction approximation error"` and `"prediction error metrics"`. Full scan confirms 0 residual mentions of "Euclidean distance". |
| **5. Figure 1 Caption Precision** | Caption claimed Qwen exhibited `"severe overconfidence"` and the ensemble `"restores an ascending calibration curve"`. | Qwen exhibits upward unsafe-risk prediction (predicting hazard where human consensus is low). The ensemble's 6 populated bins reflect broader score dispersion across the scale, not mathematical proof of better calibration. | Figure 1 caption rewritten to describe Qwen's behavior as systematic upward unsafe-risk prediction relative to human consensus, and clarified that the ensemble's 6 decile intervals indicate broader prediction dispersion rather than intrinsic probability calibration. |
| **6. Calibration vs. Mean Prediction Bias** | Abstract Finding 1 and Section 6.2 described Qwen's elevated mean as a `"positive calibration shift (\mu = 0.751 vs. human sample mean 0.338)"`. | The difference between mean model prediction ($0.751$) and human consensus mean ($0.338$) is a **positive mean prediction bias** (location shift in expectation), distinct from decile calibration metrics such as ECE ($0.4128$). | Replaced `"positive calibration shift"` with `"positive mean prediction bias"`, reporting the mean location difference separately from decile miscalibration ($\text{ECE-10} = 0.4128$). |
| **7. SmolLM2 vs. Ensemble MAE Inference** | Described SmolLM2 MAE advantage as significant under $t$-test and sign test, while Wilcoxon non-significance was noted separately. | Paired absolute error differences violate normality (Shapiro-Wilk $W = 0.8776, p = 9.47 \times 10^{-5}$). Significance is method-dependent: significant under $t$-test ($p_{\text{Holm}} = 0.0425$) and sign test ($p_{\text{Holm}} = 0.0026$), but does not survive family-wise correction under Wilcoxon signed-rank ($p_{\text{Holm}} = 0.0843$). | Explicitly characterized the MAE comparison as **inferentially test-sensitive** in Abstract Finding 2 and Section 6.3, preserving all test statistics and Holm-adjusted $p$-values. |
| **8. Memory Guard Audit & Implementation** | Section 4.6 cited `memory_limit_gb: 4.5` as a safety limit without verifying how it was operationalized in code. | Code inspection of `scripts/08_run_50_experiment.py` reveals that `memory_limit_gb: 4.5` was a declarative YAML setting. Runtime safety was enforced dynamically via system available RAM: GC triggered at $<300\text{ MB}$ and $<80\text{ MB}$, and a hard safety abort at $<50\text{ MB}$. | Section 4.6 rewritten to document the actual runtime implementation: dynamic host available RAM polling (`psutil.virtual_memory().available`) and safety abort at $<50\text{ MB}$, noting that `memory_limit_gb: 4.5` served as a declarative planning ceiling. Physical Working Set ($<1.2\text{ GB}$) and private commit ($\approx 2.4\text{ GB}$) preserved. |
| **9. HarmBench Bibliography Record** | Cited title as `HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Safety Evaluation`, pages `35049–35078`. | Official ICML 2024 / PMLR 235 publication record lists title as: `HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal`, pages `35181–35224`. Full 12-author list preserved. | Corrected title to "...and Robust Refusal" and pagination to `35181–35224` in Section 13 references. |
| **10. Full-Manuscript Residual Scan** | Required comprehensive audit across all sections for residual errata. | Programmatic regex and substring scanning across all 1,168 lines of V2.5.2. | Confirmed zero residual instances of forbidden phrases, zero non-printing control characters, exact bibliographic alignment, and intact prior versions. |

---

## 3. Code and Telemetry Audit Details (Requirement 8)

To resolve the operational meaning of `memory_limit_gb: 4.5` in `configs/experiment.yaml`, an exhaustive codebase audit was conducted across all scripts in `D:\Research\TrustEval`.

### 3.1 Script Implementation Analysis
Inspection of `scripts/08_run_50_experiment.py` (lines 140–215) and `src/trusteval/judges/hf_judge.py` confirms the following runtime memory control flow:
1. **Pre-Load Check:**
   ```python
   pre_rss = get_process_memory_mb()
   pre_avail = get_system_available_ram_mb()
   if pre_avail < 300.0:
       logger.warning(f"Low system memory before load ({pre_avail:.1f} MB). Running pre-emptive GC...")
       gc.collect()
   ```
2. **Inference Loop Safety Guard:**
   ```python
   avail_ram = get_system_available_ram_mb()
   if avail_ram < 80.0:
       gc.collect()
       avail_ram = get_system_available_ram_mb()
   if avail_ram < 50.0:
       raise RuntimeError(f"SAFETY ABORT: Available RAM dropped critically to {avail_ram:.1f} MB (< 50 MB).")
   ```
3. **Absence of YAML Key Binding:**
   The parameter `memory_limit_gb: 4.5` appears exclusively in `configs/experiment.yaml` (line 117). Neither `08_run_50_experiment.py` nor `hf_judge.py` binds or enforces this variable as a process RSS ceiling.

### 3.2 Reconciled Telemetry Documentation
- **Declarative vs. Operational:** `memory_limit_gb: 4.5` was a declarative configuration ceiling formulated during early Milestone 2 planning (motivated by the exploratory $1.4 \times 3.42\text{ GB} = 4.79\text{ GB}$ loading overhead estimate).
- **Runtime Enforcement:** Operational safeguarding was enforced dynamically by monitoring system available RAM via `psutil.virtual_memory().available`, with an abort threshold of $50\text{ MB}$.
- **Measured Metrics:**
  - `Qwen2.5-0.5B`: Peak process Working Set $= 952.1\text{ MB}$.
  - `SmolLM2-1.7B`: Peak process Working Set $= 1,189.1\text{ MB}$.
  - Peak private committed bytes (commit charge) during weight loading reached $\approx 2.4\text{ GB}$ before releasing transient allocation buffers.
  - Post-inference release: Process Working Set dropped cleanly to $<258\text{ MB}$.

---

## 4. Full Artifact Verification & Sanity Checks

### 4.1 Binary Control Character Scan
An automated binary scanner evaluated all 78,785 bytes of [`TRUSTEVAL_PAPER_V2_5_2.md`](TRUSTEVAL_PAPER_V2_5_2.md):
- **Command:**
  ```python
  bad_chars = [b for b in raw if b < 32 and b not in (9, 10, 13)]
  ```
- **Output:** `Count of non-printing control characters: 0`
- **Result:** All LaTeX expressions (e.g. `\bar{h}`, `\mu`, `\sigma`, `\Delta`, `\text{...}`) and Markdown tables render cleanly.

### 4.2 Forbidden Phrases Scan
A programmatic case-insensitive scan was executed across all 1,168 lines of V2.5.2:
- `104 demographic raters`: 0 matches found.
- `overlapping subsets`: 0 matches found.
- `euclidean distance`: 0 matches found.
- `severe overconfidence`: 0 matches found.
- `pathological overconfidence`: 0 matches found.
- `positive calibration shift`: 0 matches found.
- `78% sample class imbalance`: 0 matches found.
- `generalization gain`: 0 matches found.
- `restores an ascending calibration curve`: 0 matches found.

### 4.3 Bibliography and In-Text Citation Alignment
Every entry in Section 13 was cross-checked against in-text mentions:
- `Aroyo et al. (2023)`: Cited in Section 2.2, 3.1
- `Basile et al. (2021)`: Cited in Section 2.2
- `Brier (1950)`: Cited in Section 5.1 (two locations), references
- `Davani et al. (2022)`: Cited in Section 2.2
- `Feng et al. (2026)`: Cited in Section 2.4, official ICLR proceedings URL
- `Gordon et al. (2021, 2022)`: Cited in Section 2.2
- `Guo et al. (2017)`: Cited in Section 5.2
- `Kuhn et al. (2023)`: Cited in Section 2.4
- `Lakshminarayanan et al. (2017)`: Cited in Section 1, 2.4
- `Malinin & Gales (2018)`: Cited in Section 2.4
- `Mazeika et al. (2024)`: Cited in Section 2.1, Table 1, official PMLR title and pages 35181–35224
- `Ovadia et al. (2019)`: Cited in Section 1
- `Qian et al. (2026)`: Cited in Section 1, 2.4, Table 1
- `Röttger et al. (2022)`: Cited in Section 2.2
- `Tan et al. (2025)`: Cited in Section 1, 2.1
- `Wang et al. (2024)`: Cited in Section 1, 2.1, Table 1
- `Zhang et al. (2024)`: Cited in Section 2.1
- `Zheng et al. (2023)`: Cited in Section 1, 2.1, Table 1
- `Verga et al. (2024)`: Cited in Section 1, complete 9 authors in Section 13
- `Allal et al. (2025)`: Cited in Section 1, 2.3, 4.1
- `Chiang et al. (2023)`: Cited in Section 1, 2.1
- `Li (2026)`: Cited in Section 2.4
- `Yang et al. (2024)`: Cited in Section 1, 2.3
- `Zhang et al. (2026)`: Cited in Section 1
- `Whose-Safety-Judge Research Team (2024)`: Cited in Section 3.1
- **Result:** Complete 1-to-1 consistency; 0 orphaned references; 0 uncited entries.

---

## 5. Archival Preservation Table

```
Complete Manuscript and Report Archive
```

| File Name | Byte Size | Status | Purpose / Description |
| :--- | :---: | :---: | :--- |
| `TRUSTEVAL_PAPER_V2_5_2.md` | 78,785 | **Created** | Master Research Manuscript (Phase 3C.5) |
| `PHASE_3C_5_FINAL_AUDIT_REPORT.md` | 19,000+ | **Created** | Phase 3C.5 Final Audit & Verification Report |
| `TRUSTEVAL_PAPER_V2_5_1.md` | 76,572 | Preserved | Phase 3C.4 Errata Manuscript |
| `PHASE_3C_4_ERRATA_REPORT.md` | 18,629 | Preserved | Phase 3C.4 Errata Report |
| `TRUSTEVAL_PAPER_V2_5.md` | 73,990 | Preserved | Phase 3C.3 Master Manuscript |
| `PHASE_3C_3_FINAL_AUDIT_REPORT.md` | 17,017 | Preserved | Phase 3C.3 Final Audit Report |
| `TRUSTEVAL_PAPER_V2_4.md` | 70,116 | Preserved | Phase 3C.2 Manuscript |
| `PHASE_3C_2_CORRECTION_REPORT.md` | 19,588 | Preserved | Phase 3C.2 Reconciliation Report |
| `PHASE_3C_1_VERIFICATION_REPORT.md` | 38,748 | Preserved | Phase 3C.1 Verification Report |
| `TRUSTEVAL_PAPER_V2_3.md` | 64,874 | Preserved | Phase 3C Refinement Manuscript |
| `PHASE_3C_REFINEMENT_REPORT.md` | 27,345 | Preserved | Phase 3C Refinement Report |
| `TRUSTEVAL_PAPER_V2_2.md` | 58,840 | Preserved | Phase 3B Manuscript |
| `PHASE_3B_CORRECTION_REPORT.md` | 15,820 | Preserved | Phase 3B Correction Report |
| `TRUSTEVAL_PAPER_V2_1.md` | 57,198 | Preserved | Phase 3A/2.1 Manuscript |
| `PHASE_3A_MANUSCRIPT_QUALITY_AUDIT.md` | 28,370 | Preserved | Phase 3A Quality Audit |
| `TRUSTEVAL_PAPER_V2.md` | 50,850 | Preserved | Phase 2B Revision Manuscript |
| `PHASE_2B_REVISION_REPORT.md` | 13,378 | Preserved | Phase 2B Revision Report |
| `TRUSTEVAL_PAPER_DRAFT.md` | 17,676 | Preserved | Phase 1 Initial Paper Draft |

---

## 6. Disclaimers and Limitations

1. **Exploratory Benchmark Sample:** The evaluation remains based on the fixed-seed simple random sample of $N=50$ conversations without replacement (seed `20261103`) drawn from DICES-350. Statistical power for fine-grained subgroup analyses remains limited.
2. **Pre-Submission Working Paper:** Manuscript V2.5.2 represents a methodologically audited, uninflated working paper. Completion of this errata pass does **not** constitute external peer review or automatic submission readiness.
