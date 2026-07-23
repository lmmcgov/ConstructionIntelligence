"""
ImportRun domain model.

Tracks a single execution of an import pipeline.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .ids import ImportRunId, new_id


@dataclass(slots=True)
class ImportRun:
    """Represents one import execution."""

    id: ImportRunId = field(
        default_factory=new_id
    )

    #
    # Source information
    #
    source_file: str = ""

    #
    # Timing
    #
    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    completed_at: datetime | None = None

    #
    # Import statistics
    #
    candidates_processed: int = 0

    projects_created: int = 0

    projects_updated: int = 0

    evidence_created: int = 0

    evidence_reused: int = 0

    projects_skipped: int = 0

    #
    # Results
    #
    failures: list[str] = field(
        default_factory=list
    )

    elapsed_seconds: float = 0.0

    def complete(
        self,
    ) -> None:
        """Mark the import as completed."""

        self.completed_at = datetime.now(UTC)