"""
SQLite implementation of the Project repository.
"""

from __future__ import annotations

from construction_intelligence.core.enums import (
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.ids import ProjectId
from construction_intelligence.core.project import Project
from construction_intelligence.database.sqlite import Database
from construction_intelligence.mappers.sqlite_project_mapper import (
    SQLiteProjectMapper,
)
from construction_intelligence.repositories.project_repository import (
    ProjectRepository,
)


class SQLiteProjectRepository(ProjectRepository):
    """SQLite-backed repository for Project objects."""

    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database

    def add(
        self,
        project: Project,
    ) -> None:

        row = SQLiteProjectMapper.to_row(project)

        self.database.execute(
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
                country,
                state,
                city,
                latitude,
                longitude,
                created_at,
                updated_at,
                last_seen
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                row["id"],
                row["name"],
                row["description"],
                row["status"],
                row["category"],
                row["origin"],
                row["origin_id"],
                row["road_name"],
                row["road_ref"],
                row["country"],
                row["state"],
                row["city"],
                row["latitude"],
                row["longitude"],
                row["created_at"],
                row["updated_at"],
                row["last_seen"],
            ),
        )

    def update(
        self,
        project: Project,
    ) -> None:

        row = SQLiteProjectMapper.to_row(project)

        self.database.execute(
            """
            UPDATE projects
            SET
                name=?,
                description=?,
                status=?,
                category=?,
                origin=?,
                origin_id=?,
                road_name=?,
                road_ref=?,
                country=?,
                state=?,
                city=?,
                latitude=?,
                longitude=?,
                created_at=?,
                updated_at=?,
                last_seen=?
            WHERE id=?
            """,
            (
                row["name"],
                row["description"],
                row["status"],
                row["category"],
                row["origin"],
                row["origin_id"],
                row["road_name"],
                row["road_ref"],
                row["country"],
                row["state"],
                row["city"],
                row["latitude"],
                row["longitude"],
                row["created_at"],
                row["updated_at"],
                row["last_seen"],
                row["id"],
            ),
        )

    def get(
        self,
        project_id: ProjectId,
    ) -> Project | None:

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE id = ?
            """,
            (str(project_id),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return SQLiteProjectMapper.from_row(row)

    def list(
        self,
    ) -> list[Project]:

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            ORDER BY created_at
            """
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def remove(
        self,
        project_id: ProjectId,
    ) -> None:

        self.database.execute(
            """
            DELETE
            FROM projects
            WHERE id = ?
            """,
            (str(project_id),),
        )

    def exists(
        self,
        project_id: ProjectId,
    ) -> bool:

        cursor = self.database.query(
            """
            SELECT 1
            FROM projects
            WHERE id = ?
            LIMIT 1
            """,
            (str(project_id),),
        )

        return cursor.fetchone() is not None

    def clear(
        self,
    ) -> None:

        self.database.execute(
            """
            DELETE FROM projects
            """
        )

    def count(
        self,
    ) -> int:

        cursor = self.database.query(
            """
            SELECT COUNT(*)
            FROM projects
            """
        )

        return cursor.fetchone()[0]

    def get_by_origin_id(
        self,
        origin: ProjectOrigin,
        origin_id: str,
    ) -> Project | None:

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE origin = ?
              AND origin_id = ?
            """,
            (
                origin.value,
                origin_id,
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return SQLiteProjectMapper.from_row(row)

    def get_by_road_name(
        self,
        road_name: str,
    ) -> list[Project]:
        """Return all projects matching a road name."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE road_name = ?
            ORDER BY created_at
            """,
            (road_name,),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def get_by_country(
        self,
        country: str,
    ) -> list[Project]:
        """Return all projects in the specified country."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE country = ?
            ORDER BY created_at
            """,
            (country,),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def get_by_state(
        self,
        state: str,
    ) -> list[Project]:
        """Return all projects in the specified state."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE state = ?
            ORDER BY created_at
            """,
            (state,),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def get_by_city(
        self,
        city: str,
    ) -> list[Project]:
        """Return all projects in the specified city."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE city = ?
            ORDER BY created_at
            """,
            (city,),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def get_by_status(
        self,
        status: ProjectStatus,
    ) -> list[Project]:
        """Return all projects with the specified status."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE status = ?
            ORDER BY created_at
            """,
            (status.value,),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def get_recently_seen(
        self,
        limit: int = 100,
    ) -> list[Project]:
        """Return projects ordered by most recently seen."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            ORDER BY last_seen DESC
            LIMIT ?
            """,
            (limit,),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]

    def search_by_name(
        self,
        name: str,
    ) -> list[Project]:
        """Search projects by name."""

        cursor = self.database.query(
            """
            SELECT *
            FROM projects
            WHERE name LIKE ?
            ORDER BY created_at
            """,
            (f"%{name}%",),
        )

        return [
            SQLiteProjectMapper.from_row(row)
            for row in cursor.fetchall()
        ]