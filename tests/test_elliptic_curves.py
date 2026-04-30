"""Tests for elliptic_curves.py v1.29."""

import unittest
import math
from lean4py.elliptic_curves import (
    EllipticCurve, GroupLaw, TorsionPoint,
    Rank, Isogeny
)


class TestEllipticCurve(unittest.TestCase):
    def test_creation(self):
        E = EllipticCurve(1.0, 1.0)
        self.assertEqual(E.A, 1.0)

    def test_is_smooth(self):
        E = EllipticCurve(1.0, 1.0)
        self.assertTrue(E.is_smooth())

    def test_evaluate(self):
        E = EllipticCurve(1.0, 1.0)
        result = E.evaluate(0.0)
        self.assertIsInstance(result, list)


class TestGroupLaw(unittest.TestCase):
    def test_add(self):
        E = EllipticCurve(1.0, 1.0)
        P = (0.0, 1.0)
        Q = (1.0, math.sqrt(3.0))  # Different x-coordinate
        result = GroupLaw.add(P, Q, E)
        self.assertIsInstance(result, tuple)

    def test_double(self):
        E = EllipticCurve(1.0, 1.0)
        P = (0.0, 1.0)
        result = GroupLaw.double(P, E)
        self.assertIsInstance(result, tuple)

    def test_identity(self):
        result = GroupLaw.identity()
        self.assertEqual(result, "O")


class TestTorsionPoint(unittest.TestCase):
    def test_find(self):
        E = EllipticCurve(1.0, 1.0)
        result = TorsionPoint.find(E, 2)
        self.assertIsInstance(result, list)

    def test_order(self):
        E = EllipticCurve(1.0, 1.0)
        P = (0.0, 1.0)
        result = TorsionPoint.order(P, E)
        self.assertIsInstance(result, int)


class TestRank(unittest.TestCase):
    def test_compute(self):
        E = EllipticCurve(1.0, 1.0)
        result = Rank.compute(E)
        self.assertIsInstance(result, int)

    def test_is_finite_generated(self):
        E = EllipticCurve(1.0, 1.0)
        self.assertTrue(Rank.is_finite_generated(E))


class TestIsogeny(unittest.TestCase):
    def test_exists(self):
        E1 = EllipticCurve(1.0, 1.0)
        E2 = EllipticCurve(1.0, 1.0)
        self.assertTrue(Isogeny.exists(E1, E2))

    def test_degree(self):
        result = Isogeny.degree("phi")
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
