"""
Business logic for managing Evidence objects.
"""

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.ids import (
    EvidenceId,
)
from construction_intelligence.models.evidence_create_result import (
    EvidenceCreateResult,
)
from construction_intelligence.repositories.evidence_repository import (
    EvidenceRepository,
)


class EvidenceService:
    """Business logic for managing Evidence objects."""

    def __init__(
        self,
        repository: EvidenceRepository,
    ) -> None:
        self.repository = repository

    # ---------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------

    def _require_evidence(
        self,
        evidence_id: EvidenceId,
    ) -> Evidence:
        """Return an evidence object or raise an error."""

        evidence = self.repository.get(
            evidence_id
        )

        if evidence is None:
            raise ValueError(
                f"Evidence {evidence_id} does not exist."
            )

        return evidence

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def create_evidence(
        self,
        evidence: Evidence,
    ) -> EvidenceCreateResult:
        """
        Create evidence unless matching evidence already exists.

        Returns an EvidenceCreateResult indicating whether a new
        evidence record was created or an existing record was reused.
        """

        existing = self.repository.get_by_origin_id(
            evidence.source,
            evidence.origin_id,
        )

        if existing:
            return EvidenceCreateResult(
                evidence=existing[0],
                created=False,
            )

        self.repository.add(
            evidence
        )

        return EvidenceCreateResult(
            evidence=evidence,
            created=True,
        )

    def get_evidence(
        self,
        evidence_id: EvidenceId,
    ) -> Evidence | None:
        """Retrieve evidence."""

        return self.repository.get(
            evidence_id
        )

    def list_evidence(
        self,
    ) -> list[Evidence]:
        """Return all evidence."""

        return self.repository.list()

    def delete_evidence(
        self,
        evidence_id: EvidenceId,
    ) -> None:
        """Delete evidence."""

        self._require_evidence(
            evidence_id
        )

        self.repository.remove(
            evidence_id
        )