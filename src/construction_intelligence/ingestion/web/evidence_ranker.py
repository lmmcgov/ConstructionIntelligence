"""
Evidence candidate ranking.

Ranks discovered URLs before extraction by evaluating:

- Source authority
- Municipal authority
- Construction relevance
- Procurement relevance
- Project similarity
- Document signals
- Negative intent signals

Designed for construction evidence discovery.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from construction_intelligence.core.project import (
    Project,
)


@dataclass(frozen=True)
class RankedEvidenceCandidate:
    """
    URL candidate with ranking information.
    """

    url: str

    score: int

    reasons: list[str]


class EvidenceRanker:
    """
    Rank evidence candidates before extraction.

    During development, retain a larger candidate pool
    because SearXNG search ordering can vary between runs.
    """

    def __init__(
        self,
        max_results: int = 50,
    ) -> None:

        self.max_results = max_results


    def rank(
        self,
        urls: list[str],
        project: Project,
    ) -> list[str]:

        ranked = self.rank_with_details(
            urls,
            project,
        )

        return [
            item.url
            for item in ranked[
                : self.max_results
            ]
        ]


    def rank_with_details(
        self,
        urls: list[str],
        project: Project,
    ) -> list[RankedEvidenceCandidate]:

        candidates = [
            self._score_url(
                url,
                project,
            )
            for url in urls
        ]

        return sorted(
            candidates,
            key=lambda item: item.score,
            reverse=True,
        )


    def _score_url(
        self,
        url: str,
        project: Project,
    ) -> RankedEvidenceCandidate:

        score = 0

        reasons: list[str] = []


        parsed = urlparse(url)

        domain = (
            parsed.netloc
            .lower()
        )

        path = (
            parsed.path
            .lower()
        )


        text = (
            domain
            + " "
            + path
        )


        #
        # SOURCE AUTHORITY
        #

        if any(
            term in domain
            for term in [
                ".gov",
                ".gov.",
                ".gouv.",
                ".gc.ca",
            ]
        ):

            score += 25

            reasons.append(
                "Government domain"
            )


        #
        # Municipal/local authority sources.
        #

        municipal_domains = [
            "gjcity",
            "city",
            "town",
            "county",
            "municipal",
            "publicworks",
            "horizondrivedistrict",
        ]


        if any(
            term in domain
            for term in municipal_domains
        ):

            score += 25

            reasons.append(
                "Municipal authority source"
            )


        #
        # Construction contractors.
        #

        contractor_terms = [
            "construction",
            "contractor",
            "builders",
            "engineering",
        ]


        if any(
            term in domain
            for term in contractor_terms
        ):

            score += 10

            reasons.append(
                "Construction company source"
            )


        #
        # Local news.
        #

        if any(
            term in domain
            for term in [
                "news",
                "sentinel",
                "gazette",
                "journal",
            ]
        ):

            score += 10

            reasons.append(
                "Local news source"
            )


        #
        # DOCUMENT TYPE SIGNALS
        #

        if ".pdf" in path:

            score += 15

            reasons.append(
                "PDF document"
            )


        if any(
            term in path
            for term in [
                "documentcenter",
                "download",
                "attachment",
            ]
        ):

            score += 15

            reasons.append(
                "Official document repository"
            )


        #
        # PROJECT PAGE SIGNALS
        #

        project_path_terms = [
            "project",
            "projects",
            "construction",
            "contract",
            "bid",
            "procurement",
            "award",
        ]


        for term in project_path_terms:

            if term in path:

                score += 8

                reasons.append(
                    f"Project path signal: {term}"
                )


        #
        # CONSTRUCTION SIGNALS
        #

        construction_terms = {

            "construction": 15,
            "improvement": 12,
            "improvements": 12,
            "roundabout": 15,
            "intersection": 10,
            "corridor": 8,
            "transportation": 8,
            "road": 5,
            "engineering": 8,
            "contract": 10,
            "award": 10,
            "bid": 8,
            "rfp": 8,

        }


        for term, weight in construction_terms.items():

            if term in text:

                score += weight

                reasons.append(
                    f"Construction signal: {term}"
                )


        #
        # PROJECT MATCHING
        #

        project_terms: list[str] = []


        if project.name:

            project_terms.extend(
                project.name.lower()
                .replace("-", " ")
                .split()
            )


        if project.aliases:

            for alias in project.aliases:

                project_terms.extend(
                    alias.lower()
                    .replace("-", " ")
                    .split()
                )


        if project.road_name:

            project_terms.extend(
                project.road_name.lower()
                .replace("-", " ")
                .split()
            )


        if project.city:

            project_terms.append(
                project.city.lower()
            )


        if project.state:

            project_terms.append(
                project.state.lower()
            )


        project_terms = [
            term
            for term in project_terms
            if len(term) > 3
            and term not in {
                "road",
                "drive",
                "project",
                "construction",
                "improvement",
                "improvements",
            }
        ]


        matched_terms = [
            term
            for term in set(project_terms)
            if term in text
        ]


        if len(matched_terms) >= 3:

            score += 30

            reasons.append(
                "Strong project match"
            )


        elif len(matched_terms) == 2:

            score += 20

            reasons.append(
                "Moderate project match"
            )


        elif len(matched_terms) == 1:

            score += 8

            reasons.append(
                "Weak project match"
            )


        #
        # Exact project indicators.
        #

        if any(
            phrase in text
            for phrase in [
                "g-road",
                "and-g-road",
                "roundabout",
            ]
        ):

            score += 15

            reasons.append(
                "Intersection signal"
            )


        #
        # NEGATIVE INTENT
        #

        negative_terms = {

            "playstation": -50,
            "steam": -50,
            "imdb": -50,
            "movie": -40,
            "film": -40,
            "game": -40,

            "hotel": -30,
            "restaurant": -30,
            "menu": -30,
            "careers": -20,
            "jobs": -20,

        }


        for term, penalty in negative_terms.items():

            if term in text:

                score += penalty

                reasons.append(
                    f"Negative signal: {term}"
                )


        return RankedEvidenceCandidate(
            url=url,
            score=score,
            reasons=reasons,
        )