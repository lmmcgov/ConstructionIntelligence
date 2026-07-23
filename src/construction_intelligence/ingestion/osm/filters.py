"""
Filtering utilities for OSM construction features.
"""

from collections.abc import Mapping


def is_construction_way(tags: Mapping[str, str]) -> bool:
    """Return True if a way represents a road under construction."""

    if tags.get("highway") == "construction":
        return True

    if "construction" in tags and "highway" in tags:
        return True

    return False