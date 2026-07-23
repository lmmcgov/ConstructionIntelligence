"""
Integration test for SQLite repositories.
"""

from construction_intelligence.core.enums import (
    ConfidenceLevel,
    ProjectOrigin,
)
from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.project import Project
from construction_intelligence.database.schema.create_tables import (
    create_tables,
)
from construction_intelligence.database.sqlite import Database
from construction_intelligence.repositories.sqlite.sqlite_project_repository import (
    SQLiteProjectRepository,
)
from construction_intelligence.repositories.sqlite.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)


def main() -> None:
    """Test SQLite persistence."""

    database = Database(
        "test_construction_intelligence.db"
    )

    try:
        #
        # Create schema
        #
        create_tables(database)

        #
        # Create repositories
        #
        project_repository = SQLiteProjectRepository(
            database
        )

        evidence_repository = SQLiteEvidenceRepository(
            database
        )

        #
        # Create project
        #
        project = Project(
            name="Test Highway Construction",
            origin=ProjectOrigin.OSM,
            origin_id="test-osm-project-001",
            country="United States",
            state="Colorado",
            city="Grand Junction",
            road_name="Test Road",
        )

        project_repository.add(project)

        print(
            f"Projects after insert: "
            f"{project_repository.count()}"
        )

        #
        # Retrieve project
        #
        retrieved_project = (
            project_repository.get(
                project.id
            )
        )

        assert retrieved_project is not None
        assert (
            retrieved_project.name
            == "Test Highway Construction"
        )

        print(
            "Project retrieval: PASS"
        )

        #
        # Create evidence
        #
        evidence = Evidence(
            project_id=project.id,
            source=ProjectOrigin.OSM,
            origin_id="test-evidence-001",
            title="OSM Construction Tag",
            content="Test construction evidence.",
            confidence=ConfidenceLevel.HIGH,
            metadata={
                "highway": "construction",
            },
        )

        evidence_repository.add(evidence)

        print(
            f"Evidence after insert: "
            f"{evidence_repository.count()}"
        )

        #
        # Retrieve evidence
        #
        retrieved_evidence = (
            evidence_repository.get(
                evidence.id
            )
        )

        assert retrieved_evidence is not None
        assert (
            retrieved_evidence.title
            == "OSM Construction Tag"
        )

        print(
            "Evidence retrieval: PASS"
        )

        #
        # Query relationships
        #
        project_evidence = (
            evidence_repository.get_by_project_id(
                project.id
            )
        )

        assert len(project_evidence) == 1

        print(
            "Evidence-project relationship: PASS"
        )

        #
        # Test update
        #
        project.name = (
            "Updated Highway Construction"
        )

        project_repository.update(project)

        updated_project = (
            project_repository.get(
                project.id
            )
        )

        assert updated_project is not None
        assert (
            updated_project.name
            == "Updated Highway Construction"
        )

        print(
            "Project update: PASS"
        )

        print(
            "\nSQLite repository integration test: PASS"
        )

    finally:
        database.close()


if __name__ == "__main__":
    main()