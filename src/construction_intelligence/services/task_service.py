"""
Task service.

Contains the business logic for creating, retrieving, updating,
listing, and deleting tasks.
"""

from construction_intelligence.core.ids import MissionId, ProjectId, TaskId
from construction_intelligence.core.task import Task
from construction_intelligence.repositories.task_repository import TaskRepository


class TaskService:
    """Service for managing tasks."""

    def __init__(self, repository: TaskRepository):
        self._repository = repository

    def create_task(
        self,
        task_type: str,
        mission_id: MissionId | None = None,
        project_id: ProjectId | None = None,
        payload: dict | None = None,
    ) -> Task:
        """Create and store a new task."""

        self._validate_task_type(task_type)

        task = Task(
            task_type=task_type,
            mission_id=mission_id,
            project_id=project_id,
            payload=payload or {},
        )

        self._repository.add(task)

        return task

    def get_task(self, task_id: TaskId) -> Task:
        """Return a task by ID."""

        return self._require_task(task_id)

    def list_tasks(self) -> list[Task]:
        """Return all tasks."""

        return self._repository.list()

    def delete_task(self, task_id: TaskId) -> None:
        """Delete a task."""

        self._require_task(task_id)

        self._repository.remove(task_id)

    def start_task(self, task_id: TaskId) -> Task:
        """Mark a task as running."""

        task = self._require_task(task_id)

        task.start()

        return task

    def complete_task(self, task_id: TaskId) -> Task:
        """Mark a task as completed."""

        task = self._require_task(task_id)

        task.complete()

        return task

    def fail_task(self, task_id: TaskId) -> Task:
        """Mark a task as failed."""

        task = self._require_task(task_id)

        task.fail()

        return task

    def update_payload(
        self,
        task_id: TaskId,
        payload: dict,
    ) -> Task:
        """Replace the payload of a task."""

        task = self._require_task(task_id)

        task.payload = payload
        task.updated_at = task.created_at.__class__.now(task.updated_at.tzinfo)

        return task

    def _require_task(self, task_id: TaskId) -> Task:
        """Return a task or raise an exception."""

        task = self._repository.get(task_id)

        if task is None:
            raise ValueError(f"Task '{task_id}' does not exist.")

        return task

    def _validate_task_type(self, task_type: str) -> None:
        """Validate the task type."""

        if not task_type.strip():
            raise ValueError("Task type cannot be empty.")