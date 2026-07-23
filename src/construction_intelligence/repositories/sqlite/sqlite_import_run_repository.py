"""
SQLite implementation of the ImportRun repository.
"""

from __future__ import annotations

import json

from construction_intelligence.core.ids import ImportRunId
from construction_intelligence.core.import_run import ImportRun
from construction_intelligence.database.sqlite import Database


class SQLiteImportRunRepository:
    """SQLite-backed repository for ImportRun objects."""

    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database

    def add(
        self,
        import_run: ImportRun,
    ) -> None:
        """Store a new import run."""

        self.database.execute(
            """
            INSERT INTO import_runs (
                id,
                source_file,
                started_at,
                completed_at,
                candidates_processed,
                projects_created,
                projects_updated,
                evidence_created,
                evidence_reused,
                projects_skipped,
                failures,
                elapsed_seconds
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                str(import_run.id),
                import_run.source_file,
                import_run.started_at.isoformat(),
                (
                    import_run.completed_at.isoformat()
                    if import_run.completed_at
                    else None
                ),
                import_run.candidates_processed,
                import_run.projects_created,
                import_run.projects_updated,
                import_run.evidence_created,
                import_run.evidence_reused,
                import_run.projects_skipped,
                json.dumps(import_run.failures),
                import_run.elapsed_seconds,
            ),
        )

    def update(
        self,
        import_run: ImportRun,
    ) -> None:
        """Update an existing import run."""

        self.database.execute(
            """
            UPDATE import_runs
            SET
                source_file=?,
                started_at=?,
                completed_at=?,
                candidates_processed=?,
                projects_created=?,
                projects_updated=?,
                evidence_created=?,
                evidence_reused=?,
                projects_skipped=?,
                failures=?,
                elapsed_seconds=?
            WHERE id=?
            """,
            (
                import_run.source_file,
                import_run.started_at.isoformat(),
                (
                    import_run.completed_at.isoformat()
                    if import_run.completed_at
                    else None
                ),
                import_run.candidates_processed,
                import_run.projects_created,
                import_run.projects_updated,
                import_run.evidence_created,
                import_run.evidence_reused,
                import_run.projects_skipped,
                json.dumps(import_run.failures),
                import_run.elapsed_seconds,
                str(import_run.id),
            ),
        )

    def get(
        self,
        import_run_id: ImportRunId,
    ) -> ImportRun | None:
        """Retrieve an import run by ID."""

        cursor = self.database.query(
            """
            SELECT *
            FROM import_runs
            WHERE id = ?
            """,
            (str(import_run_id),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._from_row(row)

    def list(
        self,
    ) -> list[ImportRun]:
        """Return all import runs."""

        cursor = self.database.query(
            """
            SELECT *
            FROM import_runs
            ORDER BY started_at DESC
            """
        )

        return [
            self._from_row(row)
            for row in cursor.fetchall()
        ]

    def count(
        self,
    ) -> int:
        """Return number of import runs."""

        cursor = self.database.query(
            """
            SELECT COUNT(*)
            FROM import_runs
            """
        )

        return cursor.fetchone()[0]

    def clear(
        self,
    ) -> None:
        """Delete all import runs."""

        self.database.execute(
            """
            DELETE FROM import_runs
            """
        )

    @staticmethod
    def _from_row(
        row,
    ) -> ImportRun:
        """Convert SQLite row into an ImportRun."""

        from datetime import datetime

        return ImportRun(
            id=ImportRunId(row["id"]),
            source_file=row["source_file"],
            started_at=datetime.fromisoformat(
                row["started_at"]
            ),
            completed_at=(
                datetime.fromisoformat(
                    row["completed_at"]
                )
                if row["completed_at"]
                else None
            ),
            candidates_processed=row["candidates_processed"],
            projects_created=row["projects_created"],
            projects_updated=row["projects_updated"],
            evidence_created=row["evidence_created"],
            evidence_reused=row["evidence_reused"],
            projects_skipped=row["projects_skipped"],
            failures=json.loads(
                row["failures"]
            )
            if row["failures"]
            else [],
            elapsed_seconds=row["elapsed_seconds"],
        )