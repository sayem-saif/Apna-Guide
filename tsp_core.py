"""Core TSP (Traveling Salesman Problem) logic for the Apna Guide application.

Provides graph construction, nearest-neighbor heuristic, path trimming,
distance calculation, and city validation -- all independent of the GUI.
"""

import networkx as nx


VALID_CITIES = ['Mumbai', 'Pune', 'Thane', 'Delhi']

CITY_POSITIONS = {
    'Mumbai': (0, 0),
    'Pune': (1, 2),
    'Thane': (3, 1),
    'Delhi': (2, 3),
}

EDGES = [
    ('Mumbai', 'Pune', 120),
    ('Mumbai', 'Thane', 15),
    ('Mumbai', 'Delhi', 400),
    ('Pune', 'Thane', 90),
    ('Pune', 'Delhi', 250),
    ('Thane', 'Delhi', 305),
]

DEFAULT_START = 'Mumbai'


def build_city_graph():
    """Build and return a networkx Graph with predefined cities and distances."""
    G = nx.Graph()
    for city, pos in CITY_POSITIONS.items():
        G.add_node(city, pos=pos)
    for u, v, w in EDGES:
        G.add_edge(u, v, weight=w)
    return G


def nearest_neighbor_path(graph, start_node):
    """Compute a TSP tour using the nearest-neighbor heuristic.

    Returns the full tour as a list of nodes ending back at *start_node*.
    """
    path = [start_node]
    visited = {node: False for node in graph.nodes}
    visited[start_node] = True

    while len(path) < graph.number_of_nodes():
        current_node = path[-1]
        min_dist = float('inf')
        next_node = None
        for neighbor in graph.neighbors(current_node):
            if not visited[neighbor] and graph[current_node][neighbor]['weight'] < min_dist:
                min_dist = graph[current_node][neighbor]['weight']
                next_node = neighbor
        path.append(next_node)
        visited[next_node] = True

    path.append(start_node)
    return path


def trim_path_to_destination(path, destination):
    """Trim *path* so it stops at *destination* (inclusive)."""
    dest_index = path.index(destination)
    return path[:dest_index + 1]


def calculate_path_distance(graph, path):
    """Return the total weight along *path* in *graph*."""
    return sum(
        graph[path[i]][path[i + 1]]['weight']
        for i in range(len(path) - 1)
    )


def validate_city(city_name):
    """Return ``True`` if *city_name* is in the known city list."""
    return city_name in VALID_CITIES
