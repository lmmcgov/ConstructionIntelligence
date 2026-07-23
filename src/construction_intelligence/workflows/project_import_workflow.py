"""
Application workflow for importing construction project candidates.
"""

from collections.abc import Iterable
from time import perf_counter

from construction_intelligence.ingestion.osm.evidence_factory import (
    OSMEvidenceFactory,
)
from construction_intelligence.models.construction_project_candidate import (
    ConstructionProjectCandidate,
)
from construction_intelligence.models.project_import_summary import (
    ProjectImportSummary,
)
from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)
from construction_intelligence.services.evidence_service import (
    EvidenceService,
)
from construction_intelligence.services.project_service import (
    ProjectService,
)
from construction_intelligence.workflows.project_import_report_builder import (
    ProjectImportReportBuilder,
)


class ProjectImportWorkflow:
    """
    Coordinates importing ConstructionProjectCandidate objects into
    the Construction Intelligence domain model.
    """

    def __init__(
        self,
        project_service: ProjectService,
        evidence_service: EvidenceService,
        evidence_evaluation_service: EvidenceEvaluationService | None = None,
    ) -> None:
        self.project_service = project_service
        self.evidence_service = evidence_service
        self.evidence_factory = OSMEvidenceFactory()

        self.evidence_evaluation_service = (
            evidence_evaluation_service
            if evidence_evaluation_service is not None
            else None
        )

    def import_candidates(
        self,
        candidates: Iterable[
            ConstructionProjectCandidate
        ],
    ) -> ProjectImportSummary:
        """
        Import a collection of construction project candidates.

        Returns
        -------
        ProjectImportSummary
            Summary statistics describing the completed import.
        """

        builder = ProjectImportReportBuilder()

        start = perf_counter()

        for candidate in candidates:

            builder.candidate_processed()

            try:
                #
                # Import or update the project.
                #
                project_result = (
                    self.project_service.import_candidate(
                        candidate
                    )
                )

                if project_result.created:
                    builder.project_created()
                else:
                    builder.project_updated()

                #
                # Create evidence object.
                #
                evidence = self.evidence_factory.create(
                    project_result.project,
                    candidate,
                )

                #
                # Persist evidence.
                #
                evidence_result = (
                    self.evidence_service.create_evidence(
                        evidence
                    )
                )

                if evidence_result.created:
                    builder.evidence_added()
                else:
                    builder.evidence_reused()

                #
                # Associate evidence with the project.
                #
                self.project_service.add_evidence(
                    project_result.project.id,
                    evidence_result.evidence.id,
                )

                #
                # Evaluate evidence quality and project match.
                #
                # This is optional during transition so existing
                # imports continue to work until the repository is wired.
                #
                if self.evidence_evaluation_service is not None:

                    self.evidence_evaluation_service.evaluate_and_store(
                        project_result.project,
                        evidence_result.evidence,
                    )

            except Exception as exc:
                builder.failure(
                    f"[import_candidate] "
                    f"{candidate.origin_id}: {exc}"
                )

        elapsed = perf_counter() - start

        return builder.build(elapsed)