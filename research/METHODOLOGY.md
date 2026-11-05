# TrustEval Mathematical Methodology and Evaluation Specifications

**Project:** TrustEval  
**Document Target:** `D:\Research\TrustEval\research\METHODOLOGY.md`  
**Date:** November 2026

---

## 1. Mathematical Notation and Problem Formulation

Let $\mathcal{D} = \{ (c_i, r_i, \mathcal{A}_i) \}_{i=1}^N$ denote a set of $N=350$ conversation evaluation items, where:
* $c_i$ is the conversation context (multi-turn dialog).
* $r_i$ is the chatbot's final response turn.
* $\mathcal{A}_i = \{ a_{i, 1}, a_{i, 2}, \dots, a_{i, K_i} \}$ is the set of human rater judgements on item $i$ after quality filtering ($K_i = 104$).

Each rater annotation $a_{i, k} \in \{ \text{"Yes"}, \text{"No"}, \text{"Unsure"} \}$ represents the rater's assessment of whether response $r_i$ is unsafe under conversational safety guidelines.

Let:
* $Y_i = \sum_{k=1}^{K_i} \mathbb{I}[a_{i, k} = \text{"Yes"}]$ (count of unsafe votes).
* $N_i = \sum_{k=1}^{K_i} \mathbb{I}[a_{i, k} = \text{"No"}]$ (count of safe votes).
* $U_i = \sum_{k=1}^{K_i} \mathbb{I}[a_{i, k} = \text{"Unsure"}]$ (count of unsure votes).

### 1.1 Human Target Definitions
* **Primary Human Proportion ($h_i$):**
  $$h_i = \frac{Y_i}{Y_i + N_i}$$
  where $Y_i + N_i > 0$.
* **Sensitivity Human Proportion ($h'_i$):**
  $$h'_i = \frac{Y_i + 0.5 \cdot U_i}{Y_i + N_i + U_i}$$
* **Binary Majority Consensus ($m_i$):**
  $$m_i = \begin{cases} 1 & \text{if } h_i \ge 0.5 \\ 0 & \text{if } h_i < 0.5 \end{cases}$$

---

## 2. LLM Judge Inference Formulation

Let $\mathcal{M} = \{ M_1, M_2, \dots, M_J \}$ denote the panel of $J$ small open-weight LLM judges ($J=3$).

Given prompt $\mathcal{P}(c_i, r_i)$ formatted via model $M_j$'s native chat template:
1. Model $M_j$ executes a single deterministic forward pass in float32 precision.
2. Logits for next-token candidates $v_{\text{Yes}}$ and $v_{\text{No}}$ are extracted:
   $$l_{j, i, \text{Yes}} = \text{Logit}(M_j, \mathcal{P}(c_i, r_i), v_{\text{Yes}})$$
   $$l_{j, i, \text{No}} = \text{Logit}(M_j, \mathcal{P}(c_i, r_i), v_{\text{No}})$$
3. The raw predicted unsafe probability is computed via binary softmax:
   $$p_{\text{raw}, j, i} = \frac{\exp(l_{j, i, \text{Yes}})}{\exp(l_{j, i, \text{Yes}}) + \exp(l_{j, i, \text{No}})} = \sigma(l_{j, i, \text{Yes}} - l_{j, i, \text{No}})$$
4. Next-token format-following probability mass is tracked:
   $$\Omega_{j, i} = \frac{\exp(l_{j, i, \text{Yes}}) + \exp(l_{j, i, \text{No}})}{\sum_{w \in \mathcal{V}_j} \exp(l_{j, i, w})}$$

---

## 3. Cross-Validation and Out-of-Fold Platt Calibration

To prevent test-set leakage, calibration and baselines are strictly computed out-of-fold.

Let $\mathcal{D}$ be partitioned into $K=5$ disjoint folds $\mathcal{F}_1, \dots, \mathcal{F}_5$, stratified by $m_i$.
For each fold $k \in \{1, \dots, 5\}$:
* $\mathcal{D}_{\text{train}}^{(k)} = \mathcal{D} \setminus \mathcal{F}_k$ ($N_{\text{train}} = 280$)
* $\mathcal{D}_{\text{val}}^{(k)} = \mathcal{F}_k$ ($N_{\text{val}} = 70$)

### 3.1 Platt Scaling
For each judge $j$, we fit a univariate logistic regression on $\mathcal{D}_{\text{train}}^{(k)}$:
$$\text{logit}(p_{\text{cal}, j, i}) = a_{j}^{(k)} \cdot \text{logit}(p_{\text{raw}, j, i}) + b_{j}^{(k)}$$
Objective function with $L_2$ regularization:
$$\min_{a, b} -\sum_{i \in \mathcal{D}_{\text{train}}^{(k)}} \left[ h_i \log(\sigma(a z_{j,i} + b)) + (1 - h_i) \log(1 - \sigma(a z_{j,i} + b)) \right] + \frac{1}{2C} (a^2 + b^2)$$
where $z_{j,i} = \text{logit}(p_{\text{raw}, j, i}) = \log\left(\frac{p_{\text{raw}, j, i}}{1 - p_{\text{raw}, j, i}}\right)$ and $C=1.0$.

Applying parameters $(\hat{a}_j^{(k)}, \hat{b}_j^{(k)})$ to $i \in \mathcal{F}_k$ yields out-of-fold calibrated probabilities $p_{\text{cal}, j, i}^{\text{oof}}$.

### 3.2 Out-of-Fold Baselines
1. **Training Constant Baseline ($c_{\text{train}}^{(k)}$):**
   $$c_{\text{train}}^{(k)} = \frac{1}{|\mathcal{D}_{\text{train}}^{(k)}|} \sum_{i \in \mathcal{D}_{\text{train}}^{(k)}} h_i$$
2. **Training Majority Baseline ($maj_{\text{train}}^{(k)}$):**
   $$maj_{\text{train}}^{(k)} = \mathbb{I}\left[ \frac{1}{|\mathcal{D}_{\text{train}}^{(k)}|} \sum_{i \in \mathcal{D}_{\text{train}}^{(k)}} m_i \ge 0.5 \right]$$

---

## 4. Multi-Judge Ensemble Aggregation

On held-out validation fold items $i \in \mathcal{F}_k$, ensemble predictions are formed:

### 4.1 Calibrated Mean Probability Ensemble (Primary)
$$p_{\text{ens}, i}^{\text{cal}} = \frac{1}{J} \sum_{j=1}^J p_{\text{cal}, j, i}^{\text{oof}}$$

### 4.2 Raw Mean Probability Ensemble
$$p_{\text{ens}, i}^{\text{raw}} = \frac{1}{J} \sum_{j=1}^J p_{\text{raw}, j, i}$$

### 4.3 Hard Majority Voting Ensemble
$$p_{\text{ens}, i}^{\text{vote}} = \mathbb{I}\left[ \sum_{j=1}^J \mathbb{I}[p_{\text{raw}, j, i} \ge 0.5] \ge \left\lceil \frac{J}{2} \right\rceil \right]$$

---

## 5. Evaluation Metrics

For any predictor $p \in [0, 1]^N$ against human target $h \in [0, 1]^N$ and majority label $m \in \{0, 1\}^N$:

1. **Brier Score (Primary Metric):**
   $$\text{Brier}(p, h) = \frac{1}{N} \sum_{i=1}^N (p_i - h_i)^2$$
2. **Mean Absolute Error (MAE):**
   $$\text{MAE}(p, h) = \frac{1}{N} \sum_{i=1}^N |p_i - h_i|$$
3. **Bernoulli Jensen-Shannon Divergence (JSD):**
   $$\text{JSD}(p, h) = \frac{1}{N} \sum_{i=1}^N \left[ H\left(\frac{p_i + h_i}{2}\right) - \frac{H(p_i) + H(h_i)}{2} \right]$$
   where $H(x) = -x \log_2 x - (1-x) \log_2 (1-x)$ in bits.
4. **Spearman Rank Correlation ($\rho$):**
   $$\rho(p, h) = \frac{\text{Cov}(\text{Rank}(p), \text{Rank}(h))}{\sigma_{\text{Rank}(p)} \sigma_{\text{Rank}(h)}}$$
5. **Area Under the ROC Curve (AUROC):**
   $$\text{AUROC}(p, m) = P(p_u > p_s \mid m_u = 1, m_s = 0)$$

---

## 6. Disagreement and Predictive Error Modeling

### 6.1 Disagreement Metrics
For item $i$ evaluated by $J=3$ judges:
* **Continuous Standard Deviation ($D_i$, Primary):**
  $$D_i = \sqrt{\frac{1}{J - 1} \sum_{j=1}^J \left(p_{\text{cal}, j, i}^{\text{oof}} - p_{\text{ens}, i}^{\text{cal}}\right)^2}$$
* **Continuous Interquartile Range ($\text{IQR}_i$):**
  $$\text{IQR}_i = \max_j(p_{\text{cal}, j, i}^{\text{oof}}) - \min_j(p_{\text{cal}, j, i}^{\text{oof}})$$

### 6.2 Ensemble Loss
$$E_i = (p_{\text{ens}, i}^{\text{cal}} - h_i)^2$$

### 6.3 Nested Cross-Validated Regression Analysis
To test whether $D_i$ predicts $E_i$ beyond epistemic proximity to the decision threshold and verbosity:
* **Model 0 (Baseline):**
  $$\hat{E}_i^{(0)} = \gamma_0 + \gamma_1 |p_{\text{ens}, i}^{\text{cal}} - 0.5| + \gamma_2 \text{Length}_i$$
* **Model 1 (Disagreement Extended):**
  $$\hat{E}_i^{(1)} = \beta_0 + \beta_1 |p_{\text{ens}, i}^{\text{cal}} - 0.5| + \beta_2 \text{Length}_i + \beta_3 D_i$$
  where $\text{Length}_i = \text{CharacterCount}(r_i)$.

Incremental predictive performance is quantified strictly out-of-fold:
$$\Delta R^2 = R^2_{\text{Model 1, oof}} - R^2_{\text{Model 0, oof}}$$
$$\Delta \text{MSE} = \text{MSE}_{\text{Model 0, oof}} - \text{MSE}_{\text{Model 1, oof}}$$

---

## 7. Paired Bootstrap Hypothesis Testing & Multiplicity

For any metric $M$ and pair of predictors $(A, B)$:
1. For $b \in \{1, \dots, B\}$ ($B=2,000$, seed `20261103`):
   * Sample item indices $\mathcal{I}_b$ of length $N=350$ with replacement.
   * Evaluate $\Delta M_b = M(p_A[\mathcal{I}_b], h[\mathcal{I}_b]) - M(p_B[\mathcal{I}_b], h[\mathcal{I}_b])$.
2. The empirical 95% bootstrap confidence interval is $[q_{0.025}(\Delta M), q_{0.975}(\Delta M)]$.
3. Two-sided empirical p-values:
   $$p = 2 \cdot \min\left( \frac{1}{B} \sum_{b=1}^B \mathbb{I}[\Delta M_b \ge 0], \frac{1}{B} \sum_{b=1}^B \mathbb{I}[\Delta M_b \le 0] \right)$$
4. Primary comparison family ($k=5$ tests) is adjusted via **Holm-Bonferroni step-down correction**:
   $$p_{(i)}^{\text{Holm}} = \min\left( 1, \max_{j \le i} (k - j + 1) p_{(j)} \right)$$

