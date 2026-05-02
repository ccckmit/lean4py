"""Tests for algebrai_geometry_advanced.py v1.31."""

import unittest
from lean4py.algebraic_geometry_advanced import (
    Divisor, LineBundle, RiemannRoch,
    Genus, CanonicalDivisor
)


class TestDivisor(unittest.TestCase):
    def test_creation(self):
        D = Divisor({"P1": 1, "P2": -1})
        self.assertEqual(D.degree(), 0)

    def test_is_effective(self):
        D = Divisor({"P1": 1})
        self.assertTrue(D.is_effective())
        D2 = Divisor({"P1": -1})
        self.assertFalse(D2.is_effective())


class TestLineBundle(unittest.TestCase):
    def test_from_divisor(self):
        D = Divisor({"P1": 1})
        result = LineBundle.from_divisor(D)
        self.assertIn("bundle", result)

    def test_is_isomorphic(self):
        L1 = {"degree": 1}
        L2 = {"degree": 1}
        self.assertTrue(LineBundle.is_isomorphic(L1, L2))


class TestRiemannRoch(unittest.TestCase):
    def test_compute(self):
        D = Divisor({"P1": 1})
        result = RiemannRoch.compute(D, genus=0)
        self.assertIsInstance(result, int)

    def test_holds(self):
        D = Divisor({"P1": 1})
        self.assertTrue(RiemannRoch.holds(D, genus=0))


class TestGenus(unittest.TestCase):
    def test_of_curve(self):
        result = Genus.of_curve(3)
        self.assertIsInstance(result, int)

    def test_of_riemann_surface(self):
        result = Genus.of_riemann_surface(1)
        self.assertEqual(result, 1)


class TestCanonicalDivisor(unittest.TestCase):
    def test_compute(self):
        result = CanonicalDivisor.compute(genus=1)
        self.assertIsInstance(result, Divisor)

    def test_degree(self):
        result = CanonicalDivisor.degree(genus=1)
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
