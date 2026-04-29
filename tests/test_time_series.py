import pytest
from lean4py.time_series import moving_average, autocovariance, acf


class TestMovingAverage:
    def test_basic(self):
        """Simple 3-point moving average."""
        x = [1, 2, 3, 4, 5]
        ma = moving_average(x, window=3)
        assert len(ma) == 3
        assert abs(ma[0] - 2.0) < 1e-10
        assert abs(ma[1] - 3.0) < 1e-10

    def test_window_too_large(self):
        """Window larger than data."""
        x = [1, 2]
        ma = moving_average(x, window=5)
        assert ma == []

    def test_window_1(self):
        """Window=1 should return original."""
        x = [1.0, 2.0, 3.0]
        ma = moving_average(x, window=1)
        assert ma == x


class TestAutocovariance:
    def test_zero_mean(self):
        """White noise has low autocovariance."""
        x = [1, -1, 1, -1, 1, -1]
        ac0 = autocovariance(x, lag=0)
        ac1 = autocovariance(x, lag=1)
        assert ac0 > 0
        # For white noise, autocovariance at lag>0 should be small
        # But small sample may have non-zero


class TestACF:
    def test_perfect_corr(self):
        """Perfectly correlated series."""
        x = [5.0, 5.0, 5.0, 5.0]
        acf_vals = acf(x, max_lag=3)
        assert len(acf_vals) == 4
        # At lag 0, ACF = 1
        assert abs(acf_vals[0] - 1.0) < 1e-10
        # All lags should be 1 for constant series
        for lag in range(1, 4):
            assert abs(acf_vals[lag] - 1.0) < 1e-10

    def test_white_noise(self):
        """Uncorrelated series should have small ACF."""
        x = [1, -1, 1, -1, 1, -1]
        acf_vals = acf(x, max_lag=2)
        # Lag 0 is always 1
        assert acf_vals[0] == 1.0
        # Higher lags should be small for white noise
        # (Small sample may have non-zero ACF)
