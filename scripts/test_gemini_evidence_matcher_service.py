"""
Test Gemini evidence matcher service.

Uses a mocked Gemini runner so the test validates:
- prompt flow
- Gemini response parsing
- EvidenceMatchResult creation

without requiring a live Gemini call.
"""

from uuid import uuid4

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.integrations.gemini_cli.runner import (
    GeminiCLIRunner,
)

from construction_intelligence.services.gemini_evidence_matcher_service import (
    GeminiEvidenceMatcherService,
)


class MockGeminiRunner:
    """
    Fake Gemini CLI response for testing.
    """

    def run(
        self,
        prompt: str,
    ) -> str:
        """
        Return simulated Gemini JSON output.
        """

        return """
        ✦ {
          "match_score": 0.95,
          "status": "confirmed",
          "reasons": [
            "Road name matches",
            "Project location matches"
          ],
          "resources": [
            {
              "url": "https://grandjunction.gov/projects/horizon",
              "title": "Horizon Glen Drive Improvements",
              "source": "City of Grand Junction",
              "resource_type": "government_page",
              "excerpt": "Construction begins in summer 2026"
            }
          ]
        }
        """


def main() -> None:
    """
    Test Gemini evidence matching workflow.
    """

    project = Project(
        id=uuid4(),
        name="Horizon Glen Drive Improvements",
        city="Grand Junction",
        road_name="Horizon Glen Drive",
    )

    evidence = Evidence(
        id=uuid4(),
        project_id=project.id,
        source=EvidenceSource.GOVERNMENT_RECORD,
        title=(
            "Horizon Glen Drive Improvements "
            "Begin Construction"
        ),
        content=(
            "The City of Grand Junction announced "
            "construction on Horizon Glen Drive."
        ),
        url=(
            "https://grandjunction.gov/projects/horizon"
        ),
        confidence="high",
    )

    matcher = GeminiEvidenceMatcherService(
        runner=MockGeminiRunner()
    )

    result = matcher.match(
        project,
        evidence,
    )

    print(
        "Gemini evidence matcher service test"
    )
    print(
        "------------------------------------"
    )

    print(
        f"Match score: {result.match_score}"
    )

    print(
        "Reasons:"
    )

    for reason in result.reasons:
        print(
            f"- {reason}"
        )

    assert (
        result.match_score == 0.95
    )

    assert (
        len(result.reasons) == 2
    )

    print(
        "\nGemini evidence matcher service test: PASS"
    )


if __name__ == "__main__":
    main()