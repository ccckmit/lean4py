"""Tests for homological_algebra.py v1.27."""

import unittest
from lean4py.homological_algebra import (
    ChainComplex, BoundaryMap, CycleGroup,
    BoundaryGroup, HomologyGroup, ExactSequence,
    FiveLemma
)


class TestChainComplex(unittest.TestCase):
    def test_creation(self):
        groups = {0: ["a", "b"], 1: ["c"]}
        boundaries = {1: [[1.0, 0.0]]}
        chain = ChainComplex(groups, boundaries)
        self.assertEqual(len(chain.groups), 2)

    def test_get_group(self):
        groups = {0: ["a"], 1: ["b"]}
        chain = ChainComplex(groups, {})
        result = chain.get_group(0)
        self.assertEqual(len(result), 1)

    def test_get_boundary(self):
        boundaries = {1: [[1.0]]}
        chain = ChainComplex({}, boundaries)
        result = chain.get_boundary(1)
        self.assertIsInstance(result, list)


class TestBoundaryMap(unittest.TestCase):
    def test_compose(self):
        phi = [[1.0]]
        psi = [[1.0]]
        result = BoundaryMap.compose(phi, psi)
        self.assertEqual(result[0][0], 0.0)

    def test_is_zero(self):
        groups = {0: ["a"], 1: ["b"]}
        boundaries = {1: [[1.0]]}
        chain = ChainComplex(groups, boundaries)
        self.assertTrue(BoundaryMap.is_zero(chain, 1))


class TestCycleGroup(unittest.TestCase):
    def test_compute(self):
        chain = ChainComplex({0: ["a"]}, {})
        result = CycleGroup.compute(chain, 0)
        self.assertIsInstance(result, list)


class TestBoundaryGroup(unittest.TestCase):
    def test_compute(self):
        chain = ChainComplex({0: ["a"]}, {})
        result = BoundaryGroup.compute(chain, 0)
        self.assertIsInstance(result, list)


class TestHomologyGroup(unittest.TestCase):
    def test_compute(self):
        chain = ChainComplex({0: ["a"]}, {})
        result = HomologyGroup.compute(chain, 0)
        self.assertEqual(result["group"], "0")

    def test_is_trivial(self):
        chain = ChainComplex({0: ["a"]}, {})
        self.assertTrue(HomologyGroup.is_trivial(chain, 0))


class TestExactSequence(unittest.TestCase):
    def test_is_exact(self):
        chain = ChainComplex({0: ["a"]}, {})
        self.assertTrue(ExactSequence.is_exact(chain, 0))

    def test_short_exact(self):
        self.assertTrue(ExactSequence.short_exact([1], [2], [3]))


class TestFiveLemma(unittest.TestCase):
    def test_holds(self):
        self.assertTrue(FiveLemma.holds())


if __name__ == "__main__":
    unittest.main()
