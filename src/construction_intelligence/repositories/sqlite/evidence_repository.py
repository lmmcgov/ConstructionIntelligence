"""
SQLite implementation of the EvidenceRepository.
"""

import json
import sqlite3
from datetime import datetime
from uuid import UUID

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.enums import (
    ConfidenceLevel,
)
from construction_intelligence.database.sqlite import Database


class SQLiteEvidenceRepository:
    """Stores Evidence objects in SQLite."""

    def __init__(
        self,
        database: Database,
    ) -> None:
        self._database = database

    def add(
        self,
        evidence: Evidence,
    ) -> None:
        """Insert a new evidence record."""

        self._database.execute(
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
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
            """,
            (
                str(evidence.id),
                str(evidence.project_id),
                evidence.source.value,
                evidence.origin_id,
                evidence.title,
                evidence.url,
                evidence.content,
                evidence.confidence.value,
                json.dumps(evidence.metadata),
                evidence.discovered_at.isoformat(),
            ),
        )

    def get(
        self,
        evidence_id: UUID,
    ) -> Evidence | None:
        """Retrieve evidence by its identifier."""

        cursor = self._database.query(
            """
            SELECT *
            FROM evidence
            WHERE id = ?;
            """,
            (str(evidence_id),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_evidence(row)

    def get_by_origin_id(
        self,
        origin_id: str,
    ) -> Evidence | None:
        """Retrieve evidence by its source identifier."""

        cursor = self._database.query(
            """
            SELECT *
            FROM evidence
            WHERE origin_id = ?;
            """,
            (origin_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_evidence(row)

    def list_all(
        self,
    ) -> list[Evidence]:
        """Return all evidence."""

        cursor = self._database.query(
            """
            SELECT *
            FROM evidence
            ORDER BY id;
            """
        )

        return [
            self._row_to_evidence(row)
            for row in cursor.fetchall()
        ]

    def update(
        self,
        evidence: Evidence,
    ) -> None:
        """Update an existing evidence record."""

        self._database.execute(
            """
            UPDATE evidence
            SET
                project_id = ?,
                source = ?,
                origin_id = ?,
                title = ?,
                url = ?,
                content = ?,
                confidence = ?,
                metadata = ?,
                discovered_at = ?
            WHERE id = ?;
            """,
            (
                str(evidence.project_id),
                evidence.source.value,
                evidence.origin_id,
                evidence.title,
                evidence.url,
                evidence.content,
                evidence.confidence.value,
                json.dumps(evidence.metadata),
                evidence.discovered_at.isoformat(),
                str(evidence.id),
            ),
        )

    def delete(
        self,
        evidence_id: UUID,
    ) -> None:
        """Delete evidence."""

        self._database.execute(
            """
            DELETE FROM evidence
            WHERE id = ?;
            """,
            (str(evidence_id),),
        )

    @staticmethod
    def _row_to_evidence(
        row: sqlite3.Row,
    ) -> Evidence:
        """Convert a SQLite row into an Evidence object."""

        return Evidence(
            id=UUID(row["id"]),
            project_id=UUID(row["project_id"]),
            source=EvidenceSource(row["source"]),
            origin_id=row["origin_id"],
            title=row["title"],
            url=row["url"],
            content=row["content"],
            confidence=ConfidenceLevel(row["confidence"]),
            metadata=(
                json.loads(row["metadata"])
                if row["metadata"]
                else {}
            ),
            discovered_at=datetime.fromisoformat(
                row["discovered_at"]
            ),
        )