"""
Abstract repository interface.

Concrete implementations may store objects in memory, SQLite,
PostgreSQL, or any other persistence mechanism.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """Abstract base class for repositories."""

    @abstractmethod
    def add(
        self,
        item: T,
    ) -> None:
        """Persist a new item."""

    @abstractmethod
    def update(
        self,
        item: T,
    ) -> None:
        """Persist changes to an existing item."""

    @abstractmethod
    def get(
        self,
        item_id: ID,
    ) -> T | None:
        """Retrieve an item by its identifier."""

    @abstractmethod
    def list(
        self,
    ) -> list[T]:
        """Return all stored items."""

    @abstractmethod
    def remove(
        self,
        item_id: ID,
    ) -> None:
        """Delete an item."""

    @abstractmethod
    def exists(
        self,
        item_id: ID,
    ) -> bool:
        """Return True if the item exists."""

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """Remove all items."""

    @abstractmethod
    def count(
        self,
    ) -> int:
        """Return the number of stored items."""