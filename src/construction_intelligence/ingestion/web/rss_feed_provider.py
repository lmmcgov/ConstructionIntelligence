"""
RSS/Atom feed implementation of FeedProvider.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone

import diskcache
import feedparser
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


DEFAULT_CACHE_DIR = "data/feed_cache/rss"

DEFAULT_TIMEOUT_SECONDS = 15


class RSSFeedProvider(FeedProvider):
    """
    Polls a set of RSS/Atom feeds and returns
    only entries not previously observed.

    Seen-state persists across runs via a
    disk-backed cache, keyed by feed URL and
    entry id/link, so repeated polls only
    surface genuinely new items.
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
        """
        Poll all configured feeds concurrently
        and return newly observed entries.
        """

        results = parallel_map(
            self._poll_one,
            self.feed_sources,
        )

        candidates: list[DiscoveredCandidate] = []

        for feed_candidates in results:

            candidates.extend(
                feed_candidates
            )

        return candidates


    def _poll_one(
        self,
        source: FeedSource,
    ) -> list[DiscoveredCandidate]:
        """
        Poll a single feed.

        Errors are isolated per-feed so one
        broken or unreachable feed cannot
        block the others.
        """

        try:

            raw = self.fetcher(
                source.url
            )

        except Exception as error:

            print(
                f"RSS fetch failed: {source.url} ({error})"
            )

            return []


        parsed = feedparser.parse(raw)

        new_candidates: list[DiscoveredCandidate] = []


        for entry in parsed.entries:

            url = entry.get("link")

            if not url:

                continue


            entry_id = (
                entry.get("id")
                or url
            )

            cache_key = (
                f"{source.url}::{entry_id}"
            )

            if cache_key in self.cache:

                continue


            self.cache.set(
                cache_key,
                True,
            )

            new_candidates.append(
                DiscoveredCandidate(
                    url=url,
                    title=entry.get("title", ""),
                    snippet=entry.get("summary", ""),
                    published_at=self._parse_published(entry),
                    source_type=source.category,
                    feed_url=source.url,
                )
            )

        return new_candidates


    def _parse_published(
        self,
        entry,
    ) -> datetime | None:

        parsed_time = entry.get(
            "published_parsed"
        )

        if not parsed_time:

            return None


        return datetime(
            *parsed_time[:6],
            tzinfo=timezone.utc,
        )


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
