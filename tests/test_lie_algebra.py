"""Tests for lie_algebra module."""
import pytest
from lean4py.lie_algebra import (
    LieAlgebra, LieSubalgebra, LieAlgebraRepresentation, AdjointRepresentation,
    UniversalEnvelopingAlgebra, SerreRelations, RootSystem,
    sl2_lie_algebra, gl2_lie_algebra
)


class TestLieAlgebra:
    def test_creation(self):
        def bracket(x, y):
            return [0.0, 0.0, 0.0]
        la = LieAlgebra("test", 3, bracket)
        assert la.name == "test"
        assert la.dimension == 3

    def test_default_basis(self):
        def bracket(x, y):
            return [0.0] * 3
        la = LieAlgebra("test", 3, bracket)
        assert len(la.basis) == 3

    def test_bracket_of_basis(self):
        def bracket(x, y):
            return [0.0, y[0] - x[0], 0.0]
        la = LieAlgebra("test", 3, bracket)
        result = la.bracket_of_basis(0, 1)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_is_abelian(self):
        def zero_bracket(x, y):
            return [0.0, 0.0, 0.0]
        la = LieAlgebra("abelian", 2, zero_bracket)
        assert la.is_abelian() is True

    def test_is_lie_algebra(self):
        def bracket(x, y):
            return [0.0] * 3
        la = LieAlgebra("test", 3, bracket)
        assert la.is_lie_algebra() is True


class TestLieSubalgebra:
    def test_creation(self):
        def bracket(x, y):
            return [0.0] * 3
        la = LieAlgebra("test", 3, bracket)
        sub = LieSubalgebra(la, {0, 1})
        assert sub.parent == la
        assert sub._dimension == 2

    def test_is_subalgebra(self):
        def bracket(x, y):
            return [0.0] * 3
        la = LieAlgebra("test", 3, bracket)
        sub = LieSubalgebra(la, {0})
        assert sub.is_subalgebra() is True

    def test_is_ideal(self):
        def bracket(x, y):
            return [0.0] * 3
        la = LieAlgebra("test", 3, bracket)
        sub = LieSubalgebra(la, {0, 1})
        assert sub.is_ideal() is True


class TestAdjointRepresentation:
    def test_creation(self):
        def bracket(x, y):
            return [0.0, y[0] - x[0], 0.0]
        la = LieAlgebra("test", 3, bracket)
        ad = AdjointRepresentation(la)
        assert ad.lie_algebra == la

    def test_compute(self):
        def bracket(x, y):
            return [0.0, y[0] - x[0], 0.0]
        la = LieAlgebra("test", 3, bracket)
        ad = AdjointRepresentation(la)
        result = ad.compute([1, 0, 0], [0, 1, 0])
        assert isinstance(result, list)

    def test_killing_form(self):
        def bracket(x, y):
            return [0.0, y[0] - x[0], 0.0]
        la = LieAlgebra("test", 3, bracket)
        ad = AdjointRepresentation(la)
        result = ad.killing_form([1, 0, 0], [0, 1, 0])
        assert isinstance(result, (int, float))


class TestUniversalEnvelopingAlgebra:
    def test_creation(self):
        def bracket(x, y):
            return [0.0] * 3
        la = LieAlgebra("test", 3, bracket)
        uea = UniversalEnvelopingAlgebra(la)
        assert uea.lie_algebra == la

    def test_basis(self):
        def bracket(x, y):
            return [0.0] * 2
        la = LieAlgebra("test", 2, bracket)
        uea = UniversalEnvelopingAlgebra(la)
        basis = uea.basis()
        assert isinstance(basis, list)
        assert len(basis) > 0

    def test_dimension(self):
        def bracket(x, y):
            return [0.0] * 2
        la = LieAlgebra("test", 2, bracket)
        uea = UniversalEnvelopingAlgebra(la)
        assert uea.dimension() == -1


class TestRootSystem:
    def test_creation(self):
        rs = RootSystem(2)
        assert rs.rank == 2

    def test_simple_root(self):
        rs = RootSystem(2, [[1, 0], [0, 1]])
        result = rs.simple_root(0)
        assert result == [1, 0]

    def test_simple_root_out_of_range(self):
        rs = RootSystem(1)
        result = rs.simple_root(10)
        assert result == [0.0]

    def test_cartan_matrix_element(self):
        rs = RootSystem(2, [[1, 0], [0, 1]], [[2, -1], [-1, 2]])
        assert rs.cartan_matrix_element(0, 0) == 2
        assert rs.cartan_matrix_element(0, 1) == -1

    def test_is_cartan_type(self):
        rs1 = RootSystem(1)
        assert rs1.is_cartan_type() == "A_1"
        rs2 = RootSystem(2, [[1, 0], [0, 1]], [[2, -1], [-1, 2]])
        result = rs2.is_cartan_type()
        assert "A" in result or "B" in result or "C" in result or "G" in result

    def test_compute_positive_roots(self):
        rs = RootSystem(2, [[1, 0], [0, 1]])
        roots = rs.compute_positive_roots()
        assert isinstance(roots, list)

    def test_get_rank(self):
        rs = RootSystem(3)
        assert rs.get_rank() == 3


class TestSerreRelations:
    def test_creation(self):
        rs = RootSystem(2)
        sr = SerreRelations(rs)
        assert sr.root_system == rs

    def test_generate_relations(self):
        rs = RootSystem(2, [[1, 0], [0, 1]], [[2, -1], [-1, 2]])
        sr = SerreRelations(rs)
        rels = sr.generate_relations()
        assert isinstance(rels, list)


class TestStandardLieAlgebras:
    def test_sl2(self):
        sl2 = sl2_lie_algebra()
        assert sl2.name == "sl2"
        assert sl2.dimension == 3
        assert sl2.is_lie_algebra() is True

    def test_gl2(self):
        gl2 = gl2_lie_algebra()
        assert gl2.name == "gl2"
        assert gl2.dimension == 4


def test_import_from_package():
    from lean4py import (
        LieAlgebra, LieSubalgebra, LieAlgebraRepresentation, AdjointRepresentation,
        UniversalEnvelopingAlgebra, SerreRelations, RootSystem,
        sl2_lie_algebra, gl2_lie_algebra
    )
    assert LieAlgebra is not None
    assert RootSystem is not None
    assert sl2_lie_algebra is not None