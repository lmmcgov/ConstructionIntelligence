"""
Initialize the Construction Intelligence SQLite database.
"""

from __future__ import annotations

from construction_intelligence.database.schema.create_tables import create_tables
from construction_intelligence.database.sqlite import Database


def main() -> None:
    """Create all database tables."""

    database = Database()

    try:
        create_tables(database)
        print("Database created successfully.")
    finally:
        database.close()


if __name__ == "__main__":
    main()