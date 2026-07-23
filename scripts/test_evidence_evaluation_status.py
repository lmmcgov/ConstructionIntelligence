"""
Test evidence evaluation status classification.
"""

from construction_intelligence.core.evidence_evaluation_classifier import (
    EvidenceEvaluationClassifier,
)
from construction_intelligence.core.evidence_evaluation_status import (
    EvidenceEvaluationStatus,
)


def main() -> None:

    tests = [
        (
            0.95,
            EvidenceEvaluationStatus.CONFIRMED,
        ),
        (
            0.75,
            EvidenceEvaluationStatus.LIKELY,
        ),
        (
            0.50,
            EvidenceEvaluationStatus.UNCERTAIN,
        ),
        (
            0.20,
            EvidenceEvaluationStatus.REJECTED,
        ),
    ]

    print(
        "Evidence evaluation status test"
    )
    print(
        "------------------------------"
    )

    for score, expected in tests:

        result = (
            EvidenceEvaluationClassifier.classify(
                score
            )
        )

        print(
            f"{score:.2f} -> {result.value}"
        )

        assert result == expected

    print(
        "\nEvidence evaluation status test: PASS"
    )


if __name__ == "__main__":
    main()