"""Tests for Manifold Learning module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.manifold_learning import isomap, LLE, compute_geodesic_distances
import math


class TestIsomap:
    """Tests for Isomap algorithm."""
    
    def test_isomap_basic(self):
        """Test Isomap on simple data."""
        # Simple 2D data points
        data = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        
        embedded = isomap(data, n_components=2, k=3)
        
        assert len(embedded) == 4
        assert all(len(point) == 2 for point in embedded)
    
    def test_isomap_single_point(self):
        """Test Isomap with single point."""
        data = [[1.0, 2.0]]
        
        embedded = isomap(data, n_components=1, k=1)
        
        assert len(embedded) == 1
    
    def test_isomap_dimension_reduction(self):
        """Test Isomap reduces dimensionality correctly."""
        # 3D data
        data = [[i*0.1, i*0.2, i*0.3] for i in range(10)]
        
        embedded = isomap(data, n_components=2, k=5)
        
        assert len(embedded) == 10
        assert all(len(point) == 2 for point in embedded)


class TestLLE:
    """Tests for Locally Linear Embedding."""
    
    def test_lle_basic(self):
        """Test LLE on simple data."""
        data = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        
        # Use k=2 to avoid dimension issues
        embedded = LLE(data, n_components=2, k=2)
        
        assert len(embedded) == 4
        assert all(len(point) == 2 for point in embedded)
    
    def test_lle_empty_data(self):
        """Test LLE with empty data."""
        embedded = LLE([], n_components=2, k=2)
        
        assert embedded == []
    
    def test_lle_dimension_reduction(self):
        """Test LLE reduces dimensionality."""
        # 5D data
        data = [[float(i+j) for j in range(5)] for i in range(10)]
        
        # Use k=4 which is less than n_features=5
        embedded = LLE(data, n_components=2, k=4)
        
        assert len(embedded) == 10
        assert all(len(point) == 2 for point in embedded)


class TestGeodesicDistances:
    """Tests for geodesic distance computation."""
    
    def test_geodesic_distances(self):
        """Test computing geodesic distances."""
        data = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [3.0, 0.0]]
        
        distances = compute_geodesic_distances(data, k=2)
        
        assert len(distances) == 4
        assert all(len(row) == 4 for row in distances)
    
    def test_geodesic_self_distance(self):
        """Test that self-distance is zero."""
        data = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]]
        
        distances = compute_geodesic_distances(data, k=2)
        
        for i in range(len(data)):
            assert abs(distances[i][i]) < 1e-6