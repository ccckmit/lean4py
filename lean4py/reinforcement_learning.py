"""Reinforcement Learning module with Q-learning and SARSA."""

from typing import List, Dict, Tuple, Optional, Callable
import random
import math


class QLearning:
    """Q-learning agent for discrete state/action spaces."""
    
    def __init__(self, n_states: int, n_actions: int, learning_rate: float = 0.1, 
                 discount: float = 0.9):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount
        # Initialize Q-table with zeros
        self.q_table = [[0.0 for _ in range(n_actions)] for _ in range(n_states)]
    
    def select_action(self, state: int, epsilon: float = 0.1) -> int:
        """Select action using epsilon-greedy policy."""
        if random.random() < epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return self.q_table[state].index(max(self.q_table[state]))
    
    def update(self, state: int, action: int, reward: float, next_state: int, 
              done: bool = False):
        """Update Q-value using Q-learning rule."""
        current_q = self.q_table[state][action]
        
        if done:
            target = reward
        else:
            max_next_q = max(self.q_table[next_state])
            target = reward + self.gamma * max_next_q
        
        # Q-learning update
        self.q_table[state][action] += self.lr * (target - current_q)
    
    def get_policy(self) -> List[int]:
        """Get greedy policy from Q-table."""
        return [max(range(self.n_actions), key=lambda a: self.q_table[s][a]) 
                for s in range(self.n_states)]


class SARSA:
    """SARSA (State-Action-Reward-State-Action) learning agent."""
    
    def __init__(self, n_states: int, n_actions: int, learning_rate: float = 0.1,
                 discount: float = 0.9):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount
        self.q_table = [[0.0 for _ in range(n_actions)] for _ in range(n_states)]
    
    def select_action(self, state: int, epsilon: float = 0.1) -> int:
        """Select action using epsilon-greedy policy."""
        if random.random() < epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return self.q_table[state].index(max(self.q_table[state]))
    
    def update(self, state: int, action: int, reward: float, 
              next_state: int, next_action: int, done: bool = False):
        """Update Q-value using SARSA rule."""
        current_q = self.q_table[state][action]
        
        if done:
            target = reward
        else:
            target = reward + self.gamma * self.q_table[next_state][next_action]
        
        # SARSA update
        self.q_table[state][action] += self.lr * (target - current_q)


def epsilon_greedy(q_values: List[float], epsilon: float = 0.1) -> int:
    """Epsilon-greedy action selection.
    
    Args:
        q_values: Q-values for each action
        epsilon: Exploration rate (0 = greedy, 1 = random)
        
    Returns:
        Selected action index
    """
    if random.random() < epsilon:
        return random.randint(0, len(q_values) - 1)
    else:
        return q_values.index(max(q_values))


def run_episode(
    agent: object,
    env_step: Callable[[int, int], Tuple[float, int, bool]],
    n_actions: int,
    start_state: int = 0,
    epsilon: float = 0.1,
    max_steps: int = 100
) -> Tuple[float, List[int]]:
    """Run one episode with an agent.
    
    Args:
        agent: QLearning or SARSA agent
        env_step: Function that takes (state, action) and returns (reward, next_state, done)
        n_actions: Number of actions available
        start_state: Initial state
        epsilon: Exploration rate
        max_steps: Maximum steps per episode
        
    Returns:
        (total_reward, action_sequence)
    """
    state = start_state
    total_reward = 0.0
    actions = []
    
    for step in range(max_steps):
        action = agent.select_action(state, epsilon)
        actions.append(action)
        
        reward, next_state, done = env_step(state, action)
        total_reward += reward
        
        if hasattr(agent, 'update'):
            if isinstance(agent, QLearning):
                agent.update(state, action, reward, next_state, done)
            elif isinstance(agent, SARSA):
                next_action = agent.select_action(next_state, epsilon)
                agent.update(state, action, reward, next_state, next_action, done)
        
        state = next_state
        if done:
            break
    
    return total_reward, actions
