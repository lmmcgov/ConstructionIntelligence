"""
Evidence discovery and evaluation pipeline.

Coordinates:

- Web evidence discovery
- Evidence ingestion
- Evidence evaluation
- Evidence quality filtering
- Evidence ranking
"""

from __future__ import annotations

from dataclasses import dataclass


from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.evidence_score import (
    EvidenceScore,
)

from construction_intelligence.ingestion.web.web_evidence_ingestion_service import (
    WebEvidenceIngestionService,
)

from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)

from construction_intelligence.services.evidence_quality_gate_service import (
    EvidenceQualityGateService,
)


@dataclass(frozen=True)
class EvaluatedEvidence:
    """
    Evidence record with evaluation result.
    """

    evidence: Evidence

    score: EvidenceScore



class EvidencePipelineService:
    """
    Complete construction evidence pipeline.

    Flow:

    Project
       |
       v
    Discover URLs
       |
       v
    Ingest Evidence
       |
       v
    Evaluate Evidence
       |
       v
    Quality Gate
       |
       v
    Rank Evidence
    """


    def __init__(
        self,
        ingestion_service: WebEvidenceIngestionService,
        evaluation_service: EvidenceEvaluationService,
        quality_gate_service: EvidenceQualityGateService | None = None,
    ) -> None:

        self.ingestion_service = (
            ingestion_service
        )

        self.evaluation_service = (
            evaluation_service
        )

        self.quality_gate_service = (
            quality_gate_service
            if quality_gate_service is not None
            else EvidenceQualityGateService()
        )


    def run(
        self,
        project: Project,
    ) -> list[EvaluatedEvidence]:
        """
        Discover, ingest, evaluate,
        quality filter, and rank evidence.
        """

        evidence_records = (
            self.ingestion_service.ingest(
                project
            )
        )


        evaluated: list[EvaluatedEvidence] = []

        rejected_count = 0


        for evidence in evidence_records:

            try:

                score = (
                    self.evaluation_service.evaluate(
                        project,
                        evidence,
                    )
                )


                #
                # Quality gate filtering.
                #
                if not self.quality_gate_service.accept(
                    evidence,
                    score,
                ):

                    rejected_count += 1

                    self._log_rejection(
                        evidence,
                        score,
                    )

                    continue


                evaluated.append(
                    EvaluatedEvidence(
                        evidence=evidence,
                        score=score,
                    )
                )


            except Exception as error:

                #
                # One bad evidence record should
                # never terminate the pipeline.
                #
                self._log_failure(
                    evidence,
                    error,
                )

                continue



        #
        # Highest scoring evidence first.
        #
        ranked = sorted(
            evaluated,
            key=lambda item: (
                item.score.overall_score
            ),
            reverse=True,
        )


        print()

        print(
            "Evidence pipeline summary"
        )

        print(
            "-------------------------"
        )

        print(
            f"Accepted evidence: {len(ranked)}"
        )

        print(
            f"Rejected evidence: {rejected_count}"
        )


        return ranked



    def _log_rejection(
        self,
        evidence: Evidence,
        score: EvidenceScore,
    ) -> None:
        """
        Log evidence rejected by quality gate.
        """

        print()

        print(
            "Evidence rejected:"
        )

        print(
            evidence.title
        )

        print(
            evidence.url
        )

        print(
            f"Match score: "
            f"{score.match_score:.2f}"
        )

        print(
            self.quality_gate_service.rejection_reason(
                evidence,
                score,
            )
        )



    def _log_failure(
        self,
        evidence: Evidence,
        error: Exception,
    ) -> None:
        """
        Log unexpected evidence processing failures.
        """

        print()

        print(
            "Evidence evaluation failed:"
        )

        print(
            evidence.url
        )

        print(
            f"Reason: {error}"
        )