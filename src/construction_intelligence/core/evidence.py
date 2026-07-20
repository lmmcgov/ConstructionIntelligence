"""
Evidence domain model.

Evidence represents a single piece of information that supports one or more
facts about a construction project.
"""

from datetime import UTC, datetime
from typing import Dict, Any

from pydantic import BaseModel, Field

from .ids import EvidenceId, ProjectId, new_id


class Evidence(BaseModel):
    """Represents one piece of supporting evidence."""

    id: EvidenceId = Field(default_factory=new_id)

    project_id: ProjectId

    source: str
    url: str | None = None
    title: str | None = None

    content: str | None = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

    discovered_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )