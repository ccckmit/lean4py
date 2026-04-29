"""Tests for free_probability module (v1.16)."""
import pytest
from lean4py.free_probability import (
    FreeProbabilitySpace, FreeRandomVariable, FreeCentralLimitTheorem,
    MarchenkoPastur, FreeConvolution, NoncommutativeSpace, SpectralTriple,
    ConnesDifferential, SpectralFlow, FredholmModule
)


class TestFreeProbabilitySpace:
    def test_creation(self):
        fp = FreeProbabilitySpace("algebra", lambda x: 1)
        assert fp.algebra == "algebra"

    def test_expectation(self):
        fp = FreeProbabilitySpace("algebra", lambda x: 2)
        assert fp.expectation("x") == 2

    def test_variance(self):
        fp = FreeProbabilitySpace("algebra", lambda x: 3)
        result = fp.variance(5)  # Use a number
        assert isinstance(result, (int, float))


class TestFreeRandomVariable:
    def test_creation(self):
        frv = FreeRandomVariable(lambda x: x**2, [0, 1])
        assert frv.distribution is not None
        assert len(frv.cumulants) == 2

    def test_free_cumulants(self):
        frv = FreeRandomVariable(lambda x: x**2, [0, 1])
        assert frv.free_cumulants() == [0, 1]


class TestFreeCentralLimitTheorem:
    def test_creation(self):
        clt = FreeCentralLimitTheorem([FreeRandomVariable(lambda x: x, [0, 1])])
        assert len(clt.variables) == 1

    def test_limit_distribution(self):
        clt = FreeCentralLimitTheorem([])
        dist = clt.limit_distribution()
        assert isinstance(dist, FreeRandomVariable)


class TestMarchenkoPastur:
    def test_creation(self):
        mp = MarchenkoPastur(1.0, 1.0)
        assert mp.lambda_param == 1.0
        assert mp.ratio == 1.0

    def test_support(self):
        mp = MarchenkoPastur(1.0, 1.0)
        left, right = mp.support()
        assert left >= 0
        assert right > left

    def test_density_inside(self):
        mp = MarchenkoPastur(1.0, 1.0)
        density = mp.density(1.0)
        assert density > 0

    def test_density_outside(self):
        mp = MarchenkoPastur(1.0, 1.0)
        density = mp.density(10.0)
        assert density == 0.0


class TestFreeConvolution:
    def test_convolve(self):
        result = FreeConvolution.convolve("mu", "nu")
        assert result == "mu"


class TestNoncommutativeSpace:
    def test_creation(self):
        ncs = NoncommutativeSpace("algebra", "H", "D")
        assert ncs.algebra == "algebra"


class TestSpectralTriple:
    def test_creation(self):
        st = SpectralTriple("algebra", 10, [1.0, 2.0])
        assert st.algebra == "algebra"
        assert st.hilbert_space_dim == 10

    def test_zeta_function(self):
        st = SpectralTriple("algebra", 10, [1.0, 2.0])
        result = st.zeta_function(2)
        assert isinstance(result, (int, float))


class TestConnesDifferential:
    def test_creation(self):
        st = SpectralTriple("algebra", 10, [1.0])
        cd = ConnesDifferential(st)
        assert cd.spectral_triple is not None

    def test_compute_differential(self):
        st = SpectralTriple("algebra", 10, [1.0])
        cd = ConnesDifferential(st)
        result = cd.compute_differential("a")
        assert "D" in result


class TestSpectralFlow:
    def test_compute(self):
        result = SpectralFlow.compute([])
        assert result == 0

    def test_index_formula(self):
        result = SpectralFlow.index_formula("dirac")
        assert result == 0


class TestFredholmModule:
    def test_creation(self):
        fm = FredholmModule("algebra", "H", "F")
        assert fm.algebra == "algebra"

    def test_is_fredholm(self):
        fm = FredholmModule("algebra", "H", "F")
        assert fm.is_fredholm() is True


def test_import_from_package():
    from lean4py import (
        FreeProbabilitySpace, FreeRandomVariable, MarchenkoPastur,
        SpectralTriple, ConnesDifferential, SpectralFlow
    )
    assert FreeProbabilitySpace is not None
    assert FreeRandomVariable is not None
    assert MarchenkoPastur is not None
    assert SpectralTriple is not None
    assert ConnesDifferential is not None
    assert SpectralFlow is not None