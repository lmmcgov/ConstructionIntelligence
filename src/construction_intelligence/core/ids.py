"""
Shared identifier helpers used throughout the Construction Intelligence platform.
"""

from uuid import UUID, uuid4

ProjectId = UUID
MissionId = UUID
WorkflowId = UUID
TaskId = UUID
EvidenceId = UUID
AgentId = UUID
EventId = UUID


def new_id() -> UUID:
    """Create a new UUID4 identifier."""
    return uuid4()