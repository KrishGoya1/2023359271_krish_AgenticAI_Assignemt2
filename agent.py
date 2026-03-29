# -*- coding: utf-8 -*-
"""
agent.py
========
Rule-based ReAct agent:

  agent_decide()    — deterministic decision function (no LLM needed).
  run_react_agent() — full Thought → Action → Observe loop.
"""

from model           import load_model
from tools           import search_web, search_wikipedia
from report          import generate_detailed_report
from utils           import clean_and_combine, create_cover_page, save_report
from config          import OPENROUTER_MODEL


# ── Tool Registry ─────────────────────────────────────────────
TOOLS = {
    "search_web"      : search_web,
    "search_wikipedia": search_wikipedia,
    "generate_report" : generate_detailed_report,
}


def agent_decide(steps_done: list) -> tuple[str, str]:
    """
    Rule-based decision function — no LLM required.

    Follows a fixed ReAct sequence:
      1. No web data yet?   → search_web
      2. No wiki data yet?  → search_wikipedia
      3. Have both?         → generate_report
      4. Report done?       → done

    Args:
        steps_done: List of action names already completed.

    Returns:
        (thought, action) tuple.
    """
    if "search_web" not in steps_done:
        thought = "I don't have web data yet. I should search the web."
        action  = "search_web"

    elif "search_wikipedia" not in steps_done:
        thought = "I have web data but need encyclopedic context."
        action  = "search_wikipedia"

    elif "generate_report" not in steps_done:
        thought = "I have all context needed. Time to write the report."
        action  = "generate_report"

    else:
        thought = "Report is complete. My work is done."
        action  = "done"

    return thought, action


def run_react_agent() -> str:
    """
    ReAct Agent Loop — Rule-Based Decision + Tool Execution.

    Pattern: Thought → Action → Observe → Repeat

    Loads the Phi-2 model on first invocation, runs the full loop,
    prints and saves the report, then returns the report string.

    Returns:
        The full formatted report as a string.
    """
    print("=" * 65)
    print("     🤖 REACT RESEARCH AGENT — STARTING")
    print("=" * 65)

    # ── Get Topic ─────────────────────────────────────────────
    topic = input("\n📌 Enter research topic: ").strip()
    if not topic:
        print("❌ No topic entered.")
        return ""

    print(f"\n✅ Topic: '{topic}'")
    print("-" * 65)

    # ── Load Model ────────────────────────────────────────────
    llm = load_model()

    # ── Agent Memory (State) ──────────────────────────────────
    memory = {
        "topic"      : topic,
        "web"        : "",
        "wiki"       : "",
        "context"    : "",
        "report"     : "",
        "steps_done" : [],
    }

    max_steps  = 6
    step_count = 0
    done       = False

    # ── ReAct Loop ────────────────────────────────────────────
    while not done and step_count < max_steps:

        step_count += 1
        print(f"\n{'─'*65}")
        print(f"  🔁 STEP {step_count}")

        # ── THOUGHT ───────────────────────────────────────────
        thought, action = agent_decide(memory["steps_done"])
        print(f"  💭 THOUGHT : {thought}")
        print(f"  ⚡ ACTION  : {action}")

        # ── ACTION + OBSERVE ──────────────────────────────────
        if action == "search_web":
            print(f"  👁  OBSERVE : Running web search...")
            result        = search_web(topic, max_results=3)
            memory["web"] = result
            memory["steps_done"].append("search_web")
            memory["context"] = clean_and_combine(
                topic, memory["web"], memory["wiki"]
            )
            print(f"  ✅ Web search complete ({len(result)} chars)")

        elif action == "search_wikipedia":
            print(f"  👁  OBSERVE : Running Wikipedia search...")
            result         = search_wikipedia(topic, sentences=5)
            memory["wiki"] = result
            memory["steps_done"].append("search_wikipedia")
            memory["context"] = clean_and_combine(
                topic, memory["web"], memory["wiki"]
            )
            print(f"  ✅ Wikipedia complete ({len(result)} chars)")

        elif action == "generate_report":
            print(f"  👁  OBSERVE : Generating detailed report...")
            memory["report"] = generate_detailed_report(
                topic, memory["context"], llm
            )
            memory["steps_done"].append("generate_report")
            print(f"  ✅ Report generated.")
            done = True

        elif action == "done":
            print("  🏁 Agent decided it is done.")
            done = True

    # ── Build Final Report ────────────────────────────────────
    cover = create_cover_page(topic)

    agent_trace = (
        f"\n{'='*65}\n"
        f"{'AGENT EXECUTION TRACE':^65}\n"
        f"{'='*65}\n"
        f"  Steps : {' → '.join(memory['steps_done'])}\n"
        f"  Total : {step_count} step(s)\n"
    )

    full_report = (
        cover
        + agent_trace
        + "\n" + "=" * 65 + "\n"
        + memory["report"]
    )

    print("\n" + "=" * 65)
    print("          📋 FINAL REPORT")
    print("=" * 65)
    print(full_report)

    save_report(topic, full_report)
    print(f"\n✅ Agent complete! Report saved.")
    return full_report
