"""Unit tests for fir.py numpy operations."""

import numpy as np


class TestNumpyOperations:
    def test_array_creation(self):
        """
        Verifies that creating a 1-D NumPy array from a Python list preserves element order and contents.
        
        Creates an array from [1, 2, 3] and asserts that converting it to a list yields [1, 2, 3].
        """
        arr = np.array([1, 2, 3])
        assert list(arr) == [1, 2, 3]

    def test_scalar_shape(self):
        assert np.shape(2) == ()

    def test_structured_array(self):
        """
        Verify creation of a structured NumPy array with two integer fields ('x' and 'y') and that field-based indexing and overall shape match expectations.
        
        Asserts that the array has shape (3,), that the 'x' field yields [1, 3, 5], and the 'y' field yields [2, 4, 6].
        """
        a = np.array(
            [(1, 2), (3, 4), (5, 6)],
            dtype=[('x', 'i4'), ('y', 'i4')],
        )
        assert a.shape == (3,)
        assert list(a['x']) == [1, 3, 5]
        assert list(a['y']) == [2, 4, 6]

    def test_structured_array_indexing(self):
        """
        Verify that structured NumPy arrays support field access by record index and field name.
        
        Asserts that the 'x' field of the first record equals 1 and the 'y' field of the third record equals 6.
        """
        a = np.array(
            [(1, 2), (3, 4), (5, 6)],
            dtype=[('x', 'i4'), ('y', 'i4')],
        )
        assert a[0]['x'] == 1
        assert a[2]['y'] == 6
