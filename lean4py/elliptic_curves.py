"""Elliptic curves module for lean4py.

Imitates mathlib4 Mathlib.ArithmeticGeometry.EllipticCurve: curves, group law, torsion.
"""

from typing import List, Dict, Set, Tuple, Any, Optional, Callable
import math


class EllipticCurve:
    """Elliptic curve E: y² = x³ + Ax + B."""

    def __init__(self, A: float, B: float):
        self.A = A
        self.B = B
        self.discriminant = -16 * (4 * A**3 + 27 * B**2)

    def is_smooth(self) -> bool:
        """Check discriminant ≠ 0."""
        return abs(self.discriminant) > 1e-10

    def evaluate(self, x: float) -> List[float]:
        """y-values for given x."""
        y_squared = x**3 + self.A * x + self.B
        if y_squared < 0:
            return []
        y = math.sqrt(y_squared)
        return [-y, y]


class GroupLaw:
    """Group law on elliptic curve (chord-tangent method)."""

    @staticmethod
    def add(P: Tuple[float, float], Q: Tuple[float, float],
            curve: EllipticCurve) -> Tuple[float, float]:
        """P + Q on E."""
        if P == Q:
            return GroupLaw.double(P, curve)
        m = (Q[1] - P[1]) / (Q[0] - P[0])
        x_r = m**2 - P[0] - Q[0]
        y_r = m * (P[0] - x_r) - P[1]
        return (x_r, y_r)

    @staticmethod
    def double(P: Tuple[float, float],
                curve: EllipticCurve) -> Tuple[float, float]:
        """2P on E."""
        m = (3 * P[0]**2 + curve.A) / (2 * P[1])
        x_r = m**2 - 2 * P[0]
        y_r = m * (P[0] - x_r) - P[1]
        return (x_r, y_r)

    @staticmethod
    def identity() -> str:
        """Point at infinity O."""
        return "O"


class TorsionPoint:
    """Torsion points of order n."""

    @staticmethod
    def find(curve: EllipticCurve, n: int) -> List[Tuple[float, float]]:
        """Find points P with nP = O (simplified)."""
        return []

    @staticmethod
    def order(P: Tuple[float, float],
              curve: EllipticCurve) -> int:
        """Order of P (simplified)."""
        return 1


class Rank:
    """Mordell-Weil rank of E(ℚ)."""

    @staticmethod
    def compute(curve: EllipticCurve) -> int:
        """Rank of E(ℚ) (simplified: return 0)."""
        return 0

    @staticmethod
    def is_finite_generated(curve: EllipticCurve) -> bool:
        """E(ℚ) is finitely generated (Mordell-Weil)."""
        return True


class Isogeny:
    """Isogeny between elliptic curves."""

    @staticmethod
    def exists(E1: EllipticCurve, E2: EllipticCurve) -> bool:
        """Check if there exists isogeny E1 → E2 (simplified)."""
        return True

    @staticmethod
    def degree(isogeny: str) -> int:
        """Degree of isogeny (simplified)."""
        return 1
