"""
In-memory implementation of the Evidence repository.
"""

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)

from construction_intelligence.repositories.evidence_repository import (
    EvidenceRepository,
)
from construction_intelligence.repositories.in_memory_repository import (
    InMemoryRepository,
)


class InMemoryEvidenceRepository(
    InMemoryRepository[
        Evidence,
        EvidenceId,
    ],
    EvidenceRepository,
):
    """In-memory Evidence repository."""

    def get_by_project_id(
        self,
        project_id: ProjectId,
    ) -> list[Evidence]:
        """Return all evidence belonging to a project."""

        return [
            evidence
            for evidence in self.list()
            if evidence.project_id == project_id
        ]

    def get_by_origin_id(
        self,
        source: EvidenceSource,
        origin_id: str,
    ) -> list[Evidence]:
        """Return evidence matching an external source."""

        return [
            evidence
            for evidence in self.list()
            if (
                evidence.source == source
                and evidence.origin_id == origin_id
            )
        ]