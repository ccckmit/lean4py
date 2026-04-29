"""Tests for homological_algebra module."""
import pytest
from lean4py.homological_algebra import (
    ChainComplex, CochainComplex, LongExactSequence, Ext, Tor,
    exact_sequence_from_chain, connecting_homomorphism
)


class TestChainComplex:
    def test_chain_complex_creation(self):
        modules = [1, 2, 3]
        diffs = [lambda x: x * 2, lambda x: x]
        cc = ChainComplex(modules, diffs)
        assert len(cc.modules) == 3
        assert len(cc.differentials) == 2

    def test_homology_zero_degree(self):
        modules = [1, 2, 3]
        diffs = [lambda x: 0, lambda x: 0]
        cc = ChainComplex(modules, diffs)
        result = cc.homology(0)
        assert isinstance(result, set)

    def test_homology_out_of_range(self):
        cc = ChainComplex([], [])
        assert cc.homology(5) == set()
        assert cc.homology(-1) == set()

    def test_cochain_complex(self):
        modules = [1, 2, 3]
        coboundaries = [lambda x: x]
        coc = CochainComplex(modules, coboundaries)
        assert len(coc.modules) == 3

    def test_cohomology(self):
        coc = CochainComplex([1], [lambda x: 0])
        result = coc.cohomology(0)
        assert isinstance(result, set)


class TestExtTor:
    def test_ext_creation(self):
        ext = Ext("M", "N", "R")
        assert ext.module_m == "M"
        assert ext.module_n == "N"
        assert ext.ring == "R"

    def test_ext_compute(self):
        ext = Ext("M", "N", "R")
        assert ext.compute(0) == "N"
        assert ext.compute(1) is None

    def test_tor_creation(self):
        tor = Tor("M", "N", "R")
        assert tor.module_m == "M"
        assert tor.module_n == "N"
        assert tor.ring == "R"

    def test_tor_compute(self):
        tor = Tor("M", "N", "R")
        result = tor.compute(0)
        assert result is not None
        assert "M" in result and "N" in result


class TestLongExactSequence:
    def test_les_creation(self):
        les = LongExactSequence([1, 2, 3], [lambda x: x])
        assert len(les.terms) == 3
        assert len(les.connecting_maps) == 1

    def test_verify_exactness(self):
        les = LongExactSequence([], [])
        result = les.verify_exactness()
        assert isinstance(result, bool)


class TestHelpers:
    def test_exact_sequence_from_chain(self):
        cc = ChainComplex([1, 2, 3], [lambda x: 0, lambda x: 0])
        result = exact_sequence_from_chain(cc, 0)
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_exact_sequence_out_of_range(self):
        cc = ChainComplex([], [])
        result = exact_sequence_from_chain(cc, 10)
        assert result is None

    def test_connecting_homomorphism(self):
        les = LongExactSequence([1, 2], [])
        delta = connecting_homomorphism(les, 0)
        assert callable(delta)
        assert delta("x") == "x"


def test_import_from_package():
    from lean4py import ChainComplex, CochainComplex, Ext, Tor
    assert ChainComplex is not None
    assert CochainComplex is not None
    assert Ext is not None
    assert Tor is not None