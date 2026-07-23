"""
Gemini-powered web document extractor.

Fallback extractor for pages that cannot be
processed by normal HTML extraction.
"""

from __future__ import annotations

import json

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class GeminiExtractor(
    WebExtractor,
):
    """
    Uses Gemini to extract evidence from a URL.
    """

    def __init__(
        self,
        runner,
    ) -> None:

        self.runner = runner

    def extract(
        self,
        url: str,
    ) -> RawWebDocument:
        """
        Extract document information using Gemini.
        """

        prompt = f"""
Extract construction project information from this source:

{url}

Return JSON with:

{{
    "title": "",
    "source": "",
    "content": ""
}}

Only include information related to the construction project.
"""

        response = self.runner.run(
            prompt
        )

        return self._parse_response(
            url,
            response,
        )

    def _parse_response(
        self,
        url: str,
        response: str,
    ) -> RawWebDocument:
        """
        Convert Gemini response into RawWebDocument.
        """

        try:

            data = json.loads(
                response
            )

            title = data.get(
                "title",
                "Gemini extracted evidence",
            )

            source = data.get(
                "source",
                "Gemini",
            )

            content = data.get(
                "content",
                response,
            )

        except json.JSONDecodeError:

            title = (
                "Gemini extracted evidence"
            )

            source = "Gemini"

            content = response

        return RawWebDocument(
            url=url,
            title=title,
            content=content,
            source_name=source,
        )