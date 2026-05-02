"""Tests for adeles.py v1.30."""

import unittest
from lean4py.adeles import (
    AdeleRing, FiniteAdeles,
    InfiniteAdeles, RestrictedProduct
)


class TestAdeleRing(unittest.TestCase):
    def test_creation(self):
        A = AdeleRing("Q")
        self.assertEqual(A.field, "Q")

    def test_is_ring(self):
        A = AdeleRing("Q")
        self.assertTrue(A.is_ring())

    def test_diagonal_embedding(self):
        A = AdeleRing("Q")
        result = A.diagonal_embedding(1.0)
        self.assertIn("type", result)


class TestFiniteAdeles(unittest.TestCase):
    def test_restricted_product(self):
        result = FiniteAdeles.restricted_product("Q")
        self.assertIn("type", result)

    def test_is_locally_compact(self):
        self.assertTrue(FiniteAdeles.is_locally_compact("Q"))


class TestInfiniteAdeles(unittest.TestCase):
    def test_product(self):
        result = InfiniteAdeles.product("Q")
        self.assertIn("type", result)

    def test_is_euclidean_space(self):
        self.assertTrue(InfiniteAdeles.is_euclidean_space("Q"))


class TestRestrictedProduct(unittest.TestCase):
    def test_compute(self):
        components = [("Q_2", 1), ("Q_3", 2)]
        result = RestrictedProduct.compute(components)
        self.assertIn("type", result)

    def test_is_topological_ring(self):
        components = ["Q_2", "Q_3"]
        self.assertTrue(RestrictedProduct.is_topological_ring(components))


if __name__ == "__main__":
    unittest.main()
