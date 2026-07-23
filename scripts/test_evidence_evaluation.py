"""
Test EvidenceEvaluationService behavior.

Tests the combined pipeline:

Project + Evidence
        |
        v
EvidenceMatcherService
        |
        v
EvidenceScoringService
        |
        v
EvidenceScore
"""

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)
from construction_intelligence.core.enums import (
    ConfidenceLevel,
)
from construction_intelligence.core.project import Project
from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)


def create_project() -> Project:
    """Create a sample construction project."""

    return Project(
        name="Horizon Glen Drive",
        origin_id="osm-project-123",
        city="Grand Junction",
        road_name="Horizon Glen Drive",
        latitude=39.0639,
        longitude=-108.5506,
    )


def test_strong_match(
    evaluator: EvidenceEvaluationService,
    project: Project,
) -> None:
    """A specific government record should score highly."""

    evidence = Evidence(
        project_id=project.id,
        source=EvidenceSource.GOVERNMENT_RECORD,
        origin_id="government-record-123",
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

    score = evaluator.evaluate(
        project,
        evidence,
    )

    print("\nTest 1 - Strong match")
    print("--------------------")
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

    assert score.match_score > 0.80
    assert score.quality_score > 0.80
    assert score.overall_score > 0.80


def test_unrelated_project(
    evaluator: EvidenceEvaluationService,
    project: Project,
) -> None:
    """Same city but unrelated project should score poorly."""

    evidence = Evidence(
        project_id=project.id,
        source=EvidenceSource.GOVERNMENT_RECORD,
        origin_id="government-record-456",
        title=(
            "Canyon Rim Drive improvements approved"
        ),
        content=(
            "The City of Grand Junction approved "
            "transportation improvements on "
            "Canyon Rim Drive."
        ),
        confidence=ConfidenceLevel.HIGH,
        metadata={
            "document_type": "city_notice",
        },
    )

    score = evaluator.evaluate(
        project,
        evidence,
    )

    print("\nTest 2 - Unrelated project")
    print("--------------------------")
    print(
        f"Match score: "
        f"{score.match_score:.2f}"
    )
    print(
        f"Overall score: "
        f"{score.overall_score:.2f}"
    )

    assert score.match_score < 0.50
    assert score.overall_score < 0.50


def main() -> None:
    """Run evaluation tests."""

    evaluator = EvidenceEvaluationService()

    project = create_project()

    test_strong_match(
        evaluator,
        project,
    )

    test_unrelated_project(
        evaluator,
        project,
    )

    print(
        "\nEvidence evaluation test: PASS"
    )


if __name__ == "__main__":
    main()