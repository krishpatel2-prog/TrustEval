"""Hugging Face CPU inference backend for deterministic next-token probability extraction."""

import gc
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from ..utils.text import format_prompt
from .cache import PredictionCache, generate_cache_key

logger = logging.getLogger(__name__)


def get_process_memory_mb() -> float:
    """Return current process resident set size (RSS) memory in megabytes."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def get_system_available_ram_mb() -> float:
    """Return system available memory in megabytes."""
    return psutil.virtual_memory().available / (1024 * 1024)


def calculate_binary_softmax_probabilities(
    logit_yes: float,
    logit_no: float,
    full_logits: np.ndarray,
    yes_token_id: int,
    no_token_id: int,
) -> Dict[str, float]:
    """Calculate full-vocabulary and conditional binary probabilities from raw logits.

    Parameters
    ----------
    logit_yes : float
        Next-token logit for the Yes token.
    logit_no : float
        Next-token logit for the No token.
    full_logits : np.ndarray
        Next-token logits over the entire vocabulary.
    yes_token_id : int
        Vocabulary token ID for Yes.
    no_token_id : int
        Vocabulary token ID for No.

    Returns
    -------
    Dict[str, float]
        Dictionary with:
        - 'logit_yes': raw logit
        - 'logit_no': raw logit
        - 'p_yes_full_vocab': full vocabulary softmax probability
        - 'p_no_full_vocab': full vocabulary softmax probability
        - 'mass_yes_no': sum of Yes and No probabilities in vocabulary
        - 'conditional_p_yes': P(Yes) / (P(Yes) + P(No))
        - 'conditional_p_no': P(No) / (P(Yes) + P(No))
    """
    if np.isnan(logit_yes) or np.isnan(logit_no) or np.isinf(logit_yes) or np.isinf(logit_no):
        raise ValueError(f"Non-finite logits detected: Yes={logit_yes}, No={logit_no}")

    # Full vocabulary softmax
    max_vocab = np.max(full_logits)
    exp_vocab = np.exp(full_logits - max_vocab)
    sum_exp_vocab = np.sum(exp_vocab)

    p_yes_full = float(exp_vocab[yes_token_id] / sum_exp_vocab)
    p_no_full = float(exp_vocab[no_token_id] / sum_exp_vocab)
    mass = p_yes_full + p_no_full

    # Stable binary softmax
    m = max(logit_yes, logit_no)
    ea = np.exp(logit_yes - m)
    eb = np.exp(logit_no - m)
    cond_yes = float(ea / (ea + eb))
    cond_no = float(eb / (ea + eb))

    return {
        "logit_yes": float(logit_yes),
        "logit_no": float(logit_no),
        "p_yes_full_vocab": p_yes_full,
        "p_no_full_vocab": p_no_full,
        "mass_yes_no": mass,
        "conditional_p_yes": cond_yes,
        "conditional_p_no": cond_no,
    }


class HFJudge:
    """Deterministic, CPU-optimized Hugging Face LLM judge."""

    def __init__(
        self,
        model_id: str,
        revision: str = "main",
        threads: int = 4,
        seed: int = 20261103,
        dtype: torch.dtype = torch.bfloat16,
        unsafe_word: str = "Yes",
        safe_word: str = "No",
    ):
        self.model_id = model_id
        self.revision = revision
        self.threads = threads
        self.seed = seed
        self.dtype = dtype
        self.unsafe_word = unsafe_word
        self.safe_word = safe_word

        logger.info(f"Initializing HFJudge: {model_id} (rev: {revision}, dtype: {dtype}, threads: {threads})...")
        t0 = time.time()
        start_ram = get_process_memory_mb()

        # Deterministic PyTorch CPU configuration
        torch.manual_seed(seed)
        torch.set_num_threads(threads)
        torch.use_deterministic_algorithms(True)

        # Ensure Hugging Face cache resides on D: drive where disk space is abundant
        hf_cache_dir = os.environ.get("HF_HOME", "D:/hf_cache")
        os.environ["HF_HOME"] = hf_cache_dir

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            revision=revision,
            cache_dir=hf_cache_dir,
            local_files_only=True,
            use_fast=True,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            revision=revision,
            cache_dir=hf_cache_dir,
            local_files_only=True,
            dtype=self.dtype,
        )
        self.model.eval()

        # Verify next-token candidates
        y_tokens = self.tokenizer.encode(self.unsafe_word, add_special_tokens=False)
        n_tokens = self.tokenizer.encode(self.safe_word, add_special_tokens=False)

        if len(y_tokens) != 1 or len(n_tokens) != 1:
            raise ValueError(
                f"Model {model_id} does not represent Yes/No as single tokens. "
                f"Yes={y_tokens}, No={n_tokens}. Next-token scoring is invalid."
            )

        self.yes_token_id = int(y_tokens[0])
        self.no_token_id = int(n_tokens[0])

        self.load_duration_sec = time.time() - t0
        self.loaded_ram_mb = get_process_memory_mb()
        self.net_ram_increase_mb = self.loaded_ram_mb - start_ram
        logger.info(
            f"Loaded {model_id} in {self.load_duration_sec:.2f}s "
            f"(Process RAM: {self.loaded_ram_mb:.1f} MB, Net increase: {self.net_ram_increase_mb:.1f} MB)."
        )

    def evaluate_conversation(
        self,
        context: str,
        response: str,
        prompt_template: str,
        system_message: str,
    ) -> Dict[str, Any]:
        """Perform a single forward pass and extract Yes/No probabilities.

        Parameters
        ----------
        context : str
            Multi-turn conversation history.
        response : str
            Chatbot final response.
        prompt_template : str
            Template containing `{context}` and `{response}`.
        system_message : str
            System instructions.

        Returns
        -------
        Dict[str, Any]
            Detailed probability extraction and diagnostics dictionary.
        """
        messages = format_prompt(
            template=prompt_template,
            system_message=system_message,
            context=context,
            response=response,
        )

        rendered = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        enc = self.tokenizer(rendered, return_tensors="pt", add_special_tokens=False)
        input_ids = enc["input_ids"]
        n_prompt_tokens = int(input_ids.shape[1])

        t0 = time.time()
        with torch.inference_mode():
            outputs = self.model(input_ids=input_ids)
            last_logits = outputs.logits[0, -1].to(torch.float32).cpu().numpy()
            del outputs
            del enc
            del input_ids

        duration = time.time() - t0

        l_yes = float(last_logits[self.yes_token_id])
        l_no = float(last_logits[self.no_token_id])

        probs = calculate_binary_softmax_probabilities(
            logit_yes=l_yes,
            logit_no=l_no,
            full_logits=last_logits,
            yes_token_id=self.yes_token_id,
            no_token_id=self.no_token_id,
        )

        # Check top predicted token
        top_token_id = int(np.argmax(last_logits))
        top_token_str = self.tokenizer.decode([top_token_id])

        return {
            "n_prompt_tokens": n_prompt_tokens,
            "inference_duration_sec": duration,
            "yes_token_id": self.yes_token_id,
            "no_token_id": self.no_token_id,
            "top_token_id": top_token_id,
            "top_token_text": top_token_str,
            **probs,
        }

    def evaluate_and_cache(
        self,
        item_id: int,
        context: str,
        response: str,
        prompt_template: str,
        system_message: str,
        prompt_version: str,
        prompt_hash: str,
        cache: PredictionCache,
    ) -> Dict[str, Any]:
        """Evaluate a conversation and persist the record if not already cached."""
        scoring_method = "next_token_binary_softmax"
        cache_key = generate_cache_key(
            model_id=self.model_id,
            model_revision=self.revision,
            prompt_hash=prompt_hash,
            item_id=item_id,
            scoring_method=scoring_method,
        )

        existing = cache.get(cache_key)
        if existing is not None:
            return existing

        eval_result = self.evaluate_conversation(
            context=context,
            response=response,
            prompt_template=prompt_template,
            system_message=system_message,
        )

        record = {
            "cache_key": cache_key,
            "item_id": int(item_id),
            "model_id": self.model_id,
            "model_revision": self.revision,
            "tokenizer_id": self.model_id,
            "prompt_version": prompt_version,
            "prompt_hash": prompt_hash,
            "scoring_method": scoring_method,
            "precision": str(self.dtype),
            "status": "success",
            "error_msg": None,
            **eval_result,
        }

        cache.put(record)
        return record

    def unload(self) -> None:
        """Explicitly release model and tokenizer tensors and run garbage collection."""
        logger.info(f"Unloading model {self.model_id} from memory...")
        self.model = None
        self.tokenizer = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info(f"Model unloaded. Remaining process RAM: {get_process_memory_mb():.1f} MB.")

