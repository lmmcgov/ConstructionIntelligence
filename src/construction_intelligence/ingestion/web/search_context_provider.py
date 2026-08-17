"""
Search context provider.

Loads localized search intelligence
from country profiles.

Responsibilities:

- Normalize country names
- Resolve country aliases
- Return localized SearchContext
- Provide safe fallback behavior
"""

from __future__ import annotations

from construction_intelligence.ingestion.web.country_aliases import (
    COUNTRY_ALIASES,
)

from construction_intelligence.ingestion.web.country_normalization import (
    normalize_country_name,
)

from construction_intelligence.ingestion.web.country_profiles import (
    COUNTRY_PROFILES,
)

from construction_intelligence.ingestion.web.search_context import (
    SearchContext,
)


class SearchContextProvider:
    """
    Provides country-specific search contexts.
    """

    def get_context(
        self,
        country: str | None,
    ) -> SearchContext:
        """
        Return localized search context.

        Resolution order:

        1. Exact normalized country
        2. Alias lookup
        3. English global fallback
        """

        country_key = normalize_country_name(
            country
        )

        #
        # Exact match
        #
        if country_key in COUNTRY_PROFILES:

            return COUNTRY_PROFILES[
                country_key
            ]


        #
        # Alias match
        #
        alias = COUNTRY_ALIASES.get(
            country_key
        )

        if alias:

            if alias in COUNTRY_PROFILES:

                return COUNTRY_PROFILES[
                    alias
                ]


        #
        # Global fallback
        #
        return COUNTRY_PROFILES[
            "united states"
        ]