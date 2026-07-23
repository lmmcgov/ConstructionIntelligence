"""
Mock web extractor for testing.
"""

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)
from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class MockWebExtractor(
    WebExtractor,
):
    """
    Returns predefined documents.
    """

    def __init__(
        self,
        documents: dict[str, RawWebDocument],
    ) -> None:
        self.documents = documents

    def extract(
        self,
        url: str,
    ) -> RawWebDocument:

        return self.documents[url]