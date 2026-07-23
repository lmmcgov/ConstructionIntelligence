"""
Maps Gemini CLI responses into Construction Intelligence models.
"""

from construction_intelligence.core.evidence_evaluation import (
    EvidenceEvaluation,
)
from construction_intelligence.core.evidence_resource import (
    EvidenceResource,
)
from construction_intelligence.integrations.gemini_cli.schemas import (
    GeminiEvaluationResponse,
)


class GeminiEvaluationMapper:
    """
    Converts Gemini output into domain objects.
    """

    def to_resources(
        self,
        response: GeminiEvaluationResponse,
    ) -> tuple[EvidenceResource, ...]:

        return tuple(
            EvidenceResource(
                url=resource.url,
                title=resource.title,
                source_name=resource.source,
                resource_type=resource.resource_type,
                excerpt=resource.excerpt,
            )
            for resource in response.resources
        )

    def to_evaluation(
        self,
        response: GeminiEvaluationResponse,
        project_id,
        evidence_id,
    ) -> EvidenceEvaluation:

        return EvidenceEvaluation(
            project_id=project_id,
            evidence_id=evidence_id,
            match_score=response.match_score,
            quality_score=1.0,
            reasons=response.reasons,
            resources=self.to_resources(
                response
            ),
        )