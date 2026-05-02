# 强化学习测试文档

本文档说明 `test_reinforcement_learning.py` 中测试用例的数学原理。

## 1. 测试验证内容概述

本测试文件验证强化学习模块的核心功能，包括：

- **Q-Learning 算法**：时序差分学习方法，基于最优 Q 值进行动作选择
- **SARSA 算法**：同策略时序差分学习方法
- **ε-贪心策略**：探索与利用的平衡机制
- **回合执行**：单回合交互的完整流程

---

## 2. MDP（马尔可夫决策过程）测试

### 2.1 MDP 基础数学模型

MDP 由四元组 $(S, A, P, R)$ 定义：

- $S$：状态空间
- $A$：动作空间
- $P$：状态转移概率 $P(s'|s,a)$
- $R$：奖励函数 $R(s,a,s')$

### 2.2 测试中的 MDP 元素

测试中的 `simple_env` 函数实现了确定性的 MDP：

```python
def simple_env(state, action):
    next_state = (state + action) % 2
    reward = 1.0 if next_state == 1 else 0.0
    done = False
    return reward, next_state, done
```

这对应一个转移规则：
- 状态转移：$s' = (s + a) \mod 2$
- 奖励：$R(s,a) = 1$ 当 $s' = 1$，否则 $R(s,a) = 0$

### 2.3 贝尔曼方程

值函数满足贝尔曼方程：

**状态值函数** $V^\pi(s)$：
$$V^\pi(s) = \sum_a \pi(a|s) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]$$

**动作值函数** $Q^\pi(s,a)$：
$$Q^\pi(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a')]$$

---

## 3. 值函数测试

### 3.1 Q 表初始化

```python
agent = QLearning(n_states=5, n_actions=3)
```

Q 表 $Q(s,a)$ 初始化为 $5 \times 3$ 的零矩阵：
$$Q = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$$

### 3.2 Q 值更新规则

Q-Learning 的更新公式为：
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

其中：
- $\alpha$：学习率（代码中为 `learning_rate`）
- $\gamma$：折扣因子（代码中为 `discount`）
- $r$：即时奖励
- $\max_{a'} Q(s',a')$：下一状态的最大 Q 值

### 3.3 测试验证

```python
def test_update(self):
    agent = QLearning(n_states=3, n_actions=2, learning_rate=0.5)
    initial_q = agent.q_table[0][0]
    agent.update(state=0, action=0, reward=1.0, next_state=1)
    assert agent.q_table[0][0] != initial_q
```

验证更新后 Q 值发生变化。

---

## 4. Q-Learning 测试

### 4.1 算法原理

Q-Learning 是一种**离策略**（off-policy）算法，直接学习最优策略：

$$Q_{t+1}(s,a) = Q_t(s,a) + \alpha [r + \gamma \max_{a'} Q_t(s',a') - Q_t(s,a)]$$

### 4.2 测试用例

#### 4.2.1 贪心动作选择

```python
def test_select_action_greedy(self):
    agent = QLearning(n_states=2, n_actions=2)
    agent.q_table[0] = [0.0, 1.0]  # 偏好动作 1
    action = agent.select_action(0, epsilon=0.0)
    assert action == 1
```

当 $\epsilon = 0$ 时，策略完全贪心：
$$\pi(a|s) = \begin{cases} 1 & \text{if } a = \arg\max_{a'} Q(s,a') \\ 0 & \text{otherwise} \end{cases}$$

由于 $Q(0,1) > Q(0,0)$，选择动作 $1$。

#### 4.2.2 探索机制

```python
def test_select_action_exploration(self):
    random.seed(42)
    actions = [agent.select_action(0, epsilon=1.0) for _ in range(10)]
    assert len(set(actions)) > 1
```

当 $\epsilon = 1$ 时，完全随机选择：
$$P(\text{选择 } a) = \frac{1}{|A|}$$

### 4.3 离策略特性

Q-Learning 使用 $\max$ 操作选择下一状态的最优动作，不依赖于当前策略：
$$\text{TD目标} = r + \gamma \max_{a'} Q(s',a')$$

---

## 5. SARSA 测试

### 5.1 算法原理

SARSA 是一种**同策略**（on-policy）算法，学习当前策略：

$$Q_{t+1}(s,a) = Q_t(s,a) + \alpha [r + \gamma Q_t(s',a') - Q_t(s,a)]$$

其中 $a'$ 是实际执行的动作。

### 5.2 与 Q-Learning 的区别

| 特性 | Q-Learning | SARSA |
|------|------------|-------|
| 策略类型 | 离策略 | 同策略 |
| TD目标 | $r + \gamma \max_{a'} Q(s',a')$ | $r + \gamma Q(s',a')$ |
| 收敛性 | 收敛于最优策略 | 收敛于安全策略 |

### 5.3 测试用例

```python
def test_select_action(self):
    agent = SARSA(n_states=3, n_actions=2)
    agent.q_table[0] = [1.0, 0.0]
    action = agent.select_action(0, epsilon=0.0)
    assert action == 0
```

验证 SARSA 的动作选择与 Q-Learning 一致（均为贪心），但更新规则不同。

---

## 6. ε-贪心策略测试

### 6.1 数学定义

ε-贪心策略：
$$\pi(a|s) = \begin{cases} 1 - \epsilon + \frac{\epsilon}{|A|} & \text{if } a = \arg\max Q(s,\cdot) \\ \frac{\epsilon}{|A|} & \text{otherwise} \end{cases}$$

### 6.2 测试验证

```python
def test_greedy_selection(self):
    q_values = [1.0, 2.0, 0.5]
    action = epsilon_greedy(q_values, epsilon=0.0)
    assert action == 1  # 最大值索引

def test_random_selection(self):
    q_values = [1.0, 2.0, 0.5]
    random.seed(42)
    actions = [epsilon_greedy(q_values, epsilon=1.0) for _ in range(20)]
    assert len(set(actions)) > 1
```

---

## 7. 回合执行测试

### 7.1 回合交互流程

```python
def run_episode(agent, env_step, n_actions, start_state=0, epsilon=0.1, max_steps=100):
    state = start_state
    total_reward = 0.0
    actions = []

    for step in range(max_steps):
        action = agent.select_action(state, epsilon)
        actions.append(action)

        reward, next_state, done = env_step(state, action)
        total_reward += reward

        if isinstance(agent, QLearning):
            agent.update(state, action, reward, next_state, done)
        elif isinstance(agent, SARSA):
            next_action = agent.select_action(next_state, epsilon)
            agent.update(state, action, reward, next_state, next_action, done)

        state = next_state
        if done:
            break

    return total_reward, actions
```

### 7.2 测试验证

```python
def test_simple_episode(self):
    agent = QLearning(n_states=2, n_actions=2)
    total_reward, actions = run_episode(
        agent, simple_env, n_actions=2,
        start_state=0, epsilon=0.1, max_steps=10
    )
    assert total_reward >= 0
    assert len(actions) <= 10
```

验证：
1. 总奖励非负
2. 动作数量不超过最大步数

---

## 8. 关键公式汇总

### 8.1 Q-Learning 更新
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$$

### 8.2 SARSA 更新
$$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma Q(s',a') - Q(s,a)]$$

### 8.3 ε-贪心
$$\pi(a|s) = \begin{cases} \epsilon/|A| & \text{随机} \\ 1 - \epsilon + \epsilon/|A| & \text{贪心} \end{cases}$$

### 8.4 折扣回报
$$G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k}$$