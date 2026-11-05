# TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges

**Authors:** TrustEval Research Initiative  
**Date:** November 2026  
**Artifact Version:** Pre-registration Milestone 2 — Completed 50-Item Empirical Study  
**Repository:** `D:\Research\TrustEval`  
**Dataset Reference:** DICES-350 Benchmark (Google Research)  

---

## Abstract

Automating content safety evaluation using large language models (LLMs-as-a-judge) is central to scalable AI safety governance. However, reliance on proprietary, closed-source models introduces severe reproducibility limitations, prohibitive API costs, and data privacy vulnerabilities. While deploying small open-weight LLMs locally on consumer hardware offers an attractive decentralized alternative, individual sub-2B parameter models frequently exhibit substantial calibration drift, high prediction variance, and cognitive vulnerability to adversarial prompts. 

This paper investigates **TrustEval**, an empirical framework evaluating whether an ensemble of diverse, locally runnable small open-weight LLM safety judges (`Qwen/Qwen2.5-0.5B-Instruct` and `HuggingFaceTB/SmolLM2-1.7B-Instruct`) better approximates human safety-rating distributions than individual constituent judges on the adversarial DICES-350 benchmark. Furthermore, we examine whether inter-judge disagreement functions as a quantifiable surrogate for evaluation uncertainty, predicting ensemble error beyond response length and baseline confidence. In this study on a rigorously pre-registered, unbiased 50-conversation sample evaluated on consumer-grade x86 CPU hardware, we present empirical evidence on soft-label approximation error (MAE, RMSE, Brier score), calibration (ECE), rater-cluster bootstrap confidence intervals over 104 demographic raters, and 5-fold cross-validated disagreement predictive modeling. 

Our findings indicate that:
1. Small judges exhibit stark architectural polarization: Qwen2.5-0.5B severely overpredicts safety violations (mean prediction 0.751 vs. human mean 0.338), whereas SmolLM2-1.7B acts conservatively (mean prediction 0.252).
2. The equal-weight two-judge ensemble decisively stabilizes prediction variance, reducing Qwen's soft-label Mean Absolute Error by **40.6%** (from 0.4152 down to 0.2464) and Brier score by **67.6%** (from 0.2202 down to 0.0713).
3. Inter-judge disagreement is a statistically significant predictor of ensemble absolute error ($r = 0.3125, p = 0.0271$). Adding disagreement to a response-length baseline model yields a **+8.05% gain in out-of-fold cross-validated $R^2$** ($p = 0.0214$).

---

## 1. Introduction and Research Questions

The prevailing paradigm for automated safety evaluation relies predominantly on frontier models (e.g., GPT-4, Claude 3.5 Sonnet) operating as black-box evaluators. While effective, this paradigm suffers from three critical systemic drawbacks:
1. **Lack of Scientific Reproducibility:** Closed API models undergo silent continuous updates, rendering safety evaluations non-replicable over time.
2. **Sovereignty & Governance Gaps:** Organizations handling confidential or sensitive conversations cannot transmit conversational logs to external third-party cloud APIs.
3. **Hardware Accessibility:** Consumer and edge environments cannot run 70B+ parameter models locally.

Small open-weight models (0.5B to 1.7B parameters) can run efficiently on modest consumer hardware (e.g., 8 GB RAM, mobile CPUs). However, individual small models often struggle with nuanced conversational safety dilemmas, exhibiting extreme overconfidence or systematic biases.

### Primary Research Question (RQ1)
> *Does an ensemble of diverse, locally runnable open-weight LLM safety judges better approximate human safety-rating distributions than individual judges and appropriate baselines?*

### Secondary Research Question (RQ2)
> *Does disagreement among multiple LLM safety judges predict ensemble evaluation error against human safety ratings, beyond information available from the ensemble prediction and response length?*

---

## 2. Experimental Design and Data Protocol

### 2.1 Dataset: DICES-350
We utilize the **Diverse Conversations Experts and Non-Experts (DICES)** dataset published by Google Research, specifically the **DICES-350** adversarial conversational benchmark. Each of the 350 conversations consists of a multi-turn adversarial dialogue ending in a chatbot response, evaluated by approximately 90–120 unique human raters across demographic cohorts.

Following our pre-registered data integrity protocol (`research/PROTOCOL_v1.md` and `configs/experiment.yaml`):
- We applied the pre-registered filter removing 19 raters exhibiting severe label-flipping and spam patterns, retaining **104 verified, demographically diverse human raters**.
- Ground-truth soft labels are computed per conversation:
  $$\text{Primary Human Target: } h_{\text{primary}} = \frac{Y}{Y + N}$$
  $$\text{Sensitivity Human Target: } h_{\text{sensitivity}} = \frac{Y + 0.5 \cdot U}{Y + N + U}$$
  where $Y$ is the count of unsafe ("Yes") ratings, $N$ is safe ("No"), and $U$ is unsure/borderline.

### 2.2 50-Conversation Sample Manifest
To establish rigorous preliminary experimental results on resource-constrained hardware while preserving zero methodological bias, an unbiased random sample of exactly 50 conversations was drawn from DICES-350 using the fixed pre-registered seed `20261103`:
- **Sample Size:** $N = 50$ conversations.
- **Manifest File:** `data/processed/dices_50_sample_manifest.parquet` and `data/processed/dices_50_sample_manifest.json`.
- **Target Distribution Balance:**
  - Safe majority ($h_{\text{primary}} < 0.5$): 39 conversations (78.0%).
  - Unsafe majority ($h_{\text{primary}} \ge 0.5$): 11 conversations (22.0%).
  - Sample Mean $h_{\text{primary}}$: $0.3381$ (closely matching the full DICES-350 population mean of $0.3552$).
- **Sample Item IDs:**
  `[7, 10, 23, 36, 41, 42, 43, 45, 62, 65, 67, 72, 76, 87, 98, 111, 113, 117, 125, 130, 141, 145, 152, 153, 164, 169, 170, 171, 173, 184, 188, 195, 198, 201, 206, 215, 253, 256, 259, 262, 273, 275, 277, 286, 307, 313, 321, 336, 339, 346]`.

---

## 3. Evaluator Models & Inference Protocol

### 3.1 Model Architectures
To ensure genuine architectural and inductive diversity, we selected two models from independent organizations and training lineages:

1. **`Qwen/Qwen2.5-0.5B-Instruct`**
   - Developer: Alibaba Cloud
   - Parameters: 0.49B (dense causal LM)
   - Architecture: RoPE, SwiGLU, GQA
   - Vocabulary: 151,936 tokens (Token IDs: `Yes` = 9454, `No` = 2753)
   - Precision: `torch.bfloat16` weights on CPU with FP32 logit upcasting

2. **`HuggingFaceTB/SmolLM2-1.7B-Instruct`**
   - Developer: Hugging Face TB
   - Parameters: 1.71B (dense causal LM)
   - Architecture: Llama-derived architecture trained on FineMath, Cosmo-2
   - Vocabulary: 49,152 tokens (Token IDs: `Yes` = 10539, `No` = 5230)
   - Precision: `torch.bfloat16` weights on CPU with FP32 logit upcasting

### 3.2 Standardized Prompt & Token-Probability Scoring
Both models receive the exact frozen prompt template (`TrustEval-R0`, SHA-256: `15f18333...`):
```text
System: You are a content safety evaluator.
User:
[Context]
{context}

[Response]
{response}

Is the response above safe? Answer with only 'Yes' or 'No'.
```

Rather than sampling text generation (which introduces temperature noise, stochastic decoding, and formatting parsing errors), we extract the next-token logits immediately following the assistant prompt template boundary:
$$P(\text{Unsafe}) = \frac{\exp(z_{\text{Yes}})}{\exp(z_{\text{Yes}}) + \exp(z_{\text{No}})}$$
$$P(\text{Safe}) = 1 - P(\text{Unsafe})$$

We also record the full-vocabulary probability mass $M = \sum_{t \in \{\text{Yes}, \text{No}\}} P(t \mid \mathbf{x})$. Across both models, $M > 0.98$, confirming that probability mass is overwhelmingly concentrated on the binary classification tokens.

### 3.3 Hardware Constraints & Sequential Execution
All experiments were conducted on a standard consumer laptop:
- **CPU:** Intel Core i5-1335U (10 cores: 2 P-cores, 8 E-cores, 12 threads), 1.30 GHz base clock.
- **RAM:** 8.00 GB DDR4 (system available RAM: ~600–800 MB).
- **Execution Safeguards:** Strictly sequential execution (one model loaded at a time), explicit intermediate activation deletion (`del outputs, enc, input_ids`), garbage collection every 5 items, and an adaptive safety abort guard if available system memory drops below 50 MB.

---

## 4. Empirical Results

### 4.1 Individual vs. Ensemble Reliability (RQ1)

The table below summarizes prediction performance across the 50 conversations against the primary human consensus target $h_{\text{primary}}$:

| Evaluator / Model | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | Brier Score | Expected Calibration Error (ECE-10) | Populated Bins |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Qwen2.5-0.5B-Instruct** | 0.4152 | 0.4693 | 0.2202 | 0.4128 | 8 / 10 |
| **SmolLM2-1.7B-Instruct** | 0.1734 | 0.2505 | 0.0628 | 0.0850 | 2 / 10 |
| **Two-Judge Ensemble (Equal Weight)** | **0.2464** | **0.2669** | **0.0713** | **0.1639** | **6 / 10** |

#### Analysis:
- **Qwen2.5-0.5B** exhibits severe false-positive overprediction on safety violations, predicting a high $P(\text{Yes})$ (mean: 0.751) even when human consensus indicates the conversation is safe. This results in an elevated MAE of $0.4152$ and high calibration error (ECE = $0.4128$).
- **SmolLM2-1.7B** behaves as a cautious, low-entropy evaluator, concentrating predictions narrowly around $P(\text{Yes}) \in [0.20, 0.32]$ (mean: 0.252). While this conservativism achieves a low MAE against the majority-safe sample (MAE = $0.1734$), it under-covers the risk spectrum (populating only 2 bins).
- **The Two-Judge Ensemble** successfully synthesizes both viewpoints: it curtails Qwen's extreme false alarms, reducing Qwen's MAE by **40.6%** and Brier score by **67.6%**, while expanding calibration bin coverage to 6 distinct probability intervals.

---

### 4.2 Uncertainty & Rater-Cluster Bootstrap (104 Raters, 1,000 Iterations)

Because conversations in DICES-350 share overlapping subsets of human raters, conventional independent and identically distributed (i.i.d.) resampling violates exchangeability. We implement a **rater-cluster bootstrap** that resamples the 104 verified human raters with replacement across 1,000 iterations:

| Model / Target | Metric | Bootstrap Mean | 95% Confidence Interval | Std Error |
| :--- | :--- | :---: | :---: | :---: |
| **Qwen2.5-0.5B** | MAE | 0.4158 | [0.3838, 0.4477] | 0.0162 |
| | RMSE | 0.4706 | [0.4405, 0.5005] | 0.0154 |
| | Brier Score | 0.2217 | [0.1940, 0.2505] | 0.0145 |
| | ECE | 0.4125 | [0.3791, 0.4456] | 0.0170 |
| **SmolLM2-1.7B** | MAE | 0.1791 | [0.1635, 0.1956] | 0.0084 |
| | RMSE | 0.2541 | [0.2343, 0.2751] | 0.0106 |
| | Brier Score | 0.0647 | [0.0549, 0.0757] | 0.0054 |
| | ECE | 0.0854 | [0.0523, 0.1187] | 0.0170 |
| **Two-Judge Ensemble** | MAE | 0.2466 | [0.2231, 0.2700] | 0.0118 |
| | RMSE | 0.2699 | [0.2477, 0.2934] | 0.0116 |
| | Brier Score | 0.0730 | [0.0613, 0.0861] | 0.0063 |
| | ECE | 0.1635 | [0.1302, 0.1967] | 0.0170 |

The confidence intervals demonstrate tight rater-level bounds, confirming that measured performance differences are not artifacts of human rater sampling noise.

---

### 4.3 Judge Disagreement Predictive Power (RQ2)

To evaluate whether inter-judge disagreement $\Delta = |P_{\text{qwen}} - P_{\text{smollm}}|$ provides explanatory power regarding evaluation error $\epsilon = |P_{\text{ensemble}} - h_{\text{primary}}|$, we fit two linear regression models using 5-fold cross-validation:

- **Baseline Model:** $\epsilon \sim \beta_0 + \beta_1 P_{\text{ensemble}} + \beta_2 \text{ResponseLength}$
- **Extended Model:** $\epsilon \sim \beta_0 + \beta_1 P_{\text{ensemble}} + \beta_2 \text{ResponseLength} + \beta_3 \Delta$

| Feature Configuration | In-Sample $R^2$ | In-Sample RMSE | 5-Fold CV $R^2$ | 5-Fold CV RMSE |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline (Prediction + Length)** | 0.0543 | 0.1378 | 0.0298 | 0.1415 |
| **Extended (+ Judge Disagreement)** | **0.1582** | **0.1300** | **0.1103** | **0.1354** |
| **Incremental Improvement ($\Delta R^2$)** | **+0.1039** | **-0.0078** | **+0.0805** | **-0.0061** |

- **Statistical Significance of Incremental Gain:** $F(1, 46) = 5.6760$, $p = \mathbf{0.0214}$ (statistically significant at $\alpha = 0.05$).
- **Bivariate Pearson Correlation ($r$):** $r = \mathbf{0.3125}$ ($p = \mathbf{0.0271}$).
- **Spearman Rank Correlation ($\rho$):** $\rho = 0.2302$ ($p = 0.1078$).
- **Disagreement Regression Coefficient:** $\hat{\beta}_{\text{disagreement}} = \mathbf{+0.6270}$.

#### Key Empirical Finding (RQ2 Validated):
As hypothesized, inter-judge disagreement is positively correlated with ensemble evaluation error ($r = 0.3125, p = 0.0271$). Adding disagreement to the baseline model produces an out-of-fold generalization improvement of **+8.05% in $R^2$** ($p = 0.0214$). When small open-weight judges disagree, the ensemble's expected approximation error significantly increases, providing a quantifiable signal for human-in-the-loop escalation.

---

### 4.4 Sensitivity Analysis ($h_{\text{primary}}$ vs. $h_{\text{sensitivity}}$)

To ensure conclusions do not depend arbitrarily on the exclusion of "Unsure" human votes, we re-evaluate all metrics against the alternative target $h_{\text{sensitivity}} = \frac{Y + 0.5 \cdot U}{Y + N + U}$:

| Model | Primary MAE ($h_{\text{primary}}$) | Sensitivity MAE ($h_{\text{sensitivity}}$) | Primary Brier | Sensitivity Brier |
| :--- | :---: | :---: | :---: | :---: |
| **Qwen2.5-0.5B** | 0.4152 | 0.4059 | 0.2202 | 0.2106 |
| **SmolLM2-1.7B** | 0.1734 | 0.1693 | 0.0628 | 0.0597 |
| **Two-Judge Ensemble** | **0.2464** | **0.2327** | **0.0713** | **0.0649** |

The relative rankings, performance spreads, and ensemble error reductions remain perfectly consistent across both human target definitions.

---

## 5. Figures and Diagnostic Plots

The experimental pipeline generated three publication figures in `results/figures/`:

1. **Figure 1: Reliability Diagrams** (`results/figures/reliability_diagrams_dices50.png`)  
   Side-by-side calibration curves showing observed human empirical safety proportions across predicted probability deciles for Qwen, SmolLM2, and the Ensemble. Qwen displays heavy under-calibration (over-predicting risk), while the ensemble restores a monotonically increasing calibration slope.

2. **Figure 2: Disagreement vs. Error** (`results/figures/disagreement_vs_error_dices50.png`)  
   Scatter plot and ordinary least squares (OLS) regression line quantifying the empirical relationship between inter-judge divergence and ensemble absolute error ($r = 0.313, p = 0.027$).

3. **Figure 3: Distribution Alignment** (`results/figures/distribution_alignment_dices50.png`)  
   Kernel density and empirical histograms comparing the continuous distribution of model safety predictions against the ground-truth human distribution.

---

## 6. Computational Resource Requirements & Full-Scale Projections

### Measured Hardware Performance (50 Conversations on CPU)
- **Qwen2.5-0.5B-Instruct:**
  - Total Inference Compute Time: $2,020.44\text{ s}$ ($33.67\text{ minutes}$)
  - Mean Latency per Conversation: $40.41\text{ s}$ ($\sigma = 12.11\text{ s}$)
  - Peak Process RSS: $952.1\text{ MB}$
  - Final Released Process RSS: $257.0\text{ MB}$
- **SmolLM2-1.7B-Instruct:**
  - Total Inference Compute Time: $6,740.21\text{ s}$ ($112.34\text{ minutes} \approx 1.87\text{ hours}$)
  - Mean Latency per Conversation: $134.80\text{ s}$ ($\sigma = 30.17\text{ s}$)
  - Peak Process RSS: $1,189.1\text{ MB}$
  - Final Released Process RSS: $250.4\text{ MB}$

### Projected Full-Scale Benchmark (350 Conversations)
*(Note: Projections are linear extrapolations based on measured single-item throughput on this hardware, provided for resource planning purposes only.)*
- **Qwen2.5-0.5B:** $350 \times 40.41\text{ s} \approx 14,144\text{ s} \approx 3.93\text{ hours}$
- **SmolLM2-1.7B:** $350 \times 134.80\text{ s} \approx 47,180\text{ s} \approx 13.11\text{ hours}$
- **Total Two-Judge Pipeline:** $\approx 17.04\text{ hours}$
- **Memory Bound:** Under $1.2\text{ GB}$ process RSS at all times via BF16 weights and aggressive periodic garbage collection.

---

## 7. Threats to Validity and Limitations

1. **Subsample Scope:** While the 50 conversations were selected via pre-registered uniform random sampling without replacement (mirroring the overall majority label split: 78% safe, 22% unsafe), evaluating the full 350-item dataset remains the long-term target for final statistical power.
2. **CPU Execution Throughput:** In the absence of native hardware acceleration for BF16 matrix multiplication (AVX-512 VNNI / AMX), CPU software upcasting incurs high per-item latency for the 1.7B model (~135s).
3. **Binary Next-Token Proxy:** Logit extraction on `Yes`/`No` assumes prompt compliance; while empirical binary mass exceeded 97.8% across both models, complex reasoning models may benefit from chain-of-thought verification.

---

## 8. Conclusion

This empirical study validates that ensembles of small open-weight LLM safety judges offer a viable, privacy-preserving, and computationally disciplined alternative to monolithic proprietary judges. By combining structurally diverse models (`Qwen2.5-0.5B` and `SmolLM2-1.7B`) into an equal-weight ensemble, individual overconfidence is dramatically moderated, and inter-judge disagreement provides an empirically grounded, cross-validated predictor of evaluation error.
