"""
Evidence discovery service.

Generates localized search queries and discovers
potential evidence URLs for construction projects.

Uses:

- Country-specific SearchContext
- SearchQueryGenerator
- Tiered search execution
- Search provider integration
- Feed-based discovery (RSS, sitemaps)
- Candidate pool expansion before ranking
"""

from __future__ import annotations


from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.concurrency import (
    parallel_map,
)

from construction_intelligence.ingestion.web.feed_provider import (
    FeedProvider,
)

from construction_intelligence.ingestion.web.feed_registry import (
    FeedRegistry,
)

from construction_intelligence.ingestion.web.rss_feed_provider import (
    RSSFeedProvider,
)

from construction_intelligence.ingestion.web.search_context_provider import (
    SearchContextProvider,
)

from construction_intelligence.ingestion.web.search_query_generator import (
    SearchQueryGenerator,
)

from construction_intelligence.ingestion.web.sitemap_feed_provider import (
    SitemapFeedProvider,
)


class EvidenceDiscoveryService:
    """
    Discovers evidence URLs for projects.

    Uses country-specific search intelligence
    and executes searches by evidence priority tier.

    Also polls any feed sources (RSS, sitemaps)
    registered for the project's country. Feed-based
    discovery runs alongside tiered search rather than
    replacing it, and counts toward minimum_candidates
    so tiered search does less work when feeds already
    surface enough candidates.

    Discovery intentionally collects a broad candidate
    pool before ranking and filtering.
    """


    def __init__(
        self,
        search_provider,
        context_provider: SearchContextProvider | None = None,
        query_generator: SearchQueryGenerator | None = None,
        feed_registry: FeedRegistry | None = None,
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


        #
        # None disables feed-based discovery
        # entirely (default, fully backward
        # compatible). Pass a populated
        # FeedRegistry to enable it.
        #
        self.feed_registry = (
            feed_registry
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

        Feed-based discovery (RSS, sitemaps) runs
        first and seeds the candidate pool; tiered
        search then tops it up to minimum_candidates.
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


        #
        # Feed-based discovery seeds the pool.
        # It is the highest-signal source when
        # feeds are registered for this country.
        #
        urls: list[str] = (
            self._discover_feed_urls(
                project
            )
        )


        #
        # Group queries by execution tier.
        #
        tiers = (
            self._group_queries_by_tier(
                queries
            )
        )


        #
        # Execute tiered search only if feeds
        # have not already met the candidate
        # floor. Run all useful tiers until
        # enough candidates are collected.
        #
        if len(urls) < self.minimum_candidates:

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


    def _discover_feed_urls(
        self,
        project: Project,
    ) -> list[str]:
        """
        Poll feed sources registered for this
        project's country.

        Returns an empty list when no feed
        registry is configured, or when no
        feeds are registered for the country.

        RSS and sitemap providers are polled
        concurrently, since each covers a
        distinct set of sources.
        """

        if self.feed_registry is None:

            return []


        feed_sources = (
            self.feed_registry.get_feeds(
                project.country
            )
        )

        if not feed_sources:

            return []


        rss_sources = [
            source
            for source in feed_sources
            if source.kind == "rss"
        ]

        sitemap_sources = [
            source
            for source in feed_sources
            if source.kind == "sitemap"
        ]


        providers: list[FeedProvider] = []

        if rss_sources:

            providers.append(
                RSSFeedProvider(rss_sources)
            )

        if sitemap_sources:

            providers.append(
                SitemapFeedProvider(sitemap_sources)
            )

        if not providers:

            return []


        results = parallel_map(
            lambda provider: provider.poll(),
            providers,
        )

        urls: list[str] = []

        for provider_candidates in results:

            urls.extend(
                candidate.url
                for candidate in provider_candidates
            )

        return urls