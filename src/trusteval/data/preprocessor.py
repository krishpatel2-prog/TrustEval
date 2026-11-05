"""Data cleaning, quality filtering, human target calculation, and cross-validation splitting."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, KFold

from ..utils.text import calculate_response_length

logger = logging.getLogger(__name__)


def filter_raters(df: pd.DataFrame, removed_rater_ids: List[str]) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Remove raters flagged by the dataset authors for failing quality criteria.

    Parameters
    ----------
    df : pd.DataFrame
        Raw annotations dataframe.
    removed_rater_ids : List[str]
        List of string rater IDs to remove.

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, int]]
        Filtered dataframe and audit metrics dictionary.
    """
    initial_rows = len(df)
    initial_raters = df["rater_id"].nunique()

    # Normalize rater IDs to strings
    removed_set = set(str(r).strip() for r in removed_rater_ids)
    clean_df = df[~df["rater_id"].astype(str).str.strip().isin(removed_set)].copy()

    remaining_rows = len(clean_df)
    remaining_raters = clean_df["rater_id"].nunique()

    audit = {
        "initial_rows": initial_rows,
        "remaining_rows": remaining_rows,
        "initial_raters": initial_raters,
        "removed_raters_count": initial_raters - remaining_raters,
        "remaining_raters": remaining_raters,
    }
    logger.info(f"Rater filtering: {initial_raters} -> {remaining_raters} raters ({initial_rows} -> {remaining_rows} rows).")
    return clean_df, audit


def calculate_human_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-conversation human safety proportions and consensus labels from Q_overall.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered annotations dataframe containing `item_id` and `Q_overall`.

    Returns
    -------
    pd.DataFrame
        Target dataframe indexed by `item_id` with columns:
        - `item_id`: conversation identifier
        - `count_yes`: number of unsafe votes
        - `count_no`: number of safe votes
        - `count_unsure`: number of unsure votes
        - `total_valid_votes`: count_yes + count_no
        - `total_all_votes`: count_yes + count_no + count_unsure
        - `h_primary`: Y / (Y + N)
        - `h_sensitivity`: (Y + 0.5 * U) / (Y + N + U)
        - `majority_label`: 1 if h_primary >= 0.5 else 0
        - `is_tie`: True if h_primary == 0.5
    """
    # Normalize labels: case-insensitive strip
    df_clean = df.copy()
    df_clean["clean_label"] = df_clean["Q_overall"].astype(str).str.strip().str.capitalize()

    # Pivot aggregation
    counts = df_clean.groupby(["item_id", "clean_label"]).size().unstack(fill_value=0)

    # Ensure all three expected columns exist
    for col in ["Yes", "No", "Unsure"]:
        if col not in counts.columns:
            counts[col] = 0

    y = counts["Yes"].astype(float)
    n = counts["No"].astype(float)
    u = counts["Unsure"].astype(float)

    valid_denom = y + n
    all_denom = y + n + u

    # Primary proportion: Y / (Y + N), NaN if valid_denom == 0
    with np.errstate(divide="ignore", invalid="ignore"):
        h_primary = np.where(valid_denom > 0, y / valid_denom, np.nan)
        h_sens = np.where(all_denom > 0, (y + 0.5 * u) / all_denom, np.nan)

    # Majority label: 1 if >= 0.5 else 0 (ties broken towards 1/unsafe)
    majority_label = np.where(h_primary >= 0.5, 1, 0)
    is_tie = np.isclose(h_primary, 0.5)

    targets = pd.DataFrame(
        {
            "item_id": counts.index.astype(int),
            "count_yes": y.astype(int),
            "count_no": n.astype(int),
            "count_unsure": u.astype(int),
            "total_valid_votes": valid_denom.astype(int),
            "total_all_votes": all_denom.astype(int),
            "h_primary": h_primary,
            "h_sensitivity": h_sens,
            "majority_label": majority_label,
            "is_tie": is_tie,
        }
    ).reset_index(drop=True)

    return targets


def build_conversation_table(df: pd.DataFrame) -> pd.DataFrame:
    """Extract deduplicated conversation contexts, final responses, and length covariates.

    Parameters
    ----------
    df : pd.DataFrame
        Annotations dataframe with `item_id`, `context`, and `response`.

    Returns
    -------
    pd.DataFrame
        Deduplicated conversations dataframe sorted by `item_id`.
    """
    # Take the first occurrence per conversation item
    items = df.drop_duplicates(subset=["item_id"])[["item_id", "context", "response"]].copy()
    items["item_id"] = items["item_id"].astype(int)
    items = items.sort_values("item_id").reset_index(drop=True)

    # Calculate independent response length covariates
    items["response_char_length"] = items["response"].apply(
        lambda r: calculate_response_length(r, method="character")
    )
    items["response_word_length"] = items["response"].apply(
        lambda r: calculate_response_length(r, method="word")
    )

    return items


def create_stratified_folds(
    targets_df: pd.DataFrame,
    n_splits: int = 5,
    seed: int = 20261103,
    allow_fallback: bool = False,
) -> pd.DataFrame:
    """Assign deterministic stratified cross-validation fold IDs based on majority label.

    Parameters
    ----------
    targets_df : pd.DataFrame
        Targets dataframe containing `majority_label`.
    n_splits : int, default=5
        Number of cross-validation folds.
    seed : int, default=20261103
        Random seed for reproducibility.
    allow_fallback : bool, default=False
        If True, falls back to unstratified KFold when sample sizes are small (for unit tests).
        In production, must be False to guarantee strict stratification.

    Returns
    -------
    pd.DataFrame
        Targets dataframe with an added `cv_fold` column (0-indexed).

    Raises
    ------
    ValueError
        If class distribution cannot support stratified splitting and allow_fallback is False.
    """
    df = targets_df.copy()
    y = df["majority_label"].to_numpy()
    unique, counts = np.unique(y, return_counts=True)

    if len(counts) < 2 or np.min(counts) < n_splits:
        if allow_fallback:
            logger.warning(
                f"Class count {dict(zip(unique, counts))} is less than n_splits={n_splits}. "
                "allow_fallback=True: falling back to standard KFold for test fixture."
            )
            splitter = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
            split_iter = splitter.split(df)
        else:
            raise ValueError(
                f"Cannot create {n_splits} stratified folds: class counts {dict(zip(unique, counts))} "
                f"have a minimum count ({np.min(counts)}) < n_splits ({n_splits}). "
                "Failing safely in production mode."
            )
    else:
        splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        split_iter = splitter.split(df, y)

    df["cv_fold"] = -1
    for fold_idx, (_, val_idx) in enumerate(split_iter):
        df.loc[val_idx, "cv_fold"] = fold_idx

    return df


def prepare_dices_350(
    raw_df: pd.DataFrame,
    removed_rater_ids: List[str],
    n_splits: int = 5,
    seed: int = 20261103,
    allow_fallback: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, any]]:
    """Complete preprocessing pipeline for DICES-350.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Raw dataset from official CSV.
    removed_rater_ids : List[str]
        List of rater IDs to remove.
    n_splits : int, default=5
        Number of cross-validation folds.
    seed : int, default=20261103
        Random seed.
    allow_fallback : bool, default=False
        Whether to allow KFold fallback if classes are deficient (test fixtures only).

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, Dict[str, any]]
        (conversations_df, targets_df, pipeline_audit)
    """
    filtered_df, audit = filter_raters(raw_df, removed_rater_ids)
    conversations_df = build_conversation_table(filtered_df)
    targets_df = calculate_human_targets(filtered_df)
    targets_df = create_stratified_folds(
        targets_df, n_splits=n_splits, seed=seed, allow_fallback=allow_fallback
    )

    audit["conversations_count"] = len(conversations_df)
    audit["targets_count"] = len(targets_df)
    audit["majority_unsafe_count"] = int(targets_df["majority_label"].sum())
    audit["majority_safe_count"] = int(len(targets_df) - targets_df["majority_label"].sum())
    audit["ties_count"] = int(targets_df["is_tie"].sum())
    audit["mean_h_primary"] = float(targets_df["h_primary"].mean())
    audit["mean_h_sensitivity"] = float(targets_df["h_sensitivity"].mean())

    return conversations_df, targets_df, audit

