"""
Test Project query capabilities.
"""

from construction_intelligence.database.sqlite import Database
from construction_intelligence.repositories.sqlite.sqlite_project_repository import (
    SQLiteProjectRepository,
)
from construction_intelligence.services.project_service import (
    ProjectService,
)


def main() -> None:
    database = Database()

    try:
        repository = SQLiteProjectRepository(
            database
        )

        service = ProjectService(
            repository
        )

        print("Total projects:")
        print(
            len(service.list_projects())
        )

        print("\nSearch by road name:")
        projects = service.get_projects_by_road_name(
            "I-70"
        )

        for project in projects:
            print(
                project.name
            )

        print("\nRecent projects:")
        projects = service.get_recent_projects(
            limit=5
        )

        for project in projects:
            print(
                project.name
            )

        print("\nSearch by name:")
        projects = service.search_projects(
            "road"
        )

        for project in projects:
            print(
                project.name
            )

    finally:
        database.close()


if __name__ == "__main__":
    main()