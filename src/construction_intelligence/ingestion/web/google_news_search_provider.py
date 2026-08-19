"""
Google News RSS implementation of SearchProvider.

Needs no local infrastructure (unlike SearXNGSearchProvider,
which requires a running local instance) -- this is the main
reason to use it alongside SearXNG, not instead of it.

Google News RSS <link> values are opaque redirect tokens
(news.google.com/rss/articles/CBMi...) that only resolve to the
real article URL via a client-side JS redirect -- there is no
server-side 3xx and no embedded URL in the initial page payload
(verified directly; both the old base64-decode trick and a plain
HTTP fetch were tried and failed). Resolving them for real
requires an actual JS-executing browser, hence the Playwright
dependency here -- heavier than the rest of this project's
providers, but there was no lighter-weight way to get a real,
fetchable article URL out of Google News.
"""

from __future__ import annotations

import xml.etree.ElementTree as ElementTree
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import diskcache
import httpx
from playwright.sync_api import sync_playwright

from construction_intelligence.ingestion.web.country_codes import (
    get_country_code,
)
from construction_intelligence.ingestion.web.search_provider import (
    SearchProvider,
)


DEFAULT_CACHE_DIR = "data/feed_cache/google_news_resolved"

DEFAULT_TIMEOUT_SECONDS = 15

#
# Resolving each item costs a real browser navigation --
# capped per query so one query can't stall discovery for
# minutes. Google News RSS typically returns ~10 anyway.
#
MAX_RESULTS_PER_QUERY = 5

NAVIGATION_TIMEOUT_MS = 20000

REDIRECT_WAIT_TIMEOUT_MS = 8000


class GoogleNewsSearchProvider(SearchProvider):
    """
    Searches Google News RSS and resolves each result to its
    real, fetchable article URL via a shared headless browser.

    Playwright's sync API ties a browser to the exact OS thread
    that created it -- calling it from a different thread later
    raises (or worse, silently misbehaves), not just races. Since
    callers here run inside a thread pool (MultiSearchProvider,
    itself called from web_ui/app.py's per-project worker pool),
    a plain lock isn't enough -- it only serializes access, it
    doesn't pin execution to one thread. All browser work is
    dispatched through a dedicated single-worker executor
    instead, so it always runs on the same thread for this
    instance's whole lifetime, no matter which thread calls
    search()/close().
    """

    def __init__(
        self,
        cache_dir: str = DEFAULT_CACHE_DIR,
        fetcher: "object | None" = None,
    ) -> None:

        self.cache = diskcache.Cache(cache_dir)

        self._fetcher = fetcher

        self._executor = ThreadPoolExecutor(
            max_workers=1
        )

        self._playwright = None

        self._browser = None


    def search(
        self,
        query: str,
        country: str | None = None,
    ) -> list[str]:

        feed_url = self._build_feed_url(query, country)

        try:

            raw = self._fetch(feed_url)

        except Exception as error:

            print(
                f"Google News RSS fetch failed: {feed_url} ({error})"
            )

            return []

        try:

            root = ElementTree.fromstring(raw)

        except ElementTree.ParseError as error:

            print(
                f"Google News RSS parse failed: {feed_url} ({error})"
            )

            return []

        redirect_urls = [
            item.findtext("link")
            for item in root.findall(".//item")
        ]

        redirect_urls = [
            url
            for url in redirect_urls
            if url
        ][:MAX_RESULTS_PER_QUERY]

        resolved: list[str] = []

        for redirect_url in redirect_urls:

            real_url = self._resolve(redirect_url)

            if real_url:

                resolved.append(real_url)

        return resolved


    def close(self) -> None:
        """
        Shut down the shared browser. Not required for the
        process to exit cleanly, but avoids leaving a Chromium
        process running during long-lived local dev sessions.
        """

        self._executor.submit(
            self._close_on_worker_thread
        ).result()

        self._executor.shutdown(
            wait=True
        )


    def _close_on_worker_thread(self) -> None:

        if self._browser is not None:

            self._browser.close()

            self._browser = None

        if self._playwright is not None:

            self._playwright.stop()

            self._playwright = None


    def _build_feed_url(
        self,
        query: str,
        country: str | None,
    ) -> str:

        encoded_query = quote(query)

        url = (
            f"https://news.google.com/rss/search?q={encoded_query}"
        )

        code = get_country_code(country)

        if code:

            alpha2, language = code

            url += (
                f"&hl={language}-{alpha2}"
                f"&gl={alpha2}"
                f"&ceid={alpha2}:{language}"
            )

        return url


    def _resolve(
        self,
        redirect_url: str,
    ) -> str | None:
        """
        Resolve a Google News redirect URL to the real article
        URL, using a cache keyed by the redirect URL itself so
        repeated queries surfacing the same article don't pay
        for a second browser navigation.
        """

        if redirect_url in self.cache:

            return self.cache[redirect_url]

        try:

            resolved_url = self._executor.submit(
                self._resolve_on_worker_thread,
                redirect_url,
            ).result()

        except Exception as error:

            print(
                f"Google News redirect resolution failed: "
                f"{redirect_url} ({error})"
            )

            return None

        #
        # None (navigation failed) or still on news.google.com
        # (redirect never fired in time) -- either way, not
        # something our extractor can do anything useful with.
        #
        if not resolved_url or "news.google.com" in resolved_url:

            return None

        self.cache.set(redirect_url, resolved_url)

        return resolved_url


    def _resolve_on_worker_thread(
        self,
        redirect_url: str,
    ) -> str | None:
        """
        Runs only on self._executor's single worker thread --
        never call this directly from any other thread.
        """

        page = self._get_browser().new_page()

        try:

            page.goto(
                redirect_url,
                wait_until="domcontentloaded",
                timeout=NAVIGATION_TIMEOUT_MS,
            )

            try:

                #
                # Waiting specifically for the URL to leave
                # news.google.com is what we actually need --
                # far faster than waiting for the whole page
                # (ads, trackers) to go network-idle, and
                # correct regardless of how "settled" the rest
                # of the page is.
                #
                page.wait_for_url(
                    lambda url: (
                        "news.google.com" not in url
                    ),
                    timeout=REDIRECT_WAIT_TIMEOUT_MS,
                )

            except Exception:

                #
                # Didn't leave news.google.com in time -- the
                # page.url read below still reflects wherever
                # navigation actually landed, and the caller
                # treats a still-on-google URL as a failed
                # resolution.
                #
                pass

            return page.url

        finally:

            page.close()


    def _get_browser(self):
        """
        Runs only on self._executor's single worker thread --
        never call this directly from any other thread.
        """

        if self._browser is not None:

            return self._browser

        self._playwright = sync_playwright().start()

        self._browser = self._playwright.chromium.launch(
            headless=True
        )

        return self._browser


    def _fetch(
        self,
        url: str,
    ) -> bytes:

        if self._fetcher is not None:

            return self._fetcher(url)

        response = httpx.get(
            url,
            timeout=DEFAULT_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        response.raise_for_status()

        return response.content
