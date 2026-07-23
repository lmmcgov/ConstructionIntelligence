"""
Abstract repository interface for Evidence objects.
"""

from __future__ import annotations

from abc import abstractmethod

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)

from .base import Repository


class EvidenceRepository(
    Repository[
        Evidence,
        EvidenceId,
    ],
):
    """Abstract repository for Evidence objects."""

    @abstractmethod
    def get_by_project_id(
        self,
        project_id: ProjectId,
    ) -> list[Evidence]:
        """Return all evidence belonging to a project."""
        raise NotImplementedError

    @abstractmethod
    def get_by_origin_id(
        self,
        source: EvidenceSource,
        origin_id: str,
    ) -> list[Evidence]:
        """Return evidence matching an external source."""
        raise NotImplementedError