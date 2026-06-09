"""City data configuration for Apna Guide TSP solver."""

# Node definitions: city name -> (x, y) position for graph layout
CITY_POSITIONS = {
    'Mumbai': (0, 0),
    'Pune': (1, 2),
    'Thane': (3, 1),
    'Delhi': (2, 3),
}

# Edge definitions: (city_a, city_b, distance_km)
CITY_EDGES = [
    ('Mumbai', 'Pune', 120),
    ('Mumbai', 'Thane', 15),
    ('Mumbai', 'Delhi', 400),
    ('Pune', 'Thane', 90),
    ('Pune', 'Delhi', 250),
    ('Thane', 'Delhi', 305),
]

# Valid destination cities that users can query
VALID_CITIES = list(CITY_POSITIONS.keys())

# Default starting city for TSP path
START_CITY = 'Mumbai'
