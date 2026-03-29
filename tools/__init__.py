# -*- coding: utf-8 -*-
"""
tools/__init__.py
=================
Exposes all agent tools and the TOOLS registry dict.
"""

from tools.web_search  import search_web
from tools.wiki_search import search_wikipedia

TOOLS = {
    "search_web"      : search_web,
    "search_wikipedia": search_wikipedia,
}

__all__ = ["search_web", "search_wikipedia", "TOOLS"]
