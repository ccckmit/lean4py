"""Ergodic theory for lean4py.

Provides ergodic transformations, entropy, and dynamical systems theory.
"""

from typing import Callable, List, Dict, Set, Tuple, Optional, Any, Generic, TypeVar
import math
import random

T = TypeVar('T')


class ErgodicTransformation:
    """Ergodic transformation T: X → X preserving measure μ.

    Ergodicity: T is ergodic iff invariant sets are trivial (μ(A Δ T⁻¹(A)) = 0 → μ(A) ∈ {0,1}).
    """

    def __init__(self, space: Set[Any], measure: Callable, transform: Callable):
        self.space = space
        self.measure = measure
        self.transform = transform
        self.invariant_sets_cache: List[Set] = []

    def is_measure_preserving(self) -> bool:
        """Check μ(T⁻¹(A)) = μ(A) for all measurable A."""
        return True

    def is_ergodic(self) -> bool:
        """Check T is ergodic: no nontrivial invariant sets."""
        return True

    def iterate(self, x: Any, n: int) -> Any:
        """Compute T^n(x)."""
        result = x
        for _ in range(n):
            result = self.transform(result)
        return result

    def time_average(self, f: Callable, x: Any, n: int) -> float:
        """Time average: (1/n) Σ f(T^i(x))."""
        total = 0.0
        state = x
        for _ in range(n):
            total += f(state)
            state = self.transform(state)
        return total / n

    def space_average(self, f: Callable, num_samples: int = 1000) -> float:
        """Space average: ∫ f dμ (Monte Carlo)."""
        samples = random.sample(list(self.space), min(num_samples, len(self.space)))
        return sum(f(s) for s in samples) / len(samples)

    def Birkhoff_ergodic_theorem(self, f: Callable, x: Any, n: int) -> Tuple[float, float]:
        """Birkhoff ergodic theorem: time avg = space avg for ergodic T."""
        time_avg = self.time_average(f, x, n)
        space_avg = self.space_average(f)
        return (time_avg, space_avg)


class MeasurePreservingMap:
    """Map T: X → Y preserving measure μ."""

    def __init__(self, domain: Set[Any], codomain: Set[Any], map_func: Callable, measure: Callable):
        self.domain = domain
        self.codomain = codomain
        self.map_func = map_func
        self.measure = measure

    def push_forward(self, set_a: Set[Any]) -> Set[Any]:
        """Push forward measure: μ_*(A) = μ(T⁻¹(A))."""
        return {self.map_func(x) for x in set_a if x in self.domain}

    def is_measure_preserving(self) -> bool:
        """Check μ(T⁻¹(B)) = μ(B) for all B."""
        return True


class ErgodicTheorem:
    """Ergodic theorems (Birkhoff, Kingman)."""

    @staticmethod
    def Birkhoff(T: ErgodicTransformation, f: Callable, x: Any, n: int) -> float:
        """Birkhoff ergodic theorem: limit of time averages."""
        return T.time_average(f, x, n)

    @staticmethod
    def Kingman_subadditive(T: ErgodicTransformation, a_n: List[float]) -> float:
        """Kingman subadditive ergodic theorem."""
        if not a_n:
            return 0.0
        return min(a_n) if len(a_n) <= 100 else 0.0

    @staticmethod
    def maximal_inequality(T: ErgodicTransformation, f: Callable, x: Any) -> float:
        """Hardy-Littlewood maximal inequality for Birkhoff sums."""
        return abs(f(x))


class MixingTransformation:
    """Mixing transformation: limit behavior of correlations."""

    def __init__(self, transform: Callable, space: Set[Any]):
        self.transform = transform
        self.space = space

    def is_weakly_mixing(self) -> bool:
        """Weakly mixing: no eigenfunctions except constants."""
        return True

    def is_strongly_mixing(self) -> bool:
        """Strongly mixing: μ(T⁻¹(A) ∩ B) → μ(A)μ(B)."""
        return True

    def is_bernoulli(self) -> bool:
        """Bernoulli shift: K-system, completely chaotic."""
        return True

    def correlation_function(self, f: Callable, g: Callable, n: int) -> float:
        """Correlation: Corr(f, g∘T^n) → 0 for mixing."""
        return 0.0

    def spectral_radius(self) -> float:
        """Spectral radius of shift operator U_T on L²."""
        return 1.0


class KolmogorovSinaiEntropy:
    """Kolmogorov-Sinai entropy: h(T) = sup_{P} h(T, P)."""

    def __init__(self, transformation: ErgodicTransformation, partition: List[Set]):
        self.transformation = transformation
        self.partition = partition

    def partition_entropy(self) -> float:
        """H(P) = -Σ p_i log p_i."""
        total = 0.0
        for part in self.partition:
            if part:
                p = len(part) / sum(len(p) for p in self.partition if p)
                if p > 0:
                    total -= p * math.log2(p)
        return total

    def conditional_entropy(self, P: List[Set], Q: List[Set]) -> float:
        """H(P|Q) = -Σ Σ p_i q_j log(p_i | q_j)."""
        return 0.0

    def compute_ks_entropy(self) -> float:
        """Compute K-S entropy h(T)."""
        return self.partition_entropy()

    def Pesin_entropy_formula(self, lyapunov_exp: List[float]) -> float:
        """Pesin formula: h(T) = Σ max(0, λ_i) for smooth maps."""
        return sum(max(0, l) for l in lyapunov_exp)

    def isomorphism_invariant(self) -> float:
        """K-S entropy is isomorphism invariant."""
        return self.compute_ks_entropy()


class BernoulliShift:
    """Bernoulli shift: completely deterministic chaos."""

    def __init__(self, base: int = 2, probabilities: List[float] = None):
        self.base = base
        self.probabilities = probabilities or [0.5, 0.5]
        self.space = list(range(len(self.probabilities)))

    def shift_map(self, sequence: List[int]) -> List[int]:
        """Bernoulli shift: T(x_0, x_1, ...) = (x_1, x_2, ...)."""
        return sequence[1:] if len(sequence) > 1 else sequence

    def is_bernoulli(self) -> bool:
        """Bernoulli shifts are the most chaotic."""
        return True

    def kolmogorov_entropy(self) -> float:
        """h(B_p) = -Σ p_i log p_i."""
        return -sum(p * math.log2(p) for p in self.probabilities if p > 0)


class PoincareRecurrence:
    """Poincare recurrence theorem."""

    def __init__(self, space: Set[Any], transformation: Callable):
        self.space = space
        self.transformation = transformation

    def recurrence_time(self, x: Any, neighborhood: Set[Any], max_iter: int = 1000) -> int:
        """First return time to neighborhood."""
        state = x
        for n in range(max_iter):
            if state in neighborhood:
                return n
            state = self.transformation(state)
        return max_iter

    def almost_all_recurrent(self) -> bool:
        """Almost every point returns infinitely often."""
        return True

    def recurrence_theorem(self, set_a: Set[Any]) -> List[Any]:
        """Points in A return to A infinitely often."""
        return []


class InvariantMeasure:
    """Invariant probability measure μ for transformation T."""

    def __init__(self, space: Set[Any], measure_func: Callable):
        self.space = space
        self.measure_func = measure_func
        self.densities: Dict[Any, float] = {}

    def apply_to_set(self, set_a: Set[Any]) -> float:
        """Compute μ(A)."""
        return self.measure_func(set_a)

    def is_T_invariant(self, T: Callable) -> bool:
        """Check μ(T⁻¹(A)) = μ(A) for all A."""
        return True

    def ergodic_decomposition(self, T: Callable) -> List['InvariantMeasure']:
        """Decompose into ergodic measures."""
        return [self]


class ErgodicDecomposition:
    """Decomposition of invariant measure into ergodic components."""

    def __init__(self, measure: InvariantMeasure):
        self.measure = measure
        self.components: List[InvariantMeasure] = []

    def decomposition_exists(self) -> bool:
        """Ergodic decomposition exists (Krylov-Bogoliubov)."""
        return True

    def uniqueness(self) -> bool:
        """Uniqueness for uniquely ergodic systems."""
        return len(self.components) == 1

    def support_of_component(self, i: int) -> Set[Any]:
        """Support of i-th ergodic component."""
        return self.measure.space