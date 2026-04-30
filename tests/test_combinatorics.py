"""Tests for combinatoric module."""

import pytest
from lean4py.combinatorics import (
    PigeonholePrinciple, CatalanNumber, BellNumber, DyckWord,
    SetFamily, SpernerTheorem, HallMarriage, BinomialCoefficient
)


class TestPigeonholePrinciple:
    """Test pigeonhole principle."""

    def test_finite_pigeonhole(self):
        items = [1, 2, 3, 4, 5]
        result = PigeonholePrinciple.finite_pigeonhole(items, 3)
        assert result is not None
        assert len(result) == 5

    def test_strong_pigeonhole(self):
        items = list(range(10))
        assert PigeonholePrinciple.strong_pigeonhole(items, 3, 2) is True
        assert PigeonholePrinciple.strong_pigeonhole(items, 10, 2) is False

    def test_infinite_pigeonhole(self):
        infinite = {1, 2, 3, 4, 5}
        f = lambda x: x % 2
        result = PigeonholePrinciple.infinite_pigeonhole(infinite, {0, 1}, f)
        assert result in {0, 1}


class TestCatalanNumber:
    """Test Catalan numbers."""

    def test_catalan_0(self):
        assert CatalanNumber.catalan(0) == 1

    def test_catalan_1(self):
        assert CatalanNumber.catalan(1) == 1

    def test_catalan_2(self):
        assert CatalanNumber.catalan(2) == 2

    def test_catalan_3(self):
        assert CatalanNumber.catalan(3) == 5

    def test_catalan_4(self):
        assert CatalanNumber.catalan(4) == 14

    def test_catalan_list(self):
        lst = CatalanNumber.catalan_list(4)
        assert lst == [1, 1, 2, 5, 14]

    def test_dyck_words_count(self):
        result = CatalanNumber.Dyck_words(3)
        assert len(result) == CatalanNumber.catalan(3)


class TestBellNumber:
    """Test Bell numbers."""

    def test_bell_0(self):
        assert BellNumber.bell(0) == 1

    def test_bell_1(self):
        assert BellNumber.bell(1) == 1

    def test_bell_2(self):
        assert BellNumber.bell(2) == 2

    def test_bell_3(self):
        assert BellNumber.bell(3) == 5

    def test_bell_4(self):
        assert BellNumber.bell(4) == 15

    def test_bell_list(self):
        lst = BellNumber.bell_list(3)
        assert lst == [1, 1, 2, 5]


class TestDyckWord:
    """Test Dyck words."""

    def test_is_dyck_empty(self):
        assert DyckWord.is_dyck('') is True

    def test_is_dyck_valid(self):
        assert DyckWord.is_dyck('()') is True
        assert DyckWord.is_dyck('(())') is True
        assert DyckWord.is_dyck('()()') is True

    def test_is_dyck_invalid(self):
        assert DyckWord.is_dyck('(') is False
        assert DyckWord.is_dyck(')') is False
        assert DyckWord.is_dyck(')(') is False
        assert DyckWord.is_dyck('(()') is False

    def test_generate_count(self):
        result = DyckWord.generate(3)
        assert len(result) == CatalanNumber.catalan(3)


class TestSetFamily:
    """Test set families."""

    def test_is_antichain_true(self):
        family = [{1}, {2}, {3}]
        assert SetFamily.is_antichain(family) is True

    def test_is_antichain_false(self):
        family = [{1}, {1, 2}]
        assert SetFamily.is_antichain(family) is False

    def test_is_intersecting_true(self):
        family = [{1, 2}, {1, 3}, {1, 4}]
        assert SetFamily.is_intersecting(family) is True

    def test_is_intersecting_false(self):
        family = [{1, 2}, {3, 4}]
        assert SetFamily.is_intersecting(family) is False

    def test_union_size(self):
        family = [{1, 2}, {2, 3}]
        assert SetFamily.union_size(family) == 3


class TestSpernerTheorem:
    """Test Sperner's theorem."""

    def test_max_antichain_size_1(self):
        assert SpernerTheorem.max_antichain_size(1) == 1

    def test_max_antichain_size_2(self):
        assert SpernerTheorem.max_antichain_size(2) == 2

    def test_max_antichain_size_3(self):
        assert SpernerTheorem.max_antichain_size(3) == 3

    def test_max_antichain_size_4(self):
        assert SpernerTheorem.max_antichain_size(4) == 6

    def test_middle_level(self):
        result = SpernerTheorem.middle_level(4)
        assert len(result) == SpernerTheorem.max_antichain_size(4)


class TestHallMarriage:
    """Test Hall's marriage theorem."""

    def test_hall_condition_true(self):
        # 2 brides, each can marry grooms 0 or 1
        bridesides = [{0, 1}, {0, 1}]
        assert HallMarriage.hall_condition(bridesides) is True

    def test_hall_condition_false(self):
        # 2 brides, both can only marry groom 0
        bridesides = [{0}, {0}]
        assert HallMarriage.hall_condition(bridesides) is False

    def test_has_perfect_matching_true(self):
        # Each bride has a distinct groom
        bridesides = [{0}, {1}]
        assert HallMarriage.has_perfect_matching(bridesides) is True


class TestBinomialCoefficient:
    """Test binomial coefficients."""

    def test_binom_0_0(self):
        assert BinomialCoefficient.binom(0, 0) == 1

    def test_binom_5_2(self):
        assert BinomialCoefficient.binom(5, 2) == 10

    def test_binom_5_5(self):
        assert BinomialCoefficient.binom(5, 5) == 1

    def test_binom_5_6(self):
        assert BinomialCoefficient.binom(5, 6) == 0

    def test_vandermonde(self):
        assert BinomialCoefficient.vandermonde(3, 2, 2) is True

    def test_binomial_theorem(self):
        result = BinomialCoefficient.binomial_theorem(1, 1, 3)
        assert abs(result - 8.0) < 1e-10
