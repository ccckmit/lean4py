"""Statistics module: descriptive statistics and regression."""

from typing import List, Tuple, Optional
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
    """Variance."""
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


def t_test_one_sample(data: List[float], mu0: float = 0.0) -> Tuple[float, float]:
    """One-sample t-test."""
    n = len(data)
    if n < 2:
        return (0.0, 1.0)
    x_bar = mean(data)
    s = std_dev(data)
    if s == 0:
        return (float('inf'), 0.0) if x_bar != mu0 else (0.0, 1.0)
    t = (x_bar - mu0) / (s / (n ** 0.5))
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(t) / (2 ** 0.5))))
    return (t, p)


def confidence_interval_mean(data: List[float], confidence: float = 0.95) -> Tuple[float, float]:
    """Confidence interval for population mean."""
    n = len(data)
    if n < 2:
        return (0.0, 0.0)
    x_bar = mean(data)
    s = std_dev(data)
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence, 1.96)
    margin = z * s / (n ** 0.5)
    return (x_bar - margin, x_bar + margin)


def anova_one_way(groups: List[List[float]]) -> Tuple[float, float, float]:
    """One-way ANOVA."""
    k = len(groups)
    n_total = sum(len(g) for g in groups)
    
    if k < 2 or n_total <= k:
        return (0.0, 1.0, 0.0)
    
    group_means = [mean(g) for g in groups]
    overall_mean = mean([x for g in groups for x in g])
    
    SS_between = sum(len(groups[i]) * (group_means[i] - overall_mean)**2 for i in range(k))
    df_between = k - 1
    
    SS_within = sum(sum((x - group_means[i])**2 for x in groups[i]) for i in range(k))
    df_within = n_total - k
    
    if SS_within == 0:
        return (float('inf'), 0.0, 1.0)
    
    MS_between = SS_between / df_between
    MS_within = SS_within / df_within
    F = MS_between / MS_within
    
    z = (F - 1) / (2 ** 0.5)
    p = 2 * (1 - 0.5 * (1 + math.erf(z)))
    if p > 1.0:
        p = 1.0
    
    eta_sq = SS_between / (SS_between + SS_within)
    return (F, p, eta_sq)


def chi_square_test(observed: List[int], expected: Optional[List[float]] = None) -> Tuple[float, float]:
    """Chi-square goodness-of-fit test."""
    n = sum(observed)
    k = len(observed)
    
    if expected is None:
        expected = [n / k] * k
    
    chi2 = sum((observed[i] - expected[i])**2 / expected[i] for i in range(k) if expected[i] > 0)
    
    df = k - 1
    z = (chi2 - df) / (2 * df) ** 0.5
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / (2 ** 0.5))))
    
    return (chi2, p)
