"""
Shared identifier helpers used throughout the Construction Intelligence platform.
"""

import hashlib
from uuid import UUID, uuid4


#
# Domain identifier type aliases
#

ProjectId = UUID
EvidenceId = UUID
ImportRunId = UUID

MissionId = UUID
WorkflowId = UUID
TaskId = UUID
AgentId = UUID
EventId = UUID


def new_id() -> UUID:
    """Generate a new UUID4 identifier."""
    return uuid4()


def build_origin_id(
    connected_way_ids: list[int],
) -> str:
    """
    Build a deterministic identifier for an OSM construction project.

    The identifier is derived from the sorted connected OSM way IDs,
    making it stable across repeated pipeline runs.
    """

    normalized = ",".join(
        str(way_id)
        for way_id in sorted(connected_way_ids)
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()