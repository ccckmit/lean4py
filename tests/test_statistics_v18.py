"""Tests for Mann-Kendall and Wilcoxon tests."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.statistics import (
    mann_kendall, wilcoxon_signed_rank, wilcoxon_rank_sum
)


class TestMannKendall:
    """Tests for Mann-Kendall trend test."""
    
    def test_no_trend(self):
        """Test on data with no clear trend."""
        # Random data
        x = [1.0, 2.0, 1.5, 2.5, 1.8, 2.2]
        tau, p = mann_kendall(x)
        
        assert -1 <= tau <= 1
        assert 0 <= p <= 1
    
    def test_increasing_trend(self):
        """Test on clearly increasing trend."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        tau, p = mann_kendall(x)
        
        assert tau > 0  # Should have positive tau for increasing trend
    
    def test_decreasing_trend(self):
        """Test on clearly decreasing trend."""
        x = [5.0, 4.0, 3.0, 2.0, 1.0]
        tau, p = mann_kendall(x)
        
        assert tau < 0  # Should have negative tau for decreasing trend
    
    def test_short_series(self):
        """Test on very short time series."""
        x = [1.0, 2.0]
        tau, p = mann_kendall(x)
        
        assert -1 <= tau <= 1
        assert p >= 0


class TestWilcoxonSignedRank:
    """Tests for Wilcoxon signed-rank test."""
    
    def test_symmetric_distribution(self):
        """Test on data symmetric around zero."""
        x = [-2.0, -1.0, 0.0, 1.0, 2.0]
        W, p = wilcoxon_signed_rank(x, mu=0.0)
        
        assert W >= 0
        assert 0 <= p <= 1
    
    def test_centered_at_nonzero(self):
        """Test on data centered at non-zero mu."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        W, p = wilcoxon_signed_rank(x, mu=3.0)
        
        # Differences from mu=3 are [-2, -1, 0, 1, 2]
        assert W >= 0
    
    def test_empty_data(self):
        """Test on empty data."""
        W, p = wilcoxon_signed_rank([], mu=0.0)
        
        assert W == 0.0
        assert p == 1.0


class TestWilcoxonRankSum:
    """Tests for Wilcoxon rank-sum test."""
    
    def test_similar_distributions(self):
        """Test on samples from similar distributions."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [1.5, 2.5, 3.5, 4.5, 5.5]
        
        U, p = wilcoxon_rank_sum(x, y)
        
        assert U >= 0
        assert 0 <= p <= 1
    
    def test_different_distributions(self):
        """Test on samples from different distributions."""
        x = [1.0, 2.0, 3.0]
        y = [100.0, 101.0, 102.0]
        
        U, p = wilcoxon_rank_sum(x, y)
        
        # U should be small since x values are consistently smaller
        assert U < 9  # n1 * n2 = 9
    
    def test_empty_sample(self):
        """Test on empty sample."""
        U, p = wilcoxon_rank_sum([], [1.0, 2.0])
        
        assert U == 0.0
        assert p == 1.0