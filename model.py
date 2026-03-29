# -*- coding: utf-8 -*-
"""
model.py  (openrouter branch)
==============================
Returns a LangChain ChatOpenAI client pointed at OpenRouter.

No GPU, no 5 GB download — just an API key.

Usage:
    from model import load_model
    llm = load_model()          # reads OPENROUTER_API_KEY from .env
    llm = load_model(model="openai/gpt-4o-mini")   # override model
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from config import OPENROUTER_BASE_URL, OPENROUTER_MODEL


def load_model(model: str | None = None) -> ChatOpenAI:
    """
    Build a ChatOpenAI client configured for the OpenRouter API.

    API key is read from the OPENROUTER_API_KEY environment variable
    (or from a .env file in the project root).

    Args:
        model: Optional OpenRouter model slug to override the default
               set in config.py (OPENROUTER_MODEL).

    Returns:
        A LangChain ChatOpenAI instance ready to invoke.

    Raises:
        EnvironmentError: If OPENROUTER_API_KEY is not set.
    """
    load_dotenv()   # load .env if present

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY is not set.\n"
            "Create a .env file with:\n"
            "  OPENROUTER_API_KEY=sk-or-...\n"
            "Or export it in your shell before running."
        )

    chosen_model = model or OPENROUTER_MODEL
    print(f"🤖 Using OpenRouter model: {chosen_model}")

    llm = ChatOpenAI(
        model           = chosen_model,
        openai_api_key  = api_key,
        openai_api_base = OPENROUTER_BASE_URL,
        temperature     = 0.7,
        max_tokens      = 1000,
        # OpenRouter-specific headers for leaderboard attribution (optional)
        default_headers = {
            "HTTP-Referer": "https://github.com/KrishGoya1/2023359271_krish_AgenticAI_Assignemt2",
            "X-Title"     : "ReAct Research Agent",
        },
    )

    print("✅ OpenRouter client ready\n")
    return llm
