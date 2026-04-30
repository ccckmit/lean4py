"""Tests for algebraic_topology.py v1.27."""

import unittest
from lean4py.algebraic_topology import (
    FundamentalGroup, Homotopy, SimplicialComplex,
    CWComplex, Homology, BettiNumber
)


class TestFundamentalGroup(unittest.TestCase):
    def test_compute(self):
        space = [(0, 0), (1, 0), (0, 1)]
        result = FundamentalGroup.compute(space, (0, 0))
        self.assertEqual(result["group_type"], "trivial")

    def test_is_trivial(self):
        space = [(0, 0), (1, 0)]
        self.assertTrue(FundamentalGroup.is_trivial(space, (0, 0)))


class TestHomotopy(unittest.TestCase):
    def test_are_homotopic(self):
        f = lambda x: x
        g = lambda x: x
        self.assertTrue(Homotopy.are_homotopic(f, g, [(0, 0)]))

    def test_homotopy_class(self):
        f = lambda x: x
        self.assertEqual(Homotopy.homotopy_class(f), "identity")


class TestSimplicialComplex(unittest.TestCase):
    def test_creation(self):
        vertices = [(0, 0), (1, 0), (0, 1)]
        simplices = [[0, 1], [1, 2], [0, 2]]
        k = SimplicialComplex(vertices, simplices)
        self.assertEqual(len(k.vertices), 3)

    def test_dimension(self):
        vertices = [(0, 0), (1, 0), (0, 1)]
        simplices = [[0, 1, 2]]
        k = SimplicialComplex(vertices, simplices)
        self.assertEqual(k.dimension(), 2)

    def test_euler_characteristic(self):
        vertices = [(0, 0), (1, 0), (0, 1)]
        simplices = [[0], [1], [2], [0, 1], [1, 2], [0, 2]]
        k = SimplicialComplex(vertices, simplices)
        self.assertIsInstance(k.euler_characteristic(), int)


class TestCWComplex(unittest.TestCase):
    def test_build_sphere(self):
        result = CWComplex.build_sphere(2)
        self.assertEqual(result["skeleton"], 2)


class TestHomology(unittest.TestCase):
    def test_compute(self):
        vertices = [(0, 0), (1, 0)]
        simplices = [[0], [1]]
        k = SimplicialComplex(vertices, simplices)
        result = Homology.compute(k, 0)
        self.assertEqual(result["group"], "0")

    def test_is_trivial(self):
        vertices = [(0, 0)]
        simplices = [[0]]
        k = SimplicialComplex(vertices, simplices)
        self.assertTrue(Homology.is_trivial(k, 0))


class TestBettiNumber(unittest.TestCase):
    def test_compute(self):
        vertices = [(0, 0), (1, 0)]
        simplices = [[0], [1]]
        k = SimplicialComplex(vertices, simplices)
        result = BettiNumber.compute(k)
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
