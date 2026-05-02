# Markov Chains 测试文档

本文档说明 `test_markov_chains.py` 中测试用例的数学原理。

## 1. 测试验证概述

该测试文件验证马尔可夫链模块的核心功能，涵盖离散时间马尔可夫链（DTMC）、连续时间马尔可夫链（CTMC）、转移矩阵、平稳分布、细致平衡条件、吸收态、马尔可夫链蒙特卡洛（MCMC）、命中概率和混合时间等方面。

## 2. 转移矩阵测试 (Transition Matrix Tests)

### 2.1 行和为1的性质

```python
def test_row_sums_to_one(self):
    P = [[0.5, 0.5], [0.5, 0.5]]
    chain = DiscreteTimeMarkovChain(states, P)
    for row in chain.transition_matrix:
        assert abs(sum(row) - 1.0) < 1e-6
```

**数学原理**：转移矩阵 $P$ 的每一行表示从当前状态到所有可能状态的转移概率分布。根据概率公理，每行的和必须等于1：

$$\sum_{j} P_{ij} = 1, \quad \forall i$$

这是任何有效转移矩阵的基本约束条件。

### 2.2 矩阵有效性验证

```python
def test_invalid_matrix_raises(self):
    P = [[0.5, 0.5], [0.6, 0.3]]  # 行和为0.9和0.9，不是1.0
    with pytest.raises(ValueError):
        DiscreteTimeMarkovChain(states, P)
```

**数学原理**：非方阵或行和不为1的矩阵不是有效的转移矩阵。系统通过检查矩阵维度（$n \times n$）和行和约束（$\sum_j P_{ij} = 1$）来验证有效性。

### 2.3 从边构建转移矩阵

```python
def test_from_edges(self):
    edges = [("a", "b", 1.0), ("b", "a", 1.0)]
    P = TransitionMatrix.from_edges(states, edges)
```

**数学原理**：转移概率可以通过有向加权边定义。若从状态 $i$ 到 $j$ 的边权重为 $w_{ij}$，则：

$$P_{ij} = \frac{w_{ij}}{\sum_k w_{ik}}$$

`from_edges` 方法自动对每行的权重进行归一化。

## 3. 平稳分布测试 (Stationary Distribution Tests)

### 3.1 平稳分布定义

```python
def test_stationary_distribution(self):
    Q = [[-1.0, 1.0], [1.0, -1.0]]
    ctmc = ContinuousTimeMarkovChain(states, Q)
    pi = ctmc.stationary_distribution(max_iterations=100)
    assert abs(sum(pi) - 1.0) < 1e-3
```

**数学原理**：平稳分布 $\pi$ 满足以下条件：

**DTMC（离散时间）**：
$$\pi P = \pi, \quad \sum_i \pi_i = 1$$

**CTMC（连续时间）**：
$$\pi Q = 0, \quad \sum_i \pi_i = 1$$

其中 $Q$ 是生成元矩阵（generator matrix），满足每行和为0。

### 3.2 平稳分布验证

```python
def test_verify(self):
    P = [[1.0, 0.0], [0.0, 1.0]]
    sd = StationaryDistribution([1.0, 0.0], chain)
    assert sd.verify() is True
```

**数学原理**：`verify()` 方法检查 $\pi P = \pi$ 是否成立。对于单位矩阵（每个状态都是吸收态），任何在吸收态的概率分布都是平稳的。

### 3.3 细致平衡条件 (Detailed Balance)

```python
def test_holds(self):
    P = [[0.5, 0.5], [0.5, 0.5]]
    db = DetailedBalance(chain, [0.5, 0.5])
    assert db.holds() is True

def test_does_not_hold(self):
    P = [[0.9, 0.1], [0.3, 0.7]]
    db = DetailedBalance(chain, [0.5, 0.5])
    assert db.holds() is False
```

**数学原理**：细致平衡条件是平稳分布的更强形式。对于可逆马尔可夫链：

$$\pi_i P_{ij} = \pi_j P_{ji}, \quad \forall i, j$$

这意味着从状态 $i$ 到 $j$ 的净流为零。均匀分布 $\pi_i = 1/n$ 对于双随机矩阵（每列和也为1）总是满足细致平衡。

## 4. 马尔可夫性质测试 (Markov Property Tests)

### 4.1 转移概率

```python
def test_transition_prob(self):
    P = [[0.5, 0.5], [0.3, 0.7]]
    assert abs(chain.transition_prob(0, 0) - 0.5) < 1e-6
```

**数学原理**：转移概率 $P_{ij}$ 表示在当前状态为 $i$ 的条件下，下一步到达状态 $j$ 的概率。马尔可夫性质表明这一概率仅取决于当前状态，而与历史路径无关。

### 4.2 不可约性 (Irreducibility)

```python
def test_is_irreducible(self):
    P = [[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]
    assert chain.is_irreducible() is True

def test_is_not_irreducible(self):
    P = [[1.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.0, 0.5, 0.5]]
    assert chain.is_irreducible() is False
```

**数学原理**：不可约性表示从任意状态都可以（以正概率）在有限步内到达任意其他状态。数学定义：存在 $n > 0$ 使得对所有 $i, j$，$(P^n)_{ij} > 0$。

对于转移矩阵：
- 第一个矩阵形成一个强连通图，所有状态互通
- 第二个矩阵中状态0是吸收态，其他状态无法到达状态0

### 4.3 周期性与非周期性

```python
def test_is_aperiodic(self):
    P = [[0.5, 0.5], [0.5, 0.5]]
    assert chain.is_aperiodic() is True
```

**数学原理**：状态 $i$ 的周期定义为：
$$d(i) = \gcd\{n \geq 1 : (P^n)_{ii} > 0\}$$

若 $d(i) = 1$，则状态 $i$ 是非周期的。均匀转移矩阵（所有条目非零）保证非周期性。

### 4.4 通讯类 (Communicating Classes)

```python
def test_communicating_classes(self):
    P = [[1.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.0, 0.5, 0.5]]
    classes = chain.communicating_classes()
```

**数学原理**：状态 $i$ 和 $j$ 互通（$i \leftrightarrow j$）当且仅当存在 $n, m > 0$ 使得 $(P^n)_{ij} > 0$ 且 $(P^m)_{ji} > 0$。互通关系是等价关系，将状态空间划分为若干通讯类。

## 5. Chapman-Kolmogorov 测试

### 5.1 n步转移概率

```python
def test_n_step_prob(self):
    P = [[1.0, 0.0], [0.0, 1.0]]
    assert abs(chain.n_step_prob(2, 0, 0) - 1.0) < 1e-6
```

**数学原理**：Chapman-Kolmogorov 方程描述了多步转移概率：
$$(P^{n+m})_{ij} = \sum_{k} (P^n)_{ik} \cdot (P^m)_{kj}$$

对于单位矩阵（恒等链），$P^n = I$ 对所有 $n$ 成立，因此从状态0经过任意步仍停留在状态0。

### 5.2 连续时间马尔可夫链的生成元

```python
def test_rows_sum_to_zero(self):
    Q = [[-1.0, 1.0], [1.0, -1.0]]
    for row in ctmc.generator_matrix:
        assert abs(sum(row)) < 1e-6
```

**数学原理**：连续时间马尔可夫链的生成元矩阵 $Q$ 满足：
$$q_{ij} = \begin{cases}
\lambda_{ij} & i \neq j \text{（从 } i \text{ 到 } j \text{ 的转移率）} \\
-\lambda_i & i = j \text{（状态 } i \text{ 的总离开率）}
\end{cases}$$

每行和为零：$\sum_j q_{ij} = 0$。

### 5.3 转移率与总率

```python
def test_rate(self):
    Q = [[-1.0, 1.0], [1.0, -1.0]]
    assert abs(ctmc.rate(0, 1) - 1.0) < 1e-6

def test_total_rate(self):
    Q = [[-1.0, 1.0], [1.0, -1.0]]
    assert abs(ctmc.total_rate(0) - 1.0) < 1e-6
```

**数学原理**：
- 转移率 $q_{ij}$（$i \neq j$）表示从状态 $i$ 到 $j$ 的瞬时转移率
- 总率 $\lambda_i = -\qii$ 是状态 $i$ 的总离开率

对于两状态 CTMC，从状态0到1的转移率为1，总离开率也是1。

## 6. 吸收态与基本矩阵

### 6.1 吸收态识别

```python
def test_absorbing_states(self):
    P = [[1.0, 0.0, 0.0], [0.3, 0.4, 0.3], [0.0, 0.0, 1.0]]
    absorbing = ab.absorbing_states()
    assert 0 in absorbing
    assert 2 in absorbing
```

**数学原理**：状态 $i$ 是吸收态当且仅当 $P_{ii} = 1$。一旦进入吸收态，系统永远无法离开。在给定示例中，状态0和2是吸收态（对角线元素为1）。

### 6.2 基本矩阵

```python
def test_fundamental_matrix(self):
    P = [[1.0, 0.0], [0.5, 0.5]]
    N = ab.fundamental_matrix()
```

**数学原理**：对于包含吸收态的链，将其重排为 $(I, 0; R, Q)$ 形式，其中 $Q$ 是瞬态子矩阵。基本矩阵定义为：
$$N = (I - Q)^{-1} = I + Q + Q^2 + \cdots$$

$N_{ij}$ 表示从瞬态 $i$ 出发被吸收前的预期访问次数。

## 7. 马尔可夫链蒙特卡洛测试

### 7.1 Metropolis-Hastings 算法

```python
def test_metropolis_hastings(self):
    samples = mcmc.metropolis_hastings(proposal, 1.0, num_samples=10)
    assert len(samples) == 11  # 初始样本 + 10个采样
```

**数学原理**：Metropolis-Hastings 算法通过以下步骤从目标分布 $\pi(x)$ 采样：
1. 从提议分布 $q(x'|x)$ 采样 $x'$
2. 计算接受率 $\alpha = \min\left(1, \frac{\pi(x')q(x|x')}{\pi(x)q(x'|x)}\right)$
3. 以概率 $\alpha$ 接受 $x'$，否则保留 $x$

### 7.2 Gibbs 采样

```python
def test_gibbs_sampling(self):
    samples = mcmc.gibbs_sampling(1.0, num_samples=10)
```

**数学原理**：Gibbs 采样是 Metropolis-Hastings 的特例，提议分布为条件分布：
$$q(x'|x) = \pi(x'_i | x_{-i})$$

对于满条件分布已知的模型，Gibbs 采样是更高效的采样方法。

## 8. 命中概率与混合时间

### 8.1 命中概率

```python
def test_compute_hitting(self):
    h = hp.compute_hitting(0)
    assert h[0] == 1.0
```

**数学原理**：命中概率 $h_i$ 表示从状态 $i$ 出发最终命中目标状态 $A$ 的概率。满足：
$$h_i = \sum_j P_{ij} h_j, \quad i \notin A$$
$$h_i = 1, \quad i \in A$$

对于均匀双状态链，从任何状态出发命中状态0的概率为1（因为链是对称的）。

### 8.2 预期命中时间

```python
def test_expected_hitting_time(self):
    tau = hp.expected_hitting_time(0)
```

**数学原理**：预期命中时间 $\tau_i$ 满足：
$$\tau_i = 1 + \sum_j P_{ij} \tau_j, \quad i \notin A$$
$$\tau_i = 0, \quad i \in A$$

### 8.3 总变差距离

```python
def test_total_variation_distance(self):
    dist = mt.total_variation_distance(0, 0)
    assert dist >= 0.0
```

**数学原理**：总变差距离定义为：
$$d(t) = \frac{1}{2} \sum_i |P_{ij}^{(t)} - \pi_j|$$

这衡量了 $t$ 步后的分布与平稳分布的接近程度。

### 8.4 混合时间

```python
def test_mixing_time(self):
    tau = mt.mixing_time(0.25)
    assert isinstance(tau, int)
```

**数学原理**：$\epsilon$-混合时间定义为首次满足 $d(t) \leq \epsilon$ 的最小时间：
$$\tau(\epsilon) = \min\{t : d(t) \leq \epsilon\}$$

对于均匀链，混合时间与谱隙（spectral gap）$1 - \lambda_2$ 相关。

## 9. 测试类结构总结

| 测试类 | 测试内容 | 关键数学概念 |
|--------|----------|--------------|
| `TestDiscreteTimeMarkovChain` | 离散时间链基本性质 | 转移矩阵、行和约束、不可约性 |
| `TestContinuousTimeMarkovChain` | 连续时间链基本性质 | 生成元矩阵、转移率、平稳分布 |
| `TestTransitionMatrix` | 转移矩阵构建 | 边权重归一化 |
| `TestStationaryDistribution` | 平稳分布验证 | $\pi P = \pi$、$\pi Q = 0$ |
| `TestDetailedBalance` | 细致平衡条件 | 可逆性、细致流平衡 |
| `TestAbsorbingStates` | 吸收态分析 | 基本矩阵 $N = (I-Q)^{-1}$ |
| `TestMarkovChainMonteCarlo` | MCMC 采样方法 | Metropolis-Hastings、Gibbs |
| `TestHittingProbability` | 命中分析 | 命中概率方程、预期时间 |
| `TestMixingTime` | 收敛速度 | 总变差距离、混合时间界 |

## 10. 参考数学公式

### 核心方程

**Chapman-Kolmogorov**：
$$P^{(n+m)} = P^{(n)} \cdot P^{(m)}$$

**平稳分布**：
$$\pi = \pi P \quad \text{或} \quad \pi Q = 0$$

**细致平衡**：
$$\pi_i P_{ij} = \pi_j P_{ji}$$

**混合时间**：
$$\tau(\epsilon) = \min\{t : \|P^t - \pi\|_{TV} \leq \epsilon\}$$