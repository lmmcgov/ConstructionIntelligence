"""
Service for discovering and creating evidence from web sources.

Pipeline:

Discovery
    |
    v
URL Deduplication
    |
    v
Candidate Ranking
    |
    v
Candidate Scoring
    |
    v
Extraction
    |
    v
Evidence Creation
"""

from __future__ import annotations


from construction_intelligence.core.evidence import (
    Evidence,
)

from construction_intelligence.core.project import (
    Project,
)

from construction_intelligence.ingestion.web.evidence_discovery_service import (
    EvidenceDiscoveryService,
)

from construction_intelligence.ingestion.web.evidence_factory import (
    WebEvidenceFactory,
)

from construction_intelligence.ingestion.web.extractor import (
    WebExtractor,
)

from construction_intelligence.ingestion.web.evidence_ranker import (
    EvidenceRanker,
)

from construction_intelligence.services.evidence_candidate_scoring_service import (
    EvidenceCandidateScoringService,
)



class WebEvidenceIngestionService:
    """
    Discovers URLs, ranks candidates,
    filters weak candidates, extracts documents,
    and converts them into Evidence objects.
    """


    def __init__(
        self,
        discovery_service: EvidenceDiscoveryService,
        extractor: WebExtractor,
        evidence_factory: WebEvidenceFactory | None = None,
        ranker: EvidenceRanker | None = None,
        candidate_scoring_service: EvidenceCandidateScoringService | None = None,
    ) -> None:


        self.discovery_service = (
            discovery_service
        )


        self.extractor = extractor


        self.evidence_factory = (
            evidence_factory
            if evidence_factory is not None
            else WebEvidenceFactory()
        )


        self.ranker = (
            ranker
            if ranker is not None
            else EvidenceRanker()
        )


        self.candidate_scoring_service = (
            candidate_scoring_service
            if candidate_scoring_service is not None
            else EvidenceCandidateScoringService()
        )



    def ingest(
        self,
        project: Project,
    ) -> list[Evidence]:
        """
        Discover, rank, filter, extract,
        and create evidence records.
        """


        #
        # Discover candidate URLs.
        #
        urls = (
            self.discovery_service
            .discover_urls(
                project
            )
        )


        #
        # Remove duplicate URLs.
        #
        urls = self._deduplicate_urls(
            urls
        )


        print()

        print(
            "DISCOVERED URLS"
        )

        print(
            "----------------"
        )


        for url in urls:

            print(url)



        #
        # Rank candidates before filtering.
        #
        # Ranking understands project context:
        #
        # - aliases
        # - city
        # - state
        #
        ranked_urls = (
            self.ranker.rank(
                urls,
                project,
            )
        )


        print()

        print(
            "RANKED URLS"
        )

        print(
            "----------------"
        )


        for url in ranked_urls:

            print(url)



        #
        # Candidate scoring after ranking.
        #
        filtered_urls: list[str] = []

        rejected_candidates = 0



        for url in ranked_urls:

            if self.candidate_scoring_service.accept(
                url,
                project,
            ):

                filtered_urls.append(
                    url
                )

            else:

                rejected_candidates += 1


                print()

                print(
                    "Candidate rejected:"
                )

                print(
                    url
                )

                print(
                    self.candidate_scoring_service.rejection_reason(
                        url,
                        project,
                    )
                )



        print()

        print(
            "CANDIDATE FILTERING"
        )

        print(
            "-------------------"
        )

        print(
            f"Accepted candidates: {len(filtered_urls)}"
        )

        print(
            f"Rejected candidates: {rejected_candidates}"
        )



        evidence_records: list[Evidence] = []



        #
        # Extract only candidates that passed
        # discovery scoring.
        #
        for url in filtered_urls:

            try:

                document = (
                    self.extractor.extract(
                        url
                    )
                )


                evidence = (
                    self.evidence_factory.create(
                        project.id,
                        document,
                    )
                )


                evidence_records.append(
                    evidence
                )



            except Exception as error:

                print()

                print(
                    "Evidence extraction failed"
                )

                print(
                    url
                )

                print(
                    f"Reason: {error}"
                )

                continue



        return evidence_records



    def _deduplicate_urls(
        self,
        urls: list[str],
    ) -> list[str]:
        """
        Remove duplicate URLs while preserving order.
        """


        seen: set[str] = set()

        unique_urls: list[str] = []



        for url in urls:

            normalized = (
                url.strip()
                .lower()
            )


            if normalized not in seen:

                seen.add(
                    normalized
                )

                unique_urls.append(
                    url
                )



        return unique_urls