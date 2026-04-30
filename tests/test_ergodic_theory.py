"""Tests for ergodic_theory module."""
import pytest
from lean4py.ergodic_theory import (
    ErgodicTransformation,
    MeasurePreservingMap,
    ErgodicTheorem,
    MixingTransformation,
    KolmogorovSinaiEntropy,
    BernoulliShift,
    PoincareRecurrence,
    InvariantMeasure,
    ErgodicDecomposition,
)


class TestErgodicTransformation:
    def test_creation(self):
        space = {"a", "b", "c"}
        mu = lambda A: len(A) / 3
        T = lambda x: {"a": "b", "b": "c", "c": "a"}[x]
        et = ErgodicTransformation(space, mu, T)
        assert et.space == space

    def test_is_measure_preserving(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        assert et.is_measure_preserving() is True

    def test_is_ergodic(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        assert et.is_ergodic() is True

    def test_iterate(self):
        space = {"a", "b", "c"}
        T = lambda x: {"a": "b", "b": "c", "c": "a"}[x]
        et = ErgodicTransformation(space, lambda x: 1/3, T)
        assert et.iterate("a", 2) == "c"
        assert et.iterate("a", 3) == "a"

    def test_time_average(self):
        space = {"a", "b"}
        T = lambda x: x
        et = ErgodicTransformation(space, lambda x: 0.5, T)
        f = lambda x: 1 if x == "a" else 0
        avg = et.time_average(f, "a", 10)
        assert avg == 1.0

    def test_space_average(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        f = lambda x: 1 if x == "a" else 0
        avg = et.space_average(f, num_samples=10)
        assert 0.0 <= avg <= 1.0

    def test_Birkhoff_ergodic_theorem(self):
        space = {"a", "b", "c"}
        T = lambda x: {"a": "a", "b": "b", "c": "c"}[x]
        et = ErgodicTransformation(space, lambda x: 1/3, T)
        f = lambda x: 1
        time_avg, space_avg = et.Birkhoff_ergodic_theorem(f, "a", 100)
        assert time_avg == 1.0


class TestMeasurePreservingMap:
    def test_creation(self):
        domain = {"a", "b"}
        codomain = {"x", "y"}
        T = lambda x: "y" if x == "a" else "x"
        mpm = MeasurePreservingMap(domain, codomain, T, lambda A: 0.5)
        assert mpm.domain == domain

    def test_push_forward(self):
        domain = {"a", "b"}
        codomain = {"x", "y"}
        T = lambda x: "y" if x == "a" else "x"
        mpm = MeasurePreservingMap(domain, codomain, T, lambda A: 0.5)
        result = mpm.push_forward({"a"})
        assert "y" in result

    def test_is_measure_preserving(self):
        domain = {"a", "b"}
        codomain = {"x", "y"}
        mpm = MeasurePreservingMap(domain, codomain, lambda x: x, lambda A: 0.5)
        assert mpm.is_measure_preserving() is True


class TestErgodicTheorem:
    def test_Birkhoff(self):
        space = {"a", "b"}
        T = lambda x: x
        et = ErgodicTransformation(space, lambda x: 0.5, T)
        result = ErgodicTheorem.Birkhoff(et, lambda x: 1, "a", 10)
        assert result == 1.0

    def test_Kingman_subadditive(self):
        result = ErgodicTheorem.Kingman_subadditive(None, [1.0, 2.0, 3.0])
        assert result == 1.0

    def test_maximal_inequality(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        result = ErgodicTheorem.maximal_inequality(et, lambda x: 1, "a")
        assert result == 1


class TestMixingTransformation:
    def test_creation(self):
        T = lambda x: x
        mt = MixingTransformation(T, {"a", "b", "c"})
        assert mt.transform == T

    def test_is_weakly_mixing(self):
        mt = MixingTransformation(lambda x: x, {"a", "b"})
        assert mt.is_weakly_mixing() is True

    def test_is_strongly_mixing(self):
        mt = MixingTransformation(lambda x: x, {"a", "b"})
        assert mt.is_strongly_mixing() is True

    def test_is_bernoulli(self):
        mt = MixingTransformation(lambda x: x, {"a", "b"})
        assert mt.is_bernoulli() is True

    def test_correlation_function(self):
        mt = MixingTransformation(lambda x: x, {"a", "b"})
        f = lambda x: 1
        g = lambda x: 1
        corr = mt.correlation_function(f, g, 10)
        assert corr == 0.0

    def test_spectral_radius(self):
        mt = MixingTransformation(lambda x: x, {"a", "b"})
        assert mt.spectral_radius() == 1.0


class TestKolmogorovSinaiEntropy:
    def test_creation(self):
        space = {"a", "b", "c", "d"}
        T = lambda x: x
        et = ErgodicTransformation(space, lambda x: 0.25, T)
        partition = [{"a", "b"}, {"c", "d"}]
        ks = KolmogorovSinaiEntropy(et, partition)
        assert ks.transformation is et

    def test_partition_entropy(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        partition = [{"a"}, {"b"}]
        ks = KolmogorovSinaiEntropy(et, partition)
        H = ks.partition_entropy()
        assert H >= 0

    def test_conditional_entropy(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        partition = [{"a"}, {"b"}]
        ks = KolmogorovSinaiEntropy(et, partition)
        H = ks.conditional_entropy(partition, partition)
        assert H == 0.0

    def test_compute_ks_entropy(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        partition = [{"a"}, {"b"}]
        ks = KolmogorovSinaiEntropy(et, partition)
        h = ks.compute_ks_entropy()
        assert h >= 0

    def test_Pesin_entropy_formula(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        ks = KolmogorovSinaiEntropy(et, [])
        lyap = [0.5, -0.3]
        h = ks.Pesin_entropy_formula(lyap)
        assert h == 0.5

    def test_isomorphism_invariant(self):
        space = {"a", "b"}
        et = ErgodicTransformation(space, lambda x: 0.5, lambda x: x)
        partition = [{"a"}, {"b"}]
        ks = KolmogorovSinaiEntropy(et, partition)
        assert ks.isomorphism_invariant() >= 0


class TestBernoulliShift:
    def test_creation(self):
        bs = BernoulliShift(2, [0.5, 0.5])
        assert bs.base == 2

    def test_shift_map(self):
        bs = BernoulliShift(2)
        seq = [0, 1, 0, 1]
        shifted = bs.shift_map(seq)
        assert shifted == [1, 0, 1]

    def test_is_bernoulli(self):
        bs = BernoulliShift(2)
        assert bs.is_bernoulli() is True

    def test_kolmogorov_entropy(self):
        bs = BernoulliShift(2, [0.5, 0.5])
        h = bs.kolmogorov_entropy()
        assert h == 1.0

    def test_kolmogorov_entropy_unfair(self):
        bs = BernoulliShift(2, [0.75, 0.25])
        h = bs.kolmogorov_entropy()
        assert h > 0 and h < 2


class TestPoincareRecurrence:
    def test_creation(self):
        space = {"a", "b", "c"}
        T = lambda x: {"a": "b", "b": "c", "c": "a"}[x]
        pr = PoincareRecurrence(space, T)
        assert pr.space == space

    def test_recurrence_time(self):
        space = {"a", "b", "c"}
        T = lambda x: {"a": "b", "b": "c", "c": "a"}[x]
        pr = PoincareRecurrence(space, T)
        t = pr.recurrence_time("c", {"a", "b"}, max_iter=10)
        assert t == 1

    def test_almost_all_recurrent(self):
        pr = PoincareRecurrence({"a", "b"}, lambda x: x)
        assert pr.almost_all_recurrent() is True

    def test_recurrence_theorem(self):
        pr = PoincareRecurrence({"a", "b"}, lambda x: x)
        result = pr.recurrence_theorem({"a"})
        assert isinstance(result, list)


class TestInvariantMeasure:
    def test_creation(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        assert mu.space == space

    def test_apply_to_set(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        assert mu.apply_to_set({"a"}) == 0.5

    def test_is_T_invariant(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        assert mu.is_T_invariant(lambda x: x) is True

    def test_ergodic_decomposition(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        decomp = mu.ergodic_decomposition(lambda x: x)
        assert isinstance(decomp, list)


class TestErgodicDecomposition:
    def test_creation(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        ed = ErgodicDecomposition(mu)
        assert ed.measure is mu

    def test_decomposition_exists(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        ed = ErgodicDecomposition(mu)
        assert ed.decomposition_exists() is True

    def test_uniqueness(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        ed = ErgodicDecomposition(mu)
        result = ed.uniqueness()
        assert isinstance(result, bool)

    def test_support_of_component(self):
        space = {"a", "b"}
        mu = InvariantMeasure(space, lambda A: len(A) / 2)
        ed = ErgodicDecomposition(mu)
        assert ed.support_of_component(0) == space