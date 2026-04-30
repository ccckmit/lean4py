"""Tests for markov_chains module."""
import pytest
from lean4py.markov_chains import (
    DiscreteTimeMarkovChain,
    ContinuousTimeMarkovChain,
    TransitionMatrix,
    StationaryDistribution,
    DetailedBalance,
    AbsorbingStates,
    MarkovChainMonteCarlo,
    HittingProbability,
    MixingTime,
)


class TestDiscreteTimeMarkovChain:
    def test_creation(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        assert chain.n == 2

    def test_row_sums_to_one(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        for row in chain.transition_matrix:
            assert abs(sum(row) - 1.0) < 1e-6

    def test_invalid_matrix_raises(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.6, 0.3]]
        with pytest.raises(ValueError):
            DiscreteTimeMarkovChain(states, P)

    def test_transition_prob(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.3, 0.7]]
        chain = DiscreteTimeMarkovChain(states, P)
        assert abs(chain.transition_prob(0, 0) - 0.5) < 1e-6
        assert abs(chain.transition_prob(0, 1) - 0.5) < 1e-6

    def test_n_step_prob(self):
        states = {"a", "b"}
        P = [[1.0, 0.0], [0.0, 1.0]]
        chain = DiscreteTimeMarkovChain(states, P)
        assert abs(chain.n_step_prob(2, 0, 0) - 1.0) < 1e-6

    def test_is_irreducible(self):
        states = {"a", "b", "c"}
        P = [[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]
        chain = DiscreteTimeMarkovChain(states, P)
        assert chain.is_irreducible() is True

    def test_is_not_irreducible(self):
        states = {"a", "b", "c"}
        P = [[1.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.0, 0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        assert chain.is_irreducible() is False

    def test_communicating_classes(self):
        states = {"a", "b", "c"}
        P = [[1.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.0, 0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        classes = chain.communicating_classes()
        assert len(classes) >= 1

    def test_is_aperiodic(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        assert chain.is_aperiodic() is True


class TestContinuousTimeMarkovChain:
    def test_creation(self):
        states = {"a", "b"}
        Q = [[-1.0, 1.0], [1.0, -1.0]]
        ctmc = ContinuousTimeMarkovChain(states, Q)
        assert ctmc.n == 2

    def test_rows_sum_to_zero(self):
        states = {"a", "b"}
        Q = [[-1.0, 1.0], [1.0, -1.0]]
        ctmc = ContinuousTimeMarkovChain(states, Q)
        for row in ctmc.generator_matrix:
            assert abs(sum(row)) < 1e-6

    def test_invalid_generator_raises(self):
        states = {"a", "b"}
        Q = [[-1.0, 1.0], [1.0, 0.0]]
        with pytest.raises(ValueError):
            ContinuousTimeMarkovChain(states, Q)

    def test_rate(self):
        states = {"a", "b"}
        Q = [[-1.0, 1.0], [1.0, -1.0]]
        ctmc = ContinuousTimeMarkovChain(states, Q)
        assert abs(ctmc.rate(0, 1) - 1.0) < 1e-6

    def test_total_rate(self):
        states = {"a", "b"}
        Q = [[-1.0, 1.0], [1.0, -1.0]]
        ctmc = ContinuousTimeMarkovChain(states, Q)
        assert abs(ctmc.total_rate(0) - 1.0) < 1e-6

    def test_stationary_distribution(self):
        states = {"a", "b"}
        Q = [[-1.0, 1.0], [1.0, -1.0]]
        ctmc = ContinuousTimeMarkovChain(states, Q)
        pi = ctmc.stationary_distribution(max_iterations=100)
        assert len(pi) == 2
        assert abs(sum(pi) - 1.0) < 1e-3


class TestTransitionMatrix:
    def test_from_edges(self):
        states = ["a", "b"]
        edges = [("a", "b", 1.0), ("b", "a", 1.0)]
        P = TransitionMatrix.from_edges(states, edges)
        assert len(P) == 2
        assert abs(P[0][1] - 1.0) < 1e-6

    def test_from_edges_normalizes(self):
        states = ["a", "b", "c"]
        edges = [("a", "b", 1.0), ("a", "c", 1.0)]
        P = TransitionMatrix.from_edges(states, edges)
        assert abs(P[0][0]) < 1e-6
        assert abs(P[0][1] - 0.5) < 1e-6
        assert abs(P[0][2] - 0.5) < 1e-6


class TestStationaryDistribution:
    def test_creation(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        sd = StationaryDistribution([0.5, 0.5], chain)
        assert len(sd.distribution) == 2

    def test_verify(self):
        states = {"a", "b"}
        P = [[1.0, 0.0], [0.0, 1.0]]
        chain = DiscreteTimeMarkovChain(states, P)
        sd = StationaryDistribution([1.0, 0.0], chain)
        assert sd.verify() is True

    def test_probability_at_state(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        sd = StationaryDistribution([0.3, 0.7], chain)
        assert abs(sd.probability_at_state(0) - 0.3) < 1e-6
        assert abs(sd.probability_at_state(1) - 0.7) < 1e-6


class TestDetailedBalance:
    def test_holds(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        db = DetailedBalance(chain, [0.5, 0.5])
        assert db.holds() is True

    def test_does_not_hold(self):
        states = {"a", "b"}
        P = [[0.9, 0.1], [0.3, 0.7]]
        chain = DiscreteTimeMarkovChain(states, P)
        db = DetailedBalance(chain, [0.5, 0.5])
        assert db.holds() is False


class TestAbsorbingStates:
    def test_absorbing_states(self):
        states = {"a", "b", "c"}
        P = [[1.0, 0.0, 0.0], [0.3, 0.4, 0.3], [0.0, 0.0, 1.0]]
        chain = DiscreteTimeMarkovChain(states, P)
        ab = AbsorbingStates(chain)
        absorbing = ab.absorbing_states()
        assert 0 in absorbing
        assert 2 in absorbing

    def test_fundamental_matrix(self):
        states = {"a", "b"}
        P = [[1.0, 0.0], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        ab = AbsorbingStates(chain)
        N = ab.fundamental_matrix()
        assert len(N) == 2


class TestMarkovChainMonteCarlo:
    def test_creation(self):
        target = lambda x: 1.0
        mcmc = MarkovChainMonteCarlo(target)
        assert mcmc.target is target

    def test_metropolis_hastings(self):
        target = lambda x: 1.0
        proposal = lambda x: -x
        mcmc = MarkovChainMonteCarlo(target)
        samples = mcmc.metropolis_hastings(proposal, 1.0, num_samples=10)
        assert len(samples) == 11

    def test_gibbs_sampling(self):
        target = lambda x: 1.0
        mcmc = MarkovChainMonteCarlo(target)
        samples = mcmc.gibbs_sampling(1.0, num_samples=10)
        assert len(samples) == 1


class TestHittingProbability:
    def test_creation(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        hp = HittingProbability(chain)
        assert hp.chain is chain

    def test_compute_hitting(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        hp = HittingProbability(chain)
        h = hp.compute_hitting(0)
        assert len(h) == 2
        assert h[0] == 1.0

    def test_expected_hitting_time(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        hp = HittingProbability(chain)
        tau = hp.expected_hitting_time(0)
        assert len(tau) == 2


class TestMixingTime:
    def test_creation(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        mt = MixingTime(chain)
        assert mt.chain is chain

    def test_total_variation_distance(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        mt = MixingTime(chain)
        dist = mt.total_variation_distance(0, 0)
        assert dist >= 0.0

    def test_mixing_time(self):
        states = {"a", "b"}
        P = [[0.5, 0.5], [0.5, 0.5]]
        chain = DiscreteTimeMarkovChain(states, P)
        mt = MixingTime(chain)
        tau = mt.mixing_time(0.25)
        assert isinstance(tau, int)