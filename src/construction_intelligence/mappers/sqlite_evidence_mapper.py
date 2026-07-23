"""
SQLite mapper for Evidence domain objects.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import EvidenceSource
from construction_intelligence.core.enums import ConfidenceLevel
from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)


class SQLiteEvidenceMapper:
    """Maps Evidence objects to and from SQLite rows."""

    @staticmethod
    def to_row(
        evidence: Evidence,
    ) -> dict[str, object]:
        """Convert Evidence into a SQLite-compatible dictionary."""

        return {
            "id": str(evidence.id),
            "project_id": str(evidence.project_id),

            "source": evidence.source.value,
            "origin_id": evidence.origin_id,

            "title": evidence.title,
            "url": evidence.url,
            "content": evidence.content,

            "confidence": evidence.confidence.value,

            "metadata": json.dumps(
                evidence.metadata
            ),

            "discovered_at": (
                evidence.discovered_at.isoformat()
            ),
        }

    @staticmethod
    def from_row(
        row: sqlite3.Row,
    ) -> Evidence:
        """Convert a SQLite row into an Evidence object."""

        return Evidence(
            id=EvidenceId(
                row["id"]
            ),

            project_id=ProjectId(
                row["project_id"]
            ),

            source=EvidenceSource(
                row["source"]
            ),

            origin_id=row["origin_id"],

            title=row["title"],

            url=row["url"],

            content=row["content"],

            confidence=ConfidenceLevel(
                row["confidence"]
            ),

            metadata=json.loads(
                row["metadata"]
            )
            if row["metadata"]
            else {},

            discovered_at=datetime.fromisoformat(
                row["discovered_at"]
            ),
        )