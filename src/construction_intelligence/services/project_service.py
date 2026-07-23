from construction_intelligence.core.enums import (
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)
from construction_intelligence.core.project import Project
from construction_intelligence.mappers.osm_project_mapper import (
    OSMProjectMapper,
)
from construction_intelligence.models.construction_project_candidate import (
    ConstructionProjectCandidate,
)
from construction_intelligence.models.project_import_result import (
    ProjectImportResult,
)
from construction_intelligence.repositories.project_repository import (
    ProjectRepository,
)


class ProjectService:
    """Business logic for managing Project objects."""

    def __init__(
        self,
        repository: ProjectRepository,
    ) -> None:
        self.repository = repository
        self.mapper = OSMProjectMapper()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _require_project(
        self,
        project_id: ProjectId,
    ) -> Project:
        """Return a project or raise an error if it does not exist."""

        project = self.repository.get(project_id)

        if project is None:
            raise ValueError(
                f"Project {project_id} does not exist."
            )

        return project

    def _validate_name(
        self,
        name: str,
    ) -> str:
        """Validate and normalize a project name."""

        name = name.strip()

        if not name:
            raise ValueError(
                "Project name cannot be empty."
            )

        return name

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_project(
        self,
        name: str,
        *,
        origin: ProjectOrigin,
        origin_id: str | None = None,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
        road_name: str | None = None,
        road_ref: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> Project:
        """Create and store a new project."""

        project = Project(
            name=self._validate_name(name),
            origin=origin,
            origin_id=origin_id,
            country=country,
            state=state,
            city=city,
            road_name=road_name,
            road_ref=road_ref,
            latitude=latitude,
            longitude=longitude,
        )

        self.repository.add(project)

        return project

    def import_candidate(
        self,
        candidate: ConstructionProjectCandidate,
    ) -> ProjectImportResult:
        """
        Import a ConstructionProjectCandidate.

        Existing projects are updated.
        New projects are created.
        """

        project = self.repository.get_by_origin_id(
            ProjectOrigin.OSM,
            candidate.origin_id,
        )

        if project is not None:

            project.name = (
                candidate.road_names[0]
                if candidate.road_names
                else project.name
            )

            project.road_name = (
                candidate.road_names[0]
                if candidate.road_names
                else None
            )

            project.road_ref = (
                candidate.route_numbers[0]
                if candidate.route_numbers
                else None
            )

            project.latitude = candidate.centroid.y
            project.longitude = candidate.centroid.x

            project.touch()

            self.repository.update(project)

            return ProjectImportResult(
                project=project,
                created=False,
            )

        project = self.mapper.map(candidate)

        self.repository.add(project)

        return ProjectImportResult(
            project=project,
            created=True,
        )

    def get_project(
        self,
        project_id: ProjectId,
    ) -> Project | None:
        """Retrieve a project by its ID."""

        return self.repository.get(project_id)

    def get_project_by_origin(
        self,
        origin: ProjectOrigin,
        origin_id: str,
    ) -> Project | None:
        """Retrieve a project by its external source."""

        return self.repository.get_by_origin_id(
            origin,
            origin_id,
        )

    def list_projects(
        self,
    ) -> list[Project]:
        """Return all projects."""

        return self.repository.list()

    #
    # Query methods
    #

    def get_projects_by_road_name(
        self,
        road_name: str,
    ) -> list[Project]:
        """Return projects matching a road name."""

        return self.repository.get_by_road_name(
            road_name
        )

    def get_projects_by_country(
        self,
        country: str,
    ) -> list[Project]:
        """Return projects in a country."""

        return self.repository.get_by_country(
            country
        )

    def get_projects_by_state(
        self,
        state: str,
    ) -> list[Project]:
        """Return projects in a state."""

        return self.repository.get_by_state(
            state
        )

    def get_projects_by_city(
        self,
        city: str,
    ) -> list[Project]:
        """Return projects in a city."""

        return self.repository.get_by_city(
            city
        )

    def get_projects_by_status(
        self,
        status: ProjectStatus,
    ) -> list[Project]:
        """Return projects with a specific status."""

        return self.repository.get_by_status(
            status
        )

    def get_recent_projects(
        self,
        limit: int = 100,
    ) -> list[Project]:
        """Return recently seen projects."""

        return self.repository.get_recently_seen(
            limit
        )

    def search_projects(
        self,
        name: str,
    ) -> list[Project]:
        """Search projects by name."""

        return self.repository.search_by_name(
            name
        )

    def rename_project(
        self,
        project_id: ProjectId,
        new_name: str,
    ) -> Project:
        """Rename an existing project."""

        project = self._require_project(
            project_id
        )

        project.name = self._validate_name(
            new_name
        )

        project.touch()

        self.repository.update(project)

        return project

    def update_location(
        self,
        project_id: ProjectId,
        *,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> Project:
        """Update a project's location."""

        project = self._require_project(
            project_id
        )

        project.country = country
        project.state = state
        project.city = city
        project.latitude = latitude
        project.longitude = longitude

        project.touch()

        self.repository.update(project)

        return project

    def add_evidence(
        self,
        project_id: ProjectId,
        evidence_id: EvidenceId,
    ) -> Project:
        """Associate evidence with a project."""

        project = self._require_project(
            project_id
        )

        project.add_evidence(
            evidence_id
        )

        project.touch()

        self.repository.update(project)

        return project

    def delete_project(
        self,
        project_id: ProjectId,
    ) -> None:
        """Delete a project."""

        self._require_project(
            project_id
        )

        self.repository.remove(
            project_id
        )