import pytest
import math
from lean4py.pde import solve_heat_equation, solve_wave_equation


class TestHeatEquation:
    def test_zero_initial(self):
        """Zero initial condition stays zero."""
        u0 = lambda x: 0.0
        x, u = solve_heat_equation(L=1.0, T=0.1, u0=u0, nx=20, nt=50)
        for val in u:
            assert abs(val) < 1e-10

    def test_constant_initial(self):
        """Constant initial condition."""
        u0 = lambda x: 5.0
        x, u = solve_heat_equation(L=1.0, T=0.1, u0=u0, nx=20, nt=50)
        for val in u:
            assert abs(val - 5.0) < 0.1


class TestWaveEquation:
    def test_zero_initial(self):
        """Zero initial conditions."""
        u0 = lambda x: 0.0
        v0 = lambda x: 0.0
        x, u = solve_wave_equation(L=1.0, T=0.1, u0=u0, v0=v0, nx=20, nt=50)
        for val in u:
            assert abs(val) < 1e-10
