"""
Test SearXNG search provider.
"""

from construction_intelligence.ingestion.web.searxng_search_provider import (
    SearXNGSearchProvider,
)


def main() -> None:
    """
    Verify SearXNG returns URLs.
    """

    provider = SearXNGSearchProvider(
        base_url="http://localhost:8080"
    )

    results = provider.search(
        "Horizon Glen Drive Improvements Grand Junction"
    )

    print(
        "SearXNG search provider test"
    )
    print(
        "----------------------------"
    )

    print(
        f"Results found: {len(results)}"
    )

    for url in results[:5]:
        print(
            f"- {url}"
        )

    assert len(results) > 0

    print(
        "\nSearXNG search provider test: PASS"
    )


if __name__ == "__main__":
    main()