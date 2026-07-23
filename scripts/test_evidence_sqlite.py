"""
CRUD test for SQLiteEvidenceRepository.
"""

from construction_intelligence.core.enums import (
    ConfidenceLevel,
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)
from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.project import Project
from construction_intelligence.database.schema.create_tables import create_tables
from construction_intelligence.database.sqlite import Database
from construction_intelligence.repositories.sqlite.evidence_repository import (
    SQLiteEvidenceRepository,
)
from construction_intelligence.repositories.sqlite.project_repository import (
    SQLiteProjectRepository,
)


def main() -> None:
    database = Database("construction_intelligence.db")
    create_tables(database)

    project_repository = SQLiteProjectRepository(database)
    evidence_repository = SQLiteEvidenceRepository(database)

    # Ensure a clean database before testing.
    database.execute("DELETE FROM evidence;")
    database.execute("DELETE FROM projects;")

    try:
        project = Project(
            name="Test Project",
            description="Repository test",
            status=ProjectStatus.UNDER_CONSTRUCTION,
            category=ProjectCategory.ROAD,
            origin=ProjectOrigin.OSM,
            origin_id="test-project",
        )

        project_repository.add(project)
        print("✓ Project created")

        evidence = Evidence(
            project_id=project.id,
            source=ProjectOrigin.OSM,
            origin_id="way/12345",
            title="Construction Way",
            url="https://www.openstreetmap.org/way/12345",
            content="highway=construction",
            confidence=ConfidenceLevel.HIGH,
            metadata={"highway": "construction"},
        )

        evidence_repository.add(evidence)
        print("✓ Evidence created")

        loaded = evidence_repository.get(evidence.id)

        assert loaded is not None
        assert loaded.title == evidence.title

        print("✓ Evidence loaded")

        loaded.title = "Updated Title"

        evidence_repository.update(loaded)

        updated = evidence_repository.get(evidence.id)

        assert updated is not None
        assert updated.title == "Updated Title"

        print("✓ Evidence updated")

        evidence_list = evidence_repository.list_all()

        assert len(evidence_list) == 1

        print(
            f"✓ Repository contains {len(evidence_list)} evidence record(s)"
        )

        evidence_repository.delete(evidence.id)

        assert evidence_repository.get(evidence.id) is None

        print("✓ Evidence deleted")

        project_repository.delete(project.id)

        print("\nCRUD test completed successfully.")

    finally:
        # Always leave the database clean.
        database.execute("DELETE FROM evidence;")
        database.execute("DELETE FROM projects;")
        database.close()


if __name__ == "__main__":
    main()