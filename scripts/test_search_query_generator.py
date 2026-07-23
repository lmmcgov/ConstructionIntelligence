"""
Test SearchQueryGenerator.

Validates:

- Structured SearchQuery output
- Query categories
- Query priorities
- Query execution tiers
- Location-aware generation
- Negative filtering behavior
- Country localization
"""

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.search_context_provider import (
    SearchContextProvider,
)

from construction_intelligence.ingestion.web.search_query_generator import (
    SearchQueryGenerator,
)


def print_queries(
    country: str,
    queries,
) -> None:
    """
    Display generated queries.
    """

    print()
    print(
        f"Country: {country}"
    )

    print(
        "-" * 70
    )


    for index, query in enumerate(
        queries,
        start=1,
    ):

        print(
            f"{index}."
        )

        print(
            f"Query: {query.query}"
        )

        print(
            f"Category: {query.category}"
        )

        print(
            f"Priority: {query.priority}"
        )

        print(
            f"Tier: {query.tier}"
        )

        print()


def main() -> None:
    """
    Test query generation.
    """

    provider = (
        SearchContextProvider()
    )

    generator = (
        SearchQueryGenerator()
    )


    project = Project(
        name="Horizon Glen Drive Improvements",
        city="Grand Junction",
        state="Colorado",
        country="United States",
        road_name="Horizon Glen Drive",
    )


    countries = [
        "United States",
        "Brazil",
    ]


    contexts = {}


    for country in countries:

        context = (
            provider.get_context(
                country
            )
        )

        contexts[country] = context


        queries = (
            generator.generate(
                project,
                context,
            )
        )


        print_queries(
            country,
            queries,
        )


    print()
    print(
        "Validation checks"
    )

    print(
        "-----------------"
    )


    #
    # United States checks
    #

    us_structured = (
        generator.generate(
            project,
            contexts["United States"],
        )
    )


    us_queries = [
        query.query
        for query
        in us_structured
    ]


    #
    # Structured output exists.
    #

    assert len(
        us_structured
    ) > 0


    #
    # Every query has required metadata.
    #

    assert all(
        query.category
        for query
        in us_structured
    )


    assert all(
        query.priority
        for query
        in us_structured
    )


    assert all(
        query.tier
        for query
        in us_structured
    )


    #
    # Tier validation.
    #

    assert all(
        query.tier in [1, 2, 3]
        for query
        in us_structured
    )


    #
    # Category / tier relationship checks.
    #

    official_queries = [
        query
        for query
        in us_structured
        if query.category == "official"
    ]


    assert all(
        query.tier == 1
        for query
        in official_queries
    )


    procurement_queries = [
        query
        for query
        in us_structured
        if query.category == "procurement"
    ]


    assert all(
        query.tier == 1
        for query
        in procurement_queries
    )


    construction_queries = [
        query
        for query
        in us_structured
        if query.category == "construction"
    ]


    assert all(
        query.tier == 2
        for query
        in construction_queries
    )


    news_queries = [
        query
        for query
        in us_structured
        if query.category == "news"
    ]


    assert all(
        query.tier == 3
        for query
        in news_queries
    )


    #
    # Specific infrastructure project names
    # should NOT receive negative filters.
    #

    assert not any(
        "-movie"
        in query
        for query
        in us_queries
    )


    #
    # Official queries exist.
    #

    assert any(
        query.category == "official"
        for query
        in us_structured
    )


    #
    # Procurement queries exist.
    #

    assert any(
        query.category == "procurement"
        for query
        in us_structured
    )


    #
    # Location is included.
    #

    assert any(
        "Grand Junction"
        in query.query
        for query
        in us_structured
    )


    #
    # Ambiguous project name test.
    #

    ambiguous_project = Project(
        name="Horizon",
        city="Grand Junction",
        state="Colorado",
        country="United States",
    )


    ambiguous_queries = (
        generator.generate(
            ambiguous_project,
            contexts["United States"],
        )
    )


    ambiguous_query_text = [
        query.query
        for query
        in ambiguous_queries
    ]


    #
    # Ambiguous names SHOULD receive
    # negative filters.
    #

    assert any(
        "-movie"
        in query
        for query
        in ambiguous_query_text
    )


    #
    # Brazil localization check.
    #

    brazil_queries = (
        generator.generate(
            project,
            contexts["Brazil"],
        )
    )


    assert any(
        query.category == "official"
        for query
        in brazil_queries
    )


    assert any(
        "prefeitura"
        in query.query
        for query
        in brazil_queries
    )


    #
    # Verify Brazil official queries
    # remain Tier 1.
    #

    brazil_official = [
        query
        for query
        in brazil_queries
        if query.category == "official"
    ]


    assert all(
        query.tier == 1
        for query
        in brazil_official
    )


    print()
    print(
        "All SearchQueryGenerator tests passed."
    )

    print(
        "Search query generator test: PASS"
    )


if __name__ == "__main__":

    main()