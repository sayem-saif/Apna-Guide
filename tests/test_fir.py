"""Unit tests for fir.py numpy operations."""

import numpy as np


class TestNumpyOperations:
    def test_array_creation(self):
        arr = np.array([1, 2, 3])
        assert list(arr) == [1, 2, 3]

    def test_scalar_shape(self):
        assert np.shape(2) == ()

    def test_structured_array(self):
        a = np.array(
            [(1, 2), (3, 4), (5, 6)],
            dtype=[('x', 'i4'), ('y', 'i4')],
        )
        assert a.shape == (3,)
        assert list(a['x']) == [1, 3, 5]
        assert list(a['y']) == [2, 4, 6]

    def test_structured_array_indexing(self):
        a = np.array(
            [(1, 2), (3, 4), (5, 6)],
            dtype=[('x', 'i4'), ('y', 'i4')],
        )
        assert a[0]['x'] == 1
        assert a[2]['y'] == 6
