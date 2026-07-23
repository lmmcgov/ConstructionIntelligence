from collections.abc import Iterable


def is_construction_way(tags) -> bool:
    """
    Returns True if the way is tagged as highway=construction.
    """
    return tags.get("highway") == "construction"


def filter_construction_ways(ways: Iterable):
    """
    Filters an iterable of OSM ways, returning only those tagged
    highway=construction.

    Parameters
    ----------
    ways : Iterable
        Iterable of pyosmium Way objects.

    Returns
    -------
    list
        List of construction ways.
    """
    return [
        way
        for way in ways
        if is_construction_way(way.tags)
    ]