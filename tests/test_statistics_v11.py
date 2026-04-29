import pytest
import math
from lean4py.statistics import t_test_one_sample, confidence_interval_mean


class TestTTestOneSample:
    def test_basic(self):
        """Test t-test with known data."""
        data = [1, 2, 3, 4, 5]
        t_stat, p_value = t_test_one_sample(data, mu0=0.0)
        assert t_stat > 0  # Mean > 0
        assert 0 < p_value < 1

    def test_fail_to_reject(self):
        """Test when mean is close to hypothesized value."""
        data = [0.1, -0.1, 0.05, -0.05, 0.02]
        t_stat, p_value = t_test_one_sample(data, mu0=0.0)
        assert p_value > 0.05  # Should not reject

    def test_empty_data(self):
        t_stat, p_value = t_test_one_sample([], mu0=0.0)
        assert t_stat == 0.0
        assert p_value == 1.0


class TestConfidenceInterval:
    def test_basic(self):
        """95% CI should contain sample mean."""
        data = [1, 2, 3, 4, 5]
        lower, upper = confidence_interval_mean(data, confidence=0.95)
        mean_val = sum(data) / len(data)
        assert lower < mean_val < upper

    def test_90_vs_95(self):
        """90% CI should be narrower than 95%."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ci_90 = confidence_interval_mean(data, confidence=0.90)
        ci_95 = confidence_interval_mean(data, confidence=0.95)
        width_90 = ci_90[1] - ci_90[0]
        width_95 = ci_95[1] - ci_95[0]
        assert width_90 < width_95

    def test_empty_data(self):
        lower, upper = confidence_interval_mean([], confidence=0.95)
        assert lower == 0.0
        assert upper == 0.0
