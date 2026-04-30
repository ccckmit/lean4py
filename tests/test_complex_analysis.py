"""Tests for complex_analysis module."""

import pytest
from lean4py.complex_analysis import (
    ComplexFunction, CauchyRiemann, CauchyIntegralFormula,
    LiouvilleTheorem, MaximumModulusPrinciple, ResidueTheorem,
    LaurentSeries, ArgumentPrinciple
)
import cmath, math


class TestComplexFunction:
    """Test complex functions."""

    def test_evaluate(self):
        f = lambda z: z * z
        cf = ComplexFunction(f)
        result = cf.evaluate(1+1j)
        assert isinstance(result, complex)
        assert abs(result - 2j) < 1e-10

    def test_is_holomorphic(self):
        f = lambda z: z * z
        cf = ComplexFunction(f)
        assert cf.is_holomorphic(0+0j) is True


class TestCauchyRiemann:
    """Test Cauchy-Riemann equations."""

    def test_check(self):
        f = lambda z: z * z
        assert CauchyRiemann.check(f, 0+0j) is True

    def test_is_holomorphic(self):
        f = lambda z: z * z
        domain = [0+0j, 1+0j, 0+1j]
        assert CauchyRiemann.is_holomorphic(f, domain) is True


class TestCauchyIntegralFormula:
    """Test Cauchy integral formula."""

    def test_cauchy_integral(self):
        f = lambda z: z * z
        result = CauchyIntegralFormula.cauchy_integral(f, z0=0+0j, radius=1.0)
        assert isinstance(result, complex)

    def test_nth_derivative(self):
        f = lambda z: z * z
        result = CauchyIntegralFormula.nth_derivative(f, z0=0+0j, n=1)
        assert isinstance(result, complex)


class TestLiouvilleTheorem:
    """Test Liouville's theorem."""

    def test_is_constant(self):
        f = lambda z: 1.0 + 0j  # Constant function
        assert LiouvilleTheorem.is_constant(f, bound=1.0) is True


class TestMaximumModulusPrinciple:
    """Test maximum modulus principle."""

    def test_max_on_boundary(self):
        f = lambda z: z
        assert MaximumModulusPrinciple.max_on_boundary(f, center=0+0j, radius=1.0) is True


class TestResidueTheorem:
    """Test residue theorem."""

    def test_residue(self):
        f = lambda z: 1.0 / z  # Simple pole at 0
        result = ResidueTheorem.residue(f, z0=0+0j)
        assert isinstance(result, complex)

    def test_contour_integral(self):
        f = lambda z: 1.0 / z
        result = ResidueTheorem.contour_integral(f, center=0+0j, radius=1.0)
        assert isinstance(result, complex)


class TestLaurentSeries:
    """Test Laurent series."""

    def test_series(self):
        f = lambda z: 1.0 / z
        coeffs, start = LaurentSeries.series(f, z0=0+0j, n_terms=5)
        assert len(coeffs) == 11  # -5 to 5
        assert start == -5


class TestArgumentPrinciple:
    """Test argument principle."""

    def test_winding_number(self):
        f = lambda z: z
        result = ArgumentPrinciple.winding_number(f, center=0+0j, radius=1.0)
        assert isinstance(result, int)
