"""Unit tests for dataset loading and SHA-256 verification."""

import hashlib
from pathlib import Path
import pytest
import pandas as pd

from trusteval.data.loader import verify_file_sha256, load_raw_dices_csv


def test_verify_file_sha256(tmp_path):
    test_file = tmp_path / "sample.txt"
    content = b"TrustEval verifiable research test content"
    test_file.write_bytes(content)

    expected_sha256 = hashlib.sha256(content).hexdigest()
    assert verify_file_sha256(test_file, expected_sha256) is True
    assert verify_file_sha256(test_file, "0000000000000000000000000000000000000000000000000000000000000000") is False
    assert verify_file_sha256(tmp_path / "nonexistent.txt", expected_sha256) is False


def test_load_raw_dices_csv(tmp_path, sample_raw_dices_df):
    csv_file = tmp_path / "dices_sample.csv"
    sample_raw_dices_df.to_csv(csv_file, index=False)

    loaded_df = load_raw_dices_csv(csv_file)
    assert len(loaded_df) == len(sample_raw_dices_df)
    assert list(loaded_df.columns) == list(sample_raw_dices_df.columns)
    assert loaded_df["rater_id"].dtype == object  # Loaded as string


def test_load_raw_dices_csv_missing_column(tmp_path):
    invalid_df = pd.DataFrame({"id": [1], "context": ["hi"], "response": ["hello"]})
    csv_file = tmp_path / "invalid.csv"
    invalid_df.to_csv(csv_file, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        load_raw_dices_csv(csv_file)


def test_load_raw_dices_csv_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_raw_dices_csv(tmp_path / "missing.csv")

