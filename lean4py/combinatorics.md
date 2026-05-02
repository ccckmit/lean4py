# 组合数学 (Combinatorics) 模块

本模块实现了组合数学的基本概念与算法，灵感来源于 mathlib4 的 Mathlib.Combinatorics。

---

## 1. 计数原理 (Counting Principles)

### 1.1 加法原理 (Sum Rule)

若完成一件事有 **m** 种方式，完成另一件事有 **n** 种方式，且这些方式不重叠，则完成这件事共有 **m + n** 种方式。

**示例**：从 `{1,2,3}` 中选奇数或选质数 → 奇数有 `{1,3}`（2种），质数有 `{2,3}`（2种），但 `{3}` 重复，故共有 2 + 2 - 1 = 3 种。

### 1.2 乘法原理 (Product Rule)

若完成一件事需要 **m** 种选择，完成另一件事需要 **n** 种选择，则完成两件事共有 **m × n** 种方式。

**示例**：密码由 3 位数字组成，每位 0-9 → 10³ = 1000 种。

### 1.3 鸽巢原理 (Pigeonhole Principle)

> 若 n+1 个物品放入 n 个容器，则至少有一个容器装有 ≥2 个物品。

**实现**：`PigeonholePrinciple.finite_pigeonhole()`

```python
PigeonholePrinciple.finite_pigeonhole(['a','b','c','d'], 3)
# 返回分配映射，若 |items| ≤ containers 则返回 None
```

**广义鸽巢原理**：若 |items| > containers × capacity，则某容器有 > capacity 个物品。

---

## 2. 排列 (Permutations)

### 2.1 定义

从 n 个不同元素中取出 r 个按顺序排列的方案数：

$$P(n,r) = \frac{n!}{(n-r)!} = n \times (n-1) \times \cdots \times (n-r+1)$$

### 2.2 Python 实现

```python
import math
def permutation(n: int, r: int) -> int:
    """P(n,r) = n! / (n-r)!"""
    return math.perm(n, r)
```

---

## 3. 组合 (Combinations)

### 3.1 定义

从 n 个不同元素中取出 r 个（不考虑顺序）的方案数：

$$C(n,r) = \binom{n}{r} = \frac{n!}{r!(n-r)!}$$

**性质**：
- $\binom{n}{r} = \binom{n}{n-r}$
- $\binom{n}{0} = \binom{n}{n} = 1$

### 3.2 实现

```python
math.comb(n, r)  # Python 内置
BinomialCoefficient.binom(n, r)  # 模块实现
```

---

## 4. 二项式系数与帕斯卡三角形

### 4.1 帕斯卡三角形

```
       1
      1 1
     1 2 1
    1 3 3 1
   1 4 6 4 1
```

每行满足：$\binom{n}{k} + \binom{n}{k+1} = \binom{n+1}{k+1}$

### 4.2 二项式定理

$$(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k}$$

**验证**：`BinomialCoefficient.binomial_theorem()`

### 4.3 范德蒙德恒等式 (Vandermonde's Identity)

$$\sum_{k=0}^{r} \binom{m}{k} \binom{n}{r-k} = \binom{m+n}{r}$$

**验证**：`BinomialCoefficient.vandermonde()`

---

## 5. 星星与杠条 (Stars and Bars)

### 5.1 问题描述

将 n 个不可区分的球放入 k 个可区分的盒子中，允许盒子为空。

**公式**：$\binom{n+k-1}{k-1} = \binom{n+k-1}{n}$

### 5.2 推导

n 个球用 n-1 个杠分隔，k 个盒子需要 k+1 个杠，但首尾杠可省略 → 共 n+k-1 个位置放置杠。

```python
from math import comb
def stars_and_bars(n: int, k: int) -> int:
    """将 n 个球放入 k 个盒子"""
    return comb(n + k - 1, n)
```

---

## 6. 容斥原理 (Inclusion-Exclusion Principle)

### 6.1 两集合情形

$$|A \cup B| = |A| + |B| - |A \cap B|$$

### 6.2 三集合情形

$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

### 6.3 一般形式

$$|A_1 \cup \cdots \cup A_n| = \sum |A_i| - \sum |A_i \cap A_j| + \sum |A_i \cap A_j \cap A_k| - \cdots$$

---

## 7. 生成函数 (Generating Functions)

### 7.1 普通生成函数

序列 $\{a_n\}$ 的生成函数为 $A(x) = \sum_{n=0}^{\infty} a_n x^n$

**示例**：二项式系数序列 $\{\binom{n}{k}\}$ 的生成函数为 $(1+x)^n$。

### 7.2 指数生成函数

序列 $\{a_n\}$ 的指数生成函数为 $A(x) = \sum_{n=0}^{\infty} a_n \frac{x^n}{n!}$

### 7.3 组合应用

生成函数可用于求解递推关系、计数问题。

---

## 8. 划分数 (Partition Numbers)

### 8.1 定义

整数 n 的划分数 p(n) 表示将 n 写成正整数之和的方式数（不考虑顺序）。

### 8.2 示例

- p(4) = 5：4, 3+1, 2+2, 2+1+1, 1+1+1+1

### 8.3 贝尔数 (Bell Numbers)

集合 {1,...,n} 的划分数：

$$B_0 = 1, \quad B_{n+1} = \sum_{k=0}^{n} \binom{n}{k} B_k$$

**实现**：`BellNumber.bell()`

```python
BellNumber.bell(4)  # 返回 15
```

---

## 9. 卡特兰数 (Catalan Numbers)

### 9.1 定义

$$C_n = \frac{1}{n+1} \binom{2n}{n} = \frac{(2n)!}{(n+1)! \, n!}$$

**递推关系**：$C_{n+1} = \frac{2(2n+1)}{n+2} C_n$

### 9.2 实现

```python
CatalanNumber.catalan(4)  # 返回 14
```

### 9.3 应用

- 有效括号的正确匹配数
- 二叉搜索树的形状数
- 凸多边形的三角剖分数

**Dyck 字**检验：

```python
DyckWord.is_dyck('()()')   # True
DyckWord.is_dyck(')()(')   # False
```

---

## 10. 其他重要定理

### 10.1 斯珀纳定理 (Sperner's Theorem)

在集合 `[n]` 的幂集 $2^{[n]}$ 中，反链的最大大小为 $\binom{n}{\lfloor n/2 \rfloor}$。

```python
SpernerTheorem.max_antichain_size(4)  # 返回 6
```

**反链 (Antichain)**：集合族中任意两个集合互不包含。

**验证**：`SetFamily.is_antichain()`

### 10.2 霍尔婚姻定理 (Hall's Marriage Theorem)

设二分图左侧顶点集为 brides，右侧邻域集合为 bridesides。若对任意子集 $S$，$|\cup_{i \in S} N(i)| \geq |S|$，则存在完美匹配。

```python
HallMarriage.hall_condition([{0,1}, {1,2}])  # True
```

---

## 模块类结构

| 类 | 功能 |
|---|---|
| `PigeonholePrinciple` | 鸽巢原理（有限、强、无穷版本） |
| `CatalanNumber` | 卡特兰数计算 |
| `BellNumber` | 贝尔数计算 |
| `DyckWord` | Dyck 字检验与生成 |
| `SetFamily` | 集合族的性质检验 |
| `SpernerTheorem` | 斯珀纳定理 |
| `HallMarriage` | 霍尔婚姻定理 |
| `BinomialCoefficient` | 二项式系数及相关恒等式 |

---

## 参考

- Graham, Knuth, Patashnik: *Concrete Mathematics*
- Stanley: *Enumerative Combinatorics*
- mathlib4: `Mathlib.Combinatorics`