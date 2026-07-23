"""
Service for evaluating evidence source quality.
"""

from __future__ import annotations

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_quality_result import (
    EvidenceQualityResult,
)
from construction_intelligence.core.evidence_source import (
    EvidenceSource,
)


class EvidenceScoringService:
    """
    Calculates the quality of an evidence record.

    This service evaluates:
    - source reliability
    - evidence completeness
    - metadata availability

    It does not determine whether evidence matches
    a specific project.
    """

    SOURCE_QUALITY = {
        #
        # Official government sources
        #
        EvidenceSource.GOVERNMENT_RECORD: 0.95,
        EvidenceSource.GOVERNMENT_WEBSITE: 0.95,
        EvidenceSource.CITY_PROJECT_PAGE: 0.95,
        EvidenceSource.PERMIT: 0.95,
        EvidenceSource.PROCUREMENT: 0.95,
        EvidenceSource.PLANNING_DOCUMENT: 0.90,

        #
        # Private project sources
        #
        EvidenceSource.CONTRACTOR_NOTICE: 0.80,
        EvidenceSource.DEVELOPER_NOTICE: 0.80,

        #
        # Public reporting sources
        #
        EvidenceSource.NEWS_ARTICLE: 0.70,

        #
        # Mapping sources
        #
        EvidenceSource.OSM: 0.50,

        #
        # Generic web sources
        #
        EvidenceSource.OTHER_WEB: 0.40,
    }

    def score(
        self,
        evidence: Evidence,
    ) -> EvidenceQualityResult:
        """
        Calculate evidence quality.
        """

        quality_score = self.SOURCE_QUALITY.get(
            evidence.source,
            0.25,
        )

        reasons: list[str] = []

        reasons.append(
            f"Source quality baseline: "
            f"{quality_score:.2f}"
        )

        #
        # Evidence completeness bonuses
        #
        if evidence.title:
            quality_score += 0.02

            reasons.append(
                "Evidence has a title"
            )

        if evidence.content:
            quality_score += 0.05

            reasons.append(
                "Evidence contains text content"
            )

        if evidence.url:
            quality_score += 0.03

            reasons.append(
                "Evidence contains a URL"
            )

        if evidence.metadata:
            quality_score += 0.05

            reasons.append(
                "Evidence contains metadata"
            )

        #
        # Normalize score
        #
        quality_score = min(
            quality_score,
            1.0,
        )

        return EvidenceQualityResult(
            quality_score=quality_score,
            reasons=tuple(reasons),
        )