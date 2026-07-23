"""
Test SQLiteEvidenceEvaluationRepository behavior.
"""

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.enums import (
    ConfidenceLevel,
    ProjectOrigin,
)
from construction_intelligence.core.evidence_evaluation import (
    EvidenceEvaluation,
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


def main() -> None:
    """Run repository persistence test."""

    database = Database(
        "test_evidence_evaluation.db"
    )

    try:
        #
        # Create database schema.
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
        # Create parent project.
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
        # Create parent evidence.
        #
        evidence = Evidence(
            project_id=project.id,
            source=ProjectOrigin.OSM,
            origin_id="osm-evidence-123",
            title="Horizon Glen Drive construction",
            content=(
                "Construction project evidence "
                "for Horizon Glen Drive."
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
        # Create evaluation.
        #
        evaluation = EvidenceEvaluation(
            project_id=project.id,
            evidence_id=evidence.id,
            match_score=0.95,
            quality_score=0.90,
            reasons=(
                "Project name appears in evidence title",
                "Source quality is high",
            ),
        )

        #
        # Store evaluation.
        #
        evaluation_repository.add(
            evaluation
        )

        print(
            "Evidence evaluation repository test"
        )
        print(
            "----------------------------------"
        )

        count = evaluation_repository.count()

        print(
            f"Evaluation count: {count}"
        )

        assert count == 1

        #
        # Retrieve evaluation.
        #
        results = (
            evaluation_repository.get_by_project_id(
                project.id
            )
        )

        assert len(results) == 1

        retrieved = results[0]

        print(
            f"Match score: "
            f"{retrieved.match_score:.2f}"
        )

        print(
            f"Quality score: "
            f"{retrieved.quality_score:.2f}"
        )

        print(
            f"Overall score: "
            f"{retrieved.overall_score:.2f}"
        )

        print(
            "Reasons:"
        )

        for reason in retrieved.reasons:
            print(
                f"- {reason}"
            )

        assert retrieved.project_id == project.id
        assert retrieved.evidence_id == evidence.id

        assert retrieved.match_score == 0.95
        assert retrieved.quality_score == 0.90

        assert len(
            retrieved.reasons
        ) == 2

        print(
            "\nEvidence evaluation repository test: PASS"
        )

    finally:
        database.close()


if __name__ == "__main__":
    main()