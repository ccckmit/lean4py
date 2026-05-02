"""Tests for arithmetic_geometry.py v1.31."""

import unittest
from lean4py.arithmetic_geometry import (
    ArithmeticScheme, NeronModel,
    ArakelovGeometry, MordellWeil
)


class TestArithmeticScheme(unittest.TestCase):
    def test_creation(self):
        X = ArithmeticScheme("Z")
        self.assertEqual(X.base, "Z")

    def test_fiber(self):
        X = ArithmeticScheme("Z")
        result = X.fiber(5)
        self.assertIsInstance(result, str)

    def test_is_proper(self):
        X = ArithmeticScheme("Z")
        self.assertTrue(X.is_proper())


class TestNeronModel(unittest.TestCase):
    def test_compute(self):
        result = NeronModel.compute("A")
        self.assertIn("model", result)
        self.assertTrue(result["is_smooth"])

    def test_is_unirational(self):
        model = {"is_smooth": True}
        self.assertTrue(NeronModel.is_unirational(model))


class TestArakelovGeometry(unittest.TestCase):
    def test_hermitian_metric(self):
        result = ArakelovGeometry.hermitian_metric(1.0)
        self.assertIsInstance(result, float)

    def test_arithmetic_degree(self):
        result = ArakelovGeometry.arithmetic_degree("L")
        self.assertIsInstance(result, float)


class TestMordellWeil(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(MordellWeil.holds("A", "Q"))

    def test_rank(self):
        result = MordellWeil.rank("A", "Q")
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
