"""
Generic in-memory repository implementation.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from .base import Repository

T = TypeVar("T")
ID = TypeVar("ID")


class InMemoryRepository(
    Repository[T, ID],
    Generic[T, ID],
):
    """Simple in-memory repository."""

    def __init__(self) -> None:
        self._items: dict[ID, T] = {}

    def add(
        self,
        item: T,
    ) -> None:
        self._items[item.id] = item

    def update(
        self,
        item: T,
    ) -> None:
        self._items[item.id] = item

    def get(
        self,
        item_id: ID,
    ) -> T | None:
        return self._items.get(item_id)

    def list(
        self,
    ) -> list[T]:
        return list(self._items.values())

    def remove(
        self,
        item_id: ID,
    ) -> None:
        self._items.pop(item_id, None)

    def exists(
        self,
        item_id: ID,
    ) -> bool:
        return item_id in self._items

    def clear(
        self,
    ) -> None:
        self._items.clear()

    def count(
        self,
    ) -> int:
        return len(self._items)

    def __len__(
        self,
    ) -> int:
        return self.count()