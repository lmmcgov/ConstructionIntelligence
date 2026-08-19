"""
Composite SearchProvider that fans out to multiple providers.

Lets EvidenceDiscoveryService keep its existing single-provider
constructor (no change needed there) while actually querying
several backends -- e.g. SearXNG (local, needs infrastructure)
alongside Google News (hosted, needs none).
"""

from __future__ import annotations

from construction_intelligence.ingestion.web.concurrency import (
    parallel_map,
)

from construction_intelligence.ingestion.web.search_provider import (
    SearchProvider,
)


class MultiSearchProvider(SearchProvider):
    """
    Queries all configured providers concurrently and merges
    their results, deduplicated, order preserved by provider
    order then result order.

    One provider failing (e.g. SearXNG unreachable) doesn't lose
    results from the others -- matches the per-item failure
    isolation used elsewhere in this codebase (feed polling,
    tiered search, extraction).
    """

    def __init__(
        self,
        providers: list[SearchProvider],
    ) -> None:

        self.providers = providers


    def search(
        self,
        query: str,
        country: str | None = None,
    ) -> list[str]:

        results = parallel_map(
            lambda provider: self._search_one(
                provider,
                query,
                country,
            ),
            self.providers,
        )

        urls: list[str] = []

        for provider_urls in results:

            urls.extend(provider_urls)

        return list(
            dict.fromkeys(urls)
        )


    def _search_one(
        self,
        provider: SearchProvider,
        query: str,
        country: str | None,
    ) -> list[str]:

        try:

            return provider.search(
                query,
                country=country,
            )

        except Exception as error:

            print(
                f"Search provider failed: "
                f"{provider.__class__.__name__} ({error})"
            )

            return []
