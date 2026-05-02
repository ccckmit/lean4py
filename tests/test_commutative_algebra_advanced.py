"""Tests for commutative_algebra_advanced.py v1.32."""

import unittest
from lean4py.commutative_algebra_advanced import (
    Localization, PrimaryDecomposition,
    NoetherianRing, IntegralClosure,
    DedekindDomain
)


class TestLocalization(unittest.TestCase):
    def test_compute(self):
        result = Localization.compute("Z")
        self.assertIn("ring", result)
        self.assertTrue(result["is_local"])

    def test_is_local_ring(self):
        self.assertTrue(Localization.is_local_ring("Z", "pZ"))


class TestPrimaryDecomposition(unittest.TestCase):
    def test_decompose(self):
        result = PrimaryDecomposition.decompose("I")
        self.assertIsInstance(result, list)

    def test_is_primary(self):
        self.assertTrue(PrimaryDecomposition.is_primary("Q"))


class TestNoetherianRing(unittest.TestCase):
    def test_is_noetherian(self):
        self.assertTrue(NoetherianRing.is_noetherian("Z"))

    def test_hilbert_basis_theorem(self):
        self.assertTrue(NoetherianRing.hilbert_basis_theorem("Z"))


class TestIntegralClosure(unittest.TestCase):
    def test_compute(self):
        result = IntegralClosure.compute("Z")
        self.assertIn("closure", result)

    def test_is_integrally_closed(self):
        self.assertTrue(IntegralClosure.is_integrally_closed("Z"))


class TestDedekindDomain(unittest.TestCase):
    def test_is_dedekind(self):
        self.assertTrue(DedekindDomain.is_dedekind("Z"))

    def test_unique_factorization(self):
        result = DedekindDomain.unique_factorization("I")
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
