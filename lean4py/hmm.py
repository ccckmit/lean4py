"""Hidden Markov Model module."""

from typing import List, Tuple, Optional
import math


class HMM:
    """Hidden Markov Model."""
    
    def __init__(
        self,
        n_states: int,
        n_observations: int,
        transitions: Optional[List[List[float]]] = None,
        emissions: Optional[List[List[float]]] = None,
        initial_probs: Optional[List[float]] = None
    ):
        self.n_states = n_states
        self.n_observations = n_observations
        
        # Initialize with uniform probabilities if not provided
        if transitions is None:
            self.transitions = [[1.0/n_states] * n_states for _ in range(n_states)]
        else:
            self.transitions = transitions
        
        if emissions is None:
            self.emissions = [[1.0/n_observations] * n_observations for _ in range(n_states)]
        else:
            self.emissions = emissions
        
        if initial_probs is None:
            self.initial_probs = [1.0/n_states] * n_states
        else:
            self.initial_probs = initial_probs
    
    def forward_algorithm(self, observations: List[int]) -> Tuple[float, List[List[float]]]:
        """Forward algorithm to compute likelihood.
        
        Args:
            observations: List of observation indices
            
        Returns:
            (log_likelihood, alpha) where alpha is forward probabilities
        """
        T = len(observations)
        if T == 0:
            return 0.0, []
        
        # Initialize alpha_0
        alpha = [[0.0] * self.n_states for _ in range(T)]
        for s in range(self.n_states):
            alpha[0][s] = self.initial_probs[s] * self.emissions[s][observations[0]]
        
        # Recursion
        for t in range(1, T):
            for j in range(self.n_states):
                alpha[t][j] = self.emissions[j][observations[t]] * \
                             sum(alpha[t-1][i] * self.transitions[i][j] 
                                 for i in range(self.n_states))
        
        # Termination
        likelihood = sum(alpha[T-1][s] for s in range(self.n_states))
        
        # Return log likelihood
        if likelihood > 0:
            log_likelihood = math.log(likelihood)
        else:
            log_likelihood = -float('inf')
        
        return log_likelihood, alpha
    
    def viterbi(self, observations: List[int]) -> Tuple[List[int], float]:
        """Viterbi algorithm to find most likely state sequence.
        
        Args:
            observations: List of observation indices
            
        Returns:
            (best_path, log_prob) - best state sequence and its log probability
        """
        T = len(observations)
        if T == 0:
            return [], 0.0
        
        # Initialize delta and psi
        delta = [[0.0] * self.n_states for _ in range(T)]
        psi = [[0] * self.n_states for _ in range(T)]
        
        # Initialization
        for s in range(self.n_states):
            delta[0][s] = self.initial_probs[s] * self.emissions[s][observations[0]]
        
        # Recursion
        for t in range(1, T):
            for j in range(self.n_states):
                probs = [delta[t-1][i] * self.transitions[i][j] 
                         for i in range(self.n_states)]
                psi[t][j] = max(range(self.n_states), key=lambda i: probs[i])
                delta[t][j] = max(probs) * self.emissions[j][observations[t]]
        
        # Backtrack
        best_path = [0] * T
        best_path[T-1] = max(range(self.n_states), key=lambda s: delta[T-1][s])
        
        for t in range(T-2, -1, -1):
            best_path[t] = psi[t+1][best_path[t+1]]
        
        # Log probability
        log_prob = math.log(max(delta[T-1])) if max(delta[T-1]) > 0 else -float('inf')
        
        return best_path, log_prob
    
    def baum_welch(self, observations: List[int], max_iter: int = 100, tol: float = 1e-6):
        """Baum-Welch algorithm for parameter estimation.
        
        Updates transition, emission, and initial probabilities.
        
        Args:
            observations: List of observation indices
            max_iter: Maximum iterations
            tol: Convergence tolerance
        """
        T = len(observations)
        if T == 0:
            return
        
        for iteration in range(max_iter):
            # E-step: Forward and backward algorithms
            log_likelihood, alpha = self.forward_algorithm(observations)
            
            # Backward algorithm
            beta = [[0.0] * self.n_states for _ in range(T)]
            for s in range(self.n_states):
                beta[T-1][s] = 1.0
            
            for t in range(T-2, -1, -1):
                for i in range(self.n_states):
                    beta[t][i] = sum(
                        self.transitions[i][j] * self.emissions[j][observations[t+1]] * beta[t+1][j]
                        for j in range(self.n_states)
                    )
            
            # Compute xi (expected transitions)
            xi = [[[0.0] * self.n_states for _ in range(self.n_states)] for _ in range(T-1)]
            for t in range(T-1):
                denom = sum(
                    alpha[t][i] * self.transitions[i][j] * 
                    self.emissions[j][observations[t+1]] * beta[t+1][j]
                    for i in range(self.n_states)
                    for j in range(self.n_states)
                )
                if denom > 0:
                    for i in range(self.n_states):
                        for j in range(self.n_states):
                            xi[t][i][j] = alpha[t][i] * self.transitions[i][j] * \
                                         self.emissions[j][observations[t+1]] * beta[t+1][j] / denom
            
            # M-step: Update parameters
            # Update initial probabilities
            for s in range(self.n_states):
                self.initial_probs[s] = alpha[0][s] * beta[0][s]
            total = sum(self.initial_probs)
            if total > 0:
                self.initial_probs = [p/total for p in self.initial_probs]
            
            # Update transitions
            for i in range(self.n_states):
                for j in range(self.n_states):
                    numer = sum(xi[t][i][j] for t in range(T-1))
                    denom = sum(xi[t][i][k] for t in range(T-1) for k in range(self.n_states))
                    if denom > 0:
                        self.transitions[i][j] = numer / denom
            
            # Update emissions
            for j in range(self.n_states):
                for o in range(self.n_observations):
                    numer = sum(
                        xi[t][j][k] for t in range(T-1) 
                        for k in range(self.n_states)
                        if observations[t+1] == o
                    )
                    denom = sum(xi[t][j][k] for t in range(T-1) for k in range(self.n_states))
                    if denom > 0:
                        self.emissions[j][o] = numer / denom
    
    def sample(self, n_steps: int) -> Tuple[List[int], List[int]]:
        """Generate a sample sequence from the HMM.
        
        Args:
            n_steps: Number of steps to generate
            
        Returns:
            (states, observations) - sampled state and observation sequences
        """
        import random
        
        states = []
        observations = []
        
        # Sample initial state
        state = random.choices(range(self.n_states), weights=self.initial_probs)[0]
        obs = random.choices(range(self.n_observations), weights=self.emissions[state])[0]
        states.append(state)
        observations.append(obs)
        
        for _ in range(n_steps - 1):
            # Sample next state
            state = random.choices(range(self.n_states), weights=self.transitions[state])[0]
            obs = random.choices(range(self.n_observations), weights=self.emissions[state])[0]
            states.append(state)
            observations.append(obs)
        
        return states, observations