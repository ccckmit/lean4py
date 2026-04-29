import pytest
import math
from lean4py.optimization import newton_method


class TestNewtonMethod:
    def test_minimize_x_squared(self):
        """f(x) = x^2, minimum at x=0."""
        f = lambda x: x ** 2
        x_opt, f_opt = newton_method(f, x0=5.0, max_iter=10)
        assert abs(x_opt) < 0.01
        assert abs(f_opt) < 0.0001

    def test_minimize_quadratic(self):
        """f(x) = (x-3)^2 + 2, minimum at x=3."""
        f = lambda x: (x - 3) ** 2 + 2
        x_opt, f_opt = newton_method(f, x0=0.0, max_iter=10)
        assert abs(x_opt - 3.0) < 0.01
        assert abs(f_opt - 2.0) < 0.01

    def test_convergence(self):
        """Should converge quickly for convex functions."""
        f = lambda x: x ** 2 + 2*x + 1
        x_opt, f_opt = newton_method(f, x0=10.0, tol=1e-4)
        assert abs(x_opt + 1.0) < 0.01  # minimum at x = -1
