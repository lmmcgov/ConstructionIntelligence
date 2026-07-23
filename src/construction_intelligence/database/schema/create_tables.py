"""
Creates the Construction Intelligence database schema.
"""

from construction_intelligence.database.sqlite import Database


def create_tables(database: Database) -> None:
    """Create all database tables."""

    # Enable foreign key enforcement.
    database.execute(
        "PRAGMA foreign_keys = ON;"
    )

    #
    # Projects
    #
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,

            name TEXT NOT NULL,
            description TEXT,

            status TEXT NOT NULL,
            category TEXT NOT NULL,

            origin TEXT NOT NULL,
            origin_id TEXT,

            road_name TEXT,
            road_ref TEXT,

            country TEXT,
            state TEXT,
            city TEXT,

            latitude REAL,
            longitude REAL,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            last_seen TEXT NOT NULL
        );
        """
    )

    #
    # Evidence
    #
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS evidence (
            id TEXT PRIMARY KEY,

            project_id TEXT NOT NULL,

            source TEXT NOT NULL,
            origin_id TEXT,

            title TEXT,
            url TEXT,
            content TEXT,

            confidence TEXT NOT NULL,

            metadata TEXT,

            discovered_at TEXT NOT NULL,

            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        );
        """
    )

    #
    # Import runs
    #
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS import_runs (
            id TEXT PRIMARY KEY,

            source_file TEXT NOT NULL,

            started_at TEXT NOT NULL,
            completed_at TEXT,

            candidates_processed INTEGER NOT NULL,

            projects_created INTEGER NOT NULL,
            projects_updated INTEGER NOT NULL,

            evidence_created INTEGER NOT NULL,
            evidence_reused INTEGER NOT NULL,

            projects_skipped INTEGER NOT NULL,

            failures TEXT,

            elapsed_seconds REAL NOT NULL
        );
        """
    )

    #
    # Evidence evaluations
    #
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS evidence_evaluations (
            id TEXT PRIMARY KEY,

            project_id TEXT NOT NULL,
            evidence_id TEXT NOT NULL,

            match_score REAL NOT NULL,
            quality_score REAL NOT NULL,
            overall_score REAL NOT NULL,

            status TEXT NOT NULL,

            reasons TEXT,

            evaluated_at TEXT NOT NULL,

            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE,

            FOREIGN KEY (evidence_id)
                REFERENCES evidence(id)
                ON DELETE CASCADE
        );
        """
    )

    #
    # Evidence resources
    #
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS evidence_resources (
            id TEXT PRIMARY KEY,

            evaluation_id TEXT NOT NULL,

            url TEXT NOT NULL,

            title TEXT,

            source_name TEXT,

            resource_type TEXT,

            excerpt TEXT,

            FOREIGN KEY (evaluation_id)
                REFERENCES evidence_evaluations(id)
                ON DELETE CASCADE
        );
        """
    )

    #
    # Project indexes
    #
    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_projects_origin
        ON projects(origin, origin_id);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_projects_country
        ON projects(country);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_projects_city
        ON projects(city);
        """
    )

    #
    # Evidence indexes
    #
    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_project_id
        ON evidence(project_id);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_origin
        ON evidence(source, origin_id);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_source
        ON evidence(source);
        """
    )

    #
    # Import run indexes
    #
    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_import_runs_source_file
        ON import_runs(source_file);
        """
    )

    #
    # Evidence evaluation indexes
    #
    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_evaluations_project_id
        ON evidence_evaluations(project_id);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_evaluations_evidence_id
        ON evidence_evaluations(evidence_id);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_evaluations_score
        ON evidence_evaluations(overall_score);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_evaluations_status
        ON evidence_evaluations(status);
        """
    )

    #
    # Evidence resource indexes
    #
    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_resources_evaluation_id
        ON evidence_resources(evaluation_id);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_resources_source
        ON evidence_resources(source_name);
        """
    )

    database.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_evidence_resources_url
        ON evidence_resources(url);
        """
    )