"""
Test EvidenceEvaluationService persistence behavior.
"""

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.enums import (
    ConfidenceLevel,
    ProjectOrigin,
)
from construction_intelligence.core.project import Project
from construction_intelligence.database.schema.create_tables import (
    create_tables,
)
from construction_intelligence.database.sqlite import Database
from construction_intelligence.repositories.sqlite.sqlite_evidence_evaluation_repository import (
    SQLiteEvidenceEvaluationRepository,
)
from construction_intelligence.repositories.sqlite.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)
from construction_intelligence.repositories.sqlite.sqlite_project_repository import (
    SQLiteProjectRepository,
)
from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)


def main() -> None:
    """Run evaluation persistence test."""

    database = Database(
        "test_evidence_evaluation_service.db"
    )

    try:
        #
        # Create schema.
        #
        create_tables(
            database
        )

        #
        # Create repositories.
        #
        project_repository = SQLiteProjectRepository(
            database
        )

        evidence_repository = SQLiteEvidenceRepository(
            database
        )

        evaluation_repository = (
            SQLiteEvidenceEvaluationRepository(
                database
            )
        )

        #
        # Create project.
        #
        project = Project(
            name="Horizon Glen Drive",
            origin=ProjectOrigin.OSM,
            origin_id="osm-project-123",
            city="Grand Junction",
            road_name="Horizon Glen Drive",
        )

        project_repository.add(
            project
        )

        #
        # Create evidence.
        #
        evidence = Evidence(
            project_id=project.id,
            source=ProjectOrigin.OSM,
            origin_id="osm-evidence-123",
            title=(
                "Horizon Glen Drive construction project"
            ),
            content=(
                "Grand Junction approved construction "
                "of Horizon Glen Drive."
            ),
            confidence=ConfidenceLevel.HIGH,
            metadata={
                "construction_type": "road",
            },
        )

        evidence_repository.add(
            evidence
        )

        #
        # Create evaluation service with persistence.
        #
        service = EvidenceEvaluationService(
            repository=evaluation_repository,
        )

        #
        # Evaluate and store.
        #
        evaluation = service.evaluate_and_store(
            project,
            evidence,
        )

        print(
            "Evidence evaluation service persistence test"
        )
        print(
            "-------------------------------------------"
        )

        print(
            f"Match score: "
            f"{evaluation.match_score:.2f}"
        )

        print(
            f"Quality score: "
            f"{evaluation.quality_score:.2f}"
        )

        print(
            f"Overall score: "
            f"{evaluation.overall_score:.2f}"
        )

        #
        # Confirm database persistence.
        #
        stored = (
            evaluation_repository.get_by_project_id(
                project.id
            )
        )

        print(
            f"Stored evaluations: {len(stored)}"
        )

        assert len(stored) == 1

        retrieved = stored[0]

        assert (
            retrieved.project_id
            == project.id
        )

        assert (
            retrieved.evidence_id
            == evidence.id
        )

        assert (
            retrieved.match_score
            == evaluation.match_score
        )

        assert (
            retrieved.quality_score
            == evaluation.quality_score
        )

        print(
            "\nEvidence evaluation service persistence test: PASS"
        )

    finally:
        database.close()


if __name__ == "__main__":
    main()