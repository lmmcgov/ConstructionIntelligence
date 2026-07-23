"""
SQLite database manager.
"""

from pathlib import Path
import sqlite3


class Database:
    """Manages the SQLite connection."""

    def __init__(
        self,
        database_path: str = "construction_intelligence.db",
    ) -> None:
        self.database_path = Path(database_path)

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()

    def execute(
        self,
        sql: str,
        parameters: tuple = (),
    ) -> sqlite3.Cursor:
        """
        Execute a statement that modifies the database.

        Examples:
        - CREATE TABLE
        - INSERT
        - UPDATE
        - DELETE
        """

        cursor = self.connection.execute(
            sql,
            parameters,
        )

        self.connection.commit()

        return cursor

    def query(
        self,
        sql: str,
        parameters: tuple = (),
    ) -> sqlite3.Cursor:
        """
        Execute a read-only query.

        Examples:
        - SELECT
        """

        return self.connection.execute(
            sql,
            parameters,
        )