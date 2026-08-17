"""
Feed provider interface.

Provides a subscription-based counterpart
to SearchProvider.

Search providers answer a query.
Feed providers report what is new
across a fixed set of monitored sources.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from construction_intelligence.ingestion.web.discovered_candidate import (
    DiscoveredCandidate,
)


class FeedProvider(ABC):
    """
    Interface for polling subscription-based
    evidence sources (RSS, sitemaps, etc).
    """

    @abstractmethod
    def poll(self) -> list[DiscoveredCandidate]:
        """
        Poll monitored sources and return
        newly observed candidates.

        Implementations own their seen-state
        tracking, so repeated polls return only
        items not previously returned.
        """

        raise NotImplementedError
