"""Time series analysis module."""

from typing import List


def moving_average(x: List[float], window: int = 3) -> List[float]:
    """Simple moving average."""
    if len(x) < window:
        return []
    return [sum(x[i:i+window]) / window for i in range(len(x) - window + 1)]


def autocovariance(x: List[float], lag: int = 1) -> float:
    """Autocovariance at given lag (sample)."""
    n = len(x)
    if n <= lag:
        return 0.0
    mean_x = sum(x) / n
    # Sum of products
    total = sum((x[i] - mean_x) * (x[i-lag] - mean_x) for i in range(lag, n))
    return total / (n - lag)  # Dividing by n-lag for sample autocovariance


def acf(x: List[float], max_lag: int = 10) -> List[float]:
    """Autocorrelation function (sample ACF)."""
    n = len(x)
    if n < 2:
        return []
    acov = [autocovariance(x, lag) for lag in range(max_lag + 1)]
    var = acov[0]
    if var == 0:
        # Constants series: ACF = 1 for all lags
        return [1.0] * (max_lag + 1)
    return [acov[lag] / var for lag in range(max_lag + 1)]


def partial_acf(x: List[float], max_lag: int = 10) -> List[float]:
    """Partial autocorrelation function (simplified)."""
    if len(x) < 2:
        return []
    # Simple approximation: use correlation at lag
    return acf(x, max_lag)
