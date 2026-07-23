"""
Test Gemini evidence resource persistence.

Pipeline:

Project
    |
Evidence
    |
GeminiEvidenceMatcherService
    |
EvidenceEvaluationService
    |
SQLiteEvidenceEvaluationRepository
    |
    +--> evidence_evaluations
    |
    +--> evidence_resources
"""

from pathlib import Path
import tempfile

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.enums import (
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.database.sqlite import (
    Database,
)

from construction_intelligence.database.schema.create_tables import (
    create_tables,
)

from construction_intelligence.integrations.gemini_cli.mock_runner import (
    MockGeminiRunner,
)

from construction_intelligence.repositories.sqlite.sqlite_project_repository import (
    SQLiteProjectRepository,
)

from construction_intelligence.repositories.sqlite.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)

from construction_intelligence.repositories.sqlite.sqlite_evidence_evaluation_repository import (
    SQLiteEvidenceEvaluationRepository,
)

from construction_intelligence.services.gemini_evidence_matcher_service import (
    GeminiEvidenceMatcherService,
)

from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)


def main() -> None:
    """
    Test Gemini resources are persisted.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        database_path = Path(
            temp_dir
        ) / "test.db"

        database = Database(
            str(database_path)
        )

        create_tables(
            database
        )

        project_repository = (
            SQLiteProjectRepository(
                database
            )
        )

        evidence_repository = (
            SQLiteEvidenceRepository(
                database
            )
        )

        evaluation_repository = (
            SQLiteEvidenceEvaluationRepository(
                database
            )
        )

        project = Project(
            name="Horizon Glen Drive Improvements",
            description=(
                "Road reconstruction project "
                "in Grand Junction."
            ),
            status=ProjectStatus.UNDER_CONSTRUCTION,
            category=ProjectCategory.ROAD,
            origin=ProjectOrigin.OSM,
            origin_id="way/123456",
            road_name="Horizon Glen Drive",
            road_ref=None,
            country="United States",
            state="Colorado",
            city="Grand Junction",
            latitude=39.0639,
            longitude=-108.5506,
        )

        project_repository.add(
            project
        )

        evidence = Evidence(
            project_id=project.id,
            source="government_record",
            origin_id=None,
            title=(
                "Horizon Glen Drive Improvements"
            ),
            url=(
                "https://grandjunction.gov/projects/horizon"
            ),
            content=(
                "The City of Grand Junction announced "
                "Horizon Glen Drive Improvements. "
                "Construction begins in summer 2026."
            ),
            confidence="high",
            metadata={
                "source_type": "government_page"
            },
        )

        evidence_repository.add(
            evidence
        )

        matcher = GeminiEvidenceMatcherService(
            runner=MockGeminiRunner(),
        )

        evaluator = EvidenceEvaluationService(
            matcher=matcher,
            repository=evaluation_repository,
        )

        evaluation = evaluator.evaluate_and_store(
            project,
            evidence,
        )

        stored = evaluation_repository.get(
            evaluation.id
        )

        assert stored is not None

        assert len(
            stored.resources
        ) == 1

        resource = stored.resources[0]

        print(
            "Gemini resource persistence test"
        )
        print(
            "--------------------------------"
        )

        print(
            f"Evaluation stored: {stored is not None}"
        )

        print(
            f"Resources found: {len(stored.resources)}"
        )

        print(
            "\nResource:"
        )

        print(
            f"- {resource.source_name}"
        )

        print(
            f"  Title: {resource.title}"
        )

        print(
            f"  URL: {resource.url}"
        )

        assert (
            resource.source_name
            ==
            "City of Grand Junction"
        )

        assert (
            resource.title
            ==
            "Horizon Glen Drive Improvements"
        )

        assert (
            resource.url
            ==
            "https://grandjunction.gov/projects/horizon"
        )

        print(
            "\nGemini resource persistence test: PASS"
        )

        database.close()


if __name__ == "__main__":
    main()