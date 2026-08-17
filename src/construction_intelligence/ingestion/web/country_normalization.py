"""
Shared country name normalization.

Used by any component that resolves
country-specific configuration, including:

- SearchContextProvider
- FeedRegistry
"""

from __future__ import annotations

import unicodedata


def normalize_country_name(value: str | None) -> str:
    """
    Normalize a country name for lookup.

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
