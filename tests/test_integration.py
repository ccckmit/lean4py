"""Tests for integration module."""

import pytest
from lean4py.integration import (
    BochnerIntegral, FubiniTheorem, ChangeOfVariables,
    Convolution, LpSpace, HolderInequality, MinkowskiInequality
)


class TestBochnerIntegral:
    """Test Bochner integral."""

    def test_integral(self):
        f = lambda x: (x, x * 2)
        domain = {0, 1, 2}
        measure = lambda s: len(s)
        result = BochnerIntegral.integral(f, domain, measure)
        assert len(result) == 2

    def test_is_linear(self):
        f = lambda x: (x,)
        g = lambda x: (x * 2,)
        domain = {0, 1}
        measure = lambda s: 1.0
        assert BochnerIntegral.is_linear(f, g, domain, measure) is True


class TestFubiniTheorem:
    """Test Fubini's theorem."""

    def test_fubini_holds(self):
        f = lambda x, y: x + y
        x_domain = {0, 1}
        y_domain = {0, 1}
        x_measure = lambda s: len(s)
        y_measure = lambda s: len(s)
        assert FubiniTheorem.fubini_holds(f, x_domain, y_domain, x_measure, y_measure) is True

    def test_iterated_integral(self):
        f = lambda x, y: x + y
        x_domain = {0, 1}
        y_domain = {0, 1}
        result = FubiniTheorem.iterated_integral(f, x_domain, y_domain)
        assert result >= 0


class TestChangeOfVariables:
    """Test change of variables."""

    def test_change_of_variables(self):
        f = lambda x: x * x
        phi = lambda t: t * 2
        phi_inv = lambda x: x / 2
        result = ChangeOfVariables.change_of_variables(f, phi, phi_inv, 0, 1)
        assert result >= 0


class TestConvolution:
    """Test convolution."""

    def test_convolve(self):
        f = lambda x: 1.0 if 0 <= x <= 1 else 0.0
        g = lambda x: 1.0 if 0 <= x <= 1 else 0.0
        result = Convolution.convolve(f, g, 0.5)
        assert result >= 0

    def test_is_commutative(self):
        f = lambda x: x
        g = lambda x: x * 2
        assert Convolution.is_commutative(f, g) is True


class TestLpSpace:
    """Test L^p spaces."""

    def test_creation(self):
        lp = LpSpace(p=2.0, measure_space=None)
        assert lp.p == 2.0

    def test_norm(self):
        f = lambda x: x
        domain = {1, 2, 3}
        measure = lambda s: len(s)
        lp = LpSpace(p=2.0, measure_space=None)
        norm = lp.norm(f, measure, domain)
        assert norm >= 0

    def test_is_banach(self):
        lp = LpSpace(p=2.0, measure_space=None)
        assert lp.is_banach() is True


class TestHolderInequality:
    """Test Hölder inequality."""

    def test_holder_holds(self):
        assert HolderInequality.holder_holds(p=2.0, q=2.0, f_norm=1.0, g_norm=1.0, fg_norm=1.0) is True

    def test_verify(self):
        f = lambda x: x
        g = lambda x: x * 2
        domain = {1, 2}
        measure = lambda s: len(s)
        assert HolderInequality.verify(p=2.0, q=2.0, f=f, g=g, measure=measure, domain=domain) is True


class TestMinkowskiInequality:
    """Test Minkowski inequality."""

    def test_minkowski_holds(self):
        assert MinkowskiInequality.minkowski_holds(p=2.0, f_norm=1.0, g_norm=1.0, sum_norm=2.0) is True

    def test_verify(self):
        f = lambda x: x
        g = lambda x: x * 2
        domain = {1, 2}
        measure = lambda s: len(s)
        assert MinkowskiInequality.verify(p=2.0, f=f, g=g, measure=measure, domain=domain) is True
