"""Tests for proof_theory.py v1.33."""

import unittest
from lean4py.proof_theory import (
    Sequent, CutElimination,
    Consistency, Normalization
)


class TestSequent(unittest.TestCase):
    def test_creation(self):
        seq = Sequent(["A"], ["B"])
        self.assertIsNotNone(seq)

    def test_is_valid(self):
        seq = Sequent(["A"], ["B"])
        self.assertTrue(Sequent.is_valid(seq))

    def test_from_formula(self):
        result = Sequent.from_formula("A")
        self.assertIsInstance(result, Sequent)


class TestCutElimination(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(CutElimination.holds())

    def test_eliminate(self):
        proof = [Sequent(["A"], ["B"])]
        result = CutElimination.eliminate(proof)
        self.assertIsInstance(result, list)


class TestConsistency(unittest.TestCase):
    def test_is_consistent(self):
        self.assertTrue(Consistency.is_consistent("T"))

    def test_godel_second_theorem(self):
        self.assertTrue(Consistency.godel_second_theorem())


class TestNormalization(unittest.TestCase):
    def test_normalize(self):
        result = Normalization.normalize("proof_term")
        self.assertIsInstance(result, str)

    def test_is_normal(self):
        self.assertTrue(Normalization.is_normal("form"))


if __name__ == "__main__":
    unittest.main()
