"""
Shared country name aliases.

Maps common alternate spellings, native-language names,
formal/constitutional names, and abbreviations to the
canonical country name used as a lookup key elsewhere in
the ingestion layer (SearchContextProvider, FeedRegistry).

Keys should be run through normalize_country_name before
lookup (lowercase, accent-stripped) -- callers are
responsible for that, this module just stores the mapping.

Values are canonical country name strings as used by
COUNTRY_PROFILES (country_profiles.py) and by
FeedRegistry.register() call sites (feed_registry_defaults.py).
"""

from __future__ import annotations


COUNTRY_ALIASES: dict[str, str] = {

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

    "plurinational state of bolivia": (
        "bolivia"
    ),

    "bolivarian republic of venezuela": (
        "venezuela"
    ),


    #
    # Europe
    #

    "românia": "romania",

    "rumania": "romania",

    "bosnia": (
        "bosnia and herzegovina"
    ),

    "bosnia & herzegovina": (
        "bosnia and herzegovina"
    ),

    "bih": (
        "bosnia and herzegovina"
    ),

    "macedonia": "north macedonia",

    "fyrom": "north macedonia",

    "former yugoslav republic of macedonia": (
        "north macedonia"
    ),

    "republic of moldova": "moldova",


    #
    # Asia
    #

    "indonésia": "indonesia",

    "대한민국": "south korea",

    "korea": "south korea",

    "republic of korea": "south korea",

    "日本": "japan",

    "中国": "china",

    "kingdom of cambodia": "cambodia",


    #
    # Africa
    #

    "tanzania united republic": (
        "tanzania"
    ),

    "kingdom of morocco": "morocco",

}
