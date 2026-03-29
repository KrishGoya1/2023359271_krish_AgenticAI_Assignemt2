# -*- coding: utf-8 -*-
"""
model.py
========
Lazy Phi-2 model loader.

Call `load_model()` to get a ready-to-use HuggingFacePipeline (`llm`).
Nothing runs on import — the expensive GPU/CPU work happens only when
explicitly requested.
"""

import torch
from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline

from config import MODEL_NAME


def load_model() -> HuggingFacePipeline:
    """
    Load the Phi-2 model and return a LangChain-compatible HuggingFacePipeline.

    Device is selected automatically:
      - CUDA if a GPU is available
      - CPU otherwise (uses float32 to avoid half-precision issues)

    Returns:
        llm (HuggingFacePipeline): Ready-to-invoke LLM wrapper.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Running on: {device.upper()}")

    print("⚙️  Loading config...")
    config = AutoConfig.from_pretrained(MODEL_NAME, trust_remote_code=True)
    config.pad_token_id = 50256

    print("⏳ Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token    = tokenizer.eos_token
    tokenizer.pad_token_id = 50256

    print("⏳ Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        config      = config,
        torch_dtype = torch.float16 if device == "cuda" else torch.float32,
        device_map  = "auto",
        trust_remote_code = True,
    )

    print("⚙️  Building pipeline...")
    hf_pipeline = pipeline(
        "text-generation",
        model              = model,
        tokenizer          = tokenizer,
        max_new_tokens     = 1000,
        temperature        = 0.7,
        do_sample          = True,
        repetition_penalty = 1.2,
        return_full_text   = False,
        pad_token_id       = 50256,
        truncation         = True,
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    print("✅ Phi-2 ready\n")
    return llm
