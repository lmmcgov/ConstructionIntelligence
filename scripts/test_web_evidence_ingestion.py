"""
Test web evidence ingestion workflow.

Pipeline:

Project
    |
    v
EvidenceDiscoveryService
    |
    v
MockSearchProvider
    |
    v
MockWebExtractor
    |
    v
WebEvidenceFactory
    |
    v
Evidence
"""

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.core.evidence_source import (
    EvidenceSource,
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


def main() -> None:
    """
    Test web evidence discovery and ingestion.
    """

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

    url = (
        "https://grandjunction.gov/projects/horizon"
    )

    #
    # Mock search results.
    #
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

    discovery_service = EvidenceDiscoveryService(
        search_provider
    )

    #
    # Mock extracted web page.
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

    evidence_records = (
        ingestion_service.ingest(
            project
        )
    )

    print(
        "Web evidence ingestion test"
    )
    print(
        "---------------------------"
    )

    print(
        f"Evidence records created: "
        f"{len(evidence_records)}"
    )

    assert len(evidence_records) == 1

    evidence = evidence_records[0]

    print()
    print(
        f"Title: {evidence.title}"
    )

    print(
        f"URL: {evidence.url}"
    )

    print(
        f"Source: {evidence.source}"
    )

    print(
        f"Content: {evidence.content}"
    )

    assert (
        evidence.source
        ==
        EvidenceSource.OTHER_WEB
    )

    assert (
        evidence.title
        ==
        "Horizon Glen Drive Improvements"
    )

    assert (
        evidence.url
        ==
        url
    )

    assert (
        evidence.content
        is not None
    )

    print(
        "\nWeb evidence ingestion test: PASS"
    )


if __name__ == "__main__":
    main()