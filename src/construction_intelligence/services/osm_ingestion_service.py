from dataclasses import dataclass

from construction_intelligence.ingestion.osm.evidence_factory import (
    OSMEvidenceFactory,
)
from construction_intelligence.ingestion.osm.extractor import (
    OSMConstructionExtractor,
)
from construction_intelligence.mappers.osm_project_mapper import (
    OSMProjectMapper,
)
from construction_intelligence.repositories.evidence_repository import (
    EvidenceRepository,
)
from construction_intelligence.repositories.project_repository import (
    ProjectRepository,
)


@dataclass(slots=True)
class IngestionResult:
    """Summary of an ingestion run."""

    projects_created: int = 0
    projects_updated: int = 0

    evidence_created: int = 0
    evidence_updated: int = 0


class OSMIngestionService:
    """Coordinates the OpenStreetMap ingestion pipeline."""

    def __init__(
        self,
        project_repository: ProjectRepository,
        evidence_repository: EvidenceRepository,
    ) -> None:
        self._projects = project_repository
        self._evidence = evidence_repository

        self._extractor = OSMConstructionExtractor()
        self._mapper = OSMProjectMapper()
        self._evidence_factory = OSMEvidenceFactory()

    def ingest(
        self,
        pbf_path: str,
    ) -> IngestionResult:
        """Import construction projects from a PBF."""

        result = IngestionResult()

        ways = self._extractor.extract(pbf_path)

        for way in ways:
            #
            # Map the OSM way into a Project
            #
            candidate = self._mapper.map(way)

            #
            # Project
            #
            project = self._projects.get_by_origin_id(
                candidate.origin,
                candidate.origin_id,
            )

            if project is None:
                project = candidate
                self._projects.add(project)
                result.projects_created += 1
            else:
                result.projects_updated += 1

            #
            # Evidence
            #
            evidence = self._evidence.find_by_origin_id(
                candidate.origin,
                candidate.origin_id,
            )

            if evidence is None:
                evidence = self._evidence_factory.create(
                    project,
                    way,
                )

                self._evidence.add(evidence)
                project.add_evidence(evidence.id)

                result.evidence_created += 1
            else:
                result.evidence_updated += 1

        return result