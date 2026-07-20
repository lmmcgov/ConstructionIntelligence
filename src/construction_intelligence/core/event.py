"""
Event domain model.

Events record significant occurrences throughout the system.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from .ids import EventId, new_id


class Event(BaseModel):
    id: EventId = Field(default_factory=new_id)

    event_type: str

    source: str
    message: str

    data: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )