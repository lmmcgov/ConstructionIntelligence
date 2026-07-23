"""
Temporary extractor for discovered web URLs.

Used until real HTML extraction is implemented.
"""

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class SearchResultExtractor(
    WebExtractor,
):
    """
    Creates placeholder documents from search results.

    This allows real search URLs to flow through
    the evidence pipeline.
    """

    def extract(
        self,
        url: str,
    ) -> RawWebDocument:

        return RawWebDocument(
            url=url,
            title=url,
            content=(
                f"Web evidence discovered from {url}"
            ),
            source_name="SearXNG",
        )