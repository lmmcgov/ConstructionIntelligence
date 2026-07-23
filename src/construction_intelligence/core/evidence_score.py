"""
Evidence matching score model.

Represents confidence that an evidence record supports
a specific construction project.
"""

from __future__ import annotations

from dataclasses import dataclass

from construction_intelligence.core.evidence_resource import (
    EvidenceResource,
)


@dataclass(frozen=True)
class EvidenceScore:
    """
    Represents the strength of the relationship between
    a project and a piece of evidence.

    Attributes
    ----------
    match_score:
        Confidence that the evidence refers to this project.

    quality_score:
        Confidence in the reliability of the source itself.

    reasons:
        Explanation of scoring factors.

    resources:
        External resources supporting the evaluation.
    """

    match_score: float

    quality_score: float

    reasons: tuple[str, ...]

    resources: tuple[EvidenceResource, ...] = ()

    def __post_init__(self) -> None:
        """Validate score ranges."""

        if not 0.0 <= self.match_score <= 1.0:
            raise ValueError(
                "Match score must be between 0.0 and 1.0."
            )

        if not 0.0 <= self.quality_score <= 1.0:
            raise ValueError(
                "Quality score must be between 0.0 and 1.0."
            )

    @property
    def overall_score(
        self,
    ) -> float:
        """
        Combined confidence score.

        A strong source about the wrong project should
        not score highly, therefore match confidence
        is multiplied by source quality.
        """

        return (
            self.match_score
            *
            self.quality_score
        )