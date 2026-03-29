# -*- coding: utf-8 -*-
"""
report/prompts.py
=================
Prompt assembly and LLM response post-processing.

  build_prompt()    — constructs the RTF-structured prompt (used by fallback path).
  clean_response()  — strips prompt leakage, artifacts, and stray whitespace.
"""

import re
from config import SYSTEM_PERSONA


# ── Leak / noise patterns ─────────────────────────────────────
# Matches lines that indicate the model echoed the prompt or added commentary.
_LEAK_PATTERNS = re.compile(
    r'^(instruct|response|task|context|assistant|output|note|here are|here is|'
    r'the following|as a research|as an expert|write only|section content|'
    r'now write|begin your|example output|sure[,!]?|certainly[,!]?|'
    r'of course[,!]?|i will|i\'ll|i\'d be)[:\s]',
    re.IGNORECASE | re.MULTILINE,
)

# "Sentence_N:" style labels (model echoing our prompt template)
_SENTENCE_LABEL = re.compile(r'^sentence[\s_]\d+\s*:', re.IGNORECASE)

# Numbered list lines: "1.", "2.", "3." at the start of a line
_NUMBERED_LIST = re.compile(r'^\d+\.\s+')

# Inline citation markers like (1), [2]
_CITATION_PATTERN = re.compile(r'[\(\[]\d+[\)\]]')

# Stray lone quote lines (artifacts from some small models)
_LONE_QUOTE = re.compile(r'^["\'>]{1,3}$')

# Trailing artifacts: triple quotes, lone dashes
_TRAILING_ARTIFACT = re.compile(r'^("""|\'\'\'|---|===)$')


def build_prompt(topic: str, instruction: str, context: str) -> str:
    """
    Assemble a single-turn prompt using the RTF (Role → Task → Format) structure.

    Used by the per-section fallback path in report/sections.py.
    The `instruction` string already contains a few-shot example baked in.
    Context is capped at 2500 chars for better factual grounding.

    Args:
        topic:       Research topic string.
        instruction: Section-specific task prompt (may contain {topic}).
        context:     Pre-retrieved web/wiki text for factual grounding.

    Returns:
        Fully assembled prompt string ready to pass to the LLM.
    """
    instruction      = instruction.replace("{topic}", topic)
    context_snippet  = context.strip()[:2500]

    return (
        f"### ROLE\n{SYSTEM_PERSONA}\n\n"
        f"### BACKGROUND CONTEXT (factual grounding only — do not reproduce verbatim)\n"
        f"{context_snippet}\n\n"
        f"### TASK\n{instruction}\n\n"
        f"### OUTPUT\n"
        f"Write your answer immediately below. No preamble, no title, no explanation.\n"
    )


def clean_response(raw: str) -> str:
    """
    Remove prompt leakage, citation markers, numbered list prefixes,
    stray quote artifacts, and excess whitespace from a raw LLM response.

    Operates line-by-line so legitimate content is never stripped.
    Converts `1. 2. 3.` style output to bullet points where appropriate.

    Args:
        raw: Raw string returned by the LLM.

    Returns:
        Cleaned plain-text string.
    """
    lines   = raw.strip().splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()

        # Skip empty lines (re-added as single blank between paragraphs later)
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        # Drop echoed prompt / commentary lines
        if _LEAK_PATTERNS.match(line):
            continue

        # Drop "Sentence_1:" style label lines
        if _SENTENCE_LABEL.match(line):
            continue

        # Drop markdown fences, separators, or triple-quote artifacts
        if line.startswith("```") or _TRAILING_ARTIFACT.match(line):
            continue

        # Drop lone quote / arrow lines
        if _LONE_QUOTE.match(line):
            continue

        # Remove inline citations
        line = _CITATION_PATTERN.sub("", line).strip()
        if not line:
            continue

        # Convert "1. Something" → "• Something" for consistency
        line = _NUMBERED_LIST.sub("• ", line)

        cleaned.append(line)

    # Remove leading/trailing blank entries
    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return "\n".join(cleaned)
