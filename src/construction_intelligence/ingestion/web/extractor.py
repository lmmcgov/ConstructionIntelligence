"""
Web document extraction interface.
"""

from abc import ABC, abstractmethod

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


class WebExtractor(ABC):
    """
    Extracts text content from external sources.
    """

    @abstractmethod
    def extract(
        self,
        url: str,
    ) -> RawWebDocument:
        """
        Extract a document from a URL.
        """
        raise NotImplementedError