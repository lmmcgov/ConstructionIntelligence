from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectImportSummary:
    """Summary of a project import operation."""

    candidates_processed: int

    projects_created: int
    projects_updated: int

    evidence_created: int
    evidence_reused: int

    projects_skipped: int

    warnings: tuple[str, ...]

    failures: tuple[str, ...]

    elapsed_seconds: float

    @property
    def successful(self) -> bool:
        return len(self.failures) == 0