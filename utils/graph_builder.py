"""Utilities for constructing weighted city graphs."""

import networkx as nx

from config.cities import CITY_POSITIONS, CITY_EDGES


def build_city_graph(positions=None, edges=None):
    """Build a weighted NetworkX graph from city positions and edges.

    Args:
        positions: Dict mapping city name to (x, y) tuple. Defaults to CITY_POSITIONS.
        edges: List of (city_a, city_b, weight) tuples. Defaults to CITY_EDGES.

    Returns:
        A NetworkX Graph with position attributes on nodes and weight attributes on edges.
    """
    if positions is None:
        positions = CITY_POSITIONS
    if edges is None:
        edges = CITY_EDGES

    G = nx.Graph()

    for city, pos in positions.items():
        G.add_node(city, pos=pos)

    for city_a, city_b, weight in edges:
        G.add_edge(city_a, city_b, weight=weight)

    return G
