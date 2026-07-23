"""
Test EvidenceScoringService behavior.
"""

from uuid import uuid4

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.enums import (
    ConfidenceLevel,
)
from construction_intelligence.core.project import Project
from construction_intelligence.services.evidence_scoring_service import (
    EvidenceScoringService,
)


def main() -> None:
    """Run evidence scoring tests."""

    scorer = EvidenceScoringService()

    project = Project(
        name="Horizon Glen Drive",
        origin_id="osm-project-123",
        city="Grand Junction",
        road_name="Horizon Glen Drive",
        latitude=39.0639,
        longitude=-108.5506,
    )

    evidence = Evidence(
        project_id=project.id,
        source=EvidenceSource.GOVERNMENT_RECORD,
        origin_id="web-record-123",
        title=(
            "Horizon Glen Drive construction project "
            "approved by Grand Junction"
        ),
        content=(
            "The City of Grand Junction approved "
            "construction of Horizon Glen Drive."
        ),
        confidence=ConfidenceLevel.HIGH,
        metadata={
            "document_type": "city_notice",
        },
    )

    score = scorer.score(
        project,
        evidence,
    )

    print("Evidence scoring test")
    print("---------------------")

    print(
        f"Match score: "
        f"{score.match_score:.2f}"
    )

    print(
        f"Quality score: "
        f"{score.quality_score:.2f}"
    )

    print(
        f"Overall score: "
        f"{score.overall_score:.2f}"
    )

    print("\nReasons:")

    for reason in score.reasons:
        print(
            f"- {reason}"
        )

    assert score.match_score > 0.0

    assert score.quality_score > 0.0

    assert score.overall_score > 0.0

    assert (
        "Project name appears in evidence title"
        in score.reasons
    )

    print(
        "\nEvidence scoring test: PASS"
    )


if __name__ == "__main__":
    main()