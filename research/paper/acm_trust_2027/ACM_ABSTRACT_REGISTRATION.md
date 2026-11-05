# ACM TRUST 2027 — Abstract Registration Dossier

**Target Conference:** 2027 ACM Conference on Trustworthy and Responsible AI and Computing Systems (ACM TRUST 2027)  
**Location & Dates:** Washington, D.C., USA | March 7–9, 2027 (Hybrid)  
**Submission Portal:** Microsoft CMT (Symposium 5 Track)  
**Project:** TrustEval (`D:\Research\TrustEval`)  
**Workspace:** `research/paper/acm_trust_2027/`  
**Status:** Prepared for Human Author Review & Submission (Stage 1 Complete)

---

## 1. Submission Deadlines & Timing

| Event | Official Time (Pacific Time) | Equivalent India Standard Time (IST) | Action Required |
|---|---|---|---|
| **Abstract Registration** | **November 8, 2026, 11:59 PM PT** | **November 9, 2026, 1:29 PM IST** | Register title, abstract, track, and author metadata on Microsoft CMT. |
| **Full Paper Submission** | **November 15, 2026, 11:59 PM PT** | **November 16, 2026, 1:29 PM IST** | Upload final 9-page anonymous PDF (`main.pdf`) to CMT. |

*Timezone Reference:* Pacific Standard Time (PST) is UTC-8 (Daylight Saving Time ends Nov 1, 2026). Indian Standard Time (IST) is UTC+5:30. Time difference is $+13.5$ hours.

---

## 2. Track & Metadata

- **Selected Symposium / Track:** **Symposium 5: Test and Evaluation, Benchmarking & Assurance**  
  *Scope Justification:* Covers safety benchmarks, empirical assurance, evaluation methodologies, calibration audits, and stress-testing of AI components.
- **Paper Type:** Regular Research Track (Symposium Paper, max 9 pages in ACM `sigconf` format).
- **Review Model:** Double-Blind Peer Review (author identities and institutions omitted).

---

## 3. Paper Title

```
TrustEval: An Empirical Study of Ensemble Reliability in Small Open-Weight LLM Safety Judges
```

---

## 4. Submission Abstract (Word Count: 228 words)

```text
Automated LLM-as-a-judge pipelines are increasingly adopted for conversational safety evaluation, yet deploying massive cloud-hosted proprietary models introduces substantial latency, cost, and data privacy constraints. Compact open-weight language models (<2B parameters) offer an accessible on-premises alternative executable on commodity CPU hardware; however, their probability calibration, reliability, and alignment with continuous human safety consensus remain fundamentally uncharacterized. In this study, we present TrustEval, an exploratory empirical study evaluating sub-2B open-weight safety judges and their ensembling characteristics against continuous human consensus. Using a fixed sample of N=50 multi-turn adversarial dialogues from Google DICES-350 with 104 retained crowd raters per conversation (5,200 total evaluations), we extract conditional next-token unsafe probabilities from Qwen2.5-0.5B-Instruct and SmolLM2-1.7B-Instruct under standardized prompting on commodity CPUs (<1.2 GB RSS).

Our findings demonstrate pronounced single-judge polarization: Qwen exhibits aggressive, risk-averse over-prediction (mean P=0.7509, MAE=0.4152) with strong ranking sensitivity (AUROC=0.7529), while SmolLM2 displays extreme variance compression (mean P=0.2531, MAE=0.1734) clustering near benchmark prevalence. An equal-weight two-judge ensemble reduces Qwen's MAE by 40.6% (0.2464) and achieves the highest correlation with human consensus (r=0.4992, rho=0.5903) while preserving majority discrimination (AUROC=0.7517). However, the ensemble does not universally dominate, remaining systematically overpredicting (ECE_10=0.1639). Furthermore, inter-judge disagreement shows an exploratory linear association with ensemble error (r=0.3125, p=0.0271), though monotonic rank correlation is non-significant (rho=0.2302, p=0.1078) and low disagreement fails to guarantee correctness due to potential shared inductive biases.
```

---

## 5. Keywords & Classification

### ACM CCS Concepts (2012)
- **Computing methodologies $\to$ Natural language processing; Machine learning; Ensemble methods**
- **Security and privacy $\to$ Vulnerability scanners / Risk analysis and management**
- **Human-centered computing $\to$ Collaborative and social computing**

### Author Keywords
```text
LLM-as-a-Judge, Open-Weight Models, Small Language Models, Model Calibration, Ensembling, Safety Evaluation, Disagreement Auditing, Algorithmic Assurance
```

---

## 6. One-Paragraph Contribution Statement (For CMT Form)

```text
TrustEval provides an empirical evaluation of sub-2B parameter open-weight LLMs (Qwen2.5-0.5B and SmolLM2-1.7B) deployed as localized safety judges against continuous, multi-rater human consensus distributions (5,200 crowd ratings across 50 adversarial conversations from Google DICES-350). The study provides four concrete contributions to AI test and assurance: (1) revealing severe single-judge polarization between risk-averse overprediction and conservative variance compression on commodity CPUs; (2) demonstrating that simple equal-weight ensembling partially mitigates single-judge bias and maximizes correlation with human consensus, while documenting where it fails to dominate; (3) empirically characterizing inter-judge disagreement as a candidate uncertainty signal with verified diagnostic boundaries; and (4) establishing that compact sub-2B models are suitable for privacy-preserving research triage rather than unvalidated, autonomous production safety certification.
```

---

## 7. Author Metadata Placeholders (To Confirm Before CMT Registration)

> [!IMPORTANT]
> **Action Required by Authors:** Fill in institutional details and primary contact before CMT registration.

- **Author 1 (Primary Contact):**
  - Name: [Author 1 Name]
  - Email: [Author 1 Institutional Email]
  - Affiliation: [Author 1 Department & Institution]
  - Country: [Country]
- **Author 2:**
  - Name: [Author 2 Name]
  - Email: [Author 2 Institutional Email]
  - Affiliation: [Author 2 Department & Institution]
  - Country: [Country]
- **Corresponding Author:** Author 1
- **ACM Open / APC Status:** Institutional agreement or geographic/hardship waiver to be declared upon acceptance ($0 submission fee).
