"""
Test SearchContextProvider.

Validates:

- Country resolution
- Alias handling
- Language selection
- Construction vocabulary
- Government signals
- Negative filtering terms
"""

from construction_intelligence.ingestion.web.search_context_provider import (
    SearchContextProvider,
)


def print_context(
    requested_country: str,
    context,
) -> None:
    """
    Display resolved search context.
    """

    print()

    print(
        f"Requested country: {requested_country}"
    )

    print(
        f"Resolved country: {context.country}"
    )

    print(
        "-" * 60
    )

    print(
        f"Language: {context.language}"
    )

    print(
        f"Region: {context.region}"
    )

    print(
        "Construction terms:"
    )

    print(
        ", ".join(
            context.construction_terms
        )
    )

    print(
        "Infrastructure terms:"
    )

    print(
        ", ".join(
            context.infrastructure_terms
        )
    )

    print(
        "Procurement terms:"
    )

    print(
        ", ".join(
            context.procurement_terms
        )
    )

    print(
        "Government domains:"
    )

    print(
        ", ".join(
            context.government_domains
        )
    )

    print(
        "Official source terms:"
    )

    print(
        ", ".join(
            context.official_source_terms
        )
    )

    print(
        "Negative terms:"
    )

    print(
        ", ".join(
            context.negative_terms
        )
    )


def main() -> None:
    """
    Test country-specific search contexts.
    """

    provider = SearchContextProvider()


    #
    # Test exact matches and aliases.
    #
    test_cases = {

        "United States":
            "United States",

        "USA":
            "United States",

        "Brazil":
            "Brazil",

        "Brasil":
            "Brazil",

        "Mexico":
            "Mexico",

        "México":
            "Mexico",

        "Romania":
            "Romania",

        "România":
            "Romania",

        "Indonesia":
            "Indonesia",

        "Pakistan":
            "Pakistan",

        "Philippines":
            "Philippines",

        "South Africa":
            "South Africa",

        "China":
            "China",

        "Japan":
            "Japan",

        "South Korea":
            "South Korea",

        "Unknown Country":
            "United States",
    }


    contexts = {}


    for requested, expected in test_cases.items():

        context = (
            provider.get_context(
                requested
            )
        )

        contexts[requested] = context

        print_context(
            requested,
            context,
        )


        assert (
            context.country
            == expected
        ), (
            f"{requested} resolved incorrectly: "
            f"{context.country}"
        )


    print()

    print(
        "Validation checks"
    )

    print(
        "-----------------"
    )


    #
    # Brazil
    #
    brazil = contexts["Brazil"]

    assert (
        brazil.language == "pt"
    )

    assert (
        "licitação"
        in brazil.procurement_terms
    )

    assert (
        ".gov.br"
        in brazil.government_domains
    )


    #
    # Brazil alias
    #
    brasil = contexts["Brasil"]

    assert (
        brasil.country == "Brazil"
    )


    #
    # Mexico accent normalization
    #
    mexico = contexts["México"]

    assert (
        mexico.language == "es"
    )

    assert (
        "obra"
        in mexico.construction_terms
    )


    #
    # Indonesia
    #
    indonesia = contexts["Indonesia"]

    assert (
        indonesia.language == "id"
    )

    assert (
        "lelang"
        in indonesia.procurement_terms
    )

    assert (
        ".go.id"
        in indonesia.government_domains
    )


    #
    # Romania
    #
    romania = contexts["România"]

    assert (
        romania.language == "ro"
    )

    assert (
        "licitație"
        in romania.procurement_terms
    )


    #
    # Pakistan
    #
    pakistan = contexts["Pakistan"]

    assert (
        pakistan.language == "ur"
    )

    assert (
        ".gov.pk"
        in pakistan.government_domains
    )


    #
    # South Africa
    #
    south_africa = contexts["South Africa"]

    assert (
        ".gov.za"
        in south_africa.government_domains
    )


    #
    # East Asia
    #
    china = contexts["China"]

    assert (
        china.language == "zh"
    )

    assert (
        ".gov.cn"
        in china.government_domains
    )


    japan = contexts["Japan"]

    assert (
        japan.language == "ja"
    )


    korea = contexts["South Korea"]

    assert (
        korea.language == "ko"
    )


    #
    # Unknown fallback
    #
    fallback = contexts["Unknown Country"]

    assert (
        fallback.country
        == "United States"
    )


    print()

    print(
        "All SearchContextProvider tests passed."
    )

    print(
        "Search context provider test: PASS"
    )


if __name__ == "__main__":

    main()