"""Tests for etale_cohomology.py v1.28."""

import unittest
from lean4py.etale_cohomology import (
    EtaleSite, EtaleCohomologyGroup,
    BaseChange, WeilConjectures
)


class TestEtaleSite(unittest.TestCase):
    def test_creation(self):
        e = EtaleSite("X")
        self.assertEqual(e.scheme, "X")

    def test_is_etale_covering(self):
        result = EtaleSite.is_etale_covering(["U1", "U2"], "X")
        self.assertTrue(result)

    def test_topology(self):
        result = EtaleSite.topology()
        self.assertEqual(result["type"], "etale_topology")


class TestEtaleCohomologyGroup(unittest.TestCase):
    def test_compute(self):
        result = EtaleCohomologyGroup.compute("X", "F", 1)
        self.assertEqual(result["group"], "0")

    def test_is_finite(self):
        result = EtaleCohomologyGroup.is_finite("X", "F", 2)
        self.assertTrue(result)


class TestBaseChange(unittest.TestCase):
    def test_flat_base_change(self):
        result = BaseChange.flat_base_change("X", "f")
        self.assertTrue(result)

    def test_is_cdh_descendable(self):
        result = BaseChange.is_cdh_descendable()
        self.assertTrue(result)


class TestWeilConjectures(unittest.TestCase):
    def test_rationality(self):
        result = WeilConjectures.rationality("X", "Z")
        self.assertTrue(result)

    def test_functional_equation(self):
        result = WeilConjectures.functional_equation("X")
        self.assertTrue(result)

    def test_riemann_hypothesis(self):
        result = WeilConjectures.riemann_hypothesis("X")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
