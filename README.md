# TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: Apache 2.0](https://img.shields.io/badge/Code_License-Apache_2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Compute: CPU-Only](https://img.shields.io/badge/Compute-CPU--only%20(%3C1.2%20GB%20RAM)-orange.svg)]()
[![Tests: Pytest Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

> **Official Research Engineering Repository** for *TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges*.  
> Investigating probability calibration, ranking discrimination, and ensemble uncertainty in compact ($\le 1.7\text{B}$) open-weight language models evaluated against continuous human crowd safety consensus on commodity CPU hardware.

---

## 📌 Executive Summary

Automated LLM-as-a-judge pipelines typically rely on massive, closed-source commercial APIs ($70\text{B}+$ parameters). While capable, this cloud-centric paradigm introduces substantial API latency, recurring financial expenditures, confidentiality constraints under data protection regulations (e.g., GDPR, HIPAA), and lack of access to raw output logits.

**TrustEval** investigates whether **sub-2B parameter open-weight language models**—specifically `Qwen2.5-0.5B-Instruct` (0.49B) and `SmolLM2-1.7B-Instruct` (1.71B)—can serve as localized, deterministic safety evaluators executing entirely on consumer CPUs ($<1.2\text{ GB}$ physical resident set size). Rather than reducing evaluations to artificial binary majority votes, we evaluate model predictions directly against continuous human safety consensus ($h_{\text{primary}} \in [0, 1]$) derived from **104 retained crowd annotators per conversation** ($5,200$ total evaluations) across 50 multi-turn adversarial dialogues from Google DICES-350.

Furthermore, TrustEval evaluates whether **inter-judge disagreement** ($\Delta = |P_{\text{qwen}} - P_{\text{smol}}|$) between architecturally diverse compact models serves as an empirical surrogate signal for ensemble prediction error.

---

## 🔬 Core Empirical Findings

```
                            THE CAPABILITY TRADE-OFF FRONTIER
     AUROC (Higher is Better)
       ▲
  0.76 ┼                          ● Qwen2.5-0.5B (0.415, 0.753)
       │                    ● Ensemble (0.246, 0.752)
  0.72 ┼
       │
  0.68 ┼         ● SmolLM2-1.7B (0.173, 0.669)
       │
  0.64 ┼────────────────────────────────────────────────────────►
      0.15      0.20      0.25      0.30      0.35      0.40   0.45
                         Mean Absolute Error (MAE; Lower is Better)
```

1. **Pronounced Single-Judge Polarization:**
   * **`Qwen2.5-0.5B-Instruct`** acts as an aggressive, risk-averse detector ($\bar{P} = 0.7509, s = 0.1884$). This positive bias incurs high pointwise error ($\text{MAE} = 0.4152, \text{Soft MSE} = 0.2202$), but preserves strong discriminative hazard ordering ($\text{AUROC} = 0.7529, \text{Spearman } \rho = 0.5680$).
   * **`SmolLM2-1.7B-Instruct`** exhibits severe variance compression ($\bar{P} = 0.2531, s = 0.0279$), clustering tightly below sample prevalence. It achieves low absolute error ($\text{MAE} = 0.1734$) primarily through conservative anchoring, with compressed ranking sensitivity ($\text{AUROC} = 0.6690, \rho = 0.3929$).
2. **Empirical Trade-Off Expansion via Ensembling:**
   * An equal-weight two-judge ensemble ($P_{\text{ens}} = \frac{1}{2}(P_{\text{qwen}} + P_{\text{smol}})$) moderates Qwen's bias, cutting MAE by **$40.6\%$** ($0.2464$, $p = 1.04 \times 10^{-7}$) and Soft MSE by **$67.6\%$** ($0.0713$, $p = 2.85 \times 10^{-9}$).
   * The ensemble captures the highest linear and rank correlation with human consensus across all evaluated models ($r = \mathbf{0.4992}, \rho = \mathbf{0.5903}$) while maintaining majority discrimination ($\text{AUROC} = 0.7517$).
3. **No Universal Dominance & Baseline Reality Check:**
   * The ensemble does not dominate across all criteria: SmolLM2 achieves lower sample MAE ($0.1734$), and a naive 5-fold held-out prevalence baseline achieves lower squared error ($\text{Soft MSE} = 0.0602$ vs. ensemble $0.0713$), illustrating how quadratic loss functions strongly reward zero-variance prevalence anchoring.
4. **Inter-Judge Disagreement as an Error Correlate:**
   * Inter-judge disagreement ($\Delta$) exhibits a nominally significant positive association with ensemble absolute error ($r = 0.3125, p = 0.0271$).
   * In nested in-sample OLS regressions controlling for dialogue length and predicted probability, adding $\Delta$ yields a statistically significant incremental variance gain ($F(1, 46) = 5.676, p = 0.0214, \Delta R^2_{\text{in}} = +0.1039$) and an out-of-fold cross-validated increment of $\Delta R^2_{\text{OOF}} = +0.0805$.
   * **Crucial Scientific Limitation:** Low disagreement ($\Delta < 0.20$) does *not* guarantee correctness; small models sharing pretraining heuristics can suffer common failure modes on identical conversational subtleties.

---

## 📊 Consolidated Evaluation Performance Matrix

Evaluated on $N = 50$ multi-turn adversarial dialogues from Google DICES-350 ($5,200$ decisive and unsure crowd ratings):

| Evaluator System | Mean Pred. ($\bar{P} \pm s$) | MAE $\downarrow$ | RMSE $\downarrow$ | Soft MSE $\downarrow$ | $\text{ECE}_{10}$ $\downarrow$ | Pop. Bins | Pearson $r$ | Spearman $\rho$ | AUROC $\uparrow$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Qwen2.5-0.5B-Instruct** | $0.7509 \pm 0.1884$ | $0.4152$ | $0.4693$ | $0.2202$ | $0.4128$ | $8/10$ | $0.4812$ ($p=4.0\times 10^{-4}$) | $0.5680$ ($p=1.7\times 10^{-5}$) | **$0.7529$** |
| **SmolLM2-1.7B-Instruct** | $0.2531 \pm 0.0279$ | **$0.1734$** | $0.2505$ | $0.0628$ | $0.0850$ | $2/10$ | $0.2743$ ($p=0.0539$) | $0.3929$ ($p=0.0048$) | $0.6690$ |
| **Two-Judge Ensemble (Equal-Weight)** | $0.5020 \pm 0.0984$ | $0.2464$ | $0.2669$ | $0.0713$ | $0.1639$ | $6/10$ | **$0.4992$** ($p=2.2\times 10^{-4}$) | **$0.5903$** ($p=6.4\times 10^{-6}$) | $0.7517$ |
| *Prevalence Baseline (5-Fold OOF)* | $0.3398 \pm 0.0144$ | $0.1983$ | **$0.2454$** | **$0.0602$** | $0.0017^*$ | $1/10$ | $-0.2353$ ($p=0.1001$) | $-0.1941$ ($p=0.1769$) | N/A$^\dagger$ |

$^*$Single-bin aggregation artifact across $[0.3, 0.4)$ ($(\bar{p}, \bar{h}) = (0.3398, 0.3381)$); degenerate in-sample constant reference yields $\text{ECE} = 0.0000$.  
$^\dagger$Constant-style prediction within folds; non-ranking baseline. Standard deviations ($s$) denote sample standard deviations ($\text{ddof}=1$; corresponding population values $\sigma$ are $0.1865$, $0.0276$, $0.0975$, and $0.0142$).

---

## 🛠️ Repository Architecture

```
TrustEval/
├── configs/
│   ├── experiment.yaml          # Frozen experimental hyperparameters and paths
│   └── prompts/
│       └── safety_judge_v1.txt  # Standardized TrustEval-R0 zero-shot prompt template
├── data/
│   ├── raw/                     # Raw DICES-350 CSV (fetch script provided)
│   └── processed/
│       ├── dices_50_sample_manifest.json # Immutable 50-conversation sample IDs
│       ├── dices_350_targets.csv         # Computed human consensus targets
│       └── dices_350_conversations.csv   # Structured conversational turns
├── research/
│   ├── PROTOCOL_v1.md           # Pre-experimental research protocol (Nov 3, 2026)
│   ├── METHODOLOGY.md          # Formal mathematical equations and derivations
│   ├── PROVENANCE.md           # Data licensing, source commit hash, and rater audit
│   └── paper/
│       ├── final_full_manuscript/ # Complete 19-page IEEE research paper LaTeX project
│       │   ├── main.tex
│       │   ├── IEEEtran.cls
│       │   ├── references.bib
│       │   ├── sections/
│       │   ├── appendices/
│       │   └── figures/
│       └── acm_trust_2027/        # Retargeted 9-page ACM sigconf submission draft
├── results/
│   ├── tables/
│   │   ├── ensemble_predictions_dices50.csv # Authoritative predictions (50 items)
│   │   ├── evaluation_metrics_dices50.json  # Comprehensive evaluation metrics
│   │   └── disagreement_cv_dices50.json     # OLS regression and 5-fold CV output
│   └── diagnostics/
│       ├── phase_3c_statistical_refinements.json # Paired tests and bootstrap CIs
│       └── predictive_discrimination_audit.json  # Model discrimination metrics
├── scripts/
│   ├── 01_fetch_dices.py        # Automated download from official Google Research repo
│   ├── 02_prepare_data.py       # Rater filtering (104 raters) & target generation
│   ├── 03_benchmark_hardware.py # Hardware memory RSS and throughput profiler
│   ├── 06_evaluate_judges.py    # Zero-shot inference and next-token logit extraction
│   ├── 07_run_analysis_pipeline.py # Metrics calculation and calibration curves
│   ├── 08_run_50_experiment.py  # End-to-end 50-conversation pipeline runner
│   └── 98_compute_phase3c_stats.py # Paired tests, bootstrap, and nested OLS regression
├── src/
│   └── trusteval/
│       ├── data/                # Data loaders, schemas, and preprocessors
│       ├── judges/              # HuggingFace causal LM backend & logit extraction
│       ├── evaluation/          # Metrics, calibration, bootstrap, and ensembling
│       └── utils/               # Native ChatML formatting, logging, and configs
├── tests/                       # Complete pytest unit and regression test suite
├── pyproject.toml               # Modern build configuration
├── requirements.txt             # Pinned library dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Quickstart & Reproduction

### 1. Environment Setup

TrustEval runs entirely on **commodity x86-64 CPUs** without GPU acceleration. Python 3.10+ is required.

```bash
# Clone the repository
git clone https://github.com/krishpatel2-prog/TrustEval.git
cd TrustEval

# Create and activate a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install package in editable development mode
pip install -e .
```

### 2. Run Test Suite

Verify that all unit tests and statistical fixtures pass:

```bash
pytest tests/ -v
```

### 3. Data Acquisition & Rater Filtering

Fetch the official Google DICES-350 corpus (pinned to commit `b5596d9`) and apply the quality exclusion filter (`removed_raters_350` removing 19 anomalous raters):

```bash
# Download raw DICES-350 dataset from Google Research
python scripts/01_fetch_dices.py

# Filter raters (123 -> 104 per conversation) and build continuous targets
python scripts/02_prepare_data.py
```

### 4. Deterministic Model Inference (CPU-Only)

Execute zero-shot next-token logit extraction across the 50 sampled conversations. This runs locally on CPU with peak RAM under $1.2\text{ GB}$:

```bash
# Runs Qwen2.5-0.5B-Instruct and SmolLM2-1.7B-Instruct
python scripts/08_run_50_experiment.py
```

### 5. Reproduce All Statistics & Hypothesis Tests

Recompute the exact performance matrix, parametric $t$-tests, Wilcoxon signed-rank tests, item bootstrap ($B=2,000$), rater-cluster bootstrap ($B=1,000$), and nested disagreement OLS regressions:

```bash
python scripts/98_compute_phase3c_stats.py
```

---

## 💻 Hardware Execution Envelope

Inference is executed strictly on CPU with deterministic causal forward passes:

* **Compute Substrate:** Consumer-grade x86-64 CPU (4 execution threads via `torch.set_num_threads(4)`).
* **Precision & Memory:** Models loaded in `bfloat16` with `float32` logit upcasting on CPU.
* **Peak Resident Set Size (RSS):**
  * `Qwen2.5-0.5B-Instruct`: Net memory footprint $\approx 0.9\text{ GB}$.
  * `SmolLM2-1.7B-Instruct`: Net memory footprint $\approx 1.1\text{ GB}$.
* **Data Sovereignty:** Zero outbound network calls or commercial cloud API dependencies; evaluated transcripts remain within local memory boundaries.

---

## 📄 Academic Research Paper

The complete, unabridged 19-page IEEE double-column manuscript is available in [`research/paper/final_full_manuscript/`](research/paper/final_full_manuscript/):

* **Master Document:** `main.tex`
* **Class File:** `IEEEtran.cls` (v1.8b)
* **All Vector Figures:** `figures/fig1_tradeoff.pdf`, `figures/fig2_architecture.pdf`, `figures/fig3_reliability.pdf`, `figures/fig4_disagreement.pdf`, `figures/fig6_escalation.pdf`.
* **Complete Bibliography:** `references.bib` (31 verified academic entries).
* **Overleaf Ready:** Contains self-contained modular sections and appendices.

---

## 📜 Citation & License

### Benchmark License
* The underlying conversation transcripts and human safety ratings are from the **Google DICES dataset**, released by Google LLC under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.
* The evaluated model weights (`Qwen2.5-0.5B-Instruct` and `SmolLM2-1.7B-Instruct`) are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

### BibTeX Citation
```bibtex
@article{trusteval2026,
  title     = {TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges},
  author    = {Anonymous Author(s)},
  journal   = {IEEE Transactions / Conference Submission},
  year      = {2026},
  url       = {https://github.com/krishpatel2-prog/TrustEval}
}
```
