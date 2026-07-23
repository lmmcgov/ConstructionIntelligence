"""
Streaming extractor for construction-related OSM ways.
"""

from __future__ import annotations

import osmium

from .filters import is_construction_way
from .models import ExtractedWay


class OSMConstructionExtractor(osmium.SimpleHandler):
    """Extract construction-related highway ways from an OSM PBF."""

    def __init__(self) -> None:
        super().__init__()
        self._ways: list[ExtractedWay] = []

    @property
    def ways(self) -> list[ExtractedWay]:
        """Return all extracted construction ways."""
        return self._ways

    def way(self, way: osmium.osm.Way) -> None:
        """Called automatically for every way in the PBF."""

        tags = {tag.k: tag.v for tag in way.tags}

        if not is_construction_way(tags):
            return

        node_ids: list[int] = []
        coordinates: list[tuple[float, float]] = []

        for node in way.nodes:
            node_ids.append(node.ref)

            if node.location.valid():
                coordinates.append(
                    (
                        node.location.lon,
                        node.location.lat,
                    )
                )

        self._ways.append(
            ExtractedWay(
                osm_id=way.id,
                tags=tags,
                node_ids=node_ids,
                coordinates=coordinates,
            )
        )

    def extract(self, pbf_path: str) -> list[ExtractedWay]:
        """Extract all construction ways from a PBF."""

        self._ways.clear()

        self.apply_file(
            pbf_path,
            locations=True,
        )

        return self._ways