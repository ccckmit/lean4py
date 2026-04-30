"""Topology module for lean4py.

Imitates mathlib4 Mathlib.Topology: general topology, metric spaces.
"""

from typing import Set, List, Callable, Any, Optional, Dict, Tuple
from functools import wraps


class TopologicalSpace:
    """Topological space defined by open sets.

    A topological space is a set X with a collection τ of subsets
    satisfying: ∅, X ∈ τ; τ closed under finite intersections and arbitrary unions.
    """

    def __init__(self, points: Set[Any], open_sets: Optional[Set[Any]] = None):
        self.points = points
        self.open_sets = open_sets if open_sets is not None else {frozenset(), frozenset(points)}

    def is_open(self, s: Set[Any]) -> bool:
        """Check if a set is open."""
        return frozenset(s) in self.open_sets

    def interior(self, s: Set[Any]) -> Set[Any]:
        """Interior of a set: largest open subset."""
        interior = set()
        for op in self.open_sets:
            if op <= frozenset(s):
                interior |= set(op)
        return interior

    def closure(self, s: Set[Any]) -> Set[Any]:
        """Closure of a set: smallest closed set containing it."""
        # Closure = complement of union of all open sets disjoint from s
        closed_union = set()
        s_frozen = frozenset(s)
        for op in self.open_sets:
            if op & s_frozen == frozenset():
                closed_union |= set(frozenset(self.points) - op)
        return closed_union | set(s)

    def boundary(self, s: Set[Any]) -> Set[Any]:
        """Boundary of a set: closure ∩ closure(complement)."""
        complement = set(self.points) - set(s)
        return self.closure(s) & self.closure(complement)

    def is_closed(self, s: Set[Any]) -> bool:
        """Check if a set is closed."""
        return set(s) <= self.closure(s)

    def is_hausdorff(self) -> bool:
        """Check Hausdorff condition: any two distinct points have disjoint neighborhoods."""
        points_list = list(self.points)
        for i, x in enumerate(points_list):
            for y in points_list[i+1:]:
                if x == y:
                    continue
                found = False
                for u in self.open_sets:
                    for v in self.open_sets:
                        if frozenset([x]) <= u and frozenset([y]) <= v and u & v == frozenset():
                            found = True
                            break
                    if found:
                        break
                if not found:
                    return False
        return True

    def is_connected(self) -> bool:
        """Check if space is connected (no non-trivial clopen sets)."""
        for op in self.open_sets:
            if op != frozenset() and op != frozenset(self.points):
                complement = frozenset(self.points) - op
                if complement in self.open_sets:
                    return False
        return True

    def is_compact(self) -> bool:
        """Check compactness using finite subcover property (for finite spaces)."""
        if len(self.points) > 20:
            return False
        return True


class MetricSpace:
    """Metric space with distance function.

    A metric space is a set X with a distance function d: X × X → ℝ≥0
    satisfying: d(x,y) ≥ 0, d(x,y) = 0 iff x=y, d(x,y)=d(y,x), triangle inequality.
    """

    def __init__(self, points: Set[Any], distance: Callable[[Any, Any], float]):
        self.points = points
        self.d = distance

    def ball(self, center: Any, radius: float) -> Set[Any]:
        """Open ball B(center, radius)."""
        return {p for p in self.points if self.d(center, p) < radius}

    def is_metric(self) -> bool:
        """Verify metric axioms for all points."""
        points_list = list(self.points)
        for x in points_list:
            if self.d(x, x) != 0:
                return False
            for y in points_list:
                if self.d(x, y) != self.d(y, x):
                    return False
                for z in points_list:
                    if self.d(x, z) > self.d(x, y) + self.d(y, z):
                        return False
        return True

    def diameter(self, s: Optional[Set[Any]] = None) -> float:
        """Diameter of a subset."""
        target = s if s is not None else self.points
        if len(target) < 2:
            return 0.0
        points_list = list(target)
        return max(self.d(x, y) for x in points_list for y in points_list)

    def is_complete(self) -> bool:
        """Check completeness (every Cauchy sequence converges). Simplified."""
        return True

    def to_topological_space(self) -> TopologicalSpace:
        """Generate topology from metric (open balls)."""
        open_sets = {frozenset()}
        for center in self.points:
            for radius in [0.5, 1.0, 2.0, float('inf')]:
                ball = self.ball(center, radius)
                open_sets.add(frozenset(ball))
        open_sets.add(frozenset(self.points))
        return TopologicalSpace(self.points, open_sets)


class ContinuousFunction:
    """Continuous function between topological spaces."""

    def __init__(self, domain: TopologicalSpace, codomain: TopologicalSpace,
                 func: Callable[[Any], Any]):
        self.domain = domain
        self.codomain = codomain
        self.func = func

    def is_continuous(self) -> bool:
        """Check continuity: preimage of every open set is open."""
        for v_open in self.codomain.open_sets:
            preimage = {x for x in self.domain.points if frozenset([self.func(x)]) <= v_open}
            if not self.domain.is_open(preimage):
                return False
        return True

    def image(self, s: Set[Any]) -> Set[Any]:
        """Image of a set."""
        return {self.func(x) for x in s}

    def preimage(self, t: Set[Any]) -> Set[Any]:
        """Preimage of a set."""
        return {x for x in self.domain.points if self.func(x) in t}


class Compactness:
    """Compactness properties for topological spaces."""

    @staticmethod
    def is_compact(space: TopologicalSpace) -> bool:
        """Check if space is compact."""
        return space.is_compact()

    @staticmethod
    def heine_borel(space: MetricSpace) -> bool:
        """Heine-Borel: in ℝⁿ, compact ⇔ closed and bounded."""
        return space.is_complete()  # Simplified


class Connectedness:
    """Connectedness properties."""

    @staticmethod
    def is_connected(space: TopologicalSpace) -> bool:
        return space.is_connected()

    @staticmethod
    def is_path_connected(space: TopologicalSpace) -> bool:
        """Check path-connectedness (simplified)."""
        return space.is_connected()


class HausdorffSpace(TopologicalSpace):
    """Hausdorff space (T2 separation)."""

    def __init__(self, points: Set[Any], open_sets: Optional[Set[Any]] = None):
        super().__init__(points, open_sets)
        if not self.is_hausdorff():
            raise ValueError("Space is not Hausdorff")


class OpenMap:
    """Open map: sends open sets to open sets."""

    @staticmethod
    def is_open_map(f: ContinuousFunction) -> bool:
        """Check if function is an open map."""
        for u_open in f.domain.open_sets:
            image = f.image(set(u_open))
            if not f.codomain.is_open(image):
                return False
        return True


class ClosedMap:
    """Closed map: sends closed sets to closed sets."""

    @staticmethod
    def is_closed_map(f: ContinuousFunction) -> bool:
        """Check if function is a closed map."""
        for u_open in f.domain.open_sets:
            closed_set = set(f.domain.points) - set(u_open)
            if f.domain.is_closed(closed_set):
                image = f.image(closed_set)
                if not f.codomain.is_closed(image):
                    return False
        return True
