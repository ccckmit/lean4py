# Markov Chains 马尔可夫链

本模块提供离散时间和连续时间马尔可夫链的理论支持，包括转移矩阵、n 步转移概率、平稳分布、细致平衡条件等核心概念。

## 1. 马尔可夫性质 (Markov Property)

马尔可夫性质是马尔可夫链的核心假设：**未来的状态只依赖于当前状态，与过去的历史无关**。

数学表述：对于任意 n ≥ 0 和任意状态 i₀, i₁, ..., iₙ₊₁，

```
P(X_{n+1} = i_{n+1} | X_0 = i_0, X_1 = i_1, ..., X_n = i_n) = P(X_{n+1} = i_{n+1} | X_n = i_n)
```

马尔可夫链的代码实现见 `DiscreteTimeMarkovChain` 类（第 13-119 行），其转移概率由转移矩阵 P 定义。

## 2. 状态空间 S 与转移概率矩阵 P

**状态空间 S** 是马尔可夫链所有可能状态的集合。在有限状态空间中，设 |S| = n，则状态可以编号为 {0, 1, 2, ..., n-1}。

**转移概率矩阵 P** 是一个 n×n 的矩阵，其中元素 P_{ij} 表示从状态 i 转移到状态 j 的一步转移概率：

```
P_{ij} = P(X_{n+1} = j | X_n = i)
```

矩阵的每一行之和必须等于 1（`DiscreteTimeMarkovChain._validate`，第 25-30 行）：

```
∑_{j∈S} P_{ij} = 1,  ∀i ∈ S
```

## 3. Chapman-Kolmogorov 方程

Chapman-Kolmogorov 方程描述了多步转移概率与单步转移概率之间的关系：

```
P^{(n+m)} = P^{(n)} · P^{(m)}
```

即从状态 i 到状态 j 的 (n+m) 步转移概率，等于所有中间状态 k 的 n 步转移概率与 m 步转移概率的乘积之和：

```
P^{(n+m)}_{ij} = ∑_{k∈S} P^{(n)}_{ik} · P^{(m)}_{kj}
```

本模块通过 `_matrix_power` 方法（第 41-50 行）计算矩阵的 n 次幂来得到 n 步转移概率。

## 4. n 步转移概率

n 步转移概率 P^{(n)}_{ij} 表示从状态 i 出发，经过 n 步之后到达状态 j 的概率：

```
P^{(n)}_{ij} = P(X_n = j | X_0 = i)
```

计算方法为矩阵幂运算：`P^{(n)} = P^n`（`n_step_prob` 方法，第 36-39 行）。

## 5. 平稳分布 π (Stationary Distribution)

平稳分布 π 是一个概率分布，满足：

```
π = πP  （左特征向量，特征值为 1）
∑_{i∈S} π_i = 1
```

这意味着如果链在时刻 0 服从平稳分布，则在任意时刻 n 都服从相同的分布。

`StationaryDistribution` 类（第 187-211 行）实现了平稳分布的验证，通过 `verify` 方法检查 πP = π 是否成立。

## 6. 平稳分布的存在性与唯一性

对于有限状态的马尔可夫链，平稳分布的存在性和唯一性条件为：

**存在性**：链至少有一个平稳分布（对于有限链总是成立）

**唯一性**：如果链是**不可约的（irreducible）**，则平稳分布唯一

`is_irreducible` 方法（第 61-67 行）通过可达性检查来判断链是否不可约：所有状态都相互可达，即对于任意 i, j ∈ S，存在 n ≥ 0 使得 P^{(n)}_{ij} > 0。

`communicating_classes` 方法（第 85-94 行）用于找到所有的互通类。

## 7. 细致平衡条件 (Detailed Balance Condition)

细致平衡条件是平稳分布的一个更强条件：

```
π_i P_{ij} = π_j P_{ji},  ∀i, j ∈ S
```

如果一条链满足细致平衡条件，则称其为**可逆的（reversible）**。

`DetailedBalance` 类（第 214-229 行）实现了这一条件的检验（`holds` 方法）。

## 8. 不可约与非周期链

**不可约（Irreducible）**：所有状态互通（见第 6 节）

**非周期（Aperiodic）**：状态的返回时间的最大公约数为 1。周期性的定义：

```
period(i) = gcd{n ≥ 1 : P^{(n)}_{ii} > 0}
```

如果所有状态的周期为 1，则链是非周期的。

`is_aperiodic` 方法（第 117-119 行）当前返回 True（占位实现）。

## 9. 遍历定理 (Ergodic Theorem)

对于**不可约且非周期的**马尔可夫链，遍历定理成立：

```
lim_{n→∞} P(X_n = i) = π_i,  ∀i ∈ S
```

即无论初始状态如何，经过足够长的运行后，链在任意状态 i 的概率收敛到平稳分布 π_i。

`MixingTime` 类（第 296-317 行）通过总变差距离来量化收敛速度：

```
d(n) = (1/2) ∑_{j} |P^{(n)}_{ij} - π_j|
```

## 10. 击中概率与期望击中时间

**击中概率** h_i 表示从状态 i 出发，最终到达目标状态的概率：

```
h_i = P_i(τ_target < ∞)
```

`HittingProbability` 类（第 279-293 行）提供了计算方法（`compute_hitting`）。

**期望击中时间** E_i[τ_target] 表示从状态 i 出发到达目标状态的平均步数：

```
E_i[τ_target] = E_i[min{n ≥ 0 : X_n = target}]
```

`expected_hitting_time` 方法（第 291-293 行）返回期望击中时间向量。

**吸收态**：满足 P_{ii} = 1 的状态，一旦进入则永远停留。`AbsorbingStates` 类（第 232-248 行）用于识别吸收态。

## 11. 连续时间马尔可夫链（简介）

连续时间马尔可夫链由**生成元矩阵 Q**（infinitesimal generator）刻画：

```
Q_{ij} = λ_{ij},  i ≠ j  （从 i 到 j 的转移率）
Q_{ii} = -λ_i     （λ_i = ∑_{j≠i} λ_{ij}，总离开率）
```

每行的和为 0（`ContinuousTimeMarkovChain._validate`，第 134-139 行）。

`rate` 方法（第 141-143 行）获取转移率 λ_{ij}，而 `total_rate` 方法（第 145-147 行）计算总离开率 λ_i。

连续时间链的平稳分布 π 满足：

```
πQ = 0,  Σπ_i = 1
```

`stationary_distribution` 方法（第 149-163 行）通过迭代法求解此方程。

## 主要类与对应关系

| 类名 | 行号 | 功能 |
|------|------|------|
| `DiscreteTimeMarkovChain` | 13-119 | 离散时间马尔可夫链 |
| `ContinuousTimeMarkovChain` | 122-163 | 连续时间马尔可夫链 |
| `TransitionMatrix` | 166-184 | 转移矩阵构造 |
| `StationaryDistribution` | 187-211 | 平稳分布 |
| `DetailedBalance` | 214-229 | 细致平衡检验 |
| `AbsorbingStates` | 232-248 | 吸收态与基础矩阵 |
| `MarkovChainMonteCarlo` | 251-276 | MCMC 方法（Metropolis-Hastings, Gibbs） |
| `HittingProbability` | 279-293 | 击中概率与击中时间 |
| `MixingTime` | 296-317 | 混合时间 |

## 使用示例

```python
from lean4py.markov_chains import DiscreteTimeMarkovChain, StationaryDistribution

states = {'0', '1', '2'}
P = [
    [0.5, 0.3, 0.2],
    [0.2, 0.5, 0.3],
    [0.3, 0.2, 0.5]
]
chain = DiscreteTimeMarkovChain(states, P)

# n步转移概率
p_2_0 = chain.n_step_prob(2, 2, 0)

# 检验平稳分布
pi = [1/3, 1/3, 1/3]
stationary = StationaryDistribution(pi, chain)
assert stationary.verify()
```