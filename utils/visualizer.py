"""Graph visualization utilities for Apna Guide."""

import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(G):
    """Draw the full city graph with labeled nodes and weighted edges.

    Args:
        G: A NetworkX Graph with 'pos' node attributes and 'weight' edge attributes.

    Returns:
        The position dict used for layout (useful for subsequent drawing calls).
    """
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=5000, font_size=15, font_color='white')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)

    return pos


def highlight_path(G, pos, path, total_distance):
    """Highlight a path on an already-drawn graph and display it.

    Args:
        G: A NetworkX Graph (must already be drawn via draw_graph).
        pos: Position dict from draw_graph.
        path: List of nodes forming the path to highlight.
        total_distance: Total distance of the path (shown in title).
    """
    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    path_str = ' \u2192 '.join(path)
    plt.suptitle(f"Path: {path_str} | Distance: {total_distance} km", fontsize=10, y=0.98, x=0.02, ha='left')
    plt.subplots_adjust(top=0.75)
    plt.tight_layout()
    plt.show()
