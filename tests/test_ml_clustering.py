"""Tests for clustering algorithms (k-means)."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.ml_basics import kmeans
import math


class TestKMeans:
    """Tests for k-means clustering."""
    
    def test_simple_clusters(self):
        """Test k-means on clearly separated clusters."""
        # Two clear clusters: around (0,0) and (10,10)
        data = [
            [0.0, 0.0], [0.5, 0.5], [1.0, 1.0],  # Cluster 1
            [10.0, 10.0], [10.5, 10.5], [11.0, 11.0]  # Cluster 2
        ]
        
        centroids, labels = kmeans(data, k=2, n_init=5)
        
        assert len(centroids) == 2
        assert len(labels) == len(data)
        assert all(l in [0, 1] for l in labels)
    
    def test_perfect_separation(self):
        """Test when clusters are perfectly separated."""
        data = [[0.0], [1.0], [100.0], [101.0]]
        k = 2
        
        centroids, labels = kmeans(data, k=k, n_init=10)
        
        # First two points should be in same cluster
        assert labels[0] == labels[1]
        # Last two points should be in same cluster
        assert labels[2] == labels[3]
        # Clusters should be different
        assert labels[0] != labels[2]
    
    def test_single_cluster(self):
        """Test k=1 returns single cluster."""
        data = [[i*0.1] for i in range(10)]
        
        centroids, labels = kmeans(data, k=1)
        
        assert len(centroids) == 1
        assert all(l == 0 for l in labels)
    
    def test_empty_data(self):
        """Test with empty data."""
        centroids, labels = kmeans([], k=2)
        
        assert centroids == []
        assert labels == []
    
    def test_k_equals_n(self):
        """Test when k equals number of data points."""
        data = [[0.0], [1.0], [2.0]]
        k = 3
        
        centroids, labels = kmeans(data, k=k)
        
        assert len(centroids) == k
        assert len(labels) == len(data)
