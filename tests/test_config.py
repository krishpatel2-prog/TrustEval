"""Unit tests for experiment configuration loader."""

from pathlib import Path
import pytest
import yaml

from trusteval.utils.config import load_experiment_config


def test_load_real_experiment_config():
    root = Path(__file__).resolve().parent.parent
    config_path = root / "configs" / "experiment.yaml"

    config = load_experiment_config(config_path)
    assert isinstance(config, dict)
    assert config["experiment"]["name"] == "TrustEval_DICES350_Ensemble_Study"
    assert config["dataset"]["total_conversations"] == 350
    assert config["dataset"]["filtered_raters_count"] == 104
    assert len(config["dataset"]["removed_raters"]) == 19
    assert config["evaluation"]["cv_folds"] == 5


def test_load_config_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_experiment_config(tmp_path / "nonexistent.yaml")


def test_load_config_missing_section(tmp_path):
    invalid_config = {"experiment": {"name": "Test"}}
    cfg_file = tmp_path / "invalid.yaml"
    with open(cfg_file, "w") as f:
        yaml.dump(invalid_config, f)

    with pytest.raises(ValueError, match="Configuration file missing required sections"):
        load_experiment_config(cfg_file)


def test_load_config_missing_dataset_key(tmp_path):
    cfg_data = {
        "experiment": {},
        "dataset": {"raw_file": "path.csv"},
        "models": {},
        "prompt": {},
        "evaluation": {},
        "disagreement": {},
        "hardware": {},
    }
    cfg_file = tmp_path / "missing_dataset_key.yaml"
    with open(cfg_file, "w") as f:
        yaml.dump(cfg_data, f)

    with pytest.raises(ValueError, match="Dataset section missing required keys"):
        load_experiment_config(cfg_file)

