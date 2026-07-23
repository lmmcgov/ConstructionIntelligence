"""
Test the OpenStreetMap ingestion pipeline.
"""

from construction_intelligence.repositories.evidence_repository import (
    EvidenceRepository,
)
from construction_intelligence.repositories.project_repository import (
    ProjectRepository,
)
from construction_intelligence.services.osm_ingestion_service import (
    OSMIngestionService,
)


def print_result(title: str, result) -> None:
    print(title)
    print("-" * 40)
    print(f"Projects created : {result.projects_created}")
    print(f"Projects updated : {result.projects_updated}")
    print(f"Evidence created : {result.evidence_created}")
    print(f"Evidence updated : {result.evidence_updated}")
    print()


def main() -> None:
    project_repository = ProjectRepository()
    evidence_repository = EvidenceRepository()

    service = OSMIngestionService(
        project_repository=project_repository,
        evidence_repository=evidence_repository,
    )

    result1 = service.ingest("data/raw/GJ.osm.pbf")
    result2 = service.ingest("data/raw/GJ.osm.pbf")

    print_result("FIRST INGESTION", result1)
    print_result("SECOND INGESTION", result2)

    print("REPOSITORY TOTALS")
    print("-" * 40)
    print(f"Projects : {project_repository.count()}")
    print(f"Evidence : {evidence_repository.count()}")


if __name__ == "__main__":
    main()