"""
SearXNG implementation of web search provider.
"""

from __future__ import annotations

from collections import Counter

import requests

from construction_intelligence.ingestion.web.search_provider import (
    SearchProvider,
)


class SearXNGSearchProvider(
    SearchProvider,
):
    """
    Searches the web using a local SearXNG instance.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        pages: int = 3,
    ) -> None:

        self.base_url = (
            base_url.rstrip("/")
        )

        self.pages = pages


    def search(
        self,
        query: str,
    ) -> list[str]:
        """
        Execute search and return result URLs.

        SearXNG defaults to roughly 10 results.
        We paginate to build a larger candidate pool.

        Debug logging included to verify:
        - pagination behavior
        - result counts per page
        - search engine diversity
        - cumulative URL collection
        """

        urls: list[str] = []

        engine_counts = Counter()


        for page in range(
            1,
            self.pages + 1,
        ):

            response = requests.get(
                f"{self.base_url}/search",
                params={
                    "q": query,
                    "format": "json",
                    "pageno": str(page),
                },
                timeout=15,
            )


            response.raise_for_status()


            data = response.json()


            results = data.get(
                "results",
                []
            )


            print()

            print(
                f"SearXNG page {page}"
            )

            print(
                "----------------"
            )

            print(
                f"Results returned: {len(results)}"
            )


            if not results:

                print(
                    "No results returned. Stopping pagination."
                )

                break



            for result in results:

                url = result.get(
                    "url"
                )

                engine = result.get(
                    "engine",
                    "unknown",
                )

                title = result.get(
                    "title",
                    "",
                )


                engine_counts[
                    engine
                ] += 1


                print()

                print(
                    f"Engine: {engine}"
                )

                print(
                    f"Title: {title}"
                )

                print(
                    f"URL: {url}"
                )

                print(
                    "----------------"
                )


                if url:

                    urls.append(
                        url
                    )


            print()

            print(
                f"Total URLs collected so far: {len(urls)}"
            )



        unique_urls = list(
            dict.fromkeys(
                urls
            )
        )


        print()

        print(
            "SearXNG SEARCH SUMMARY"
        )

        print(
            "----------------------"
        )

        print(
            f"Pages requested: {self.pages}"
        )

        print(
            f"Raw URLs collected: {len(urls)}"
        )

        print(
            f"Unique URLs returned: {len(unique_urls)}"
        )


        print()

        print(
            "SEARCH ENGINE SUMMARY"
        )

        print(
            "---------------------"
        )


        if engine_counts:

            for engine, count in engine_counts.items():

                print(
                    f"{engine}: {count}"
                )

        else:

            print(
                "No engine metadata returned"
            )


        return unique_urls