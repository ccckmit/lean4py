"""Tests for numerical_methods module (v1.19)."""
import pytest
import math
from lean4py.numerical_methods import (
    NewtonRaphson, SecantMethod, BisectionMethod, FixedPointIteration,
    LagrangeInterpolation, NewtonInterpolation, GaussianQuadrature,
    SimpsonRule, RombergIntegration
)


class TestNewtonRaphson:
    def test_creation(self):
        nr = NewtonRaphson(lambda x: x**2 - 2)
        assert nr.f is not None

    def test_creation_with_derivative(self):
        nr = NewtonRaphson(lambda x: x**2 - 2, lambda x: 2*x)
        assert nr.f_prime is not None

    def test_find_root(self):
        nr = NewtonRaphson(lambda x: x**2 - 2)
        root, iters, conv = nr.find_root(1.0)
        assert conv is True
        assert abs(root - math.sqrt(2)) < 1e-6

    def test_find_root_no_convergence(self):
        nr = NewtonRaphson(lambda x: x**3 - x + 2)
        root, iters, conv = nr.find_root(0.0, max_iterations=5)
        assert conv is False

    def test_find_all_roots_simple(self):
        nr = NewtonRaphson(lambda x: x**2 - 2)
        roots = nr.find_all_roots((0, 10), step=2.0)
        assert len(roots) >= 1


class TestSecantMethod:
    def test_creation(self):
        sm = SecantMethod(lambda x: x**2 - 2)
        assert sm.f is not None

    def test_find_root(self):
        sm = SecantMethod(lambda x: x**2 - 2)
        root, iters, conv = sm.find_root(1.0, 2.0)
        assert conv is True
        assert abs(root - math.sqrt(2)) < 1e-4


class TestBisectionMethod:
    def test_creation(self):
        bm = BisectionMethod(lambda x: x**2 - 2)
        assert bm.f is not None

    def test_find_root(self):
        bm = BisectionMethod(lambda x: x**2 - 2)
        root, iters, conv = bm.find_root(0.0, 2.0)
        assert conv is True
        assert abs(root - math.sqrt(2)) < 1e-8


class TestFixedPointIteration:
    def test_creation(self):
        fpi = FixedPointIteration(lambda x: x**0.5)
        assert fpi.g is not None

    def test_find_fixed_point(self):
        fpi = FixedPointIteration(lambda x: x / 2 + 1)
        root, iters, conv = fpi.find_fixed_point(0.5)
        assert conv is True
        assert abs(root - 2.0) < 1e-6

    def test_has_convergence_guarantee(self):
        fpi = FixedPointIteration(lambda x: x * 0.5)
        assert fpi.has_convergence_guarantee(1.0) is True


class TestLagrangeInterpolation:
    def test_creation(self):
        li = LagrangeInterpolation([0, 1, 2], [0, 1, 4])
        assert li.n == 3

    def test_evaluate(self):
        li = LagrangeInterpolation([0, 1, 2], [1, 3, 5])
        result = li.evaluate(0.5)
        assert isinstance(result, float)

    def test_coefficients(self):
        li = LagrangeInterpolation([0, 1], [1, 2])
        coeff = li.coefficients()
        assert len(coeff) == 2


class TestNewtonInterpolation:
    def test_creation(self):
        ni = NewtonInterpolation([0, 1, 2], [1, 3, 5])
        assert ni.n == 3

    def test_evaluate(self):
        ni = NewtonInterpolation([0, 1, 2], [1, 3, 5])
        result = ni.evaluate(0.5)
        assert isinstance(result, float)

    def test_divided_diffs(self):
        ni = NewtonInterpolation([0, 1, 2], [1, 3, 5])
        assert len(ni.divided_diffs) == 3


class TestGaussianQuadrature:
    def test_creation(self):
        gq = GaussianQuadrature()
        assert gq is not None

    def test_legendre_polynomial_n0(self):
        result = GaussianQuadrature.legendre_polynomial(0, 0.5)
        assert result == 1.0

    def test_legendre_polynomial_n1(self):
        result = GaussianQuadrature.legendre_polynomial(1, 0.5)
        assert result == 0.5

    def test_legendre_polynomial_n2(self):
        result = GaussianQuadrature.legendre_polynomial(2, 0.5)
        assert abs(result - (-0.125)) < 1e-6

    def test_gauss_legendre_nodes_weights(self):
        nodes, weights = GaussianQuadrature.gauss_legendre_nodes_weights(3)
        assert len(nodes) == 3
        assert len(weights) == 3

    def test_integrate(self):
        gq = GaussianQuadrature()
        result = gq.integrate(lambda x: x**2, 0, 1, n=5)
        assert abs(result - 1/3) < 1e-4


class TestSimpsonRule:
    def test_creation(self):
        sr = SimpsonRule()
        assert sr is not None

    def test_integrate(self):
        sr = SimpsonRule()
        result = sr.integrate(lambda x: x**2, 0, 1, n=100)
        assert abs(result - 1/3) < 1e-4


class TestRombergIntegration:
    def test_creation(self):
        ri = RombergIntegration()
        assert ri is not None

    def test_integrate(self):
        ri = RombergIntegration()
        val, iters = ri.integrate(lambda x: x, 0, 1, max_iterations=5)
        assert abs(val - 0.5) < 0.1