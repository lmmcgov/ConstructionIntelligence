"""
Evidence quality gate service.

Determines whether evaluated evidence is strong enough
to be included in the final project intelligence pipeline.

Filters:

- Weak project matches
- Non-construction references
- Administrative documents
- Generic location matches
- Low-confidence evidence
"""

from __future__ import annotations

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.evidence_score import (
    EvidenceScore,
)


class EvidenceQualityGateService:
    """
    Accepts or rejects evidence after evaluation.

    Ranking happens elsewhere.

    This service answers:

    "Is this evidence sufficiently relevant
     to become project intelligence?"
    """


    def __init__(
        self,
        minimum_match_score: float = 0.35,
    ) -> None:

        self.minimum_match_score = (
            minimum_match_score
        )


    def accept(
        self,
        evidence: Evidence,
        score: EvidenceScore,
    ) -> bool:
        """
        Determine whether evidence should
        continue through the pipeline.
        """


        #
        # Minimum project relevance threshold.
        #
        if (
            score.match_score
            <
            self.minimum_match_score
        ):

            return False


        #
        # Reject obvious unrelated content.
        #
        if self._contains_negative_signals(
            evidence
        ):

            return False


        #
        # Require construction relevance.
        #
        if not self._has_construction_signal(
            evidence
        ):

            return False


        #
        # Strong evidence.
        #
        # Examples:
        #
        # - Government documents
        # - Contractor announcements
        # - Official project pages
        #
        if (
            score.match_score
            >=
            0.60
        ):

            return True


        #
        # Moderate evidence.
        #
        # Examples:
        #
        # - Local news articles
        # - Planning documents
        # - Community project pages
        #
        if (
            score.match_score
            >=
            self.minimum_match_score
            and
            self._has_location_signal(
                evidence
            )
        ):

            return True


        return False


    def rejection_reason(
        self,
        evidence: Evidence,
        score: EvidenceScore,
    ) -> str:
        """
        Explain why evidence was rejected.
        """


        if (
            score.match_score
            <
            self.minimum_match_score
        ):

            return (
                "Match score below threshold"
            )


        if self._contains_negative_signals(
            evidence
        ):

            return (
                "Negative intent signals detected"
            )


        if not self._has_construction_signal(
            evidence
        ):

            return (
                "No construction relevance detected"
            )


        if not self._has_location_signal(
            evidence
        ):

            return (
                "No project location confirmation"
            )


        return (
            "Evidence rejected by quality rules"
        )


    def _has_construction_signal(
        self,
        evidence: Evidence,
    ) -> bool:
        """
        Determine whether evidence contains
        construction-related terminology.
        """

        text = self._combined_text(
            evidence
        )


        construction_terms = [
            "construction",
            "roundabout",
            "road improvement",
            "roadway",
            "intersection",
            "transportation",
            "corridor",
            "engineering",
            "contract",
            "contractor",
            "bid",
            "award",
            "awarded",
            "infrastructure",
            "project",
            "capital improvement",
        ]


        return any(
            term in text
            for term in construction_terms
        )


    def _has_project_metadata(
        self,
        evidence: Evidence,
    ) -> bool:
        """
        Determine whether evidence contains
        structured project metadata.
        """

        metadata = (
            evidence.metadata
            or {}
        )


        strong_fields = [
            "contractor",
            "construction_start_date",
            "expected_completion",
            "contract_status",
            "project_phase",
        ]


        matches = [
            field
            for field in strong_fields
            if field in metadata
        ]


        return (
            len(matches)
            >=
            2
        )


    def _has_location_signal(
        self,
        evidence: Evidence,
    ) -> bool:
        """
        Determine whether evidence contains
        project location signals.
        """

        text = self._combined_text(
            evidence
        )


        location_terms = [
            "grand junction",
            "colorado",
            "horizon drive",
            "g road",
            "27 road",
        ]


        return any(
            term in text
            for term in location_terms
        )


    def _contains_negative_signals(
        self,
        evidence: Evidence,
    ) -> bool:
        """
        Detect obviously unrelated sources.
        """

        text = self._combined_text(
            evidence
        )


        negative_terms = [
            "playstation",
            "steam",
            "imdb",
            "movie",
            "video game",
            "gaming",
            "casting",
            "bank account",
            "insurance",
            "hotel directory",
            "restaurant menu",
            "jobs",
            "careers",
        ]


        return any(
            term in text
            for term in negative_terms
        )


    def _combined_text(
        self,
        evidence: Evidence,
    ) -> str:
        """
        Combine evidence fields for analysis.
        """

        parts = [
            evidence.title or "",
            evidence.content or "",
        ]


        return (
            " "
            .join(parts)
            .lower()
        )