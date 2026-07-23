"""
Project repository interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from construction_intelligence.core.enums import (
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.ids import ProjectId
from construction_intelligence.core.project import Project


class ProjectRepository(ABC):
    """Abstract repository for Project objects."""

    @abstractmethod
    def add(
        self,
        project: Project,
    ) -> None:
        """Add a project."""
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        project: Project,
    ) -> None:
        """Update a project."""
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        project_id: ProjectId,
    ) -> Project | None:
        """Retrieve a project by ID."""
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> list[Project]:
        """Return all projects."""
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        project_id: ProjectId,
    ) -> None:
        """Remove a project."""
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        project_id: ProjectId,
    ) -> bool:
        """Check if a project exists."""
        raise NotImplementedError

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """Remove all projects."""
        raise NotImplementedError

    @abstractmethod
    def count(
        self,
    ) -> int:
        """Count projects."""
        raise NotImplementedError

    @abstractmethod
    def get_by_origin_id(
        self,
        origin: ProjectOrigin,
        origin_id: str,
    ) -> Project | None:
        """Retrieve a project by external source identifier."""
        raise NotImplementedError

    #
    # Query methods
    #

    @abstractmethod
    def get_by_road_name(
        self,
        road_name: str,
    ) -> list[Project]:
        """Return projects matching a road name."""
        raise NotImplementedError

    @abstractmethod
    def get_by_country(
        self,
        country: str,
    ) -> list[Project]:
        """Return projects in a country."""
        raise NotImplementedError

    @abstractmethod
    def get_by_state(
        self,
        state: str,
    ) -> list[Project]:
        """Return projects in a state."""
        raise NotImplementedError

    @abstractmethod
    def get_by_city(
        self,
        city: str,
    ) -> list[Project]:
        """Return projects in a city."""
        raise NotImplementedError

    @abstractmethod
    def get_by_status(
        self,
        status: ProjectStatus,
    ) -> list[Project]:
        """Return projects by status."""
        raise NotImplementedError

    @abstractmethod
    def get_recently_seen(
        self,
        limit: int = 100,
    ) -> list[Project]:
        """Return recently seen projects."""
        raise NotImplementedError

    @abstractmethod
    def search_by_name(
        self,
        name: str,
    ) -> list[Project]:
        """Search projects by name."""
        raise NotImplementedError