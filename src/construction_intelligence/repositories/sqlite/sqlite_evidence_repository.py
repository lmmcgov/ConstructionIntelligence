"""
SQLite implementation of the Evidence repository.
"""

from __future__ import annotations

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)
from construction_intelligence.database.sqlite import Database
from construction_intelligence.mappers.sqlite_evidence_mapper import (
    SQLiteEvidenceMapper,
)
from construction_intelligence.repositories.evidence_repository import (
    EvidenceRepository,
)


class SQLiteEvidenceRepository(
    EvidenceRepository,
):
    """SQLite-backed repository for Evidence objects."""

    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database

    def add(
        self,
        evidence: Evidence,
    ) -> None:

        row = SQLiteEvidenceMapper.to_row(evidence)

        self.database.execute(
            """
            INSERT INTO evidence (
                id,
                project_id,
                source,
                origin_id,
                title,
                url,
                content,
                confidence,
                metadata,
                discovered_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["project_id"],
                row["source"],
                row["origin_id"],
                row["title"],
                row["url"],
                row["content"],
                row["confidence"],
                row["metadata"],
                row["discovered_at"],
            ),
        )

    def update(
        self,
        evidence: Evidence,
    ) -> None:

        row = SQLiteEvidenceMapper.to_row(evidence)

        self.database.execute(
            """
            UPDATE evidence
            SET
                project_id=?,
                source=?,
                origin_id=?,
                title=?,
                url=?,
                content=?,
                confidence=?,
                metadata=?,
                discovered_at=?
            WHERE id=?
            """,
            (
                row["project_id"],
                row["source"],
                row["origin_id"],
                row["title"],
                row["url"],
                row["content"],
                row["confidence"],
                row["metadata"],
                row["discovered_at"],
                row["id"],
            ),
        )

    def get(
        self,
        evidence_id: EvidenceId,
    ) -> Evidence | None:

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence
            WHERE id = ?
            """,
            (str(evidence_id),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return SQLiteEvidenceMapper.from_row(row)

    def list(
        self,
    ) -> list[Evidence]:

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence
            ORDER BY discovered_at
            """
        )

        return [
            SQLiteEvidenceMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def remove(
        self,
        evidence_id: EvidenceId,
    ) -> None:

        self.database.execute(
            """
            DELETE
            FROM evidence
            WHERE id = ?
            """,
            (str(evidence_id),),
        )

    def exists(
        self,
        evidence_id: EvidenceId,
    ) -> bool:

        cursor = self.database.query(
            """
            SELECT 1
            FROM evidence
            WHERE id = ?
            LIMIT 1
            """,
            (str(evidence_id),),
        )

        return cursor.fetchone() is not None

    def clear(
        self,
    ) -> None:

        self.database.execute(
            """
            DELETE FROM evidence
            """
        )

    def count(
        self,
    ) -> int:

        cursor = self.database.query(
            """
            SELECT COUNT(*)
            FROM evidence
            """
        )

        return cursor.fetchone()[0]

    def get_by_project_id(
        self,
        project_id: ProjectId,
    ) -> list[Evidence]:

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence
            WHERE project_id = ?
            ORDER BY discovered_at
            """,
            (str(project_id),),
        )

        return [
            SQLiteEvidenceMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def get_by_origin_id(
        self,
        source: EvidenceSource,
        origin_id: str,
    ) -> list[Evidence]:

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence
            WHERE source = ?
              AND origin_id = ?
            ORDER BY discovered_at
            """,
            (
                source.value,
                origin_id,
            ),
        )

        return [
            SQLiteEvidenceMapper.from_row(row)
            for row in cursor.fetchall()
        ]