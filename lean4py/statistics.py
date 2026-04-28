"""Statistics module: descriptive statistics and regression."""

from typing import List, Tuple
import math


def mean(data: List[float]) -> float:
    """Arithmetic mean."""
    if not data:
        return 0.0
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """Median value."""
    if not data:
        return 0.0
    s = sorted(data)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def mode(data: List[float]) -> List[float]:
    """Mode(s) - most frequent value(s)."""
    if not data:
        return []
    from collections import Counter
    counts = Counter(data)
    max_count = max(counts.values())
    return [k for k, v in counts.items() if v == max_count]


def variance(data: List[float], sample: bool = True) -> float:
    """Variance. sample=True for sample variance (n-1), False for population."""
    if len(data) < 2:
        return 0.0
    m = mean(data)
    ss = sum((x - m) ** 2 for x in data)
    return ss / (len(data) - 1 if sample else len(data))


def std_dev(data: List[float], sample: bool = True) -> float:
    """Standard deviation."""
    return math.sqrt(variance(data, sample))


def covariance(x: List[float], y: List[float]) -> float:
    """Covariance between two variables."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    n = len(x)
    mean_x, mean_y = mean(x), mean(y)
    return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)


def correlation(x: List[float], y: List[float]) -> float:
    """Pearson correlation coefficient."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    cov = covariance(x, y)
    std_x = std_dev(x)
    std_y = std_dev(y)
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)


def linear_regression(x: List[float], y: List[float]) -> Tuple[float, float]:
    """Linear regression: y = slope * x + intercept."""
    if len(x) != len(y) or len(x) < 2:
        return (0.0, 0.0)
    n = len(x)
    sum_x, sum_y = sum(x), sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(xi ** 2 for xi in x)
    denominator = n * sum_x2 - sum_x ** 2
    if denominator == 0:
        return (0.0, mean(y))
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return (slope, intercept)


def skewness(data: List[float]) -> float:
    """Sample skewness (Fisher-Pearson)."""
    if len(data) < 3:
        return 0.0
    n = len(data)
    m = mean(data)
    s = std_dev(data)
    if s == 0:
        return 0.0
    return (n / ((n-1) * (n-2))) * sum(((x - m) / s) ** 3 for x in data)


def kurtosis(data: List[float]) -> float:
    """Sample kurtosis (excess kurtosis)."""
    if len(data) < 4:
        return 0.0
    n = len(data)
    m = mean(data)
    s = std_dev(data)
    if s == 0:
        return 0.0
    return (n*(n+1) / ((n-1)*(n-2)*(n-3))) * sum((x - m) ** 4 for x in data) / (s ** 4) - 3*(n-1)**2 / ((n-2)*(n-3))
