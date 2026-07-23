from construction_intelligence.core.enums import MissionStatus
from construction_intelligence.core.mission import Mission
from construction_intelligence.core.ids import WorkflowId

from .base import Repository


class MissionRepository(Repository[Mission]):
    """Repository for Mission objects."""

    def find_by_workflow(
        self,
        workflow_id: WorkflowId,
    ) -> list[Mission]:

        return [
            mission
            for mission in self.list()
            if mission.workflow_id == workflow_id
        ]

    def find_by_status(
        self,
        status: MissionStatus,
    ) -> list[Mission]:

        return [
            mission
            for mission in self.list()
            if mission.status == status
        ]