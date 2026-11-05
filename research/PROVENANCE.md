# Provenance, Citations, and Attribution Record

**Project:** TrustEval  
**Document Target:** `D:\Research\TrustEval\research\PROVENANCE.md`  
**Date:** November 2026

---

## 1. Primary Dataset Provenance

* **Dataset Name:** DICES-350 (Diversity in Conversational AI Evaluation for Safety - 350 adversarial conversations)
* **Official Repository:** `https://github.com/google-research-datasets/dices-dataset`
* **Pinned Release Commit:** `b5596d9edd585361967991a591abc7b11fb1f7a3`
* **Authoring Organization:** Google LLC
* **Licence:** Creative Commons Attribution 4.0 International License (CC BY 4.0).
  * *Permitted Uses:* Sharing, copying, redistributing, adapting, transforming, and building upon the material for any purpose, including commercial and research, with appropriate credit.
* **Attribution Notice:**
  > "DICES Dataset: Diversity in Conversational AI Evaluation for Safety (2023). Lora Aroyo, Alex S. Taylor, Mark Diaz, Christopher M. Homan, Alicia Parrish, Greg Serapio-Garcia, Vinodkumar Prabhakaran, Ding Wang. arXiv:2306.11247."
* **Acquisition Method:** Downloaded directly from Google Research raw GitHub distribution via `scripts/01_fetch_dices.py` with SHA-256 verification. No intermediary copy or third-party cache is utilized.

---

## 2. Reference Repository & Relationship to TrustEval

* **Reference Project:** `whose-safety-judge`
* **Author / Handle:** `excel16061`
* **Repository URL:** `https://github.com/excel16061/whose-safety-judge`
* **Licensing Status:** All Rights Reserved (No root open-source code licence detected in repository).
* **Strict Reuse Boundary:**
  1. *Zero Code Copying:* No source files, classes, or scripts from `whose-safety-judge` are copied, imported, or adapted into `TrustEval`.
  2. *Zero Prediction Reuse:* The cached model predictions (`cache/judge_scores.jsonl`) from the reference repository are strictly ignored. All model inferences in `TrustEval` will be recomputed independently.
  3. *Academic Influence:* `whose-safety-judge` evaluated individual model alignment against DICES distributions and explored demographic splits. `TrustEval` independently conceptualizes and builds a multi-judge ensemble framework, investigating ensemble distribution approximation and inter-judge continuous disagreement as an error predictor.

---

## 3. Academic Literature & Theoretical Foundations

1. **DICES Dataset Formulation:**
   * *Aroyo, L., Taylor, A. S., Diaz, M., Homan, C. M., Parrish, A., Serapio-Garcia, G., Prabhakaran, V., & Wang, D. (2023).* "DICES Dataset: Diversity in Conversational AI Evaluation for Safety." *arXiv preprint arXiv:2306.11247*.
   * *Contribution to TrustEval:* Grounding safety as an empirical rater distribution over adversarial multi-turn conversations rather than a binary ground truth.

2. **Annotation Alignment & Safety Judging:**
   * *Movva, R., Koh, P. W., & Pierson, E. (2024).* "Annotation Alignment: Comparing LLM and Human Annotations of Conversational Safety." *Findings of the Association for Computational Linguistics: EMNLP 2024*, pages 8094–8110.
   * *Contribution to TrustEval:* Benchmarking individual LLMs against human average ratings on DICES-350; highlights that single models fail to capture distributional variance.

3. **Multi-Model Judge Ensembles (Panels / Juries):**
   * *Verga, P., Hofstatter, S., Albalak, A., Su, P. H., Collins, N., & Cohen, W. W. (2024).* "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models." *arXiv preprint arXiv:2404.18796*.
   * *Chan, C. M., Chen, W., Su, Y., Yu, J., Xue, W., Zhang, S., Fu, J., & Liu, Z. (2023).* "ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate." *Proceedings of EMNLP 2023*.
   * *Contribution to TrustEval:* Demonstrates that panels of smaller diverse models mitigate intra-model bias on ranking tasks. TrustEval extends this principle to continuous safety rating distributions.

4. **Pluralistic Alignment:**
   * *Sorensen, T. et al. (2024).* "Position: A Roadmap to Pluralistic Alignment." *Proceedings of the 41st International Conference on Machine Learning (ICML 2024)*.
   * *Contribution to TrustEval:* Formalization of distributional pluralism: evaluating systems based on their calibration to human populations.

5. **Probability Calibration & Platt Scaling:**
   * *Platt, J. (1999).* "Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods." *Advances in Large Margin Classifiers*, 10(3): 61–74.
   * *Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017).* "On Calibration of Modern Neural Networks." *ICML 2017*.
   * *Contribution to TrustEval:* Providing regularized, parametric mapping from uncalibrated model logits to empirical human target proportions within out-of-fold cross-validation.

---

## 4. Independent Implementation Declarations

| Component | Independent TrustEval Implementation | Prior Reference / Provenance |
| :--- | :--- | :--- |
| **Data Ingestion Engine** | `trusteval.data.loader` (SHA-256 verified directly from Google GitHub) | Official DICES-350 GitHub repo |
| **Target Preprocessor** | `trusteval.data.preprocessor` (Filtered proportions & CV folds) | Formulated from DICES schema |
| **Model Inference Backend** | `trusteval.judges.hf_backend` (CPU deterministic next-token extractor) | Hugging Face Transformers API |
| **Calibrator** | `trusteval.analysis.calibration` (Out-of-fold Platt scaling via scikit-learn LogisticRegression) | Platt (1999) |
| **Ensemble Aggregators** | `trusteval.analysis.ensemble` (Calibrated mean & majority voting) | TrustEval original design |
| **Disagreement Modeling** | `trusteval.analysis.disagreement` (Continuous $D_i$ & nested regression) | TrustEval original design |
| **Statistical Resampling** | `trusteval.evaluation.bootstrap` (Paired bootstrap engine + Holm step-down) | Standard non-parametric statistics |

---

## 5. Summary of Excluded Assets

To ensure strict legal and academic separation:
* No code from `D:\Research\whose-safety-judge-main` was imported or adapted.
* No cached inference rows from `whose-safety-judge-main/cache/judge_scores.jsonl` were transferred.
* All experimental runs in TrustEval will be executed from scratch using independent scripts.

