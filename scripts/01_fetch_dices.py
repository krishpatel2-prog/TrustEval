"""Standalone script to fetch and verify the official DICES-350 dataset."""

import logging
import sys
from pathlib import Path

# Add src to pythonpath
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from trusteval.utils.config import load_experiment_config
from trusteval.data.loader import download_dices_dataset, verify_file_sha256

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("fetch_dices")


def main():
    config_path = PROJECT_ROOT / "configs" / "experiment.yaml"
    logger.info(f"Loading configuration from {config_path}...")
    config = load_experiment_config(config_path)

    d_cfg = config["dataset"]
    raw_path = PROJECT_ROOT / d_cfg["raw_file"]
    url = d_cfg["url"]
    expected_sha256 = d_cfg["expected_sha256"]

    logger.info(f"Target raw file path: {raw_path}")
    logger.info(f"Official download URL: {url}")
    logger.info(f"Expected SHA-256: {expected_sha256}")

    try:
        downloaded_path = download_dices_dataset(
            output_path=raw_path,
            url=url,
            expected_sha256=expected_sha256,
        )
        logger.info(f"Successfully fetched and verified DICES dataset at: {downloaded_path}")
        return 0
    except Exception as e:
        logger.error(f"Failed to fetch DICES dataset: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

