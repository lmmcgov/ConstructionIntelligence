"""
Default feed registry population.

Verified RSS/Atom feeds and sitemaps for construction/
infrastructure evidence discovery, researched and live-
verified per country against the countries of concern list
(South America, Central America & Caribbean, Southeast/South
Asia, Europe & Central Asia, Africa).

Coverage as of 2026-08-17:

- All 32 requested countries have at least one verified, live
  feed or sitemap. 19 were found in the first research pass; the
  remaining 13 (Chile, Peru, Honduras, Nicaragua, Panama,
  Indonesia, Pakistan, Philippines, Cambodia, Albania, Serbia,
  Nigeria, Morocco) required a second, more targeted pass after
  their first-attempt candidates failed on bot-blocking, wrong
  domains, or stale/abandoned content -- see the inline comment
  on each entry for specifics.
- About a third of entries are "news" category fallbacks (a
  national news outlet or wire service) rather than a government/
  procurement source, used only where every government-domain
  candidate was unreachable or feedless after real attempts.
  These carry a lower source_priority weight than government/
  procurement feeds by design (see search_context.py), and one
  (Nicaragua's) carries an explicit editorial-bias caveat --
  worth weighing that when interpreting results from those
  countries specifically.
- Several "government"-category entries are general national
  government feeds/sitemaps rather than infrastructure-specific
  ministry ones, used where the relevant ministry had no working
  feed. Discovery casts a broad net by design; ranking and scoring
  filter for relevance downstream.

Feeds here were not filtered for construction relevance beyond
what their category implies -- discovery intentionally casts a
broad net; EvidenceRanker and the scoring services filter
downstream, per this project's high-recall-then-high-precision
design (see README.md).

Countries are registered under their canonical English name.
FeedRegistry.get_feeds() resolves a Project.country value against
these keys via normalize_country_name (lowercase, accent-stripped)
and then, on a miss, COUNTRY_ALIASES (shared with
SearchContextProvider) -- e.g. "Bosnia" or "FYROM" both resolve
to the "bosnia and herzegovina" / "north macedonia" entries below.
A country with no exact or alias match still resolves to an empty
list rather than a default -- there is no safe global fallback for
feed URLs the way there is for search vocabulary.
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

    registry.register(
        "chile",
        [
            FeedSource(
                url="https://www.mop.gob.cl/feed/",
                category="government",
                kind="rss",
            ),
            #
            # Ministerio de Obras Publicas. Correct domain is
            # mop.gob.cl, not mop.cl (which just redirects here) --
            # the redirect was the reason an earlier pass missed it.
            # Directly construction-relevant: verified top item was
            # a road-concession bid announcement.
            #
        ],
    )

    registry.register(
        "peru",
        [
            FeedSource(
                url="https://andina.pe/agencia/rss.aspx",
                category="news",
                kind="rss",
            ),
            #
            # News fallback -- Agencia Peruana de Noticias Andina,
            # Peru's state-owned news wire (state-owned but not a
            # ministry press office, hence "news" not "government").
            # gob.pe (incl. OSCE/MTC) remains bot-blocked (HTTP 418)
            # on every path tried.
            #
        ],
    )


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

    registry.register(
        "honduras",
        [
            FeedSource(
                url="https://oncae.gob.hn/feed/",
                category="procurement",
                kind="rss",
            ),
            #
            # ONCAE (Oficina Normativa de Contratacion y
            # Adquisiciones del Estado) -- Honduras' national
            # procurement office. Verified top item was a
            # procurement circular. Use the no-www canonical form;
            # www.oncae.gob.hn redirects here.
            #
        ],
    )

    registry.register(
        "nicaragua",
        [
            FeedSource(
                url="https://www.confidencial.digital/feed/",
                category="news",
                kind="rss",
            ),
            #
            # CAVEAT: independent Nicaraguan outlet operating in
            # exile, editorially opposition-aligned -- not a
            # neutral source, but the only Nicaraguan source that
            # resolved at all. Every government domain tried
            # (mti.gob.ni times out at TCP; presidencia.gob.ni has
            # broken DNS) and most other independent outlets are
            # Cloudflare-blocked -- Nicaragua's web presence is
            # broadly unreachable from this environment, not simply
            # feedless.
            #
        ],
    )

    registry.register(
        "panama",
        [
            FeedSource(
                url="https://www.mef.gob.pa/feed/",
                category="government",
                kind="rss",
            ),
            #
            # Ministerio de Economia y Finanzas -- oversees
            # PanamaCompra procurement; verified content includes
            # housing-policy items. mop.gob.pa (the actual Ministry
            # of Public Works) remains connection-refused on every
            # protocol/subdomain combination tried.
            #
        ],
    )


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

    registry.register(
        "albania",
        [
            FeedSource(
                url="https://www.arrsh.gov.al/feed",
                category="government",
                kind="rss",
            ),
            #
            # Autoriteti Rrugor Shqiptar (Albanian Road Authority)
            # -- directly construction-relevant, e.g. a verified
            # item on Tirane-Durres highway widening work.
            # infrastruktura.gov.al (the ministry itself) remains
            # confirmed stale (newest sitemap lastmod 2020-12-10).
            #
        ],
    )

    registry.register(
        "serbia",
        [
            FeedSource(
                url="https://www.mgsi.gov.rs/lat/rss.xml",
                category="government",
                kind="rss",
            ),
            #
            # Ministry of Construction, Transport and
            # Infrastructure. Earlier 404s were on /feed and
            # /sitemap.xml at domain root -- this ministry runs
            # Drupal, not WordPress, so the feed lives at this
            # non-standard path instead. A Cyrillic-script variant
            # exists at the same path without /lat/.
            #
        ],
    )


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

    registry.register(
        "nigeria",
        [
            FeedSource(
                url="https://ferma.gov.ng/feed/",
                category="government",
                kind="rss",
            ),
            #
            # Federal Roads Maintenance Agency -- directly
            # construction/procurement relevant, e.g. verified
            # items on a road maintenance programme and a tender
            # invitation. fmw.gov.ng (the ministry itself) also has
            # a sitemap but its lastmod dates max out at 2024-02 --
            # excluded as abandoned.
            #
        ],
    )

    registry.register(
        "morocco",
        [
            FeedSource(
                url="https://www.maroc.ma/fr/rss.xml",
                category="government",
                kind="rss",
            ),
            #
            # Official government portal -- general national news,
            # not infrastructure-specific, but a real official
            # source (same tier as Moldova/Montenegro's general
            # government feeds above). equipement.gov.ma and
            # transport.gov.ma remain persistently unreachable
            # across three separate fetch attempts.
            #
        ],
    )

    registry.register(
        "philippines",
        [
            FeedSource(
                url="https://www.philstar.com/rss/business",
                category="news",
                kind="rss",
            ),
            #
            # News fallback -- DPWH (dpwh.gov.ph) is behind
            # Incapsula bot protection on both /feed and
            # /sitemap.xml; PhilGEPS has no feed or sitemap at any
            # standard path.
            #
        ],
    )

    registry.register(
        "indonesia",
        [
            FeedSource(
                url="https://www.antaranews.com/rss/ekonomi.xml",
                category="news",
                kind="rss",
            ),
            #
            # News fallback -- pu.go.id blocked (403) on every
            # path across two fetch attempts. binamarga.pu.go.id
            # (roads directorate) has a live sitemap but ~500 of
            # 501 entries are lastmod 2023, effectively abandoned.
            # sda.pu.go.id returns HTML, not a real feed/sitemap.
            #
        ],
    )

    registry.register(
        "pakistan",
        [
            FeedSource(
                url="https://www.dawn.com/feeds/business",
                category="news",
                kind="rss",
            ),
            #
            # News fallback -- no government/procurement source
            # found despite checking federal PPRA (500/403) and
            # three provincial procurement authorities (Punjab,
            # KPK, Sindh -- 404/HTML-not-XML/timeout respectively).
            #
        ],
    )

    registry.register(
        "cambodia",
        [
            FeedSource(
                url="https://www.mlmupc.gov.kh/feed",
                category="government",
                kind="rss",
            ),
            #
            # Ministry of Land Management, Urban Planning and
            # Construction -- the correct ministry for this domain;
            # verified titles reference district infrastructure and
            # road planning. mpwt.gov.kh (Public Works and
            # Transport) remains unreachable across every fetch
            # path tried.
            #
        ],
    )
