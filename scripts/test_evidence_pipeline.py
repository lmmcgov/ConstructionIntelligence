"""
Integration test for EvidencePipelineService using live web evidence.

Validates:

- Live URL discovery through SearXNG
- Search query generation
- Candidate ranking
- PDF/HTML extraction routing
- Evidence creation from external sources
- Evidence metadata extraction
- Evidence evaluation and scoring
- Evidence ranking by project relevance

This test verifies the end-to-end evidence discovery pipeline
using a real construction project search.
"""

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.web_evidence_ingestion_service import (
    WebEvidenceIngestionService,
)

from construction_intelligence.ingestion.web.evidence_discovery_service import (
    EvidenceDiscoveryService,
)

from construction_intelligence.ingestion.web.searxng_search_provider import (
    SearXNGSearchProvider,
)

from construction_intelligence.ingestion.web.search_context_provider import (
    SearchContextProvider,
)

from construction_intelligence.ingestion.web.search_query_generator import (
    SearchQueryGenerator,
)

from construction_intelligence.ingestion.web.fallback_extractor import (
    FallbackExtractor,
)

from construction_intelligence.ingestion.web.html_extractor import (
    HTMLExtractor,
)

from construction_intelligence.ingestion.web.pdf_extractor import (
    PDFExtractor,
)

from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)

from construction_intelligence.services.evidence_pipeline_service import (
    EvidencePipelineService,
)


def create_project() -> Project:
    """
    Create test project.
    """

    return Project(
        name="Horizon Glen Drive Improvements",

        aliases=[
            "Horizon Drive",
            "Horizon Drive and G Road",
            "Horizon Drive Roundabout",
            "Horizon Drive and G Road Roundabout",
        ],

        city="Grand Junction",

        state="Colorado",

        country="United States",

        road_name="Horizon Glen Drive",
    )


def test_pipeline() -> None:
    """
    Validate end-to-end evidence discovery and evaluation
    using live search discovery.
    """

    project = create_project()


    #
    # Live discovery stack.
    #
    discovery_service = EvidenceDiscoveryService(
        search_provider=SearXNGSearchProvider(),
        context_provider=SearchContextProvider(),
        query_generator=SearchQueryGenerator(),
    )


    #
    # Extraction stack.
    #
    extractor = FallbackExtractor(
        primary=HTMLExtractor(),
        fallback=HTMLExtractor(),
        pdf_extractor=PDFExtractor(),
    )


    ingestion_service = WebEvidenceIngestionService(
        discovery_service=discovery_service,
        extractor=extractor,
    )


    evaluation_service = EvidenceEvaluationService()


    pipeline = EvidencePipelineService(
        ingestion_service=ingestion_service,
        evaluation_service=evaluation_service,
    )


    results = pipeline.run(
        project
    )


    print()

    print(
        "Evidence pipeline results"
    )

    print(
        "-------------------------"
    )


    for result in results:

        print()

        print(
            result.evidence.title
        )

        print(
            result.evidence.url
        )

        print()

        print(
            "Metadata:"
        )

        for key, value in (
            result.evidence.metadata.items()
        ):

            print(
                f" - {key}: {value}"
            )


        print()

        print(
            f"Match score: "
            f"{result.score.match_score:.2f}"
        )

        print(
            f"Quality score: "
            f"{result.score.quality_score:.2f}"
        )

        print(
            f"Overall score: "
            f"{result.score.overall_score:.2f}"
        )

        print()

        print(
            "Reasons:"
        )

        for reason in result.score.reasons:

            print(
                f" - {reason}"
            )


    #
    # Discovery should return evidence.
    #
    assert len(results) > 0, (
        "No evidence returned from discovery pipeline"
    )


    #
    # Locate relevant Horizon Drive
    # construction evidence.
    #
    selected_result = None


    for result in results:

        evidence = (
            result.evidence
        )

        content = (
            evidence.content
            .lower()
        )


        construction_terms = [
            "construction",
            "improvement",
            "roundabout",
            "transportation",
            "infrastructure",
            "project",
        ]


        construction_matches = [
            term
            for term in construction_terms
            if term in content
        ]


        if (
            "horizon drive"
            in content
            and
            len(construction_matches) >= 2
        ):

            selected_result = result

            break


    assert selected_result is not None, (
        "Could not locate Horizon Drive construction evidence"
    )


    evidence = (
        selected_result.evidence
    )


    #
    # Verify strong project match.
    #
    assert (
        selected_result
        .score
        .match_score
        >= 0.5
    )


    content = (
        evidence.content
        .lower()
    )


    assert (
        "horizon"
        in content
    )


    assert any(
        term in content
        for term in [
            "construction",
            "improvement",
            "roundabout",
            "transportation",
            "infrastructure",
        ]
    )


    #
    # Verify metadata extraction.
    #
    metadata = (
        evidence.metadata
    )


    assert (
        "project_phase"
        in metadata
    )


    assert (
        metadata["project_phase"]
        ==
        "construction"
    )


    print()

    print(
        "Selected evidence:"
    )

    print(
        evidence.title
    )

    print(
        evidence.url
    )

    print()

    print(
        "Evidence pipeline test: PASS"
    )


if __name__ == "__main__":

    test_pipeline()