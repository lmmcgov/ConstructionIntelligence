"""
Test Gemini-powered evidence evaluation workflow.

Pipeline:

Project
    |
Evidence
    |
GeminiEvidenceMatcherService
    |
EvidenceEvaluationService
    |
EvidenceEvaluation
"""

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.project import (
    Project,
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


def main() -> None:
    """
    Test Gemini evidence evaluation integration.
    """

    #
    # Create test project.
    #
    project = Project(
        name="Horizon Glen Drive Improvements",
        description=(
            "Road reconstruction project "
            "in Grand Junction."
        ),
        status="active",
        category="road_construction",
        origin="osm",
        origin_id="way/123456",
        road_name="Horizon Glen Drive",
        road_ref=None,
        country="United States",
        state="Colorado",
        city="Grand Junction",
        latitude=39.0639,
        longitude=-108.5506,
    )

    #
    # Create supporting evidence.
    #
    evidence = Evidence(
        project_id=project.id,
        source="government_record",
        origin_id=None,
        title=(
            "Horizon Glen Drive Improvements"
        ),
        url=(
            "https://grandjunction.gov/projects/horizon"
        ),
        content=(
            "The City of Grand Junction announced "
            "Horizon Glen Drive Improvements. "
            "Construction begins in summer 2026."
        ),
        confidence="high",
        metadata={
            "source_type": "government_page"
        },
    )

    #
    # Gemini CLI response simulation.
    #
    # This avoids making a real Gemini call during testing.
    #
    runner = MockGeminiRunner()

    matcher = GeminiEvidenceMatcherService(
        runner=runner,
    )

    #
    # Inject Gemini matcher.
    #
    evaluator = EvidenceEvaluationService(
        matcher=matcher,
    )

    result = evaluator.evaluate(
        project,
        evidence,
    )

    print(
        "Gemini evidence evaluation test"
    )
    print(
        "--------------------------------"
    )

    print(
        f"Match score: {result.match_score}"
    )

    print(
        f"Quality score: {result.quality_score}"
    )

    print(
        f"Overall score: "
        f"{result.match_score * result.quality_score:.2f}"
    )

    print(
        "\nReasons:"
    )

    for reason in result.reasons:
        print(
            f"- {reason}"
        )

    print(
        "\nResources:"
    )

    for resource in result.resources:
        print(
            f"- {resource.source_name}"
        )

        print(
            f"  Title: {resource.title}"
        )

        print(
            f"  URL: {resource.url}"
        )

        print(
            f"  Type: {resource.resource_type}"
        )

        print(
            f"  Excerpt: {resource.excerpt}"
        )

    #
    # Assertions.
    #
    assert result.match_score == 0.95

    assert result.quality_score >= 0.90

    assert (
        result.match_score
        *
        result.quality_score
        >= 0.85
    )

    assert len(result.resources) == 1

    assert (
        result.resources[0].source_name
        ==
        "City of Grand Junction"
    )

    assert (
        result.resources[0].title
        ==
        "Horizon Glen Drive Improvements"
    )

    print(
        "\nGemini evidence evaluation test: PASS"
    )


if __name__ == "__main__":
    main()