"""Tests for homological_algebra_advanced.py v1.32."""

import unittest
from lean4py.homological_algebra_advanced import (
    SpectralSequence, DerivedFunctorAdvanced,
    ExtTorAdvanced, Hypercohomology
)


class TestSpectralSequence(unittest.TestCase):
    def test_from_filtered_complex(self):
        result = SpectralSequence.from_filtered_complex("FC")
        self.assertIn("type", result)

    def test_converges(self):
        ss = {"page": 1}
        self.assertTrue(SpectralSequence.converges(ss, "H"))


class TestDerivedFunctorAdvanced(unittest.TestCase):
    def test_left_derived(self):
        result = DerivedFunctorAdvanced.left_derived(lambda x: x, "C")
        self.assertIsNotNone(result)

    def test_right_derived(self):
        result = DerivedFunctorAdvanced.right_derived(lambda x: x, "C")
        self.assertIsNotNone(result)


class TestExtTorAdvanced(unittest.TestCase):
    def test_ext_group(self):
        result = ExtTorAdvanced.ext_group(1, "M", "N")
        self.assertIn("group", result)

    def test_tor_group(self):
        result = ExtTorAdvanced.tor_group(1, "M", "N")
        self.assertIn("group", result)


class TestHypercohomology(unittest.TestCase):
    def test_compute(self):
        result = Hypercohomology.compute("complex", "F")
        self.assertIsInstance(result, list)

    def test_coincides_with_cohomology(self):
        self.assertTrue(Hypercohomology.coincides_with_cohomology("F"))


if __name__ == "__main__":
    unittest.main()
