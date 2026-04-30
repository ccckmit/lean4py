"""Order theory module for lean4py.

Imitates mathlib4 Mathlib.Order: partial orders, lattices, Galois connections.
"""

from typing import List, Set, Callable, Any, Optional, Dict, Tuple, Generic, TypeVar

T = TypeVar('T')


class PartialOrder:
    """Partial order (≤) on a set.

    Axioms: reflexive (x ≤ x), antisymmetric (x ≤ y ∧ y ≤ x ⇒ x=y),
    transitive (x ≤ y ∧ y ≤ z ⇒ x ≤ z).
    """

    def __init__(self, elements: Set[Any],
                 leq: Callable[[Any, Any], bool]):
        self.elements = elements
        self._leq = leq

    def leq(self, x: Any, y: Any) -> bool:
        """Check if x ≤ y."""
        return self._leq(x, y)

    def is_partial_order(self) -> bool:
        """Verify partial order axioms."""
        for x in self.elements:
            if not self.leq(x, x):
                return False
        for x in self.elements:
            for y in self.elements:
                if self.leq(x, y) and self.leq(y, x) and x != y:
                    return False
        for x in self.elements:
            for y in self.elements:
                for z in self.elements:
                    if self.leq(x, y) and self.leq(y, z) and not self.leq(x, z):
                        return False
        return True

    def is_comparable(self, x: Any, y: Any) -> bool:
        """Check if x and y are comparable."""
        return self.leq(x, y) or self.leq(y, x)

    def min_elements(self) -> List[Any]:
        """Find minimal elements."""
        result = []
        for x in self.elements:
            if not any(self.leq(y, x) for y in self.elements if y != x):
                result.append(x)
        return result

    def max_elements(self) -> List[Any]:
        """Find maximal elements."""
        result = []
        for x in self.elements:
            if not any(self.leq(x, y) for y in self.elements if y != x):
                result.append(x)
        return result


class TotalOrder(PartialOrder):
    """Total order (linear order): every pair is comparable."""

    def __init__(self, elements: Set[Any],
                 leq: Callable[[Any, Any], bool]):
        super().__init__(elements, leq)

    def is_total_order(self) -> bool:
        """Verify total order: all pairs comparable."""
        if not self.is_partial_order():
            return False
        for x in self.elements:
            for y in self.elements:
                if not self.is_comparable(x, y):
                    return False
        return True


class Lattice(PartialOrder):
    """Lattice: every pair has sup (join) and inf (meet)."""

    def __init__(self, elements: Set[Any],
                 leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any],
                 meet: Callable[[Any, Any], Any]):
        super().__init__(elements, leq)
        self._join = join
        self._meet = meet

    def join(self, x: Any, y: Any) -> Any:
        """Supremum (least upper bound)."""
        return self._join(x, y)

    def meet(self, x: Any, y: Any) -> Any:
        """Infimum (greatest lower bound)."""
        return self._meet(x, y)

    def is_lattice(self) -> bool:
        """Verify lattice properties."""
        if not self.is_partial_order():
            return False
        for x in self.elements:
            for y in self.elements:
                j = self.join(x, y)
                if not self.leq(x, j) or not self.leq(y, j):
                    return False
                m = self.meet(x, y)
                if not self.leq(m, x) or not self.leq(m, y):
                    return False
        return True


class CompleteLattice(Lattice):
    """Complete lattice: every subset has sup and inf."""

    def __init__(self, elements: Set[Any],
                 leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any],
                 meet: Callable[[Any, Any], Any]):
        super().__init__(elements, leq, join, meet)
        self._complete = True

    def is_complete(self) -> bool:
        """Verify complete lattice property."""
        return self._complete


class HeytingAlgebra(Lattice):
    """Heyting algebra: intuitionistic logic.

    Has implication operation: x → y is the greatest z s.t. z ∧ x ≤ y.
    """

    def __init__(self, elements: Set[Any],
                 leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any],
                 meet: Callable[[Any, Any], Any],
                 implication: Callable[[Any, Any], Any]):
        super().__init__(elements, leq, join, meet)
        self._imp = implication

    def implies(self, x: Any, y: Any) -> Any:
        """Heyting implication: x → y."""
        return self._imp(x, y)

    def is_heyting(self) -> bool:
        """Verify Heyting algebra properties."""
        if not self.is_lattice():
            return False
        for x in self.elements:
            for y in self.elements:
                imp = self.implies(x, y)
                if not self.leq(self.meet(x, imp), y):
                    return False
        return True


class BooleanAlgebra(HeytingAlgebra):
    """Boolean algebra: complemented distributive lattice."""

    def __init__(self, elements: Set[Any],
                 leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any],
                 meet: Callable[[Any, Any], Any],
                 implication: Callable[[Any, Any], Any],
                 complement: Callable[[Any], Any]):
        super().__init__(elements, leq, join, meet, implication)
        self._not = complement

    def complement(self, x: Any) -> Any:
        """Complement: ¬x."""
        return self._not(x)

    def is_boolean(self) -> bool:
        """Verify Boolean algebra properties."""
        if not self.is_heyting():
            return False
        for x in self.elements:
            if not self.leq(self.join(x, self.complement(x)),
                           self.join(self.complement(x), x)):
                return False
        return True


class GaloisConnection:
    """Galois connection between two partial orders.

    Pair of monotone maps f: P → Q, g: Q → P s.t.
    f(x) ≤ y ⇔ x ≤ g(y).
    """

    def __init__(self,
                 order_p: PartialOrder, order_q: PartialOrder,
                 f: Callable[[Any], Any], g: Callable[[Any], Any]):
        self.order_p = order_p
        self.order_q = order_q
        self.f = f
        self.g = g

    def is_galois_connection(self) -> bool:
        """Verify Galois connection property."""
        for x in self.order_p.elements:
            for y in self.order_q.elements:
                if self.order_q.leq(self.f(x), y) != self.order_p.leq(x, self.g(y)):
                    return False
        return True

    def unit(self, x: Any) -> bool:
        """Check x ≤ g(f(x))."""
        return self.order_p.leq(x, self.g(self.f(x)))

    def counit(self, y: Any) -> bool:
        """Check f(g(y)) ≤ y."""
        return self.order_q.leq(self.f(self.g(y)), y)
