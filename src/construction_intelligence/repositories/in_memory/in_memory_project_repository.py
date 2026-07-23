"""
In-memory implementation of the Project repository.
"""

from construction_intelligence.core.enums import ProjectOrigin
from construction_intelligence.core.ids import ProjectId
from construction_intelligence.core.project import Project

from construction_intelligence.repositories.in_memory_repository import (
    InMemoryRepository,
)
from construction_intelligence.repositories.project_repository import (
    ProjectRepository,
)


class InMemoryProjectRepository(
    InMemoryRepository[
        Project,
        ProjectId,
    ],
    ProjectRepository,
):
    """In-memory Project repository."""

    def get_by_origin_id(
        self,
        origin: ProjectOrigin,
        origin_id: str,
    ) -> Project | None:

        for project in self.list():
            if (
                project.origin == origin
                and project.origin_id == origin_id
            ):
                return project

        return None

    def get_by_road_name(
        self,
        road_name: str,
    ) -> list[Project]:

        return [
            project
            for project in self.list()
            if project.road_name == road_name
        ]

    def get_by_country(
        self,
        country: str,
    ) -> list[Project]:

        return [
            project
            for project in self.list()
            if project.country == country
        ]