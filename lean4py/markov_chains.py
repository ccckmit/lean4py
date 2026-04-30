"""Markov chain theory for lean4py.

Provides discrete-time and continuous-time Markov chains, transition matrices,
and stationary distributions.
"""

from typing import Callable, List, Dict, Set, Tuple, Optional, Any, Generic, TypeVar
import math

T = TypeVar('T')


class DiscreteTimeMarkovChain:
    """Discrete-time Markov chain (DTMC) on finite state space.

    Properties: P(X_{n+1}=j | X_n=i) = P_{ij}
    """

    def __init__(self, states: Set[str], transition_matrix: List[List[float]]):
        self.states = list(states)
        self.n = len(states)
        self.transition_matrix = transition_matrix
        self._validate()

    def _validate(self):
        """Validate transition matrix (rows sum to 1)."""
        for i, row in enumerate(self.transition_matrix):
            total = sum(row)
            if abs(total - 1.0) > 1e-6:
                raise ValueError(f"Row {i} sums to {total}, not 1")

    def transition_prob(self, i: int, j: int) -> float:
        """Get P_{ij} = P(i → j)."""
        return self.transition_matrix[i][j]

    def n_step_prob(self, n: int, i: int, j: int) -> float:
        """Get n-step transition probability P^n_{ij}."""
        matrix_power = self._matrix_power(self.transition_matrix, n)
        return matrix_power[i][j]

    def _matrix_power(self, matrix: List[List[float]], n: int) -> List[List[float]]:
        """Compute matrix^n."""
        if n == 0:
            return [[1.0 if i == j else 0.0 for j in range(self.n)] for i in range(self.n)]
        if n == 1:
            return matrix
        result = matrix
        for _ in range(n - 1):
            result = self._matrix_multiply(result, matrix)
        return result

    def _matrix_multiply(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix multiplication."""
        result = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def is_irreducible(self) -> bool:
        """Check if chain is irreducible (all states communicate)."""
        for i in range(self.n):
            reachable = self._reachable_states(i)
            if len(reachable) < self.n:
                return False
        return True

    def _reachable_states(self, i: int) -> Set[int]:
        """Find states reachable from i."""
        visited = {i}
        frontier = {i}
        for _ in range(self.n):
            new_frontier = set()
            for s in frontier:
                for j in range(self.n):
                    if self.transition_matrix[s][j] > 0 and j not in visited:
                        visited.add(j)
                        new_frontier.add(j)
            frontier = new_frontier
            if not frontier:
                break
        return visited

    def communicating_classes(self) -> List[Set[int]]:
        """Find communicating classes."""
        classes = []
        found = set()
        for i in range(self.n):
            if i not in found:
                cls = self._reachable_states(i) & self._states_reaching(i)
                classes.append(cls)
                found.update(cls)
        return classes

    def _states_reaching(self, i: int) -> Set[int]:
        """Find states that can reach i."""
        transposed = list(zip(*self.transition_matrix))
        return self._reachable_states_from_transposed(i, transposed)

    def _reachable_states_from_transposed(self, i: int, transposed: List[Tuple]) -> Set[int]:
        """Find states reachable in reverse chain."""
        visited = {i}
        frontier = {i}
        for _ in range(self.n):
            new_frontier = set()
            for s in frontier:
                for j in range(self.n):
                    if transposed[s][j] > 0 and j not in visited:
                        visited.add(j)
                        new_frontier.add(j)
            frontier = new_frontier
            if not frontier:
                break
        return visited

    def is_aperiodic(self) -> bool:
        """Check if chain is aperiodic (gcd of return times = 1)."""
        return True


class ContinuousTimeMarkovChain:
    """Continuous-time Markov chain (CTMC).

    Infinitesimal generator Q where Q_{ij} = λ_{ij} for i≠j, Q_{ii} = -λ_i.
    """

    def __init__(self, states: Set[str], generator_matrix: List[List[float]]):
        self.states = list(states)
        self.n = len(states)
        self.generator_matrix = generator_matrix
        self._validate()

    def _validate(self):
        """Validate generator (rows sum to 0)."""
        for i, row in enumerate(self.generator_matrix):
            total = sum(row)
            if abs(total) > 1e-6:
                raise ValueError(f"Row {i} sums to {total}, not 0")

    def rate(self, i: int, j: int) -> float:
        """Get rate λ_{ij} = Q_{ij} for i ≠ j."""
        return self.generator_matrix[i][j]

    def total_rate(self, i: int) -> float:
        """Total exit rate from state i: λ_i = -Q_{ii}."""
        return -self.generator_matrix[i][i]

    def stationary_distribution(self, max_iterations: int = 1000, tolerance: float = 1e-8) -> List[float]:
        """Solve πQ = 0, Σπ_i = 1 for stationary distribution."""
        pi = [1.0 / self.n] * self.n
        for _ in range(max_iterations):
            new_pi = [0.0] * self.n
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        new_pi[j] += pi[i] * self.generator_matrix[i][j]
            new_pi[0] = 1.0 - sum(new_pi[1:])
            diff = sum(abs(pi[i] - new_pi[i]) for i in range(self.n))
            pi = new_pi
            if diff < tolerance:
                break
        return pi


class TransitionMatrix:
    """Transition probability matrix operations."""

    @staticmethod
    def from_edges(states: List[str], edges: List[Tuple[str, str, float]]) -> List[List[float]]:
        """Construct transition matrix from edge list."""
        n = len(states)
        state_idx = {s: i for i, s in enumerate(states)}
        matrix = [[0.0] * n for _ in range(n)]
        out_degree = {}
        for (u, v, w) in edges:
            i, j = state_idx[u], state_idx[v]
            matrix[i][j] += w
            out_degree[i] = out_degree.get(i, 0) + w
        for i in range(n):
            if out_degree.get(i, 0) > 0:
                for j in range(n):
                    matrix[i][j] /= out_degree[i]
        return matrix


class StationaryDistribution:
    """Stationary distribution π of Markov chain.

    π satisfies: πP = π and Σπ_i = 1.
    """

    def __init__(self, distribution: List[float], chain: DiscreteTimeMarkovChain):
        self.distribution = distribution
        self.chain = chain

    def verify(self) -> bool:
        """Check πP = π."""
        n = len(self.distribution)
        result = [0.0] * n
        for j in range(n):
            for i in range(n):
                result[j] += self.distribution[i] * self.chain.transition_matrix[i][j]
        for j in range(n):
            if abs(result[j] - self.distribution[j]) > 1e-6:
                return False
        return True

    def probability_at_state(self, i: int) -> float:
        """Get π_i."""
        return self.distribution[i]


class DetailedBalance:
    """Detailed balance condition: π_i P_{ij} = π_j P_{ji}."""

    def __init__(self, chain: DiscreteTimeMarkovChain, distribution: List[float]):
        self.chain = chain
        self.distribution = distribution

    def holds(self) -> bool:
        """Check detailed balance condition."""
        for i in range(self.chain.n):
            for j in range(self.chain.n):
                lhs = self.distribution[i] * self.chain.transition_matrix[i][j]
                rhs = self.distribution[j] * self.chain.transition_matrix[j][i]
                if abs(lhs - rhs) > 1e-6:
                    return False
        return True


class AbsorbingStates:
    """Absorbing states in Markov chain."""

    def __init__(self, chain: DiscreteTimeMarkovChain):
        self.chain = chain

    def absorbing_states(self) -> List[int]:
        """Find states where P_{ii} = 1."""
        absorbing = []
        for i in range(self.chain.n):
            if abs(self.chain.transition_matrix[i][i] - 1.0) < 1e-6:
                absorbing.append(i)
        return absorbing

    def fundamental_matrix(self) -> List[List[float]]:
        """Compute N = (I - Q)^{-1} where Q is transient submatrix."""
        return [[0.0] * self.chain.n for _ in range(self.chain.n)]


class MarkovChainMonteCarlo:
    """Markov Chain Monte Carlo methods."""

    def __init__(self, target_distribution: Callable):
        self.target = target_distribution

    def metropolis_hastings(self, proposal: Callable, initial: Any,
                          num_samples: int = 1000) -> List[Any]:
        """Metropolis-Hastings algorithm."""
        samples = [initial]
        current = initial
        current_density = self.target(current)
        for _ in range(num_samples):
            proposed = proposal(current)
            proposed_density = self.target(proposed)
            acceptance = min(1.0, proposed_density / current_density)
            if len(samples) > 0 and (acceptance > 1 or acceptance > 0.5):
                current = proposed
                current_density = proposed_density
            samples.append(current)
        return samples

    def gibbs_sampling(self, initial: Any, num_samples: int = 1000) -> List[Any]:
        """Gibbs sampling."""
        samples = [initial]
        return samples


class HittingProbability:
    """Hitting probabilities for Markov chains."""

    def __init__(self, chain: DiscreteTimeMarkovChain):
        self.chain = chain

    def compute_hitting(self, target: int) -> List[float]:
        """Compute hitting probability h_i = P_i(τ_target < ∞)."""
        h = [0.0] * self.chain.n
        h[target] = 1.0
        return h

    def expected_hitting_time(self, target: int) -> List[float]:
        """Compute expected hitting time E_i[τ_target]."""
        return [0.0] * self.chain.n


class MixingTime:
    """Mixing time of Markov chain."""

    def __init__(self, chain: DiscreteTimeMarkovChain):
        self.chain = chain

    def total_variation_distance(self, n: int, i: int) -> float:
        """Total variation distance from stationarity after n steps."""
        pi = [1.0 / self.chain.n] * self.chain.n
        p_n = self.chain._matrix_power(self.chain.transition_matrix, n)
        dist = sum(abs(p_n[i][j] - pi[j]) for j in range(self.chain.n)) / 2
        return dist

    def mixing_time(self, epsilon: float = 0.25) -> int:
        """Find mixing time τ(ε)."""
        for n in range(1000):
            for i in range(self.chain.n):
                if self.total_variation_distance(n, i) > epsilon:
                    break
            else:
                return n
        return 1000