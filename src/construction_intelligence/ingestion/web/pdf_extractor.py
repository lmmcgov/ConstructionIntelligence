"""
PDF document extractor.

Downloads PDF files and converts them
into RawWebDocument objects.
"""

from __future__ import annotations

import io
import re

import requests
from pypdf import PdfReader

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class PDFExtractor(
    WebExtractor,
):
    """
    Extracts text content from PDF documents.
    """

    def __init__(
        self,
        timeout: int = 30,
    ) -> None:

        self.timeout = timeout


    def extract(
        self,
        url: str,
    ) -> RawWebDocument:
        """
        Download and extract PDF content.
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


        pdf_file = io.BytesIO(
            response.content
        )


        reader = PdfReader(
            pdf_file
        )


        pages: list[str] = []


        for page in reader.pages:

            text = (
                page.extract_text()
                or ""
            )

            pages.append(
                text
            )


        content = "\n".join(
            pages
        )


        content = re.sub(
            r"\s+",
            " ",
            content,
        ).strip()


        #
        # Prevent enormous documents
        # overwhelming downstream evaluation.
        #
        content = content[:20000]


        title = (
            url.split("/")[-1]
            .replace("-", " ")
            .replace("_", " ")
        )


        return RawWebDocument(
            url=url,
            title=title,
            content=content,
            source_name=self._extract_domain(
                url
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