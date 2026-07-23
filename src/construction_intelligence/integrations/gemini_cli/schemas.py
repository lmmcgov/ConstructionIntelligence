"""
Schemas for Gemini CLI structured responses.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GeminiResourceResponse:
    """
    Resource returned by Gemini as supporting evidence.
    """

    url: str

    title: str | None = None

    source: str | None = None

    resource_type: str | None = None

    excerpt: str | None = None


@dataclass(frozen=True)
class GeminiEvaluationResponse:
    """
    Structured response expected from Gemini CLI.
    """

    match_score: float

    status: str

    reasons: tuple[str, ...]

    resources: tuple[GeminiResourceResponse, ...]