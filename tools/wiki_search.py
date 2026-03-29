# -*- coding: utf-8 -*-
"""
tools/wiki_search.py
====================
Wikipedia search tool used by the ReAct agent.
"""

import wikipedia


def search_wikipedia(topic: str, sentences: int = 5) -> str:
    """
    Fetch a summary from Wikipedia for the given `topic`.

    Handles disambiguation automatically by taking the first
    suggested alternative.

    Args:
        topic:     The search query.
        sentences: Number of sentences to include in the summary.

    Returns:
        A plain-text summary string, or an error message on failure.
    """
    try:
        wikipedia.set_lang("en")
        topic = topic.replace(";", "").strip()

        results = wikipedia.search(topic)
        if not results:
            return "No Wikipedia content"

        title = results[0]

        try:
            return wikipedia.summary(title, sentences=sentences, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            return wikipedia.summary(e.options[0], sentences=sentences)

    except Exception as e:
        return f"Wikipedia failed: {e}"
