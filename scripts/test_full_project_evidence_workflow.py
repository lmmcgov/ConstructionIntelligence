"""
Test full project evidence workflow.

Pipeline:

Project
    |
    v
SQLiteProjectRepository
    |
    v
EvidenceDiscoveryService
    |
    v
MockSearchProvider
    |
    v
WebEvidenceIngestionService
    |
    v
Evidence
    |
    v
SQLiteEvidenceRepository
    |
    v
GeminiEvidenceMatcherService
    |
    v
EvidenceEvaluationService
    |
    v
SQLiteEvidenceEvaluationRepository
    |
    +--> evidence_evaluations
    |
    +--> evidence_resources
"""

from pathlib import Path
import tempfile

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.database.sqlite import (
    Database,
)

from construction_intelligence.database.schema.create_tables import (
    create_tables,
)

from construction_intelligence.ingestion.web.evidence_discovery_service import (
    EvidenceDiscoveryService,
)

from construction_intelligence.ingestion.web.mock_search_provider import (
    MockSearchProvider,
)

from construction_intelligence.ingestion.web.mock_extractor import (
    MockWebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)

from construction_intelligence.ingestion.web.web_evidence_ingestion_service import (
    WebEvidenceIngestionService,
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
    Test complete project-to-evaluation workflow.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        database_path = (
            Path(temp_dir)
            /
            "test.db"
        )

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

        #
        # Create project candidate.
        #
        project = Project(
            name="Horizon Glen Drive Improvements",
            description=(
                "Road reconstruction project "
                "in Grand Junction."
            ),
            road_name="Horizon Glen Drive",
            city="Grand Junction",
            state="Colorado",
            country="United States",
        )

        #
        # Persist project before evidence.
        #
        project_repository.add(
            project
        )

        #
        # Mock web search.
        #
        url = (
            "https://grandjunction.gov/projects/horizon"
        )

        search_provider = MockSearchProvider(
            results={
                '"Horizon Glen Drive Improvements"': [
                    url
                ],
                '"Horizon Glen Drive" construction': [
                    url
                ],
                '"Horizon Glen Drive Improvements" Grand Junction': [
                    url
                ],
            }
        )

        discovery_service = (
            EvidenceDiscoveryService(
                search_provider
            )
        )

        #
        # Mock page extraction.
        #
        extractor = MockWebExtractor(
            documents={
                url: RawWebDocument(
                    url=url,
                    title=(
                        "Horizon Glen Drive Improvements"
                    ),
                    content=(
                        "The City of Grand Junction "
                        "announced Horizon Glen Drive "
                        "Improvements. Construction "
                        "begins in summer 2026."
                    ),
                    source_name=(
                        "City of Grand Junction"
                    ),
                )
            }
        )

        ingestion_service = (
            WebEvidenceIngestionService(
                discovery_service=discovery_service,
                extractor=extractor,
            )
        )

        #
        # Discover and create evidence.
        #
        evidence_records = (
            ingestion_service.ingest(
                project
            )
        )

        assert len(
            evidence_records
        ) == 1

        evidence = evidence_records[0]

        #
        # Persist evidence.
        #
        evidence_repository.add(
            evidence
        )

        #
        # Gemini evaluation.
        #
        matcher = (
            GeminiEvidenceMatcherService(
                runner=MockGeminiRunner(),
            )
        )

        evaluator = (
            EvidenceEvaluationService(
                matcher=matcher,
                repository=evaluation_repository,
            )
        )

        evaluation = (
            evaluator.evaluate_and_store(
                project,
                evidence,
            )
        )

        stored = (
            evaluation_repository.get(
                evaluation.id
            )
        )

        assert stored is not None

        print(
            f"Match score: {stored.match_score}"
        )

        print(
            f"Quality score: {stored.quality_score}"
        )

        print(
            f"Overall score: {stored.overall_score}"
        )

        #
        # Validate evaluation quality.
        #
        # Gemini should strongly identify the
        # correct project.
        #
        assert stored.match_score >= 0.90

        #
        # Web-discovered evidence begins with
        # medium confidence.
        #
        assert stored.quality_score >= 0.50

        #
        # Combined confidence should remain meaningful.
        #
        assert stored.overall_score >= 0.50

        assert len(
            stored.resources
        ) == 1

        resource = stored.resources[0]

        print(
            "Full project evidence workflow test"
        )
        print(
            "-----------------------------------"
        )

        print(
            f"Evidence created: {evidence.title}"
        )

        print(
            f"Evaluation score: {stored.overall_score:.2f}"
        )

        print(
            f"Resources stored: {len(stored.resources)}"
        )

        print()
        print(
            "Resource:"
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

        print(
            "\nFull project evidence workflow test: PASS"
        )

        database.close()


if __name__ == "__main__":
    main()