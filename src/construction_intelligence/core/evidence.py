"""
Evidence domain model.

Evidence represents a single piece of information that supports one or more
facts about a construction project.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from .evidence_source import EvidenceSource
from .enums import ConfidenceLevel
from .ids import EvidenceId, ProjectId, new_id


class Evidence(BaseModel):
    """Represents one piece of supporting evidence."""

    id: EvidenceId = Field(
        default_factory=new_id
    )

    #
    # Which project this evidence supports
    #
    project_id: ProjectId

    #
    # Evidence source information
    #
    source: EvidenceSource

    origin_id: str | None = None

    url: str | None = None

    title: str | None = None

    content: str | None = None

    #
    # Confidence assigned to this evidence
    #
    confidence: ConfidenceLevel = (
        ConfidenceLevel.LOW
    )

    #
    # Arbitrary structured metadata
    #
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    discovered_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )