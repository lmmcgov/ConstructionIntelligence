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

import unicodedata

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

    COUNTRY_ALIASES = {

        #
        # North America
        #

        "usa": "united states",

        "us": "united states",

        "united states of america": "united states",

        "america": "united states",


        #
        # Latin America
        #

        "brasil": "brazil",

        "méxico": "mexico",

        "mexico": "mexico",

        "república dominicana": (
            "dominican republic"
        ),

        "dominican republic": (
            "dominican republic"
        ),


        #
        # Europe
        #

        "românia": "romania",

        "rumania": "romania",


        #
        # Asia
        #

        "indonésia": "indonesia",

        "대한민국": "south korea",

        "korea": "south korea",

        "republic of korea": "south korea",

        "日本": "japan",

        "中国": "china",


        #
        # Africa
        #

        "tanzania united republic": (
            "tanzania"
        ),

    }


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

        country_key = self._normalize(
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
        alias = self.COUNTRY_ALIASES.get(
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


    def _normalize(
        self,
        value: str | None,
    ) -> str:
        """
        Normalize country input.

        Handles:

        - None
        - capitalization
        - whitespace
        - accents
        """

        if not value:

            return ""


        value = value.strip().lower()


        #
        # Normalize accents.
        #
        value = (
            unicodedata
            .normalize(
                "NFKD",
                value,
            )
            .encode(
                "ascii",
                "ignore",
            )
            .decode(
                "ascii",
            )
        )


        return value