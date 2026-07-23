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
    ) -> list[str]:
        """
        Search the web and return URLs.

        Parameters
        ----------
        query:
            Search query string.

        Returns
        -------
        list[str]
            URLs matching the query.
        """

        raise NotImplementedError