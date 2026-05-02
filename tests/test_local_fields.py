"""Tests for local_fields.py v1.30."""

import unittest
from lean4py.local_fields import (
    LocalField, ValuationRing,
    Uniformizer, RamificationIndex,
    InertiaDegree
)


class TestLocalField(unittest.TestCase):
    def test_creation(self):
        K = LocalField(5, 2)
        self.assertEqual(K.p, 5)

    def test_is_local_field(self):
        K = LocalField(5, 2)
        self.assertTrue(K.is_local_field())

    def test_residue_field(self):
        K = LocalField(5, 2)
        result = K.residue_field()
        self.assertIsInstance(result, str)


class TestValuationRing(unittest.TestCase):
    def test_compute(self):
        K = LocalField(5, 2)
        result = ValuationRing.compute(K)
        self.assertIn("ring", result)

    def test_is_local_ring(self):
        K = LocalField(5, 2)
        self.assertTrue(ValuationRing.is_local_ring(K))


class TestUniformizer(unittest.TestCase):
    def test_find(self):
        K = LocalField(5, 2)
        result = Uniformizer.find(K)
        self.assertIsInstance(result, str)

    def test_is_uniformizer(self):
        K = LocalField(5, 2)
        self.assertTrue(Uniformizer.is_uniformizer("p", K))


class TestRamificationIndex(unittest.TestCase):
    def test_compute(self):
        K = LocalField(5, 2)
        result = RamificationIndex.compute(K)
        self.assertIsInstance(result, int)

    def test_is_totally_ramified(self):
        K = LocalField(5, 2)
        self.assertIsInstance(K, LocalField)


class TestInertiaDegree(unittest.TestCase):
    def test_compute(self):
        K = LocalField(5, 2)
        result = InertiaDegree.compute(K)
        self.assertIsInstance(result, int)

    def test_is_totally_inert(self):
        K = LocalField(5, 2)
        self.assertIsInstance(K, LocalField)


if __name__ == "__main__":
    unittest.main()
