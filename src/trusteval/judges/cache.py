"""Persistent, deterministic JSONL prediction cache for model inferences."""

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def generate_cache_key(
    model_id: str,
    model_revision: str,
    prompt_hash: str,
    item_id: int,
    scoring_method: str = "next_token_binary_softmax",
) -> str:
    """Generate a deterministic SHA-256 cache key for an inference result.

    Parameters
    ----------
    model_id : str
        Hugging Face model identifier.
    model_revision : str
        Git commit hash or revision string.
    prompt_hash : str
        SHA-256 hash of the rendered prompt template.
    item_id : int
        DICES conversation item identifier.
    scoring_method : str, default="next_token_binary_softmax"
        Scoring algorithm identifier.

    Returns
    -------
    str
        Hexadecimal SHA-256 digest uniquely identifying the evaluation configuration.
    """
    key_payload = json.dumps(
        [
            model_id.strip(),
            model_revision.strip(),
            prompt_hash.strip(),
            int(item_id),
            scoring_method.strip(),
        ],
        sort_keys=True,
    )
    return hashlib.sha256(key_payload.encode("utf-8")).hexdigest()


class PredictionCache:
    """Append-only JSONL cache supporting deterministic resumption and duplicate avoidance."""

    def __init__(self, cache_path: Path | str):
        self.path = Path(cache_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._entries: Dict[str, Dict[str, Any]] = {}
        self._load_existing()

    def _load_existing(self) -> None:
        """Read existing cache entries into memory, validating line integrity."""
        if not self.path.is_file():
            return

        loaded = 0
        corrupt = 0
        with open(self.path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    record = json.loads(clean_line)
                    if "cache_key" in record:
                        self._entries[record["cache_key"]] = record
                        loaded += 1
                except json.JSONDecodeError:
                    corrupt += 1
                    logger.warning(f"Corrupt JSON line {line_no} encountered in {self.path}. Skipping.")

        logger.info(f"Loaded {loaded} cached predictions from {self.path} (corrupt lines: {corrupt}).")

    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a cached prediction by its key."""
        return self._entries.get(cache_key)

    def contains(self, cache_key: str) -> bool:
        """Check if a cache key has already been evaluated."""
        return cache_key in self._entries

    def __contains__(self, cache_key: str) -> bool:
        return cache_key in self._entries

    def put(self, record: Dict[str, Any]) -> None:
        """Append a prediction record to disk and update the in-memory index."""
        if "cache_key" not in record:
            raise ValueError("Record must contain 'cache_key' field.")

        key = record["cache_key"]
        self._entries[key] = record

        # Append immediately to guarantee persistence
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

    def __len__(self) -> int:
        return len(self._entries)

