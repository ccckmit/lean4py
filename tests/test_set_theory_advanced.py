"""Tests for set_theory_advanced.py v1.33."""

import unittest
from lean4py.set_theory_advanced import (
    Ordinal, Cardinal, TransfiniteInduction,
    WellOrdering, AxiomOfChoice
)


class TestOrdinal(unittest.TestCase):
    def test_creation(self):
        alpha = Ordinal(5)
        self.assertIsNotNone(alpha)

    def test_zero(self):
        zero = Ordinal.zero()
        self.assertIsInstance(zero, Ordinal)

    def test_successor(self):
        alpha = Ordinal(5)
        succ = Ordinal.successor(alpha)
        self.assertIsInstance(succ, Ordinal)

    def test_is_limit(self):
        alpha = Ordinal(None)
        self.assertTrue(alpha.is_limit())


class TestCardinal(unittest.TestCase):
    def test_of_set(self):
        result = Cardinal.of_set([1, 2, 3])
        self.assertIsInstance(result, int)

    def test_aleph(self):
        result = Cardinal.aleph(0)
        self.assertIsInstance(result, str)

    def test_continuum_hypothesis(self):
        self.assertTrue(Cardinal.continuum_hypothesis())


class TestTransfiniteInduction(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(TransfiniteInduction.holds(lambda x: True))

    def test_define_by_recursion(self):
        result = TransfiniteInduction.define_by_recursion(lambda x: x)
        self.assertIn("function", result)


class TestWellOrdering(unittest.TestCase):
    def test_well_orders(self):
        self.assertTrue(WellOrdering.well_orders([1, 2, 3]))

    def test_is_well_order(self):
        self.assertTrue(WellOrdering.is_well_order(lambda x, y: x < y))


class TestAxiomOfChoice(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(AxiomOfChoice.holds())

    def test_zorns_lemma(self):
        self.assertTrue(AxiomOfChoice.zorns_lemma())

    def test_well_ordering_theorem(self):
        self.assertTrue(AxiomOfChoice.well_ordering_theorem())


if __name__ == "__main__":
    unittest.main()
