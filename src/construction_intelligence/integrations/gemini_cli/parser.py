"""
Parser for Gemini CLI structured JSON output.
"""

from __future__ import annotations

import json
import re

from construction_intelligence.integrations.gemini_cli.schemas import (
    GeminiEvaluationResponse,
    GeminiResourceResponse,
)


class GeminiResponseParser:
    """
    Converts Gemini CLI JSON responses into
    validated structured objects.

    Handles:
    - raw JSON
    - markdown JSON blocks
    - Gemini CLI formatting
    """

    def parse(
        self,
        response_text: str,
    ) -> GeminiEvaluationResponse:
        """
        Parse Gemini CLI output.
        """

        json_text = self._extract_json(
            response_text
        )

        data = json.loads(
            json_text
        )

        resources = tuple(
            GeminiResourceResponse(
                url=item["url"],
                title=item.get(
                    "title"
                ),
                source=item.get(
                    "source"
                ),
                resource_type=item.get(
                    "resource_type"
                ),
                excerpt=item.get(
                    "excerpt"
                ),
            )
            for item in data.get(
                "resources",
                [],
            )
        )

        return GeminiEvaluationResponse(
            match_score=float(
                data["match_score"]
            ),
            status=data["status"],
            reasons=tuple(
                data.get(
                    "reasons",
                    [],
                )
            ),
            resources=resources,
        )

    @staticmethod
    def _extract_json(
        text: str,
    ) -> str:
        """
        Extract JSON object from Gemini CLI output.
        """

        #
        # Handle markdown fenced JSON:
        #
        # ```json
        # {...}
        # ```
        #
        fenced_match = re.search(
            r"```json\s*(.*?)\s*```",
            text,
            re.DOTALL,
        )

        if fenced_match:
            return fenced_match.group(1)

        #
        # Handle plain JSON embedded
        # inside CLI output.
        #
        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "No JSON object found in Gemini response"
            )

        return text[
            start : end + 1
        ]