"""Synthetic pytest test fixtures for TrustEval data pipeline and utilities."""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_raw_dices_df() -> pd.DataFrame:
    """Create a minimal synthetic raw DICES dataframe mimicking the official schema."""
    # 2 conversations (item_id 1, 2), rated by 4 raters (rater_1, rater_2, rater_bad, rater_3)
    rows = [
        # Item 1: rater_1 (Yes), rater_2 (No), rater_bad (Yes, will be filtered), rater_3 (Unsure)
        {
            "id": 101,
            "rater_id": "rater_1",
            "item_id": 1,
            "context": "USER: What is the weather?\nBOT: It is sunny.",
            "response": "It is sunny.",
            "Q_overall": "Yes",
        },
        {
            "id": 102,
            "rater_id": "rater_2",
            "item_id": 1,
            "context": "USER: What is the weather?\nBOT: It is sunny.",
            "response": "It is sunny.",
            "Q_overall": "No",
        },
        {
            "id": 103,
            "rater_id": "rater_bad",
            "item_id": 1,
            "context": "USER: What is the weather?\nBOT: It is sunny.",
            "response": "It is sunny.",
            "Q_overall": "Yes",
        },
        {
            "id": 104,
            "rater_id": "rater_3",
            "item_id": 1,
            "context": "USER: What is the weather?\nBOT: It is sunny.",
            "response": "It is sunny.",
            "Q_overall": "Unsure",
        },
        # Item 2: rater_1 (No), rater_2 (No), rater_bad (Yes), rater_3 (No)
        {
            "id": 201,
            "rater_id": "rater_1",
            "item_id": 2,
            "context": "USER: Hello\nBOT: Greetings.",
            "response": "Greetings.",
            "Q_overall": "No",
        },
        {
            "id": 202,
            "rater_id": "rater_2",
            "item_id": 2,
            "context": "USER: Hello\nBOT: Greetings.",
            "response": "Greetings.",
            "Q_overall": "No",
        },
        {
            "id": 203,
            "rater_id": "rater_bad",
            "item_id": 2,
            "context": "USER: Hello\nBOT: Greetings.",
            "response": "Greetings.",
            "Q_overall": "Yes",
        },
        {
            "id": 204,
            "rater_id": "rater_3",
            "item_id": 2,
            "context": "USER: Hello\nBOT: Greetings.",
            "response": "Greetings.",
            "Q_overall": "No",
        },
    ]
    return pd.DataFrame(rows)


@pytest.fixture
def sample_config_dict() -> dict:
    """Minimal valid experiment configuration dictionary."""
    return {
        "experiment": {"name": "TestExp", "seed": 42},
        "dataset": {
            "raw_file": "data/raw/test.csv",
            "total_conversations": 2,
            "filtered_raters_count": 3,
            "removed_raters": ["rater_bad"],
        },
        "models": {"primary_candidates": []},
        "prompt": {"id": "P0", "system_message": "test", "template": "{context}\n{response}"},
        "evaluation": {"cv_folds": 2},
        "disagreement": {"primary_metric": "inter_judge_std"},
        "hardware": {"device": "cpu"},
    }

