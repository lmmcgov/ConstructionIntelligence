"""
In-memory job store for GeoJSON upload processing.

Single-process, in-memory only -- results are lost on server
restart. Appropriate for a local, single-user tool; not meant to
survive a restart or scale across multiple processes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from threading import Lock
from typing import Any


class ProjectJobStatus(StrEnum):

    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


@dataclass
class ProjectJobResult:
    """
    Processing status for a single project within a job.
    """

    project_name: str

    status: ProjectJobStatus = (
        ProjectJobStatus.PENDING
    )

    evidence_count: int = 0

    evidence: list[dict[str, Any]] = field(
        default_factory=list
    )

    warning: str | None = None

    error: str | None = None


@dataclass
class Job:
    """
    A single GeoJSON upload's processing job -- one
    ProjectJobResult per feature in the uploaded file.
    """

    id: str

    created_at: datetime

    truncated: bool = False

    results: list[ProjectJobResult] = field(
        default_factory=list
    )

    @property
    def is_complete(self) -> bool:

        return all(
            result.status
            in (
                ProjectJobStatus.DONE,
                ProjectJobStatus.ERROR,
            )
            for result in self.results
        )


#
# Repeated uploads would otherwise grow this dict forever --
# oldest jobs are evicted once this many are retained.
#
MAX_RETAINED_JOBS = 50


class JobStore:
    """
    Thread-safe, bounded, in-memory store of upload jobs.

    Written to from background worker threads and read from
    request-handling coroutines, so all access goes through a
    lock.
    """

    def __init__(self) -> None:

        self._jobs: dict[str, Job] = {}

        #
        # Insertion order, for oldest-first eviction. dict
        # preserves insertion order in Python, but a separate
        # list keeps eviction O(1) instead of re-deriving order
        # from dict iteration each time.
        #
        self._order: list[str] = []

        self._lock = Lock()


    def create(
        self,
        job_id: str,
        project_names: list[str],
        truncated: bool,
    ) -> Job:

        job = Job(
            id=job_id,
            created_at=datetime.now(UTC),
            truncated=truncated,
            results=[
                ProjectJobResult(project_name=name)
                for name in project_names
            ],
        )

        with self._lock:

            self._jobs[job_id] = job

            self._order.append(job_id)

            while len(self._order) > MAX_RETAINED_JOBS:

                oldest_id = self._order.pop(0)

                self._jobs.pop(oldest_id, None)

        return job


    def get(
        self,
        job_id: str,
    ) -> Job | None:

        with self._lock:

            return self._jobs.get(job_id)


    def update_result(
        self,
        job_id: str,
        index: int,
        **updates: Any,
    ) -> None:

        with self._lock:

            job = self._jobs.get(job_id)

            if job is None:

                return

            result = job.results[index]

            for key, value in updates.items():

                setattr(result, key, value)
