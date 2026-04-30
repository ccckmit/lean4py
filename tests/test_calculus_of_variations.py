"""Tests for calculus_of_variations module."""

import pytest
from lean4py.calculus_of_variations import (
    Functional, EulerLagrangeEquation, HamiltonPrinciple,
    Brachistochrone, IsoperimetricProblem, NoetherTheorem
)


class TestFunctional:
    """Test functionals."""

    def test_creation(self):
        L = lambda t, y, dy: y * y + dy * dy
        func = Functional(L, t_start=0.0, t_end=1.0)
        assert func.t_start == 0.0
        assert func.t_end == 1.0

    def test_evaluate(self):
        L = lambda t, y, dy: dy * dy
        func = Functional(L, t_start=0.0, t_end=1.0)
        y = lambda t: t
        dy = lambda t: 1.0
        result = func.evaluate(y, dy)
        assert result >= 0


class TestEulerLagrangeEquation:
    """Test Euler-Lagrange equation."""

    def test_euler_lagrange(self):
        L = lambda t, y, dy: dy * dy
        euler = EulerLagrangeEquation.euler_lagrange(
            L, t=0.5, y=0.5, dy=1.0,
            dL_dy=lambda t, y, dy: 0.0,
            dL_dy_prime=lambda t, y, dy: 2 * dy
        )
        assert isinstance(euler, (int, float))

    def test_is_extremal(self):
        L = lambda t, y, dy: dy * dy
        y = lambda t: t
        dy = lambda t: 1.0
        assert EulerLagrangeEquation.is_extremal(L, y, dy, lambda: 0.0) is True


class TestHamiltonPrinciple:
    """Test Hamilton's principle."""

    def test_action(self):
        L = lambda t, y, dy: dy * dy
        y = lambda t: t
        dy = lambda t: 1.0
        action = HamiltonPrinciple.action(L, y, dy, 0.0, 1.0)
        assert action >= 0

    def test_is_stationary(self):
        L = lambda t, y, dy: dy * dy
        y = lambda t: t
        dy = lambda t: 1.0
        assert HamiltonPrinciple.is_stationary(L, y, dy, 0.0, 1.0) is True


class TestBrachistochrone:
    """Test brachistochrone problem."""

    def test_time_of_descent(self):
        curve = lambda t: t * t
        time = Brachistochrone.time_of_descent(curve, y_start=1.0, y_end=0.0)
        assert time >= 0

    def test_cycloid_solution(self):
        x, y = Brachistochrone.cycloid_solution(t=1.0, a=1.0)
        assert x >= 0
        assert y >= 0


class TestIsoperimetricProblem:
    """Test isoperimetric problem."""

    def test_creation(self):
        J = lambda y: 0.0
        G = lambda y: 0.0
        prob = IsoperimetricProblem(J, G, constraint_value=1.0)
        assert prob.constraint_value == 1.0

    def test_solve_with_lagrange(self):
        J = lambda y: 0.0
        prob = IsoperimetricProblem(J, lambda y: 0.0, constraint_value=1.0)
        result = prob.solve_with_lagrange(lambda t: t)
        assert isinstance(result, (int, float))


class TestNoetherTheorem:
    """Test Noether's theorem."""

    def test_has_symmetry(self):
        L = lambda t, y, dy: dy * dy
        trans = lambda y: y
        assert NoetherTheorem.has_symmetry(L, trans) is True

    def test_conserved_quantity(self):
        L = lambda t, y, dy: dy * dy
        symmetry = lambda y: y
        Q = NoetherTheorem.conserved_quantity(L, symmetry)
        assert callable(Q)
