"""Unit tests for rater filtering, target calculation, and fold stratification."""

import numpy as np
import pandas as pd
import pytest

from trusteval.data.preprocessor import (
    filter_raters,
    calculate_human_targets,
    build_conversation_table,
    create_stratified_folds,
    prepare_dices_350,
)


def test_filter_raters(sample_raw_dices_df):
    clean_df, audit = filter_raters(sample_raw_dices_df, removed_rater_ids=["rater_bad"])

    assert audit["initial_rows"] == 8
    assert audit["remaining_rows"] == 6
    assert audit["initial_raters"] == 4
    assert audit["remaining_raters"] == 3
    assert audit["removed_raters_count"] == 1
    assert "rater_bad" not in clean_df["rater_id"].values


def test_calculate_human_targets(sample_raw_dices_df):
    # Filter first
    clean_df, _ = filter_raters(sample_raw_dices_df, removed_rater_ids=["rater_bad"])
    targets = calculate_human_targets(clean_df)

    assert len(targets) == 2

    # Item 1: rater_1 (Yes), rater_2 (No), rater_3 (Unsure)
    t1 = targets[targets["item_id"] == 1].iloc[0]
    assert t1["count_yes"] == 1
    assert t1["count_no"] == 1
    assert t1["count_unsure"] == 1
    assert t1["total_valid_votes"] == 2
    assert t1["total_all_votes"] == 3
    assert t1["h_primary"] == pytest.approx(0.5)
    assert t1["h_sensitivity"] == pytest.approx(1.5 / 3.0)
    assert t1["majority_label"] == 1
    assert t1["is_tie"] == True

    # Item 2: rater_1 (No), rater_2 (No), rater_3 (No)
    t2 = targets[targets["item_id"] == 2].iloc[0]
    assert t2["count_yes"] == 0
    assert t2["count_no"] == 3
    assert t2["count_unsure"] == 0
    assert t2["total_valid_votes"] == 3
    assert t2["total_all_votes"] == 3
    assert t2["h_primary"] == pytest.approx(0.0)
    assert t2["h_sensitivity"] == pytest.approx(0.0)
    assert t2["majority_label"] == 0
    assert t2["is_tie"] == False


def test_calculate_human_targets_all_unsure():
    # Test edge case: conversation where valid_denom is 0
    df = pd.DataFrame([
        {"item_id": 99, "Q_overall": "Unsure"},
        {"item_id": 99, "Q_overall": "Unsure"},
    ])
    targets = calculate_human_targets(df)
    t = targets.iloc[0]
    assert t["total_valid_votes"] == 0
    assert np.isnan(t["h_primary"])
    assert t["h_sensitivity"] == pytest.approx(0.5)


def test_build_conversation_table(sample_raw_dices_df):
    conv_df = build_conversation_table(sample_raw_dices_df)
    assert len(conv_df) == 2
    assert list(conv_df["item_id"]) == [1, 2]

    # Item 1 response: "It is sunny." (12 chars, 3 words)
    assert conv_df.loc[conv_df["item_id"] == 1, "response_char_length"].iloc[0] == 12
    assert conv_df.loc[conv_df["item_id"] == 1, "response_word_length"].iloc[0] == 3

    # Item 2 response: "Greetings." (10 chars, 1 word)
    assert conv_df.loc[conv_df["item_id"] == 2, "response_char_length"].iloc[0] == 10
    assert conv_df.loc[conv_df["item_id"] == 2, "response_word_length"].iloc[0] == 1


def test_create_stratified_folds():
    # Create 10 synthetic targets with balanced majority labels
    targets = pd.DataFrame({
        "item_id": list(range(10)),
        "majority_label": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    })
    folded = create_stratified_folds(targets, n_splits=2, seed=123)
    assert "cv_fold" in folded.columns
    assert set(folded["cv_fold"].unique()) == {0, 1}
    assert (folded["cv_fold"] == 0).sum() == 5
    assert (folded["cv_fold"] == 1).sum() == 5


def test_create_stratified_folds_fails_in_production_mode():
    # 2 items with 1 member per class cannot form 2 stratified folds without fallback
    targets = pd.DataFrame({
        "item_id": [1, 2],
        "majority_label": [0, 1]
    })
    with pytest.raises(ValueError, match="Cannot create 2 stratified folds"):
        create_stratified_folds(targets, n_splits=2, seed=123, allow_fallback=False)


def test_prepare_dices_350_pipeline(sample_raw_dices_df):
    conv_df, targets_df, audit = prepare_dices_350(
        raw_df=sample_raw_dices_df,
        removed_rater_ids=["rater_bad"],
        n_splits=2,
        seed=42,
        allow_fallback=True,
    )
    assert len(conv_df) == 2
    assert len(targets_df) == 2
    assert audit["remaining_raters"] == 3
    assert audit["conversations_count"] == 2
    assert "cv_fold" in targets_df.columns

