"""
World Bank Procurement Notices API implementation of FeedProvider.

Covers World Bank-financed projects across nearly every developing
country -- valuable specifically for countries with no working
government/procurement RSS or sitemap of their own (verified: Peru,
Honduras, Nicaragua, Panama, Pakistan, Indonesia, and the Philippines
all have substantial construction-works notice volume here, all
countries that came back empty or weak on government-side feeds).

Not RSS or a sitemap -- a JSON REST API
(search.worldbank.org/api/v2/procnotices), verified live with
project_ctry_name (exact country name, e.g. "Nigeria") and
procurement_group=CW (Construction Works) as real, working filter
params. Several plausible-looking param names were tried and
silently ignored rather than erroring (countryname, countrycode,
countryshortname) -- worth remembering if extending this, since a
silently-ignored filter returns the unfiltered global total, which
reads as "it worked" if you don't check the count.

Results default-sort newest-first without an explicit `order` param
-- the documented order syntax returned a 400 (the backend, revealed
by the error message, is Azure Cognitive Search under the API
gateway, not a fully open documented interface), so this doesn't
try to force a different order.

The notice detail page (projects.worldbank.org/.../procurement-detail/{id})
is a client-rendered SPA shell with no server-side content, same
category of problem as Google News -- but unlike Google News, the
API response already contains the full notice text, so
WorldBankNoticeExtractor (extractor.py) reads it directly by
re-querying id= rather than needing a browser at all.
"""

from __future__ import annotations

from datetime import datetime, timezone

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


DEFAULT_CACHE_DIR = "data/feed_cache/worldbank"

DEFAULT_TIMEOUT_SECONDS = 15

#
# Bounded per poll for the same reason as everywhere else in
# this codebase -- a handful of countries have 1000+ total
# notices, we only want what's new since last poll, not a full
# history dump every time.
#
MAX_NOTICES_PER_POLL = 20

NOTICE_DETAIL_URL_TEMPLATE = (
    "https://projects.worldbank.org/en/projects-operations/"
    "procurement-detail/{notice_id}"
)


class WorldBankProcurementProvider(FeedProvider):
    """
    Polls the World Bank Procurement Notices API for new
    construction-related notices per country.
    """

    def __init__(
        self,
        feed_sources: list[FeedSource],
        cache_dir: str = DEFAULT_CACHE_DIR,
        fetcher: "object | None" = None,
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

        for source_candidates in results:

            candidates.extend(
                source_candidates
            )

        return candidates


    def _poll_one(
        self,
        source: FeedSource,
    ) -> list[DiscoveredCandidate]:

        try:

            notices = self.fetcher(
                source.url
            )

        except Exception as error:

            print(
                f"World Bank procurement fetch failed: "
                f"{source.url} ({error})"
            )

            return []

        new_candidates: list[DiscoveredCandidate] = []

        for notice in notices:

            notice_id = notice.get("id")

            if not notice_id:

                continue

            cache_key = f"{source.url}::{notice_id}"

            if cache_key in self.cache:

                continue

            self.cache.set(
                cache_key,
                True,
            )

            new_candidates.append(
                DiscoveredCandidate(
                    url=NOTICE_DETAIL_URL_TEMPLATE.format(
                        notice_id=notice_id
                    ),
                    title=(
                        f"{notice.get('project_name', '')}: "
                        f"{notice.get('notice_type', '')}"
                    ),
                    snippet=notice.get(
                        "bid_description",
                        "",
                    )
                    or "",
                    published_at=self._parse_notice_date(
                        notice.get("noticedate")
                    ),
                    source_type=source.category,
                    feed_url=source.url,
                )
            )

        return new_candidates


    def _parse_notice_date(
        self,
        value: str | None,
    ) -> datetime | None:

        if not value:

            return None

        try:

            #
            # World Bank's own date format, e.g. "17-Aug-2026".
            #
            return datetime.strptime(
                value,
                "%d-%b-%Y",
            ).replace(
                tzinfo=timezone.utc
            )

        except ValueError:

            return None


    def _fetch(
        self,
        url: str,
    ) -> list[dict]:

        response = httpx.get(
            url,
            params={
                "format": "json",
                "rows": MAX_NOTICES_PER_POLL,
            },
            timeout=DEFAULT_TIMEOUT_SECONDS,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "procnotices",
            [],
        )
