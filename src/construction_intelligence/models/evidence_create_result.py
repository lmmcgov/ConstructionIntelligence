from dataclasses import dataclass

from construction_intelligence.core.evidence import Evidence


@dataclass(frozen=True)
class EvidenceCreateResult:
    """
    Result of creating or reusing an Evidence object.
    """

    evidence: Evidence
    created: bool