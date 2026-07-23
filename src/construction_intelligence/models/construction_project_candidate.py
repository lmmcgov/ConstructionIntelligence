from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shapely.geometry import MultiLineString, Point


@dataclass(slots=True)
class ConstructionProjectCandidate:
    """
    Represents a single connected construction project extracted
    directly from an OpenStreetMap PBF.

    This object contains only information derived from OSM.
    No AI-generated information belongs in this model.
    """

    # Runtime identifier
    id: UUID

    # Stable identifier derived from the connected OSM way IDs
    origin_id: str

    # Geometry
    geometry: MultiLineString
    centroid: Point
    bbox: tuple[float, float, float, float]

    # Connectivity
    connected_way_ids: list[int]
    connected_way_count: int

    # Physical characteristics
    length_m: float

    # Dominant OSM classifications
    construction_type: str | None
    highway_type: str | None

    # Aggregated metadata
    road_names: list[str]
    route_numbers: list[str]

    # Combined tags from all connected ways
    tags: dict[str, str]