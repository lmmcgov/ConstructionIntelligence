"""
SQLite implementation of EvidenceResource repository.
"""

from __future__ import annotations

import sqlite3
from uuid import UUID

from construction_intelligence.core.evidence_resource import (
    EvidenceResource,
)
from construction_intelligence.database.sqlite import Database


class SQLiteEvidenceResourceRepository:
    """
    Stores external resources supporting evaluations.
    """

    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database

    def add(
        self,
        evaluation_id: UUID | str,
        resource: EvidenceResource,
    ) -> None:
        """
        Store a supporting resource.
        """

        self.database.execute(
            """
            INSERT INTO evidence_resources (
                id,
                evaluation_id,
                url,
                title,
                source_name,
                resource_type,
                excerpt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resource.id,
                str(evaluation_id),
                resource.url,
                resource.title,
                resource.source_name,
                resource.resource_type,
                resource.excerpt,
            ),
        )

    def add_many(
        self,
        evaluation_id: UUID | str,
        resources: tuple[EvidenceResource, ...],
    ) -> None:
        """
        Store multiple supporting resources.
        """

        for resource in resources:
            self.add(
                evaluation_id,
                resource,
            )

    def get_by_evaluation_id(
        self,
        evaluation_id: UUID | str,
    ) -> list[EvidenceResource]:
        """
        Retrieve all resources for an evaluation.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_resources
            WHERE evaluation_id = ?
            """,
            (
                str(evaluation_id),
            ),
        )

        return [
            self._row_to_resource(row)
            for row in cursor.fetchall()
        ]

    @staticmethod
    def _row_to_resource(
        row: sqlite3.Row,
    ) -> EvidenceResource:

        return EvidenceResource(
            id=row["id"],
            url=row["url"],
            title=row["title"],
            source_name=row["source_name"],
            resource_type=row["resource_type"],
            excerpt=row["excerpt"],
        )