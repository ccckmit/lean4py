"""Tests for formal_languages.py v1.34."""

import unittest
from lean4py.formal_languages import (
    RegularLanguage, ContextFreeGrammar,
    ChomskyHierarchy, PumpingLemma
)


class TestRegularLanguage(unittest.TestCase):
    def test_from_regex(self):
        result = RegularLanguage.from_regex("a*b")
        self.assertIn("language", result)
        self.assertTrue(result["is_regular"])

    def test_is_regular(self):
        self.assertTrue(RegularLanguage.is_regular("L"))

    def test_pumping_lemma(self):
        self.assertTrue(RegularLanguage.pumping_lemma("L"))


class TestContextFreeGrammar(unittest.TestCase):
    def test_creation(self):
        G = ContextFreeGrammar(["S"], ["a"], {"S": ["aS", ""]}, "S")
        self.assertIsNotNone(G)

    def test_is_context_free(self):
        G = ContextFreeGrammar(["S"], ["a"], {"S": ["aS", ""]}, "S")
        self.assertTrue(G.is_context_free())

    def test_generates(self):
        G = ContextFreeGrammar(["S"], ["a"], {"S": ["aS", ""]}, "S")
        self.assertTrue(G.generates("aaa"))


class TestChomskyHierarchy(unittest.TestCase):
    def test_level(self):
        result = ChomskyHierarchy.level("L")
        self.assertIsInstance(result, int)

    def test_is_strict_subset(self):
        self.assertTrue(ChomskyHierarchy.is_strict_subset(3, 2))


class TestPumpingLemma(unittest.TestCase):
    def test_for_regular(self):
        self.assertTrue(PumpingLemma.for_regular("L"))

    def test_for_context_free(self):
        self.assertTrue(PumpingLemma.for_context_free("L"))


if __name__ == "__main__":
    unittest.main()
