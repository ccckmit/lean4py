# 隐马尔可夫模型 (Hidden Markov Model)

## 1. 概述

隐马尔可夫模型（HMM）是一种统计模型，用于描述由一个隐藏的马尔可夫链生成观测序列的过程。HMM 广泛应用语音识别、自然语言处理、生物信息学等领域。

### 1.1 基本组成

- **隐状态 (Latent States)**：系统的真实状态，记为 $S = \{s_1, s_2, \ldots, s_N\}$，共 $N$ 个状态
- **观测 (Observations)**：可观测到的输出，记为 $O = \{o_1, o_2, \ldots, o_M\}$，共 $M$ 种观测值
- **转移概率 (Transition Probabilities)**：$A = [a_{ij}] = P(q_t = s_j | q_{t-1} = s_i)$，表示从状态 $i$ 转移到状态 $j$ 的概率
- **发射概率 (Emission Probabilities)**：$B = [b_j(k)] = P(o_t = o_k | q_t = s_j)$，表示在状态 $j$ 下观测到 $o_k$ 的概率
- **初始概率 (Initial Probabilities)**：$\pi = [\pi_i] = P(q_1 = s_i)$，表示初始状态的概率分布

HMM 由三元组 $\lambda = (A, B, \pi)$ 完全描述。

---

## 2. 三个基本问题

### 问题一：评估问题 (Evaluation)
给定模型 $\lambda$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$，计算 $P(O|\lambda)$，即观测序列出现的概率。

### 问题二：解码问题 (Decoding)
给定模型 $\lambda$ 和观测序列 $O$，找出最可能的状态序列 $Q = (q_1, q_2, \ldots, q_T)$。

### 问题三：学习问题 (Learning)
给定观测序列 $O$，调整模型参数 $\lambda = (A, B, \pi)$ 使得 $P(O|\lambda)$ 最大。

---

## 3. 前向算法 (Forward Algorithm)

### 3.1 问题背景

直接计算 $P(O|\lambda)$ 需要对所有可能的状态序列求和：

$$P(O|\lambda) = \sum_{Q} P(O|Q, \lambda) P(Q|\lambda)$$

这在长度为 $T$ 时需要 $O(N^T)$ 的计算量，前向算法将此复杂度降至 $O(N^2 T)$。

### 3.2 前向变量

定义前向变量 $\alpha_t(i)$ 为：

$$\alpha_t(i) = P(o_1, o_2, \ldots, o_t, q_t = s_i | \lambda)$$

即给定模型 $\lambda$，到时刻 $t$ 为止观测到 $(o_1, \ldots, o_t)$ 且当前状态为 $s_i$ 的概率。

### 3.3 算法步骤

**初始化** ($t = 1$)：
$$\alpha_1(i) = \pi_i \cdot b_i(o_1)$$

**递归** ($t = 2, 3, \ldots, T$)：
$$\alpha_t(j) = b_j(o_t) \sum_{i=1}^{N} \alpha_{t-1}(i) \cdot a_{ij}$$

**终止**：
$$P(O|\lambda) = \sum_{i=1}^{N} \alpha_T(i)$$

### 3.4 代码实现

```python
def forward_algorithm(self, observations: List[int]) -> Tuple[float, List[List[float]]]:
    T = len(observations)
    alpha = [[0.0] * self.n_states for _ in range(T)]

    # 初始化
    for s in range(self.n_states):
        alpha[0][s] = self.initial_probs[s] * self.emissions[s][observations[0]]

    # 递归
    for t in range(1, T):
        for j in range(self.n_states):
            alpha[t][j] = self.emissions[j][observations[t]] * \
                         sum(alpha[t-1][i] * self.transitions[i][j]
                             for i in range(self.n_states))

    # 终止：计算似然
    likelihood = sum(alpha[T-1][s] for s in range(self.n_states))
    log_likelihood = math.log(likelihood) if likelihood > 0 else -float('inf')

    return log_likelihood, alpha
```

### 3.5 对数似然

为避免概率连乘导致的数值下溢，通常使用对数似然 $\log P(O|\lambda)$。本模块在返回前自动进行对数变换。

---

## 4. Viterbi 算法

### 4.1 问题背景

Viterbi 算法解决解码问题：找到最可能生成观测序列的状态序列。

### 4.2 算法思想

动态规划思想，定义 $\delta_t(i)$ 为时刻 $t$ 到达状态 $s_i$ 的最优路径的概率：

$$\delta_t(i) = \max_{q_1, \ldots, q_{t-1}} P(q_t = s_i, q_1, \ldots, q_{t-1}, o_1, \ldots, o_t | \lambda)$$

同时记录回溯指针 $\psi_t(i)$ 记录到达状态 $s_i$ 的前一个最优状态。

### 4.3 算法步骤

**初始化** ($t = 1$)：
$$\delta_1(i) = \pi_i \cdot b_i(o_1)$$
$$\psi_1(i) = 0$$

**递归** ($t = 2, 3, \ldots, T$)：
$$\delta_t(j) = \max_{i} [\delta_{t-1}(i) \cdot a_{ij}] \cdot b_j(o_t)$$
$$\psi_t(j) = \arg\max_{i} [\delta_{t-1}(i) \cdot a_{ij}]$$

**终止**：
$$P^* = \max_{i} \delta_T(i)$$
$$q_T^* = \arg\max_{i} \delta_T(i)$$

**回溯** ($t = T-1, T-2, \ldots, 1$)：
$$q_t^* = \psi_{t+1}(q_{t+1}^*)$$

### 4.4 代码实现

```python
def viterbi(self, observations: List[int]) -> Tuple[List[int], float]:
    T = len(observations)
    delta = [[0.0] * self.n_states for _ in range(T)]
    psi = [[0] * self.n_states for _ in range(T)]

    # 初始化
    for s in range(self.n_states):
        delta[0][s] = self.initial_probs[s] * self.emissions[s][observations[0]]

    # 递归
    for t in range(1, T):
        for j in range(self.n_states):
            probs = [delta[t-1][i] * self.transitions[i][j]
                     for i in range(self.n_states)]
            psi[t][j] = max(range(self.n_states), key=lambda i: probs[i])
            delta[t][j] = max(probs) * self.emissions[j][observations[t]]

    # 回溯
    best_path = [0] * T
    best_path[T-1] = max(range(self.n_states), key=lambda s: delta[T-1][s])

    for t in range(T-2, -1, -1):
        best_path[t] = psi[t+1][best_path[t+1]]

    log_prob = math.log(max(delta[T-1])) if max(delta[T-1]) > 0 else -float('inf')
    return best_path, log_prob
```

---

## 5. Baum-Welch 算法

### 5.1 问题背景

Baum-Welch 算法是 EM 算法在 HMM 参数估计中的应用，用于学习给定观测序列下的最优模型参数。

### 5.2 后向变量

定义后向变量 $\beta_t(i)$：

$$\beta_t(i) = P(o_{t+1}, o_{t+2}, \ldots, o_T | q_t = s_i, \lambda)$$

**初始化**：
$$\beta_T(i) = 1$$

**递归** ($t = T-1, T-2, \ldots, 1$)：
$$\beta_t(i) = \sum_{j=1}^{N} a_{ij} \cdot b_j(o_{t+1}) \cdot \beta_{t+1}(j)$$

### 5.3 EM 算法步骤

**E 步**：计算期望的充分统计量

1. 计算前向变量 $\alpha_t(i)$ 和后向变量 $\beta_t(i)$
2. 计算 $\xi_t(i, j)$：时刻 $t$ 在状态 $s_i$，时刻 $t+1$ 在状态 $s_j$ 的概率

$$\xi_t(i, j) = \frac{\alpha_t(i) a_{ij} b_j(o_{t+1}) \beta_{t+1}(j)}{\sum_{i'}\sum_{j'} \alpha_t(i') a_{i'j'} b_{j'}(o_{t+1}) \beta_{t+1}(j')}$$

**M 步**：更新参数

$$\pi_i = \frac{\alpha_1(i) \beta_1(i)}{\sum_{j} \alpha_1(j) \beta_1(j)}$$

$$a_{ij} = \frac{\sum_{t=1}^{T-1} \xi_t(i, j)}{\sum_{t=1}^{T-1} \sum_{k} \xi_t(i, k)}$$

$$b_j(k) = \frac{\sum_{t=1}^{T-1} \xi_t(j, k) \cdot \mathbf{1}(o_{t+1} = o_k)}{\sum_{t=1}^{T-1} \sum_{k} \xi_t(j, k)}$$

### 5.4 代码实现

```python
def baum_welch(self, observations: List[int], max_iter: int = 100, tol: float = 1e-6):
    T = len(observations)

    for iteration in range(max_iter):
        # E步：前向后向算法
        log_likelihood, alpha = self.forward_algorithm(observations)

        # 后向算法
        beta = [[0.0] * self.n_states for _ in range(T)]
        for s in range(self.n_states):
            beta[T-1][s] = 1.0

        for t in range(T-2, -1, -1):
            for i in range(self.n_states):
                beta[t][i] = sum(
                    self.transitions[i][j] * self.emissions[j][observations[t+1]] * beta[t+1][j]
                    for j in range(self.n_states)
                )

        # 计算 xi (期望转移次数)
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

        # M步：更新参数
        # 更新初始概率
        for s in range(self.n_states):
            self.initial_probs[s] = alpha[0][s] * beta[0][s]
        total = sum(self.initial_probs)
        if total > 0:
            self.initial_probs = [p/total for p in self.initial_probs]

        # 更新转移概率
        for i in range(self.n_states):
            for j in range(self.n_states):
                numer = sum(xi[t][i][j] for t in range(T-1))
                denom = sum(xi[t][i][k] for t in range(T-1) for k in range(self.n_states))
                if denom > 0:
                    self.transitions[i][j] = numer / denom

        # 更新发射概率
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
```

---

## 6. 似然计算

### 6.1 观测序列似然

给定模型 $\lambda$ 和观测序列 $O$，观测序列的似然为：

$$P(O|\lambda) = \sum_{Q} P(O|Q, \lambda) P(Q|\lambda)$$

通过前向算法计算，时间复杂度为 $O(N^2 T)$。

### 6.2 对数似然的数值稳定性

概率值可能极小，导致下溢。使用对数似然：

$$\log P(O|\lambda) = \log \sum_{i=1}^{N} \alpha_T(i)$$

本模块通过 `forward_algorithm` 返回对数似然值。

---

## 7. 状态后验概率

### 7.1 后验概率定义

给定观测序列和模型，时刻 $t$ 处于状态 $s_i$ 的后验概率为：

$$\gamma_t(i) = P(q_t = s_i | O, \lambda) = \frac{\alpha_t(i) \beta_t(i)}{P(O|\lambda)}$$

其中 $\alpha_t(i)$ 是前向变量，$\beta_t(i)$ 是后向变量。

### 7.2 计算方法

结合前向和后向变量：

1. 运行前向算法得到 $\alpha_t(i)$
2. 运行后向算法得到 $\beta_t(i)$
3. 对每个 $t, i$ 计算 $\gamma_t(i) = \frac{\alpha_t(i) \beta_t(i)}{\sum_{j} \alpha_t(j) \beta_t(j)}$

### 7.3 应用场景

- 状态序列的边际概率计算
- 识别特定时刻最可能的状态
- 作为其他算法（如条件随机场）的特征

---

## 8. HMM 类接口

### 8.1 初始化参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `n_states` | int | 隐状态数量 $N$ |
| `n_observations` | int | 观测值数量 $M$ |
| `transitions` | List[List[float]] | 转移概率矩阵 $A$ ($N \times N$) |
| `emissions` | List[List[float]] | 发射概率矩阵 $B$ ($N \times M$) |
| `initial_probs` | List[float] | 初始概率向量 $\pi$ ($N$) |

### 8.2 主要方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `forward_algorithm(observations)` | (log_likelihood, alpha) | 计算似然和前向变量 |
| `viterbi(observations)` | (best_path, log_prob) | 解码最优状态序列 |
| `baum_welch(observations, max_iter, tol)` | None | EM 算法训练 |
| `sample(n_steps)` | (states, observations) | 生成样本序列 |

---

## 9. 数学符号汇总

| 符号 | 含义 |
|------|------|
| $N$ | 隐状态数量 |
| $M$ | 观测值数量 |
| $T$ | 观测序列长度 |
| $A = [a_{ij}]$ | 转移概率矩阵 |
| $B = [b_j(k)]$ | 发射概率矩阵 |
| $\pi = [\pi_i]$ | 初始概率向量 |
| $\alpha_t(i)$ | 前向变量 |
| $\beta_t(i)$ | 后向变量 |
| $\gamma_t(i)$ | 状态后验概率 |
| $\xi_t(i,j)$ | 状态对转移期望 |

---

## 参考资料

- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. Proceedings of the IEEE, 77(2), 257-286.
- Baum, L. E., & Petrie, T. (1966). Statistical inference for probabilistic functions of finite state Markov chains. The Annals of Mathematical Statistics, 37(6), 1554-1563.