from dataclasses import dataclass

from construction_intelligence.core.project import Project


@dataclass(frozen=True)
class ProjectImportResult:
    """Result of importing a construction project candidate."""

    project: Project
    created: bool

    @property
    def updated(self) -> bool:
        """True if an existing project was updated."""

        return not self.created