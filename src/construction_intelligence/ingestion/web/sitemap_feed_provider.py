"""
XML sitemap implementation of FeedProvider.

Complements RSS for agencies that publish a
sitemap but not a feed. Does not follow
sitemap-index files (a sitemap of sitemaps) —
point feed sources directly at a leaf urlset.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from xml.etree import ElementTree

import diskcache
import httpx

from construction_intelligence.ingestion.web.concurrency import (
    parallel_map,
)

from construction_intelligence.ingestion.web.discovered_candidate import (
    DiscoveredCandidate,
)

from construction_intelligence.ingestion.web.feed_provider import (
    FeedProvider,
)

from construction_intelligence.ingestion.web.feed_source import (
    FeedSource,
)


DEFAULT_CACHE_DIR = "data/feed_cache/sitemap"

DEFAULT_TIMEOUT_SECONDS = 15

SITEMAP_NAMESPACE = (
    "{http://www.sitemaps.org/schemas/sitemap/0.9}"
)


class SitemapFeedProvider(FeedProvider):
    """
    Polls XML sitemaps and returns URLs whose
    <lastmod> has changed since last observed.
    """

    def __init__(
        self,
        feed_sources: list[FeedSource],
        cache_dir: str = DEFAULT_CACHE_DIR,
        fetcher: Callable[[str], bytes] | None = None,
    ) -> None:

        self.feed_sources = feed_sources

        self.cache = diskcache.Cache(cache_dir)

        self.fetcher = (
            fetcher
            if fetcher is not None
            else self._fetch
        )


    def poll(self) -> list[DiscoveredCandidate]:

        results = parallel_map(
            self._poll_one,
            self.feed_sources,
        )

        candidates: list[DiscoveredCandidate] = []

        for sitemap_candidates in results:

            candidates.extend(
                sitemap_candidates
            )

        return candidates


    def _poll_one(
        self,
        source: FeedSource,
    ) -> list[DiscoveredCandidate]:

        try:

            raw = self.fetcher(
                source.url
            )

        except Exception as error:

            print(
                f"Sitemap fetch failed: {source.url} ({error})"
            )

            return []


        try:

            root = ElementTree.fromstring(raw)

        except ElementTree.ParseError as error:

            print(
                f"Sitemap parse failed: {source.url} ({error})"
            )

            return []


        new_candidates: list[DiscoveredCandidate] = []


        for url_element in root.findall(
            f"{SITEMAP_NAMESPACE}url"
        ):

            loc = url_element.findtext(
                f"{SITEMAP_NAMESPACE}loc"
            )

            if not loc:

                continue


            lastmod = url_element.findtext(
                f"{SITEMAP_NAMESPACE}lastmod"
            )

            cache_key = (
                f"{source.url}::{loc}::{lastmod or ''}"
            )

            if cache_key in self.cache:

                continue


            self.cache.set(
                cache_key,
                True,
            )

            new_candidates.append(
                DiscoveredCandidate(
                    url=loc,
                    published_at=self._parse_lastmod(lastmod),
                    source_type=source.category,
                    feed_url=source.url,
                )
            )

        return new_candidates


    def _parse_lastmod(
        self,
        value: str | None,
    ) -> datetime | None:

        if not value:

            return None


        try:

            return datetime.fromisoformat(value)

        except ValueError:

            return None


    def _fetch(
        self,
        url: str,
    ) -> bytes:

        response = httpx.get(
            url,
            timeout=DEFAULT_TIMEOUT_SECONDS,
            follow_redirects=True,
        )

        response.raise_for_status()

        return response.content
