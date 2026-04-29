"""Tests for Newton-Raphson and Levenberg-Marquardt."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.optimization import newton_raphson, levenberg_marquardt
import math


class TestNewtonRaphson:
    """Tests for Newton-Raphson method."""
    
    def test_1d_minimum(self):
        """Test Newton-Raphson on 1D function."""
        f = lambda x: (x[0] - 2.0)**2
        x0 = [0.0]
        x_opt, f_opt = newton_raphson(f, x0, max_iter=50)
        
        assert abs(x_opt[0] - 2.0) < 0.5
        assert f_opt < 1.0
    
    def test_1d_convergence(self):
        """Test Newton-Raphson convergence on 1D."""
        f = lambda x: (x[0] - 3.0)**2
        x0 = [0.0]
        x_opt, f_opt = newton_raphson(f, x0, max_iter=100)
        
        assert f_opt < f(x0)


class TestLevenbergMarquardt:
    """Tests for Levenberg-Marquardt algorithm."""
    
    def test_simple_regression(self):
        """Test LM on simple regression."""
        def residuals(params):
            return [params[0] * 1.0 - 1.0]
        
        x0 = [0.0]
        x_opt, r_opt = levenberg_marquardt(residuals, x0, max_iter=100)
        
        assert len(x_opt) == 1
        assert abs(x_opt[0] - 1.0) < 0.5
    
    def test_residual_reduction(self):
        """Test that LM reduces residual sum of squares."""
        def residuals(params):
            return [params[0] * 1.0 - 1.0]
        
        x0 = [0.0]
        x_opt, r_opt = levenberg_marquardt(residuals, x0, max_iter=50)
        
        initial_error = sum(r**2 for r in residuals(x0))
        final_error = sum(r**2 for r in r_opt)
        
        assert final_error < initial_error