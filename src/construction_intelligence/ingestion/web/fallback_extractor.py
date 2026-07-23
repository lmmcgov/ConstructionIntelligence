"""
Fallback web extractor.

Routes documents to the appropriate extractor:

PDF:
    PDFExtractor

HTML:
    Primary HTML extractor

Fallback:
    Gemini extractor
"""

from __future__ import annotations

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class FallbackExtractor(
    WebExtractor,
):
    """
    Uses specialized extractors with fallback support.

    Extraction order:

    1. PDF extractor for PDF-like URLs
    2. Primary HTML extractor
    3. Gemini fallback
    """

    def __init__(
        self,
        primary: WebExtractor,
        fallback: WebExtractor,
        pdf_extractor: WebExtractor | None = None,
    ) -> None:

        self.primary = primary

        self.fallback = fallback

        self.pdf_extractor = pdf_extractor


    def extract(
        self,
        url: str,
    ) -> RawWebDocument:
        """
        Extract document using the appropriate strategy.
        """

        #
        # PDF routing
        #
        if (
            self.pdf_extractor is not None
            and self._is_pdf_url(url)
        ):

            try:

                document = (
                    self.pdf_extractor.extract(
                        url
                    )
                )

                if document.content:

                    return document


            except Exception as error:

                print(
                    "PDF extraction failed:"
                )

                print(url)

                print(
                    f"Reason: {error}"
                )


        #
        # HTML extraction
        #
        try:

            document = (
                self.primary.extract(
                    url
                )
            )

            if document.content:

                return document


        except Exception as error:

            print(
                f"Primary extraction failed: {url}"
            )

            print(
                f"Reason: {error}"
            )


        #
        # Gemini fallback
        #
        print(
            f"Using Gemini fallback: {url}"
        )

        return (
            self.fallback.extract(
                url
            )
        )


    def _is_pdf_url(
        self,
        url: str,
    ) -> bool:
        """
        Detect PDF URLs.

        Many government systems do not expose
        .pdf extensions. Examples:

        /DocumentCenter/View/12345
        /download?id=12345
        """

        indicators = [
            ".pdf",
            "/pdf",
            "documentcenter/view",
            "download",
        ]


        normalized = (
            url.lower()
        )


        return any(
            indicator in normalized
            for indicator in indicators
        )