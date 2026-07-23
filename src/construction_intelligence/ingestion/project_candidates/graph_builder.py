from collections import defaultdict
from itertools import combinations

import networkx as nx

from construction_intelligence.ingestion.osm.extractor import ExtractedWay


def build_way_graph(ways: list[ExtractedWay]) -> nx.Graph:
    """
    Build a graph where each node represents a construction way.

    Two ways are connected if they share ANY OSM node.

    This correctly handles:
        - road splits
        - road merges
        - T-intersections
        - ramps
        - divided highways
        - roundabouts
        - complex interchanges
    """

    graph = nx.Graph()

    # Maps OSM node ID -> list of construction way IDs
    node_index: dict[int, list[int]] = defaultdict(list)

    # Add every construction way as a graph node
    for way in ways:
        graph.add_node(way.osm_id)

        # Skip malformed ways
        if len(way.node_ids) < 2:
            continue

        # Index every node in the way
        for node_id in way.node_ids:
            node_index[node_id].append(way.osm_id)

    # Connect ways that share one or more nodes
    for connected_way_ids in node_index.values():

        # Remove duplicate way IDs while preserving order
        unique_way_ids = list(dict.fromkeys(connected_way_ids))

        if len(unique_way_ids) < 2:
            continue

        graph.add_edges_from(combinations(unique_way_ids, 2))

    return graph


def connected_components(graph: nx.Graph) -> list[set[int]]:
    """
    Return the connected components of the construction graph.

    Each connected component represents one candidate
    construction project.
    """
    return list(nx.connected_components(graph))