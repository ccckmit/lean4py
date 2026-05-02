"""Tests for type_theory_advanced.py v1.33."""

import unittest
from lean4py.type_theory_advanced import (
    MartinLofType, IdentityType,
    UniversePolymorphism, HeterogeneousEquality
)


class TestMartinLofType(unittest.TestCase):
    def test_type_of_types(self):
        result = MartinLofType.type_of_types(0)
        self.assertIsInstance(result, str)

    def test_is_type(self):
        self.assertTrue(MartinLofType.is_type("A"))


class TestIdentityType(unittest.TestCase):
    def test_reflexivity(self):
        result = IdentityType.reflexivity("A", "x")
        self.assertIn("term", result)

    def test_is_equality(self):
        self.assertTrue(IdentityType.is_equality("A", "x", "y"))


class TestUniversePolymorphism(unittest.TestCase):
    def test_lift(self):
        result = UniversePolymorphism.lift("type_term", 1)
        self.assertIn("lifted", result)

    def test_is_polymorphic(self):
        self.assertTrue(UniversePolymorphism.is_polymorphic("type_term"))


class TestHeterogeneousEquality(unittest.TestCase):
    def test_make(self):
        result = HeterogeneousEquality.make("x", "y")
        self.assertIn("equality", result)

    def test_is_heterogeneous(self):
        eq_term = {"is_heterogeneous": True}
        self.assertTrue(HeterogeneousEquality.is_heterogeneous(eq_term))


if __name__ == "__main__":
    unittest.main()
