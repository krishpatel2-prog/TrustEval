# TrustEval: Research Gap, Positioning & Defensible Contributions

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\audits`  
**Date:** November 2026  

---

## 1. What Prior Literature Has Established

A rigorous synthesis of prior literature reveals several well-established findings:

1. **Frontier Models as Judges:**  
   Zheng et al. (NeurIPS 2023) demonstrated that frontier closed-weight models (e.g., GPT-4) can achieve high agreement with crowd workers in conversational quality assessment, but suffer from verbosity, position, and self-enhancement biases.
2. **Subjectivity and Disagreement in Human Safety Ratings:**  
   Aroyo et al. (NeurIPS 2023) established via the DICES benchmark that content safety is inherently non-consensus; demographic cohorts diverge substantially on sensitive, polarizing, and ambiguous conversations. Aggregating to binary majority labels discards essential minority safety viewpoints.
3. **Unreliability of Automated Judges on Complex Tasks:**  
   Tan et al. (JudgeBench, ICLR 2025) and Zhang et al. (2024) proved that judging capability does not scale monotonically with parameter size or general generative fluency; LLM evaluators often fail on nuanced, adversarial inputs.
4. **Multi-Model Jury Aggregation:**  
   Qian et al. (ICML 2026) showed that aggregating panels of LLM judges using Bradley-Terry models improves pairwise ranking in NLG, while Li (2026) demonstrated that retaining and calibrating diverse, noisy judges outperforms pruning weaker models.
5. **Demographic Alignment in Small Open LLMs:**  
   The reference repository (`whose-safety-judge`, 2024) observed that small individual models (0.5B to 1.5B parameters) display extreme calibration drift and sensitivity to prompt phrasing when evaluated on DICES demographic splits.

---

## 2. Overlap with Existing Work

TrustEval acknowledges legitimate overlap with prior research:
- **Shared Benchmark Domain:** Like Aroyo et al. (2023) and `whose-safety-judge` (2024), TrustEval evaluates conversational safety on DICES-350.
- **Shared Motivation for Ensembling:** Like Qian et al. (2026) and Zhang et al. (2024), TrustEval recognizes that individual LLM evaluators are too noisy and biased to serve as standalone arbiters.
- **Next-Token Probability Scoring:** Like `whose-safety-judge` and SafetyBench (Zhang et al., 2024), TrustEval bypasses autoregressive decoding stochasticity by extracting next-token logits from normalized binary answer tokens.

---

## 3. What Is Genuinely Novel and Distinct in TrustEval

TrustEval differentiates itself through four distinct design and conceptual choices:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               TrustEval Core Novelties                                 │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │
    ┌──────────────────────────────────────┼──────────────────────────────────────┐
    ▼                                      ▼                                      ▼
1. Continuous Soft-Target              2. Inter-Judge Disagreement            3. Ultra-Low Resource
   Approximation                       as an Error Predictor                  Decentralized CPU Focus
   • Bypasses binary collapse;         • First empirical test of whether      • Strictly sub-2B parameter
     evaluates alignment to              |P1 - P2| predicts ensemble            models (0.49B & 1.71B).
     full human consensus                error via 5-fold CV.                 • Sequential BF16 execution
     proportions (h in [0, 1]).        • Demonstrates +8.05% OOF gain.          on consumer 8 GB RAM laptop.
```

### 3.1 Continuous Soft-Target Alignment on Adversarial Safety
Unlike standard LLM-as-a-judge studies that reduce safety evaluation to discrete binary accuracy or pairwise preference wins, TrustEval evaluates whether small open models can approximate **continuous human rating distributions** ($h_{\text{primary}} \in [0, 1]$). This respects the inherent subjectivity documented by DICES without forcing artificial consensus.

### 3.2 Inter-Judge Disagreement as an Automated Triage Signal (RQ2)
Prior multi-judge studies (e.g., Qian et al., 2026) aggregate votes to maximize point accuracy. TrustEval is the first to systematically investigate whether the **magnitude of divergence between small open models** ($\Delta = |P_{\text{qwen}} - P_{\text{smollm}}|$) serves as an informative predictor of evaluation error against human ground truth. We demonstrate that disagreement correlates significantly with error ($r = 0.3125, p = 0.0271$), providing an empirical foundation for selective escalation to human raters.

### 3.3 Strict Edge/Consumer Hardware Constraints
While frontier evaluation requires cloud clusters or costly API dependencies, TrustEval restricts itself to **sub-2B parameter open-weight models** executed sequentially on consumer laptop CPU hardware with 8 GB RAM. We rigorously quantify process RSS (<1.2 GB), memory release, and CPU latency.

### 3.4 Methodological Exposure of Prevalence-Dominated Metrics
TrustEval's audit demonstrates that standard uncentered error metrics (MAE, RMSE, soft Brier) are heavily distorted by class imbalance on safety benchmarks. We show that a trivial held-out constant baseline beats individual models on soft Brier, establishing that **predictive discrimination (AUROC, Spearman rank correlation $\rho$)** must be reported alongside calibration metrics.

---

## 4. Defensible Contributions Supported by Current Evidence (50 Items)

The current 50-conversation empirical evidence supports five defensible claims:

1. **Hardware Feasibility of Decentralized Safety Auditing:**  
   We prove that sub-2B open-weight LLMs (`Qwen2.5-0.5B` and `SmolLM2-1.7B`) can execute sequential, deterministic probability scoring locally on consumer x86 laptop hardware under 8 GB RAM with stable memory footprints (<1.2 GB peak RSS) and zero data loss.
2. **Empirical Characterization of Architectural Polarization:**  
   Small models from independent lineages exhibit extreme, opposing behavioral profiles: Qwen2.5-0.5B suffers from severe false-alarm overprediction (mean 0.751 vs. human 0.338), whereas SmolLM2-1.7B collapses into a quasi-constant conservative predictor ($\mu = 0.253, \sigma = 0.028$).
3. **Superior Discriminative Ranking of the Ensemble (RQ1):**  
   While SmolLM2 mechanically achieves low Euclidean error due to proximity to the safe-majority prevalence, the Two-Judge Ensemble achieves the **highest ranking correlation of all evaluators** ($r = \mathbf{0.4992}, p = 0.0002$; Spearman $\rho = \mathbf{0.5903}, p = 6.43 \times 10^{-6}$) and achieves an AUROC of **0.7517** (outperforming SmolLM2's 0.6690 by $+0.0827$). The ensemble successfully tempers Qwen's false alarms while preserving its discriminative sensitivity.
4. **Statistical Validation of Disagreement Predictive Power (RQ2):**  
   Inter-judge disagreement is a statistically significant predictor of ensemble absolute error ($r = 0.3125, p = 0.0271$). In a nested regression controlling for ensemble confidence and response length, adding disagreement yields a statistically significant in-sample improvement ($F(1, 46) = 5.6760, p = 0.0214$) and an **out-of-fold generalization gain of $\Delta R^2 = \mathbf{+0.0805}$ in 5-fold cross-validation**.
5. **Robustness Across Consensus Definitions:**  
   Rater-cluster bootstrap resampling (1,000 iterations over 104 demographic raters) and sensitivity analysis incorporating unsure votes ($h_{\text{sensitivity}}$) confirm that relative model rankings and ensemble gains are invariant to rater sampling noise and consensus target definitions.

---

## 5. Claims Requiring Full 350-Item Evaluation (Future Scope)

To maintain scientific integrity, the manuscript must explicitly delimit what the 50-item sample cannot substantiate:

| Claim / Analysis | Status in 50-Item Study | Reason Full 350-Item Run Is Required |
| :--- | :---: | :--- |
| **Fine-Grained Demographic Subgroup Alignment** | Deliberately Excluded | Subdividing 50 conversations into demographic sub-cohorts yields insufficient cell counts per subgroup ($n < 10$). |
| **Fine-Grained 20-Bin Calibration Curves** | Binned into 10 deciles | 50 items populate only 6 deciles for the ensemble. Reliable 20-bin ECE estimation requires the full 350 items. |
| **Spearman Rank Significance for Disagreement** | Non-significant ($\rho = 0.230, p = 0.108$) | While Pearson $r$ is significant ($p = 0.027$), Spearman rank power at $N=50$ is limited. Under $N=350$, an effect size of $\rho \approx 0.23$ achieves $p < 0.0001$. |
| **Nonlinear Disagreement Interactions** | Linear OLS only | Testing polynomial or spline interactions between disagreement and response length requires higher sample degrees of freedom. |

---

## 6. Defensible Research-Gap Statement for the Paper

The revised manuscript should position its contribution as follows:

> *"While prior research has explored multi-LLM juries using frontier models on closed cloud APIs, and analyzed human demographic disagreement on safety benchmarks, the reliability, calibration, and uncertainty characteristics of decentralized, sub-2B parameter open-weight LLM safety judges on consumer hardware remain largely uncharacterized. Furthermore, existing automated evaluation frameworks treat multi-judge disagreement as noise to be resolved through voting, overlooking its potential as an actionable signal of evaluation error.*
>
> *TrustEval addresses this gap by conducting a rigorous empirical study of two structurally independent, sub-2B open-weight safety judges (`Qwen2.5-0.5B` and `SmolLM2-1.7B`) evaluated sequentially on consumer CPU hardware across an unbiased sample of the adversarial DICES-350 benchmark. We demonstrate that while individual small models suffer from either severe overconfidence or low-variance prevalence collapse, an equal-weight ensemble achieves superior discriminative ranking ($r = 0.499, \rho = 0.590, \text{AUROC} = 0.752$). Moreover, we provide cross-validated empirical evidence that inter-judge disagreement functions as an effective, statistically significant surrogate for predictive uncertainty ($\Delta R^2_{\text{OOF}} = +8.05\%$), offering a practical, privacy-preserving mechanism for automated triage and selective human escalation in decentralized AI governance."*
