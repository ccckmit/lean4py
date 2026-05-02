# 信息论测试文档 (test_information_theory.py)

本文件测试 lean4py 信息论模块的核心功能，基于 mathlib4 的 `Mathlib.ProbabilityTheory.InformationTheory` 设计。

---

## 1. 测试概述

信息论由克劳德·香农（Claude Shannon）于 1948 年创立，主要研究信息的量化、存储和通信。本测试验证以下核心概念：

| 函数 | 功能 |
|------|------|
| `entropy(p)` | 香农熵 H(X) |
| `mutual_information(joint, x_marginal, y_marginal)` | 互信息 I(X;Y) |
| `kl_divergence(P, Q)` | KL 散度 D(P\|\|Q) |

---

## 2. 熵 (Entropy) 测试

### 2.1 数学原理

**香农熵** 衡量随机变量的不确定性，定义为：

$$H(X) = -\sum_{i} p_i \log_2 p_i$$

- 使用以 2 为底的对数，单位为 **比特 (bits)**
- 当所有事件概率相等时（均匀分布），熵最大
- 当某一事件概率为 1 时，熵为 0

### 2.2 测试用例

| 测试 | 分布 | 期望结果 |
|------|------|----------|
| `test_entropy_uniform` | p = [0.25, 0.25, 0.25, 0.25] | H = log₂(4) = 2 bits |
| `test_entropy_certain` | p = [1.0, 0.0, 0.0] | H = 0 (确定事件) |
| `test_entropy_empty` | p = [] | H = 0 |
| `test_entropy_not_normalized` | p = [1, 1, 1, 1] | 自动归一化后 H = 2 bits |
| `test_entropy_bernoulli` | p = 0.3 | H = -0.3log₂(0.3) - 0.7log₂(0.7) |

### 2.3 均匀分布的物理意义

```python
p = [0.25, 0.25, 0.25, 0.25]  # 4 个等概率事件
H = log₂(4) = 2 bits
```

表示需要 **2 比特** 来编码 4 个等概率事件，这正是香农源编码定理的直接体现。

---

## 3. 互信息 (Mutual Information) 测试

### 3.1 数学原理

**互信息** 衡量两个随机变量之间的依赖程度：

$$I(X;Y) = H(X) + H(Y) - H(X,Y)$$

其中：
- H(X), H(Y) 是边缘熵
- H(X,Y) 是联合熵

互信息也可以表示为：

$$I(X;Y) = \sum_{x,y} p(x,y) \log_2 \frac{p(x,y)}{p(x)p(y)}$$

**性质：**
- I(X;Y) ≥ 0 （非负性）
- I(X;Y) = 0 当且仅当 X 和 Y 独立
- I(X;Y) = H(X) = H(Y) 当 X 和 Y 完全相关

### 3.2 测试用例

| 测试 | 联合分布 | x 边缘 | y 边缘 | 期望结果 |
|------|----------|--------|--------|----------|
| `test_mi_independent` | [[0.25,0.25],[0.25,0.25]] | [0.5,0.5] | [0.5,0.5] | I ≈ 0 |
| `test_mi_dependent` | [[0.5,0.0],[0.0,0.5]] | [0.5,0.5] | [0.5,0.5] | I ≈ 1 bit |
| `test_mi_empty` | [] | [] | [] | I = 0 |

### 3.3 独立 vs 完全相关

**独立情况：**
```python
joint = [[0.25, 0.25],   # p(X=0,Y=0)=0.25, p(X=0,Y=1)=0.25
         [0.25, 0.25]]   # p(X=1,Y=0)=0.25, p(X=1,Y=1)=0.25
# p(X=0) = 0.5, p(X=1) = 0.5
# p(Y=0) = 0.5, p(Y=1) = 0.5
# 联合分布 = 边缘分布的乘积 → 独立 → I = 0
```

**完全相关情况：**
```python
joint = [[0.5, 0.0],    # X=0 时 Y 必为 0
         [0.0, 0.5]]    # X=1 时 Y 必为 1
# H(X) = 1 bit, H(Y) = 1 bit, H(X,Y) = 1 bit
# I = 1 + 1 - 1 = 1 bit
```

---

## 4. KL 散度 (KL Divergence) 测试

### 4.1 数学原理

**KL 散度** 衡量两个概率分布的差异：

$$D_{KL}(P \| Q) = \sum_{i} p_i \log_2 \frac{p_i}{q_i}$$

**性质：**
- D(P||Q) ≥ 0（非负性）
- D(P||Q) = 0 当且仅当 P = Q
- **不对称性**：D(P||Q) ≠ D(Q||P)
- **当 q_i = 0 且 p_i > 0 时**：D = ∞

### 4.2 测试用例

| 测试 | P | Q | 期望结果 |
|------|---|---|----------|
| `test_kl_identical` | [0.5, 0.3, 0.2] | [0.5, 0.3, 0.2] | D = 0 |
| `test_kl_different` | [0.5, 0.5] | [0.7, 0.3] | D > 0 |
| `test_kl_mismatch_length` | [0.5, 0.5] | [0.5] | 抛出 ValueError |
| `test_kl_q_zero` | [1.0, 0.0] | [0.0, 1.0] | D = ∞ |

### 4.3 零概率处理

```python
p = [1.0, 0.0]  # P(X=0)=1, P(X=1)=0
q = [0.0, 1.0]  # Q(X=0)=0, Q(X=1)=1

# D(P||Q) = 1·log₂(1/0) + 0·log₂(0/1) = ∞
kl_divergence(p, q)  # 返回 float('inf')
```

**注意**：KL 散度只对 p_i > 0 的项求和，p_i = 0 的项贡献为 0。

---

## 5. 信道容量 (Channel Capacity) 测试

### 5.1 数学原理

**信道容量** 定义为：

$$C = \max_{p(x)} I(X;Y)$$

表示在给定信道条件下，可靠传输信息的最大速率。

**香农信道编码定理**：
- 当传输速率 R < C 时，存在编码方案使错误概率任意小
- 当 R > C 时，任何编码方案都无法可靠传输

### 5.2 实现说明

lean4py 的 `ChannelCapacity.compute(channel)` 方法返回简化值 1.0，用于验证：
- `is_achievable(rate, capacity)` 检查 rate < capacity

---

## 6. 测试实现细节

### 6.1 熵的计算

```python
def entropy(probabilities: List[float]) -> float:
    # 自动归一化
    total = sum(probabilities)
    if abs(total - 1.0) > 1e-10:
        probabilities = [p / total for p in probabilities]
    # 使用以 2 为底的对数
    return -sum(p * math.log2(p) for p in probabilities if p > 0)
```

### 6.2 互信息的计算

```python
def mutual_information(joint, x_marginal, y_marginal) -> float:
    H_X = -sum(p * math.log2(p) for p in x_marginal if p > 0)
    H_Y = -sum(p * math.log2(p) for p in y_marginal if p > 0)
    H_XY = sum(p * math.log2(p) for row in joint for p in row if p > 0)
    return H_X + H_Y - H_XY
```

### 6.3 KL 散度的计算

```python
def kl_divergence(P: List[float], Q: List[float]) -> float:
    return sum(p * math.log2(p / q) if q > 0 else float('inf')
               for p, q in zip(P, Q) if p > 0)
```

---

## 7. 与 mathlib4 的对应关系

本模块模仿 `mathlib4` 的 `Mathlib.ProbabilityTheory.InformationTheory`：

| lean4py | mathlib4 |
|---------|----------|
| `entropy(p)` | `Entropy.ofDistribution` |
| `mutual_information(joint, x, y)` | `MutualInformation.mk` |
| `kl_divergence(P, Q)` | `KullbackLeibler.div` |

---

## 8. 运行测试

```bash
pytest tests/test_information_theory.py -v
```