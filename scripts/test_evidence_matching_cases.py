"""
Test evidence matching scenarios.

Covers:
1. Exact project match.
2. Same city but unrelated project.
3. High-quality source with weak project match.

Uses EvidenceEvaluationService because matching requires:
- project
- evidence
- matcher
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
    """
    Create a sample project.
    """

    return Project(
        name="Horizon Glen Drive",
        origin_id="osm-project-123",
        city="Grand Junction",
        road_name="Horizon Glen Drive",
        latitude=39.0639,
        longitude=-108.5506,
    )


def test_exact_match(
    evaluator: EvidenceEvaluationService,
    project: Project,
) -> None:
    """
    Exact project evidence should score highly.
    """

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

    score = evaluator.evaluate(
        project,
        evidence,
    )

    print("\nTest 1 - Exact match")
    print("-------------------")

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
    assert score.overall_score > 0.80


def test_same_city_unrelated_project(
    evaluator: EvidenceEvaluationService,
    project: Project,
) -> None:
    """
    Same city but unrelated project should score low.
    """

    evidence = Evidence(
        project_id=project.id,
        source=EvidenceSource.NEWS_ARTICLE,
        origin_id="news-record-123",
        title=(
            "Grand Junction approves "
            "Canyon Rim Drive improvements"
        ),
        content=(
            "The City of Grand Junction approved "
            "transportation improvements on "
            "Canyon Rim Drive."
        ),
        confidence=ConfidenceLevel.MEDIUM,
        metadata={
            "document_type": "news",
        },
    )

    score = evaluator.evaluate(
        project,
        evidence,
    )

    print("\nTest 2 - Same city, unrelated project")
    print("------------------------------------")

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


def test_high_quality_weak_match(
    evaluator: EvidenceEvaluationService,
    project: Project,
) -> None:
    """
    A reliable source should not overcome a weak project match.
    """

    evidence = Evidence(
        project_id=project.id,
        source=EvidenceSource.GOVERNMENT_RECORD,
        origin_id="government-record-456",
        title="Grand Junction transportation projects",
        content=(
            "The City of Grand Junction "
            "has several transportation projects planned."
        ),
        confidence=ConfidenceLevel.HIGH,
        metadata={
            "document_type": "government_summary",
        },
    )

    score = evaluator.evaluate(
        project,
        evidence,
    )

    print("\nTest 3 - High quality, weak match")
    print("---------------------------------")

    print(
        f"Quality score: "
        f"{score.quality_score:.2f}"
    )

    print(
        f"Match score: "
        f"{score.match_score:.2f}"
    )

    print(
        f"Overall score: "
        f"{score.overall_score:.2f}"
    )

    assert score.quality_score > 0.80
    assert score.match_score < 0.50
    assert score.overall_score < 0.50


def main() -> None:
    """
    Run evidence matching tests.
    """

    evaluator = EvidenceEvaluationService()

    project = create_project()

    test_exact_match(
        evaluator,
        project,
    )

    test_same_city_unrelated_project(
        evaluator,
        project,
    )

    test_high_quality_weak_match(
        evaluator,
        project,
    )

    print(
        "\nEvidence matching cases: PASS"
    )


if __name__ == "__main__":

    main()