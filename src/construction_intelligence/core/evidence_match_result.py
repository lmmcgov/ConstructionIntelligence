"""
Evidence matching result model.

Represents how strongly an evidence record appears
to correspond to a specific project.
"""

from __future__ import annotations

from dataclasses import dataclass

from construction_intelligence.core.evidence_resource import (
    EvidenceResource,
)


@dataclass(frozen=True)
class EvidenceMatchResult:
    """
    Result of matching evidence to a project.

    Attributes
    ----------
    match_score:
        Confidence that the evidence refers to the project.
        Value between 0.0 and 1.0.

    reasons:
        Human-readable explanations for the score.

    resources:
        External resources supporting the match decision.
    """

    match_score: float

    reasons: tuple[str, ...]

    resources: tuple[EvidenceResource, ...] = ()

    def __post_init__(self) -> None:
        """Validate match score boundaries."""

        if not 0.0 <= self.match_score <= 1.0:
            raise ValueError(
                "Match score must be between 0.0 and 1.0."
            )

    @classmethod
    def empty(
        cls,
    ) -> EvidenceMatchResult:
        """Create an empty match result."""

        return cls(
            match_score=0.0,
            reasons=(),
            resources=(),
        )

    def add_reason(
        self,
        reason: str,
    ) -> EvidenceMatchResult:
        """
        Return a new result with an additional reason.
        """

        return EvidenceMatchResult(
            match_score=self.match_score,
            reasons=(
                *self.reasons,
                reason,
            ),
            resources=self.resources,
        )