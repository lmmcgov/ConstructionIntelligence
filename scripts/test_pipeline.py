"""
Test the Construction Intelligence ingestion pipeline.

Usage:
    python scripts/test_pipeline.py data/colorado.osm.pbf
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from construction_intelligence.ingestion import (
    build_candidates_from_pbf,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test the Construction Intelligence ingestion pipeline."
    )

    parser.add_argument(
        "pbf",
        help="Path to an OSM PBF file.",
    )

    args = parser.parse_args()

    pbf = Path(args.pbf)

    if not pbf.exists():
        raise FileNotFoundError(
            f"PBF not found: {pbf}"
        )

    print("=" * 80)
    print("Construction Intelligence Pipeline Test")
    print("=" * 80)
    print(f"PBF: {pbf}")
    print()

    start = time.perf_counter()

    candidates = build_candidates_from_pbf(str(pbf))

    elapsed = time.perf_counter() - start

    print(f"Pipeline completed in {elapsed:.2f} seconds")
    print(f"Construction projects found: {len(candidates)}")

    if not candidates:
        print("\nNo construction projects found.")
        return

    print("\nFirst 10 projects:\n")

    for i, project in enumerate(candidates[:10], start=1):

        print("-" * 80)
        print(f"Project {i}")
        print("-" * 80)

        print(f"ID: {project.id}")
        print(f"Origin ID: {project.origin_id}")

        print(
            f"Connected Ways: "
            f"{project.connected_way_count}"
        )

        print(
            f"Length (m): "
            f"{project.length_m:,.1f}"
        )

        print(
            f"Construction Type: "
            f"{project.construction_type}"
        )

        print(
            f"Highway Type: "
            f"{project.highway_type}"
        )

        print(
            f"Road Names: "
            f"{project.road_names}"
        )

        print(
            f"Route Numbers: "
            f"{project.route_numbers}"
        )

        print(
            f"Bounding Box: "
            f"{project.bbox}"
        )

        print(
            f"Tag Count: "
            f"{len(project.tags)}"
        )

    print("\nDone.")


if __name__ == "__main__":
    main()