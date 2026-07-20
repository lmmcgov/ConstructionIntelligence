"""
Workflow domain model.

A workflow defines how a mission should be executed.
"""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from .ids import MissionId, WorkflowId, new_id


class Workflow(BaseModel):
    id: WorkflowId = Field(default_factory=new_id)

    name: str
    description: str | None = None

    mission_id: MissionId | None = None

    enabled: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def enable(self) -> None:
        self.enabled = True
        self.touch()

    def disable(self) -> None:
        self.enabled = False
        self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)