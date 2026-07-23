"""
Construction Intelligence ingestion pipeline.
"""

from __future__ import annotations

from construction_intelligence.ingestion.osm.extractor import (
    ExtractedWay,
    OSMConstructionExtractor,
)

from construction_intelligence.ingestion.project_candidates.candidate_builder import (
    build_candidates,
)

from construction_intelligence.ingestion.project_candidates.graph_builder import (
    build_way_graph,
    connected_components,
)

from construction_intelligence.models.construction_project_candidate import (
    ConstructionProjectCandidate,
)


def extract_candidates(
    pbf_path: str,
) -> tuple[
    list[ExtractedWay],
    list[ConstructionProjectCandidate],
]:
    """
    Execute the ingestion pipeline.

    Returns both the extracted OSM ways and the resulting
    ConstructionProjectCandidate objects.
    """

    extractor = OSMConstructionExtractor()

    extracted_ways = extractor.extract(pbf_path)

    graph = build_way_graph(extracted_ways)

    components = connected_components(graph)

    candidates = build_candidates(
        extracted_ways,
        components,
    )

    return extracted_ways, candidates


def build_candidates_from_pbf(
    pbf_path: str,
) -> list[ConstructionProjectCandidate]:
    """
    Execute the ingestion pipeline and return construction
    project candidates.
    """

    _, candidates = extract_candidates(pbf_path)

    return candidates