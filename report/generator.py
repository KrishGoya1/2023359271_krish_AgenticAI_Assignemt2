# -*- coding: utf-8 -*-
"""
report/generator.py
===================
Orchestrates the end-to-end report generation pipeline:

  generate_detailed_report() — Cover Page → Sections → Footer
"""

from config          import REPORT_SECTIONS, WIDTH
from report.sections  import generate_section
from report.formatter import format_cover_page, format_section


def generate_detailed_report(topic: str, context: str, llm) -> str:
    """
    Generate a complete structured report with cover page.

    Report structure:
      Cover Page → Introduction → Key Findings →
      Challenges → Future Scope → Conclusion → Footer

    Args:
        topic:   The research topic string.
        context: Pre-retrieved web/wiki content for factual grounding.
        llm:     A callable LLM interface (e.g. HuggingFacePipeline).

    Returns:
        A single formatted string containing the full report.
    """
    total = len(REPORT_SECTIONS)
    print(f"\n📄 Building report: '{topic}'")
    print(f"   Structure: Cover Page + {total} sections\n")

    # ── Cover Page ────────────────────────────────────────────
    parts = [format_cover_page(topic)]

    # ── Body Sections ─────────────────────────────────────────
    for i, section in enumerate(REPORT_SECTIONS, 1):
        print(f"  ✍️  [{i}/{total}] {section['title']}...")

        content = generate_section(
            topic       = topic,
            instruction = section["instruction"],
            context     = context,
            llm         = llm,
            section_num = i,
        )

        parts.append(format_section(i, section["title"], content))
        print(f"         ✅  {len(content)} chars")

    # ── Footer ────────────────────────────────────────────────
    parts.append(
        f"\n{'═' * WIDTH}\n"
        f"{'END OF REPORT'.center(WIDTH)}\n"
        f"{'═' * WIDTH}\n"
    )

    print(f"\n✅ Report complete — {total} sections generated.\n")
    return "\n".join(parts)
