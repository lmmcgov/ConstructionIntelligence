"""
Gemini-powered evidence matching service.

Uses Gemini CLI to evaluate whether evidence
corresponds to a construction project.
"""

from __future__ import annotations

from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.evidence_match_result import (
    EvidenceMatchResult,
)

from construction_intelligence.core.evidence_resource import (
    EvidenceResource,
)

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.integrations.gemini_cli.runner import (
    GeminiCLIRunner,
)

from construction_intelligence.integrations.gemini_cli.parser import (
    GeminiResponseParser,
)

from construction_intelligence.integrations.gemini_cli.prompts import (
    GeminiPromptBuilder,
)


class GeminiEvidenceMatcherService:
    """
    Evaluates evidence/project relationships using Gemini.
    """

    def __init__(
        self,
        runner: GeminiCLIRunner | None = None,
    ) -> None:

        self.runner = (
            runner
            if runner is not None
            else GeminiCLIRunner()
        )

        self.parser = GeminiResponseParser()

        self.prompt_builder = (
            GeminiPromptBuilder()
        )

    def match(
        self,
        project: Project,
        evidence: Evidence,
    ) -> EvidenceMatchResult:
        """
        Determine whether evidence matches project.
        """

        prompt = (
            self.prompt_builder
            .build_evidence_match_prompt(
                project,
                evidence,
            )
        )

        response = self.runner.run(
            prompt
        )

        gemini_result = (
            self.parser.parse(
                response
            )
        )

        #
        # Convert Gemini integration objects
        # into domain objects.
        #
        resources = tuple(
            EvidenceResource(
                url=resource.url,
                title=resource.title,
                source_name=resource.source,
                resource_type=resource.resource_type,
                excerpt=resource.excerpt,
            )
            for resource in gemini_result.resources
        )

        return EvidenceMatchResult(
            match_score=(
                gemini_result.match_score
            ),
            reasons=(
                gemini_result.reasons
            ),
            resources=resources,
        )