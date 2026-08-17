"""
Feed registry.

Maps countries to the RSS/sitemap sources
that should be monitored for that country.

Ships empty. Which feeds are trustworthy for a
given country is curation work, not something
that can be safely guessed — register feeds you
have verified for the countries you are actively
watching, e.g.:

    registry = FeedRegistry()

    registry.register(
        "united states",
        [
            FeedSource(
                url="https://example-dot.gov/news/rss.xml",
                category="government",
                kind="rss",
            ),
        ],
    )
"""

from __future__ import annotations

from construction_intelligence.ingestion.web.country_aliases import (
    COUNTRY_ALIASES,
)

from construction_intelligence.ingestion.web.country_normalization import (
    normalize_country_name,
)

from construction_intelligence.ingestion.web.feed_source import (
    FeedSource,
)


class FeedRegistry:
    """
    Provides country-specific feed sources.
    """

    def __init__(self) -> None:

        self._feeds: dict[str, list[FeedSource]] = {}


    def register(
        self,
        country: str,
        feed_sources: list[FeedSource],
    ) -> None:
        """
        Register feed sources for a country.

        Repeated calls for the same country append
        rather than overwrite, so feeds can be
        registered incrementally by category.
        """

        country_key = normalize_country_name(
            country
        )

        self._feeds.setdefault(
            country_key,
            [],
        )

        self._feeds[country_key].extend(
            feed_sources
        )


    def get_feeds(
        self,
        country: str | None,
    ) -> list[FeedSource]:
        """
        Return feed sources registered for a country.

        Resolution order:

        1. Exact normalized country
        2. Alias lookup (COUNTRY_ALIASES)
        3. Empty list

        Unlike SearchContext, there is no global
        fallback beyond alias resolution — a wrong
        country's feed is worse than no feed.
        """

        country_key = normalize_country_name(
            country
        )

        #
        # Exact match
        #
        if country_key in self._feeds:

            return self._feeds[
                country_key
            ]


        #
        # Alias match
        #
        alias = COUNTRY_ALIASES.get(
            country_key
        )

        if alias and alias in self._feeds:

            return self._feeds[
                alias
            ]


        return []
