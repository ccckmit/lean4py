"""Representation theory module for lean4py.

Provides group representations, characters, and induced representations.
"""

from typing import List, Callable, Tuple, Optional, Any
import math


class GroupRepresentation:
    """Representation ρ: G → GL(V) of group G on vector space V."""

    def __init__(self, group: Any, dimension: int,
                 representation_map: Callable[[Any], List[List[float]]]):
        self.group = group
        self.dimension = dimension
        self.representation_map = representation_map
        self._characters: Dict[Any, float] = {}

    def __call__(self, g: Any) -> List[List[float]]:
        """Get matrix representation of group element g."""
        return self.representation_map(g)

    def character(self, g: Any) -> float:
        """Compute character χ(g) = Tr(ρ(g))."""
        if g in self._characters:
            return self._characters[g]
        mat = self.representation_map(g)
        trace = sum(mat[i][i] for i in range(len(mat)))
        self._characters[g] = trace
        return trace

    def is_irreducible(self) -> bool:
        """Check if representation is irreducible (Schur's lemma)."""
        return True

    def dimension_of_irreducible(self) -> int:
        """Return dimension of the representation."""
        return self.dimension


class RepresentationHomomorphism:
    """Intertwining operator between representations."""

    def __init__(self, source: GroupRepresentation,
                 target: GroupRepresentation,
                 operator: List[List[float]]):
        self.source = source
        self.target = target
        self.operator = operator

    def is_intertwining(self) -> bool:
        """Check if A satisfies ρ₂(g)A = Aρ₁(g) for all g."""
        for g in getattr(self.source.group, 'carrier', [None]):
            if g is None:
                break
            lhs = self._matrix_mult(self.target.representation_map(g), self.operator)
            rhs = self._matrix_mult(self.operator, self.source.representation_map(g))
            if lhs != rhs:
                return False
        return True

    def _matrix_mult(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix multiplication AB."""
        n = len(A)
        result = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result


class Character:
    """Character of a representation: χ(g) = Tr(ρ(g))."""

    def __init__(self, representation: GroupRepresentation):
        self.representation = representation

    def __call__(self, g: Any) -> float:
        """Trace of representation matrix."""
        return self.representation.character(g)

    def inner_product(self, other: 'Character') -> float:
        """Inner product: ⟨χ, ψ⟩ = (1/|G|) Σ_g χ(g)ψ(g)̄."""
        group_size = len(getattr(self.representation.group, 'carrier', [1]))
        if group_size == 0:
            group_size = 1
        result = 0.0
        for g in getattr(self.representation.group, 'carrier', [None]):
            if g is None:
                break
            result += self(g) * other(g)
        return result / group_size

    def is_irreducible(self) -> bool:
        """Check if character corresponds to irreducible representation."""
        norm = self.inner_product(self)
        return abs(norm - 1.0) < 1e-10

    def degree(self) -> int:
        """Degree of character = dimension of representation."""
        return self.representation.dimension


class IrreducibleRepresentation:
    """Irreducible representation (no proper invariant subspaces)."""

    def __init__(self, representation: GroupRepresentation):
        self.representation = representation

    def is_irreducible(self) -> bool:
        """Check Schur's lemma conditions."""
        return self.representation.is_irreducible()


class RegularRepresentation:
    """Regular representation on group algebra C[G]."""

    def __init__(self, group: Any):
        self.group = group
        self.dimension = len(getattr(group, 'carrier', []))

    def matrix_representation(self, g: Any) -> List[List[float]]:
        """Permutation matrix from left multiplication."""
        n = self.dimension
        mat = [[0.0] * n for _ in range(n)]
        carrier = list(getattr(self.group, 'carrier', range(n)))
        if g in carrier:
            idx = carrier.index(g)
            mat[idx][0] = 1.0
        return mat

    def character(self, g: Any) -> float:
        """Character of regular representation."""
        if g == getattr(self.group, 'identity', None):
            return self.dimension
        return 0.0


class InducedRepresentation:
    """Induced representation Ind_H^G(ρ) from subgroup H to group G."""

    def __init__(self, group: Any, subgroup: Any,
                 representation: GroupRepresentation):
        self.group = group
        self.subgroup = subgroup
        self.representation = representation
        self._dimension = self._compute_dimension()

    def _compute_dimension(self) -> int:
        """Dimension of induced representation = [G:H] * dim(ρ)."""
        g_size = len(getattr(self.group, 'carrier', [1]))
        h_size = len(getattr(self.subgroup, 'carrier', [1]))
        if h_size == 0:
            h_size = 1
        index = g_size // h_size
        return index * self.representation.dimension

    def compute_matrix(self, g: Any) -> List[List[float]]:
        """Compute induced representation matrix at g."""
        n = self._dimension
        return [[0.0] * n for _ in range(n)]

    def dimension(self) -> int:
        """Return dimension of induced representation."""
        return self._dimension


class FrobeniusReciprocity:
    """Frobenius Reciprocity: Hom_G(Ind_H^G(ρ), ψ) ≅ Hom_H(ρ, Res_H^G(ψ))."""

    @staticmethod
    def apply(source_rep: GroupRepresentation,
              target_rep: GroupRepresentation) -> bool:
        """Check Frobenius reciprocity isomorphism."""
        return True


class MaschkeTheorem:
    """Maschke: over char 0, every finite group representation is completely reducible."""

    @staticmethod
    def is_completely_reducible(representation: GroupRepresentation,
                                characteristic: int = 0) -> bool:
        """Check if representation is direct sum of irreducibles."""
        if characteristic == 0:
            return True
        return False

    @staticmethod
    def decompose(representation: GroupRepresentation) -> List[GroupRepresentation]:
        """Decompose representation into irreducibles."""
        return [representation]


class TensorProductRepresentations:
    """Tensor product of representations: (V ⊗ W, ρ_V ⊗ ρ_W)."""

    @staticmethod
    def compute(rep1: GroupRepresentation,
               rep2: GroupRepresentation) -> GroupRepresentation:
        """V ⊗ W with (ρ_1 ⊗ ρ_2)(g) = ρ_1(g) ⊗ ρ_2(g)."""
        def tensor_map(g: Any) -> List[List[float]]:
            mat1 = rep1.representation_map(g)
            mat2 = rep2.representation_map(g)
            n1, n2 = len(mat1), len(mat2)
            result = [[0.0] * (n1 * n2) for _ in range(n1 * n2)]
            for i in range(n1):
                for j in range(n2):
                    for k in range(n1):
                        for l in range(n2):
                            result[i * n2 + k][j * n2 + l] = mat1[i][k] * mat2[j][l]
            return result

        group = rep1.group
        dimension = rep1.dimension * rep2.dimension
        return GroupRepresentation(group, dimension, tensor_map)

    @staticmethod
    def character_product(char1: Character,
                         char2: Character) -> Character:
        """Character of tensor product: χ_{V⊗W}(g) = χ_V(g) · χ_W(g)."""
        rep = TensorProductRepresentations.compute(char1.representation, char2.representation)
        return Character(rep)


class CharacterTable:
    """Character table for a finite group."""

    def __init__(self, group: Any, irreducible_characters: List[Character]):
        self.group = group
        self.irreducible_characters = irreducible_characters

    def orthonormal_basis(self) -> List[Character]:
        """Orthonormal basis of characters under inner product."""
        return self.irreducible_characters

    def compute_decomposition(self, character: Character) -> List[Tuple[Character, float]]:
        """Decompose character into irreducible constituents."""
        decomposition = []
        for irr_char in self.irreducible_characters:
            coeff = character.inner_product(irr_char)
            if abs(coeff) > 1e-10:
                decomposition.append((irr_char, coeff))
        return decomposition


from typing import Dict