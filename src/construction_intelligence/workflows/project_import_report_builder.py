from construction_intelligence.models.project_import_summary import (
    ProjectImportSummary,
)


class ProjectImportReportBuilder:
    """Collects import statistics during a workflow run."""

    def __init__(self) -> None:
        self.processed = 0
        self.created = 0
        self.updated = 0

        self.evidence_created = 0
        self.evidence_reused_count = 0

        self.skipped = 0

        self.warnings: list[str] = []
        self.failures: list[str] = []

    def candidate_processed(self) -> None:
        self.processed += 1

    def project_created(self) -> None:
        self.created += 1

    def project_updated(self) -> None:
        self.updated += 1

    def evidence_added(self) -> None:
        self.evidence_created += 1

    def evidence_reused(self) -> None:
        self.evidence_reused_count += 1

    def candidate_skipped(self) -> None:
        self.skipped += 1

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def failure(self, message: str) -> None:
        self.failures.append(message)

    def build(
        self,
        elapsed_seconds: float,
    ) -> ProjectImportSummary:
        return ProjectImportSummary(
            candidates_processed=self.processed,
            projects_created=self.created,
            projects_updated=self.updated,
            evidence_created=self.evidence_created,
            evidence_reused=self.evidence_reused_count,
            projects_skipped=self.skipped,
            warnings=tuple(self.warnings),
            failures=tuple(self.failures),
            elapsed_seconds=elapsed_seconds,
        )