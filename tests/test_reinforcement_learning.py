"""Tests for reinforcement learning module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.reinforcement_learning import (
    QLearning, SARSA, epsilon_greedy, run_episode
)
import random


class TestQLearning:
    """Tests for Q-learning agent."""
    
    def test_initialization(self):
        """Test Q-learning agent initializes correctly."""
        agent = QLearning(n_states=5, n_actions=3)
        
        assert agent.n_states == 5
        assert agent.n_actions == 3
        assert len(agent.q_table) == 5
        assert all(len(row) == 3 for row in agent.q_table)
    
    def test_select_action_greedy(self):
        """Test greedy action selection."""
        agent = QLearning(n_states=2, n_actions=2)
        agent.q_table[0] = [0.0, 1.0]  # Prefer action 1
        
        action = agent.select_action(0, epsilon=0.0)
        assert action == 1  # Should select action with highest Q-value
    
    def test_select_action_exploration(self):
        """Test epsilon-greedy includes exploration."""
        agent = QLearning(n_states=2, n_actions=2)
        
        # With epsilon=1.0, should select randomly
        random.seed(42)
        actions = [agent.select_action(0, epsilon=1.0) for _ in range(10)]
        assert len(set(actions)) > 1  # Should see multiple actions
    
    def test_update(self):
        """Test Q-learning update rule."""
        agent = QLearning(n_states=3, n_actions=2, learning_rate=0.5)
        
        initial_q = agent.q_table[0][0]
        
        # Update: Q(s,a) = Q(s,a) + lr * (r + gamma * max Q(s',:) - Q(s,a))
        agent.update(state=0, action=0, reward=1.0, next_state=1)
        
        assert agent.q_table[0][0] != initial_q


class TestSARSA:
    """Tests for SARSA agent."""
    
    def test_initialization(self):
        """Test SARSA agent initializes correctly."""
        agent = SARSA(n_states=4, n_actions=3)
        
        assert agent.n_states == 4
        assert agent.n_actions == 3
    
    def test_select_action(self):
        """Test action selection."""
        agent = SARSA(n_states=3, n_actions=2)
        agent.q_table[0] = [1.0, 0.0]
        
        action = agent.select_action(0, epsilon=0.0)
        assert action == 0  # Should select action with highest Q-value


class TestEpsilonGreedy:
    """Tests for epsilon-greedy function."""
    
    def test_greedy_selection(self):
        """Test greedy selection when epsilon=0."""
        q_values = [1.0, 2.0, 0.5]
        action = epsilon_greedy(q_values, epsilon=0.0)
        assert action == 1  # Index of max value
    
    def test_random_selection(self):
        """Test random selection when epsilon=1."""
        q_values = [1.0, 2.0, 0.5]
        random.seed(42)
        actions = [epsilon_greedy(q_values, epsilon=1.0) for _ in range(20)]
        assert len(set(actions)) > 1


class TestRunEpisode:
    """Tests for run_episode function."""
    
    def test_simple_episode(self):
        """Test running a simple episode."""
        agent = QLearning(n_states=2, n_actions=2)
        
        def simple_env(state, action):
            # Deterministic environment: move to next state
            next_state = (state + action) % 2
            reward = 1.0 if next_state == 1 else 0.0
            done = False
            return reward, next_state, done
        
        total_reward, actions = run_episode(
            agent, simple_env, n_actions=2,
            start_state=0, epsilon=0.1, max_steps=10
        )
        
        assert total_reward >= 0
        assert len(actions) <= 10