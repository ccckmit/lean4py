"""Tests for automorphic_forms.py v1.31."""

import unittest
import cmath
from lean4py.automorphic_forms import (
    AutomorphicForm, HeckeOperatorGeneral,
    LanglandsFunctioriality, LFunction
)


class TestAutomorphicForm(unittest.TestCase):
    def test_creation(self):
        f = AutomorphicForm("GL(2)", weight=12)
        self.assertEqual(f.group, "GL(2)")

    def test_evaluate(self):
        f = AutomorphicForm()
        result = f.evaluate(cmath.sqrt(-1))
        self.assertIsInstance(result, complex)

    def test_is_automorphic(self):
        f = AutomorphicForm()
        self.assertTrue(f.is_automorphic())


class TestHeckeOperatorGeneral(unittest.TestCase):
    def test_apply(self):
        f = AutomorphicForm()
        result = HeckeOperatorGeneral.apply(5, f)
        self.assertIn("operator", result)

    def test_eigenvalues(self):
        f = AutomorphicForm()
        result = HeckeOperatorGeneral.eigenvalues(f, 5)
        self.assertIsInstance(result, list)


class TestLanglandsFunctioriality(unittest.TestCase):
    def test_transfer(self):
        f = AutomorphicForm()
        result = LanglandsFunctioriality.transfer("GL(2)", "GL(3)", f)
        self.assertIn("source", result)

    def test_holds(self):
        self.assertTrue(LanglandsFunctioriality.holds())


class TestLFunction(unittest.TestCase):
    def test_compute(self):
        f = AutomorphicForm()
        result = LFunction.compute(f, complex(2.0, 0.0))
        self.assertIsInstance(result, complex)

    def test_analytic_continuation(self):
        f = AutomorphicForm()
        self.assertTrue(LFunction.analytic_continuation(f))


if __name__ == "__main__":
    unittest.main()
