"""
SQLite implementation of the ProjectRepository.
"""

import sqlite3
from datetime import datetime
from uuid import UUID

from construction_intelligence.core.enums import (
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.project import Project
from construction_intelligence.database.sqlite import Database


class SQLiteProjectRepository:
    """Stores Project objects in SQLite."""

    def __init__(
        self,
        database: Database,
    ) -> None:
        self._database = database

    def add(
        self,
        project: Project,
    ) -> None:
        """Insert a new project into the database."""

        self._database.execute(
            """
            INSERT INTO projects (
                id,
                name,
                description,
                status,
                category,
                origin,
                origin_id,
                road_name,
                road_ref,
                created_at,
                updated_at,
                last_seen
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
            """,
            (
                str(project.id),
                project.name,
                project.description,
                project.status.value,
                project.category.value,
                project.origin.value,
                project.origin_id,
                project.road_name,
                project.road_ref,
                project.created_at.isoformat(),
                project.updated_at.isoformat(),
                project.last_seen.isoformat(),
            ),
        )

    def get(
        self,
        project_id: UUID,
    ) -> Project | None:
        """Retrieve a project by its identifier."""

        cursor = self._database.query(
            """
            SELECT *
            FROM projects
            WHERE id = ?;
            """,
            (str(project_id),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_project(row)

    def get_by_origin_id(
        self,
        origin: ProjectOrigin,
        origin_id: str,
    ) -> Project | None:
        """Retrieve a project by its source identifier."""

        cursor = self._database.query(
            """
            SELECT *
            FROM projects
            WHERE origin = ?
              AND origin_id = ?;
            """,
            (
                origin.value,
                origin_id,
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_project(row)

    def list_all(
        self,
    ) -> list[Project]:
        """Return all projects in the database."""

        cursor = self._database.query(
            """
            SELECT *
            FROM projects
            ORDER BY created_at;
            """
        )

        return [
            self._row_to_project(row)
            for row in cursor.fetchall()
        ]

    def update(
        self,
        project: Project,
    ) -> None:
        """Update an existing project."""

        self._database.execute(
            """
            UPDATE projects
            SET
                name = ?,
                description = ?,
                status = ?,
                category = ?,
                origin = ?,
                origin_id = ?,
                road_name = ?,
                road_ref = ?,
                created_at = ?,
                updated_at = ?,
                last_seen = ?
            WHERE id = ?;
            """,
            (
                project.name,
                project.description,
                project.status.value,
                project.category.value,
                project.origin.value,
                project.origin_id,
                project.road_name,
                project.road_ref,
                project.created_at.isoformat(),
                project.updated_at.isoformat(),
                project.last_seen.isoformat(),
                str(project.id),
            ),
        )

    def delete(
        self,
        project_id: UUID,
    ) -> None:
        """Delete a project."""

        self._database.execute(
            """
            DELETE FROM projects
            WHERE id = ?;
            """,
            (str(project_id),),
        )

    @staticmethod
    def _row_to_project(
        row: sqlite3.Row,
    ) -> Project:
        """Convert a SQLite row into a Project."""

        return Project(
            id=UUID(row["id"]),
            name=row["name"],
            description=row["description"],
            status=ProjectStatus(row["status"]),
            category=ProjectCategory(row["category"]),
            origin=ProjectOrigin(row["origin"]),
            origin_id=row["origin_id"],
            road_name=row["road_name"],
            road_ref=row["road_ref"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
            last_seen=datetime.fromisoformat(
                row["last_seen"]
            ),
        )