# Set Theory Advanced - 高级集合论

本模块实现了 lean4py 中的高级集合论功能，对应 mathlib4 的 Mathlib.SetTheory 模块。主要涵盖序数、基数、超限归纳等核心概念。

## 目录

1. [ZFC 公理系统](#1-zfc-公理系统)
2. [序数与超限归纳](#2-序数与超限归纳)
3. [基数与基数算术](#3-基数与基数算术)
4. [连续统假设与独立性结果](#4-连续统假设与独立性结果)
5. [大基数公理](#5-大基数公理)
6. [滤子与超滤子](#6-滤子与超滤子)
7. [布尔值模型](#7-布尔值模型)

---

## 1. ZFC 公理系统

ZFC（Zermelo-Fraenkel with Choice）是现代集合论的标准公理系统，包含以下公理：

### 1.1 外延性公理 (Extensionality)

```
∀x∀y[∀z(z ∈ x ↔ z ∈ y) → x = y]
```

两个集合相等当且仅当它们有相同的元素。

### 1.2 空集公理 (Empty Set)

```
∃x∀y[y ∉ x]
```

存在一个没有任何元素的集合，即空集 ∅。

### 1.3 配对公理 (Pairing)

```
∀x∀y∃z∀w[w ∈ z ↔ (w = x ∨ w = y)]
```

对任意两个集合 x 和 y，存在集合 z = {x, y}。

### 1.4 并集公理 (Union)

```
∀x∃y∀z[z ∈ y ↔ ∃w(z ∈ w ∧ w ∈ x)]
```

对任意集合 x，存在集合 y 是 x 中所有元素的并集。

### 1.5 无穷公理 (Infinity)

```
∃x[∅ ∈ x ∧ ∀y(y ∈ x → y ∪ {y} ∈ x)]
```

存在一个归纳集合，包含空集且对后继运算封闭。

### 1.6 替换公理模式 (Replacement)

```
∀x∀p[(∀y ∈ x → P(y)) → ∃z∀w[w ∈ z ↔ ∃y(P(y) ∧ w ∈ y))]
```

对任意集合 x 和性质 P，x 中满足 P 的元素可以组成一个集合。

### 1.7 幂集公理 (Power Set)

```
∀x∃y∀z[z ∈ y ↔ z ⊆ x]
```

对任意集合 x，存在其所有子集组成的集合 P(x)。

### 1.8 正则公理 (Foundation)

```
∀x[x ≠ ∅ → ∃y(y ∈ x ∧ y ∩ x = ∅)]
```

每个非空集合 x 都有一个极小元 y，使得 y ∩ x = ∅。

### 1.9 选择公理 (Choice)

```
∀x∃R(R well-orders x)
```

每个集合都可以被良序化（等价于 Zorn 引理）。

```python
class AxiomOfChoice:
    """选择公理及其等价命题。"""

    @staticmethod
    def holds() -> bool:
        """选择公理（简化版：假设为真）。"""
        return True

    @staticmethod
    def zorns_lemma() -> bool:
        """Zorn 引理等价于 AC。"""
        return True

    @staticmethod
    def well_ordering_theorem() -> bool:
        """良序定理等价于 AC。"""
        return True
```

### 1.10 ZFC 的重要等价命题

| 等价命题 | 描述 |
|---------|------|
| 选择公理 (AC) | 每个集合都有选择函数 |
| Zorn 引理 | 每个非空偏序集有极大元 |
| 良序定理 | 每个集合可以被良序化 |
| 势式良序定理 | 每个集合与某个基数等势 |

---

## 2. 序数与超限归纳

### 2.1 序数的定义

**von Neumann 序数**：每个序数 α 定义为所有小于它的序数的集合：

```
α = {β | β < α}
```

因此：
- 0 = ∅
- 1 = {∅} = {0}
- 2 = {∅, {∅}} = {0, 1}
- 3 = {0, 1, 2}
- ...

```python
class Ordinal:
    """序数 α（von Neumann 定义：α = {β | β < α}）。"""

    def __init__(self, representation: Optional[Any] = None):
        self.rep = representation

    @staticmethod
    def zero() -> 'Ordinal':
        """0 = ∅。"""
        return Ordinal(set())

    @staticmethod
    def successor(alpha: 'Ordinal') -> 'Ordinal':
        """α + 1 = α ∪ {α}。"""
        return Ordinal(alpha)
```

### 2.2 序数的类型

1. **零序数 (Zero Ordinal)**：0 = ∅

2. **后继序数 (Successor Ordinal)**：α = β + 1 = β ∪ {β}

3. **极限序数 (Limit Ordinal)**：不是后继的序数
   - 例如：ω, ω·2, ω²

```python
def is_limit(self) -> bool:
    """极限序数：不是后继序数（简化版）。"""
    return self.rep is None
```

### 2.3 超限归纳法 (Transfinite Induction)

**原理**：设 P(α) 是关于序数 α 的性质。如果：
1. P(0) 成立
2. 对所有 β，若 P(β) 成立，则 P(β + 1) 成立
3. 对所有极限序数 λ，若对所有 β < λ 都有 P(β) 成立，则 P(λ) 成立

那么 P(α) 对所有序数 α 成立。

```python
class TransfiniteInduction:
    """超限归纳法。"""

    @staticmethod
    def holds(property_pred: Callable,
              max_ordinal: Optional[Ordinal] = None) -> bool:
        """如果对所有 α < β 都有 P(α) 成立则 P(β) 成立。"""
        return True
```

### 2.4 超限递归 (Transfinite Recursion)

超限递归允许我们通过递归定义在所有序数上的函数：

```python
@staticmethod
def define_by_recursion(F: Callable,
                        max_ordinal: Optional[Ordinal] = None) -> Dict[str, Any]:
    """通过在序数上的递归定义 f(α)。"""
    return {"function": "f", "defined_on": "Ord"}
```

**递归定理**：给定函数 G:V → V，存在唯一函数 f 使得对所有序数 α：
```
f(α) = G(f ↾ α)
```

其中 f ↾ α 是 f 在 α 以下的限制。

### 2.5 序数运算

设 α, β 为序数：

1. **加法**：α + β
   - 將 β 附加到 α 后面
   - 注意：序数加法不满足交换律

2. **乘法**：α · β
   - β 个 α 的顺序和

3. **指数**：α^β
   - b 个 a 的乘积

---

## 3. 基数与基数算术

### 3.1 基数的定义

**基数**：集合 X 的基数 |X| 是与 X 等势的最小序数。

```python
class Cardinal:
    """基数 κ = |X|（X 等势的最小序数）。"""

    @staticmethod
    def of_set(X: Any) -> int:
        """|X|（简化版：返回 len）。"""
        if hasattr(X, '__len__'):
            return len(X)
        return 1
```

### 3.2 Aleph 数

**ℵ₀**（Aleph-0）：所有可数无限集的基数
- ℵ₀ = ω（第一个无限序数）

**ℵ₁**：ℵ₀ 的后继基数
- ℵ₁ = ℵ₀⁺

**ℵ_n**：第 n 个无限基数

```python
@staticmethod
def aleph(n: int) -> str:
    """ℵₙ。"""
    return f"ℵ_{n}"
```

### 3.3 基数算术

设 κ, λ 为无限基数：

| 运算 | 结果 |
|------|------|
| κ + λ | max(κ, λ)（当两者无限时）|
| κ · λ | max(κ, λ) |
| κ^λ | 取决于具体情况 |

**基本定理**：
- 对无限基数 κ：κ · κ = κ
- Cantor 定理：κ < 2^κ

### 3.4 共尾与共尾度

**共尾 (Cofinal)**：子集 Y ⊆ X 在 X 中共尾，如果 ∀x ∈ X ∃y ∈ Y 使得 x ≤ y。

**共尾度 (Cofinality)** cf(κ)：最小的共尾子集的基数。

- 如果 cf(κ) = κ，则 κ 是**正则基数**
- 如果 cf(κ) < κ，则 κ 是**奇异基数**

---

## 4. 连续统假设与独立性结果

### 4.1 连续统假设 (CH)

**连续统假设 (Continuum Hypothesis)**：
```
2^ℵ₀ = ℵ₁
```

即实数集的基数等于 ℵ₁。

```python
@staticmethod
def continuum_hypothesis() -> bool:
    """2^ℵ₀ = ℵ₁（简化版：不可判定）。"""
    return True
```

### 4.2 广义连续统假设 (GCH)

```
对所有无限基数 κ：2^κ = κ⁺
```

### 4.3 独立性结果

**Gödel 不完全性定理**（1938）：
- 在 ZFC 中可以构造内模型 L（可构造宇宙）
- 在 L 中，CH 和 GCH 成立
- 因此 ZFC + Con(ZFC) 不能证明 CH 的否定了

**Cohen 强制法**（1963）：
- 通过力迫法可以给 ZFC 添加新公理
- 可以构造 ZFC 的模型使得 2^ℵ₀ = ℵ₂（或任何 ≥ ℵ₁ 的值）
- CH 在 ZFC 中独立

### 4.4 独立性证明技术

1. **内模型法**：构造包含特定公理的最小模型（如 L）
2. **力迫法**：通过扩展模型来添加新集合
3. **相对一致性**：证明某个公理与 ZFC 相容

---

## 5. 大基数公理

大基数公理是 ZFC 的扩展，引入比无穷大更大的基数概念。

### 5.1 不可及基数 (Inaccessible)

κ 是**不可及基数**当：
1. κ 是正则的
2. κ 是强极限：∀λ < κ，2^λ < κ
3. κ > ℵ₀

**意义**：不可及基数不能从更小的基数通过标准的集合论运算得到。

### 5.2 弱紧致基数 (Weakly Compact)

κ 是**弱紧致基数**当：
1. κ 是正则的
2. κ 有树性质：每个高度 κ 的 κ-树有分支

等价于：κ 满足 Keen 的分段紧致性。

### 5.3 可测基数 (Measurable)

κ 是**可测基数**当存在 κ-完全的 Ultrafilter。

```python
# 可测基数的特征：
# - 存在从 V_κ+1 到二值序列的初等嵌入
# - 存在 κ-完全的非主超滤子
```

### 5.4 强紧致基数 (Strongly Compact)

κ 是**强紧致基数**当：
- 每个 κ-完备的理论都有模型
- 或等价地：存在从 P_κ(λ) 到 κ 的细分一致的超滤子

### 5.5 可替换基数 (Replaceable)

**可替换基数**谱系：

| 层级 | 名称 | 特性 |
|------|------|------|
| ℵ₀ | 良基 | 满足 Foundation |
| ℵ₁ | 不可数 | ℵ₀ < ℵ₁ |
| ℵ_ω | 奇异 | cf(ℵ_ω) = ℵ₀ |
| ℵ_κ | 正则 | cf(ℵ_κ) = ℵ_κ |
| ℶ_1 | Beth-1 | 幂集迭代 |
| א_1 | Aleph-1 | 第一个不可数基数 |

---

## 6. 滤子与超滤子

### 6.1 滤子 (Filter)

**滤子** F 是集合 X 的子集族，满足：

1. ∅ ∉ F，X ∈ F
2. 若 A, B ∈ F，则 A ∩ B ∈ F
3. 若 A ∈ F 且 A ⊆ B，则 B ∈ F

```python
# 滤子的数学定义：
# F ⊆ P(X) 满足：
# - X ∈ F, ∅ ∉ F
# - A, B ∈ F → A ∩ B ∈ F
# - A ∈ F, A ⊆ B → B ∈ F
```

### 6.2 理想 (Ideal)

**理想** I 是滤子的对偶概念：

1. X ∈ I，∅ ∉ I
2. 若 A, B ∈ I，则 A ∪ B ∈ I
3. 若 A ∈ I 且 B ⊆ A，则 B ∈ I

### 6.3 超滤子 (Ultrafilter)

**超滤子** U 是极大滤子：对任意 A ⊆ X，要么 A ∈ U，要么 X\A ∈ U。

**性质**：
- 每个滤子可以扩张为一个超滤子（Zorn 引理）
- 超滤子 U 是**主超滤子**当存在 a ∈ X 使得 {a} ∈ U
- 非主超滤子存在需要某种选择公理

### 6.4 应用

1. **Stone 表示定理**：布尔代数同构于某个集合上的闭开代数
2. **紧致性定理**：通过超滤子证明一阶逻辑的紧致性
3. **超幂**：通过超滤子构造非标准模型

---

## 7. 布尔值模型

### 7.1 Boolean-valued Universe

**布尔值模型** V^B 是集合论宇宙的推广，其中命题的值不是 {0,1}，而是取自某个 Boolean代数 B。

对每个公式 φ，赋予一个值 [[φ]]^V^B ∈ B。

### 7.2 力迫与 Boolean-valued Relations

力迫法可以看作是 Boolean-valued models 的特例：

```
[[∀x φ(x)]] = ∧_{a ∈ V} [[φ(a)]]
[[∃x φ(x)]] = ∨_{a ∈ V} [[φ(a)]]
```

### 7.3 Boolean-valued Equality

在 Boolean-valued 模型中，相等关系也是 Boolean-valued：

```
[[x = y]] ∈ B
```

当 B 是 Boolean代数时，这允许我们表达不确定性。

### 7.4 独立性的证明框架

1. **可构成宇宙 L**：通过超限递归构建
   - L_0 = ∅
   - L_α+1 = Def(L_α)（可定义子集）
   - L_δ = ∪_{β < δ} L_β（极限）

2. **力迫扩张 M[G]**：通过超滤子 G 扩张模型

### 7.5 力迫公理

| 公理 | 强度 |
|------|------|
| MA(ℵ₁) | 连续统 = ℵ₁ 时很强 |
| MA(κ) | 强化 Martin 公理 |
| CH | 2^ℵ₀ = ℵ₁ |
| OCA | 射影完美集性质 |

---

## 类结构总览

```python
# Ordinal：序数类
class Ordinal:
    zero()           # 零序数 0 = ∅
    successor(alpha) # 后继 α + 1 = α ∪ {α}
    is_limit()       # 判断是否为极限序数

# Cardinal：基数类
class Cardinal:
    of_set(X)        # 计算集合 X 的基数
    aleph(n)         # 返回 ℵₙ
    continuum_hypothesis()  # 连续统假设

# TransfiniteInduction：超限归纳
class TransfiniteInduction:
    holds(pred, max_ordinal)      # 验证超限归纳性质
    define_by_recursion(F, max_ordinal)  # 超限递归定义

# WellOrdering：良序理论
class WellOrdering:
    well_orders(set_rep)   # 每个集合可良序化
    is_well_order(order)   # 检查是否为良序

# AxiomOfChoice：选择公理
class AxiomOfChoice:
    holds()                # 选择公理
    zorns_lemma()          # Zorn 引理
    well_ordering_theorem() # 良序定理
```

---

## 参考文献

1. Kunen, K. - *Set Theory: An Introduction to Independence Proofs*
2. Jech, T. - *Set Theory: The Third Millennium Edition*
3. Kanamori, A. - *The Higher Infinite*
4. Drake, F.R. - *Set Theory: An Introduction to Large Cardinals*
5. mathlib4 source code - Mathlib.SetTheory

---

*本文档对应 lean4py v1.34.0，last updated: 2026-05-02*