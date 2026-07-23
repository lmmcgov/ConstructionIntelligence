"""
Classifies evidence evaluation confidence levels.
"""

from construction_intelligence.core.evidence_evaluation_status import (
    EvidenceEvaluationStatus,
)


class EvidenceEvaluationClassifier:
    """
    Converts numeric evidence scores into
    human-readable confidence states.
    """

    @staticmethod
    def classify(
        overall_score: float,
    ) -> EvidenceEvaluationStatus:
        """
        Determine evaluation status.

        Thresholds:

        >= 0.85:
            CONFIRMED

        >= 0.60:
            LIKELY

        >= 0.40:
            UNCERTAIN

        < 0.40:
            REJECTED
        """

        if overall_score >= 0.85:
            return EvidenceEvaluationStatus.CONFIRMED

        if overall_score >= 0.60:
            return EvidenceEvaluationStatus.LIKELY

        if overall_score >= 0.40:
            return EvidenceEvaluationStatus.UNCERTAIN

        return EvidenceEvaluationStatus.REJECTED