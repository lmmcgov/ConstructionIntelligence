from construction_intelligence.ingestion.web.searxng_search_provider import (
    SearXNGSearchProvider,
)


def main():

    provider = SearXNGSearchProvider(
        "http://localhost:8080"
    )

    results = provider.search(
        "Horizon Glen Drive Improvements construction Grand Junction"
    )

    print("\nSearch Results")
    print("----------------")

    for url in results[:10]:
        print(url)


if __name__ == "__main__":
    main()