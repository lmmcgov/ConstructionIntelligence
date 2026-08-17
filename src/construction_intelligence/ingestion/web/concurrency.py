"""
Lightweight concurrency helper for I/O-bound polling.

Feed and sitemap polling is network-I/O-bound and
low-volume (a handful of sources per country), so a
thread pool is sufficient and an async rewrite of the
discovery layer is not warranted.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def parallel_map(
    fn: Callable[[T], R],
    items: Iterable[T],
    max_workers: int = 8,
) -> list[R]:
    """
    Apply fn to each item concurrently.

    Callers that need per-item failure isolation
    should catch exceptions inside fn — a failure
    here fails the whole call.
    """

    items = list(items)

    if not items:

        return []


    with ThreadPoolExecutor(
        max_workers=min(
            max_workers,
            len(items),
        )
    ) as executor:

        return list(
            executor.map(
                fn,
                items,
            )
        )
