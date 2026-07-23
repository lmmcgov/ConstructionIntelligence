"""
Mock web search provider for testing.
"""

from __future__ import annotations

from construction_intelligence.ingestion.web.search_provider import (
    SearchProvider,
)


class MockSearchProvider(SearchProvider):
    """
    Returns predetermined URLs for testing.
    """

    def __init__(
        self,
        results: dict[str, list[str]] | None = None,
    ) -> None:

        self.results = (
            results
            if results is not None
            else {}
        )

    def search(
        self,
        query: str,
    ) -> list[str]:
        """
        Return URLs associated with a query.
        """

        return self.results.get(
            query,
            [],
        )