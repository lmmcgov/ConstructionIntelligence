"""
Run evidence discovery and evaluation for a project.

Workflow:

Project
    |
    v
WebEvidenceIngestionService
    |
    v
Evidence
    |
    v
GeminiEvidenceMatcherService
    |
    v
EvidenceEvaluationService
"""

from __future__ import annotations

import argparse

from construction_intelligence.core.project import (
    Project,
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
            "Run web evidence discovery "
            "and Gemini evaluation for a project."
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
        help="Road name associated with project",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run evidence search for a project.
    """

    args = parse_arguments()

    #
    # Create project from command-line input.
    #
    # This can later be replaced with a project
    # loaded from a PBF file.
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

    #
    # Temporary mock search.
    #
    # This will later become a real search provider.
    #
    url = (
        "https://grandjunction.gov/projects/horizon"
    )

    search_provider = MockSearchProvider(
        results={
            f'"{project.name}"': [
                url
            ],
            f'"{project.road_name}" construction': [
                url
            ],
            f'"{project.name}" {project.city}': [
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
    # Temporary mock extractor.
    #
    extractor = MockWebExtractor(
        documents={
            url: RawWebDocument(
                url=url,
                title=project.name,
                content=(
                    f"The City of {project.city} "
                    f"announced {project.name}. "
                    "Construction begins in summer 2026."
                ),
                source_name=(
                    f"City of {project.city}"
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

    evidence_records = (
        ingestion_service.ingest(
            project
        )
    )

    matcher = (
        GeminiEvidenceMatcherService(
            runner=MockGeminiRunner(),
        )
    )

    evaluator = (
        EvidenceEvaluationService(
            matcher=matcher,
        )
    )

    print(
        "Project evidence search"
    )
    print(
        "-----------------------"
    )

    print(
        f"Project: {project.name}"
    )

    print(
        f"Location: "
        f"{project.city}, "
        f"{project.state}, "
        f"{project.country}"
    )

    print(
        f"Evidence found: {len(evidence_records)}"
    )

    for evidence in evidence_records:

        evaluation = (
            evaluator.evaluate(
                project,
                evidence,
            )
        )

        print()

        print(
            "Evidence:"
        )

        print(
            f"- {evidence.title}"
        )

        print(
            f"  URL: {evidence.url}"
        )

        print(
            f"  Match score: "
            f"{evaluation.match_score}"
        )

        print(
            f"  Quality score: "
            f"{evaluation.quality_score}"
        )

        print(
            f"  Overall score: "
            f"{evaluation.overall_score:.2f}"
        )

        print(
            "  Reasons:"
        )

        for reason in evaluation.reasons:
            print(
                f"    - {reason}"
            )


if __name__ == "__main__":
    main()