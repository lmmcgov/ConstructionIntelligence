"""
Workflow service.

Coordinates missions, tasks, projects, and evidence into
higher-level workflows.
"""

from construction_intelligence.core.mission import Mission
from construction_intelligence.core.project import Project
from construction_intelligence.core.task import Task
from construction_intelligence.services.evidence_service import EvidenceService
from construction_intelligence.services.mission_service import MissionService
from construction_intelligence.services.project_service import ProjectService
from construction_intelligence.services.task_service import TaskService


class WorkflowService:
    """High-level orchestration service."""

    def __init__(
        self,
        project_service: ProjectService,
        mission_service: MissionService,
        task_service: TaskService,
        evidence_service: EvidenceService,
    ):
        self.project_service = project_service
        self.mission_service = mission_service
        self.task_service = task_service
        self.evidence_service = evidence_service

    def create_project_workflow(
        self,
        project_name: str,
        mission_name: str,
        task_type: str,
        payload: dict | None = None,
    ) -> tuple[Project, Mission, Task]:
        """
        Create a project, mission, and initial task.
        """

        project = self.project_service.create_project(project_name)

        mission = self.mission_service.create_mission(
            name=mission_name
        )

        task = self.task_service.create_task(
            task_type=task_type,
            mission_id=mission.id,
            project_id=project.id,
            payload=payload or {},
        )

        mission.add_task(task.id)

        return project, mission, task

    def start_task(self, task_id):
        return self.task_service.start_task(task_id)

    def complete_task(self, task_id):
        return self.task_service.complete_task(task_id)

    def fail_task(self, task_id):
        return self.task_service.fail_task(task_id)