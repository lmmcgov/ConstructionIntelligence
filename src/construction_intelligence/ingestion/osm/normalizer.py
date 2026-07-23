"""
Normalizes extracted OpenStreetMap construction ways into Project domain models.
"""

from construction_intelligence.core.enums import ProjectOrigin
from construction_intelligence.core.project import Project
from construction_intelligence.ingestion.osm.extractor import ExtractedWay


class OSMNormalizer:
    """Converts extracted OSM ways into Project domain models."""

    def normalize(self, way: ExtractedWay) -> Project:
        tags = way.tags

        # Prefer the OSM name; otherwise create a stable placeholder.
        name = tags.get("name") or f"OSM Construction {way.osm_id}"

        return Project(
            name=name,
            origin=ProjectOrigin.OSM,
            origin_id=str(way.osm_id),
            road_name=tags.get("name"),
            road_ref=tags.get("ref"),
        )