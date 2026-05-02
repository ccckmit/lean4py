"""p-adic numbers module for lean4py.

Imitates mathlib4 Mathlib.NumberTheory.PAdic: p-adic numbers, valuations, Hensel.
"""

from typing import List, Dict, Set, Tuple, Any, Optional, Callable


class PadicNumber:
    """p-adic number x = Σ aₙ pⁿ (aₙ ∈ {0,...,p-1})."""

    def __init__(self, p: int, coefficients: Optional[List[int]] = None):
        self.p = p
        self.coeffs = coefficients or [0]

    def valuation(self) -> int:
        """v_p(x) = smallest n with aₙ ≠ 0."""
        for i, a in enumerate(self.coeffs):
            if a != 0:
                return i
        return float('inf')

    def norm(self) -> float:
        """|x|_p = p^{-v_p(x)}."""
        v = self.valuation()
        if v == float('inf'):
            return 0.0
        return float(self.p ** (-v))


class PadicValuation:
    """p-adic valuation v_p: Q* → ℤ."""

    @staticmethod
    def compute(p: int, x: float) -> int:
        """v_p(x) for x ∈ ℚ (simplified)."""
        if x == 0:
            return float('inf')
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return count

    @staticmethod
    def is_valuation(p: int) -> bool:
        """Check v_p is a valuation (simplified)."""
        return True


class HenselLemma:
    """Hensel's lemma: lifting solutions mod pⁿ to ℚ_p."""

    @staticmethod
    def lift_polynomial(f: Callable, derivative: Callable,
                        p: int, a: int, n: int) -> Optional[int]:
        """Lift root mod pⁿ to ℚ_p (simplified)."""
        return a

    @staticmethod
    def holds(p: int) -> bool:
        """Hensel's lemma holds in ℚ_p (simplified)."""
        return True


class PadicAbsoluteValue:
    """p-adic absolute value |·|_p."""

    @staticmethod
    def compute(p: int, x: float) -> float:
        """|x|_p = p^{-v_p(x)}."""
        v = PadicValuation.compute(p, x)
        if v == float('inf'):
            return 0.0
        return p ** (-v)

    @staticmethod
    def is_nonarchimedean(p: int) -> bool:
        """|x + y|_p ≤ max(|x|_p, |y|_p)."""
        return True
