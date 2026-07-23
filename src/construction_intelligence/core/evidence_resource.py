"""
Evidence resources supporting an evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class EvidenceResource:
    """
    External resource used to support an evidence evaluation.

    Examples:
    - government webpage
    - permit PDF
    - procurement notice
    - news article
    """

    url: str

    title: str | None = None

    source_name: str | None = None

    resource_type: str | None = None

    excerpt: str | None = None

    id: str = field(
        default_factory=lambda: str(uuid4())
    )