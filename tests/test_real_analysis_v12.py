import pytest
import math
from lean4py.real_analysis import adaptive_simpson


class TestAdaptiveSimpson:
    def test_linear(self):
        """Integral of x from 0 to 1 = 0.5."""
        f = lambda x: x
        result = adaptive_simpson(f, 0.0, 1.0, tol=1e-6)
        assert abs(result - 0.5) < 1e-4

    def test_quadratic(self):
        """Integral of x^2 from 0 to 1 = 1/3."""
        f = lambda x: x**2
        result = adaptive_simpson(f, 0.0, 1.0, tol=1e-6)
        assert abs(result - 1.0/3.0) < 1e-4

    def test_constant(self):
        """Integral of 5 from 0 to 2 = 10."""
        f = lambda x: 5
        result = adaptive_simpson(f, 0.0, 2.0, tol=1e-6)
        assert abs(result - 10.0) < 1e-4

    def test_sin(self):
        """Integral of sin(x) from 0 to pi = 2."""
        f = lambda x: math.sin(x)
        result = adaptive_simpson(f, 0.0, math.pi, tol=1e-6)
        assert abs(result - 2.0) < 1e-3
