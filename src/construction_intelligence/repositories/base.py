from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(Generic[T]):
    """Simple in-memory repository."""

    def __init__(self):
        self._items: dict = {}

    def add(self, item: T) -> None:
        self._items[item.id] = item

    def get(self, item_id):
        return self._items.get(item_id)

    def list(self) -> list[T]:
        return list(self._items.values())

    def remove(self, item_id) -> None:
        self._items.pop(item_id, None)

    def exists(self, item_id) -> bool:
        return item_id in self._items

    def clear(self) -> None:
        self._items.clear()

    def __len__(self) -> int:
        return len(self._items)