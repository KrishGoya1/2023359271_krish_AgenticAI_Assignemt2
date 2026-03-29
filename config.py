# -*- coding: utf-8 -*-
"""
config.py
=========
Shared constants: model name, layout width, LLM persona,
and the full REPORT_SECTIONS definition.
"""

# ── Model ─────────────────────────────────────────────────────
MODEL_NAME = "microsoft/phi-2"

# ── Layout ────────────────────────────────────────────────────
WIDTH = 65          # character width used across cover page + section formatter

# ── LLM Persona ───────────────────────────────────────────────
SYSTEM_PERSONA = (
    "You are a professional research analyst writing a formal structured report. "
    "Your writing is precise, factual, and free of filler phrases. "
    "You follow formatting instructions exactly. "
    "You never add titles, labels, preambles, or commentary to your output. "
    "You output only what is explicitly requested."
)

# ── Report Sections ───────────────────────────────────────────
# Each entry has:
#   id          → machine key
#   title       → display title
#   instruction → task prompt (supports {topic} placeholder + few-shot example)
REPORT_SECTIONS = [
    {
        "id"         : "introduction",
        "title"      : "INTRODUCTION",
        "instruction": (
            "Write exactly 3 sentences introducing the topic: '{topic}'.\n"
            "— Sentence 1: A precise, factual definition of {topic}.\n"
            "— Sentence 2: Why {topic} matters in the real world today.\n"
            "— Sentence 3: What this report examines.\n\n"
            "RULES:\n"
            "• Output exactly 3 sentences. No more, no less.\n"
            "• Do NOT use bullet points.\n"
            "• Do NOT start with 'This report', 'In this report', or 'Introduction'.\n"
            "• Do NOT include a title or section header.\n\n"
            "EXAMPLE OUTPUT (for topic 'Quantum Computing'):\n"
            "Quantum computing is a paradigm of computation that exploits quantum-mechanical "
            "phenomena such as superposition and entanglement to process information in ways "
            "classical computers cannot. As industries from pharmaceuticals to cryptography "
            "seek exponential gains in processing power, quantum computing has emerged as a "
            "central priority for governments and technology companies worldwide. "
            "This report surveys the field's key developments, persistent challenges, and "
            "trajectory over the coming decade.\n\n"
            "Now write 3 sentences for: {topic}"
        ),
    },
    {
        "id"         : "key_findings",
        "title"      : "KEY FINDINGS",
        "instruction": (
            "Write exactly 5 bullet points summarising the most important facts, "
            "statistics, or developments in: '{topic}'.\n\n"
            "FORMAT RULES:\n"
            "• Every line must start with the • symbol.\n"
            "• Each bullet must be one complete, self-contained sentence.\n"
            "• Include at least one specific number, percentage, or year per bullet.\n"
            "• Do NOT write an intro sentence before the bullets.\n"
            "• Do NOT write anything after the 5th bullet.\n"
            "• Do NOT repeat the topic name more than once.\n\n"
            "EXAMPLE OUTPUT (for topic 'Renewable Energy'):\n"
            "• Solar photovoltaic costs fell by 89% between 2010 and 2023, making it the "
            "cheapest electricity source in history.\n"
            "• Global wind capacity surpassed 1 terawatt for the first time in 2023, "
            "supplying roughly 7% of worldwide electricity demand.\n"
            "• The International Energy Agency projects renewables will account for nearly "
            "half of global power generation by 2030.\n"
            "• Battery storage installations tripled between 2020 and 2023, addressing "
            "intermittency as the sector's primary technical constraint.\n"
            "• Over 300,000 clean-energy jobs were added globally in 2023, outpacing "
            "fossil-fuel employment growth by a factor of three.\n\n"
            "Now write 5 bullet points for: {topic}"
        ),
    },
    {
        "id"         : "challenges",
        "title"      : "CHALLENGES",
        "instruction": (
            "Write exactly 4 bullet points about the key challenges facing '{topic}'.\n"
            "Each bullet must address one of these four dimensions, in order:\n"
            "  1. Technical\n"
            "  2. Ethical\n"
            "  3. Economic\n"
            "  4. Social\n\n"
            "FORMAT RULES:\n"
            "• Start every bullet with • followed by the dimension label in bold-style caps "
            "and a colon: e.g. '• TECHNICAL: ...'.\n"
            "• Each bullet is one or two sentences maximum.\n"
            "• Be specific — name actual constraints, not vague generalities.\n"
            "• Do NOT add an intro or closing sentence.\n\n"
            "EXAMPLE OUTPUT (for topic 'Autonomous Vehicles'):\n"
            "• TECHNICAL: Current LiDAR and sensor fusion systems fail in adverse weather "
            "conditions such as heavy rain or snow, limiting reliable deployment to ~30% of "
            "global geographies.\n"
            "• ETHICAL: Algorithmic decision-making in collision scenarios raises unresolved "
            "questions about legal liability and the moral weighting of human lives.\n"
            "• ECONOMIC: Full vehicle autonomy requires sensor stacks costing $50,000–$100,000 "
            "per unit, making consumer pricing unviable without significant cost reductions.\n"
            "• SOCIAL: Public trust remains low, with 65% of US adults reporting they would "
            "feel unsafe in a fully self-driving car as of 2023.\n\n"
            "Now write 4 challenge bullets for: {topic}"
        ),
    },
    {
        "id"         : "future_scope",
        "title"      : "FUTURE SCOPE",
        "instruction": (
            "Write exactly 3 sentences about the future outlook for '{topic}'.\n"
            "— Sentence 1: One concrete near-term development expected within 2–3 years.\n"
            "— Sentence 2: One transformative long-term possibility expected in 10+ years.\n"
            "— Sentence 3: A forward-looking synthesis of why the trajectory is significant.\n\n"
            "RULES:\n"
            "• Output exactly 3 sentences. No bullet points.\n"
            "• Be specific — cite timelines, technologies, or expected outcomes.\n"
            "• Do NOT use the phrase 'it is clear that' or 'the future is bright'.\n"
            "• Do NOT add a title or section label.\n\n"
            "EXAMPLE OUTPUT (for topic 'mRNA Vaccines'):\n"
            "Within the next two to three years, mRNA platforms are expected to yield "
            "approved therapies for influenza, RSV, and several cancer subtypes, building "
            "directly on infrastructure established during the COVID-19 response. "
            "Looking further ahead, personalised mRNA cancer vaccines—tailored to an "
            "individual patient's tumour mutations—could shift oncology from reactive "
            "treatment to preventive immunisation within 15 years. "
            "The programmability and speed of mRNA technology position it as one of the "
            "most consequential biomedical platforms of the 21st century.\n\n"
            "Now write 3 sentences for: {topic}"
        ),
    },
    {
        "id"         : "conclusion",
        "title"      : "CONCLUSION",
        "instruction": (
            "Write exactly 3 sentences concluding the report on '{topic}'.\n"
            "— Sentence 1: Restate the core significance of {topic} in one sentence.\n"
            "— Sentence 2: Identify the single most important challenge that must be solved.\n"
            "— Sentence 3: A measured, forward-looking closing statement.\n\n"
            "RULES:\n"
            "• Exactly 3 sentences. No bullet points. No title.\n"
            "• Do NOT start with 'In conclusion' or 'To summarise'.\n"
            "• Do NOT introduce new facts not covered earlier in the report.\n"
            "• Avoid hyperbole — keep the tone professional and grounded.\n\n"
            "EXAMPLE OUTPUT (for topic 'Large Language Models'):\n"
            "Large language models represent a foundational shift in how humanity builds, "
            "accesses, and applies knowledge at scale. The most pressing challenge ahead "
            "is not technical capability but alignment — ensuring these systems act "
            "reliably in accordance with human values across high-stakes domains. "
            "With sustained investment in interpretability research and robust governance "
            "frameworks, the next generation of language models holds genuine potential "
            "to accelerate scientific discovery and expand access to expertise globally.\n\n"
            "Now write 3 sentences for: {topic}"
        ),
    },
]
