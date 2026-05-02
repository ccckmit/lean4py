# 强化学习模块 (Reinforcement Learning Module)

> 本模块实现了经典的强化学习算法，包括 Q-Learning 和 SARSA。代码位于 `lean4py/reinforcement_learning.py`。

---

## 1. 马尔可夫决策过程 (MDP)

马尔可夫决策过程是强化学习的数学基础，由五元组定义：

```
MDP = (S, A, P, R, γ)
```

| 符号 | 含义 |
|------|------|
| **S** | 状态空间 (State Space)，所有可能状态的集合 |
| **A** | 动作空间 (Action Space)，所有可能动作的集合 |
| **P** | 状态转移概率 (Transition Probability)，P(s'|s,a) 表示在状态 s 执行动作 a 后转移到状态 s' 的概率 |
| **R** | 奖励函数 (Reward Function)，R(s,a) 或 R(s,a,s') 给出即时奖励 |
| **γ** | 折扣因子 (Discount Factor)，γ ∈ [0,1]，决定未来奖励的重要性 |

**马尔可夫性质**：未来状态仅依赖于当前状态和动作，与历史无关。

---

## 2. 策略 (Policy)

策略定义了智能体在给定状态下的行为：

```
π(a|s) = P(a_t = a | s_t = s)
```

- **确定性策略**：给定状态输出确定的动作 a = π(s)
- **随机策略**：给定状态下选择各动作的概率分布

本模块使用 **ε-greedy** 探索策略：

```python
def epsilon_greedy(q_values, epsilon=0.1):
    if random.random() < epsilon:
        return random.randint(0, len(q_values) - 1)  # 探索
    else:
        return q_values.index(max(q_values))           # 利用
```

---

## 3. 价值函数 (Value Function)

价值函数评估状态或状态-动作对的好坏程度。

### 状态价值函数 V^π(s)

```
V^π(s) = E_π[ Σ γ^t r_t | s_0 = s ]
```

- 从状态 s 出发，按照策略 π 行动，获得的折扣奖励总和的期望
- 衡量状态 s 的长期价值

### 状态-动作价值函数 Q^π(s,a)

```
Q^π(s,a) = E_π[ Σ γ^t r_t | s_0 = s, a_0 = a ]
```

- 从状态 s 出发，先执行动作 a，然后按照策略 π 行动，获得的折扣奖励总和的期望
- 衡量在状态 s 执行特定动作 a 的价值

---

## 4. 贝尔曼方程 (Bellman Equations)

### 贝尔曼期望方程

价值函数可递归分解：

```
V^π(s) = Σ_a π(a|s) · Σ_{s'} P(s'|s,a) · [ R(s,a,s') + γ · V^π(s') ]

Q^π(s,a) = Σ_{s'} P(s'|s,a) · [ R(s,a,s') + γ · Σ_{a'} π(a'|s') · Q^π(s',a') ]
```

### 贝尔曼最优方程 (Bellman Optimality Equations)

最优价值函数满足：

```
V*(s) = max_a Σ_{s'} P(s'|s,a) · [ R(s,a,s') + γ · V*(s') ]

Q*(s,a) = Σ_{s'} P(s'|s,a) · [ R(s,a,s') + γ · max_{a'} Q*(s',a') ]
```

最优策略：选择使价值最大化的动作

```
π*(s) = argmax_a Q*(s,a)
```

---

## 5. Q-Learning：离策略 TD 控制

Q-Learning 是一种**离策略**（off-policy）算法，直接学习最优 Q 函数。

### 算法核心

```python
# Q-Learning 更新规则
target = reward + gamma * max(Q(s', a'))  # 使用下一个状态的最大 Q 值
Q(s, a) += learning_rate * (target - Q(s, a))
```

### 关键特性

| 特性 | 说明 |
|------|------|
| **离策略** | 使用 ε-greedy 策略探索，但学习最优策略 |
| **时序差分 (TD)** | 结合蒙特卡洛和动态规划的思想 |
| **收敛性** | 在有限 MDP 中保证收敛到最优 Q 函数 |

### 本模块实现

```python
class QLearning:
    def update(self, state, action, reward, next_state, done=False):
        current_q = self.q_table[state][action]
        if done:
            target = reward  # 终止状态无未来奖励
        else:
            max_next_q = max(self.q_table[next_state])
            target = reward + self.gamma * max_next_q
        self.q_table[state][action] += self.lr * (target - current_q)
```

---

## 6. SARSA：同策略 TD 控制

SARSA 是一种**同策略**（on-policy）算法，学习正在执行的策略。

### 算法核心

```python
# SARSA 更新规则
target = reward + gamma * Q(s', a')  # 使用实际执行的下一个动作的 Q 值
Q(s, a) += learning_rate * (target - Q(s, a))
```

### Q-Learning vs SARSA

| 方面 | Q-Learning | SARSA |
|------|-----------|-------|
| 策略 | 离策略（学最优，用探索） | 同策略（学正在用的） |
| 更新 | 使用 max Q(s',a') | 使用 Q(s', a') 其中 a' 是实际执行的动作 |
| 探索安全性 | 可能学到冒险策略 | 更保守，适合在线学习 |
| 收敛性 | 更快收敛到最优 | 更保守，可能不是最优 |

---

## 7. 策略梯度方法 (Policy Gradient)

策略梯度方法直接优化策略参数 θ：

```
J(θ) = E_πθ[ Σ γ^t r_t ]
∇θ J(θ) = E_πθ[ ∇θ log πθ(a|s) · Q^π(s,a) ]
```

### REINFORCE 算法

```
θ ← θ + α · ∇θ log πθ(a|s) · G_t
```

其中 G_t 是从时间 t 开始的折扣奖励总和。

### 策略梯度定理

```
∇θ V^π(s) = Σ_a [ ∇θ π(a|s) · Q^π(s,a) ] = E_π [ ∇θ log π(a|s) · Q^π(s,a) ]
```

---

## 8. Actor-Critic 算法

Actor-Critic 结合了策略梯度（Actor）和价值函数（Critic）的优点。

### 结构

- **Actor**：策略网络，学习策略 π(a|s; θ)
- **Critic**：价值网络，学习 Q(s,a) 或 V(s)

### 算法流程

```
1. 根据当前策略 π 选择动作 a
2. 执行动作，获得 reward 和 next_state
3. Critic 更新价值估计：
   - TD 误差：δ = r + γ · V(s') - V(s)
   - V(s) ← V(s) + α · δ
4. Actor 更新策略：
   θ ← θ + β · ∇θ log π(a|s) · δ
```

### 优势

- 方差降低：使用价值函数作为 baseline
- 效率提升：Critic 帮助减少方差
- 在线学习：每步都可以更新

---

## 模块 API 参考

### QLearning 类

```python
class QLearning:
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount=0.9)
    def select_action(self, state, epsilon=0.1) -> int
    def update(self, state, action, reward, next_state, done=False)
    def get_policy(self) -> List[int]
```

### SARSA 类

```python
class SARSA:
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount=0.9)
    def select_action(self, state, epsilon=0.1) -> int
    def update(self, state, action, reward, next_state, next_action, done=False)
```

### 辅助函数

```python
def epsilon_greedy(q_values: List[float], epsilon: float = 0.1) -> int
def run_episode(agent, env_step, n_actions, start_state=0, epsilon=0.1, max_steps=100) -> Tuple[float, List[int]]
```

---

## 参考资料

1. Sutton, R. S., & Barto, A. G. *Reinforcement Learning: An Introduction* (2nd ed.)
2. Watkins, C. J. C. H. *Learning from Delayed Rewards* (1989)
3. Mnih, V. et al. *Human-level control through deep reinforcement learning* (Nature, 2015)