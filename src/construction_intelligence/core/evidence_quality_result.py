"""
Evidence quality result model.

Represents the reliability and completeness of an evidence record
independent of whether it matches a specific project.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceQualityResult:
    """
    Represents the quality of an evidence source.

    Attributes
    ----------
    quality_score:
        Confidence in the reliability of the evidence source.
        Value between 0.0 and 1.0.

    reasons:
        Human-readable explanations for the assigned score.
    """

    quality_score: float

    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate quality score boundaries."""

        if not 0.0 <= self.quality_score <= 1.0:
            raise ValueError(
                "Quality score must be between 0.0 and 1.0."
            )

    @classmethod
    def empty(
        cls,
    ) -> EvidenceQualityResult:
        """Create an empty quality result."""

        return cls(
            quality_score=0.0,
            reasons=(),
        )

    def add_reason(
        self,
        reason: str,
    ) -> EvidenceQualityResult:
        """
        Return a new quality result with an additional reason.
        """

        return EvidenceQualityResult(
            quality_score=self.quality_score,
            reasons=(
                *self.reasons,
                reason,
            ),
        )