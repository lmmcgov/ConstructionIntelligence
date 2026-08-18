"""
Localized search query generation.

Generates construction intelligence search queries
using:

- Project metadata
- Project aliases
- Country-specific SearchContext
- Construction terminology
- Infrastructure terminology
- Procurement terminology
- Government signals
- News signals
- Intelligent negative filtering
"""

from __future__ import annotations


from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.search_context import (
    SearchContext,
)

from construction_intelligence.ingestion.web.search_query import (
    SearchQuery,
)


#
# Search strategy priorities.
#

OFFICIAL_PRIORITY = 1
PROCUREMENT_PRIORITY = 2
CONSTRUCTION_PRIORITY = 3
INFRASTRUCTURE_PRIORITY = 4
NEWS_PRIORITY = 5
DISCOVERY_PRIORITY = 6


#
# Search execution tiers.
#

OFFICIAL_TIER = 1
PROCUREMENT_TIER = 1
CONSTRUCTION_TIER = 2
INFRASTRUCTURE_TIER = 2
NEWS_TIER = 3
DISCOVERY_TIER = 3



class SearchQueryGenerator:
    """
    Generates localized search strategies
    for construction evidence discovery.
    """

    def __init__(
        self,
        max_queries: int = 25,
    ) -> None:

        self.max_queries = max_queries



    def generate(
        self,
        project: Project,
        context: SearchContext,
    ) -> list[SearchQuery]:

        queries: list[SearchQuery] = []


        #
        # Build project identity terms.
        #
        search_terms = self._project_search_terms(
            project
        )


        location = self._location_string(
            project,
            include_country=False,
        )


        #
        # High-confidence construction queries.
        #
        high_confidence_terms = [
            "construction",
            "construction project",
            "road improvement",
            "capital improvement",
            "roundabout",
            "infrastructure",
            "contract",
            "contractor",
            "project",
        ]


        for project_term in search_terms[:8]:

            for intent in high_confidence_terms:

                self._add(
                    queries,
                    (
                        f'"{project_term}" '
                        f'{intent} '
                        f'{location}'
                    ),
                    category="construction",
                    priority=CONSTRUCTION_PRIORITY,
                    tier=CONSTRUCTION_TIER,
                )



        #
        # Government-specific construction searches.
        #
        # {state}.gov is a US state-domain convention -- only
        # generate this query when a state is present.
        #
        if project.state:

            for project_term in search_terms[:8]:

                self._add(
                    queries,
                    (
                        f'"{project_term}" '
                        f'construction '
                        f'site:{project.state.lower()}'
                        f'.gov'
                    ),
                    category="official",
                    priority=OFFICIAL_PRIORITY,
                    tier=OFFICIAL_TIER,
                )



        #
        # Official government searches.
        #
        self._add_official_queries(
            queries,
            project,
            context,
            search_terms,
        )



        #
        # Procurement searches.
        #
        self._add_terms(
            queries,
            project,
            context.procurement_terms,
            search_terms,
            category="procurement",
            priority=PROCUREMENT_PRIORITY,
            tier=PROCUREMENT_TIER,
        )



        #
        # Infrastructure searches.
        #
        self._add_terms(
            queries,
            project,
            context.infrastructure_terms,
            search_terms,
            category="infrastructure",
            priority=INFRASTRUCTURE_PRIORITY,
            tier=INFRASTRUCTURE_TIER,
        )



        #
        # News searches.
        #
        self._add_news_queries(
            queries,
            project,
            context,
            search_terms,
        )



        #
        # General discovery searches.
        #
        for term in search_terms:

            self._add(
                queries,
                (
                    f'"{term}" '
                    f'{location}'
                ),
                category="discovery",
                priority=DISCOVERY_PRIORITY,
                tier=DISCOVERY_TIER,
            )



        #
        # Apply exclusions.
        #
        queries = self._apply_negative_terms(
            queries,
            context,
            project,
        )



        #
        # Debug output.
        #
        print()

        print(
            "GENERATED SEARCH QUERIES"
        )

        print(
            "-------------------------"
        )


        for query in queries[:20]:

            print(
                query.query
            )



        return self._sort_queries(
            self._deduplicate(
                queries
            )
        )[: self.max_queries]



    def _project_search_terms(
        self,
        project: Project,
    ) -> list[str]:

        terms: list[str] = []


        if project.aliases:

            terms.extend(
                project.aliases
            )


        if project.road_name:

            terms.append(
                project.road_name
            )


        if project.name:

            terms.append(
                project.name
            )


        return list(
            dict.fromkeys(
                terms
            )
        )



    def _location_string(
        self,
        project: Project,
        include_country: bool = False,
    ) -> str:

        parts = []


        if project.city:

            parts.append(
                project.city
            )


        if project.state:

            parts.append(
                project.state
            )


        if include_country and project.country:

            parts.append(
                project.country
            )


        return " ".join(parts)



    def _add_terms(
        self,
        queries,
        project,
        terms,
        search_terms,
        category,
        priority,
        tier,
    ) -> None:

        for project_term in search_terms[:5]:

            for term in terms[:5]:

                self._add(
                    queries,
                    (
                        f'"{project_term}" '
                        f'{term} '
                        f'{project.city or ""}'
                    ),
                    category,
                    priority,
                    tier,
                )



    def _add_official_queries(
        self,
        queries,
        project,
        context,
        search_terms,
    ) -> None:

        for project_term in search_terms[:8]:

            self._add(
                queries,
                (
                    f'"{project_term}" '
                    f'construction '
                    f'{project.city or ""} '
                    f'{project.state or ""}'
                ),
                "official",
                OFFICIAL_PRIORITY,
                OFFICIAL_TIER,
            )


            for term in (
                context.official_source_terms
                +
                context.government_terms
            )[:6]:

                self._add(
                    queries,
                    (
                        f'"{project_term}" '
                        f'{term}'
                    ),
                    "official",
                    OFFICIAL_PRIORITY,
                    OFFICIAL_TIER,
                )


            #
            # Government + municipal domains.
            #
            # Includes:
            #
            # - national government sites
            # - state government sites
            # - city/municipal sources
            #
            for domain in context.all_official_domains():

                self._add(
                    queries,
                    (
                        f'"{project_term}" '
                        f'site:{domain}'
                    ),
                    "official",
                    OFFICIAL_PRIORITY,
                    OFFICIAL_TIER,
                )



    def _add_news_queries(
        self,
        queries,
        project,
        context,
        search_terms,
    ) -> None:

        for project_term in search_terms[:3]:

            for term in context.news_terms[:3]:

                self._add(
                    queries,
                    (
                        f'"{project_term}" '
                        f'{term} '
                        f'{project.city or ""}'
                    ),
                    "news",
                    NEWS_PRIORITY,
                    NEWS_TIER,
                )



    def _apply_negative_terms(
        self,
        queries,
        context,
        project,
    ):

        exclusions = list(
            context.negative_terms
        )


        exclusions.extend(
            [
                "playstation",
                "steam",
                "imdb",
                "movie",
                "film",
            ]
        )


        exclusion_string = " ".join(
            [
                f"-{term.replace(' ', '-')}"
                for term in exclusions[:10]
            ]
        )


        return [
            SearchQuery(
                query=(
                    f"{item.query} "
                    f"{exclusion_string}"
                ),
                category=item.category,
                priority=item.priority,
                tier=item.tier,
            )
            for item in queries
        ]



    def _add(
        self,
        queries,
        query,
        category,
        priority,
        tier,
    ) -> None:

        if query:

            queries.append(
                SearchQuery(
                    query=query.strip(),
                    category=category,
                    priority=priority,
                    tier=tier,
                )
            )



    def _deduplicate(
        self,
        queries,
    ):

        seen = set()

        results = []


        for query in queries:

            key = (
                query.query
                .lower()
            )


            if key not in seen:

                seen.add(
                    key
                )

                results.append(
                    query
                )


        return results



    def _sort_queries(
        self,
        queries,
    ):

        return sorted(
            queries,
            key=lambda item: (
                item.tier,
                item.priority,
                item.category,
            ),
        )