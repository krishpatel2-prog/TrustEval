"""Configuration loader and schema validator."""

from pathlib import Path
from typing import Any, Dict
import yaml


def load_experiment_config(config_path: str | Path) -> Dict[str, Any]:
    """Load and validate the YAML experiment configuration.

    Parameters
    ----------
    config_path : str | Path
        Path to the YAML configuration file.

    Returns
    -------
    Dict[str, Any]
        Parsed configuration dictionary.

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist.
    ValueError
        If required configuration sections or keys are missing.
    """
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError(f"Invalid configuration format in {path}: expected dictionary root.")

    # Validate mandatory top-level sections
    required_sections = ["experiment", "dataset", "models", "prompt", "evaluation", "disagreement", "hardware"]
    missing_sections = [s for s in required_sections if s not in config]
    if missing_sections:
        raise ValueError(f"Configuration file missing required sections: {missing_sections}")

    # Validate mandatory dataset keys
    required_dataset_keys = ["raw_file", "filtered_raters_count", "removed_raters", "total_conversations"]
    missing_dataset_keys = [k for k in required_dataset_keys if k not in config["dataset"]]
    if missing_dataset_keys:
        raise ValueError(f"Dataset section missing required keys: {missing_dataset_keys}")

    return config

