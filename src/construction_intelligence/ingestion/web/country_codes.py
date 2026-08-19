"""
Country name -> (ISO 3166-1 alpha-2, primary language) mapping.

Used by GoogleNewsSearchProvider to build the hl/gl/ceid params
Google News uses to localize results. Standalone from
country_profiles.py because that file only covers a subset of
the countries the feed registry (and this) needs, and this data
is small, static, and independently verifiable (unlike feed
URLs, ISO codes aren't something that can silently go stale).

Covers the full countries-of-concern watchlist. Keys are
canonical country names matching FeedRegistry/country_profiles.py
conventions.
"""

from __future__ import annotations


#
# country name -> (alpha-2 country code, ISO 639-1 language)
#
COUNTRY_CODES: dict[str, tuple[str, str]] = {

    #
    # South America
    #
    "bolivia": ("BO", "es"),
    "brazil": ("BR", "pt"),
    "chile": ("CL", "es"),
    "colombia": ("CO", "es"),
    "ecuador": ("EC", "es"),
    "peru": ("PE", "es"),
    "venezuela": ("VE", "es"),

    #
    # Central America & Caribbean
    #
    "belize": ("BZ", "en"),
    "costa rica": ("CR", "es"),
    "cuba": ("CU", "es"),
    "el salvador": ("SV", "es"),
    "guatemala": ("GT", "es"),
    "honduras": ("HN", "es"),
    "nicaragua": ("NI", "es"),
    "panama": ("PA", "es"),

    #
    # Southeast & South Asia
    #
    "indonesia": ("ID", "id"),
    "pakistan": ("PK", "en"),
    "philippines": ("PH", "en"),

    #
    # Europe & Central Asia
    #
    "albania": ("AL", "sq"),
    "bosnia and herzegovina": ("BA", "bs"),
    "bulgaria": ("BG", "bg"),
    "cambodia": ("KH", "km"),
    "kazakhstan": ("KZ", "ru"),
    "moldova": ("MD", "ro"),
    "montenegro": ("ME", "sr"),
    "north macedonia": ("MK", "mk"),
    "romania": ("RO", "ro"),
    "serbia": ("RS", "sr"),

    #
    # Africa
    #
    "south africa": ("ZA", "en"),
    "ghana": ("GH", "en"),
    "nigeria": ("NG", "en"),
    "morocco": ("MA", "fr"),

    #
    # Countries with existing country_profiles.py coverage that
    # aren't on the watchlist but are worth having codes for.
    #
    "united states": ("US", "en"),
    "mexico": ("MX", "es"),
    "argentina": ("AR", "es"),
    "dominican republic": ("DO", "es"),
    "haiti": ("HT", "fr"),
    "jamaica": ("JM", "en"),
    "kenya": ("KE", "en"),
    "tanzania": ("TZ", "en"),
    "uganda": ("UG", "en"),
    "india": ("IN", "en"),
    "bangladesh": ("BD", "bn"),
    "vietnam": ("VN", "vi"),
    "thailand": ("TH", "th"),
    "malaysia": ("MY", "en"),
    "japan": ("JP", "ja"),
    "south korea": ("KR", "ko"),
    "china": ("CN", "zh"),
}


def get_country_code(
    country: str | None,
) -> tuple[str, str] | None:
    """
    Return (alpha-2, language) for a country, or None if
    unmapped. Caller is responsible for normalization -- this
    does an exact lookup against COUNTRY_CODES's keys.
    """

    if not country:

        return None

    return COUNTRY_CODES.get(
        country.strip().lower()
    )
