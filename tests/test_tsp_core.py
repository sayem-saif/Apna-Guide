"""Unit tests for tsp_core module."""

import networkx as nx
import pytest

from tsp_core import (
    VALID_CITIES,
    CITY_POSITIONS,
    EDGES,
    DEFAULT_START,
    build_city_graph,
    nearest_neighbor_path,
    trim_path_to_destination,
    calculate_path_distance,
    validate_city,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_valid_cities_contains_expected(self):
        assert set(VALID_CITIES) == {'Mumbai', 'Pune', 'Thane', 'Delhi'}

    def test_city_positions_keys_match_valid_cities(self):
        assert set(CITY_POSITIONS.keys()) == set(VALID_CITIES)

    def test_positions_are_two_tuples(self):
        for city, pos in CITY_POSITIONS.items():
            assert len(pos) == 2, f"{city} position should be a 2-tuple"

    def test_edges_reference_known_cities(self):
        for u, v, _ in EDGES:
            assert u in VALID_CITIES, f"Edge source {u} not in VALID_CITIES"
            assert v in VALID_CITIES, f"Edge target {v} not in VALID_CITIES"

    def test_edge_weights_positive(self):
        for u, v, w in EDGES:
            assert w > 0, f"Edge ({u}, {v}) weight should be positive"

    def test_default_start_is_valid(self):
        assert DEFAULT_START in VALID_CITIES


# ---------------------------------------------------------------------------
# build_city_graph
# ---------------------------------------------------------------------------

class TestBuildCityGraph:
    def test_returns_graph(self):
        G = build_city_graph()
        assert isinstance(G, nx.Graph)

    def test_node_count(self):
        G = build_city_graph()
        assert G.number_of_nodes() == len(VALID_CITIES)

    def test_edge_count(self):
        G = build_city_graph()
        assert G.number_of_edges() == len(EDGES)

    def test_nodes_have_pos_attribute(self):
        G = build_city_graph()
        for node in G.nodes:
            assert 'pos' in G.nodes[node]

    def test_edges_have_weight_attribute(self):
        G = build_city_graph()
        for u, v in G.edges:
            assert 'weight' in G[u][v]

    def test_specific_edge_weight(self):
        G = build_city_graph()
        assert G['Mumbai']['Pune']['weight'] == 120
        assert G['Mumbai']['Thane']['weight'] == 15
        assert G['Mumbai']['Delhi']['weight'] == 400

    def test_graph_is_undirected(self):
        G = build_city_graph()
        assert not G.is_directed()


# ---------------------------------------------------------------------------
# nearest_neighbor_path
# ---------------------------------------------------------------------------

class TestNearestNeighborPath:
    def test_path_starts_and_ends_at_start(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, 'Mumbai')
        assert path[0] == 'Mumbai'
        assert path[-1] == 'Mumbai'

    def test_path_visits_all_nodes(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, 'Mumbai')
        visited = set(path[:-1])  # exclude closing node
        assert visited == set(G.nodes)

    def test_path_length(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, 'Mumbai')
        assert len(path) == G.number_of_nodes() + 1

    def test_greedy_first_step_is_nearest(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, 'Mumbai')
        # Nearest to Mumbai is Thane (15 km)
        assert path[1] == 'Thane'

    def test_no_duplicate_internal_visits(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, 'Mumbai')
        internal = path[:-1]
        assert len(internal) == len(set(internal))

    def test_different_start_node(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, 'Delhi')
        assert path[0] == 'Delhi'
        assert path[-1] == 'Delhi'
        assert len(path) == G.number_of_nodes() + 1

    def test_small_graph(self):
        G = nx.Graph()
        G.add_node('A')
        G.add_node('B')
        G.add_edge('A', 'B', weight=10)
        path = nearest_neighbor_path(G, 'A')
        assert path == ['A', 'B', 'A']


# ---------------------------------------------------------------------------
# trim_path_to_destination
# ---------------------------------------------------------------------------

class TestTrimPathToDestination:
    def test_trim_to_middle(self):
        path = ['Mumbai', 'Thane', 'Pune', 'Delhi', 'Mumbai']
        assert trim_path_to_destination(path, 'Pune') == ['Mumbai', 'Thane', 'Pune']

    def test_trim_to_first(self):
        path = ['Mumbai', 'Thane', 'Pune', 'Delhi', 'Mumbai']
        assert trim_path_to_destination(path, 'Mumbai') == ['Mumbai']

    def test_trim_to_last_before_return(self):
        path = ['Mumbai', 'Thane', 'Pune', 'Delhi', 'Mumbai']
        assert trim_path_to_destination(path, 'Delhi') == ['Mumbai', 'Thane', 'Pune', 'Delhi']

    def test_trim_to_second(self):
        path = ['Mumbai', 'Thane', 'Pune', 'Delhi', 'Mumbai']
        assert trim_path_to_destination(path, 'Thane') == ['Mumbai', 'Thane']

    def test_raises_on_missing_destination(self):
        path = ['Mumbai', 'Thane', 'Pune']
        with pytest.raises(ValueError):
            trim_path_to_destination(path, 'Kolkata')


# ---------------------------------------------------------------------------
# calculate_path_distance
# ---------------------------------------------------------------------------

class TestCalculatePathDistance:
    def test_single_edge(self):
        G = build_city_graph()
        assert calculate_path_distance(G, ['Mumbai', 'Pune']) == 120

    def test_two_edges(self):
        G = build_city_graph()
        assert calculate_path_distance(G, ['Mumbai', 'Thane', 'Pune']) == 15 + 90

    def test_full_path(self):
        G = build_city_graph()
        path = ['Mumbai', 'Thane', 'Pune', 'Delhi']
        expected = 15 + 90 + 250
        assert calculate_path_distance(G, path) == expected

    def test_single_node_distance_is_zero(self):
        G = build_city_graph()
        assert calculate_path_distance(G, ['Mumbai']) == 0

    def test_round_trip(self):
        G = build_city_graph()
        path = ['Mumbai', 'Thane', 'Mumbai']
        assert calculate_path_distance(G, path) == 15 + 15


# ---------------------------------------------------------------------------
# validate_city
# ---------------------------------------------------------------------------

class TestValidateCity:
    @pytest.mark.parametrize("city", VALID_CITIES)
    def test_valid(self, city):
        assert validate_city(city) is True

    @pytest.mark.parametrize("city", ['Kolkata', 'Chennai', '', 'mumbai', 'MUMBAI'])
    def test_invalid(self, city):
        assert validate_city(city) is False


# ---------------------------------------------------------------------------
# Integration: full pipeline
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_pipeline_pune(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, DEFAULT_START)
        trimmed = trim_path_to_destination(path, 'Pune')
        dist = calculate_path_distance(G, trimmed)
        assert trimmed[0] == 'Mumbai'
        assert trimmed[-1] == 'Pune'
        assert dist > 0

    def test_full_pipeline_thane(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, DEFAULT_START)
        trimmed = trim_path_to_destination(path, 'Thane')
        dist = calculate_path_distance(G, trimmed)
        assert trimmed == ['Mumbai', 'Thane']
        assert dist == 15

    def test_full_pipeline_delhi(self):
        G = build_city_graph()
        path = nearest_neighbor_path(G, DEFAULT_START)
        trimmed = trim_path_to_destination(path, 'Delhi')
        dist = calculate_path_distance(G, trimmed)
        assert trimmed[-1] == 'Delhi'
        assert dist > 0
