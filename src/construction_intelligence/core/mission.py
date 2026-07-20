"""
Mission domain model.

A mission represents a collection of related tasks that pursue a single goal.
"""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from .ids import MissionId, TaskId, new_id
from .enums import MissionStatus


class Mission(BaseModel):
    id: MissionId = Field(default_factory=new_id)

    name: str
    description: str | None = None

    status: MissionStatus = MissionStatus.PENDING

    tasks: list[TaskId] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    def add_task(self, task_id: TaskId) -> None:
        if task_id not in self.tasks:
            self.tasks.append(task_id)
            self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)