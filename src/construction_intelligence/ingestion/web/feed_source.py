"""
Feed source configuration.

Identifies a single feed to poll for
evidence discovery, and how it should
be interpreted.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeedSource:
    """
    A single feed to monitor for new evidence.
    """

    url: str

    #
    # Matches SearchContext.source_priority keys
    # (e.g. "government", "municipal", "procurement",
    # "news") so feed-sourced candidates can reuse
    # the same ranking weights as query-based ones.
    #
    category: str

    #
    # "rss" or "sitemap".
    #
    kind: str = "rss"
