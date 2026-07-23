"""
Models used during OSM ingestion.

These models represent raw OpenStreetMap features extracted
from a PBF before they are converted into
ConstructionProjectCandidate objects.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExtractedWay:
    """
    A construction-related OSM way extracted from the PBF.
    """

    osm_id: int

    tags: dict[str, str]

    node_ids: list[int]

    coordinates: list[tuple[float, float]]


@dataclass(slots=True)
class OSMConstructionRoad:
    """
    Lightweight normalized construction road model.
    """

    osm_id: int

    tags: dict[str, str]

    road_name: str | None = None

    road_ref: str | None = None

    construction: str | None = None