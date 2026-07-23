"""
Import OpenStreetMap construction project candidates into SQLite.
"""

from __future__ import annotations

import sys

from construction_intelligence.core.import_run import (
    ImportRun,
)
from construction_intelligence.database.schema.create_tables import (
    create_tables,
)
from construction_intelligence.database.sqlite import Database
from construction_intelligence.ingestion.pipeline import (
    build_candidates_from_pbf,
)
from construction_intelligence.repositories.sqlite.sqlite_evidence_evaluation_repository import (
    SQLiteEvidenceEvaluationRepository,
)
from construction_intelligence.repositories.sqlite.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)
from construction_intelligence.repositories.sqlite.sqlite_import_run_repository import (
    SQLiteImportRunRepository,
)
from construction_intelligence.repositories.sqlite.sqlite_project_repository import (
    SQLiteProjectRepository,
)
from construction_intelligence.services.evidence_evaluation_service import (
    EvidenceEvaluationService,
)
from construction_intelligence.services.evidence_service import (
    EvidenceService,
)
from construction_intelligence.services.project_service import (
    ProjectService,
)
from construction_intelligence.workflows.project_import_workflow import (
    ProjectImportWorkflow,
)


def main() -> None:
    """Run OSM construction project import."""

    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/import_osm_projects.py <osm.pbf>"
        )
        sys.exit(1)

    pbf_path = sys.argv[1]

    database = Database()

    try:
        #
        # Ensure database exists.
        #
        create_tables(database)

        #
        # Build repositories.
        #
        project_repository = SQLiteProjectRepository(
            database
        )

        evidence_repository = SQLiteEvidenceRepository(
            database
        )

        evidence_evaluation_repository = (
            SQLiteEvidenceEvaluationRepository(
                database
            )
        )

        import_run_repository = SQLiteImportRunRepository(
            database
        )

        #
        # Create import run record.
        #
        import_run = ImportRun(
            source_file=pbf_path,
        )

        import_run_repository.add(
            import_run
        )

        #
        # Build services.
        #
        project_service = ProjectService(
            project_repository
        )

        evidence_service = EvidenceService(
            evidence_repository
        )

        evidence_evaluation_service = (
            EvidenceEvaluationService(
                repository=evidence_evaluation_repository,
            )
        )

        #
        # Build workflow.
        #
        workflow = ProjectImportWorkflow(
            project_service,
            evidence_service,
            evidence_evaluation_service,
        )

        #
        # Extract candidates.
        #
        print(
            "Building construction candidates..."
        )

        candidates = build_candidates_from_pbf(
            pbf_path
        )

        print(
            f"Found {len(candidates)} candidates."
        )

        #
        # Import.
        #
        summary = workflow.import_candidates(
            candidates
        )

        #
        # Update import run record.
        #
        import_run.candidates_processed = (
            summary.candidates_processed
        )

        import_run.projects_created = (
            summary.projects_created
        )

        import_run.projects_updated = (
            summary.projects_updated
        )

        import_run.evidence_created = (
            summary.evidence_created
        )

        import_run.evidence_reused = (
            summary.evidence_reused
        )

        import_run.projects_skipped = (
            summary.projects_skipped
        )

        import_run.failures = list(
            summary.failures
        )

        import_run.elapsed_seconds = (
            summary.elapsed_seconds
        )

        import_run.complete()

        import_run_repository.update(
            import_run
        )

        #
        # Report.
        #
        print("\nImport complete")
        print("----------------")

        print(
            f"Candidates processed: "
            f"{summary.candidates_processed}"
        )

        print(
            f"Projects created: "
            f"{summary.projects_created}"
        )

        print(
            f"Projects updated: "
            f"{summary.projects_updated}"
        )

        print(
            f"Evidence created: "
            f"{summary.evidence_created}"
        )

        print(
            f"Evidence reused: "
            f"{summary.evidence_reused}"
        )

        print(
            f"Projects skipped: "
            f"{summary.projects_skipped}"
        )

        print(
            f"Elapsed seconds: "
            f"{summary.elapsed_seconds:.2f}"
        )

        if summary.warnings:
            print("\nWarnings:")

            for warning in summary.warnings:
                print(
                    f"- {warning}"
                )

        if summary.failures:
            print("\nFailures:")

            for failure in summary.failures:
                print(
                    f"- {failure}"
                )

    finally:
        database.close()


if __name__ == "__main__":
    main()