"""Tests for order_theory module."""

import pytest
from lean4py.order_theory import (
    PartialOrder, TotalOrder, Lattice, CompleteLattice,
    HeytingAlgebra, BooleanAlgebra, GaloisConnection
)


class TestPartialOrder:
    """Test partial orders."""

    def test_creation(self):
        elements = {1, 2, 3}
        order = PartialOrder(elements, lambda x, y: x <= y)
        assert len(order.elements) == 3

    def test_leq(self):
        elements = {1, 2, 3}
        order = PartialOrder(elements, lambda x, y: x <= y)
        assert order.leq(1, 2) is True
        assert order.leq(2, 1) is False

    def test_is_partial_order(self):
        elements = {1, 2, 3}
        order = PartialOrder(elements, lambda x, y: x <= y)
        assert order.is_partial_order() is True

    def test_is_comparable(self):
        elements = {1, 2, 3}
        order = PartialOrder(elements, lambda x, y: x <= y)
        assert order.is_comparable(1, 2) is True
        assert order.is_comparable(1, 1) is True

    def test_min_elements(self):
        elements = {1, 2, 3}
        order = PartialOrder(elements, lambda x, y: x <= y)
        min_elems = order.min_elements()
        assert 1 in min_elems

    def test_max_elements(self):
        elements = {1, 2, 3}
        order = PartialOrder(elements, lambda x, y: x <= y)
        max_elems = order.max_elements()
        assert 3 in max_elems


class TestTotalOrder:
    """Test total orders."""

    def test_creation(self):
        elements = {1, 2, 3}
        order = TotalOrder(elements, lambda x, y: x <= y)
        assert len(order.elements) == 3

    def test_is_total_order(self):
        elements = {1, 2, 3}
        order = TotalOrder(elements, lambda x, y: x <= y)
        assert order.is_total_order() is True


class TestLattice:
    """Test lattices."""

    def test_creation(self):
        elements = {1, 2, 3}
        lattice = Lattice(elements,
                        lambda x, y: x <= y,
                        lambda x, y: max(x, y),
                        lambda x, y: min(x, y))
        assert len(lattice.elements) == 3

    def test_join(self):
        elements = {1, 2, 3}
        lattice = Lattice(elements,
                        lambda x, y: x <= y,
                        lambda x, y: max(x, y),
                        lambda x, y: min(x, y))
        assert lattice.join(1, 2) == 2

    def test_meet(self):
        elements = {1, 2, 3}
        lattice = Lattice(elements,
                        lambda x, y: x <= y,
                        lambda x, y: max(x, y),
                        lambda x, y: min(x, y))
        assert lattice.meet(1, 2) == 1

    def test_is_lattice(self):
        elements = {1, 2, 3}
        lattice = Lattice(elements,
                        lambda x, y: x <= y,
                        lambda x, y: max(x, y),
                        lambda x, y: min(x, y))
        assert lattice.is_lattice() is True


class TestCompleteLattice:
    """Test complete lattices."""

    def test_creation(self):
        elements = {1, 2, 3}
        lattice = CompleteLattice(elements,
                                lambda x, y: x <= y,
                                lambda x, y: max(x, y),
                                lambda x, y: min(x, y))
        assert lattice._complete is True

    def test_is_complete(self):
        elements = {1, 2, 3}
        lattice = CompleteLattice(elements,
                                lambda x, y: x <= y,
                                lambda x, y: max(x, y),
                                lambda x, y: min(x, y))
        assert lattice.is_complete() is True


class TestHeytingAlgebra:
    """Test Heyting algebras."""

    def test_creation(self):
        elements = {0, 1}
        ha = HeytingAlgebra(elements,
                         lambda x, y: x <= y,
                         lambda x, y: max(x, y),
                         lambda x, y: min(x, y),
                         lambda x, y: 1 if x <= y else 0)
        assert len(ha.elements) == 2

    def test_implies(self):
        elements = {0, 1}
        ha = HeytingAlgebra(elements,
                         lambda x, y: x <= y,
                         lambda x, y: max(x, y),
                         lambda x, y: min(x, y),
                         lambda x, y: 1 if x <= y else 0)
        assert ha.implies(0, 1) == 1

    def test_is_heyting(self):
        elements = {0, 1}
        ha = HeytingAlgebra(elements,
                         lambda x, y: x <= y,
                         lambda x, y: max(x, y),
                         lambda x, y: min(x, y),
                         lambda x, y: 1 if x <= y else 0)
        assert ha.is_heyting() is True


class TestBooleanAlgebra:
    """Test Boolean algebras."""

    def test_creation(self):
        elements = {0, 1}
        ba = BooleanAlgebra(elements,
                         lambda x, y: x <= y,
                         lambda x, y: max(x, y),
                         lambda x, y: min(x, y),
                         lambda x, y: 1 if x <= y else 0,
                         lambda x: 1 - x)
        assert len(ba.elements) == 2

    def test_complement(self):
        elements = {0, 1}
        ba = BooleanAlgebra(elements,
                         lambda x, y: x <= y,
                         lambda x, y: max(x, y),
                         lambda x, y: min(x, y),
                         lambda x, y: 1 if x <= y else 0,
                         lambda x: 1 - x)
        assert ba.complement(0) == 1

    def test_is_boolean(self):
        elements = {0, 1}
        ba = BooleanAlgebra(elements,
                         lambda x, y: x <= y,
                         lambda x, y: max(x, y),
                         lambda x, y: min(x, y),
                         lambda x, y: 1 if x <= y else 0,
                         lambda x: 1 - x)
        assert ba.is_boolean() is True


class TestGaloisConnection:
    """Test Galois connections."""

    def test_creation(self):
        elements_p = {1, 2}
        elements_q = {10, 20}
        order_p = PartialOrder(elements_p, lambda x, y: x <= y)
        order_q = PartialOrder(elements_q, lambda x, y: x <= y)

        def f(x):
            return x * 10

        def g(y):
            return y // 10

        gc = GaloisConnection(order_p, order_q, f, g)
        assert gc.order_p is order_p
        assert gc.order_q is order_q

    def test_is_galois_connection(self):
        elements_p = {1, 2}
        elements_q = {10, 20}
        order_p = PartialOrder(elements_p, lambda x, y: x <= y)
        order_q = PartialOrder(elements_q, lambda x, y: x <= y)

        def f(x):
            return x * 10

        def g(y):
            return y // 10

        gc = GaloisConnection(order_p, order_q, f, g)
        assert gc.is_galois_connection() is True
