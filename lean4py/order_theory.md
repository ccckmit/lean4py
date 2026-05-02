# Order Theory 模块文档

本模块实现了序理论（Order Theory）的基本概念，对应 mathlib4 的 `Mathlib.Order` 库。序理论是数学的一个基础分支，研究元素之间的顺序关系及其性质。

## 1. 偏序集（Partial Orders / Posets）

偏序集是序理论的核心概念。偏序是由集合上的一个二元关系定义的，满足以下三个公理：

### 1.1 公理定义

- **自反性（Reflexive）**：对所有元素 x，有 x ≤ x
- **反对称性（Antisymmetric）**：若 x ≤ y 且 y ≤ x，则 x = y
- **传递性（Transitive）**：若 x ≤ y 且 y ≤ z，则 x ≤ z

### 1.2 代码实现

```python
class PartialOrder:
    def __init__(self, elements: Set[Any], leq: Callable[[Any, Any], bool]):
        self.elements = elements
        self._leq = leq
```

其中 `leq` 函数定义了偏序关系 `≤`。`is_partial_order()` 方法验证三个公理是否满足。

### 1.3 偏序集的应用

偏序集在计算机科学中有广泛应用：
- 程序分析的抽象解释
- 数据库理论的函数依赖
- 类型理论的子类型关系

### 1.4 可比性与极值元素

- **可比性（Comparable）**：两个元素 x 和 y 是可比的，当且仅当 x ≤ y 或 y ≤ x
- **极小元（Minimal Element）**：没有其他元素严格小于它的元素
- **极大元（Maximal Element）**：没有其他元素严格大于它的元素

---

## 2. 全序与链（Total Orders and Chains）

### 2.1 全序定义

全序（Total Order）或线性序（Linear Order）是每两个元素都可比的偏序：

```
∀x, y ∈ S: x ≤ y 或 y ≤ x
```

这意味着全序集中的任意两个元素都能比较大小，形成一条"线性的"顺序。

### 2.2 代码实现

```python
class TotalOrder(PartialOrder):
    def is_total_order(self) -> bool:
        if not self.is_partial_order():
            return False
        for x in self.elements:
            for y in self.elements:
                if not self.is_comparable(x, y):
                    return False
        return True
```

### 2.3 链

在偏序集中，链（Chain）是两两可比的元素子集。实际上，链就是全序子集。

---

## 3. 上确界与下确界（Supremum and Infimum）

### 3.1 上确界（Supremum / Least Upper Bound）

设 S 是偏序集 P 的子集，u 是 S 的上界。如果对于 S 的所有上界 m，都有 u ≤ m，则称 u 是 S 的**最小上界**或**上确界**，记为 sup(S) 或 ⋁S。

### 3.2 下确界（Infimum / Greatest Lower Bound）

设 S 是偏序集 P 的子集，l 是 S 的下界。如果对于 S 的所有下界 m，都有 m ≤ l，则称 l 是 S 的**最大下界**或**下确界**，记为 inf(S) 或 ⋀S。

### 3.3 性质

- 上确界和下确界如果存在则唯一
- 在全序集中，任何有上界（下界）的非空有限子集都有上确界（下确界）
- 在偏序集中，上确界和下确界不一定存在

---

## 4. 格（Lattices）

### 4.1 格的基本定义

格是特殊的偏序集，其中每对元素都有上确界（称为**并**或 **join**，记为 x ∨ y）和下确界（称为**交**或 **meet**，记为 x ∧ y）。

### 4.2 代数定义

格也可以定义为具有两个二元运算 ∨ 和 ∧ 的代数系统，满足：
- **交换律**：x ∨ y = y ∨ x，x ∧ y = y ∧ x
- **结合律**：(x ∨ y) ∨ z = x ∨ (y ∨ z)，(x ∧ y) ∧ z = x ∧ (y ∧ z)
- **吸收律**：x ∨ (x ∧ y) = x，x ∧ (x ∨ y) = x
- **幂等律**：x ∨ x = x，x ∧ x = x

### 4.3 代码实现

```python
class Lattice(PartialOrder):
    def __init__(self, elements: Set[Any], leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any], meet: Callable[[Any, Any], Any]):
        super().__init__(elements, leq)
        self._join = join
        self._meet = meet

    def join(self, x: Any, y: Any) -> Any:
        return self._join(x, y)

    def meet(self, x: Any, y: Any) -> Any:
        return self._meet(x, y)
```

### 4.4 格的例子

| 格 | 并 (∨) | 交 (∧) |
|---|--------|-------|
| 幂集格 | 并集 | 交集 |
| 自然数格（按整除性） | 最小公倍数 | 最大公约数 |
| 实数区间 [0,1] | max | min |

---

## 5. 完全格（Complete Lattices）

### 5.1 完全格的定义

完全格是任意子集（包括无限子集）都有上确界和下确界的格。相比之下，普通格只要求有限对元素有并和交。

### 5.2 完全格的重要性

完全格在数学中有特殊地位，因为：
- 幂集格是完全格
- 任何有限格都是完全格
- 完全格一定有最大元（⊤）和最小元（⊥）

### 5.3 代码实现

```python
class CompleteLattice(Lattice):
    def __init__(self, elements: Set[Any], leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any], meet: Callable[[Any, Any], Any]):
        super().__init__(elements, leq, join, meet)
        self._complete = True

    def is_complete(self) -> bool:
        return self._complete
```

### 5.4 完全格的性质

在完全格中：
- 任意子集 S 的上确界 sup(S) 存在
- 任意子集 S 的下确界 inf(S) 存在
- sup(∅) = ⊥（最小元），inf(∅) = ⊤（最大元）

---

## 6. 伽罗瓦连接（Galois Connections）

### 6.1 定义

设 (P, ≤) 和 (Q, ≲) 是两个偏序集。称函数对 (f: P → Q, g: Q → P) 构成**伽罗瓦连接**，当且仅当：

```
f(x) ≲ y ⇔ x ≤ g(y)
```

对所有 x ∈ P 和 y ∈ Q 成立。

### 6.2 基本性质

- f 是单调递增的（monotone）
- g 是单调递增的（monotone）
- f 和 g 是伴随的（adjoint），f 是左伴随，g 是右伴随

### 6.3 代码实现

```python
class GaloisConnection:
    def __init__(self, order_p: PartialOrder, order_q: PartialOrder,
                 f: Callable[[Any], Any], g: Callable[[Any], Any]):
        self.order_p = order_p
        self.order_q = order_q
        self.f = f
        self.g = g

    def is_galois_connection(self) -> bool:
        for x in self.order_p.elements:
            for y in self.order_q.elements:
                if self.order_q.leq(self.f(x), y) != self.order_p.leq(x, self.g(y)):
                    return False
        return True
```

### 6.4 伽罗瓦连接的经典例子

1. **幂集与集合包含**：设 P = ℘(U)，Q = ℘(V)，f(A) = C(A) 是闭包，g(B) = I(B) 是内部，则 (C, I) 构成伽罗瓦连接
2. **群与子群**：子群格上的包含关系与正规子群对应
3. **概念格**：形式概念分析中的概念层次

### 6.5 单位与余单位

- **单位（Unit）**：x ≤ g(f(x))
- **余单位（Counit）**：f(g(y)) ≤ y

---

## 7. 有向集与网（Directed Sets and Nets）

### 7.1 有向集

有向集（Directed Set）是带有偏序的集合，其中每两个元素都有上界。具体来说：
- D 是非空集合
- ≤ 是 D 上的偏序
- 对任意 x, y ∈ D，存在 z ∈ D 使得 x ≤ z 且 y ≤ z

有向集用于定义有向完备偏序（DCPO，Directed Complete Partial Order）。

### 7.2 网

网（Net）是从有向集到偏序集的映射，用于研究收敛性。网是序列的推广，允许索引集是有向集而非自然数。

### 7.3 在程序语义学中的应用

有向集和网在域理论（Domain Theory）中至关重要，用于：
- 定义递归函数的最小不动点
- 程序的指称语义（Denotational Semantics）
- 不确定性和并发程序的建模

---

## 8. 海廷代数与布尔代数（Heyting and Boolean Algebras）

### 8.1 海廷代数（Heyting Algebra）

海廷代数是直觉主义命题逻辑的代数模型，包含：
- 格结构（并和交）
- 蕴含运算 →

**定义**：在海廷代数中，x → y 是满足以下条件的最大元 z：
```
z ∧ x ≤ y
```

### 8.2 代码实现

```python
class HeytingAlgebra(Lattice):
    def __init__(self, elements: Set[Any], leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any], meet: Callable[[Any, Any], Any],
                 implication: Callable[[Any, Any], Any]):
        super().__init__(elements, leq, join, meet)
        self._imp = implication

    def implies(self, x: Any, y: Any) -> Any:
        return self._imp(x, y)

    def is_heyting(self) -> bool:
        if not self.is_lattice():
            return False
        for x in self.elements:
            for y in self.elements:
                imp = self.implies(x, y)
                if not self.leq(self.meet(x, imp), y):
                    return False
        return True
```

### 8.3 布尔代数（Boolean Algebra）

布尔代数是特殊的海廷代数，其中每个元素都有补元。布尔代数是经典命题逻辑的代数模型。

**公理**：在布尔代数中，对所有 x ∈ B：
- 排中律：x ∨ ¬x = ⊤
- 矛盾律：x ∧ ¬x = ⊥

### 8.4 代码实现

```python
class BooleanAlgebra(HeytingAlgebra):
    def __init__(self, elements: Set[Any], leq: Callable[[Any, Any], bool],
                 join: Callable[[Any, Any], Any], meet: Callable[[Any, Any], Any],
                 implication: Callable[[Any, Any], Any],
                 complement: Callable[[Any], Any]):
        super().__init__(elements, leq, join, meet, implication)
        self._not = complement

    def complement(self, x: Any) -> Any:
        return self._not(x)

    def is_boolean(self) -> bool:
        if not self.is_heyting():
            return False
        for x in self.elements:
            if not self.leq(self.join(x, self.complement(x)),
                           self.join(self.complement(x), x)):
                return False
        return True
```

### 8.5 代数结构层次

```
偏序集 (Partial Order)
    ↓
格 (Lattice) — 每对元素有并和交
    ↓
Heyting 代数 — 格 + 蕴含运算
    ↓
布尔代数 — Heyting 代数 + 补元
```

### 8.6 逻辑对应

| 代数结构 | 对应逻辑 |
|---------|---------|
| 偏序集 | 预序逻辑 |
| 格 | 含交换/结合/吸收律的逻辑 |
| Heyting 代数 | 直觉主义命题逻辑 |
| 布尔代数 | 经典命题逻辑 |

---

## 模块类图

```
PartialOrder
    ├── TotalOrder
    └── Lattice
            ├── CompleteLattice
            └── HeytingAlgebra
                    └── BooleanAlgebra

GaloisConnection (独立类)
```

---

## 使用示例

### 创建偏序集

```python
# 自然数集上的小于等于关系
nat_leq = lambda x, y: x <= y
poset = PartialOrder({1, 2, 3, 4}, nat_leq)
assert poset.is_partial_order() == True
```

### 创建格

```python
# 幂集格的例子
from lean4py.order_theory import Lattice

elements = [set(), {1}, {2}, {1, 2}]
leq = lambda x, y: x.issubset(y)
join = lambda x, y: x.union(y)
meet = lambda x, y: x.intersection(y)
lattice = Lattice(set(elements), leq, join, meet)
```

### 布尔代数验证

```python
# 二元素 Boolean 代数 {0, 1}
from lean4py.order_theory import BooleanAlgebra

B = {0, 1}
leq = lambda x, y: x <= y
join = lambda x, y: max(x, y)
meet = lambda x, y: min(x, y)
impl = lambda x, y: max(1 - x, y)  # x → y = ¬x ∨ y
comp = lambda x: 1 - x            # ¬x = 1 - x
bool_alg = BooleanAlgebra(B, leq, join, meet, impl, comp)
assert bool_alg.is_boolean() == True
```

---

## 数学意义

本模块实现了序理论的核心概念，这些概念在数学和计算机科学中有深远影响：

1. **范畴论视角**：偏序集可以视为特殊的小范畴，格是带有有限积和余积的范畴
2. **拓扑学应用**：偏序集的序拓扑、连续性
3. **逻辑学基础**： Heyting 代数和布尔代数是数理逻辑的代数基础
4. **程序分析**：抽象解释中使用格理论进行不动点计算
5. **形式概念分析**：伽罗瓦连接用于概念格的构建

本模块的设计遵循 mathlib4 的组织方式，便于与 Lean 4 数学库进行互操作。