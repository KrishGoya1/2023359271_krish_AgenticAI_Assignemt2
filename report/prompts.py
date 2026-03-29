# -*- coding: utf-8 -*-
"""
report/prompts.py
=================
Prompt assembly and LLM response post-processing.

  build_prompt()    — constructs the RTF-structured prompt sent to the model.
  clean_response()  — strips prompt leakage, citations, and stray whitespace.
"""

import re
from config import SYSTEM_PERSONA


# ── Leak / noise patterns ─────────────────────────────────────
# Lines starting with any of these indicate the model echoed its
# prompt back or added unwanted commentary.
_LEAK_PATTERNS = re.compile(
    r'^(instruct|response|task|context|assistant|output|note|here are|here is|'
    r'the following|as a research|as an expert|write only|section content|'
    r'now write|begin your|example output)[:\s]',
    re.IGNORECASE | re.MULTILINE,
)

# Inline citation markers like (1), [2], etc.
_CITATION_PATTERN = re.compile(r'[\(\[]\d+[\)\]]')


def build_prompt(topic: str, instruction: str, context: str) -> str:
    """
    Assemble the final prompt using the RTF (Role → Task → Format) structure.

    The `instruction` string already contains a few-shot example baked in.
    Context is appended as a grounding reference block, capped at 800 chars
    so lengthy passages do not distract the model.

    Args:
        topic:       Research topic string.
        instruction: Section-specific task prompt (may contain {topic}).
        context:     Pre-retrieved web/wiki text for factual grounding.

    Returns:
        Fully assembled prompt string ready to pass to the LLM.
    """
    instruction      = instruction.replace("{topic}", topic)
    context_snippet  = context.strip()[:800]

    return (
        f"### ROLE\n{SYSTEM_PERSONA}\n\n"
        f"### BACKGROUND CONTEXT (use only as factual grounding)\n"
        f"{context_snippet}\n\n"
        f"### TASK\n{instruction}\n\n"
        f"### OUTPUT\n"
        f"(Begin your output immediately below this line. "
        f"No preamble. No title. No explanation.)\n"
    )


def clean_response(raw: str) -> str:
    """
    Remove prompt leakage, citation markers, markdown fences, and stray
    whitespace from a raw LLM response.

    Operates line-by-line so legitimate content is never stripped.

    Args:
        raw: Raw string returned by the LLM.

    Returns:
        Cleaned plain-text string.
    """
    lines   = raw.strip().splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if _LEAK_PATTERNS.match(line):
            continue
        if line.startswith("```") or line == "---":
            continue
        line = _CITATION_PATTERN.sub("", line).strip()
        if line:
            cleaned.append(line)

    return "\n".join(cleaned)
