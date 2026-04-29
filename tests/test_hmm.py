"""Tests for Hidden Markov Model module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.hmm import HMM
import math


class TestHMM:
    """Tests for HMM class."""
    
    def test_initialization(self):
        """Test HMM initializes correctly."""
        hmm = HMM(n_states=3, n_observations=4)
        
        assert hmm.n_states == 3
        assert hmm.n_observations == 4
        assert len(hmm.transitions) == 3
        assert len(hmm.emissions) == 3
        assert len(hmm.initial_probs) == 3
    
    def test_forward_algorithm(self):
        """Test forward algorithm computes likelihood."""
        # Simple HMM: 2 states, 2 observations
        hmm = HMM(
            n_states=2,
            n_observations=2,
            transitions=[[0.9, 0.1], [0.1, 0.9]],
            emissions=[[0.9, 0.1], [0.1, 0.9]],
            initial_probs=[0.5, 0.5]
        )
        
        # All observations in state 0
        log_lik, alpha = hmm.forward_algorithm([0, 0, 0])
        
        assert isinstance(log_lik, float)
        assert len(alpha) == 3
        assert len(alpha[0]) == 2
    
    def test_viterbi(self):
        """Test Viterbi algorithm finds best path."""
        hmm = HMM(
            n_states=2,
            n_observations=2,
            transitions=[[0.9, 0.1], [0.1, 0.9]],
            emissions=[[0.9, 0.1], [0.1, 0.9]],
            initial_probs=[0.5, 0.5]
        )
        
        observations = [0, 0, 0]
        best_path, log_prob = hmm.viterbi(observations)
        
        assert len(best_path) == 3
        assert isinstance(log_prob, float)
    
    def test_sample(self):
        """Test generating samples from HMM."""
        hmm = HMM(
            n_states=2,
            n_observations=2,
            transitions=[[0.9, 0.1], [0.1, 0.9]],
            emissions=[[0.9, 0.1], [0.1, 0.9]],
            initial_probs=[0.5, 0.5]
        )
        
        states, observations = hmm.sample(10)
        
        assert len(states) == 10
        assert len(observations) == 10
        assert all(s in [0, 1] for s in states)
        assert all(o in [0, 1] for o in observations)