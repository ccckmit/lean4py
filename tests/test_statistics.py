import pytest
from lean4py.statistics import (
    mean, median, mode, variance, std_dev,
    covariance, correlation, linear_regression
)


class TestMean:
    def test_mean_empty(self):
        assert mean([]) == 0.0

    def test_mean_single(self):
        assert mean([5.0]) == 5.0

    def test_mean_multiple(self):
        assert mean([1.0, 2.0, 3.0, 4.0, 5.0]) == 3.0

    def test_mean_negative(self):
        assert mean([-1.0, 1.0]) == 0.0


class TestMedian:
    def test_median_empty(self):
        assert median([]) == 0.0

    def test_median_single(self):
        assert median([5.0]) == 5.0

    def test_median_odd(self):
        assert median([1.0, 3.0, 2.0]) == 2.0

    def test_median_even(self):
        assert median([1.0, 2.0, 3.0, 4.0]) == 2.5


class TestMode:
    def test_mode_empty(self):
        assert mode([]) == []

    def test_mode_single(self):
        assert mode([5.0]) == [5.0]

    def test_mode_multiple(self):
        result = mode([1.0, 2.0, 2.0, 3.0])
        assert result == [2.0]

    def test_mode_multi_modal(self):
        result = mode([1.0, 1.0, 2.0, 2.0])
        assert 1.0 in result
        assert 2.0 in result
        assert len(result) == 2


class TestVariance:
    def test_variance_empty(self):
        assert variance([]) == 0.0

    def test_variance_single(self):
        assert variance([5.0]) == 0.0

    def test_variance_sample(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        var = variance(data)
        assert abs(var - 2.5) < 0.01

    def test_variance_population(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        var = variance(data, sample=False)
        assert abs(var - 2.0) < 0.01


class TestStdDev:
    def test_std_dev_empty(self):
        assert std_dev([]) == 0.0

    def test_std_dev_single(self):
        assert std_dev([5.0]) == 0.0

    def test_std_dev_normal(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        std = std_dev(data)
        assert abs(std - 1.581) < 0.01


class TestCovariance:
    def test_covariance_empty(self):
        assert covariance([], []) == 0.0

    def test_covariance_mismatch(self):
        assert covariance([1.0], [1.0, 2.0]) == 0.0

    def test_covariance_simple(self):
        x = [1.0, 2.0, 3.0]
        y = [2.0, 4.0, 6.0]
        cov = covariance(x, y)
        assert abs(cov - 2.0) < 0.01


class TestCorrelation:
    def test_correlation_empty(self):
        assert correlation([], []) == 0.0

    def test_correlation_mismatch(self):
        assert correlation([1.0], [1.0, 2.0]) == 0.0

    def test_correlation_perfect(self):
        x = [1.0, 2.0, 3.0]
        y = [2.0, 4.0, 6.0]
        r = correlation(x, y)
        assert abs(r - 1.0) < 0.01

    def test_correlation_negative(self):
        x = [1.0, 2.0, 3.0]
        y = [6.0, 4.0, 2.0]
        r = correlation(x, y)
        assert abs(r + 1.0) < 0.01


class TestLinearRegression:
    def test_regression_empty(self):
        slope, intercept = linear_regression([], [])
        assert slope == 0.0
        assert intercept == 0.0

    def test_regression_perfect(self):
        x = [1.0, 2.0, 3.0]
        y = [2.0, 4.0, 6.0]
        slope, intercept = linear_regression(x, y)
        assert abs(slope - 2.0) < 0.01
        assert abs(intercept) < 0.01

    def test_regression_negative(self):
        x = [1.0, 2.0, 3.0]
        y = [6.0, 4.0, 2.0]
        slope, intercept = linear_regression(x, y)
        assert abs(slope + 2.0) < 0.01
        assert abs(intercept - 8.0) < 0.01
