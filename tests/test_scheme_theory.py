"""Tests for scheme_theory.py v1.28."""

import unittest
from lean4py.scheme_theory import (
    AffineScheme, ProjectiveScheme, SchemeMorphism,
    FiberProduct, ProperMorphism
)


class TestAffineScheme(unittest.TestCase):
    def test_creation(self):
        a = AffineScheme("Z")
        self.assertEqual(a.ring, "Z")

    def test_spectrum(self):
        result = AffineScheme.spectrum("Q")
        self.assertEqual(result["type"], "affine_scheme")

    def test_is_affine(self):
        self.assertTrue(AffineScheme.is_affine())


class TestProjectiveScheme(unittest.TestCase):
    def test_creation(self):
        p = ProjectiveScheme("Z", 2)
        self.assertEqual(p.dim, 2)

    def test_projective_space(self):
        result = ProjectiveScheme.projective_space(3, "Z")
        self.assertEqual(result["type"], "projective_space")

    def test_is_proper(self):
        self.assertTrue(ProjectiveScheme.is_proper())


class TestSchemeMorphism(unittest.TestCase):
    def test_creation(self):
        f = SchemeMorphism("X", "Y")
        self.assertEqual(f.source, "X")

    def test_is_continuous(self):
        f = SchemeMorphism("X", "Y")
        self.assertTrue(f.is_continuous())

    def test_is_morphism(self):
        f = SchemeMorphism("X", "Y")
        self.assertTrue(f.is_morphism())


class TestFiberProduct(unittest.TestCase):
    def test_compute(self):
        result = FiberProduct.compute("X", "Y", "Z", lambda x: x, lambda x: x)
        self.assertEqual(result["type"], "fiber_product")


class TestProperMorphism(unittest.TestCase):
    def test_is_proper(self):
        f = SchemeMorphism("X", "Y")
        self.assertTrue(ProperMorphism.is_proper(f))

    def test_valuation_criterion(self):
        f = SchemeMorphism("X", "Y")
        self.assertTrue(ProperMorphism.valuation_criterion(f))


if __name__ == "__main__":
    unittest.main()
