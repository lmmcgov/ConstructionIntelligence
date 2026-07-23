"""
Test Gemini CLI response parsing.
"""

from construction_intelligence.integrations.gemini_cli.parser import (
    GeminiResponseParser,
)


def main() -> None:
    """
    Test parsing Gemini CLI formatted output.
    """

    #
    # Simulate actual Gemini CLI output.
    #
    # Gemini may wrap JSON with:
    #
    # ✦ {
    #   ...
    # }
    #
    # or markdown fences.
    #
    response = """
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

    parser = GeminiResponseParser()

    result = parser.parse(
        response
    )

    print(
        "Gemini response parser test"
    )
    print(
        "---------------------------"
    )

    print(
        f"Match score: {result.match_score}"
    )

    print(
        f"Status: {result.status}"
    )

    print(
        f"Reasons: {len(result.reasons)}"
    )

    print(
        f"Resources: {len(result.resources)}"
    )

    print(
        "\nResource details:"
    )

    for resource in result.resources:
        print(
            f"- {resource.title}"
        )
        print(
            f"  Source: {resource.source}"
        )
        print(
            f"  URL: {resource.url}"
        )

    assert result.match_score == 0.95

    assert (
        result.status
        ==
        "confirmed"
    )

    assert len(result.reasons) == 2

    assert len(result.resources) == 1

    assert (
        result.resources[0].source
        ==
        "City of Grand Junction"
    )

    assert (
        result.resources[0].resource_type
        ==
        "government_page"
    )

    print(
        "\nGemini response parser test: PASS"
    )


if __name__ == "__main__":
    main()