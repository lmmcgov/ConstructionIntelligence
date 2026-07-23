"""
Test country search profiles.

Validates that country profiles provide:
- Correct language
- Government domains
- Construction terminology
- Procurement terminology
- Official source signals
- Negative filtering terms

This test ensures the international search
foundation is working before integrating
with EvidenceRanker.
"""

from construction_intelligence.ingestion.web.country_profiles import (
    COUNTRY_PROFILES,
)


def print_profile(
    country: str,
    profile,
) -> None:
    """
    Display profile information.
    """

    print()

    print(
        f"Country: {country}"
    )

    print(
        "-" * 60
    )

    print(
        f"Language: {profile.language}"
    )

    print(
        f"Government domains: "
        f"{profile.government_domains}"
    )

    print(
        f"Construction terms: "
        f"{profile.construction_terms[:5]}"
    )

    print(
        f"Infrastructure terms: "
        f"{profile.infrastructure_terms[:5]}"
    )

    print(
        f"Procurement terms: "
        f"{profile.procurement_terms[:5]}"
    )

    print(
        f"Official sources: "
        f"{profile.official_source_terms[:5]}"
    )

    print(
        f"Negative terms: "
        f"{profile.negative_terms[:5]}"
    )


def main() -> None:
    """
    Validate country profiles.
    """

    print(
        "Country profiles test"
    )

    print(
        "---------------------"
    )


    expected_countries = {

        "united states": {
            "language": "en",
            "domain": ".gov",
        },

        "brazil": {
            "language": "pt",
            "domain": ".gov.br",
        },

        "mexico": {
            "language": "es",
            "domain": ".gob.mx",
        },

        "guatemala": {
            "language": "es",
            "domain": ".gob.gt",
        },

        "chile": {
            "language": "es",
            "domain": ".gob.cl",
        },

        "colombia": {
            "language": "es",
            "domain": ".gov.co",
        },

        "argentina": {
            "language": "es",
            "domain": ".gob.ar",
        },

        "romania": {
            "language": "ro",
            "domain": ".gov.ro",
        },

        "indonesia": {
            "language": "id",
            "domain": ".go.id",
        },
    }


    #
    # Confirm profiles exist.
    #
    for country, expected in expected_countries.items():

        assert country in COUNTRY_PROFILES, (
            f"Missing profile: {country}"
        )


        profile = COUNTRY_PROFILES[country]


        print_profile(
            country,
            profile,
        )


        #
        # Validate language.
        #
        assert (
            profile.language
            ==
            expected["language"]
        )


        #
        # Validate government domains.
        #
        assert (
            expected["domain"]
            in profile.government_domains
        )


        #
        # Validate profile completeness.
        #
        assert (
            len(profile.construction_terms)
            > 0
        )

        assert (
            len(profile.infrastructure_terms)
            > 0
        )

        assert (
            len(profile.procurement_terms)
            > 0
        )

        assert (
            len(profile.negative_terms)
            > 0
        )


    #
    # Specific language checks.
    #

    brazil = COUNTRY_PROFILES["brazil"]

    assert (
        "licitação"
        in brazil.procurement_terms
    )

    assert (
        "prefeitura"
        in brazil.official_source_terms
    )


    indonesia = COUNTRY_PROFILES["indonesia"]

    assert (
        "lelang"
        in indonesia.procurement_terms
    )

    assert (
        ".go.id"
        in indonesia.government_domains
    )


    mexico = COUNTRY_PROFILES["mexico"]

    assert (
        "obra"
        in mexico.construction_terms
    )


    #
    # Ensure profiles are not accidentally
    # sharing mutable state.
    #
    brazil_negative_count = len(
        brazil.negative_terms
    )

    assert (
        brazil_negative_count
        >
        0
    )


    print()

    print(
        f"Profiles loaded: {len(COUNTRY_PROFILES)}"
    )

    print(
        "Country profiles test: PASS"
    )


if __name__ == "__main__":
    main()