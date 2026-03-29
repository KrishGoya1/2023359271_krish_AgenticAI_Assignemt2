# -*- coding: utf-8 -*-
"""
utils.py
========
General-purpose helpers shared across the project:
  - Text formatting
  - Context combination
  - Legacy cover-page builder (v1 — used in agent footer)
  - Report file saving
"""

import textwrap
from datetime import datetime


def format_text_block(text: str, width: int = 65) -> str:
    """
    Wrap every paragraph in `text` to `width` characters,
    preserving blank lines between paragraphs.
    """
    return "\n".join([
        textwrap.fill(p, width=width, break_long_words=False)
        if p.strip() else ""
        for p in text.split("\n")
    ])


def clean_and_combine(topic: str, web: str, wiki: str, max_chars: int = 1500) -> str:
    """
    Merge Wikipedia and web-search results into a single grounding
    context string, capped at `max_chars` to keep prompts manageable.
    """
    combined = f"{wiki}\n\n{web}"
    return combined[:max_chars]


def create_cover_page(topic: str) -> str:
    """
    Legacy (v1) ASCII cover page — used by the agent execution
    trace block in run_react_agent().
    """
    return f"""
{'='*65}
{'AUTONOMOUS RESEARCH AGENT':^65}
{'Research Report':^65}
{'='*65}

Topic: {topic}
Date : {datetime.now().strftime("%B %d, %Y")}

{'='*65}
"""


def save_report(topic: str, text: str) -> None:
    """
    Write the final report to:
        outputs/{Topic_Name}/{Topic_Name}.txt

    The topic folder is created automatically if it doesn't exist.
    """
    import os
    folder_name = topic.replace(" ", "_")
    output_dir  = os.path.join("outputs", folder_name)
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, folder_name + ".txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(format_text_block(text))
    print(f"💾 Saved: {filepath}")
