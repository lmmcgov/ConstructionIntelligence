"""
Evidence evaluation status definitions.
"""

from enum import Enum


class EvidenceEvaluationStatus(str, Enum):
    """
    Human-readable confidence classification
    derived from the overall evaluation score.
    """

    CONFIRMED = "confirmed"

    LIKELY = "likely"

    UNCERTAIN = "uncertain"

    REJECTED = "rejected"