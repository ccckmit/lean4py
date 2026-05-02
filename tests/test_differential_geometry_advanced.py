"""Tests for differential_geometry_advanced.py v1.32."""

import unittest
from lean4py.differential_geometry_advanced import (
    Connection, Curvature,
    GeodesicAdvanced, Holonomy,
    CharacteristicClass
)


class TestConnection(unittest.TestCase):
    def test_covariant_derivative(self):
        result = Connection.covariant_derivative("X", "s")
        self.assertIsInstance(result, str)

    def test_is_metric_compatible(self):
        self.assertTrue(Connection.is_metric_compatible("M"))

    def test_torsion(self):
        result = Connection.torsion("∇")
        self.assertIn("tensor", result)


class TestCurvature(unittest.TestCase):
    def test_compute(self):
        result = Curvature.compute("∇")
        self.assertIn("tensor", result)

    def test_ricci_curvature(self):
        result = Curvature.ricci_curvature({"tensor": "R"})
        self.assertIn("tensor", result)

    def test_scalar_curvature(self):
        result = Curvature.scalar_curvature({"tensor": "Ric"})
        self.assertIsInstance(result, float)


class TestGeodesicAdvanced(unittest.TestCase):
    def test_exponential_map(self):
        result = GeodesicAdvanced.exponential_map("M", (0, 0), (1, 0))
        self.assertIsInstance(result, tuple)

    def test_jacobi_field(self):
        result = GeodesicAdvanced.jacobi_field("γ")
        self.assertIn("field", result)


class TestHolonomy(unittest.TestCase):
    def test_compute(self):
        result = Holonomy.compute("M", (0, 0))
        self.assertIn("group", result)

    def test_restricted_holonomy(self):
        result = Holonomy.restricted_holonomy("M", (0, 0))
        self.assertIsInstance(result, str)


class TestCharacteristicClass(unittest.TestCase):
    def test_chern_class(self):
        result = CharacteristicClass.chern_class("E", 1)
        self.assertIn("class", result)

    def test_pontryagin_class(self):
        result = CharacteristicClass.pontryagin_class("E", 1)
        self.assertIn("class", result)

    def test_euler_class(self):
        result = CharacteristicClass.euler_class("E")
        self.assertIn("class", result)


if __name__ == "__main__":
    unittest.main()
