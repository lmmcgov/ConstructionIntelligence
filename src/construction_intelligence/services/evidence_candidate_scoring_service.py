"""
Scores discovered URLs before evidence extraction.

Uses:

- URL structure
- Domain signals
- Project metadata
- Construction relevance
- Negative signals

The goal is to avoid expensive extraction
of obviously irrelevant web pages.

This is intentionally a permissive filter.
Final evidence decisions happen later through:

Discovery
    |
    v
Candidate scoring
    |
    v
Evidence ranking
    |
    v
Extraction
    |
    v
Evidence evaluation
    |
    v
Quality gate
"""

from __future__ import annotations

from urllib.parse import urlparse

from construction_intelligence.core.project import (
    Project,
)


class EvidenceCandidateScoringService:
    """
    Determines whether a discovered URL
    should proceed to extraction.

    This is a lightweight triage layer,
    not the final relevance decision.
    """


    def __init__(
        self,
        minimum_score: float = 0.05,
    ) -> None:

        self.minimum_score = (
            minimum_score
        )


    def score(
        self,
        url: str,
        project: Project,
        title: str = "",
    ) -> float:
        """
        Calculate candidate quality score.
        """

        parsed = urlparse(
            url
        )


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
            + " "
            + title.lower()
        )


        score = 0.0


        #
        # Government authority.
        #
        if any(
            indicator in domain
            for indicator in [
                ".gov",
                ".gov.",
                ".gouv.",
                ".gc.ca",
            ]
        ):

            score += 0.20


        #
        # Municipal authority.
        #
        municipal_terms = [
            "city",
            "town",
            "county",
            "municipal",
            "civic",
            "publicworks",
            "gov",
        ]


        if any(
            term in domain
            for term in municipal_terms
        ):

            score += 0.20



        #
        # Construction-related URL paths.
        #
        construction_paths = [
            "construction",
            "project",
            "projects",
            "improvement",
            "capital",
            "engineering",
            "infrastructure",
            "transportation",
            "road",
            "corridor",
        ]


        if any(
            term in path
            for term in construction_paths
        ):

            score += 0.15



        #
        # Procurement signals.
        #
        procurement_terms = [
            "bid",
            "contract",
            "procurement",
            "rfp",
            "tender",
            "award",
            "vendor",
        ]


        if any(
            term in text
            for term in procurement_terms
        ):

            score += 0.15



        #
        # Document signals.
        #
        if any(
            term in path
            for term in [
                ".pdf",
                "document",
                "download",
                "attachment",
            ]
        ):

            score += 0.05



        #
        # Construction vocabulary.
        #
        construction_terms = [
            "construction",
            "roundabout",
            "road",
            "intersection",
            "corridor",
            "contractor",
            "builder",
            "transportation",
        ]


        if any(
            term in text
            for term in construction_terms
        ):

            score += 0.10



        #
        # Project-aware signals.
        #
        # Reward URLs/titles containing:
        #
        # - project aliases
        # - city
        # - state
        #
        project_terms: list[str] = []


        if project.name:

            project_terms.append(
                project.name
            )


        if project.aliases:

            project_terms.extend(
                project.aliases
            )


        if project.road_name:

            project_terms.append(
                project.road_name
            )


        if project.city:

            project_terms.append(
                project.city
            )


        if project.state:

            project_terms.append(
                project.state
            )


        for term in project_terms:

            normalized = (
                term.lower()
                .strip()
            )


            if (
                normalized
                and
                normalized in text
            ):

                score += 0.10



        #
        # Negative signals.
        #
        # These remove obvious noise.
        #
        negative_terms = [
            "wikipedia",
            "playstation",
            "steam",
            "imdb",
            "movie",
            "film",
            "game",
            "facebook",
            "jobs",
            "careers",
            "bank",
            "hotel",
            "real-estate",
            "homes-for-sale",
        ]


        for term in negative_terms:

            if term in text:

                score -= 0.40



        return max(
            0.0,
            min(
                score,
                1.0,
            ),
        )



    def accept(
        self,
        url: str,
        project: Project,
        title: str = "",
    ) -> bool:
        """
        Determine whether candidate proceeds
        to ranking and extraction.
        """

        return (
            self.score(
                url,
                project,
                title,
            )
            >=
            self.minimum_score
        )



    def rejection_reason(
        self,
        url: str,
        project: Project,
        title: str = "",
    ) -> str:
        """
        Explain why a candidate failed.
        """

        score = self.score(
            url,
            project,
            title,
        )


        return (
            f"Candidate score {score:.2f} "
            f"below threshold "
            f"{self.minimum_score:.2f}"
        )