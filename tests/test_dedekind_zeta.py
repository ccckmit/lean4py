"""Tests for dedekind_zeta.py v1.30."""

import unittest
import cmath
from lean4py.dedekind_zeta import (
    DedekindZetaFunction, EulerProduct,
    AnalyticClassNumber, FunctionalEquation
)


class TestDedekindZetaFunction(unittest.TestCase):
    def test_creation(self):
        zeta = DedekindZetaFunction("Q")
        self.assertEqual(zeta.field, "Q")

    def test_evaluate(self):
        zeta = DedekindZetaFunction("Q")
        result = zeta.evaluate(complex(2.0, 0.0))
        self.assertIsInstance(result, complex)

    def test_euler_product(self):
        zeta = DedekindZetaFunction("Q")
        result = zeta.euler_product(complex(2.0, 0.0))
        self.assertIsInstance(result, complex)


class TestEulerProduct(unittest.TestCase):
    def test_for_dedekind(self):
        result = EulerProduct.for_dedekind("Q", complex(2.0, 0.0))
        self.assertIsInstance(result, complex)

    def test_converges_for(self):
        result = EulerProduct.converges_for("Q", complex(2.0, 0.0))
        self.assertTrue(result)


class TestAnalyticClassNumber(unittest.TestCase):
    def test_formula(self):
        result = AnalyticClassNumber.formula("Q")
        self.assertIn("class_number", result)

    def test_holds(self):
        self.assertTrue(AnalyticClassNumber.holds("Q"))


class TestFunctionalEquation(unittest.TestCase):
    def test_for_dedekind(self):
        result = FunctionalEquation.for_dedekind("Q")
        self.assertIn("equation", result)

    def test_completed_zeta(self):
        result = FunctionalEquation.completed_zeta("Q", complex(2.0, 0.0))
        self.assertIsInstance(result, complex)


if __name__ == "__main__":
    unittest.main()
