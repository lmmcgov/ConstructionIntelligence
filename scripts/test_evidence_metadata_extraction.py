from construction_intelligence.services.evidence_metadata_extraction_service import (
    EvidenceMetadataExtractionService,
)

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.enums import (
    ConfidenceLevel,
)

from construction_intelligence.core.ids import (
    new_id,
)


def test_metadata_extraction():
    """
    Validate extraction of structured project metadata.
    """

    evidence = Evidence(
        project_id=new_id(),
        source="government_website",
        origin_id="test",
        title="Horizon Drive Construction",
        url="https://example.com",
        content="""
        The City of Grand Junction will start construction
        on April 7, 2025.

        Sunroc Corporation was awarded the contract
        that is scheduled for completion in October 2025.

        The Horizon Drive and G Road Roundabout Project
        will improve transportation infrastructure.
        """,
        confidence=ConfidenceLevel.MEDIUM,
        metadata={},
    )


    service = (
        EvidenceMetadataExtractionService()
    )


    metadata = (
        service.extract(
            evidence
        )
    )


    print()

    print(
        "Extracted Metadata"
    )

    print(
        "------------------"
    )


    for key, value in metadata.items():

        print(
            f"{key}: {value}"
        )


    assert (
        metadata["contractor"]
        ==
        "Sunroc Corporation"
    )

    assert (
        metadata["construction_start_date"]
        ==
        "April 7, 2025"
    )

    assert (
        metadata["expected_completion"]
        ==
        "October 2025"
    )

    assert (
        metadata["location"]
        ==
        "Horizon Drive and G Road"
    )

    assert (
        metadata["project_phase"]
        ==
        "construction"
    )


    print()

    print(
        "Evidence metadata extraction test: PASS"
    )


if __name__ == "__main__":

    test_metadata_extraction()