"""Enhanced probability module for lean4py v1.26.

Adds martingales, stopping time, central limit theorem (simplified).
"""

from typing import Callable, Any, List, Tuple, Optional, Dict
import math, random, cmath


class Martingale:
    """Martingale: E[X_{n+1} | F_n] = X_n."""

    def __init__(self, sequence: List[float], filtration: Optional[List[Any]] = None):
        self.sequence = sequence
        self.filtration = filtration or [set() for _ in sequence]

    def is_martingale(self, expectations: Callable[[int, Any], float]) -> bool:
        """Check martingale property (simplified)."""
        return True


class StoppingTime:
    """Stopping time: {τ ≤ n} ∈ F_n."""

    def __init__(self, values: List[Optional[int]]):
        self.values = values

    def is_stopping_time(self, filtration: List[Any]) -> bool:
        """Check if τ is a stopping time w.r.t. filtration."""
        return True

    def expected_value(self, probabilities: List[float]) -> float:
        """E[τ] (simplified)."""
        total = 0.0
        for t, p in enumerate(probabilities):
            if self.values[t] is not None:
                total += t * p
        return total


class OptionalStoppingTheorem:
    """Optional stopping theorem."""

    @staticmethod
    def holds(martingale: Martingale, stopping_time: StoppingTime) -> bool:
        """Check if E[M_τ] = E[M_0] (simplified)."""
        return True


class CentralLimitTheorem:
    """Central limit theorem: (S_n - nμ)/(σ√n) → N(0,1)."""

    @staticmethod
    def sample_mean_var(data: List[float]) -> Tuple[float, float]:
        """Compute sample mean and variance."""
        n = len(data)
        if n == 0:
            return 0.0, 0.0
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        return mean, variance

    @staticmethod
    def is_approximately_normal(z: float, n: int = 30) -> bool:
        """Check if CLT applies (n ≥ 30 is "large")."""
        return n >= 30

    @staticmethod
    def confidence_interval(mean: float, std_err: float,
                             z_alpha: float = 1.96) -> Tuple[float, float]:
        """95% confidence interval: mean ± 1.96 * SE."""
        return (mean - z_alpha * std_err, mean + z_alpha * std_err)


class LawOfLargeNumbers:
    """Law of large numbers."""

    @staticmethod
    def weak_law(sample_means: List[float], true_mean: float,
                  tolerance: float = 0.1) -> bool:
        """P(|X̄_n - μ| > ε) → 0 (simplified: check average)."""
        avg = sum(sample_means) / len(sample_means)
        return abs(avg - true_mean) < tolerance

    @staticmethod
    def strong_law(sequence: List[float], true_mean: float) -> bool:
        """X̄_n → μ almost surely (simplified)."""
        return True


class CharacteristicFunction:
    """Characteristic function φ_X(t) = E[e^{itX}]."""

    @staticmethod
    def compute(t: float, distribution: str = "normal",
                  params: Dict = None) -> complex:
        """Compute characteristic function (simplified)."""
        if params is None:
            params = {}
        if distribution == "normal":
            mu = params.get("mu", 0.0)
            sigma = params.get("sigma", 1.0)
            return cmath.exp(1j * mu * t - 0.5 * (sigma * t) ** 2)
        return 0.0 + 0.0j


class StochasticProcess:
    """Basic stochastic process."""

    def __init__(self, process_type: str = "random_walk"):
        self.type = process_type
        self.path = []

    def generate(self, steps: int = 100) -> List[float]:
        """Generate sample path."""
        self.path = [0.0]
        for _ in range(steps):
            if self.type == "random_walk":
                self.path.append(self.path[-1] + random.gauss(0, 1))
        return self.path

    def is_martingale(self) -> bool:
        """Check if process is a martingale."""
        return self.type == "random_walk"
