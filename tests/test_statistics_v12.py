import pytest
import math
from lean4py.statistics import anova_one_way, chi_square_test


class TestANOVA:
    def test_basic(self):
        """Test ANOVA with three groups."""
        groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        F, p, eta = anova_one_way(groups)
        assert F > 0  # Should find significant difference
        assert 0 < p < 1

    def test_no_difference(self):
        """Groups with same mean should have low F."""
        groups = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
        F, p, eta = anova_one_way(groups)
        assert F == float('inf')  # Zero within-group variance

    def test_single_group(self):
        """Should return default values."""
        groups = [[1, 2, 3]]
        F, p, eta = anova_one_way(groups)
        assert F == 0.0
        assert p == 1.0


class TestChiSquare:
    def test_uniform(self):
        """Uniform distribution should have low chi2."""
        observed = [10, 10, 10, 10]
        chi2, p = chi_square_test(observed)
        assert chi2 < 1.0  # Should be close to 0
        assert p > 0.05

    def test_non_uniform(self):
        """Non-uniform should have high chi2."""
        observed = [50, 10, 10, 10]
        expected = [20, 20, 20, 20]
        chi2, p = chi_square_test(observed, expected)
        assert chi2 > 20  # Large chi-square
        assert p < 0.05  # Significant

    def test_empty(self):
        """Empty should work."""
        observed = []
        chi2, p = chi_square_test(observed)
        assert chi2 == 0.0
