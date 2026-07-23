"""
Structured search query model.

Represents a search query with intent metadata.

This allows downstream services to understand:

- why the query exists
- how important it is
- how it should be executed
- when it should be executed in the search pipeline
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchQuery:
    """
    Represents a prioritized and tiered search query.

    Attributes:

    query:
        Actual search engine query string.

    category:
        Search intent category.

        Examples:
        - official
        - procurement
        - construction
        - infrastructure
        - news
        - discovery

    priority:
        Ordering within a search tier.

        Lower numbers execute first.

    tier:
        Execution group.

        Tier 1:
            High-confidence evidence sources.
            Official records and procurement.

        Tier 2:
            Construction activity signals.

        Tier 3:
            Broad discovery signals.
    """

    query: str

    category: str

    priority: int

    tier: int