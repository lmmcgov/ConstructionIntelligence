"""
Web search provider interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class SearchProvider(ABC):
    """
    Interface for discovering web resources.
    """

    @abstractmethod
    def search(
        self,
        query: str,
        country: str | None = None,
    ) -> list[str]:
        """
        Search the web and return URLs.

        Parameters
        ----------
        query:
            Search query string.

        country:
            Canonical country name (as resolved by
            SearchContextProvider), if known. Optional --
            providers that don't localize by country (e.g.
            SearXNG) can ignore it; providers that do (e.g.
            Google News) use it to scope results.

        Returns
        -------
        list[str]
            URLs matching the query.
        """

        raise NotImplementedError