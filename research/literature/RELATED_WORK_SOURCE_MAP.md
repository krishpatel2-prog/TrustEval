# TrustEval: Related Work & Literature Source Map

**Project:** TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges  
**Directory:** `D:\Research\TrustEval\research\literature`  
**Date:** November 2026  

---

## 1. Taxonomy of Related Work

The scientific foundation of TrustEval bridges five distinct research domains:
```
                                 ┌─────────────────────────────────────────────────────────┐
                                 │                 TrustEval Architecture                  │
                                 └────────────────────────────┬────────────────────────────┘
                                                              │
         ┌─────────────────────────┬──────────────────────────┼──────────────────────────┬────────────────────────┐
         ▼                         ▼                          ▼                          ▼                        ▼
 1. Human Perspective     2. LLM-as-a-Judge          3. Multi-Judge            4. Calibration &        5. Standardized
    & Disagreement           Foundations &              Ensembles & Juries        Statistical Validity    Safety Benchmarks
    • DICES (NeurIPS 23)     • Zheng et al. (NeurIPS)   • LLM-as-a-Jury (Qian)    • Noisy but Valid       • SafetyBench (ACL)
    • whose-safety-judge     • JudgeBench (ICLR 25)     • Calibrate, Don't         (ICLR 26)              • HarmBench (ICML)
                             • Zhang et al. (2024)        Curate (Li 2026)        • Guo et al. (ICML)
```

---

## 2. Detailed Publication Source Map

### 2.1 Domain 1: Human Perspective Diversity & Subjective Safety

#### 1. DICES: Diversity in Conversational AI Evaluation for Safety
- **Full Title:** DICES: An Open Dataset with Diverse Perspectives on Safety of Large Language Models
- **Authors:** Lora Aroyo, Alex S. Taylor, Mark Diaz, Christopher M. Homan, Alicia Parrish, Gregory Serapio-García, Vinodkumar Prabhakaran, Ding Wang
- **Venue & Year:** NeurIPS 2023 (Track on Datasets and Benchmarks)
- **Identifiers:** arXiv:2306.11247 | DOI: 10.48550/arXiv.2306.11247
- **Research Objective:** Address the limitation of treating content safety as an objective binary ground truth by creating a benchmark capturing diverse human perspectives across demographics.
- **Main Methodology:** Collected dense annotations (60–120 ratings per conversation across 123 demographic raters) on multi-turn adversarial dialogues from chatbot systems (DICES-350 and DICES-990). Introduced group cohesion and association indices.
- **Key Findings:** Significant demographic disagreement exists on polarizing and sensitive topics; aggregating into a single majority label erases minority safety concerns.
- **Relationship to TrustEval:** Serves as the primary empirical ground truth dataset for TrustEval. TrustEval uses DICES-350 with the pre-registered 104-rater clean panel.
- **How TrustEval Differs:** DICES analyzes human rater disagreement. TrustEval investigates whether *small open-weight LLM judges* can approximate these human rating distributions, and whether *machine disagreement* predicts approximation error.

#### 2. Whose Safety Does an LLM Judge Reflect?
- **Full Title / Repository:** Whose Safety Does an LLM Judge Reflect?
- **Authors / Developers:** Anonymous / Excel16061 Research Team
- **Venue & Year:** Open-source benchmark repository (2024–2026) | `https://github.com/excel16061/whose-safety-judge`
- **Research Objective:** Measure whether small open-weight LLMs correlate with the full spread of human safety ratings or systematically align with specific demographic subgroups.
- **Main Methodology:** Evaluates 0.5B to 1.5B parameter models on DICES using 3 fixed prompt variants (P0, P1, P2) and calculates Brier Skill Scores against demographic rater subsets.
- **Key Findings:** Small models suffer from severe miscalibration and position/framing bias; prompt wording alters predicted risk by up to 30%.
- **Relationship to TrustEval:** Functions as the local reference baseline and historical context.
- **How TrustEval Differs:** The reference repository studies demographic alignment of individual models. TrustEval introduces an *independent, reproducible ensemble framework*, evaluates *inter-judge disagreement as an uncertainty proxy*, and applies 5-fold cross-validation and rater-cluster bootstrapping.

---

### 2.2 Domain 2: LLM-as-a-Judge Foundations & Biases

#### 3. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Full Title:** Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **Authors:** Lianmin Zheng, Wei-Lin Chiang, Hao Shen, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica
- **Venue & Year:** NeurIPS 2023 (Oral Presentation)
- **Identifiers:** arXiv:2306.05685 | DOI: 10.48550/arXiv.2306.05685
- **Research Objective:** Formalize the LLM-as-a-judge paradigm and evaluate whether frontier models (e.g., GPT-4) can match human preferences in open-ended conversation evaluation.
- **Main Methodology:** Pairwise and single-answer scoring across 80 multi-turn queries in MT-Bench and 30K crowdsourced battles in Chatbot Arena. Investigates position bias, verbosity bias, and self-enhancement bias.
- **Key Findings:** GPT-4 achieves >80% agreement with human crowd preferences, comparable to human-human agreement, but exhibits systematic position and length biases.
- **Relationship to TrustEval:** Foundational paper for LLM evaluation. TrustEval extends this paradigm from generative preference evaluation to continuous probability scoring for content safety.
- **How TrustEval Differs:** Zheng et al. focus on giant proprietary models (GPT-4) for general conversational quality using discrete wins/losses. TrustEval evaluates *small open-weight models (<2B params)* on *safety risk distributions* extracting exact next-token logits.

#### 4. JudgeBench: A Benchmark for Evaluating LLM-Based Judges
- **Full Title:** JudgeBench: A Benchmark for Evaluating LLM-based Judges
- **Authors:** Sijun Tan, Siyuan Zhuang, Kyle Montgomery, William Y. Tang, Alejandro Cuadron, Chenguang Wang, Raluca Ada Popa, Ion Stoica
- **Venue & Year:** ICLR 2025
- **Identifiers:** arXiv:2410.12781 | DOI: 10.48550/arXiv.2410.12781
- **Research Objective:** Evaluate whether automated judges can evaluate objective correctness in difficult domains (Knowledge, Reasoning, Math, Coding) rather than subjective style.
- **Main Methodology:** Constructs paired responses where one response is demonstrably correct and the other contains subtle, hard-to-detect errors. Evaluates prompt-based judges, fine-tuned judges, and multi-agent judges.
- **Key Findings:** State-of-the-art LLM judges perform near random chance on complex reasoning benchmarks; capability on general generation does not translate to judging accuracy.
- **Relationship to TrustEval:** Highlights the severe intrinsic limitations of LLM judges.
- **How TrustEval Differs:** JudgeBench examines objective factual/logical tasks. TrustEval focuses on safety dilemmas where ground truth is inherently distributed and subjective (human consensus distribution).

#### 5. Can We Trust LLM Judges? A Study of Capability-Dependent Biases
- **Full Title:** Can We Trust LLM Judges: A Study of Capability-Dependent Biases and Multi-Judge Ensemble for Bias Calibration
- **Authors:** Yue Zhang, Zhiheng Xi, Dingnan Jin, Junzhe Ding, Jie Chen, Qi Zhang, Xuanjing Huang
- **Venue & Year:** Preprint / Conference under review (2024–2026)
- **Identifiers:** arXiv:2406.07988
- **Research Objective:** Investigate whether evaluator models exhibit capability-dependent biases toward examinee models and whether multi-judge ensembles can calibrate evaluation.
- **Main Methodology:** Analyzes pairwise judgments across varied model tiers; proposes weighted multi-judge aggregation.
- **Key Findings:** LLM judges systematically favor models of comparable or higher capability; naive majority voting fails if all judges share correlated architectural biases.
- **Relationship to TrustEval:** Directly motivates TrustEval's core premise: combining judges from *independent training lineages* (Alibaba Qwen vs. HuggingFace SmolLM) to disrupt correlated error.
- **How TrustEval Differs:** Zhang et al. focus on pairwise model battles. TrustEval studies absolute probability calibration against human rater distributions and models inter-judge disagreement as an error predictor.

---

### 2.3 Domain 3: Multi-Judge Ensembles & Juries

#### 6. Who Can We Trust? LLM-as-a-Jury for Comparative Assessment
- **Full Title:** Who Can We Trust? LLM-as-a-Jury for Comparative Assessment
- **Authors:** Mengjie Qian, Anna V. G. P. H., Mark Gales
- **Venue & Year:** ICML 2026 / arXiv (2024)
- **Identifiers:** arXiv:2404.18796 | DOI: 10.48550/arXiv.2404.18796
- **Research Objective:** Overcome individual judge unreliability in NLG evaluation by aggregating a panel of judges using an unsupervised probabilistic framework.
- **Main Methodology:** Introduces BT-$\sigma$, an extension of the Bradley-Terry model that estimates a judge-specific discrimination parameter without requiring ground-truth human supervision.
- **Key Findings:** Multi-judge juries consistently outperform single judges; judge reliability parameters correlate with cycle consistency.
- **Relationship to TrustEval:** Validates the superiority of panel/jury aggregation over single-judge evaluation.
- **How TrustEval Differs:** Qian et al. operate in an unsupervised setting for pairwise rankings. TrustEval operates on supervised human rating distributions, extracting calibrated continuous probabilities and modeling disagreement.

#### 7. Calibrate, Don't Curate: Label-Efficient Estimation from Noisy LLM Judges
- **Full Title:** Calibrate, Don't Curate: Label-Efficient Estimation from Noisy LLM Judges
- **Authors:** Yanran Li
- **Venue & Year:** arXiv / Workshop on Reliable Evaluation (2026)
- **Identifiers:** arXiv:2601.08921
- **Research Objective:** Challenge the common practice of discarding weaker/smaller LLM judges ("curation") in favor of keeping a full heterogeneous panel and calibrating them.
- **Main Methodology:** Evaluates panels of varied model sizes; compares pruning weaker models vs. statistical post-hoc calibration on a small labeled validation set.
- **Key Findings:** Weaker judges contain non-redundant, complementary signals; calibrating an ensemble of small models achieves lower cross-entropy than relying solely on a larger single model.
- **Relationship to TrustEval:** Provides theoretical and empirical support for TrustEval's inclusion of sub-2B models (0.5B and 1.7B).
- **How TrustEval Differs:** TrustEval focuses specifically on adversarial safety evaluation on edge hardware, measuring peak RAM and CPU inference latency alongside statistical calibration.

---

### 2.4 Domain 4: Statistical Reliability, Calibration & Uncertainty

#### 8. Noisy but Valid: Robust Statistical Evaluation of LLMs with Imperfect Judges
- **Full Title:** Noisy but Valid: Robust Statistical Evaluation of LLMs with Imperfect Judges
- **Authors:** Chen Feng, Minghe Shen, Ananth Balashankar, Carsten Gerner-Beuerle, Miguel R. D. Rodrigues
- **Venue & Year:** ICLR 2026
- **Identifiers:** arXiv:2510.04322 | OpenReview: ICLR 2026
- **Research Objective:** Provide rigorous finite-sample Type-I error control for safety certification when evaluations are conducted by noisy LLM judges.
- **Main Methodology:** Formulates evaluation as a statistical hypothesis testing problem with imperfect verifiers; uses a small calibration set to bound false positive/negative rates.
- **Key Findings:** Uncalibrated LLM judges lead to invalid safety certifications; bounding judge noise guarantees rigorous safety guarantees.
- **Relationship to TrustEval:** Directly aligns with TrustEval's emphasis on statistical rigor, rater-cluster bootstrapping, and calibration.
- **How TrustEval Differs:** Feng et al. focus on hypothesis testing for thresholded compliance. TrustEval focuses on soft-target distribution approximation ($h_{\text{primary}}$) and disagreement modeling.

#### 9. On Calibration of Modern Neural Networks
- **Full Title:** On Calibration of Modern Neural Networks
- **Authors:** Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger
- **Venue & Year:** ICML 2017
- **Identifiers:** arXiv:1706.04599 | PMLR 70:1321-1330
- **Research Objective:** Demonstrate that modern deep networks, while highly accurate, are severely miscalibrated (overconfident).
- **Main Methodology:** Formulates Expected Calibration Error (ECE), Maximum Calibration Error (MCE), and temperature scaling.
- **Key Findings:** Increased depth and lack of regularization cause overconfidence; simple Platt scaling/temperature scaling effectively restores calibration.
- **Relationship to TrustEval:** Provides the mathematical definition of ECE-10 used throughout TrustEval.
- **How TrustEval Differs:** Guo et al. evaluate ECE on binary/multiclass classification against one-hot labels. TrustEval adapts ECE to continuous human consensus distributions ($h \in [0, 1]$).

---

### 2.5 Domain 5: Standardized Safety Benchmarks

#### 10. SafetyBench: Evaluating the Safety of Large Language Models with Multiple Choice Questions
- **Full Title:** SafetyBench: Evaluating the Safety of Large Language Models with Multiple Choice Questions
- **Authors:** Zhexin Zhang, Leqi Lei, Lindong Wu, Rui Sun, Yongkang Huang, Chongxuan Li, Minlie Huang
- **Venue & Year:** ACL 2024
- **Identifiers:** arXiv:2309.07045 | DOI: 10.18653/v1/2024.acl-long.448
- **Research Objective:** Comprehensive safety benchmarking covering 7 categories (ethics, bias, illegal acts, privacy, physical/mental harm, sensitive topics) across 11,435 questions.
- **Main Methodology:** Multiple-choice question answering to enable zero-shot, objective logit-based safety testing across Chinese and English.
- **Key Findings:** Open-weight models significantly lag behind proprietary models in zero-shot safety awareness; smaller models exhibit high false-positive rates on sensitive topics.
- **Relationship to TrustEval:** Provides taxonomic categorization of conversational harm categories (harmful content, bias, misinformation, policy).
- **How TrustEval Differs:** SafetyBench uses synthetic multiple-choice questions. TrustEval evaluates open-ended multi-turn dialogues with rich, distributed human annotations.

#### 11. HarmBench: A Standardized Evaluation Framework for Automated Red Teaming
- **Full Title:** HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Safety Evaluation
- **Authors:** Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven Basart, Bo Li, David Forsyth, Dan Hendrycks
- **Venue & Year:** ICML 2024
- **Identifiers:** arXiv:2402.04249 | PMLR 235:35049-35078
- **Research Objective:** Provide a standardized, reproducible benchmark for automated red teaming and automated safety evaluation.
- **Main Methodology:** 510 functional harm behaviors evaluated across automated attack algorithms and fine-tuned validation judges.
- **Key Findings:** Standard LLM evaluators are vulnerable to jailbreak artifacts; dedicated safety classifiers are needed for reliable red-teaming.
- **Relationship to TrustEval:** Contextualizes the adversarial prompt distribution present in DICES-350.
- **How TrustEval Differs:** HarmBench evaluates attack success rates on base models. TrustEval evaluates the *reliability and calibration of small models acting as judges* over conversational safety.

---

## 3. Comparison Matrix: TrustEval vs. Literature

| Feature / Dimension | DICES (Aroyo 2023) | LLM-as-a-Judge (Zheng 2023) | LLM Jury (Qian 2024) | JudgeBench (Tan 2025) | WSJ Reference (2024) | **TrustEval (This Work)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Model Size Regime** | N/A (Humans) | 70B+ / Proprietary | 7B–70B | Varied | 0.5B–1.5B | **0.49B & 1.71B (Strictly Sub-2B)** |
| **Target Representation** | Rater Distributions | Binary Wins / 1–10 | Discrete Pairwise | Binary Accuracy | Subset BSS | **Continuous Soft Consensus ($h \in [0, 1]$)** |
| **Ensemble Aggregation** | None | Single Judge | Unsupervised Bradley-Terry | Multi-Agent Debate | Individual Models | **Equal-Weight Logit Synthesis** |
| **Uncertainty Signal** | Human Inter-Rater | None | Judge Variance | None | None | **Inter-Judge Disagreement ($\Delta = \|P_1 - P_2\|$)** |
| **Statistical Validation** | Cohesion Index | None | Permutation Test | Accuracy Split | Bootstrap over items | **Rater-Cluster Bootstrap + 5-Fold CV Regression** |
| **Edge Hardware Feasibility** | N/A | Cloud APIs | GPU Clusters | GPU Clusters | CPU | **Consumer Laptop CPU (8 GB RAM)** |
