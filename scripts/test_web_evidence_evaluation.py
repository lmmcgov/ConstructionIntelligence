"""
Test external web evidence evaluation.
"""

from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.project import Project
from construction_intelligence.ingestion.web.evidence_factory import (
    WebEvidenceFactory,
)
from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)
from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)


def main() -> None:

    project = Project(
        name="Horizon Glen Drive",
        city="Grand Junction",
        road_name="Horizon Glen Drive",
    )

    document = RawWebDocument(
        url="https://grandjunction.gov/projects/horizon-glen-drive",
        title="Horizon Glen Drive Improvements Begin",
        content=(
            "The City of Grand Junction announces "
            "Horizon Glen Drive improvements."
        ),
        source_name="City of Grand Junction",
    )

    evidence = WebEvidenceFactory().create(
        project.id,
        document,
        EvidenceSource.CITY_PROJECT_PAGE,
    )

    result = EvidenceEvaluationService().evaluate(
        project,
        evidence,
    )

    print(
        "Web evidence evaluation test"
    )
    print(
        "----------------------------"
    )

    print(
        f"Match score: {result.match_score:.2f}"
    )

    print(
        f"Quality score: {result.quality_score:.2f}"
    )

    print(
        f"Overall score: {result.overall_score:.2f}"
    )

    print("\nReasons:")

    for reason in result.reasons:
        print(
            f"- {reason}"
        )

    assert result.match_score > 0.80
    assert result.quality_score > 0.80
    assert result.overall_score > 0.70

    print(
        "\nWeb evidence evaluation test: PASS"
    )


if __name__ == "__main__":
    main()