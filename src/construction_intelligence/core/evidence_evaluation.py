"""
Evidence evaluation domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from construction_intelligence.core.evidence_evaluation_classifier import (
    EvidenceEvaluationClassifier,
)

from construction_intelligence.core.evidence_evaluation_status import (
    EvidenceEvaluationStatus,
)

from construction_intelligence.core.evidence_resource import (
    EvidenceResource,
)

from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
)


@dataclass
class EvidenceEvaluation:
    """
    Represents an evaluation of evidence against a project.
    """

    project_id: ProjectId

    evidence_id: EvidenceId

    match_score: float

    quality_score: float

    reasons: tuple[str, ...]

    resources: tuple[EvidenceResource, ...] = ()

    evaluated_at: datetime = field(
        default_factory=datetime.utcnow
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    @property
    def overall_score(
        self,
    ) -> float:
        """
        Combined confidence score.
        """

        return (
            self.match_score
            *
            self.quality_score
        )

    @property
    def status(
        self,
    ) -> EvidenceEvaluationStatus:
        """
        Human-readable confidence classification.
        """

        return EvidenceEvaluationClassifier.classify(
            self.overall_score
        )