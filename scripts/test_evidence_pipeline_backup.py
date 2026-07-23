"""
Integration test for EvidencePipelineService.

Validates:

- URL discovery
- Evidence ingestion
- Evidence creation
- Evidence evaluation
- Evidence ranking
"""

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)

from construction_intelligence.ingestion.web.web_evidence_ingestion_service import (
    WebEvidenceIngestionService,
)

from construction_intelligence.ingestion.web.evidence_discovery_service import (
    EvidenceDiscoveryService,
)

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)

from construction_intelligence.services.evidence_pipeline_service import (
    EvidencePipelineService,
)


class FakeDiscoveryService:
    """
    Provides deterministic test URLs.
    """

    def discover_urls(
        self,
        project: Project,
    ) -> list[str]:

        return [
            "https://www.grandjunction.gov/projects/horizon-glen-drive-improvements.pdf",
            "https://example.com/random-page",
        ]


class FakeExtractor(WebExtractor):
    """
    Returns fake documents without network access.
    """

    def extract(
        self,
        url: str,
    ) -> RawWebDocument:

        if "horizon-glen" in url:

            return RawWebDocument(
                url=url,
                title=(
                    "Horizon Glen Drive Improvements "
                    "Construction Project"
                ),
                content=(
                    "The City of Grand Junction approved "
                    "construction improvements for "
                    "Horizon Glen Drive."
                ),
                source_name="City Government",
            )


        return RawWebDocument(
            url=url,
            title="Random webpage",
            content=(
                "This page is unrelated to transportation."
            ),
            source_name="Example",
        )


def create_project() -> Project:
    """
    Create test project.
    """

    return Project(
        name="Horizon Glen Drive Improvements",
        city="Grand Junction",
        state="Colorado",
        country="United States",
        road_name="Horizon Glen Drive",
    )


def test_pipeline() -> None:
    """
    Validate complete evidence pipeline.
    """

    project = create_project()


    ingestion_service = (
        WebEvidenceIngestionService(
            discovery_service=FakeDiscoveryService(),
            extractor=FakeExtractor(),
        )
    )


    evaluation_service = (
        EvidenceEvaluationService()
    )


    pipeline = (
        EvidencePipelineService(
            ingestion_service=ingestion_service,
            evaluation_service=evaluation_service,
        )
    )


    results = (
        pipeline.run(
            project
        )
    )


    print()

    print(
        "Evidence pipeline results"
    )

    print(
        "-------------------------"
    )


    for result in results:

        print(
            result.evidence.title
        )

        print(
            f"Score: "
            f"{result.score.overall_score:.2f}"
        )

        print()


    assert len(results) == 2

    assert (
        results[0]
        .score
        .match_score
        >
        results[1]
        .score
        .match_score
    )


    assert (
        "Horizon Glen"
        in results[0]
        .evidence
        .title
    )


    print(
        "Evidence pipeline test: PASS"
    )


if __name__ == "__main__":

    test_pipeline()