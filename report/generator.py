# -*- coding: utf-8 -*-
"""
report/generator.py
===================
Orchestrates end-to-end report generation using a SINGLE LLM call.

Single-call strategy:
  - One prompt asks the model to write all 5 sections at once.
  - Sections are delimited by sentinel markers so we can parse them reliably.
  - This produces a coherent, non-repetitive report because the model
    can see its own prior output while writing each section.
  - Falls back to section-by-section calls if parsing fails.
"""

import re
from langchain_core.messages import SystemMessage, HumanMessage

from config           import REPORT_SECTIONS, WIDTH, SYSTEM_PERSONA
from report.sections  import generate_section
from report.formatter import format_cover_page, format_section


# ── Sentinel used to delimit sections in the single-shot response ──
_SEC_MARKER = "===SECTION{n}==="


def _build_single_shot_prompt(topic: str, context: str) -> list:
    """
    Build a [SystemMessage, HumanMessage] pair that asks the model to
    write all 5 report sections in one pass, separated by sentinels.

    The sentinel format makes parsing reliable and prevents the model
    from adding its own headings or commentary between sections.
    """
    context_snippet = context.strip()[:2500]

    section_specs = "\n\n".join([
        f"{_SEC_MARKER.format(n=i+1)} — {sec['title']}\n"
        + _compress_instruction(sec["instruction"], topic)
        for i, sec in enumerate(REPORT_SECTIONS)
    ])

    system = SystemMessage(content=SYSTEM_PERSONA)

    human_content = (
        f"## RESEARCH TOPIC\n{topic}\n\n"
        f"## BACKGROUND CONTEXT (use as factual grounding only)\n"
        f"{context_snippet}\n\n"
        f"## YOUR TASK\n"
        f"Write a complete research report on '{topic}' with exactly 5 sections.\n"
        f"Separate each section with its marker line exactly as shown.\n"
        f"Do NOT add any text before the first marker or after the last section.\n"
        f"Do NOT repeat the marker inside the section content.\n\n"
        f"{section_specs}\n\n"
        f"Begin with {_SEC_MARKER.format(n=1)} on the very first line."
    )

    return [system, HumanMessage(content=human_content)]


def _compress_instruction(instruction: str, topic: str) -> str:
    """
    Condense a verbose section instruction into a tight directive.
    Replaces {topic} placeholder and strips the long few-shot example
    block — the single-call context window makes examples unnecessary.
    """
    # Replace placeholder
    inst = instruction.replace("{topic}", topic)
    # Drop everything from EXAMPLE OUTPUT onward
    cut = inst.find("EXAMPLE OUTPUT")
    if cut != -1:
        inst = inst[:cut].rstrip()
    # Drop "Now write X for: topic" trailer
    inst = re.sub(r'\nNow write.+$', '', inst, flags=re.DOTALL).strip()
    return inst


def _parse_sections(raw: str) -> dict[int, str]:
    """
    Parse the sentinel-delimited response into a dict of {section_num: content}.

    Returns an empty dict if fewer than 5 sections are found.
    """
    sections: dict[int, str] = {}

    for n in range(1, len(REPORT_SECTIONS) + 1):
        marker     = _SEC_MARKER.format(n=n)
        next_marker = _SEC_MARKER.format(n=n + 1) if n < len(REPORT_SECTIONS) else None

        start = raw.find(marker)
        if start == -1:
            return {}           # sentinel missing → parse failed

        content_start = start + len(marker)
        content_end   = raw.find(next_marker, content_start) if next_marker else len(raw)
        content       = raw[content_start:content_end].strip()

        if not content:
            return {}

        sections[n] = content

    return sections


def generate_detailed_report(topic: str, context: str, llm) -> str:
    """
    Generate a complete structured report with cover page.

    Attempts a single LLM call for all sections (better coherence).
    Falls back to per-section calls if the response cannot be parsed.

    Args:
        topic:   The research topic string.
        context: Pre-retrieved web/wiki content for factual grounding.
        llm:     A LangChain chat model instance (e.g. ChatOpenAI).

    Returns:
        A single formatted string containing the full report.
    """
    total = len(REPORT_SECTIONS)
    print(f"\n📄 Building report: '{topic}'")
    print(f"   Strategy  : single-call ({total} sections in one pass)\n")

    # ── Single-shot attempt ───────────────────────────────────
    parsed: dict[int, str] = {}
    try:
        messages = _build_single_shot_prompt(topic, context)
        raw      = llm.invoke(messages)
        raw_text = raw.content if hasattr(raw, "content") else str(raw)
        parsed   = _parse_sections(raw_text)

        if parsed:
            print("  ✅ Single-call parse succeeded.\n")
        else:
            print("  ⚠️  Single-call parse failed — falling back to per-section calls.\n")
    except Exception as e:
        print(f"  ⚠️  Single-call failed ({e}) — falling back to per-section calls.\n")

    # ── Cover Page ────────────────────────────────────────────
    parts = [format_cover_page(topic)]

    # ── Body Sections ─────────────────────────────────────────
    for i, section in enumerate(REPORT_SECTIONS, 1):
        if parsed.get(i):
            content = parsed[i]
            print(f"  ✍️  [{i}/{total}] {section['title']} — from single call ({len(content)} chars)")
        else:
            # Per-section fallback
            print(f"  ✍️  [{i}/{total}] {section['title']} — calling API...")
            content = generate_section(
                topic       = topic,
                instruction = section["instruction"],
                context     = context,
                llm         = llm,
                section_num = i,
            )
            print(f"         ✅  {len(content)} chars")

        parts.append(format_section(i, section["title"], content))

    # ── Footer ────────────────────────────────────────────────
    parts.append(
        f"\n{'═' * WIDTH}\n"
        f"{'END OF REPORT'.center(WIDTH)}\n"
        f"{'═' * WIDTH}\n"
    )

    print(f"\n✅ Report complete — {total} sections generated.\n")
    return "\n".join(parts)
