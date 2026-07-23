"""
Evidence discovery service.

Generates localized search queries and discovers
potential evidence URLs for construction projects.

Uses:

- Country-specific SearchContext
- SearchQueryGenerator
- Tiered search execution
- Search provider integration
- Candidate pool expansion before ranking
"""

from __future__ import annotations


from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.search_context_provider import (
    SearchContextProvider,
)

from construction_intelligence.ingestion.web.search_query_generator import (
    SearchQueryGenerator,
)


class EvidenceDiscoveryService:
    """
    Discovers evidence URLs for projects.

    Uses country-specific search intelligence
    and executes searches by evidence priority tier.

    Discovery intentionally collects a broad candidate
    pool before ranking and filtering.
    """


    def __init__(
        self,
        search_provider,
        context_provider: SearchContextProvider | None = None,
        query_generator: SearchQueryGenerator | None = None,
        minimum_candidates: int = 50,
        maximum_candidates: int = 100,
    ) -> None:

        self.search_provider = (
            search_provider
        )


        self.context_provider = (
            context_provider
            if context_provider is not None
            else SearchContextProvider()
        )


        self.query_generator = (
            query_generator
            if query_generator is not None
            else SearchQueryGenerator()
        )


        self.minimum_candidates = (
            minimum_candidates
        )


        self.maximum_candidates = (
            maximum_candidates
        )


    def discover_urls(
        self,
        project: Project,
    ) -> list[str]:
        """
        Discover URLs related to a project.

        Executes searches by tier.

        Tier 1:
            Official sources
            Procurement

        Tier 2:
            Construction
            Infrastructure

        Tier 3:
            News
            Discovery
        """

        context = (
            self.context_provider.get_context(
                project.country
            )
        )


        queries = (
            self.query_generator.generate(
                project,
                context,
            )
        )


        urls: list[str] = []


        #
        # Group queries by execution tier.
        #
        tiers = (
            self._group_queries_by_tier(
                queries
            )
        )


        #
        # Execute all useful tiers until
        # enough candidates are collected.
        #
        for tier in sorted(
            tiers.keys()
        ):

            for query in tiers[tier]:

                results = (
                    self.search_provider.search(
                        query.query
                    )
                )


                urls.extend(
                    results
                )


                #
                # Stop individual tier execution
                # once enough candidates exist.
                #
                if len(urls) >= self.minimum_candidates:

                    break


            #
            # Do not stop simply because
            # one tier returned results.
            #
            # Previous behavior stopped after
            # weak Tier 1 matches.
            #
            if len(urls) >= self.minimum_candidates:

                break



        #
        # Remove duplicates while preserving order.
        #
        unique_urls = list(
            dict.fromkeys(
                urls
            )
        )


        #
        # Keep discovery bounded.
        #
        return unique_urls[
            : self.maximum_candidates
        ]


    def _group_queries_by_tier(
        self,
        queries,
    ) -> dict[int, list]:
        """
        Group SearchQuery objects by tier.
        """

        grouped: dict[int, list] = {}


        for query in queries:

            grouped.setdefault(
                query.tier,
                [],
            ).append(
                query
            )


        return grouped