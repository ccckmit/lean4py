from typing import Any, Iterable, Set as _Set


class Set:
    """A finite set with support for standard set operations.

    Supports operators: + (union), * (intersection), ~ (complement, deprecated),
    - (difference), <= (subset).
    """
    def __init__(self, elems: Iterable[Any] = None):
        self._elems = set(elems) if elems is not None else set()

    def __repr__(self):
        if not self._elems:
            return "∅"
        return "{" + ", ".join(str(e) for e in sorted(self._elems, key=repr)) + "}"

    def __eq__(self, other):
        return isinstance(other, Set) and self._elems == other._elems

    def __hash__(self):
        return hash(frozenset(self._elems))

    def __contains__(self, elem):
        return elem in self._elems

    def __add__(self, other):
        return union(self, other)

    def __mul__(self, other):
        return intersection(self, other)

    def __invert__(self):
        raise TypeError("complement() now requires a universe: use complement(self, universe)")

    def __sub__(self, other):
        return difference(self, other)

    def __le__(self, other):
        return subset(self, other)

    def __lt__(self, other):
        return subset(self, other) and self != other

    def __radd__(self, other):
        return union(other, self)

    def __rmul__(self, other):
        return intersection(other, self)

    def to_set(self):
        return self._elems


def Set_from(elems: Iterable[Any]) -> Set:
    """Create a Set from an iterable of elements."""
    return Set(elems)


def in_(elem: Any, s: Set) -> bool:
    """Check if an element is in a set."""
    return elem in s._elems


def subset(s1: Set, s2: Set) -> bool:
    """Check if s1 is a subset of s2."""
    return s1._elems <= s2._elems


def union(s1: Set, s2: Set) -> Set:
    """Return the union of two sets."""
    return Set(s1._elems | s2._elems)


def intersection(s1: Set, s2: Set) -> Set:
    """Return the intersection of two sets."""
    return Set(s1._elems & s2._elems)


def complement(s: Set, universe: Set) -> Set:
    """Return the complement of s relative to universe."""
    return Set(universe._elems - s._elems)


def difference(s1: Set, s2: Set) -> Set:
    """Return the set difference: s1 \\ s2."""
    return Set(s1._elems - s2._elems)


def cartesian(s1: Set, s2: Set) -> Set:
    """Return the Cartesian product s1 × s2."""
    return Set((a, b) for a in s1._elems for b in s2._elems)


def power_set(s: Set) -> Set:
    """Return the power set P(s) (set of all subsets)."""
    if not s._elems:
        return Set([Set()])
    elems = list(s._elems)
    n = len(elems)
    result = set()
    for mask in range(1 << n):
        subset_elems = {elems[i] for i in range(n) if mask & (1 << i)}
        result.add(Set(subset_elems))
    return Set(result)


def empty_set() -> Set:
    """Return the empty set ∅."""
    return Set()


def symmetric_difference(s1: Set, s2: Set) -> Set:
    """Return the symmetric difference: (s1 - s2) ∪ (s2 - s1)."""
    return union(difference(s1, s2), difference(s2, s1))


def is_disjoint(s1: Set, s2: Set) -> bool:
    """Check if s1 and s2 have no elements in common."""
    return len(intersection(s1, s2)._elems) == 0


def is_overlapping(s1: Set, s2: Set) -> bool:
    """Check if s1 and s2 have at least one common element."""
    return len(intersection(s1, s2)._elems) > 0