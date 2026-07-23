from dataclasses import dataclass, field
from datetime import UTC, datetime

from construction_intelligence.core.enums import (
    ProjectCategory,
    ProjectOrigin,
    ProjectStatus,
)

from construction_intelligence.core.ids import (
    EvidenceId,
    ProjectId,
    new_id,
)


@dataclass(slots=True)
class Project:
    """
    Represents a real-world construction project.
    """

    id: ProjectId = field(
        default_factory=new_id
    )


    #
    # Identity
    #
    name: str = ""

    description: str | None = None

    #
    # Alternate project names.
    #
    # Construction projects frequently appear
    # under different names across:
    #
    # - government announcements
    # - procurement documents
    # - news articles
    # - GIS datasets
    #
    aliases: list[str] = field(
        default_factory=list
    )


    #
    # Classification
    #
    status: ProjectStatus = (
        ProjectStatus.UNDER_CONSTRUCTION
    )

    category: ProjectCategory = (
        ProjectCategory.ROAD
    )


    #
    # Source
    #
    origin: ProjectOrigin = (
        ProjectOrigin.OSM
    )

    origin_id: str | None = None


    #
    # Road Information
    #
    road_name: str | None = None

    road_ref: str | None = None


    #
    # Geographic Information
    #
    country: str | None = None

    state: str | None = None

    city: str | None = None


    latitude: float | None = None

    longitude: float | None = None


    #
    # Audit Information
    #
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_seen: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


    #
    # Relationships
    #
    evidence_ids: list[EvidenceId] = field(
        default_factory=list
    )


    def add_evidence(
        self,
        evidence_id: EvidenceId,
    ) -> None:
        """
        Associate an evidence record with this project.
        """

        if evidence_id not in self.evidence_ids:
            self.evidence_ids.append(
                evidence_id
            )


    def add_alias(
        self,
        alias: str,
    ) -> None:
        """
        Add an alternate project name.

        Prevents duplicate aliases.
        """

        if alias not in self.aliases:
            self.aliases.append(
                alias
            )


    def touch(self) -> None:
        """
        Update timestamps when the project changes.
        """

        now = datetime.now(UTC)

        self.updated_at = now

        self.last_seen = now