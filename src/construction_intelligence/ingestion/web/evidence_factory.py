"""
Creates Evidence objects from external web sources.
"""

from __future__ import annotations

from urllib.parse import urlparse

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)

from construction_intelligence.core.enums import (
    ConfidenceLevel,
)

from construction_intelligence.core.ids import (
    ProjectId,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)

from construction_intelligence.services.evidence_metadata_extraction_service import (
    EvidenceMetadataExtractionService,
)


class WebEvidenceFactory:
    """
    Creates Evidence objects from external web sources.

    Attempts to classify evidence sources based on:

    - domain
    - URL structure
    - document metadata
    - government indicators
    - construction document signals
    """


    def __init__(
        self,
        metadata_extractor: EvidenceMetadataExtractionService | None = None,
    ) -> None:

        self.metadata_extractor = (
            metadata_extractor
            if metadata_extractor is not None
            else EvidenceMetadataExtractionService()
        )


    def create(
        self,
        project_id: ProjectId,
        document: RawWebDocument,
        source: EvidenceSource | None = None,
    ) -> Evidence:
        """
        Convert a web document into Evidence.
        """

        evidence_source = (
            source
            if source is not None
            else self._classify_source(
                document
            )
        )


        #
        # Create base evidence record.
        #
        evidence = Evidence(
            project_id=project_id,
            source=evidence_source,
            origin_id=document.url,
            title=document.title,
            url=document.url,
            content=document.content,
            confidence=ConfidenceLevel.MEDIUM,
            metadata={
                "source_name": document.source_name,
                "classified_source": (
                    evidence_source.value
                ),
            },
        )


        #
        # Extract structured project metadata.
        #
        extracted_metadata = (
            self.metadata_extractor.extract(
                evidence
            )
        )


        #
        # Merge extracted metadata into
        # evidence metadata.
        #
        evidence.metadata.update(
            extracted_metadata
        )


        return evidence


    def _classify_source(
        self,
        document: RawWebDocument,
    ) -> EvidenceSource:
        """
        Determine evidence source type.
        """

        parsed = urlparse(
            document.url
        )

        domain = (
            parsed.netloc
            .lower()
        )

        path = (
            parsed.path
            .lower()
        )


        text = (
            domain
            + " "
            + path
            + " "
            + document.title.lower()
        )


        #
        # Government indicators.
        #
        government_domains = [
            ".gov",
            ".gov.",
            ".gouv.",
            ".gc.ca",
        ]


        municipal_domains = [
            "city",
            "town",
            "municipal",
            "county",
            "civic",
            "gjcity",
        ]


        is_government = any(
            indicator in domain
            for indicator in government_domains
        )


        is_municipal = any(
            indicator in domain
            for indicator in municipal_domains
        )


        #
        # Government document repositories.
        #
        is_document_repository = any(
            indicator in path
            for indicator in [
                "documentcenter",
                "view",
                "download",
                "attachment",
            ]
        )


        #
        # Construction project indicators.
        #
        construction_terms = [
            "construction",
            "project",
            "improvement",
            "improvements",
            "transportation",
            "road",
            "capital",
            "infrastructure",
            "engineering",
        ]


        has_construction_context = any(
            term in text
            for term in construction_terms
        )


        #
        # Government construction records.
        #
        if (
            (
                is_government
                or is_municipal
            )
            and (
                is_document_repository
                or has_construction_context
            )
        ):

            return EvidenceSource.CITY_PROJECT_PAGE


        #
        # General government websites.
        #
        if (
            is_government
            or is_municipal
        ):

            return EvidenceSource.GOVERNMENT_WEBSITE


        #
        # Procurement signals.
        #
        if any(
            term in path
            for term in [
                "bid",
                "contract",
                "procurement",
                "tender",
                "rfp",
                "award",
            ]
        ):

            return EvidenceSource.PROCUREMENT


        #
        # News signals.
        #
        if any(
            term in domain
            for term in [
                "news",
                "times",
                "journal",
                "gazette",
                "sentinel",
            ]
        ):

            return EvidenceSource.NEWS_ARTICLE


        #
        # Generic web source.
        #
        return EvidenceSource.OTHER_WEB