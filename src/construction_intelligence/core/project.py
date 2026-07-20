"""
Core Project domain model.
"""

from datetime import UTC, datetime
from typing import List

from pydantic import BaseModel, Field

from .enums import ConfidenceLevel, ProjectStatus
from .ids import EvidenceId, ProjectId, new_id


class Project(BaseModel):
    """Represents a construction project."""

    id: ProjectId = Field(default_factory=new_id)

    name: str
    aliases: List[str] = Field(default_factory=list)

    country: str | None = None
    subdivision: str | None = None
    locality: str | None = None

    status: ProjectStatus = ProjectStatus.UNKNOWN
    confidence: ConfidenceLevel = ConfidenceLevel.LOW

    evidence: List[EvidenceId] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def add_alias(self, alias: str) -> None:
        """Add an alternate project name."""
        if alias and alias not in self.aliases:
            self.aliases.append(alias)
            self.touch()

    def add_evidence(self, evidence_id: EvidenceId) -> None:
        """Associate evidence with the project."""
        if evidence_id not in self.evidence:
            self.evidence.append(evidence_id)
            self.touch()

    def touch(self) -> None:
        """Update the modification timestamp."""
        self.updated_at = datetime.now(UTC)