"""Tests for computational_complexity.py v1.34."""

import unittest
from lean4py.computational_complexity_v134 import (
    ComplexityClass, NPCompleteness,
    Reduction, CookLevin
)


class TestComplexityClass(unittest.TestCase):
    def test_P(self):
        self.assertTrue(ComplexityClass.P("L"))

    def test_NP(self):
        self.assertTrue(ComplexityClass.NP("L"))

    def test_PSPACE(self):
        self.assertTrue(ComplexityClass.PSPACE("L"))


class TestNPCompleteness(unittest.TestCase):
    def test_is_np_complete(self):
        self.assertTrue(NPCompleteness.is_np_complete("SAT"))

    def test_cook_levin(self):
        self.assertTrue(NPCompleteness.cook_levin())


class TestReduction(unittest.TestCase):
    def test_polynomial_time(self):
        self.assertTrue(Reduction.polynomial_time("L1", "L2"))

    def test_is_transitive(self):
        self.assertTrue(Reduction.is_transitive("L1", "L2", "L3"))


class TestCookLevin(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(CookLevin.holds())

    def test_reduction_to_sat(self):
        result = CookLevin.reduction_to_sat("problem")
        self.assertIn("formula", result)


if __name__ == "__main__":
    unittest.main()
