"""Tests for class_field_theory.py v1.29."""

import unittest
from lean4py.class_field_theory import (
    AbelianExtension, ArtinMap, ReciprocityLaw,
    IdeleClassGroup, HilbertClassField
)


class TestAbelianExtension(unittest.TestCase):
    def test_creation(self):
        ext = AbelianExtension("Q", "Q(ζ₅)")
        self.assertEqual(ext.base, "Q")

    def test_is_abelian(self):
        ext = AbelianExtension("Q", "Q(ζ₅)")
        self.assertTrue(ext.is_abelian())

    def test_conductor(self):
        ext = AbelianExtension("Q", "Q(ζ₅)")
        result = ext.conductor()
        self.assertIsInstance(result, int)


class TestArtinMap(unittest.TestCase):
    def test_compute(self):
        ext = AbelianExtension("Q", "Q(ζ₅)")
        result = ArtinMap.compute(ext, "idele")
        self.assertIsInstance(result, str)

    def test_is_surjective(self):
        ext = AbelianExtension("Q", "Q(ζ₅)")
        self.assertTrue(ArtinMap.is_surjective(ext))


class TestReciprocityLaw(unittest.TestCase):
    def test_holds(self):
        ext = AbelianExtension("Q", "Q(ζ₅)")
        self.assertTrue(ReciprocityLaw.holds(ext))

    def test_quadratic_reciprocity(self):
        self.assertTrue(ReciprocityLaw.quadratic_reciprocity())


class TestIdeleClassGroup(unittest.TestCase):
    def test_compute(self):
        result = IdeleClassGroup.compute("Q")
        self.assertIn("group", result)

    def test_is_locally_compact(self):
        self.assertTrue(IdeleClassGroup.is_locally_compact("Q"))


class TestHilbertClassField(unittest.TestCase):
    def test_compute(self):
        result = HilbertClassField.compute("Q")
        self.assertIn("field", result)

    def test_class_number(self):
        result = HilbertClassField.class_number("Q")
        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
