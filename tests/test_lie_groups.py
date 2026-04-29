"""Tests for lie_groups module."""
import pytest
from lean4py.lie_groups import (
    LieGroup, ClosedSubgroup, LieSubgroup, UnitaryRepresentation,
    AdjointRepresentation, ExponentialMap, BakerCampbellHausdorff,
    LieGroupCorrespondence, ClassicalGroups, OneParameterSubgroup, LieGroupHomomorphism
)


class TestLieGroup:
    def test_creation(self):
        lg = LieGroup(3)
        assert lg.dimension == 3

    def test_identity(self):
        lg = LieGroup(2, identity=1)
        assert lg.identity() == 1

    def test_is_group(self):
        lg = LieGroup(2)
        assert lg.is_group() is True

    def test_is_manifold(self):
        lg = LieGroup(2)
        assert lg.is_manifold() is True


class TestClosedSubgroup:
    def test_creation(self):
        parent = LieGroup(3)
        sub = ClosedSubgroup(parent, {1, 2})
        assert sub.parent == parent
        assert sub.elements == {1, 2}

    def test_is_closed(self):
        parent = LieGroup(3)
        sub = ClosedSubgroup(parent)
        assert sub.is_closed() is True


class TestLieSubgroup:
    def test_creation(self):
        parent = LieGroup(2)
        sub = LieSubgroup(parent, {1})
        assert sub.parent == parent


class TestUnitaryRepresentation:
    def test_creation(self):
        lg = LieGroup(3)
        rep = UnitaryRepresentation(lg, 2)
        assert rep.lie_group == lg
        assert rep.hilbert_space_dim == 2

    def test_is_unitary(self):
        lg = LieGroup(3)
        rep = UnitaryRepresentation(lg, 2)
        assert rep.is_unitary() is True

    def test_is_irreducible(self):
        lg = LieGroup(3)
        rep = UnitaryRepresentation(lg, 2)
        assert rep.is_irreducible() is True


class TestAdjointRepresentation:
    def test_creation(self):
        lg = LieGroup(3)
        ad = AdjointRepresentation(lg)
        assert ad.lie_group == lg

    def test_compute(self):
        lg = LieGroup(3)
        ad = AdjointRepresentation(lg)
        result = ad.compute(1, [1.0, 0.0, 0.0])
        assert isinstance(result, list)
        assert len(result) == 3


class TestExponentialMap:
    def test_creation(self):
        lg = LieGroup(2)
        exp = ExponentialMap(lg)
        assert exp.lie_group == lg

    def test_exp_zero(self):
        lg = LieGroup(2, identity=1)
        exp = ExponentialMap(lg)
        result = exp.exp([0.0, 0.0])
        assert result == 1

    def test_log(self):
        lg = LieGroup(2, identity=1)
        exp = ExponentialMap(lg)
        result = exp.log(1)
        assert result == [0.0, 0.0] or result is None


class TestBakerCampbellHausdorff:
    def test_compute(self):
        X = [1.0, 0.0, 0.0]
        Y = [0.0, 1.0, 0.0]
        result = BakerCampbellHausdorff.compute(X, Y, 3)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_series(self):
        result = BakerCampbellHausdorff.series(0.5, [[[1.0, 0.0], [0.0, 1.0]]])
        assert isinstance(result, list)


class TestLieGroupCorrespondence:
    def test_creation(self):
        lg = LieGroup(3)
        corr = LieGroupCorrespondence(lg)
        assert corr.lie_group == lg


class TestClassicalGroups:
    def test_GL(self):
        GL3 = ClassicalGroups.GL(3)
        assert GL3.dimension == 9

    def test_SL(self):
        SL2 = ClassicalGroups.SL(2)
        assert SL2.dimension == 3

    def test_SO(self):
        SO3 = ClassicalGroups.SO(3)
        assert SO3.dimension == 3

    def test_SU(self):
        SU2 = ClassicalGroups.SU(2)
        assert SU2.dimension == 3

    def test_Sp(self):
        Sp2 = ClassicalGroups.Sp(1)
        assert Sp2.dimension == 3


class TestOneParameterSubgroup:
    def test_creation(self):
        lg = LieGroup(3)
        ops = OneParameterSubgroup(lg, [1.0, 0.0, 0.0])
        assert ops.lie_group == lg
        assert ops.generator == [1.0, 0.0, 0.0]


class TestLieGroupHomomorphism:
    def test_creation(self):
        source = LieGroup(2)
        target = LieGroup(2)
        h = LieGroupHomomorphism(source, target, lambda x: x)
        assert h.source == source
        assert h.target == target

    def test_is_homomorphism(self):
        source = LieGroup(2)
        target = LieGroup(2)
        h = LieGroupHomomorphism(source, target, lambda x: x)
        assert h.is_homomorphism() is True


def test_import_from_package():
    from lean4py import LieGroup, ClosedSubgroup, ExponentialMap, ClassicalGroups
    assert LieGroup is not None
    assert ClosedSubgroup is not None
    assert ExponentialMap is not None
    assert ClassicalGroups is not None