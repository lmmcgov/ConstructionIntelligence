"""
Extractor for World Bank procurement notice detail pages.

The detail page itself (projects.worldbank.org/.../procurement-detail/{id})
is a client-rendered SPA shell -- verified directly, same category
of problem as Google News redirect links, confirmed identical
response with and without full browser headers, meaning it's not a
bot-detection issue, the content genuinely isn't server-rendered.

Unlike Google News, there's no need for a browser here: the
Procurement Notices API returns the full notice text for a given
id, so this just re-queries the API instead of fetching the page.
Lighter than HTML extraction, not heavier -- one JSON GET.

Returns an empty RawWebDocument for any URL that doesn't match a
World Bank notice-detail URL, so this is safe to chain into
FallbackExtractor alongside other extractors -- non-matching URLs
just fall through to whatever comes next.
"""

from __future__ import annotations

import re

import httpx
from bs4 import BeautifulSoup

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.raw_web_document import (
    RawWebDocument,
)


DEFAULT_TIMEOUT_SECONDS = 15

NOTICE_ID_PATTERN = re.compile(
    r"procurement-detail/([A-Za-z0-9]+)"
)

EMPTY_DOCUMENT_CONTENT = ""


class WorldBankNoticeExtractor(WebExtractor):
    """
    Reads World Bank procurement notice content directly from
    the Procurement Notices API instead of the (JS-only) detail
    page.
    """

    def extract(
        self,
        url: str,
    ) -> RawWebDocument:

        notice_id = self._extract_notice_id(url)

        if not notice_id:

            return self._empty_document(url)

        try:

            notice = self._fetch_notice(notice_id)

        except Exception as error:

            print(
                f"World Bank notice extraction failed: "
                f"{url} ({error})"
            )

            return self._empty_document(url)

        if notice is None:

            return self._empty_document(url)

        title = (
            f"{notice.get('project_name', '')}: "
            f"{notice.get('notice_type', '')}"
        )

        content = self._strip_html(
            notice.get("notice_text", "")
        ) or notice.get("bid_description", "") or ""

        return RawWebDocument(
            url=url,
            title=title,
            content=content,
            source_name="World Bank",
        )


    def _extract_notice_id(
        self,
        url: str,
    ) -> str | None:

        match = NOTICE_ID_PATTERN.search(url)

        return match.group(1) if match else None


    def _fetch_notice(
        self,
        notice_id: str,
    ) -> dict | None:

        response = httpx.get(
            "https://search.worldbank.org/api/v2/procnotices",
            params={
                "format": "json",
                "id": notice_id,
            },
            timeout=DEFAULT_TIMEOUT_SECONDS,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        response.raise_for_status()

        data = response.json()

        notices = data.get(
            "procnotices",
            [],
        )

        return notices[0] if notices else None


    def _strip_html(
        self,
        html: str,
    ) -> str:

        if not html:

            return ""

        return BeautifulSoup(
            html,
            "html.parser",
        ).get_text(
            separator=" ",
            strip=True,
        )


    def _empty_document(
        self,
        url: str,
    ) -> RawWebDocument:

        return RawWebDocument(
            url=url,
            title="",
            content=EMPTY_DOCUMENT_CONTENT,
        )
