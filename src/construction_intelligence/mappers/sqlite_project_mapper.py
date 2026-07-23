"""
SQLite mapper for Project domain objects.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from construction_intelligence.core.enums import (
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.ids import ProjectId
from construction_intelligence.core.project import Project


class SQLiteProjectMapper:
    """Maps Project objects to and from SQLite rows."""

    @staticmethod
    def to_row(project: Project) -> dict[str, object]:
        """Convert a Project into a SQLite-compatible dictionary."""

        return {
            "id": str(project.id),
            "name": project.name,
            "description": project.description,
            "status": project.status.value,
            "category": project.category.value,
            "origin": project.origin.value,
            "origin_id": project.origin_id,
            "road_name": project.road_name,
            "road_ref": project.road_ref,
            "country": project.country,
            "state": project.state,
            "city": project.city,
            "latitude": project.latitude,
            "longitude": project.longitude,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
            "last_seen": project.last_seen.isoformat(),
        }

    @staticmethod
    def from_row(row: sqlite3.Row) -> Project:
        """Convert a SQLite row into a Project."""

        return Project(
            id=ProjectId(row["id"]),
            name=row["name"],
            description=row["description"],
            status=ProjectStatus(row["status"]),
            category=ProjectCategory(row["category"]),
            origin=ProjectOrigin(row["origin"]),
            origin_id=row["origin_id"],
            road_name=row["road_name"],
            road_ref=row["road_ref"],
            country=row["country"],
            state=row["state"],
            city=row["city"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            last_seen=datetime.fromisoformat(row["last_seen"]),
        )