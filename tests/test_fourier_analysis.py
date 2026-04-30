"""Tests for fourier_analysis module."""

import pytest
from lean4py.fourier_analysis import (
    FourierTransform, InverseFourierTransform, FourierSeries,
    Convolution, PlancherelTheorem, RiemannLebesgueLemma, PoissonSummation
)
import cmath, math


class TestFourierTransform:
    """Test Fourier transform."""

    def test_fourier_transform(self):
        f = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        result = FourierTransform.fourier_transform(f, xi=0.0)
        assert isinstance(result, complex)

    def test_fourier_transform_sin(self):
        f = lambda x: cmath.sin(x) if -10 <= x <= 10 else 0.0
        result = FourierTransform.fourier_transform(f, xi=1.0)
        assert isinstance(result, complex)


class TestInverseFourierTransform:
    """Test inverse Fourier transform."""

    def test_inverse(self):
        F = lambda xi: cmath.exp(-cmath.pi * xi * xi)
        result = InverseFourierTransform.evaluate(F, x=0.0)
        assert isinstance(result, complex)


class TestFourierSeries:
    """Test Fourier series."""

    def test_coefficients(self):
        f = lambda x: x
        coeffs = FourierSeries.coefficients(f, period=2*math.pi, n_terms=5)
        assert len(coeffs) == 11  # -5 to 5

    def test_reconstruct(self):
        coeffs = [1.0 + 0j] * 11
        result = FourierSeries.reconstruct(coeffs, x=0.0)
        assert isinstance(result, complex)


class TestConvolution:
    """Test convolution theorem."""

    def test_convolve(self):
        f = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        g = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        result = Convolution.convolve(f, g, x=0.0)
        assert isinstance(result, complex)

    def test_convolution_theorem(self):
        f = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        g = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        assert Convolution.convolution_theorem(f, g, xi=0.0) is True


class TestPlancherelTheorem:
    """Test Plancherel theorem."""

    def test_plancherel_holds(self):
        f = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        assert PlancherelTheorem.plancherel_holds(f) is True


class TestRiemannLebesgueLemma:
    """Test Riemann-Lebesgue lemma."""

    def test_holds(self):
        f = lambda x: 1.0 if -0.5 <= x <= 0.5 else 0.0
        assert RiemannLebesgueLemma.holds(f) is True


class TestPoissonSummation:
    """Test Poisson summation formula."""

    def test_poisson_summation(self):
        f = lambda x: cmath.exp(-x * x)
        assert PoissonSummation.poisson_summation(f) is True
