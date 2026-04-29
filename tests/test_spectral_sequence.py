"""Tests for spectral_sequence module (v1.18)."""
import pytest
from lean4py.spectral_sequence import (
    SpectralSequence, AdamsSpectralSequence, SerreSpectralSequence,
    ExactCouple, Hypercohomology, FilteredComplex,
    CohomologySpectralSequence, HomologySpectralSequence
)


class TestSpectralSequence:
    def test_creation(self):
        ss = SpectralSequence({(0, 0): "Z", (1, 1): "Z/2"})
        assert len(ss.E2_page) == 2

    def test_creation_empty(self):
        ss = SpectralSequence()
        assert ss.E2_page == {}

    def test_compute_differentials(self):
        ss = SpectralSequence({(0, 0): "Z"})
        result = ss.compute_differentials(2)
        assert isinstance(result, dict)

    def test_extend_page(self):
        ss = SpectralSequence({(0, 0): "Z"})
        result = ss.extend_page(2)
        assert len(ss.pages) == 2

    def test_has_stabilized(self):
        ss = SpectralSequence({(0, 0): "Z"})
        ss.extend_page(2)
        ss.extend_page(3)
        result = ss.has_stabilized(2)
        assert isinstance(result, bool)

    def test_limit_term(self):
        ss = SpectralSequence({(0, 0): "Z", (1, 1): "Z/2"})
        result = ss.limit_term()
        assert isinstance(result, dict)

    def test_total_degree(self):
        ss = SpectralSequence()
        assert ss.total_degree(2, 3) == 5


class TestAdamsSpectralSequence:
    def test_creation(self):
        ass = AdamsSpectralSequence("cohomology_algebra")
        assert ass.cohomology_algebra == "cohomology_algebra"

    def test_compute_E2_page(self):
        ass = AdamsSpectralSequence()
        result = ass.compute_E2_page()
        assert isinstance(result, dict)

    def test_compute_extension(self):
        ass = AdamsSpectralSequence()
        result = ass.compute_extension(2)
        assert result is None


class TestSerreSpectralSequence:
    def test_creation(self):
        sss = SerreSpectralSequence("B", "F")
        assert sss.base_space == "B"
        assert sss.fiber == "F"

    def test_compute_E2(self):
        sss = SerreSpectralSequence()
        result = sss.compute_E2()
        assert isinstance(result, dict)

    def test_differentials(self):
        sss = SerreSpectralSequence()
        result = sss.differentials()
        assert isinstance(result, dict)


class TestExactCouple:
    def test_creation(self):
        ss = SpectralSequence()
        ec = ExactCouple(ss, "d", lambda x: x, lambda x: x, lambda x: x)
        assert ec.E is ss

    def test_generate(self):
        ss = SpectralSequence({(0, 0): "Z"})
        ec = ExactCouple(ss, "d", lambda x: x, lambda x: x, lambda x: x)
        result = ec.generate(5)
        assert isinstance(result, SpectralSequence)


class TestHypercohomology:
    def test_creation(self):
        h = Hypercohomology("complex")
        assert h.complex == "complex"

    def test_compute_XHn(self):
        h = Hypercohomology()
        result = h.compute_XHn(2)
        assert isinstance(result, str)


class TestFilteredComplex:
    def test_creation(self):
        fc = FilteredComplex(["M1", "M2"], [lambda x: x])
        assert len(fc.modules) == 2

    def test_creation_with_filtration(self):
        fc = FilteredComplex(["M1", "M2"], [lambda x: x], lambda x, n: n)
        assert fc.filtration is not None

    def test_associated_spectral_sequence(self):
        fc = FilteredComplex(["M1", "M2"], [lambda x: x])
        result = fc.associated_spectral_sequence()
        assert isinstance(result, SpectralSequence)

    def test_filtration_degree(self):
        fc = FilteredComplex(["M1"], [lambda x: x])
        result = fc.filtration_degree("x", 0)
        assert isinstance(result, int)


class TestCohomologySpectralSequence:
    def test_creation(self):
        css = CohomologySpectralSequence()
        assert css.pages == [{}]

    def test_compute_E2_cohomology(self):
        css = CohomologySpectralSequence()
        result = css.compute_E2_cohomology()
        assert isinstance(result, dict)


class TestHomologySpectralSequence:
    def test_creation(self):
        hss = HomologySpectralSequence()
        assert hss.pages == [{}]

    def test_compute_E2_homology(self):
        hss = HomologySpectralSequence()
        result = hss.compute_E2_homology()
        assert isinstance(result, dict)