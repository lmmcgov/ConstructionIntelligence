from construction_intelligence.core.project import Project
from construction_intelligence.database.sqlite import Database
from construction_intelligence.repositories.sqlite.project_repository import (
    SQLiteProjectRepository,
)


def main() -> None:
    database = Database()
    repository = SQLiteProjectRepository(database)

    #
    # CREATE
    #
    project = Project(
        name="Test Project",
        description="Created by CRUD test.",
    )

    repository.add(project)
    print("✓ Project created")

    #
    # READ
    #
    loaded = repository.get(project.id)

    assert loaded is not None
    assert loaded.id == project.id
    assert loaded.name == "Test Project"

    print("✓ Project loaded")

    #
    # UPDATE
    #
    loaded.name = "Updated Project"
    loaded.description = "Repository update successful."

    loaded.touch()

    repository.update(loaded)

    updated = repository.get(project.id)

    assert updated is not None
    assert updated.name == "Updated Project"
    assert updated.description == "Repository update successful."

    print("✓ Project updated")

    #
    # LIST
    #
    projects = repository.list_all()

    assert any(p.id == project.id for p in projects)

    print(f"✓ Repository contains {len(projects)} project(s)")

    #
    # DELETE
    #
    repository.delete(project.id)

    deleted = repository.get(project.id)

    assert deleted is None

    print("✓ Project deleted")

    database.close()

    print("\nCRUD test completed successfully.")


if __name__ == "__main__":
    main()