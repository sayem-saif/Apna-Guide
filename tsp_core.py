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
    """
    Constructs the predefined city graph used for TSP operations.
    
    The returned graph contains a node for each city with a `pos` attribute holding the (x, y) coordinates, and undirected edges carrying a `weight` attribute that represents the distance between cities.
    
    Returns:
        networkx.Graph: Graph with city nodes and weighted edges.
    """
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
    """
    Return the prefix of the given path that ends at `destination`.
    
    Parameters:
        path (Sequence): Ordered sequence of nodes.
        destination: Node value that must appear in `path`; trimming stops at its first occurrence.
    
    Returns:
        list: A list containing the elements of `path` from the start up to and including `destination`.
    
    Raises:
        ValueError: If `destination` is not present in `path`.
    """
    dest_index = path.index(destination)
    return path[:dest_index + 1]


def calculate_path_distance(graph, path):
    """
    Compute the total weight of the given node sequence in the graph.
    
    Parameters:
        graph (networkx.Graph): Graph whose edges store a numeric `weight` attribute.
        path (Sequence): Ordered sequence of node identifiers representing the tour or route.
    
    Returns:
        total_distance (float|int): Sum of the edge weights for each consecutive pair in `path`.
    """
    return sum(
        graph[path[i]][path[i + 1]]['weight']
        for i in range(len(path) - 1)
    )


def validate_city(city_name):
    """
    Check whether a city name is in the list of known cities.
    
    Parameters:
        city_name (str): Name of the city to validate.
    
    Returns:
        `true` if the city is in the known list, `false` otherwise.
    """
    return city_name in VALID_CITIES
