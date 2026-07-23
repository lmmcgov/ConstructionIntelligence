"""
SQLite implementation of the EvidenceEvaluation repository.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from uuid import UUID

from construction_intelligence.core.evidence_evaluation import (
    EvidenceEvaluation,
)

from construction_intelligence.core.evidence_evaluation_status import (
    EvidenceEvaluationStatus,
)

from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)

from construction_intelligence.database.sqlite import (
    Database,
)

from construction_intelligence.repositories.sqlite.sqlite_evidence_resource_repository import (
    SQLiteEvidenceResourceRepository,
)


class SQLiteEvidenceEvaluationRepository:
    """
    SQLite-backed repository for EvidenceEvaluation objects.
    """

    def __init__(
        self,
        database: Database,
    ) -> None:

        self.database = database

        self.resource_repository = (
            SQLiteEvidenceResourceRepository(
                database
            )
        )

    def add(
        self,
        evaluation: EvidenceEvaluation,
    ) -> None:
        """
        Insert a new evidence evaluation
        and supporting resources.
        """

        evaluation_id = str(
            evaluation.id
        )

        self.database.execute(
            """
            INSERT INTO evidence_evaluations (
                id,
                project_id,
                evidence_id,
                match_score,
                quality_score,
                overall_score,
                status,
                reasons,
                evaluated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evaluation_id,
                str(evaluation.project_id),
                str(evaluation.evidence_id),
                evaluation.match_score,
                evaluation.quality_score,
                evaluation.overall_score,
                evaluation.status.value,
                json.dumps(
                    list(evaluation.reasons)
                ),
                evaluation.evaluated_at.isoformat(),
            ),
        )

        self.resource_repository.add_many(
            evaluation_id,
            evaluation.resources,
        )

    def get(
        self,
        evaluation_id: UUID,
    ) -> EvidenceEvaluation | None:
        """
        Retrieve an evaluation by ID.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            WHERE id = ?
            """,
            (
                str(evaluation_id),
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_evaluation(row)

    def get_by_project_id(
        self,
        project_id: ProjectId,
    ) -> list[EvidenceEvaluation]:
        """
        Return all evaluations for a project.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            WHERE project_id = ?
            ORDER BY overall_score DESC
            """,
            (
                str(project_id),
            ),
        )

        return [
            self._row_to_evaluation(row)
            for row in cursor.fetchall()
        ]

    def get_by_evidence_id(
        self,
        evidence_id: EvidenceId,
    ) -> list[EvidenceEvaluation]:
        """
        Return all evaluations for an evidence record.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            WHERE evidence_id = ?
            ORDER BY overall_score DESC
            """,
            (
                str(evidence_id),
            ),
        )

        return [
            self._row_to_evaluation(row)
            for row in cursor.fetchall()
        ]

    def get_top_evaluations(
        self,
        limit: int = 10,
        minimum_score: float = 0.0,
    ) -> list[EvidenceEvaluation]:
        """
        Return highest-confidence evidence evaluations.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            WHERE overall_score >= ?
            ORDER BY overall_score DESC
            LIMIT ?
            """,
            (
                minimum_score,
                limit,
            ),
        )

        return [
            self._row_to_evaluation(row)
            for row in cursor.fetchall()
        ]

    def get_by_status(
        self,
        status: EvidenceEvaluationStatus,
    ) -> list[EvidenceEvaluation]:
        """
        Return evaluations matching a confidence status.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            WHERE status = ?
            ORDER BY overall_score DESC
            """,
            (
                status.value,
            ),
        )

        return [
            self._row_to_evaluation(row)
            for row in cursor.fetchall()
        ]

    def get_low_confidence_evaluations(
        self,
        maximum_score: float = 0.50,
        limit: int = 10,
    ) -> list[EvidenceEvaluation]:
        """
        Return evaluations needing additional research.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            WHERE overall_score <= ?
            ORDER BY overall_score ASC
            LIMIT ?
            """,
            (
                maximum_score,
                limit,
            ),
        )

        return [
            self._row_to_evaluation(row)
            for row in cursor.fetchall()
        ]

    def list_all(
        self,
    ) -> list[EvidenceEvaluation]:
        """
        Return all evidence evaluations.
        """

        cursor = self.database.query(
            """
            SELECT *
            FROM evidence_evaluations
            ORDER BY overall_score DESC
            """
        )

        return [
            self._row_to_evaluation(row)
            for row in cursor.fetchall()
        ]

    def delete(
        self,
        evaluation_id: UUID,
    ) -> None:
        """
        Delete an evaluation.
        """

        self.database.execute(
            """
            DELETE FROM evidence_evaluations
            WHERE id = ?
            """,
            (
                str(evaluation_id),
            ),
        )

    def count(
        self,
    ) -> int:
        """
        Return number of evaluations.
        """

        cursor = self.database.query(
            """
            SELECT COUNT(*)
            FROM evidence_evaluations
            """
        )

        return cursor.fetchone()[0]

    def _row_to_evaluation(
        self,
        row: sqlite3.Row,
    ) -> EvidenceEvaluation:
        """
        Convert SQLite row into EvidenceEvaluation.
        """

        resources = (
            self.resource_repository
            .get_by_evaluation_id(
                row["id"]
            )
        )

        return EvidenceEvaluation(
            id=row["id"],
            project_id=UUID(
                row["project_id"]
            ),
            evidence_id=UUID(
                row["evidence_id"]
            ),
            match_score=row["match_score"],
            quality_score=row["quality_score"],
            reasons=tuple(
                json.loads(
                    row["reasons"]
                )
                if row["reasons"]
                else []
            ),
            resources=tuple(
                resources
            ),
            evaluated_at=datetime.fromisoformat(
                row["evaluated_at"]
            ),
        )