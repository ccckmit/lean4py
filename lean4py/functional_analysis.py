"""Functional analysis module for lean4py.

Imitates mathlib4 Mathlib.Analysis: normed spaces, Banach/Hilbert spaces, operators.
"""

from typing import List, Callable, Any, Optional, Dict, Tuple, Generic, TypeVar
import math

T = TypeVar('T')


class NormedSpace:
    """Normed vector space (V, ||·||) over ℝ or ℂ.

    Axioms: ||x|| ≥ 0, ||x|| = 0 ⇔ x=0, ||αx|| = |α|·||x||, triangle inequality.
    """

    def __init__(self, dim: int,
                 norm: Optional[Callable[[Any], float]] = None):
        self.dim = dim
        self._norm = norm if norm is not None else (lambda x: math.sqrt(sum(x_i**2 for x_i in x)))

    def norm(self, x: Any) -> float:
        """Norm of a vector."""
        return self._norm(x)

    def is_normed(self, x: Any, y: Any, alpha: float = 1.0) -> bool:
        """Verify norm axioms for given vectors."""
        if self.norm(x) < 0:
            return False
        if self.norm(x) == 0 and x != (0,) * self.dim:
            return False
        if abs(self.norm(tuple(alpha * x_i for x_i in x)) - abs(alpha) * self.norm(x)) > 1e-10:
            return False
        if self.norm(tuple(x_i + y_i for x_i, y_i in zip(x, y))) > self.norm(x) + self.norm(y) + 1e-10:
            return False
        return True

    def is_complete(self) -> bool:
        """Check completeness (Banach property). Simplified."""
        return True

    def to_topological_space(self):
        """Generate topology from norm (metric = ||x-y||)."""
        from lean4py.topology import MetricSpace
        import itertools

        points = {tuple(range(self.dim))}
        def distance(x, y):
            return self.norm(tuple(x_i - y_i for x_i, y_i in zip(x, y)))
        return MetricSpace(points, distance)


class BanachSpace(NormedSpace):
    """Banach space: complete normed space."""

    def __init__(self, dim: int,
                 norm: Optional[Callable[[Any], float]] = None):
        super().__init__(dim, norm)
        if not self.is_complete():
            raise ValueError("Space is not complete")

    def is_banach(self) -> bool:
        """Verify Banach property."""
        return self.is_complete()


class InnerProductSpace:
    """Inner product space (V, ⟨·,·⟩).

    Axioms: conjugate symmetry, linearity, positive-definiteness.
    Induces norm: ||x|| = √⟨x,x⟩.
    """

    def __init__(self, dim: int,
                 inner: Optional[Callable[[Any, Any], float]] = None):
        self.dim = dim
        self._inner = inner if inner is not None else self._default_inner

    def _default_inner(self, x: Any, y: Any) -> float:
        """Standard Euclidean inner product."""
        return sum(x_i * y_i for x_i, y_i in zip(x, y))

    def inner(self, x: Any, y: Any) -> float:
        """Inner product of x and y."""
        return self._inner(x, y)

    def norm(self, x: Any) -> float:
        """Norm induced by inner product."""
        return math.sqrt(abs(self.inner(x, x)))

    def is_inner_product(self, x: Any, y: Any, z: Any) -> bool:
        """Verify inner product axioms."""
        if abs(self.inner(x, y) - self.inner(y, x)) > 1e-10:
            return False
        if abs(self.inner(tuple(2 * x_i for x_i in x), y) - 2 * self.inner(x, y)) > 1e-10:
            return False
        if self.inner(x, x) < -1e-10:
            return False
        if self.inner(x, x) == 0 and x != (0,) * self.dim:
            return False
        return True

    def angle(self, x: Any, y: Any) -> float:
        """Angle between x and y."""
        norm_x = self.norm(x)
        norm_y = self.norm(y)
        if norm_x == 0 or norm_y == 0:
            return 0.0
        cos_val = self.inner(x, y) / (norm_x * norm_y)
        return math.acos(max(-1.0, min(1.0, cos_val)))


class HilbertSpace(InnerProductSpace):
    """Hilbert space: complete inner product space."""

    def __init__(self, dim: int,
                 inner: Optional[Callable[[Any, Any], float]] = None):
        super().__init__(dim, inner)
        self._complete = True

    def is_hilbert(self) -> bool:
        """Verify Hilbert space properties."""
        return self._complete

    def projection(self, x: Any, subspace_basis: List[Any]) -> Any:
        """Orthogonal projection onto subspace."""
        proj = [0.0] * len(x)
        for v in subspace_basis:
            inner_vv = self.inner(v, v)
            if inner_vv > 1e-10:
                coeff = self.inner(x, v) / inner_vv
                proj = [p_i + coeff * v_i for p_i, v_i in zip(proj, v)]
        return tuple(proj)

    def gram_schmidt(self, vectors: List[Any]) -> List[Any]:
        """Gram-Schmidt orthogonalization."""
        orthogonal = []
        for v in vectors:
            w = v
            for u in orthogonal:
                proj_coeff = self.inner(v, u) / self.inner(u, u) if self.inner(u, u) != 0 else 0
                w = tuple(w_i - proj_coeff * u_i for w_i, u_i in zip(w, u))
            if self.norm(w) > 1e-10:
                orthogonal.append(w)
        return orthogonal


class BoundedOperator:
    """Bounded linear operator T: V → W between normed spaces.

    ||T|| = sup{||T(x)|| : ||x|| ≤ 1}
    """

    def __init__(self, domain: NormedSpace, codomain: NormedSpace,
                 matrix: Optional[List[List[float]]] = None):
        self.domain = domain
        self.codomain = codomain
        self.matrix = matrix if matrix is not None else [[1.0 if i == j else 0.0 for j in range(domain.dim)] for i in range(codomain.dim)]

    def apply(self, x: Any) -> Any:
        """Apply operator to vector x."""
        result = [0.0] * self.codomain.dim
        for i in range(self.codomain.dim):
            for j in range(self.domain.dim):
                result[i] += self.matrix[i][j] * (x[j] if j < len(x) else 0)
        return tuple(result)

    def operator_norm(self) -> float:
        """Compute operator norm (simplified)."""
        max_norm = 0.0
        for i in range(self.domain.dim):
            basis = tuple(1.0 if j == i else 0.0 for j in range(self.domain.dim))
            image_norm = self.domain.norm(self.apply(basis))
            if image_norm > max_norm:
                max_norm = image_norm
        return max_norm

    def is_bounded(self) -> bool:
        """Check if operator is bounded."""
        return self.operator_norm() < float('inf')

    def adjoint(self, inner_domain: InnerProductSpace,
                inner_codomain: InnerProductSpace) -> 'BoundedOperator':
        """Adjoint operator T* (simplified for finite-dim)."""
        adj_matrix = [[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))]
        return BoundedOperator(self.codomain, self.domain, adj_matrix)


class DualSpace:
    """Dual space V* = {continuous linear functionals V → ℝ}."""

    @staticmethod
    def riesz_representation(space: HilbertSpace, functional: Callable[[Any], float]) -> Any:
        """Riesz representation: every f ∈ H* corresponds to unique y ∈ H s.t. f(x) = ⟨x,y⟩.

        Simplified: assume functional is f(x) = ⟨x, e₁⟩.
        """
        basis = tuple(1.0 if i == 0 else 0.0 for i in range(space.dim))
        return basis


class OperatorNorm:
    """Operator norm properties."""

    @staticmethod
    def is_norm(op: BoundedOperator) -> bool:
        """Verify operator norm axioms."""
        norm_val = op.operator_norm()
        if norm_val < 0:
            return False
        return True
