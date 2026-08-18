"""
Maps GeoJSON construction features into Project domain models.
"""

from __future__ import annotations

from typing import Any

from shapely.geometry import shape

from construction_intelligence.core.enums import (
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.project import Project
from construction_intelligence.core.project_category_mapping import (
    CONSTRUCTION_TYPE_TO_CATEGORY,
)


class GeoJSONProjectMapper:
    """
    Maps a single GeoJSON Feature (construction object) into a
    Project domain model.

    Unlike OSMProjectMapper, there is no way-connectivity graph
    to stitch here -- each uploaded feature is already treated
    as one discrete project.

    Reads OSM-style tag conventions from `properties` where
    present (name, ref, highway/construction/building,
    addr:country/addr:state/addr:city), falling back to plain
    country/state/city keys for non-OSM-derived GeoJSON.
    """

    def map(
        self,
        feature: dict[str, Any],
        index: int,
    ) -> Project:

        properties = feature.get("properties") or {}

        name = (
            properties.get("name")
            or f"Uploaded Construction Object {index}"
        )

        latitude, longitude = self._resolve_centroid(
            feature.get("geometry")
        )

        return Project(
            name=name,
            status=ProjectStatus.UNDER_CONSTRUCTION,
            category=self._resolve_category(properties),
            origin=ProjectOrigin.GEOJSON_UPLOAD,
            origin_id=str(
                properties.get("id")
                or properties.get("osm_id")
                or index
            ),
            road_name=properties.get("name"),
            road_ref=properties.get("ref"),
            country=(
                properties.get("addr:country")
                or properties.get("country")
            ),
            state=(
                properties.get("addr:state")
                or properties.get("state")
            ),
            city=(
                properties.get("addr:city")
                or properties.get("city")
            ),
            latitude=latitude,
            longitude=longitude,
        )


    def _resolve_category(
        self,
        properties: dict[str, Any],
    ) -> ProjectCategory:
        """
        Check the same tag keys OSM uses to classify a
        construction object, in priority order.
        """

        for key in (
            "construction",
            "highway",
            "building",
        ):

            value = properties.get(key)

            if value in CONSTRUCTION_TYPE_TO_CATEGORY:

                return CONSTRUCTION_TYPE_TO_CATEGORY[value]

        return ProjectCategory.OTHER


    def _resolve_centroid(
        self,
        geometry: dict[str, Any] | None,
    ) -> tuple[float | None, float | None]:
        """
        Compute a representative point for any GeoJSON geometry
        type (Point, LineString, Polygon, Multi*) via its centroid.
        """

        if not geometry:

            return None, None

        centroid = shape(geometry).centroid

        return centroid.y, centroid.x
