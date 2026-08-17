"""
Smoke test for feed-based discovery.

Uses injected fetchers returning canned RSS/sitemap
XML instead of live network calls, so this exercises
real parsing and dedup behavior without depending on
any specific feed staying online.
"""

import tempfile

from construction_intelligence.ingestion.web.feed_source import (
    FeedSource,
)

from construction_intelligence.ingestion.web.rss_feed_provider import (
    RSSFeedProvider,
)

from construction_intelligence.ingestion.web.sitemap_feed_provider import (
    SitemapFeedProvider,
)


RSS_FEED = b"""<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Example DOT Newsroom</title>
    <item>
      <title>Horizon Drive roundabout breaks ground</title>
      <link>https://example-dot.gov/news/horizon-drive-roundabout</link>
      <guid>horizon-drive-roundabout</guid>
      <pubDate>Mon, 10 Aug 2026 12:00:00 GMT</pubDate>
      <description>Construction begins on the Horizon Drive roundabout.</description>
    </item>
    <item>
      <title>Unrelated bridge inspection notice</title>
      <link>https://example-dot.gov/news/bridge-inspection</link>
      <guid>bridge-inspection</guid>
      <pubDate>Sun, 09 Aug 2026 09:00:00 GMT</pubDate>
      <description>Routine inspection schedule.</description>
    </item>
  </channel>
</rss>
"""


SITEMAP = b"""<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example-city.gov/projects/horizon-drive</loc>
    <lastmod>2026-08-10</lastmod>
  </url>
  <url>
    <loc>https://example-city.gov/projects/main-street</loc>
    <lastmod>2026-08-01</lastmod>
  </url>
</urlset>
"""


SITEMAP_UPDATED = b"""<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example-city.gov/projects/horizon-drive</loc>
    <lastmod>2026-08-17</lastmod>
  </url>
  <url>
    <loc>https://example-city.gov/projects/main-street</loc>
    <lastmod>2026-08-01</lastmod>
  </url>
</urlset>
"""


print()
print("RSS FEED PROVIDER")
print("------------------")

rss_cache_dir = tempfile.mkdtemp()

rss_provider = RSSFeedProvider(
    feed_sources=[
        FeedSource(
            url="https://example-dot.gov/rss.xml",
            category="government",
            kind="rss",
        ),
    ],
    cache_dir=rss_cache_dir,
    fetcher=lambda url: RSS_FEED,
)

first_poll = rss_provider.poll()

for candidate in first_poll:
    print(candidate.title, "->", candidate.url)

assert len(first_poll) == 2, "expected 2 new entries on first poll"

second_poll = rss_provider.poll()

assert len(second_poll) == 0, "expected 0 new entries on repeat poll (dedup)"

print("Dedup on repeat poll: OK")


print()
print("SITEMAP FEED PROVIDER")
print("----------------------")

sitemap_cache_dir = tempfile.mkdtemp()

sitemap_fetch_state = {"raw": SITEMAP}

sitemap_provider = SitemapFeedProvider(
    feed_sources=[
        FeedSource(
            url="https://example-city.gov/sitemap.xml",
            category="municipal",
            kind="sitemap",
        ),
    ],
    cache_dir=sitemap_cache_dir,
    fetcher=lambda url: sitemap_fetch_state["raw"],
)

first_sitemap_poll = sitemap_provider.poll()

for candidate in first_sitemap_poll:
    print(candidate.url, "->", candidate.published_at)

assert len(first_sitemap_poll) == 2, "expected 2 new URLs on first poll"

second_sitemap_poll = sitemap_provider.poll()

assert len(second_sitemap_poll) == 0, "expected 0 new URLs on repeat poll (dedup)"

print("Dedup on repeat poll: OK")

#
# Simulate the sitemap reporting a new lastmod
# for an existing URL — should resurface.
#
sitemap_fetch_state["raw"] = SITEMAP_UPDATED

third_sitemap_poll = sitemap_provider.poll()

assert len(third_sitemap_poll) == 1, "expected 1 resurfaced URL after lastmod change"
assert third_sitemap_poll[0].url == "https://example-city.gov/projects/horizon-drive"

print("Resurface on lastmod change: OK")

print()
print("All feed provider checks passed.")
