from __future__ import annotations

from collections import Counter

from pyproj import Geod
from shapely.geometry import LineString, MultiLineString

from construction_intelligence.core.ids import (
    build_origin_id,
    new_id,
)
from construction_intelligence.ingestion.osm.models import ExtractedWay
from construction_intelligence.models.construction_project_candidate import (
    ConstructionProjectCandidate,
)

GEOD = Geod(ellps="WGS84")


def calculate_length_m(lines: list[LineString]) -> float:
    """
    Calculate total geodesic length of a collection of LineStrings.
    """

    total = 0.0

    for line in lines:

        coords = list(line.coords)

        if len(coords) < 2:
            continue

        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]

        length = GEOD.line_length(lons, lats)

        total += length

    return total


def most_common(values: list[str]) -> str | None:
    """
    Return the most common value or None.
    """

    values = [v for v in values if v]

    if not values:
        return None

    return Counter(values).most_common(1)[0][0]


def build_candidates(
    extracted_ways: list[ExtractedWay],
    components: list[set[int]],
) -> list[ConstructionProjectCandidate]:
    """
    Build ConstructionProjectCandidate objects from connected components.
    """

    ways_by_id = {
        way.osm_id: way
        for way in extracted_ways
    }

    candidates = []

    for component in components:

        connected_way_ids = sorted(component)

        ways = [
            ways_by_id[way_id]
            for way_id in connected_way_ids
            if way_id in ways_by_id
        ]

        lines = []

        road_names = set()
        route_numbers = set()

        construction_types = []
        highway_types = []

        merged_tags = {}

        for way in ways:

            if len(way.coordinates) < 2:
                continue

            line = LineString(way.coordinates)

            lines.append(line)

            if name := way.tags.get("name"):
                road_names.add(name)

            if ref := way.tags.get("ref"):
                route_numbers.add(ref)

            if construction := way.tags.get("construction"):
                construction_types.append(construction)

            if highway := way.tags.get("highway"):
                highway_types.append(highway)

            merged_tags.update(way.tags)

        if not lines:
            continue

        geometry = MultiLineString(lines)

        candidate = ConstructionProjectCandidate(
            id=new_id(),

            origin_id=build_origin_id(
                connected_way_ids
            ),

            geometry=geometry,

            centroid=geometry.centroid,

            bbox=geometry.bounds,

            connected_way_ids=connected_way_ids,

            connected_way_count=len(connected_way_ids),

            length_m=calculate_length_m(lines),

            construction_type=most_common(construction_types),

            highway_type=most_common(highway_types),

            road_names=sorted(road_names),

            route_numbers=sorted(route_numbers),

            tags=merged_tags,
        )

        candidates.append(candidate)

    return candidates