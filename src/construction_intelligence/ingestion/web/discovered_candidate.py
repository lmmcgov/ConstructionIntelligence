"""
Candidate discovered via feed-based discovery.

Represents a single item surfaced by polling
an RSS feed or a sitemap, carrying whatever
structured metadata the source provided.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DiscoveredCandidate:
    """
    Candidate URL surfaced by feed-based discovery.
    """

    url: str

    title: str = ""

    snippet: str = ""

    published_at: datetime | None = None

    source_type: str = ""

    feed_url: str = ""
