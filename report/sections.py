# -*- coding: utf-8 -*-
"""
report/sections.py
==================
Per-section generation logic:

  generate_section()  — invokes the LLM for one report section.
  generate_fallback() — returns a topic-aware static fallback when
                        the LLM output is too short or raises an error.
"""

from report.prompts import build_prompt, clean_response


def generate_section(
    topic       : str,
    instruction : str,
    context     : str,
    llm,
    section_num : int,
) -> str:
    """
    Generate content for a single report section.

    Builds the prompt, invokes the LLM, cleans the response, and
    falls back to a static template if the output is unusable.

    Args:
        topic:       Research topic string.
        instruction: Section instruction (with {topic} placeholder).
        context:     Grounding context from web + Wikipedia.
        llm:         LangChain-compatible LLM callable.
        section_num: 1-indexed section number (used for fallback lookup).

    Returns:
        Cleaned section content string.
    """
    prompt = build_prompt(topic, instruction, context)

    try:
        raw      = llm.invoke(prompt)
        response = clean_response(str(raw))

        if len(response.strip()) < 60:
            print(f"    ⚠️  Section {section_num} output too short — using fallback.")
            return generate_fallback(topic, section_num)

        return response

    except Exception as e:
        print(f"    ⚠️  Section {section_num} failed: {e}")
        return generate_fallback(topic, section_num)


def generate_fallback(topic: str, section_num: int) -> str:
    """
    Return topic-interpolated fallback content when generation fails.

    Each fallback mirrors the expected format for that section number:
      1 → Introduction  (3 prose sentences)
      2 → Key Findings  (5 bullet points)
      3 → Challenges    (4 dimension bullets: TECHNICAL/ETHICAL/ECONOMIC/SOCIAL)
      4 → Future Scope  (3 prose sentences)
      5 → Conclusion    (3 prose sentences)

    Args:
        topic:       Research topic string.
        section_num: 1-indexed section number.

    Returns:
        A formatted fallback string for the given section.
    """
    t = topic
    fallbacks = {
        1: (
            f"{t} is a rapidly evolving field with significant implications "
            f"across technology, society, and industry. "
            f"Its growing adoption has made it a critical area of focus for "
            f"researchers, policymakers, and business leaders worldwide. "
            f"This report examines the key findings, challenges, and future "
            f"trajectory of {t}."
        ),
        2: (
            f"• {t} has experienced substantial growth over the past five years, "
            f"with global investment exceeding hundreds of billions of dollars.\n"
            f"• Adoption rates have accelerated, with major enterprises deploying "
            f"{t}-based solutions across core operations.\n"
            f"• Performance benchmarks show consistent year-over-year improvements "
            f"driven by advances in underlying research.\n"
            f"• Regulatory frameworks in the EU, US, and Asia are actively evolving "
            f"to address the implications of {t} at scale.\n"
            f"• The workforce impact is measurable, with new specialised roles "
            f"emerging faster than training pipelines can supply them."
        ),
        3: (
            f"• TECHNICAL: Core infrastructure for {t} remains computationally "
            f"intensive, limiting deployment in resource-constrained environments.\n"
            f"• ETHICAL: Questions of bias, accountability, and transparency in "
            f"{t} systems remain largely unresolved across the industry.\n"
            f"• ECONOMIC: High upfront costs and uncertain ROI timelines deter "
            f"smaller organisations from adopting {t} at scale.\n"
            f"• SOCIAL: Public understanding of {t} is limited, fuelling "
            f"scepticism that slows beneficial adoption."
        ),
        4: (
            f"In the near term, {t} is expected to see significant capability "
            f"improvements as current research matures into production-ready "
            f"systems over the next two to three years. "
            f"Over a longer horizon, convergence with adjacent technologies could "
            f"unlock applications in {t} that are not yet technically feasible. "
            f"The overall trajectory suggests {t} will become a foundational "
            f"layer of modern infrastructure within the next decade."
        ),
        5: (
            f"{t} stands as one of the defining technological developments of "
            f"this era, with implications that extend well beyond any single "
            f"industry or use case. "
            f"The most critical challenge ahead is ensuring that its development "
            f"remains aligned with human values and governed by robust, "
            f"evidence-based policy. "
            f"With sustained investment and responsible stewardship, {t} has the "
            f"potential to deliver lasting and equitable benefit at global scale."
        ),
    }
    return fallbacks.get(section_num, f"Content unavailable for {t}.")
