"""
Test Gemini CLI runner.
"""

from construction_intelligence.integrations.gemini_cli.runner import (
    GeminiCLIRunner,
)


def main() -> None:
    """
    Verify that Python can execute Gemini CLI
    and receive a response.
    """

    runner = GeminiCLIRunner()

    prompt = """
Return only valid JSON.

{
  "match_score": 0.95,
  "status": "confirmed",
  "reasons": [
    "Gemini CLI execution successful"
  ],
  "resources": []
}
"""

    response = runner.run(
        prompt
    )

    print(
        "Gemini CLI runner test"
    )
    print(
        "---------------------"
    )

    print(
        "Response received:"
    )

    print(
        response
    )

    assert response

    assert (
        "match_score"
        in response
    )

    print(
        "\nGemini CLI runner test: PASS"
    )


if __name__ == "__main__":
    main()