"""Tests for stacks module."""
import pytest
from lean4py.stacks import (
    Groupoid, PresheafOfGroupoids, Stack, DMStack, ArtinStack,
    ModuliSpace, GITQuotient, DescentData, FiberedCategory
)


class TestGroupoid:
    def test_creation(self):
        objects = {1, 2, 3}
        g = Groupoid(objects)
        assert g.objects == objects

    def test_morphisms_between(self):
        g = Groupoid({1, 2})
        result = g.morphisms_between(1, 2)
        assert isinstance(result, set)

    def test_is_transitive(self):
        g = Groupoid({1})
        assert g.is_transitive() is True

    def test_is_connected(self):
        g = Groupoid({1})
        assert g.is_connected() is True

    def test_aut(self):
        g = Groupoid({1, 2})
        result = g.aut(1)
        assert isinstance(result, set)


class TestPresheafOfGroupoids:
    def test_creation(self):
        class MockSpace:
            pass
        p = PresheafOfGroupoids(MockSpace())
        assert p.space is not None


class TestStack:
    def test_creation(self):
        class MockSpace:
            pass
        s = Stack(MockSpace())
        assert s.is_stack() is True


class TestDMStack:
    def test_creation(self):
        class MockSpace:
            pass
        dm = DMStack(MockSpace(), {})
        assert dm.has_finite_stabilizers() is True

    def test_inertia_stack(self):
        class MockSpace:
            pass
        dm = DMStack(MockSpace(), {})
        inertia = dm.inertia_stack()
        assert isinstance(inertia, DMStack)


class TestArtinStack:
    def test_creation(self):
        class MockSpace:
            pass
        a = ArtinStack(MockSpace())
        assert a.is_artin() is True


class TestModuliSpace:
    def test_creation(self):
        m = ModuliSpace("M_g", 3)
        assert m.moduli_type == "M_g"
        assert m.dimension == 3

    def test_get_moduli_type(self):
        m = ModuliSpace("M_g", 3)
        assert m.get_moduli_type() == "M_g"

    def test_get_dimension(self):
        m = ModuliSpace("M_g", 3)
        assert m.get_dimension() == 3


class TestGITQuotient:
    def test_creation(self):
        g = GITQuotient("X", "G")
        assert g.space == "X"
        assert g.group == "G"

    def test_quotient(self):
        g = GITQuotient("X", "G")
        assert g.quotient() == "X"


class TestDescentData:
    def test_creation(self):
        d = DescentData([{1}, {2}], ["data1", "data2"])
        assert len(d.cover) == 2
        assert len(d.local_data) == 2

    def test_check_descent(self):
        d = DescentData([], [])
        assert d.check_descent() is True

    def test_gluing_data(self):
        d = DescentData([{1}], ["data"])
        assert d.gluing_data() == "data"

    def test_cocycle_condition(self):
        d = DescentData([], [])
        assert d.cocycle_condition() is True


class TestFiberedCategory:
    def test_creation(self):
        f = FiberedCategory("base")
        assert f.base_category == "base"

    def test_is_fibered(self):
        f = FiberedCategory("base")
        assert f.is_fibered() is True


def test_import_from_package():
    from lean4py import Groupoid, Stack, DMStack, ModuliSpace, GITQuotient
    assert Groupoid is not None
    assert Stack is not None
    assert DMStack is not None
    assert ModuliSpace is not None
    assert GITQuotient is not None