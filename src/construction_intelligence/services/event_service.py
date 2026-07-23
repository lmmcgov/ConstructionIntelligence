"""
Event service.

Contains the business logic for creating, retrieving,
listing, and deleting events.
"""

from typing import Any

from construction_intelligence.core.event import Event
from construction_intelligence.core.ids import EventId
from construction_intelligence.repositories.event_repository import EventRepository


class EventService:
    """Service for managing events."""

    def __init__(self, repository: EventRepository):
        self._repository = repository

    def create_event(
        self,
        event_type: str,
        source: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> Event:
        """Create and store an event."""

        self._validate_event_type(event_type)
        self._validate_source(source)

        event = Event(
            event_type=event_type,
            source=source,
            message=message,
            data=data or {},
        )

        self._repository.add(event)

        return event

    def get_event(self, event_id: EventId) -> Event:
        """Return an event by ID."""

        return self._require_event(event_id)

    def list_events(self) -> list[Event]:
        """Return all events."""

        return self._repository.list()

    def delete_event(self, event_id: EventId) -> None:
        """Delete an event."""

        self._require_event(event_id)
        self._repository.remove(event_id)

    def _require_event(self, event_id: EventId) -> Event:
        """Return an event or raise an exception."""

        event = self._repository.get(event_id)

        if event is None:
            raise ValueError(f"Event '{event_id}' does not exist.")

        return event

    def _validate_event_type(self, event_type: str) -> None:
        """Validate the event type."""

        if not event_type.strip():
            raise ValueError("Event type cannot be empty.")

    def _validate_source(self, source: str) -> None:
        """Validate the event source."""

        if not source.strip():
            raise ValueError("Event source cannot be empty.")