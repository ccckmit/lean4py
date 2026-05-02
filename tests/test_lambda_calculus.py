"""Tests for lambda_calculus.py v1.34."""

import unittest
from lean4py.lambda_calculus import (
    LambdaTerm, BetaReduction,
    SimplyTypedLambda, ChurchNumerals
)


class TestLambdaTerm(unittest.TestCase):
    def test_variable(self):
        result = LambdaTerm.variable("x")
        self.assertIn("term", result)

    def test_abstraction(self):
        var = LambdaTerm.variable("x")
        result = LambdaTerm.abstraction("x", var)
        self.assertIn("term", result)

    def test_application(self):
        func = LambdaTerm.variable("f")
        arg = LambdaTerm.variable("x")
        result = LambdaTerm.application(func, arg)
        self.assertIn("term", result)


class TestBetaReduction(unittest.TestCase):
    def test_beta_reduce(self):
        term = {"term": "λx.x", "type": "abstraction"}
        result = BetaReduction.beta_reduce(term)
        self.assertIsNotNone(result)

    def test_is_beta_normal(self):
        term = {"term": "x", "type": "variable"}
        self.assertTrue(BetaReduction.is_beta_normal(term))

    def test_church_rosser(self):
        self.assertTrue(BetaReduction.church_rosser())


class TestSimplyTypedLambda(unittest.TestCase):
    def test_type_of(self):
        term = {"term": "x"}
        result = SimplyTypedLambda.type_of(term, {})
        self.assertIsInstance(result, (str, type(None)))

    def test_is_typed(self):
        term = {"term": "x"}
        self.assertTrue(SimplyTypedLambda.is_typed(term))


class TestChurchNumerals(unittest.TestCase):
    def test_encode(self):
        result = ChurchNumerals.encode(3)
        self.assertIn("term", result)

    def test_decode(self):
        num = {"term": "λf.λx.f(f(f(x)))", "value": 3}
        result = ChurchNumerals.decode(num)
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
