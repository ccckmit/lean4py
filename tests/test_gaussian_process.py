"""Tests for Gaussian Process module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.gaussian_process import (
    GaussianProcessRegressor, rbf_kernel, predict_gp
)
import math


class TestRBFKernel:
    """Tests for RBF kernel."""
    
    def test_same_points(self):
        """Test kernel for identical points."""
        x = [1.0, 2.0]
        k = rbf_kernel(x, x)
        assert abs(k - 1.0) < 0.01  # Should be close to 1
    
    def test_different_points(self):
        """Test kernel for different points."""
        x1 = [0.0, 0.0]
        x2 = [1.0, 1.0]
        k = rbf_kernel(x1, x2)
        assert 0 < k < 1  # Should be between 0 and 1
    
    def test_length_scale(self):
        """Test kernel with different length scales."""
        x1 = [0.0]
        x2 = [1.0]
        
        k_small = rbf_kernel(x1, x2, length_scale=0.1)
        k_large = rbf_kernel(x1, x2, length_scale=10.0)
        
        assert k_small < k_large  # Smaller length scale = lower similarity


class TestGaussianProcessRegressor:
    """Tests for Gaussian Process Regressor."""
    
    def test_initialization(self):
        """Test GP initializes correctly."""
        gp = GaussianProcessRegressor()
        assert gp.kernel is not None
        assert gp.noise == 1e-8
    
    def test_fit_predict(self):
        """Test fitting and predicting."""
        X_train = [[0.0], [1.0], [2.0]]
        y_train = [0.0, 1.0, 2.0]
        
        gp = GaussianProcessRegressor()
        gp.fit(X_train, y_train)
        
        X_test = [[0.5], [1.5]]
        means, variances = gp.predict(X_test)
        
        assert len(means) == 2
        assert len(variances) == 2
        # Means should be reasonable (between min and max of training)
        assert min(y_train) - 1 <= means[0] <= max(y_train) + 1
    
    def test_empty_fit(self):
        """Test GP with empty training data."""
        gp = GaussianProcessRegressor()
        means, variances = gp.predict([[1.0]])
        
        assert means == []
        assert variances == []


class TestPredictGP:
    """Tests for predict_gp convenience function."""
    
    def test_predict_gp(self):
        """Test the convenience function."""
        X_train = [[0.0], [1.0]]
        y_train = [0.0, 1.0]
        X_test = [[0.5]]
        
        means, stds = predict_gp(X_train, y_train, X_test)
        
        assert len(means) == 1
        assert len(stds) == 1
        assert means[0] > 0  # Should predict something > 0
        assert stds[0] > 0  # Uncertainty should be positive
    
    def test_single_training_point(self):
        """Test GP with single training point."""
        X_train = [[0.0]]
        y_train = [1.0]
        
        gp = GaussianProcessRegressor()
        gp.fit(X_train, y_train)
        
        X_test = [[1.0]]
        means, variances = gp.predict(X_test)
        
        assert len(means) == 1
        assert len(variances) == 1