"""
Maps ConstructionProjectCandidate objects into Project domain models.
"""

from construction_intelligence.core.enums import (
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.project import Project
from construction_intelligence.core.project_category_mapping import (
    CONSTRUCTION_TYPE_TO_CATEGORY,
)
from construction_intelligence.models.construction_project_candidate import (
    ConstructionProjectCandidate,
)


class OSMProjectMapper:
    """Maps construction project candidates into Project objects."""

    def map(
        self,
        candidate: ConstructionProjectCandidate,
    ) -> Project:
        """Convert a ConstructionProjectCandidate into a Project."""

        category = CONSTRUCTION_TYPE_TO_CATEGORY.get(
            candidate.construction_type,
            ProjectCategory.OTHER,
        )

        name = (
            candidate.road_names[0]
            if candidate.road_names
            else f"Construction Project {candidate.origin_id[:8]}"
        )

        road_ref = (
            candidate.route_numbers[0]
            if candidate.route_numbers
            else None
        )

        return Project(
            #
            # Identity
            #
            name=name,
            description="Imported from OpenStreetMap",

            #
            # Classification
            #
            status=ProjectStatus.UNDER_CONSTRUCTION,
            category=category,

            #
            # Source
            #
            origin=ProjectOrigin.OSM,
            origin_id=candidate.origin_id,

            #
            # Road information
            #
            road_name=(
                candidate.road_names[0]
                if candidate.road_names
                else None
            ),
            road_ref=road_ref,

            #
            # Geographic information
            #
            latitude=candidate.centroid.y,
            longitude=candidate.centroid.x,
        )