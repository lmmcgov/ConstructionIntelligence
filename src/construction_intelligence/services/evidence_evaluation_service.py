"""
Service for evaluating evidence against a project.

Combines:
- project/evidence matching
- evidence source quality
- evaluation persistence
"""

from __future__ import annotations

from typing import Protocol

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.evidence_evaluation import (
    EvidenceEvaluation,
)

from construction_intelligence.core.evidence_match_result import (
    EvidenceMatchResult,
)

from construction_intelligence.core.evidence_score import (
    EvidenceScore,
)

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.repositories.sqlite.sqlite_evidence_evaluation_repository import (
    SQLiteEvidenceEvaluationRepository,
)

from construction_intelligence.services.evidence_matcher_service import (
    EvidenceMatcherService,
)

from construction_intelligence.services.evidence_scoring_service import (
    EvidenceScoringService,
)


class EvidenceMatcher(Protocol):
    """
    Interface required by evidence matchers.

    Implementations may include:
    - rule-based matching
    - Gemini-powered matching
    """

    def match(
        self,
        project: Project,
        evidence: Evidence,
    ) -> EvidenceMatchResult:
        """
        Determine whether evidence matches a project.
        """
        ...


class EvidenceEvaluationService:
    """
    Evaluates the overall confidence that evidence supports
    a construction project.

    Combines:

    EvidenceMatcher:
        Does this evidence refer to this project?

    EvidenceScoringService:
        How reliable is this evidence source?

    Can optionally persist evaluations.
    """

    def __init__(
        self,
        matcher: EvidenceMatcher | None = None,
        scorer: EvidenceScoringService | None = None,
        repository: SQLiteEvidenceEvaluationRepository | None = None,
    ) -> None:

        #
        # Default matcher remains the rule-based matcher.
        #
        # Existing behavior:
        #
        # EvidenceEvaluationService()
        #
        # New Gemini behavior:
        #
        # EvidenceEvaluationService(
        #     matcher=GeminiEvidenceMatcherService()
        # )
        #
        self.matcher = (
            matcher
            if matcher is not None
            else EvidenceMatcherService()
        )

        self.scorer = (
            scorer
            if scorer is not None
            else EvidenceScoringService()
        )

        self.repository = repository

    def evaluate(
        self,
        project: Project,
        evidence: Evidence,
    ) -> EvidenceScore:
        """
        Evaluate evidence relevance and reliability.

        Returns:
            EvidenceScore containing:
            - match score
            - quality score
            - combined reasons
            - supporting resources
        """

        match_result = self.matcher.match(
            project,
            evidence,
        )

        quality_result = self.scorer.score(
            evidence,
        )

        reasons = (
            *match_result.reasons,
            *quality_result.reasons,
        )

        return EvidenceScore(
            match_score=match_result.match_score,
            quality_score=quality_result.quality_score,
            reasons=reasons,
            resources=match_result.resources,
        )

    def evaluate_and_store(
        self,
        project: Project,
        evidence: Evidence,
    ) -> EvidenceEvaluation:
        """
        Evaluate evidence and persist the result.

        Requires an EvidenceEvaluationRepository.
        """

        if self.repository is None:
            raise ValueError(
                "Evidence evaluation repository is required "
                "for persistence."
            )

        score = self.evaluate(
            project,
            evidence,
        )

        evaluation = EvidenceEvaluation(
            project_id=project.id,
            evidence_id=evidence.id,
            match_score=score.match_score,
            quality_score=score.quality_score,
            reasons=score.reasons,
            resources=score.resources,
        )

        self.repository.add(
            evaluation
        )

        return evaluation