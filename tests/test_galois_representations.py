"""Tests for galois_representations.py v1.31."""

import unittest
from lean4py.galois_representations import (
    GaloisRepresentation, LAdicRepresentation,
    WeilDeligneRepresentation, FontaineTheory
)


class TestGaloisRepresentation(unittest.TestCase):
    def test_creation(self):
        rho = GaloisRepresentation("Gal(Q̄/Q)", 2)
        self.assertEqual(rho.galois_group, "Gal(Q̄/Q)")
        self.assertEqual(rho.dim, 2)

    def test_is_continuous(self):
        rho = GaloisRepresentation("Gal(Q̄/Q)", 2)
        self.assertTrue(rho.is_continuous())

    def test_character(self):
        rho = GaloisRepresentation("Gal(Q̄/Q)", 2)
        result = rho.character()
        self.assertIn("identity", result)


class TestLAdicRepresentation(unittest.TestCase):
    def test_is_l_adic(self):
        self.assertTrue(LAdicRepresentation.is_l_adic(5, "Q"))

    def test_weight(self):
        result = LAdicRepresentation.weight(5)
        self.assertIsInstance(result, int)


class TestWeilDeligneRepresentation(unittest.TestCase):
    def test_creation(self):
        pi = "π"
        wd = WeilDeligneRepresentation(pi)
        self.assertEqual(wd.pi, "π")

    def test_is_representation(self):
        self.assertTrue(WeilDeligneRepresentation.is_representation("π"))


class TestFontaineTheory(unittest.TestCase):
    def test_is_de_Rham(self):
        rho = GaloisRepresentation("Gal(Q̄/Q)", 2)
        self.assertTrue(FontaineTheory.is_de_Rham(rho))

    def test_is_crystalline(self):
        rho = GaloisRepresentation("Gal(Q̄/Q)", 2)
        self.assertTrue(FontaineTheory.is_crystalline(rho))


if __name__ == "__main__":
    unittest.main()
