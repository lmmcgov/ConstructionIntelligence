"""
Raw web document representation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RawWebDocument:
    """
    Represents unprocessed external web content.
    """

    url: str

    title: str

    content: str

    source_name: str | None = None