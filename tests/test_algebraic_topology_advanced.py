"""Tests for algebraic_topology_advanced.py v1.32."""

import unittest
from lean4py.algebraic_topology_advanced import (
    FundamentalGroupoid, CoveringSpace,
    HomotopyGroup, CellComplex,
    EilenbergMacLane
)


class TestFundamentalGroupoid(unittest.TestCase):
    def test_compute(self):
        space = [(0, 0), (1, 0)]
        result = FundamentalGroupoid.compute(space)
        self.assertIn("groupoid", result)

    def test_is_equivalent_to_fundamental_group(self):
        basepoint = (0, 0)
        self.assertTrue(
            FundamentalGroupoid.is_equivalent_to_fundamental_group(basepoint)
        )


class TestCoveringSpace(unittest.TestCase):
    def test_is_covering(self):
        self.assertTrue(CoveringSpace.is_covering(lambda x: x, "E", "X"))

    def test_lifting_property(self):
        self.assertTrue(CoveringSpace.lifting_property(lambda x: x, lambda x: x))

    def test_universal_cover(self):
        result = CoveringSpace.universal_cover("X")
        self.assertIn("cover", result)


class TestHomotopyGroup(unittest.TestCase):
    def test_compute(self):
        result = HomotopyGroup.compute("X", 1)
        self.assertIn("group", result)

    def test_is_abelian_for_n_ge_2(self):
        self.assertTrue(HomotopyGroup.is_abelian_for_n_ge_2(2))


class TestCellComplex(unittest.TestCase):
    def test_build(self):
        cells = {0: 1, 1: 2, 2: 1}
        result = CellComplex.build(cells)
        self.assertIn("type", result)

    def test_suspension(self):
        result = CellComplex.suspension("X")
        self.assertIsInstance(result, str)


class TestEilenbergMacLane(unittest.TestCase):
    def test_construct(self):
        result = EilenbergMacLane.construct("Z", 1)
        self.assertIn("space", result)

    def test_classification(self):
        result = EilenbergMacLane.classification(1)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
