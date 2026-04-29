"""Tests for PCA (Principal Component Analysis)."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.linear_algebra import pca, compute_covariance_matrix
import math


class TestPCA:
    """Tests for PCA implementation."""
    
    def test_simple_2d_data(self):
        """Test PCA on simple 2D data."""
        # Data along line y=x
        data = [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
        
        transformed, variance, components = pca(data, n_components=2)
        
        assert len(transformed) == 4
        assert len(variance) == 2
        assert len(components) == 2
        # All variance should be in first component
        assert variance[0] > variance[1]
    
    def test_dimensionality_reduction(self):
        """Test reducing from 3D to 2D."""
        data = [
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [3.0, 0.0, 0.0]
        ]
        
        transformed, _, _ = pca(data, n_components=2)
        
        assert len(transformed[0]) == 2  # 2 components
        assert len(transformed) == 3
    
    def test_empty_data(self):
        """Test PCA with empty data."""
        transformed, variance, components = pca([], n_components=2)
        
        assert transformed == []
        assert variance == []
        assert components == []
    
    def test_single_component(self):
        """Test requesting single component."""
        data = [[i*1.0, i*1.0] for i in range(10)]
        
        transformed, variance, components = pca(data, n_components=1)
        
        assert len(transformed[0]) == 1
        assert len(variance) == 1
        assert len(components) == 1


class TestCovarianceMatrix:
    """Tests for covariance matrix computation."""
    
    def test_identity_covariance(self):
        """Test covariance of uncorrelated data."""
        data = [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0]
        ]
        
        cov = compute_covariance_matrix(data)
        
        assert len(cov) == 2
        assert len(cov[0]) == 2
        # Off-diagonal should be ~0 (uncorrelated)
        assert abs(cov[0][1]) < 0.1
    
    def test_perfect_correlation(self):
        """Test covariance of perfectly correlated data."""
        data = [[i*1.0, i*1.0] for i in range(10)]
        
        cov = compute_covariance_matrix(data)
        
        # Diagonal elements should be positive
        assert cov[0][0] > 0
        assert cov[1][1] > 0
        # Off-diagonal should equal diagonal (perfect correlation)
        assert abs(cov[0][1] - cov[0][0]) < 0.1
