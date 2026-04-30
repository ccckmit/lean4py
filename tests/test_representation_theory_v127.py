"""Tests for representation_theory.py v1.27."""

import unittest
from lean4py.representation_theory_v127 import (
    Representation, Character, IrreducibleRepresentation,
    MaschkeTheorem, SchurLemma, Decomposition
)


class TestRepresentation(unittest.TestCase):
    def test_creation(self):
        rep = Representation("S3", 2)
        self.assertEqual(rep.group, "S3")
        self.assertEqual(rep.dim, 2)

    def test_character(self):
        rep = Representation("S3", 2)
        result = rep.character("identity")
        self.assertIsInstance(result, complex)

    def test_is_irreducible(self):
        rep = Representation("S3", 1)
        self.assertTrue(rep.is_irreducible())


class TestCharacter(unittest.TestCase):
    def test_compute(self):
        rep = Representation("S3", 2)
        result = Character.compute(rep)
        self.assertIsInstance(result, dict)

    def test_is_irreducible(self):
        rep = Representation("S3", 1)
        char = Character.compute(rep)
        self.assertTrue(Character.is_irreducible(char, 6))

    def test_inner_product(self):
        char1 = {"identity": 1.0}
        char2 = {"identity": 1.0}
        result = Character.inner_product(char1, char2, 6)
        self.assertIsInstance(result, float)


class TestIrreducibleRepresentation(unittest.TestCase):
    def test_decompose(self):
        rep = Representation("S3", 2)
        result = IrreducibleRepresentation.decompose(rep)
        self.assertIsInstance(result, list)


class TestMaschkeTheorem(unittest.TestCase):
    def test_is_semisimple(self):
        self.assertTrue(MaschkeTheorem.is_semisimple(6))


class TestSchurLemma(unittest.TestCase):
    def test_is_scalar(self):
        rep = Representation("S3", 1)
        endo = [[1.0]]
        self.assertTrue(SchurLemma.is_scalar(endo, rep))


class TestDecomposition(unittest.TestCase):
    def test_direct_sum(self):
        rep1 = Representation("S3", 1)
        rep2 = Representation("S3", 1)
        result = Decomposition.direct_sum([rep1, rep2])
        self.assertEqual(result.dim, 2)


if __name__ == "__main__":
    unittest.main()
