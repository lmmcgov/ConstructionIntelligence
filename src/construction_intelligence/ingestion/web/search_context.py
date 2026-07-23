"""
Search context for localized construction intelligence.

Provides language, regional, and domain-specific
signals used by:

- query generation
- evidence discovery
- evidence ranking
- extraction fallback selection
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SearchContext:
    """
    Localized search intelligence profile.

    Contains vocabulary and ranking signals required
    to discover construction project evidence
    internationally.
    """

    #
    # Geographic identity
    #

    country: str

    language: str

    region: str = "global"


    #
    # Construction vocabulary
    #

    construction_terms: list[str] = field(
        default_factory=list
    )

    infrastructure_terms: list[str] = field(
        default_factory=list
    )

    procurement_terms: list[str] = field(
        default_factory=list
    )


    #
    # Government and official source signals
    #

    government_terms: list[str] = field(
        default_factory=list
    )

    official_source_terms: list[str] = field(
        default_factory=list
    )

    government_domains: list[str] = field(
        default_factory=list
    )

    #
    # Municipal / local authority domains.
    #
    # Important because many construction projects
    # are published by cities rather than national
    # government domains.
    #
    local_authority_domains: list[str] = field(
        default_factory=list
    )


    #
    # Media signals
    #

    news_terms: list[str] = field(
        default_factory=list
    )


    #
    # Search filtering
    #

    negative_terms: list[str] = field(
        default_factory=list
    )


    #
    # Query generation intent
    #

    search_intents: list[str] = field(
        default_factory=lambda: [
            "construction",
            "project",
            "contract",
            "bid",
            "completion",
            "announcement",
        ]
    )


    #
    # Evidence ranking weights
    #

    source_priority: dict[str, int] = field(
        default_factory=lambda: {
            "government": 20,
            "municipal": 20,
            "procurement": 18,
            "news": 10,
            "developer": 5,
            "social_media": -10,
            "real_estate": -15,
        }
    )


    def all_search_terms(self) -> list[str]:
        """
        Return all positive search vocabulary.

        Used when generating localized queries.
        """

        return list(
            dict.fromkeys(
                self.construction_terms
                + self.infrastructure_terms
                + self.procurement_terms
                + self.government_terms
                + self.official_source_terms
            )
        )


    def all_negative_terms(self) -> list[str]:
        """
        Return all filtering terms.
        """

        return list(
            dict.fromkeys(
                self.negative_terms
            )
        )


    def all_official_domains(self) -> list[str]:
        """
        Return recognized official domains.

        Combines national government domains
        and local municipal sources.
        """

        return list(
            dict.fromkeys(
                self.government_domains
                +
                self.local_authority_domains
            )
        )


    def is_government_domain(
        self,
        domain: str,
    ) -> bool:
        """
        Check whether a domain belongs to
        a recognized government or municipal source.
        """

        domain = domain.lower()


        return any(
            government_domain in domain
            for government_domain
            in self.all_official_domains()
        )
        