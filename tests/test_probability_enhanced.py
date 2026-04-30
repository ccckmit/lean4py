"""Tests for enhanced probability module."""

import pytest
from lean4py.probability_enhanced import (
    Martingale, StoppingTime, OptionalStoppingTheorem,
    CentralLimitTheorem, LawOfLargeNumbers,
    CharacteristicFunction, StochasticProcess
)


class TestMartingale:
    """Test martingale."""

    def test_creation(self):
        sequence = [1.0, 2.0, 3.0]
        m = Martingale(sequence)
        assert len(m.sequence) == 3

    def test_is_martingale(self):
        sequence = [1.0, 2.0, 3.0]
        m = Martingale(sequence)
        assert m.is_martingale(lambda t, f: True) is True


class TestStoppingTime:
    """Test stopping time."""

    def test_creation(self):
        values = [0, 1, 2, None, None]
        st = StoppingTime(values)
        assert len(st.values) == 5

    def test_is_stopping_time(self):
        values = [0, 1, 2, None, None]
        st = StoppingTime(values)
        assert st.is_stopping_time(filtration=[set() for _ in range(5)]) is True


class TestOptionalStoppingTheorem:
    """Test optional stopping theorem."""

    def test_holds(self):
        m = Martingale([1.0, 2.0, 3.0])
        st = StoppingTime([2])
        assert OptionalStoppingTheorem.holds(m, st) is True


class TestCentralLimitTheorem:
    """Test central limit theorem."""

    def test_sample_mean_var(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        mean, var = CentralLimitTheorem.sample_mean_var(data)
        assert isinstance(mean, float)
        assert isinstance(var, float)

    def test_is_approximately_normal(self):
        assert CentralLimitTheorem.is_approximately_normal(z=1.96, n=30) is True

    def test_confidence_interval(self):
        ci = CentralLimitTheorem.confidence_interval(mean=0.0, std_err=1.0)
        assert len(ci) == 2


class TestLawOfLargeNumbers:
    """Test law of large numbers."""

    def test_weak_law(self):
        means = [0.5, 0.6, 0.4, 0.55, 0.45]
        assert LawOfLargeNumbers.weak_law(means, true_mean=0.5) is True

    def test_strong_law(self):
        seq = [0.1, 0.2, 0.3]
        assert LawOfLargeNumbers.strong_law(seq, true_mean=0.5) is True


class TestCharacteristicFunction:
    """Test characteristic function."""

    def test_compute_normal(self):
        result = CharacteristicFunction.compute(t=1.0, distribution="normal", params={"mu": 0, "sigma": 1})
        assert isinstance(result, complex)

    def test_compute_default(self):
        result = CharacteristicFunction.compute(t=1.0, distribution="unknown")
        assert isinstance(result, complex)


class TestStochasticProcess:
    """Test stochastic process."""

    def test_creation(self):
        sp = StochasticProcess(process_type="random_walk")
        assert sp.type == "random_walk"

    def test_generate(self):
        sp = StochasticProcess(process_type="random_walk")
        path = sp.generate(steps=10)
        assert len(path) == 11  # Including initial 0

    def test_is_martingale(self):
        sp = StochasticProcess(process_type="random_walk")
        assert sp.is_martingale() is True
