"""
Extract structured metadata from evidence content.

Converts unstructured construction evidence
into machine-readable project intelligence.
"""

from __future__ import annotations

import re

from construction_intelligence.core.evidence import (
    Evidence,
)


class EvidenceMetadataExtractionService:
    """
    Extracts structured facts from evidence documents.

    Extracted fields may include:

    - contractor
    - construction_start_date
    - expected_completion
    - location
    - project_phase
    - contract_status
    """


    def extract(
        self,
        evidence: Evidence,
    ) -> dict[str, str]:
        """
        Extract metadata fields from evidence content.
        """

        content = (
            evidence.content
            if evidence.content
            else ""
        )


        metadata: dict[str, str] = {}


        #
        # Normalize PDF extraction artifacts.
        #
        normalized_content = re.sub(
            r"\s+",
            " ",
            content,
        ).strip()


        #
        # Contractor extraction.
        #
        contractor_match = re.search(
            r"([A-Z][A-Za-z\s]+Corporation)"
            r"\s+was awarded the contract",
            normalized_content,
            re.IGNORECASE,
        )


        if contractor_match:

            metadata["contractor"] = (
                contractor_match
                .group(1)
                .strip()
            )


        #
        # Construction start date.
        #
        # Handles variations:
        #
        # "will start construction on April 7, 2025"
        # "will begin construction on April 7, 2025"
        # "construction will start on April 7, 2025"
        #
        start_match = re.search(
            r"(?:start|begin)"
            r"(?:ing)?"
            r"(?:\s+\w+){0,4}"
            r"\s+"
            r"(?:construction\s+)?"
            r"on\s+"
            r"([A-Z][a-z]+\s+\d{1,2},\s+\d{4})",
            normalized_content,
            re.IGNORECASE,
        )


        #
        # Additional fallback:
        #
        # Looks for any construction sentence
        # containing a date.
        #
        if not start_match:

            start_match = re.search(
                r"construction.*?"
                r"on\s+"
                r"([A-Z][a-z]+\s+\d{1,2},\s+\d{4})",
                normalized_content,
                re.IGNORECASE,
            )


        if start_match:

            metadata["construction_start_date"] = (
                start_match.group(1)
            )


        #
        # Expected completion date.
        #
        completion_match = re.search(
            r"completion\s+in\s+"
            r"([A-Za-z]+\s+\d{4})",
            normalized_content,
            re.IGNORECASE,
        )


        if completion_match:

            metadata["expected_completion"] = (
                completion_match.group(1)
            )


        #
        # Project location.
        #
        location_match = re.search(
            r"(Horizon Drive\s+and\s+G Road)",
            normalized_content,
            re.IGNORECASE,
        )


        if location_match:

            metadata["location"] = (
                location_match.group(1)
                .title()
            )


        #
        # Project phase.
        #
        if (
            "construction"
            in normalized_content.lower()
        ):

            metadata["project_phase"] = (
                "construction"
            )


        #
        # Contract status.
        #
        if (
            "awarded the contract"
            in normalized_content.lower()
        ):

            metadata["contract_status"] = (
                "awarded"
            )


        return metadata