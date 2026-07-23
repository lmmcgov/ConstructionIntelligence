"""
Run project evidence discovery and persist results.

Workflow:

CLI Arguments
    |
    v
Project
    |
    v
SQLiteProjectRepository
    |
    v
SearXNGSearchProvider
    |
    v
FallbackExtractor
    |
    +--> HTMLExtractor
    |
    +--> GeminiExtractor
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

from __future__ import annotations

import argparse

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

from construction_intelligence.ingestion.web.searxng_search_provider import (
    SearXNGSearchProvider,
)

from construction_intelligence.ingestion.web.html_extractor import (
    HTMLExtractor,
)

from construction_intelligence.ingestion.web.gemini_extractor import (
    GeminiExtractor,
)

from construction_intelligence.ingestion.web.fallback_extractor import (
    FallbackExtractor,
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


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line project inputs.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Discover and persist evidence "
            "for a construction project."
        )
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Project name",
    )

    parser.add_argument(
        "--city",
        default=None,
        help="Project city",
    )

    parser.add_argument(
        "--state",
        default=None,
        help="Project state",
    )

    parser.add_argument(
        "--country",
        default="United States",
        help="Project country",
    )

    parser.add_argument(
        "--road-name",
        default=None,
        help="Project road name",
    )

    parser.add_argument(
        "--database",
        default="construction_intelligence.db",
        help="SQLite database path",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run and persist project evidence workflow.
    """

    args = parse_arguments()

    database = Database(
        args.database
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
    # Create project.
    #
    project = Project(
        name=args.name,
        description=(
            f"Construction project: {args.name}"
        ),
        road_name=args.road_name,
        city=args.city,
        state=args.state,
        country=args.country,
    )

    project_repository.add(
        project
    )

    #
    # Real web search through local SearXNG.
    #
    search_provider = (
        SearXNGSearchProvider()
    )

    discovery_service = (
        EvidenceDiscoveryService(
            search_provider
        )
    )

    #
    # Extraction pipeline:
    #
    # 1. Try HTML extraction.
    # 2. Fall back to Gemini extraction.
    #
    gemini_runner = (
        MockGeminiRunner()
    )

    extractor = (
        FallbackExtractor(
            primary=HTMLExtractor(),
            fallback=GeminiExtractor(
                runner=gemini_runner
            ),
        )
    )

    ingestion_service = (
        WebEvidenceIngestionService(
            discovery_service=discovery_service,
            extractor=extractor,
        )
    )

    evidence_records = (
        ingestion_service.ingest(
            project
        )
    )

    #
    # Persist evidence.
    #
    for evidence in evidence_records:

        evidence_repository.add(
            evidence
        )

    #
    # Evaluate and store evidence.
    #
    matcher = (
        GeminiEvidenceMatcherService(
            runner=gemini_runner,
        )
    )

    evaluator = (
        EvidenceEvaluationService(
            matcher=matcher,
            repository=evaluation_repository,
        )
    )

    print(
        "Project evidence search and store"
    )

    print(
        "----------------------------------"
    )

    print(
        f"Project: {project.name}"
    )

    print(
        f"Evidence discovered: "
        f"{len(evidence_records)}"
    )

    for evidence in evidence_records:

        evaluation = (
            evaluator.evaluate_and_store(
                project,
                evidence,
            )
        )

        print()

        print(
            f"Evidence: {evidence.title}"
        )

        print(
            f"URL: {evidence.url}"
        )

        print(
            f"Source: {evidence.source}"
        )

        print(
            f"Match score: "
            f"{evaluation.match_score}"
        )

        print(
            f"Quality score: "
            f"{evaluation.quality_score}"
        )

        print(
            f"Overall score: "
            f"{evaluation.overall_score:.2f}"
        )

        print(
            f"Resources stored: "
            f"{len(evaluation.resources)}"
        )

    database.close()

    print()

    print(
        "Project evidence search and store: PASS"
    )


if __name__ == "__main__":
    main()