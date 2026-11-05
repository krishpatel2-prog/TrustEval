"""Ensemble prediction and disagreement aggregation for TrustEval."""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd


def build_two_judge_ensemble(
    qwen_predictions: pd.DataFrame,
    smollm_predictions: pd.DataFrame,
    conversations: Optional[pd.DataFrame] = None,
    human_targets: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """Build equal-weight two-judge ensemble and calculate judge disagreement.

    Parameters
    ----------
    qwen_predictions : pd.DataFrame
        Predictions from Qwen2.5-0.5B-Instruct containing `item_id` and `conditional_p_yes`.
    smollm_predictions : pd.DataFrame
        Predictions from SmolLM2-1.7B-Instruct containing `item_id` and `conditional_p_yes`.
    conversations : Optional[pd.DataFrame], default=None
        Conversation metadata containing `item_id` and response length columns.
    human_targets : Optional[pd.DataFrame], default=None
        Human ground truth targets containing `item_id`, `h_primary`, and `h_sensitivity`.

    Returns
    -------
    pd.DataFrame
        Consolidated dataframe with:
        - `item_id`: conversation identifier
        - `p_qwen`: Qwen2.5 predicted probability of unsafe
        - `p_smollm`: SmolLM2 predicted probability of unsafe
        - `p_ensemble`: Equal-weight average (p_qwen + p_smollm) / 2
        - `disagreement`: Absolute judge difference |p_qwen - p_smollm|
        - metadata and human targets if provided
    """
    q_sub = qwen_predictions[["item_id", "conditional_p_yes"]].rename(
        columns={"conditional_p_yes": "p_qwen"}
    )
    s_sub = smollm_predictions[["item_id", "conditional_p_yes"]].rename(
        columns={"conditional_p_yes": "p_smollm"}
    )

    merged = pd.merge(q_sub, s_sub, on="item_id", how="inner")

    if len(merged) == 0:
        raise ValueError("No common item_id values found between Qwen and SmolLM predictions.")

    merged["p_ensemble"] = 0.5 * (merged["p_qwen"] + merged["p_smollm"])
    merged["disagreement"] = np.abs(merged["p_qwen"] - merged["p_smollm"])

    if conversations is not None:
        keep_cols = [c for c in ["item_id", "response_char_length", "response_word_length"] if c in conversations.columns]
        merged = pd.merge(merged, conversations[keep_cols], on="item_id", how="left")

    if human_targets is not None:
        target_cols = [c for c in ["item_id", "h_primary", "h_sensitivity", "majority_label"] if c in human_targets.columns]
        merged = pd.merge(merged, human_targets[target_cols], on="item_id", how="left")

    return merged.sort_values("item_id").reset_index(drop=True)
