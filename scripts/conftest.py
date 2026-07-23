"""
Shared pytest fixtures for ConstructionIntelligence tests.
"""

import pytest

from uuid import uuid4

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)

from construction_intelligence.services.evidence_scoring_service import (
    EvidenceScoringService,
)


@pytest.fixture
def evaluator() -> EvidenceEvaluationService:
    """
    Evidence evaluation service fixture.
    """

    return EvidenceEvaluationService()


@pytest.fixture
def scorer() -> EvidenceScoringService:
    """
    Evidence scoring service fixture.
    """

    return EvidenceScoringService()


@pytest.fixture
def project() -> Project:
    """
    Standard construction project fixture.

    Uses a valid UUID because Project.id
    is UUID validated.
    """

    return Project(
        id=uuid4(),
        name="Horizon Glen Drive Improvements",
        city="Grand Junction",
        state="Colorado",
        country="United States",
        road_name="Horizon Glen Drive",
    )