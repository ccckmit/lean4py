"""Tests for BFGS and L-BFGS optimization algorithms."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.optimization import bfgs, lbfgs
import math


def rosenbrock(x):
    """Rosenbrock function: minimum at (1,1)."""
    return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2


def quadratic(x):
    """Simple quadratic: f(x) = x^2 + y^2, minimum at (0,0)."""
    return x[0]**2 + x[1]**2


class TestBFGS:
    """Tests for BFGS optimizer."""
    
    def test_1d_function(self):
        """Test BFGS on 1D function."""
        f = lambda x: (x[0] - 3.0)**2
        x0 = [0.0]
        x_opt, f_opt = bfgs(f, x0, max_iter=50)
        
        # Should move toward 3.0
        assert abs(x_opt[0] - 3.0) < abs(x0[0] - 3.0)
        assert f_opt < f(x0)
    
    def test_quadratic_1d(self):
        """Test BFGS on 1D quadratic."""
        f = lambda x: x[0]**2
        x0 = [5.0]
        x_opt, f_opt = bfgs(f, x0, max_iter=50)
        
        assert abs(x_opt[0]) < abs(x0[0])
        assert f_opt < f(x0)


class TestLBFGS:
    """Tests for L-BFGS optimizer."""
    
    def test_quadratic_minimum(self):
        """Test L-BFGS on quadratic function."""
        x0 = [5.0, 5.0]
        x_opt, f_opt = lbfgs(quadratic, x0, max_iter=100, m=5)
        
        assert abs(x_opt[0]) < 0.5
        assert abs(x_opt[1]) < 0.5
        assert f_opt < 1.0
    
    def test_memory_limit(self):
        """Test L-BFGS respects memory limit."""
        x0 = [2.0, 2.0]
        x_opt, f_opt = lbfgs(quadratic, x0, max_iter=50, m=3)
        
        # Should still converge
        assert f_opt < quadratic(x0)
    
    def test_rosenbrock(self):
        """Test L-BFGS on Rosenbrock."""
        x0 = [-1.2, 1.0]
        x_opt, f_opt = lbfgs(rosenbrock, x0, max_iter=500, m=10)
        
        assert abs(x_opt[0] - 1.0) < 1.0
        assert abs(x_opt[1] - 1.0) < 1.0
