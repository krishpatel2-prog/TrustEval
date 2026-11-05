"""Unit tests for judge probability calculations, numerical stability, and caching."""

import json
from pathlib import Path
import numpy as np
import pytest

from trusteval.judges.cache import PredictionCache, generate_cache_key
from trusteval.judges.hf_judge import (
    calculate_binary_softmax_probabilities,
    get_process_memory_mb,
    get_system_available_ram_mb,
)


def test_calculate_binary_softmax_probabilities_standard():
    # Vocab size = 5. Token 0: Yes, Token 1: No
    logits = np.array([2.0, 0.0, -1.0, -2.0, -3.0], dtype=float)
    y_id, n_id = 0, 1

    probs = calculate_binary_softmax_probabilities(
        logit_yes=logits[y_id],
        logit_no=logits[n_id],
        full_logits=logits,
        yes_token_id=y_id,
        no_token_id=n_id,
    )

    # Hand-computed:
    # m = max(2, 0) = 2. ea = exp(0) = 1. eb = exp(-2) = 0.135335
    # conditional_p_yes = 1 / (1 + exp(-2)) = 1 / 1.135335 = 0.880797
    expected_cond_yes = 1.0 / (1.0 + np.exp(-2.0))
    expected_cond_no = 1.0 - expected_cond_yes

    assert probs["conditional_p_yes"] == pytest.approx(expected_cond_yes, abs=1e-6)
    assert probs["conditional_p_no"] == pytest.approx(expected_cond_no, abs=1e-6)
    assert probs["conditional_p_yes"] + probs["conditional_p_no"] == pytest.approx(1.0)

    # Full vocab softmax
    exp_all = np.exp(logits - np.max(logits))
    sum_all = np.sum(exp_all)
    assert probs["p_yes_full_vocab"] == pytest.approx(exp_all[0] / sum_all, abs=1e-6)
    assert probs["p_no_full_vocab"] == pytest.approx(exp_all[1] / sum_all, abs=1e-6)
    assert probs["mass_yes_no"] == pytest.approx((exp_all[0] + exp_all[1]) / sum_all, abs=1e-6)


def test_calculate_binary_softmax_extreme_numerical_stability():
    # Test large positive logit (no overflow)
    logits_large = np.array([1000.0, 0.0, 0.0])
    res_large = calculate_binary_softmax_probabilities(1000.0, 0.0, logits_large, 0, 1)
    assert res_large["conditional_p_yes"] == pytest.approx(1.0)
    assert res_large["conditional_p_no"] == pytest.approx(0.0)

    # Test large negative logit
    logits_small = np.array([-1000.0, 0.0, 0.0])
    res_small = calculate_binary_softmax_probabilities(-1000.0, 0.0, logits_small, 0, 1)
    assert res_small["conditional_p_yes"] == pytest.approx(0.0)
    assert res_small["conditional_p_no"] == pytest.approx(1.0)


def test_calculate_binary_softmax_non_finite_rejection():
    logits_nan = np.array([np.nan, 0.0, 1.0])
    with pytest.raises(ValueError, match="Non-finite logits detected"):
        calculate_binary_softmax_probabilities(np.nan, 0.0, logits_nan, 0, 1)

    logits_inf = np.array([np.inf, 0.0, 1.0])
    with pytest.raises(ValueError, match="Non-finite logits detected"):
        calculate_binary_softmax_probabilities(np.inf, 0.0, logits_inf, 0, 1)


def test_generate_cache_key_deterministic():
    k1 = generate_cache_key("Qwen/0.5B", "main", "hash123", 1)
    k2 = generate_cache_key("Qwen/0.5B", "main", "hash123", 1)
    assert k1 == k2

    # Different item
    k3 = generate_cache_key("Qwen/0.5B", "main", "hash123", 2)
    assert k1 != k3

    # Different prompt hash
    k4 = generate_cache_key("Qwen/0.5B", "main", "hash456", 1)
    assert k1 != k4


def test_prediction_cache_persistence_and_deduplication(tmp_path):
    cache_file = tmp_path / "test_cache.jsonl"
    cache = PredictionCache(cache_file)

    rec1 = {
        "cache_key": "key_001",
        "item_id": 1,
        "model_id": "test_model",
        "conditional_p_yes": 0.75,
    }

    assert cache.contains("key_001") is False
    cache.put(rec1)
    assert cache.contains("key_001") is True
    assert len(cache) == 1

    # Reload fresh instance from disk
    cache_reloaded = PredictionCache(cache_file)
    assert len(cache_reloaded) == 1
    assert cache_reloaded.contains("key_001") is True
    retrieved = cache_reloaded.get("key_001")
    assert retrieved["conditional_p_yes"] == 0.75


def test_memory_reporting_utilities():
    rss = get_process_memory_mb()
    avail = get_system_available_ram_mb()

    assert isinstance(rss, float)
    assert rss > 0.0
    assert isinstance(avail, float)
    assert avail > 0.0

