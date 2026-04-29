import pytest
from lean4py.statistics import mann_whitney_u, kruskal_wallis


class TestMannWhitneyU:
    def test_basic(self):
        """Two groups with different medians."""
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 8, 9, 10]
        U, p = mann_whitney_u(x, y)
        # U should be 0 (complete separation)
        assert U == 0
        assert p < 0.05  # Should be significant

    def test_same_median(self):
        """Two groups with similar values."""
        x = [5, 5, 5, 5, 5]
        y = [5, 5, 5, 5, 5]
        U, p = mann_whitney_u(x, y)
        assert p > 0.05  # Should not be significant


class TestKruskalWallis:
    def test_basic(self):
        """Three groups with different medians."""
        groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        H, p = kruskal_wallis(groups)
        assert H > 0
        assert p < 0.05

    def test_same_values(self):
        """Groups with same values."""
        groups = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
        H, p = kruskal_wallis(groups)
        assert H == 0.0 or p > 0.05
