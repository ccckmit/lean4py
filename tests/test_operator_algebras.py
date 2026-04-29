"""Tests for operator_algebras module."""
import pytest
from lean4py.operator_algebras import (
    NormedSpace, HilbertSpace, BoundedOperator, CStarAlgebra, PositiveElement,
    VonNeumannAlgebra, SpectralTheorem, FunctionalCalculus, K0Group, K1Group, IndexTheory
)


class TestNormedSpace:
    def test_creation(self):
        ns = NormedSpace({1, 2, 3}, lambda x: abs(x))
        assert len(ns.carrier) == 3

    def test_norm(self):
        ns = NormedSpace({1, 2, 3}, lambda x: abs(x))
        assert ns.norm(5) == 5

    def test_is_complete(self):
        ns = NormedSpace({1}, lambda x: abs(x))
        assert ns.is_complete() is True

    def test_norm_of_sum(self):
        ns = NormedSpace({1}, lambda x: abs(x))
        assert ns.norm_of_sum(1, 1) == 2


class TestHilbertSpace:
    def test_creation(self):
        hs = HilbertSpace({1}, lambda x, y: x * y, lambda x: abs(x)**0.5)
        assert hs is not None

    def test_is_hilbert(self):
        hs = HilbertSpace({1}, lambda x, y: x * y, lambda x: abs(x)**0.5)
        assert hs.is_hilbert() is True


class TestBoundedOperator:
    def test_creation(self):
        op = BoundedOperator(2, 2)
        assert op.domain_dim == 2
        assert op.codomain_dim == 2

    def test_matrix_creation(self):
        mat = [[1, 0], [0, 1]]
        op = BoundedOperator(2, 2, matrix=mat)
        assert op.matrix == mat

    def test_norm(self):
        op = BoundedOperator(2, 2)
        assert op.norm() >= 0

    def test_adjoint(self):
        mat = [[1, 0], [0, 1]]
        op = BoundedOperator(2, 2, matrix=mat)
        adj = op.adjoint()
        assert adj is not None


class TestCStarAlgebra:
    def test_creation(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        assert 1 in alg.elements

    def test_is_cstar(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        assert alg.is_cstar() is True

    def test_is_commutative(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        assert alg.is_commutative() is True


class TestPositiveElement:
    def test_creation(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        pos = PositiveElement(1, alg)
        assert pos.element == 1

    def test_is_positive(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        pos = PositiveElement(1, alg)
        assert pos.is_positive() is True


class TestVonNeumannAlgebra:
    def test_creation(self):
        hs = HilbertSpace({1}, lambda x, y: x * y, lambda x: abs(x)**0.5)
        vna = VonNeumannAlgebra({BoundedOperator(2, 2)}, hs)
        assert len(vna.operators) == 1

    def test_commutant(self):
        hs = HilbertSpace({1}, lambda x, y: x * y, lambda x: abs(x)**0.5)
        vna = VonNeumannAlgebra(set(), hs)
        comm = vna.commutant()
        assert comm is not None

    def test_is_vonneumann(self):
        hs = HilbertSpace({1}, lambda x, y: x * y, lambda x: abs(x)**0.5)
        vna = VonNeumannAlgebra(set(), hs)
        assert vna.is_vonneumann() is True


class TestSpectralTheorem:
    def test_creation(self):
        op = BoundedOperator(2, 2)
        st = SpectralTheorem(op)
        assert st.operator == op

    def test_spectrum(self):
        op = BoundedOperator(2, 2)
        st = SpectralTheorem(op)
        spec = st.spectrum()
        assert isinstance(spec, set)

    def test_functional_calculus(self):
        op = BoundedOperator(2, 2)
        st = SpectralTheorem(op)
        result = st.functional_calculus(lambda x: x**2)
        assert result is not None


class TestFunctionalCalculus:
    def test_creation(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        fc = FunctionalCalculus(1, alg)
        assert fc.element == 1

    def test_apply(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        fc = FunctionalCalculus(1, alg)
        result = fc.apply(lambda x: x**2)
        assert result == 1


class TestK0Group:
    def test_creation(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        k = K0Group(alg)
        assert k.algebra == alg

    def test_add_projection(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        k = K0Group(alg)
        k.add_projection(0, 1)
        assert 1 in k.projections[0]


class TestK1Group:
    def test_creation(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        k = K1Group(alg)
        assert k.algebra == alg

    def test_add_unitary(self):
        alg = CStarAlgebra({1}, lambda x, y: x, lambda x: 1.0, lambda x: x)
        k = K1Group(alg)
        k.add_unitary(1)


class TestIndexTheory:
    def test_creation(self):
        op = BoundedOperator(2, 2)
        idx = IndexTheory(op)
        assert idx.operator == op

    def test_kernel_dimension(self):
        op = BoundedOperator(2, 2)
        idx = IndexTheory(op)
        assert idx.kernel_dimension() == 0

    def test_cokernel_dimension(self):
        op = BoundedOperator(2, 2)
        idx = IndexTheory(op)
        assert idx.cokernel_dimension() == 0

    def test_index(self):
        op = BoundedOperator(2, 2)
        idx = IndexTheory(op)
        assert isinstance(idx.index(), int)

    def test_is_fredholm(self):
        op = BoundedOperator(2, 2)
        idx = IndexTheory(op)
        assert idx.is_fredholm() is True


def test_import_from_package():
    from lean4py import (
        NormedSpace, HilbertSpace, BoundedOperator, CStarAlgebra,
        VonNeumannAlgebra, SpectralTheorem, K0Group, K1Group, IndexTheory
    )
    assert NormedSpace is not None
    assert HilbertSpace is not None
    assert BoundedOperator is not None
    assert CStarAlgebra is not None
    assert VonNeumannAlgebra is not None
    assert SpectralTheorem is not None
    assert K0Group is not None
    assert K1Group is not None
    assert IndexTheory is not None