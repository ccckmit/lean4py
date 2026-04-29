"""Tests for extended lie_groups module (v1.16)."""
import pytest
from lean4py.lie_groups import (
    CompactLieGroup, MaximalTorus, WeightLattice, CorootLattice, WeylChamber,
    WeylGroupOrbit, HighestWeightRep, WeylDimensionFormula, CompactGroupClassification,
    IntegrationOverGroup
)


class TestCompactLieGroup:
    def test_creation(self):
        clg = CompactLieGroup(6, 2)
        assert clg.dimension == 6
        assert clg.maximal_torus_dim == 2

    def test_has_maximal_torus(self):
        clg = CompactLieGroup(6, 2)
        assert clg.has_maximal_torus() is True

    def test_is_simply_connected(self):
        clg = CompactLieGroup(6, 2)
        assert clg.is_simply_connected() is True


class TestMaximalTorus:
    def test_creation(self):
        mt = MaximalTorus(3)
        assert mt.rank == 3

    def test_weight_lattice(self):
        mt = MaximalTorus(3)
        wl = mt.weight_lattice()
        assert wl.rank == 3


class TestWeightLattice:
    def test_creation(self):
        wl = WeightLattice(3)
        assert wl.rank == 3

    def test_add_weight(self):
        wl = WeightLattice(3)
        wl.add_weight([1, 0, 0])
        assert len(wl._lattice) == 1

    def test_simple_roots(self):
        wl = WeightLattice(3)
        roots = wl.simple_roots()
        assert len(roots) == 3

    def test_fundamental_weights(self):
        wl = WeightLattice(3)
        weights = wl.fundamental_weights()
        assert len(weights) == 3


class TestCorootLattice:
    def test_creation(self):
        cr = CorootLattice(3)
        assert cr.rank == 3

    def test_simple_coroot(self):
        cr = CorootLattice(3)
        result = cr.simple_coroot(0)
        assert len(result) == 3


class TestWeylChamber:
    def test_creation(self):
        wc = WeylChamber()
        assert wc.root_system is None

    def test_is_dominant(self):
        wc = WeylChamber()
        assert wc.is_dominant([1.0, 0.0]) is True
        assert wc.is_dominant([-1.0, 0.0]) is False

    def test_fundamental_chamber(self):
        wc = WeylChamber()
        assert isinstance(wc.fundamental_chamber(), set)


class TestWeylGroupOrbit:
    def test_creation(self):
        wo = WeylGroupOrbit([1.0, 0.0])
        assert wo.weight == [1.0, 0.0]

    def test_orbit(self):
        wo = WeylGroupOrbit([1.0, 0.0])
        result = wo.orbit()
        assert isinstance(result, list)


class TestHighestWeightRep:
    def test_creation(self):
        hwr = HighestWeightRep([1.0, 0.0], 3)
        assert hwr.highest_weight == [1.0, 0.0]
        assert hwr.dimension == 3

    def test_weight_multiplicity(self):
        hwr = HighestWeightRep([1.0, 0.0], 3)
        assert hwr.weight_multiplicity([1.0, 0.0]) == 1
        assert hwr.weight_multiplicity([0.0, 1.0]) == 0

    def test_dimension_formula(self):
        hwr = HighestWeightRep([1.0, 0.0], 3)
        assert hwr.dimension_formula() == 3


class TestWeylDimensionFormula:
    def test_compute(self):
        result = WeylDimensionFormula.compute([1.0, 0.0])
        assert result == 1


class TestCompactGroupClassification:
    def test_classify_from_root_system(self):
        result = CompactGroupClassification.classify_from_root_system()
        assert result == "semisimple_compact"


class TestIntegrationOverGroup:
    def test_creation(self):
        iog = IntegrationOverGroup()
        assert iog.group is None

    def test_haar_measure(self):
        iog = IntegrationOverGroup()
        measure = iog.haar_measure()
        assert callable(measure)


def test_import_from_package():
    from lean4py import (
        CompactLieGroup, MaximalTorus, WeightLattice, WeylChamber,
        HighestWeightRep, WeylDimensionFormula
    )
    assert CompactLieGroup is not None
    assert MaximalTorus is not None
    assert WeightLattice is not None
    assert WeylChamber is not None
    assert HighestWeightRep is not None