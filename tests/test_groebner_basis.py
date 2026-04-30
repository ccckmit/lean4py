"""Tests for groebner_basis module."""
import pytest
from lean4py.groebner_basis import (
    MonomialOrder,
    Polynomial,
    PolynomialRing,
    GroebnerBasis,
    BuchbergerAlgorithm,
    PolynomialIdeal,
    EliminationIdeal,
    IdealOperations,
)


class TestMonomialOrder:
    def test_lex_compare(self):
        order = MonomialOrder("lex")
        assert order.compare((1, 0), (0, 1)) == 1
        assert order.compare((1, 0), (1, 0)) == 0
        assert order.compare((0, 1), (1, 0)) == -1

    def test_grevlex_compare(self):
        order = MonomialOrder("grevlex")
        assert order.compare((1, 1), (2, 0)) == 1
        assert order.compare((1, 0), (0, 2)) == -1

    def test_dlex_compare(self):
        order = MonomialOrder("dlex")
        assert order.compare((2, 0), (1, 1)) == 1
        assert order.compare((1, 1), (2, 0)) == -1

    def test_compare_equal_total_degree(self):
        order = MonomialOrder("dlex")
        assert order.compare((1, 1), (0, 2)) == 1


class TestPolynomial:
    def test_zero_polynomial(self):
        order = MonomialOrder()
        p = Polynomial({}, order)
        assert p.is_zero() is True

    def test_constant_polynomial(self):
        order = MonomialOrder()
        p = Polynomial({(): 3.0}, order)
        assert p.is_zero() is False
        assert p.leading_monomial() == ()

    def test_leading_monomial(self):
        order = MonomialOrder("lex")
        p = Polynomial({(2, 1): 1.0, (1, 0): 2.0}, order)
        lm = p.leading_monomial()
        assert lm == (2, 1)

    def test_leading_coefficient(self):
        order = MonomialOrder()
        p = Polynomial({(1, 0): 3.0}, order)
        assert p.leading_coefficient() == 3.0

    def test_degree(self):
        order = MonomialOrder()
        p = Polynomial({(2, 1): 1.0, (1, 0): 2.0}, order)
        assert p.degree() == 3

    def test_degree_of_zero(self):
        order = MonomialOrder()
        p = Polynomial({}, order)
        assert p.degree() == -1

    def test_add(self):
        order = MonomialOrder()
        p1 = Polynomial({(1, 0): 1.0, (0, 1): 2.0}, order)
        p2 = Polynomial({(1, 0): 3.0}, order)
        result = p1.add(p2)
        assert result.coeffs[(1, 0)] == 4.0
        assert result.coeffs[(0, 1)] == 2.0

    def test_multiply(self):
        order = MonomialOrder()
        p1 = Polynomial({(1, 0): 2.0}, order)
        p2 = Polynomial({(0, 1): 3.0}, order)
        result = p1.multiply(p2)
        assert result.coeffs[(1, 1)] == 6.0

    def test_evaluate(self):
        order = MonomialOrder()
        p = Polynomial({(1, 0): 2.0, (0, 1): 3.0}, order)
        val = p.evaluate([1.0, 1.0])
        assert val == 5.0


class TestPolynomialRing:
    def test_creation(self):
        pr = PolynomialRing(3)
        assert pr.num_variables == 3
        assert len(pr.variables) == 3

    def test_zero(self):
        pr = PolynomialRing(2)
        z = pr.zero()
        assert z.is_zero() is True

    def test_one(self):
        pr = PolynomialRing(2)
        o = pr.one()
        assert o.is_zero() is False

    def test_variable(self):
        pr = PolynomialRing(3)
        x0 = pr.variable(0)
        assert x0.leading_monomial() == (1, 0, 0)
        x1 = pr.variable(1)
        assert x1.leading_monomial() == (0, 1, 0)

    def test_monomial(self):
        pr = PolynomialRing(2)
        m = pr.monomial((2, 3))
        assert m.leading_monomial() == (2, 3)


class TestGroebnerBasis:
    def test_creation(self):
        order = MonomialOrder()
        p = Polynomial({(1,): 1.0}, order)
        gb = GroebnerBasis([p], order)
        assert len(gb.polynomials) == 1

    def test_reduce(self):
        order = MonomialOrder()
        p = Polynomial({(1,): 1.0}, order)
        gb = GroebnerBasis([p], order)
        reduced = gb.reduce()
        assert len(reduced) == 1

    def test_contains(self):
        order = MonomialOrder()
        p = Polynomial({(1,): 1.0}, order)
        gb = GroebnerBasis([p], order)
        assert gb.contains(p) is False


class TestBuchbergerAlgorithm:
    def test_creation(self):
        algo = BuchbergerAlgorithm()
        assert algo.order is not None

    def test_s_polynomial(self):
        order = MonomialOrder("lex")
        p1 = Polynomial({(2, 0): 1.0}, order)
        p2 = Polynomial({(1, 1): 1.0}, order)
        algo = BuchbergerAlgorithm(order)
        sp = algo.S_polynomial(p1, p2)
        assert sp is not None

    def test_compute_basis(self):
        order = MonomialOrder("grevlex")
        p1 = Polynomial({(2, 0): 1.0, (1, 1): 1.0, (0, 2): 1.0}, order)
        algo = BuchbergerAlgorithm(order)
        gb = algo.compute_basis([p1], max_iterations=10)
        assert gb is not None


class TestPolynomialIdeal:
    def test_creation(self):
        order = MonomialOrder()
        p = Polynomial({(1,): 1.0}, order)
        ideal = PolynomialIdeal([p])
        assert len(ideal.generators) == 1

    def test_contains(self):
        order = MonomialOrder()
        p = Polynomial({(1,): 1.0}, order)
        ideal = PolynomialIdeal([p])
        assert ideal.contains(p) is False

    def test_intersection(self):
        order = MonomialOrder()
        p1 = Polynomial({(1,): 1.0}, order)
        p2 = Polynomial({(0, 1): 1.0}, order)
        ideal1 = PolynomialIdeal([p1])
        ideal2 = PolynomialIdeal([p2])
        result = ideal1.intersection(ideal2)
        assert len(result.generators) == 2

    def test_product(self):
        order = MonomialOrder()
        p1 = Polynomial({(1,): 1.0}, order)
        p2 = Polynomial({(0, 1): 1.0}, order)
        ideal1 = PolynomialIdeal([p1])
        ideal2 = PolynomialIdeal([p2])
        result = ideal1.product(ideal2)
        assert len(result.generators) == 1


class TestEliminationIdeal:
    def test_creation(self):
        order = MonomialOrder()
        p = Polynomial({(1,): 1.0}, order)
        ideal = PolynomialIdeal([p])
        elim = EliminationIdeal(ideal, [0])
        assert elim.eliminate_vars == [0]

    def test_compute_groebner_basis(self):
        order = MonomialOrder("lex")
        p = Polynomial({(1, 0): 1.0, (0, 1): 1.0}, order)
        ideal = PolynomialIdeal([p])
        elim = EliminationIdeal(ideal, [0])
        gb = elim.compute_groebner_basis(order)
        assert gb is not None


class TestIdealOperations:
    def test_intersection(self):
        order = MonomialOrder()
        p1 = Polynomial({(1,): 1.0}, order)
        p2 = Polynomial({(0, 1): 1.0}, order)
        ideal1 = PolynomialIdeal([p1])
        ideal2 = PolynomialIdeal([p2])
        result = IdealOperations.intersection(ideal1, ideal2)
        assert len(result.generators) == 2

    def test_sum(self):
        order = MonomialOrder()
        p1 = Polynomial({(1,): 1.0}, order)
        p2 = Polynomial({(0, 1): 1.0}, order)
        ideal1 = PolynomialIdeal([p1])
        ideal2 = PolynomialIdeal([p2])
        result = IdealOperations.sum(ideal1, ideal2)
        assert len(result.generators) == 2

    def test_product(self):
        order = MonomialOrder()
        p1 = Polynomial({(1,): 1.0}, order)
        p2 = Polynomial({(0, 1): 1.0}, order)
        ideal1 = PolynomialIdeal([p1])
        ideal2 = PolynomialIdeal([p2])
        result = IdealOperations.product(ideal1, ideal2)
        assert len(result.generators) == 1

    def test_radical(self):
        order = MonomialOrder()
        p = Polynomial({(2,): 1.0}, order)
        ideal = PolynomialIdeal([p])
        result = IdealOperations.radical(ideal)
        assert len(result.generators) == 1