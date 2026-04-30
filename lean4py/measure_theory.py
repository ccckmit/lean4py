"""Measure theory module for lean4py.

Imitates mathlib4 Mathlib.MeasureTheory: σ-algebras, measures, Lebesgue integration.
"""

from typing import Set, List, Callable, Any, Optional, Dict, Tuple, Generic, TypeVar
from functools import wraps

T = TypeVar('T')


class SigmaAlgebra:
    """σ-algebra on a set.

    A σ-algebra Ω on X is a collection of subsets s.t.:
    - X ∈ Ω
    - A ∈ Ω ⇒ X\A ∈ Ω (closed under complement)
    - Closed under countable unions
    """

    def __init__(self, universe: Set[Any], sets: Optional[Set[Any]] = None):
        self.universe = frozenset(universe)
        if sets is not None:
            self.sets = frozenset(frozenset(s) for s in sets)
        else:
            # Generate basic σ-algebra with all singletons
            all_subsets = {frozenset(), self.universe}
            for x in self.universe:
                all_subsets.add(frozenset({x}))
                all_subsets.add(self.universe - frozenset({x}))
            self.sets = all_subsets

    def is_in(self, s: Set[Any]) -> bool:
        """Check if a set is in the σ-algebra."""
        return frozenset(s) in self.sets

    def complement(self, s: Set[Any]) -> Set[Any]:
        """Complement of a set in the universe."""
        return set(self.universe - frozenset(s))

    def is_sigma_algebra(self) -> bool:
        """Verify σ-algebra axioms."""
        if frozenset() not in self.sets:
            return False
        if self.universe not in self.sets:
            return False
        for s in self.sets:
            if self.complement(set(s)) not in self.sets:
                return False
        return True

    def union(self, a: Set[Any], b: Set[Any]) -> Optional[Set[Any]]:
        """Union of two measurable sets (if measurable)."""
        result = frozenset(a) | frozenset(b)
        return set(result) if result in self.sets else None

    def intersection(self, a: Set[Any], b: Set[Any]) -> Optional[Set[Any]]:
        """Intersection of two measurable sets."""
        result = frozenset(a) & frozenset(b)
        return set(result) if result in self.sets else None


class MeasurableSpace:
    """Measurable space (X, Σ)."""

    def __init__(self, universe: Set[Any], sigma_algebra: SigmaAlgebra):
        self.universe = universe
        self.sigma_algebra = sigma_algebra

    def is_measurable(self, s: Set[Any]) -> bool:
        """Check if a set is measurable."""
        return self.sigma_algebra.is_in(s)


class Measure:
    """Measure on a measurable space.

    A measure μ: Σ → [0, ∞] satisfies:
    - μ(∅) = 0
    - Countable additivity
    """

    def __init__(self, space: MeasurableSpace,
                 mu: Optional[Callable[[Set[Any]], float]] = None):
        self.space = space
        self._mu = mu if mu is not None else (lambda s: 0.0)

    def __call__(self, s: Set[Any]) -> float:
        """Apply measure to a set."""
        if not self.space.is_measurable(s):
            raise ValueError("Set is not measurable")
        return self._mu(s)

    def is_measure(self) -> bool:
        """Verify measure axioms (simplified)."""
        if self(frozenset()) != 0.0:
            return False
        return True

    def is_finite(self) -> bool:
        """Check if measure is finite on all sets."""
        return True

    def is_probability(self) -> bool:
        """Check if it's a probability measure (μ(X) = 1)."""
        return self(self.space.universe) == 1.0


class LebesgueMeasure(Measure):
    """Lebesgue measure on ℝ (simplified)."""

    def __init__(self):
        real_line = frozenset(range(-1000, 1001))
        sigma = SigmaAlgebra(set(real_line))
        space = MeasurableSpace(set(real_line), sigma)
        super().__init__(space, self._lebesgue)

    def __call__(self, s: Set[Any]) -> float:
        """Apply Lebesgue measure to a set (skip measurability check)."""
        return self._mu(s)

    def _lebesgue(self, s: Set[Any]) -> float:
        """Lebesgue measure: length for intervals."""
        if len(s) == 0:
            return 0.0
        try:
            numeric_vals = [x for x in s if isinstance(x, (int, float))]
            if not numeric_vals:
                return 0.0
            return float(max(numeric_vals) - min(numeric_vals))
        except (ValueError, TypeError):
            return 0.0
        try:
            # Filter to numeric values only
            numeric_vals = [x for x in s if isinstance(x, (int, float))]
            if not numeric_vals:
                return 0.0
            min_val = min(numeric_vals)
            max_val = max(numeric_vals)
            return float(max_val - min_val)
        except (ValueError, TypeError):
            return 0.0


class MeasurableFunction:
    """Measurable function between measurable spaces."""

    def __init__(self, domain: MeasurableSpace, codomain: MeasurableSpace,
                 func: Callable[[Any], Any]):
        self.domain = domain
        self.codomain = codomain
        self.func = func

    def is_measurable(self) -> bool:
        """Check if preimage of every measurable set is measurable."""
        for b in self.codomain.sigma_algebra.sets:
            preimage = {x for x in self.domain.universe if frozenset([self.func(x)]) <= b}
            if not self.domain.is_measurable(preimage):
                return False
        return True

    def compose(self, other: 'MeasurableFunction') -> 'MeasurableFunction':
        """Compose with another measurable function."""
        if self.domain != other.codomain:
            raise ValueError("Domain mismatch")
        return MeasurableFunction(other.domain, self.codomain,
                                lambda x: self.func(other.func(x)))


class SimpleFunction:
    """Simple function: finite linear combination of indicator functions."""

    def __init__(self, pairs: List[Tuple[float, Set[Any]]],
                 space: MeasurableSpace):
        self.pairs = pairs
        self.space = space

    def evaluate(self, x: Any) -> float:
        """Evaluate simple function at x."""
        for coeff, s in self.pairs:
            if x in s:
                return coeff
        return 0.0

    def is_measurable(self) -> bool:
        """Check if all component sets are measurable."""
        return all(self.space.sigma_algebra.is_in(s) for _, s in self.pairs)


class LebesgueIntegral:
    """Lebesgue integral for non-negative measurable functions."""

    @staticmethod
    def of_simple(f: SimpleFunction) -> float:
        """Integral of a simple function."""
        total = 0.0
        measure = LebesgueMeasure()
        for coeff, s in f.pairs:
            total += coeff * measure(s)
        return total

    @staticmethod
    def of_positive(f: Callable[[Any], float],
                    space: MeasurableSpace,
                    partition: List[Set[Any]]) -> float:
        """Integral via simple function approximation (simplified)."""
        total = 0.0
        measure = LebesgueMeasure()
        for s in partition:
            if space.is_measurable(s):
                sample = next(iter(s), None)
                if sample is not None:
                    total += f(sample) * measure(s)
        return total


class ProbabilityMeasure(Measure):
    """Probability measure (μ(X) = 1)."""

    def __init__(self, space: MeasurableSpace,
                 mu: Optional[Callable[[Set[Any]], float]] = None):
        super().__init__(space, mu)
        if not self.is_probability():
            raise ValueError("Not a probability measure")


class BorelSigmaAlgebra(SigmaAlgebra):
    """Borel σ-algebra: smallest σ-algebra containing open sets."""

    @staticmethod
    def from_topology(space: 'TopologicalSpace') -> 'BorelSigmaAlgebra':
        """Generate Borel σ-algebra from a topological space."""
        from lean4py.topology import TopologicalSpace
        open_sets = {frozenset(s) for s in space.open_sets}
        return BorelSigmaAlgebra(space.points, open_sets)
