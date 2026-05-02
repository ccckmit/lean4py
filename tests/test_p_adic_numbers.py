"""Tests for p_adic_numbers.py v1.30."""

import unittest
from lean4py.p_adic_numbers import (
    PadicNumber, PadicValuation,
    HenselLemma, PadicAbsoluteValue
)


class TestPadicNumber(unittest.TestCase):
    def test_creation(self):
        x = PadicNumber(5, [1, 2, 3])
        self.assertEqual(x.p, 5)

    def test_valuation(self):
        x = PadicNumber(5, [0, 1, 2])
        result = x.valuation()
        self.assertIsInstance(result, (int, float))

    def test_norm(self):
        x = PadicNumber(5, [1])
        result = x.norm()
        self.assertIsInstance(result, float)


class TestPadicValuation(unittest.TestCase):
    def test_compute(self):
        result = PadicValuation.compute(5, 25.0)
        self.assertIsInstance(result, (int, float))

    def test_is_valuation(self):
        self.assertTrue(PadicValuation.is_valuation(5))


class TestHenselLemma(unittest.TestCase):
    def test_lift(self):
        f = lambda x: x**2 - 2
        df = lambda x: 2*x
        result = HenselLemma.lift_polynomial(f, df, 5, 3, 2)
        self.assertIsInstance(result, (int, type(None)))

    def test_holds(self):
        self.assertTrue(HenselLemma.holds(5))


class TestPadicAbsoluteValue(unittest.TestCase):
    def test_compute(self):
        result = PadicAbsoluteValue.compute(5, 25.0)
        self.assertIsInstance(result, float)

    def test_is_nonarchimedean(self):
        self.assertTrue(PadicAbsoluteValue.is_nonarchimedean(5))


if __name__ == "__main__":
    unittest.main()
