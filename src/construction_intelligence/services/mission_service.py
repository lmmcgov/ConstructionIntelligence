"""
Mission service.

Contains the business logic for creating, retrieving, listing,
and deleting missions.
"""

from construction_intelligence.core.ids import MissionId
from construction_intelligence.core.mission import Mission
from construction_intelligence.repositories.mission_repository import MissionRepository


class MissionService:
    """Service for managing missions."""

    def __init__(self, repository: MissionRepository):
        self._repository = repository

    def create_mission(
        self,
        name: str,
        description: str | None = None,
    ) -> Mission:
        """Create and store a new mission."""

        self._validate_name(name)

        mission = Mission(
            name=name,
            description=description,
        )

        self._repository.add(mission)

        return mission

    def get_mission(self, mission_id: MissionId) -> Mission:
        """Return a mission by ID."""

        return self._require_mission(mission_id)

    def list_missions(self) -> list[Mission]:
        """Return all missions."""

        return self._repository.list()

    def delete_mission(self, mission_id: MissionId) -> None:
        """Delete a mission."""

        self._require_mission(mission_id)

        self._repository.remove(mission_id)

    def rename_mission(
        self,
        mission_id: MissionId,
        name: str,
    ) -> Mission:
        """Rename a mission."""

        self._validate_name(name)

        mission = self._require_mission(mission_id)

        mission.name = name
        mission.touch()

        return mission

    def update_description(
        self,
        mission_id: MissionId,
        description: str | None,
    ) -> Mission:
        """Update a mission description."""

        mission = self._require_mission(mission_id)

        mission.description = description
        mission.touch()

        return mission

    def _require_mission(self, mission_id: MissionId) -> Mission:
        """Return a mission or raise an exception."""

        mission = self._repository.get(mission_id)

        if mission is None:
            raise ValueError(f"Mission '{mission_id}' does not exist.")

        return mission

    def _validate_name(self, name: str) -> None:
        """Validate a mission name."""

        if not name.strip():
            raise ValueError("Mission name cannot be empty.")