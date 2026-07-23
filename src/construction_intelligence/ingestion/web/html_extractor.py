"""
HTML-based web document extractor.

Fetches web pages and converts them into RawWebDocument objects.
"""

from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class HTMLExtractor(
    WebExtractor,
):
    """
    Extracts readable text from HTML pages.
    """

    def __init__(
        self,
        timeout: int = 15,
    ) -> None:

        self.timeout = timeout

    def extract(
        self,
        url: str,
    ) -> RawWebDocument:
        """
        Fetch a URL and extract page content.
        """

        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(ConstructionIntelligence)"
                )
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        #
        # Remove non-content elements.
        #
        for element in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
            ]
        ):
            element.decompose()

        #
        # Extract title.
        #
        title = ""

        if soup.title:
            title = soup.title.get_text(
                " ",
                strip=True,
            )

        #
        # Extract visible text.
        #
        text = soup.get_text(
            " ",
            strip=True,
        )

        #
        # Normalize whitespace.
        #
        content = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        #
        # Limit extremely large pages.
        #
        content = content[:10000]

        return RawWebDocument(
            url=url,
            title=title or url,
            content=content,
            source_name=(
                self._extract_domain(
                    url
                )
            ),
        )

    def _extract_domain(
        self,
        url: str,
    ) -> str:
        """
        Extract hostname from URL.
        """

        return (
            url.split("//")[-1]
            .split("/")[0]
        )