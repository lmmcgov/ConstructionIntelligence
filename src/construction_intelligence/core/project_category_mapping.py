"""
Shared OSM tag -> ProjectCategory mapping.

Used by any mapper that classifies a construction object from
raw OSM-style tags (highway/construction/building values),
regardless of whether those tags arrived via a PBF import or a
user-uploaded GeoJSON feature.
"""

from __future__ import annotations

from construction_intelligence.core.enums import ProjectCategory


CONSTRUCTION_TYPE_TO_CATEGORY: dict[str, ProjectCategory] = {
    "motorway": ProjectCategory.ROAD,
    "trunk": ProjectCategory.ROAD,
    "primary": ProjectCategory.ROAD,
    "secondary": ProjectCategory.ROAD,
    "tertiary": ProjectCategory.ROAD,
    "residential": ProjectCategory.ROAD,
    "service": ProjectCategory.ROAD,
    "track": ProjectCategory.ROAD,
    "bridge": ProjectCategory.BRIDGE,
    "rail": ProjectCategory.RAIL,
}
