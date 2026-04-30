"""Tests for galois_theory.py v1.27."""

import unittest
from lean4py.galois_theory import (
    FieldExtension, GaloisGroup, SeparableExtension,
    NormalExtension, GaloisExtension, FundamentalTheorem,
    SolvabilityByRadicals
)


class TestFieldExtension(unittest.TestCase):
    def test_creation(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertEqual(ext.base, "Q")
        self.assertEqual(ext.degree, 2)

    def test_is_algebraic(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertTrue(ext.is_algebraic())

    def test_is_finite(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertTrue(ext.is_finite())


class TestGaloisGroup(unittest.TestCase):
    def test_compute(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        result = GaloisGroup.compute(ext)
        self.assertEqual(result["group"], "trivial")

    def test_is_abelian(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertTrue(GaloisGroup.is_abelian(ext))


class TestSeparableExtension(unittest.TestCase):
    def test_is_separable(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertTrue(SeparableExtension.is_separable(ext))


class TestNormalExtension(unittest.TestCase):
    def test_is_normal(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertTrue(NormalExtension.is_normal(ext))


class TestGaloisExtension(unittest.TestCase):
    def test_is_galois(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        self.assertTrue(GaloisExtension.is_galois(ext))


class TestFundamentalTheorem(unittest.TestCase):
    def test_intermediate_fields(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        result = FundamentalTheorem.intermediate_fields(ext)
        self.assertIsInstance(result, list)

    def test_correspondence(self):
        ext = FieldExtension("Q", "Q(√2)", degree=2)
        result = FundamentalTheorem.correspondence(ext)
        self.assertIsInstance(result, dict)


class TestSolvabilityByRadicals(unittest.TestCase):
    def test_is_solvable(self):
        self.assertTrue(SolvabilityByRadicals.is_solvable(3))
        self.assertFalse(SolvabilityByRadicals.is_solvable(5))


if __name__ == "__main__":
    unittest.main()
