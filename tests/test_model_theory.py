"""Tests for model_theory.py v1.33."""

import unittest
from lean4py.model_theory import (
    Structure, TypeSpace, CompactnessTheorem,
    LowenheimSkolem, ElementaryExtension
)


class TestStructure(unittest.TestCase):
    def test_creation(self):
        M = Structure([1, 2, 3])
        self.assertIsNotNone(M)

    def test_is_model(self):
        M = Structure([1, 2, 3])
        self.assertTrue(M.is_model("T"))


class TestTypeSpace(unittest.TestCase):
    def test_compute(self):
        result = TypeSpace.compute([1, 2, 3])
        self.assertIn("space", result)

    def test_is_compact(self):
        result = TypeSpace.compute([1])
        self.assertTrue(TypeSpace.is_compact(result))


class TestCompactnessTheorem(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(CompactnessTheorem.holds("T"))

    def test_consequence(self):
        self.assertTrue(CompactnessTheorem.consequence("phi", "T"))


class TestLowenheimSkolem(unittest.TestCase):
    def test_downward(self):
        result = LowenheimSkolem.downward("T", 5)
        self.assertEqual(result["size"], 5)

    def test_upward(self):
        result = LowenheimSkolem.upward("T", 10)
        self.assertEqual(result["size"], 10)


class TestElementaryExtension(unittest.TestCase):
    def test_is_elementary(self):
        M = Structure([1])
        N = Structure([1, 2])
        self.assertTrue(ElementaryExtension.is_elementary(M, N))

    def test_ultrapower(self):
        M = Structure([1])
        result = ElementaryExtension.ultrapower(M)
        self.assertIn("structure", result)


if __name__ == "__main__":
    unittest.main()
