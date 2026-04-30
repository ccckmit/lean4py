"""Tests for l_functions.py v1.29."""

import unittest
import cmath
from lean4py.l_functions import (
    RiemannZeta, DirichletLFunction,
    FunctionalEquation, AnalyticContinuation,
    EulerProduct
)


class TestRiemannZeta(unittest.TestCase):
    def test_evaluate(self):
        result = RiemannZeta.evaluate(complex(2.0, 0.0))  # Re(s) > 1
        self.assertIsInstance(result, complex)

    def test_trivial_zeros(self):
        result = RiemannZeta.trivial_zeros()
        self.assertIsInstance(result, list)

    def test_critical_line(self):
        self.assertTrue(RiemannZeta.critical_line())


class TestDirichletLFunction(unittest.TestCase):
    def test_creation(self):
        chi = {1: 1.0, 3: -1.0}
        L = DirichletLFunction(chi, 4)
        self.assertEqual(L.modulus, 4)

    def test_evaluate(self):
        chi = {1: 1.0, 3: -1.0}
        L = DirichletLFunction(chi, 4)
        result = L.evaluate(cmath.sqrt(-1))
        self.assertIsInstance(result, complex)

    def test_is_entire(self):
        chi = {1: 1.0}
        L = DirichletLFunction(chi, 1)
        self.assertTrue(L.is_entire())


class TestFunctionalEquation(unittest.TestCase):
    def test_for_zeta(self):
        result = FunctionalEquation.for_zeta()
        self.assertIn("equation", result)

    def test_for_dirichlet(self):
        result = FunctionalEquation.for_dirichlet()
        self.assertIn("equation", result)


class TestAnalyticContinuation(unittest.TestCase):
    def test_continue_zeta(self):
        result = AnalyticContinuation.continue_zeta(cmath.sqrt(-1))
        self.assertIsInstance(result, complex)

    def test_continue_dirichlet(self):
        chi = {1: 1.0}
        result = AnalyticContinuation.continue_dirichlet(cmath.sqrt(-1), chi)
        self.assertIsInstance(result, complex)


class TestEulerProduct(unittest.TestCase):
    def test_for_zeta(self):
        result = EulerProduct.for_zeta(cmath.sqrt(-1))
        self.assertIsInstance(result, complex)

    def test_for_dirichlet(self):
        chi = {1: 1.0}
        result = EulerProduct.for_dirichlet(cmath.sqrt(-1), chi)
        self.assertIsInstance(result, complex)


if __name__ == "__main__":
    unittest.main()
