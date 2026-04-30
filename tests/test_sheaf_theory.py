"""Tests for sheaf_theory.py v1.28."""

import unittest
from lean4py.sheaf_theory import (
    Presheaf, Sheaf, Sheafification,
    GrothendieckTopology, SheafCohomology
)


class TestPresheaf(unittest.TestCase):
    def test_creation(self):
        p = Presheaf("X", "Set")
        self.assertEqual(p.space, "X")

    def test_restrict(self):
        p = Presheaf("X")
        result = p.restrict("section", "U")
        self.assertIsNotNone(result)

    def test_is_presheaf(self):
        p = Presheaf("X")
        self.assertTrue(p.is_presheaf())


class TestSheaf(unittest.TestCase):
    def test_satisfies_sheaf_condition(self):
        p = Presheaf("X")
        result = Sheaf.satisfies_sheaf_condition(p, ["U", "V"])
        self.assertTrue(result)

    def test_is_sheaf(self):
        result = Sheaf.is_sheaf("X", "Set")
        self.assertTrue(result)


class TestSheafification(unittest.TestCase):
    def test_sheafify(self):
        p = Presheaf("X")
        result = Sheafification.sheafify(p)
        self.assertIsInstance(result, Sheaf)

    def test_unit(self):
        p = Presheaf("X")
        result = Sheafification.unit(p)
        self.assertEqual(result["name"], "sheafification_unit")


class TestGrothendieckTopology(unittest.TestCase):
    def test_creation(self):
        g = GrothendieckTopology("C")
        self.assertEqual(g.category, "C")

    def test_is_covering(self):
        g = GrothendieckTopology("C")
        result = g.is_covering(["U1", "U2"], "X")
        self.assertTrue(result)

    def test_is_topology(self):
        g = GrothendieckTopology("C")
        self.assertTrue(g.is_topology())


class TestSheafCohomology(unittest.TestCase):
    def test_compute(self):
        s = Sheaf()
        result = SheafCohomology.compute(s, 1)
        self.assertEqual(result["group"], "0")

    def test_vanishing(self):
        s = Sheaf()
        result = SheafCohomology.vanishing(s, 2)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
