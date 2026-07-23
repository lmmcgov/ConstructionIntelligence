from construction_intelligence.core.enums import TaskStatus
from construction_intelligence.core.ids import MissionId
from construction_intelligence.core.task import Task

from .base import Repository


class TaskRepository(Repository[Task]):
    """Repository for Task objects."""

    def find_by_mission(
        self,
        mission_id: MissionId,
    ) -> list[Task]:

        return [
            task
            for task in self.list()
            if task.mission_id == mission_id
        ]

    def find_by_status(
        self,
        status: TaskStatus,
    ) -> list[Task]:

        return [
            task
            for task in self.list()
            if task.status == status
        ]