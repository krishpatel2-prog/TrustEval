"""Direct downloader and integrity verifier for official DICES datasets."""

import hashlib
import logging
from pathlib import Path
from typing import Optional
import urllib.request
import pandas as pd

logger = logging.getLogger(__name__)

# Official DICES-350 metadata
DICES_350_URL = "https://raw.githubusercontent.com/google-research-datasets/dices-dataset/b5596d9edd585361967991a591abc7b11fb1f7a3/350/diverse_safety_adversarial_dialog_350.csv"
DICES_350_SHA256 = "63cb8620eb04e64957f9e45b1f7cb3d079c4eed8e8b28909f46e0b7038ce4301"

REQUIRED_COLUMNS = [
    "id",
    "rater_id",
    "item_id",
    "context",
    "response",
    "Q_overall",
]


def verify_file_sha256(file_path: Path | str, expected_sha256: str) -> bool:
    """Calculate and compare the SHA-256 checksum of a file.

    Parameters
    ----------
    file_path : Path | str
        Path to the target file.
    expected_sha256 : str
        Hexadecimal representation of the expected SHA-256 digest.

    Returns
    -------
    bool
        True if checksum matches, False otherwise.
    """
    path = Path(file_path)
    if not path.is_file():
        return False

    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)

    computed_sha256 = hasher.hexdigest().lower()
    return computed_sha256 == expected_sha256.lower()


def download_dices_dataset(
    output_path: Path | str,
    url: str = DICES_350_URL,
    expected_sha256: str = DICES_350_SHA256,
    timeout_sec: int = 120,
) -> Path:
    """Download DICES CSV from official source and verify its integrity.

    Parameters
    ----------
    output_path : Path | str
        Destination path on disk.
    url : str, default=DICES_350_URL
        Source URL.
    expected_sha256 : str, default=DICES_350_SHA256
        Expected SHA-256 checksum.
    timeout_sec : int, default=120
        Network socket timeout in seconds.

    Returns
    -------
    Path
        Verified output file path.

    Raises
    ------
    RuntimeError
        If download fails or checksum verification fails.
    """
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if out_file.is_file():
        if verify_file_sha256(out_file, expected_sha256):
            logger.info(f"Verified existing dataset file at {out_file} (SHA-256 match).")
            return out_file
        else:
            logger.warning(f"Existing file at {out_file} has invalid checksum. Re-downloading...")
            out_file.unlink()

    temp_file = out_file.with_suffix(out_file.suffix + ".download")
    try:
        logger.info(f"Downloading DICES dataset from {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "TrustEval-Research-Downloader/1.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as response, open(temp_file, "wb") as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)

        if not verify_file_sha256(temp_file, expected_sha256):
            if temp_file.exists():
                temp_file.unlink()
            raise RuntimeError(
                f"Checksum mismatch for downloaded file from {url}. Expected {expected_sha256}."
            )

        temp_file.rename(out_file)
        logger.info(f"Successfully downloaded and verified DICES dataset at {out_file}.")
        return out_file

    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        raise RuntimeError(f"Failed to download DICES dataset: {e}") from e


def load_raw_dices_csv(file_path: Path | str) -> pd.DataFrame:
    """Load raw DICES CSV into a pandas DataFrame and validate column schema.

    Parameters
    ----------
    file_path : Path | str
        Path to the verified raw CSV.

    Returns
    -------
    pd.DataFrame
        DataFrame with validated columns and types.

    Raises
    ------
    FileNotFoundError
        If file does not exist.
    ValueError
        If required schema columns are missing.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Raw DICES file not found at {path}")

    # Explicit dtype specifications for key identifiers to preserve string rater IDs
    dtypes = {
        "id": "int64",
        "rater_id": "str",
        "item_id": "int64",
        "context": "str",
        "response": "str",
        "Q_overall": "str",
    }

    df = pd.read_csv(path, dtype=dtypes, low_memory=False)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Raw DICES file is missing required columns: {missing}")

    return df

