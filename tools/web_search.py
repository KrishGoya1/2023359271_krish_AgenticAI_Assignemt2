# -*- coding: utf-8 -*-
"""
tools/web_search.py
===================
DuckDuckGo web search tool used by the ReAct agent.
"""

from ddgs import DDGS


def search_web(topic: str, max_results: int = 3) -> str:
    """
    Search the web for `topic` using DuckDuckGo and return a
    formatted string of up to `max_results` results.

    Args:
        topic:       The search query.
        max_results: Maximum number of results to retrieve.

    Returns:
        A newline-separated string of titled snippets,
        or an error message on failure.
    """
    print(f"🔍 Searching web: {topic}")
    results = []

    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(
                topic,
                max_results = max_results,
                region      = "wt-wt",
                safesearch  = "moderate",
            ))

            for i, r in enumerate(search_results, 1):
                title = r.get("title", "")
                body  = r.get("body",  "")
                results.append(f"[{i}] {title}:\n{body}")

        return "\n\n".join(results) if results else "No web results"

    except Exception as e:
        return f"Web search failed: {e}"
