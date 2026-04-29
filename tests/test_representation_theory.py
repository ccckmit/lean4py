"""Tests for representation_theory module."""
import pytest
from lean4py.representation_theory import (
    GroupRepresentation, RepresentationHomomorphism, Character, IrreducibleRepresentation,
    RegularRepresentation, InducedRepresentation, FrobeniusReciprocity, MaschkeTheorem,
    TensorProductRepresentations, CharacterTable
)


class MockGroup:
    def __init__(self, carrier=None, identity=None):
        self.carrier = carrier or []
        self.identity = identity


class TestGroupRepresentation:
    def test_creation(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1, 2], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        assert rep.dimension == 2
        assert rep.group == group

    def test_call(self):
        def rep_map(g):
            if g == 1:
                return [[1, 0], [0, 1]]
            return [[0, 1], [1, 0]]

        group = MockGroup(carrier=[1, 2], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        mat = rep(1)
        assert mat[0][0] == 1

    def test_character(self):
        def rep_map(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = rep.character(1)
        assert char == 2.0


class TestCharacter:
    def test_creation(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        assert char.representation == rep

    def test_call(self):
        def rep_map(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        assert char(1) == 2.0

    def test_inner_product(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        result = char.inner_product(char)
        assert isinstance(result, (int, float))

    def test_is_irreducible(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        result = char.is_irreducible()
        assert isinstance(result, bool)

    def test_degree(self):
        def rep_map(g):
            return [[1.0] * 2 for _ in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        assert char.degree() == 2


class TestIrreducibleRepresentation:
    def test_creation(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        irr = IrreducibleRepresentation(rep)
        assert irr.representation == rep


class TestMaschkeTheorem:
    def test_is_completely_reducible_char0(self):
        def rep_map(g):
            return [[1.0] * 2 for _ in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        result = MaschkeTheorem.is_completely_reducible(rep, 0)
        assert result is True

    def test_is_completely_reducible_charp(self):
        def rep_map(g):
            return [[1.0] * 2 for _ in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        result = MaschkeTheorem.is_completely_reducible(rep, 2)
        assert result is False

    def test_decompose(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        result = MaschkeTheorem.decompose(rep)
        assert len(result) >= 1


class TestInducedRepresentation:
    def test_creation(self):
        def rep_map(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        group = MockGroup(carrier=[1, 2], identity=1)
        subgroup = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(subgroup, 2, rep_map)
        induced = InducedRepresentation(group, subgroup, rep)
        assert induced.group == group
        assert induced.subgroup == subgroup

    def test_dimension(self):
        def rep_map(g):
            return [[1.0] * 2 for _ in range(2)]

        group = MockGroup(carrier=[1, 2], identity=1)
        subgroup = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(subgroup, 2, rep_map)
        induced = InducedRepresentation(group, subgroup, rep)
        dim = induced.dimension()
        assert isinstance(dim, int)
        assert dim > 0

    def test_compute_matrix(self):
        def rep_map(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        group = MockGroup(carrier=[1, 2], identity=1)
        subgroup = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(subgroup, 2, rep_map)
        induced = InducedRepresentation(group, subgroup, rep)
        mat = induced.compute_matrix(1)
        assert isinstance(mat, list)
        assert all(isinstance(row, list) for row in mat)


class TestTensorProductRepresentations:
    def test_compute(self):
        def rep_map1(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        def rep_map2(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        group = MockGroup(carrier=[1], identity=1)
        rep1 = GroupRepresentation(group, 2, rep_map1)
        rep2 = GroupRepresentation(group, 2, rep_map2)
        result = TensorProductRepresentations.compute(rep1, rep2)
        assert isinstance(result, GroupRepresentation)
        assert result.dimension == 4

    def test_character_product(self):
        def rep_map(g):
            return [[1.0, 0.0], [0.0, 1.0]]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        result = TensorProductRepresentations.character_product(char, char)
        assert isinstance(result, Character)


class TestFrobeniusReciprocity:
    def test_apply(self):
        def rep_map(g):
            return [[1.0] * 2 for _ in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        result = FrobeniusReciprocity.apply(rep, rep)
        assert isinstance(result, bool)


class TestCharacterTable:
    def test_creation(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        ct = CharacterTable(group, [char])
        assert ct.group == group
        assert len(ct.irreducible_characters) == 1

    def test_orthonormal_basis(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        ct = CharacterTable(group, [char])
        basis = ct.orthonormal_basis()
        assert isinstance(basis, list)

    def test_compute_decomposition(self):
        def rep_map(g):
            return [[1.0 if i == j else 0.0 for j in range(2)] for i in range(2)]

        group = MockGroup(carrier=[1], identity=1)
        rep = GroupRepresentation(group, 2, rep_map)
        char = Character(rep)
        ct = CharacterTable(group, [char])
        decomp = ct.compute_decomposition(char)
        assert isinstance(decomp, list)


def test_import_from_package():
    from lean4py import (
        GroupRepresentation, Character, RegularRepresentation,
        InducedRepresentation, MaschkeTheorem
    )
    assert GroupRepresentation is not None
    assert Character is not None
    assert InducedRepresentation is not None
    assert MaschkeTheorem is not None