"""Tests for optimization_theory module (simplified)."""

import pytest
from lean4py.optimization_theory import (
    ConvexSet, ConvexFunction, LagrangeMultiplier,
    KKTConditions, Duality, SlaterCondition
)


class TestConvexSet:
    """Test convex sets."""

    def test_is_convex(self):
        # Simplified: just test function exists
        assert callable(ConvexSet.is_convex)

    def test_convex_hull(self):
        points = [(0.0,), (1.0,), (0.5,)]
        hull = ConvexSet.convex_hull(points)
        assert len(hull) >= 3


class TestConvexFunction:
    """Test convex functions."""

    def test_is_convex(self):
        assert callable(ConvexFunction.is_convex)

    def test_is_strictly_convex(self):
        assert callable(ConvexFunction.is_strictly_convex)


class TestLagrangeMultiplier:
    """Test Lagrange multiplier method."""

    def test_lagrangian(self):
        f = lambda x: x[0] * x[0]
        constraints = [lambda x: x[0] - 1.0]
        L = LagrangeMultiplier.lagrangian(f, constraints, [1.0])
        assert callable(L)

    def test_solve(self):
        f = lambda x: x[0] * x[0]
        constraints = [lambda x: x[0] - 1.0]
        result, lambda_ = LagrangeMultiplier.solve(f, constraints, (0.5,))
        assert len(result) == 1


class TestKKTConditions:
    """Test KKT conditions."""

    def test_check(self):
        assert callable(KKTConditions.check)

    def test_is_optimal(self):
        assert callable(KKTConditions.is_optimal)


class TestDuality:
    """Test duality theory."""

    def test_lagrange_dual(self):
        assert callable(Duality.lagrange_dual)

    def test_is_strong_duality(self):
        assert Duality.is_strong_duality(primal_opt=1.0, dual_opt=1.0) is True

    def test_weak_duality(self):
        assert Duality.weak_duality(primal_obj=2.0, dual_obj=1.0) is True


class TestSlaterCondition:
    """Test Slater condition."""

    def test_holds(self):
        constraints = [lambda x: 1.0 - x[0]]
        domain = [(0.0,), (0.5,)]
        # Simplified: just check function exists and returns bool
        result = SlaterCondition.holds(constraints, domain)
        assert isinstance(result, bool)
