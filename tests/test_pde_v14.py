import pytest
from lean4py.pde import solve_laplace_equation, solve_poisson_equation


class TestLaplaceEquation:
    def test_zero_solution(self):
        """Laplace equation with zero boundary -> zero solution."""
        u = solve_laplace_equation(Lx=1.0, Ly=1.0, nx=20, ny=20, max_iter=100)
        for row in u:
            for val in row:
                assert abs(val) < 0.1  # Should be near 0


class TestPoissonEquation:
    def test_constant_source(self):
        """Poisson with constant source."""
        source = lambda x, y: 1.0
        u = solve_poisson_equation(
            Lx=1.0, Ly=1.0, source=source, nx=20, ny=20, max_iter=100)
        # Solution should be positive
        for row in u:
            for val in row:
                assert val >= -0.1  # Should be non-negative
