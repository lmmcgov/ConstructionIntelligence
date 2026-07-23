"""
Service for determining whether evidence corresponds to a project.
"""

from __future__ import annotations

import re

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.evidence_match_result import (
    EvidenceMatchResult,
)
from construction_intelligence.core.project import Project


class EvidenceMatcherService:
    """
    Matches evidence against construction projects.

    Determines:
    "Does this evidence refer to this project?"

    This service evaluates identity matching only.
    Source quality is handled elsewhere.
    """

    def match(
        self,
        project: Project,
        evidence: Evidence,
    ) -> EvidenceMatchResult:

        score = 0.0

        reasons: list[str] = []


        title = (
            evidence.title.lower()
            if evidence.title
            else ""
        )

        content = (
            evidence.content.lower()
            if evidence.content
            else ""
        )


        text = self._normalize(
            f"{title} {content}"
        )


        #
        # Track signals.
        #
        alias_found = False
        construction_found = False
        location_count = 0


        #
        # Construction context.
        #
        construction_terms = {
            "construction",
            "roundabout",
            "improvement",
            "improvements",
            "transportation",
            "roadway",
            "intersection",
            "corridor",
            "capital project",
            "reconstruction",
        }


        matched_construction = [
            term
            for term in construction_terms
            if term in text
        ]


        if matched_construction:

            construction_found = True

            score += 0.20

            reasons.append(
                "Construction context confirmed"
            )


        #
        # Alias matching.
        #
        if project.aliases:

            for alias in project.aliases:

                normalized_alias = self._normalize(
                    alias
                )


                #
                # Exact alias.
                #
                if normalized_alias in text:

                    alias_found = True


                    if (
                        " and "
                        in normalized_alias
                        or
                        "roundabout"
                        in normalized_alias
                    ):

                        score += 0.35

                        reasons.append(
                            f"Strong project alias match: {alias}"
                        )

                    else:

                        score += 0.25

                        reasons.append(
                            f"Project alias appears: {alias}"
                        )

                    break


        #
        # Alias component matching.
        #
        # Handles:
        #
        # Horizon Drive Roundabouts
        # Horizon Drive Improvements
        # Exit 31 Horizon Drive
        #
        if not alias_found and project.aliases:

            alias_components = []

            for alias in project.aliases:

                alias_components.extend(
                    self._components(alias)
                )


            alias_components = [
                word
                for word in alias_components
                if word not in {
                    "road",
                    "drive",
                    "roundabout",
                    "project",
                    "improvement",
                    "improvements",
                    "and",
                }
            ]


            matched_alias_components = [
                word
                for word in set(alias_components)
                if word in text
            ]


            if len(
                matched_alias_components
            ) >= 2:

                score += 0.30

                reasons.append(
                    "Multiple project alias components found"
                )

                reasons.append(
                    "Matched components: "
                    +
                    ", ".join(
                        matched_alias_components
                    )
                )


            elif len(
                matched_alias_components
            ) == 1:

                score += 0.10

                reasons.append(
                    "Single project alias component found"
                )


        #
        # Project name components.
        #
        project_components = (
            self._components(
                project.name
            )
        )


        meaningful_components = [
            word
            for word in project_components
            if word not in {
                "road",
                "drive",
                "project",
                "construction",
                "improvement",
                "improvements",
            }
        ]


        matched_components = [
            word
            for word in meaningful_components
            if word in text
        ]


        if len(
            matched_components
        ) >= 2:

            score += 0.20

            reasons.append(
                "Multiple project name components found"
            )


        elif len(
            matched_components
        ) == 1:

            score += 0.05

            reasons.append(
                "Single project component found"
            )


        #
        # Road/intersection matching.
        #
        if project.road_name:

            road_name = self._normalize(
                project.road_name
            )


            if road_name in text:

                score += 0.20

                reasons.append(
                    "Road name confirmed"
                )


        #
        # Location confirmation.
        #
        for location in [
            project.city,
            project.state,
        ]:

            if (
                location
                and
                self._normalize(location)
                in text
            ):

                score += 0.10

                location_count += 1

                reasons.append(
                    f"Location confirmed: {location}"
                )


        #
        # Penalize weak matches.
        #
        # A document mentioning only Horizon Drive
        # without construction context is likely noise.
        #
        if (
            score < 0.40
            and
            not construction_found
        ):

            score *= 0.5

            reasons.append(
                "Reduced score due to missing "
                "construction context"
            )


        #
        # Normalize.
        #
        score = min(
            score,
            1.0,
        )


        if score == 0:

            reasons.append(
                "No project matching signals"
            )


        return EvidenceMatchResult(
            match_score=score,
            reasons=tuple(reasons),
        )


    def _normalize(
        self,
        text: str,
    ) -> str:

        text = re.sub(
            r"[^\w\s]",
            " ",
            text.lower(),
        )

        return re.sub(
            r"\s+",
            " ",
            text,
        ).strip()


    def _components(
        self,
        text: str,
    ) -> list[str]:

        return [
            word
            for word in re.findall(
                r"\w+",
                text.lower(),
            )
            if len(word) > 3
        ]