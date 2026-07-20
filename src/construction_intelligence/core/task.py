"""
Task domain model.

Tasks represent units of work assigned to an agent.
"""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field

from .ids import MissionId, ProjectId, TaskId, new_id


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """A unit of work for an agent."""

    id: TaskId = Field(default_factory=new_id)

    task_type: str

    mission_id: MissionId | None = None
    project_id: ProjectId | None = None

    payload: dict = Field(default_factory=dict)

    status: TaskStatus = TaskStatus.PENDING

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def start(self) -> None:
        self.status = TaskStatus.RUNNING
        self.updated_at = datetime.now(UTC)

    def complete(self) -> None:
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.now(UTC)

    def fail(self) -> None:
        self.status = TaskStatus.FAILED
        self.updated_at = datetime.now(UTC)