"""
Test SearchQuery model.
"""

from construction_intelligence.ingestion.web.search_query import (
    SearchQuery,
)


def main():

    query = SearchQuery(
        query=(
            '"Horizon Glen Drive Improvements" bid'
        ),
        category="procurement",
        priority=2,
    )


    print(
        "Query:"
    )

    print(
        query.query
    )

    print()

    print(
        "Category:"
    )

    print(
        query.category
    )

    print()

    print(
        "Priority:"
    )

    print(
        query.priority
    )


    assert (
        query.category
        ==
        "procurement"
    )

    assert (
        query.priority
        ==
        2
    )


    print()

    print(
        "SearchQuery model test: PASS"
    )


if __name__ == "__main__":

    main()