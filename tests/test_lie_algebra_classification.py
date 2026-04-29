"""Tests for lie_algebra_classification module (v1.18)."""
import pytest
from lean4py.lie_algebra_classification import (
    DynkinDiagram, ClassificationTheorem, Weight, HighestWeightVector,
    RootSystem, WeylGroup, VermaModule, KostantForm, SimpleLieAlgebra
)


class TestDynkinDiagram:
    def test_creation(self):
        dd = DynkinDiagram([0, 1], [(0, 1, 1)])
        assert len(dd.nodes) == 2

    def test_creation_empty(self):
        dd = DynkinDiagram()
        assert dd.nodes == []

    def test_classify_A1(self):
        dd = DynkinDiagram([0], [])
        assert dd.classify() == "A_1"

    def test_classify_A2(self):
        dd = DynkinDiagram([0, 1], [(0, 1, 1)])
        assert dd.classify() == "A_2"

    def test_classify_G2(self):
        dd = DynkinDiagram([0, 1], [(0, 1, 3)])
        assert dd.classify() == "G_2"

    def test_classify_F4(self):
        dd = DynkinDiagram([0, 1], [(0, 1, 4)])
        assert dd.classify() == "F_4"

    def test_classify_trivial(self):
        dd = DynkinDiagram([], [])
        assert dd.classify() == "trivial"

    def test_has_double_edge(self):
        dd1 = DynkinDiagram([0, 1], [(0, 1, 1)])
        dd2 = DynkinDiagram([0, 1], [(0, 1, 2)])
        assert dd1._has_double_edge() is False
        assert dd2._has_double_edge() is True

    def test_is_simple_chain(self):
        dd = DynkinDiagram([0, 1, 2], [(0, 1, 1), (1, 2, 1)])
        assert dd._is_simple_chain() is True

    def test_rank(self):
        dd = DynkinDiagram([0, 1, 2], [])
        assert dd.rank() == 3

    def test_add_node(self):
        dd = DynkinDiagram([0], [])
        dd.add_node(1)
        assert 1 in dd.nodes

    def test_add_edge(self):
        dd = DynkinDiagram([0, 1], [])
        dd.add_edge(0, 1, 2)
        assert len(dd.edges) == 1


class TestClassificationTheorem:
    def test_classify_from_cartAN_single(self):
        result = ClassificationTheorem.classify_from_cartAN_matrix([[2]])
        assert result == ["A_1"]

    def test_classify_from_cartAN_A2(self):
        cartan = [[2, -1], [-1, 2]]
        result = ClassificationTheorem.classify_from_cartAN_matrix(cartan)
        assert "A_2" in result

    def test_root_system_type_A1(self):
        result = ClassificationTheorem.root_system_type([[1.0], [-1.0]])
        assert result == "A_1"

    def test_root_system_type_A2(self):
        result = ClassificationTheorem.root_system_type([[1, 0], [0, 1], [-1, -1]])
        assert result in ("A_2", "BC_2")

    def test_is_cartan_matrix_valid(self):
        matrix = [[2, -1], [-1, 2]]
        assert ClassificationTheorem.is_cartan_matrix(matrix) is True

    def test_is_cartan_matrix_invalid(self):
        matrix = [[2, 1], [1, 2]]
        assert ClassificationTheorem.is_cartan_matrix(matrix) is False

    def test_is_cartan_matrix_wrong_diag(self):
        matrix = [[3, -1], [-1, 2]]
        assert ClassificationTheorem.is_cartan_matrix(matrix) is False


class TestWeight:
    def test_creation(self):
        w = Weight([1.0, 2.0])
        assert len(w.coordinates) == 2

    def test_creation_with_root_system(self):
        w = Weight([1.0], "root_system")
        assert w.root_system == "root_system"

    def test_inner_product(self):
        w1 = Weight([1.0, 2.0])
        w2 = Weight([3.0, 4.0])
        result = w1.inner_product(w2)
        assert result == 11.0

    def test_is_dominant(self):
        w = Weight([1.0, 2.0])
        assert w.is_dominant() is True

    def test_is_regular(self):
        w = Weight([1.0, 2.0])
        assert w.is_regular() is True

    def test_is_integral(self):
        w = Weight([1.0, 2.0])
        assert w.is_integral() is True

    def test_add(self):
        w1 = Weight([1.0, 2.0])
        w2 = Weight([3.0, 4.0])
        result = w1.add(w2)
        assert result.coordinates == [4.0, 6.0]

    def test_scale(self):
        w = Weight([1.0, 2.0])
        result = w.scale(3.0)
        assert result.coordinates == [3.0, 6.0]


class TestHighestWeightVector:
    def test_creation(self):
        w = Weight([1.0, 2.0])
        hwv = HighestWeightVector(w, [1.0, 0.0])
        assert hwv.weight == w
        assert hwv.vector == [1.0, 0.0]

    def test_is_highest_weight(self):
        w = Weight([1.0])
        hwv = HighestWeightVector(w, [1.0])
        assert hwv.is_highest_weight() is True


class TestRootSystem:
    def test_creation(self):
        rs = RootSystem(2)
        assert rs.rank == 2

    def test_creation_with_roots(self):
        rs = RootSystem(2, [[1.0, 0.0], [0.0, 1.0]])
        assert len(rs.roots) == 2

    def test_compute_positive_roots(self):
        rs = RootSystem(2)
        result = rs.compute_positive_roots()
        assert isinstance(result, list)

    def test_compute_simple_roots(self):
        rs = RootSystem(2)
        result = rs.compute_simple_roots()
        assert isinstance(result, list)

    def test_weyl_group_generators(self):
        rs = RootSystem(2)
        result = rs.weyl_group_generators()
        assert isinstance(result, list)


class TestWeylGroup:
    def test_creation(self):
        wg = WeylGroup()
        assert wg.root_system is None

    def test_creation_with_root_system(self):
        rs = RootSystem(2)
        wg = WeylGroup(rs)
        assert wg.root_system == rs

    def test_reflect(self):
        wg = WeylGroup()
        v = [1.0, 0.0]
        alpha = [1.0, 0.0]
        result = wg.reflect(v, alpha)
        assert result == [-1.0, 0.0]

    def test_reflect_zero_vector(self):
        wg = WeylGroup()
        v = [1.0, 2.0]
        alpha = [0.0, 0.0]
        result = wg.reflect(v, alpha)
        assert result == [1.0, 2.0]

    def test_orbit(self):
        rs = RootSystem(2, [[1.0, 0.0]])
        wg = WeylGroup(rs)
        result = wg.orbit([1.0, 0.0])
        assert len(result) >= 1

    def test_length(self):
        wg = WeylGroup()
        result = wg.length([])
        assert result == 0

    def test_longest_element(self):
        wg = WeylGroup()
        result = wg.longest_element()
        assert isinstance(result, list)


class TestVermaModule:
    def test_creation(self):
        w = Weight([1.0, 2.0])
        vm = VermaModule(w)
        assert vm.weight == w
        assert vm.lie_algebra is None

    def test_character(self):
        w = Weight([1.0])
        vm = VermaModule(w)
        result = vm.character()
        assert "M" in result

    def test_is_simple(self):
        w = Weight([1.0])
        vm = VermaModule(w)
        assert vm.is_simple() is False

    def test_socle(self):
        w = Weight([1.0])
        vm = VermaModule(w)
        result = vm.socle()
        assert isinstance(result, list)

    def test_radical(self):
        w = Weight([1.0])
        vm = VermaModule(w)
        result = vm.radical()
        assert isinstance(result, list)


class TestKostantForm:
    def test_creation(self):
        kf = KostantForm()
        assert kf.lie_algebra is None

    def test_creation_with_lie_algebra(self):
        kf = KostantForm("sl2")
        assert kf.lie_algebra == "sl2"

    def test_PBW_basis(self):
        kf = KostantForm()
        result = kf.PBW_basis()
        assert result == ["monomials"]

    def test_canonical_basis(self):
        kf = KostantForm()
        result = kf.canonical_basis()
        assert result == ["canonical"]


class TestSimpleLieAlgebra:
    def test_types(self):
        assert "A_n" in SimpleLieAlgebra.TYPES
        assert "G_2" in SimpleLieAlgebra.TYPES

    def test_from_dynkin_diagram_A1(self):
        dd = DynkinDiagram([0], [])
        result = SimpleLieAlgebra.from_dynkin_diagram(dd)
        assert result == "A_1"

    def test_rank_A1(self):
        assert SimpleLieAlgebra.rank("A_1") == 1

    def test_rank_A5(self):
        assert SimpleLieAlgebra.rank("A_5") == 5

    def test_rank_G2(self):
        assert SimpleLieAlgebra.rank("G_2") == 2

    def test_rank_E6(self):
        assert SimpleLieAlgebra.rank("E_6") == 6