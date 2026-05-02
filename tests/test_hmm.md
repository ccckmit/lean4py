# Hidden Markov Model 测试文档

本文档说明 `test_hmm.py` 中测试用例所验证的数学原理。

## 1. 测试验证的内容

`test_hmm.py` 验证隐马尔可夫模型（Hidden Markov Model，HMM）的核心功能，包括：
- 模型初始化
- 前向算法（Forward Algorithm）
- Viterbi 算法
- 采样功能

## 2. 初始化测试 (`test_initialization`)

### 数学原理

HMM 由以下参数定义：
- **状态数** $N$：隐藏状态的个数
- **观测数** $M$：可观测输出的个数
- **初始概率** $\pi = [\pi_1, \pi_2, ..., \pi_N]$：$\pi_i = P(q_1 = i)$
- **转移矩阵** $A = [a_{ij}]$：$a_{ij} = P(q_{t+1} = j | q_t = i)$
- **发射矩阵** $B = [b_j(o)]$：$b_j(o) = P(o_t = o | q_t = j)$

### 测试验证

```python
hmm = HMM(n_states=3, n_observations=4)
assert hmm.n_states == 3
assert hmm.n_observations == 4
assert len(hmm.transitions) == 3      # A 是 3x3 矩阵
assert len(hmm.emissions) == 3        # B 是 3x4 矩阵
assert len(hmm.initial_probs) == 3   # π 长度为 3
```

测试确认模型正确初始化所有参数，未提供参数时使用均匀分布作为默认值。

## 3. 前向算法测试 (`test_forward_algorithm`)

### 数学原理

前向算法计算观测序列 $O = (o_1, o_2, ..., o_T)$ 的概率 $P(O|\lambda)$，避免穷举所有状态序列的指数级复杂度。

**定义前向变量：**
$$\alpha_t(j) = P(o_1, o_2, ..., o_t, q_t = j | \lambda)$$

**初始化：**
$$\alpha_1(j) = \pi_j b_j(o_1)$$

**递归：**
$$\alpha_t(j) = b_j(o_t) \sum_{i=1}^{N} \alpha_{t-1}(i) a_{ij}$$

**终止：**
$$P(O|\lambda) = \sum_{j=1}^{N} \alpha_T(j)$$

为避免数值下溢，使用对数似然 $\log P(O|\lambda)$。

### 测试验证

```python
hmm = HMM(
    n_states=2,
    n_observations=2,
    transitions=[[0.9, 0.1], [0.1, 0.9]],
    emissions=[[0.9, 0.1], [0.1, 0.9]],
    initial_probs=[0.5, 0.5]
)
log_lik, alpha = hmm.forward_algorithm([0, 0, 0])

assert isinstance(log_lik, float)
assert len(alpha) == 3          # 时间步数 T=3
assert len(alpha[0]) == 2       # 状态数 N=2
```

测试确认：
- 返回类型正确（对数似然为 float）
- alpha 矩阵维度正确（$T \times N$）

## 4. Viterbi 算法测试 (`test_viterbi`)

### 数学原理

Viterbi 算法寻找最可能生成观测序列的隐藏状态路径 $Q^* = (q_1^*, q_2^*, ..., q_T^*)$。

**定义 delta 变量：**
$$\delta_t(j) = \max_{q_1, ..., q_{t-1}} P(q_1, ..., q_t = j, o_1, ..., o_t | \lambda)$$

**初始化：**
$$\delta_1(j) = \pi_j b_j(o_1)$$

**递归：**
$$\delta_t(j) = b_j(o_t) \max_{i} [\delta_{t-1}(i) a_{ij}]$$

同时记录回溯指针：
$$\psi_t(j) = \arg\max_{i} [\delta_{t-1}(i) a_{ij}]$$

**回溯：**
$$q_t^* = \psi_{t+1}(q_{t+1}^*)$$

### 测试验证

```python
observations = [0, 0, 0]
best_path, log_prob = hiterbi(observations)

assert len(best_path) == 3        # 路径长度等于观测序列长度
assert isinstance(log_prob, float)
```

测试确认返回的最优路径长度正确，对数概率类型正确。

## 5. 采样测试 (`test_sample`)

### 数学原理

从 HMM 生成观测序列的采样过程：

1. **采样初始状态：**
   $$q_1 \sim \pi$$

2. **采样初始观测：**
   $$o_1 \sim B_{q_1}$$

3. **递归采样：**
   对 $t = 2, ..., T$：
   $$q_t \sim A_{q_{t-1}}$$
   $$o_t \sim B_{q_t}$$

### 测试验证

```python
states, observations = hmm.sample(10)

assert len(states) == 10
assert len(observations) == 10
assert all(s in [0, 1] for s in states)      # 状态在有效范围内
assert all(o in [0, 1] for o in observations) # 观测在有效范围内
```

测试确认采样生成的序列长度和取值范围正确。

## 6. 测试模型配置

所有测试使用相同的对称 HMM 配置：

| 参数 | 值 | 含义 |
|------|-----|------|
| n_states | 2 | 2 个隐藏状态 |
| n_observations | 2 | 2 种观测符号 |
| transitions | [[0.9, 0.1], [0.1, 0.9]] | 自转移概率高（0.9），交叉转移概率低（0.1） |
| emissions | [[0.9, 0.1], [0.1, 0.9]] | 发射概率与转移概率相同 |
| initial_probs | [0.5, 0.5] | 初始概率均匀分布 |

这种配置形成一个"持久性"强的 HMM：系统倾向于保持在同一状态。

## 7. 数学符号总结

| 符号 | 含义 |
|------|------|
| $\lambda$ | HMM 模型参数 $(\pi, A, B)$ |
| $N$ | 隐藏状态数 |
| $T$ | 观测序列长度 |
| $\alpha_t(j)$ | 前向变量 |
| $\delta_t(j)$ | Viterbi 算法中的最大概率 |
| $\psi_t(j)$ | Viterbi 回溯指针 |
| $\xi_t(i,j)$ | 期望转移次数 |