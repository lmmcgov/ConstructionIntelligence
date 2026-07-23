"""
Mock Gemini CLI runner for testing.

Returns deterministic Gemini-style JSON responses.
"""

from __future__ import annotations


class MockGeminiRunner:
    """
    Fake Gemini runner used for tests.

    Simulates a Gemini response without
    making external CLI calls.
    """

    def run(
        self,
        prompt: str,
    ) -> str:
        """
        Return simulated Gemini JSON response.
        """

        return """
        {
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