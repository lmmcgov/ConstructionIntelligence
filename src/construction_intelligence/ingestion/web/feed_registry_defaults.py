"""
Default feed registry population.

Verified RSS/Atom feeds and sitemaps for construction/
infrastructure evidence discovery, researched and live-
verified per country against the countries of concern list
(South America, Central America & Caribbean, Southeast/South
Asia, Europe & Central Asia, Africa).

Coverage as of 2026-08-17:

- 19 of 32 requested countries yielded at least one verified,
  live feed or sitemap.
- 13 yielded zero despite real research attempts. Most of those
  failures were network/bot-blocking errors (403/404/500/
  connection refused/TLS errors) against government domains,
  not confirmed absence of a feed -- worth a periodic recheck
  rather than treated as permanently settled. See the comment
  block at the end of each region function for what was tried.

Feeds here were not filtered for construction relevance beyond
what their category implies -- discovery intentionally casts a
broad net; EvidenceRanker and the scoring services filter
downstream, per this project's high-recall-then-high-precision
design (see README.md).

Country keys match plain English names as resolved by
normalize_country_name (lowercase, accent-stripped) -- they do
not go through SearchContextProvider's COUNTRY_ALIASES, so a
Project.country value must match one of these keys (or a
close ASCII-folded variant) to resolve any feeds.
"""

from __future__ import annotations

from construction_intelligence.ingestion.web.feed_registry import (
    FeedRegistry,
)

from construction_intelligence.ingestion.web.feed_source import (
    FeedSource,
)


def build_default_feed_registry() -> FeedRegistry:
    """
    Build a FeedRegistry populated with every feed
    verified live during the 2026-08 research pass.
    """

    registry = FeedRegistry()

    _register_south_america(registry)
    _register_central_america_and_caribbean(registry)
    _register_europe_and_central_asia(registry)
    _register_asia_and_africa(registry)

    return registry


def _register_south_america(registry: FeedRegistry) -> None:

    registry.register(
        "colombia",
        [
            FeedSource(
                url="https://rss.colombiacompra.gov.co/RSSFiles/rssFeed-72000000.xml",
                category="procurement",
                kind="rss",
            ),
            #
            # Colombia Compra Eficiente (SECOP), UNSPSC segment
            # 72000000 = "Building and Construction Services" --
            # scoped specifically to construction tenders.
            #
        ],
    )

    registry.register(
        "ecuador",
        [
            FeedSource(
                url="https://www.mit.gob.ec/feed/",
                category="government",
                kind="rss",
            ),
            #
            # Ministerio de Infraestructura y Transporte.
            #
        ],
    )

    registry.register(
        "venezuela",
        [
            FeedSource(
                url="https://vsops.gob.ve/category/noticias/feed/",
                category="government",
                kind="rss",
            ),
            #
            # Real feed, but updates infrequently (~2 months
            # stale at verification) -- worth periodic re-check.
            #
        ],
    )

    registry.register(
        "brazil",
        [
            FeedSource(
                url="https://www.gov.br/cidades/pt-br/sitemap.xml",
                category="government",
                kind="sitemap",
            ),
            #
            # Cities/housing/urban mobility. No working RSS found
            # for PNCP/ComprasNet (federal procurement data is
            # API/JSON-only, not RSS) or DNIT (auth-gated).
            #
        ],
    )

    registry.register(
        "bolivia",
        [
            FeedSource(
                url="https://www.gob.bo/sitemap.xml",
                category="government",
                kind="sitemap",
            ),
            #
            # CAVEAT: all 1200+ entries shared one <lastmod> at
            # verification, suggesting wholesale regeneration
            # rather than incremental updates -- lastmod-based
            # dedup may surface less signal here than on a
            # normally-maintained sitemap.
            #
        ],
    )

    #
    # Chile, Peru: researched, 0 verified feeds.
    #
    # Chile -- mercadopublico.cl RSS exists but is abandoned
    # (most recent item dated 2017); mop.cl/feed/ has an expired
    # TLS certificate.
    #
    # Peru -- gob.pe (incl. OSCE/MTC pages) returns HTTP 418 to
    # automated fetches (bot-blocked, not confirmed feedless);
    # mtc.gob.pe/feed/ unresponsive.
    #


def _register_central_america_and_caribbean(registry: FeedRegistry) -> None:

    registry.register(
        "belize",
        [
            FeedSource(
                url="https://www.pressoffice.gov.bz/feed/",
                category="government",
                kind="rss",
            ),
            #
            # Government of Belize Press Office, all ministries.
            # midh.gov.bz (Infrastructure Dev. & Housing) has RSS
            # but has been abandoned since 2021/2022 -- excluded.
            #
        ],
    )

    registry.register(
        "el salvador",
        [
            FeedSource(
                url="https://www.presidencia.gob.sv/feed/",
                category="government",
                kind="rss",
            ),
        ],
    )

    registry.register(
        "guatemala",
        [
            FeedSource(
                url="https://www.prensalibre.com/feed/",
                category="news",
                kind="rss",
            ),
            #
            # News fallback -- civ.gob.gt and guatemala.gob.gt
            # both returned 403; guatecompras.gt has no
            # discoverable RSS.
            #
        ],
    )

    registry.register(
        "cuba",
        [
            FeedSource(
                url="http://www.granma.cu/feed",
                category="news",
                kind="rss",
            ),
            #
            # Official Communist Party newspaper -- about as
            # close to an official source as Cuba's web presence
            # gets, and the only one with a working feed.
            #
        ],
    )

    registry.register(
        "costa rica",
        [
            FeedSource(
                url="https://www.mopt.go.cr/sitemap.xml",
                category="government",
                kind="sitemap",
            ),
            #
            # Ministerio de Obras Publicas y Transportes, 1283
            # URLs, lastmod present on essentially all entries.
            # Confirmed directly construction-relevant content at
            # verification (e.g. bridge asphalt work notices).
            #
        ],
    )

    #
    # Honduras, Nicaragua, Panama: researched, 0 verified feeds.
    # Ministry/procurement domains failed at the network level
    # (404/ECONNREFUSED/ECONNRESET) far more often than they
    # simply lacked a feed -- worth a re-check from an unblocked
    # network path before concluding these have no viable source.
    #


def _register_europe_and_central_asia(registry: FeedRegistry) -> None:

    registry.register(
        "bosnia and herzegovina",
        [
            FeedSource(
                url="https://www.javnenabavke.gov.ba/sitemap.xml",
                category="procurement",
                kind="sitemap",
            ),
            #
            # State-level public procurement portal, 686 URLs,
            # live lastmod dates.
            #
        ],
    )

    registry.register(
        "bulgaria",
        [
            FeedSource(
                url="https://www.mrrb.bg/bg/rss/",
                category="government",
                kind="rss",
            ),
            #
            # Ministry of Regional Development and Public Works.
            #
        ],
    )

    registry.register(
        "moldova",
        [
            FeedSource(
                url="https://gov.md/ro/rss.xml",
                category="government",
                kind="rss",
            ),
            #
            # General government press releases across all
            # ministries, not infrastructure-specific.
            #
        ],
    )

    registry.register(
        "montenegro",
        [
            FeedSource(
                url="https://rss.gov.me",
                category="government",
                kind="rss",
            ),
            #
            # General government activity feed, all ministries.
            #
        ],
    )

    registry.register(
        "north macedonia",
        [
            FeedSource(
                url="https://vlada.mk/sitemap.xml",
                category="government",
                kind="sitemap",
            ),
            #
            # Government portal, ~2991 URLs, lastmod timestamps
            # current to the hour at verification -- actively
            # maintained. Found via direct curl after the
            # sandboxed research pass returned inconclusive
            # (404 on /rss, /rss.xml).
            #
        ],
    )

    registry.register(
        "romania",
        [
            FeedSource(
                url="https://www.economica.net/feed",
                category="news",
                kind="rss",
            ),
            #
            # News fallback -- e-licitatie.ro (SEAP), CNAIR, and
            # mt.ro (Ministry of Transport) all unreachable or
            # feedless; TED's Romania RSS requires an
            # authenticated saved search, no public anonymous
            # feed URL exists.
            #
        ],
    )

    registry.register(
        "kazakhstan",
        [
            FeedSource(
                url="https://www.gov.kz/sitemap.xml",
                category="government",
                kind="sitemap",
            ),
            #
            # CAVEAT: valid sitemap, 6817 URLs, but zero <lastmod>
            # tags on any entry. SitemapFeedProvider still dedupes
            # correctly (new <loc> entries surface once), but
            # cannot detect content updates on existing pages --
            # weaker freshness signal than a normally-maintained
            # sitemap. goszakup.gov.kz (state procurement) has no
            # RSS, API-only.
            #
        ],
    )

    #
    # Albania, Cambodia, Serbia, North Macedonia's RSS path (kept
    # only via sitemap above): researched, 0 additional verified
    # feeds beyond what's listed. Albania's infrastruktura.gov.al
    # sitemap is confirmed stale (newest lastmod 2020-12-10) --
    # excluded as abandoned. Cambodia's mpwt.gov.kh is unreachable
    # (connection refused/timeout) from both the research
    # environment and a direct curl re-check. Serbia's mgsi.gov.rs
    # (Ministry of Construction, Transport and Infrastructure)
    # returns 404 on standard feed/sitemap paths from both fetch
    # paths tried.
    #


def _register_asia_and_africa(registry: FeedRegistry) -> None:

    registry.register(
        "south africa",
        [
            FeedSource(
                url="https://www.gov.za/rss.xml",
                category="government",
                kind="rss",
            ),
            #
            # General national government notices/legislation,
            # not tender-specific -- National Treasury eTenders
            # and SANRAL have no discoverable feed.
            #
        ],
    )

    registry.register(
        "ghana",
        [
            FeedSource(
                url="https://ppa.gov.gh/feed/",
                category="procurement",
                kind="rss",
            ),
            #
            # Ghana Public Procurement Authority -- covers
            # procurement training, regulatory updates, GHANEPS
            # announcements.
            #
        ],
    )

    #
    # Nigeria, Morocco, Philippines, Indonesia, Pakistan:
    # researched, 0 verified feeds. Several came back 403/500/
    # connection-refused/timeout (pu.go.id, ppra.gov.pk, Morocco's
    # equipement.gov.ma and transport.gov.ma) from both the
    # sandboxed research pass and a direct curl re-check --
    # persistent enough across two fetch paths to treat as a real
    # access barrier, not just inconclusive. PhilGEPS (Philippines)
    # has no discoverable feed or sitemap at all -- third-party
    # scraping is the only current access path, which this design
    # deliberately excludes rather than substitute.
    #
