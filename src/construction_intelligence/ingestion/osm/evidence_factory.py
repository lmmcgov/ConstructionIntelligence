"""
Creates Evidence objects from ConstructionProjectCandidate objects.
"""

from construction_intelligence.core.enums import (
    ConfidenceLevel,
)
from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.project import Project
from construction_intelligence.models.construction_project_candidate import (
    ConstructionProjectCandidate,
)


class OSMEvidenceFactory:
    """Creates Evidence records for OSM-derived projects."""

    def create(
        self,
        project: Project,
        candidate: ConstructionProjectCandidate,
    ) -> Evidence:
        """Create an Evidence record from a construction project candidate."""

        return Evidence(
            project_id=project.id,

            source=EvidenceSource.OSM,

            origin_id=candidate.origin_id,

            title=project.name,

            url=None,

            content=(
                "Imported from an OpenStreetMap construction project "
                "candidate."
            ),

            confidence=ConfidenceLevel.HIGH,

            metadata={
                "connected_way_ids": list(
                    candidate.connected_way_ids
                ),
                "connected_way_count": candidate.connected_way_count,
                "construction_type": candidate.construction_type,
                "highway_type": candidate.highway_type,
                "road_names": list(
                    candidate.road_names
                ),
                "route_numbers": list(
                    candidate.route_numbers
                ),
                "length_m": candidate.length_m,
                "tags": dict(
                    candidate.tags
                ),
            },
        )