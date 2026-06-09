"""TSP solving algorithms and path utilities."""

import networkx as nx


def nearest_neighbor_path(G, start_node):
    """Compute an approximate TSP tour using the nearest neighbor heuristic.

    Starting from start_node, greedily visit the nearest unvisited neighbor
    until all nodes are visited, then return to start.

    Args:
        G: A weighted NetworkX Graph.
        start_node: The node to start and end the tour from.

    Returns:
        A list of nodes representing the tour (start_node appears at both ends).
    """
    path = [start_node]
    visited = {node: False for node in G.nodes}
    visited[start_node] = True

    while len(path) < G.number_of_nodes():
        current_node = path[-1]
        min_dist = float('inf')
        next_node = None
        for neighbor in G.neighbors(current_node):
            if not visited[neighbor] and G[current_node][neighbor]['weight'] < min_dist:
                min_dist = G[current_node][neighbor]['weight']
                next_node = neighbor
        path.append(next_node)
        visited[next_node] = True

    path.append(start_node)
    return path


def trim_path_to_destination(path, destination):
    """Trim a full TSP tour to stop at a given destination city.

    Args:
        path: A list of nodes representing the full tour.
        destination: The city to stop at.

    Returns:
        A sublist of path from the start up to and including the destination.

    Raises:
        ValueError: If destination is not found in the path.
    """
    if destination not in path:
        raise ValueError(f"Destination '{destination}' not found in path.")
    dest_index = path.index(destination)
    return path[:dest_index + 1]


def calculate_path_distance(G, path):
    """Calculate the total distance (sum of edge weights) along a path.

    Args:
        G: A weighted NetworkX Graph.
        path: A list of nodes forming a connected path in G.

    Returns:
        The total weight/distance of the path.
    """
    return sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
