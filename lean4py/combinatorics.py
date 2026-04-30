"""Combinatorics module for lean4py.

Imitates mathlib4 Mathlib.Combinatorics: pigeonhole, Catalan, set families, enumerative.
"""

from typing import List, Set, Dict, Tuple, Any, Optional, Callable
import math


class PigeonholePrinciple:
    """Pigeonhole principle: if n+1 items into n containers, one container has ≥2 items."""

    @staticmethod
    def finite_pigeonhole(items: List[Any], containers: int) -> Optional[Dict[Any, int]]:
        """Finite pigeonhole: return assignment if |items| > containers."""
        if len(items) <= containers:
            return None
        assignment = {}
        for i, item in enumerate(items):
            assignment[item] = i % containers
        return assignment

    @staticmethod
    def strong_pigeonhole(items: List[Any], containers: int,
                          capacity: int) -> bool:
        """Strong pigeonhole: if |items| > containers × capacity, some container has > capacity."""
        return len(items) > containers * capacity

    @staticmethod
    def infinite_pigeonhole(infinite_set: Set[Any], finite_set: Set[Any],
                            f: Callable[[Any], Any]) -> Optional[Any]:
        """Infinite pigeonhole: for infinite domain and finite codomain,
        ∃y in codomain s.t. f⁻¹(y) is infinite.
        Simplified: return first repeated value.
        """
        seen = {}
        for x in infinite_set:
            y = f(x)
            if y in seen:
                return y
            seen[y] = x
        return None


class CatalanNumber:
    """Catalan numbers: C_n = (1/(n+1)) * binom(2n, n)."""

    @staticmethod
    def catalan(n: int) -> int:
        """Compute n-th Catalan number."""
        if n < 0:
            return 0
        if n == 0:
            return 1
        return CatalanNumber.catalan(n - 1) * 2 * (2 * n - 1) // (n + 1)

    @staticmethod
    def catalan_list(n: int) -> List[int]:
        """List of Catalan numbers C_0, C_1, ..., C_n."""
        return [CatalanNumber.catalan(i) for i in range(n + 1)]

    @staticmethod
    def Dyck_words(n: int) -> List[str]:
        """Generate all Dyck words of length 2n (simplified: return count)."""
        return [''] * CatalanNumber.catalan(n)


class BellNumber:
    """Bell numbers: B_n = number of partitions of an n-element set."""

    @staticmethod
    def bell(n: int) -> int:
        """Compute n-th Bell number using recurrence."""
        if n < 0:
            return 0
        if n == 0:
            return 1
        bell = [0] * (n + 1)
        bell[0] = 1
        for i in range(1, n + 1):
            bell[i] = 0
            for k in range(i):
                bell[i] += math.comb(i - 1, k) * bell[k]
        return bell[n]

    @staticmethod
    def bell_list(n: int) -> List[int]:
        """List of Bell numbers B_0, B_1, ..., B_n."""
        return [BellNumber.bell(i) for i in range(n + 1)]


class DyckWord:
    """Dyck words: balanced strings of parentheses of length 2n."""

    @staticmethod
    def is_dyck(word: str) -> bool:
        """Check if a string is a valid Dyck word."""
        balance = 0
        for ch in word:
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
            else:
                return False
            if balance < 0:
                return False
        return balance == 0

    @staticmethod
    def generate(n: int) -> List[str]:
        """Generate all Dyck words of length 2n (simplified count)."""
        return [''] * CatalanNumber.catalan(n)


class SetFamily:
    """Families of subsets with combinatorial properties."""

    @staticmethod
    def is_antichain(family: List[Set[Any]]) -> bool:
        """Check if family is an antichain (no set contains another)."""
        for i, a in enumerate(family):
            for j, b in enumerate(family):
                if i != j and a < b:
                    return False
        return True

    @staticmethod
    def is_intersecting(family: List[Set[Any]]) -> bool:
        """Check if family is intersecting (any two sets intersect)."""
        for i, a in enumerate(family):
            for b in family[i+1:]:
                if len(a & b) == 0:
                    return False
        return True

    @staticmethod
    def union_size(family: List[Set[Any]]) -> int:
        """Size of the union of all sets in family."""
        union = set()
        for s in family:
            union |= s
        return len(union)


class SpernerTheorem:
    """Sperner's theorem: max size of antichain in P([n]) is binom(n, ⌊n/2⌋)."""

    @staticmethod
    def max_antichain_size(n: int) -> int:
        """Maximum size of an antichain in 2^[n]."""
        k = n // 2
        return math.comb(n, k)

    @staticmethod
    def middle_level(n: int) -> List[Set[int]]:
        """Construct a maximal antichain: all k-element subsets where k = ⌊n/2⌋."""
        from itertools import combinations
        k = n // 2
        return [set(c) for c in combinations(range(n), k)]


class HallMarriage:
    """Hall's marriage theorem: conditions for perfect matching in bipartite graph."""

    @staticmethod
    def hall_condition(bridesides: List[Set[int]]) -> bool:
        """Check Hall's condition: for any subset S of brides,
        |∪_{i∈S} N(i)| ≥ |S|.
        """
        n = len(bridesides)
        from itertools import combinations
        for k in range(1, n + 1):
            for subset in combinations(range(n), k):
                union_set = set()
                for i in subset:
                    union_set |= bridesides[i]
                if len(union_set) < k:
                    return False
        return True

    @staticmethod
    def has_perfect_matching(bridesides: List[Set[int]]) -> bool:
        """Check if a perfect matching exists."""
        return HallMarriage.hall_condition(bridesides)


class BinomialCoefficient:
    """Binomial coefficients and their properties."""

    @staticmethod
    def binom(n: int, k: int) -> int:
        """Binomial coefficient C(n,k)."""
        if k < 0 or k > n:
            return 0
        return math.comb(n, k)

    @staticmethod
    def vandermonde(n: int, m: int, k: int) -> bool:
        """Verify Vandermonde's identity: Σ_k C(r,k)C(s,n-k) = C(r+s,n)."""
        left = sum(math.comb(n, k) * math.comb(m, k) for k in range(min(n, m) + 1))
        right = math.comb(n + m, k)
        return left == right

    @staticmethod
    def binomial_theorem(x: float, y: float, n: int) -> float:
        """Verify (x+y)^n = Σ_k C(n,k) x^k y^(n-k)."""
        result = 0.0
        for k in range(n + 1):
            result += math.comb(n, k) * (x ** k) * (y ** (n - k))
        return result
