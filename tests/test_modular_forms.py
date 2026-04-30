"""Tests for modular_forms.py v1.29."""

import unittest
import cmath
from lean4py.modular_forms import (
    ModularForm, Weight, HeckeOperator,
    ModularCurve, CuspForm
)


class TestModularForm(unittest.TestCase):
    def test_creation(self):
        f = ModularForm(12)
        self.assertEqual(f.weight, 12)

    def test_evaluate(self):
        f = ModularForm(12)
        result = f.evaluate(cmath.sqrt(-1))
        self.assertIsInstance(result, complex)

    def test_is_modular(self):
        f = ModularForm(12)
        self.assertTrue(f.is_modular())


class TestWeight(unittest.TestCase):
    def test_get(self):
        f = ModularForm(12)
        result = Weight.get(f)
        self.assertEqual(result, 12)

    def test_is_even(self):
        self.assertTrue(Weight.is_even(12))
        self.assertFalse(Weight.is_even(13))


class TestHeckeOperator(unittest.TestCase):
    def test_apply(self):
        f = ModularForm(12)
        result = HeckeOperator.apply(5, f)
        self.assertEqual(result["operator"], "T_5")

    def test_eigenvalues(self):
        f = ModularForm(12)
        result = HeckeOperator.eigenvalues(f, 5)
        self.assertIsInstance(result, list)


class TestModularCurve(unittest.TestCase):
    def test_compactification(self):
        result = ModularCurve.compactification("SL2Z")
        self.assertIn("curve", result)

    def test_genus(self):
        result = ModularCurve.genus("SL2Z")
        self.assertIsInstance(result, int)


class TestCuspForm(unittest.TestCase):
    def test_is_cusp_form(self):
        f = ModularForm(12)
        self.assertTrue(CuspForm.is_cusp_form(f))

    def test_dimension(self):
        result = CuspForm.dimension(12)
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
