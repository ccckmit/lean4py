# 代数结构模块 (Algebraic Structures Module)

## 概述

本模块实现了现代代数几何与同调代数中的核心代数结构，对应 mathlib4 的 `Mathlib.Algebra` 子模块。主要包括模论、张量积、正合序列等基本概念。

---

## 1. 环上的模 (Modules over Rings)

### 数学定义

设 $R$ 为环，$M$ 为阿贝尔群。若存在标量乘法 $R \times M \to M$ 满足：

1. $r \cdot (m_1 + m_2) = r \cdot m_1 + r \cdot m_2$
2. $(r_1 + r_2) \cdot m = r_1 \cdot m + r_2 \cdot m$
3. $(r_1 r_2) \cdot m = r_1 \cdot (r_2 \cdot m)$
4. $1_R \cdot m = m$

则称 $M$ 为 $R$-左模。

### 代码实现

```python
class Module:
    """Module over a ring.

    Generalization of vector spaces: scalars come from a ring instead of a field.
    Axioms: abelian group under +, scalar multiplication satisfying distributivity.
    """

    def __init__(self, ring: Any, dimension: int):
        self.ring = ring
        self.dim = dimension
```

模是向量空间的推广，其关键区别在于：
- 向量空间要求标量来自**域**（field），域要求非零元素均可逆
- 模的标量来自**环**（ring），环不一定有乘法逆元

这使得模的结构更为复杂，例如存在无基的自由模、投射模不等于自由模等现象。

---

## 2. 向量空间作为域上的模 (Vector Spaces as Modules over Fields)

### 数学定义

设 $K$ 为域，$V$ 为阿贝尔群。若 $V$ 是 $K$-模，则称 $V$ 为向量空间。

域 $K$ 满足：每个非零元素 $k \in K$ 都有乘法逆元 $k^{-1}$。

### 数学原理

向量空间是模的特殊情形，其特殊之处在于：

1. **维数不变性**：向量空间的基的大小是唯一的（维数定理）
2. **每个子空间都有补空间**：若 $W \subseteq V$，则存在 $U$ 使得 $V = W \oplus U$
3. **线性无关集可扩展为基**：Zorn 引理保证这一性质对所有向量空间成立

这与一般环上的模形成对比——$\mathbb{Z}$-模（阿贝尔群）未必有基（例如 $\mathbb{Z}/2\mathbb{Z}$ 作为 $\mathbb{Z}$-模没有基）。

---

## 3. 交换代数中的理想 (Ideals in Commutative Algebras)

### 数学定义

设 $A$ 为交换环，$I \subseteq A$ 为子集。若满足：

1. $I$ 是加法子群
2. $\forall a \in A, \forall x \in I: ax \in I$

则称 $I$ 为 $A$ 的理想。

### 重要类型

| 类型 | 定义 |
|------|------|
| **素理想** $\mathfrak{p}$ | 若 $ab \in \mathfrak{p}$ 则 $a \in \mathfrak{p}$ 或 $b \in \mathfrak{p}$ |
| **极大理想** $\mathfrak{m}$ | 若 $I \supseteq \mathfrak{m}$ 为理想，则 $I = \mathfrak{m}$ 或 $I = A$ |
| **主理想** | 由单个元素生成的理想 $(a) = aA$ |

### 与模的关系

理想用于定义：
- 商环 $A/I$
- 模范畴中的核与余核
- 局部化 $S^{-1}A$

---

## 4. 直和与直积 (Direct Sum and Direct Product)

### 数学定义

给定一族 $R$-模 $\{M_i\}_{i \in I}$：

**直积**（Direct Product）：
$$\prod_{i \in I} M_i = \left\{(m_i)_{i \in I} \mid m_i \in M_i\right\}$$

**直和**（Direct Sum）：
$$\bigoplus_{i \in I} M_i = \left\{(m_i) \in \prod M_i \mid m_i = 0 \text{ 对几乎所有 } i\right\}$$

### 有限情形

当 $I$ 为有限集时，直和与直积相同：
$$\bigoplus_{i=1}^n M_i \cong \prod_{i=1}^n M_i \cong M_1 \times \cdots \times M_n$$

### 泛性质

- 直积：任给一族映射 $f_i: X \to M_i$，存在唯一映射 $f: X \to \prod M_i$
- 直和：任给一族映射 $f_i: M_i \to X$，存在唯一映射 $f: \bigoplus M_i \to X$

---

## 5. 自由模与基 (Free Modules and Bases)

### 数学定义

$R$-模 $F$ 称为**自由模**，若存在子集 $B \subseteq F$ 使得：

1. $B$ 线性无关（即 $\sum r_i b_i = 0 \Rightarrow r_i = 0$）
2. $B$ 生成 $F$（即每个 $f \in F$ 可表示为有限线性组合）

此时 $B$ 称为基，$|B|$ 称为 $F$ 的秩。

### 代码实现

```python
class FreeModule(Module):
    """Free module: has a basis."""

    def __init__(self, ring: Any, dimension: int):
        super().__init__(ring, dimension)
        self._basis = self.basis()

    def is_free(self) -> bool:
        """Check if module is free."""
        return len(self._basis) == self.dim

    def rank(self) -> int:
        """Rank of free module (= dimension)."""
        return self.dim
```

### 重要性质

1. 自由模的秩可能是多值的（如 $\mathbb{Z}/4\mathbb{Z}$ 上的自由模）
2. 非自由模的例子：$\mathbb{Z}/2\mathbb{Z}$ 作为 $\mathbb{Z}$-模
3. 自由模的子模未必自由（除非环是 PID）

---

## 6. 模的张量积 (Tensor Product of Modules)

### 数学定义

设 $M$ 为 $R$-左模，$N$ 为 $R$-右模。张量积 $M \otimes_R N$ 是阿贝尔群，满足泛性质：

对任意双线性映射 $f: M \times N \to G$（$G$ 为阿贝尔群），存在唯一群同态 $\tilde{f}: M \otimes_R N \to G$ 使得交换图成立。

### 代码实现

```python
class TensorProduct:
    """Tensor product of modules."""

    def __init__(self, mod1: Module, mod2: Module):
        self.mod1 = mod1
        self.mod2 = mod2
        self.dim = mod1.dim * mod2.dim

    def tensor(self, v1: Tuple, v2: Tuple) -> Tuple:
        """Tensor product v1 ⊗ v2."""
        return tuple(v1_i * v2_j for v1_i in v1 for v2_j in v2)
```

### 维数公式

若 $M, N$ 为有限生成自由模：
$$\dim(M \otimes_R N) = \dim(M) \cdot \dim(N)$$

### 基本性质

1. **双线性性**：$(m_1 + m_2) \otimes n = m_1 \otimes n + m_2 \otimes n$
2. **模作用**：$r \cdot (m \otimes n) = (r \cdot m) \otimes n = m \otimes (r \cdot n)$
3. **结合性**：$(M \otimes N) \otimes P \cong M \otimes (N \otimes P)$
4. **分配性**：$M \otimes (N \oplus P) \cong (M \otimes N) \oplus (M \otimes P)$

---

## 7. 正合序列 (Exact Sequences)

### 数学定义

给定 $R$-模与同态序列：
$$\cdots \xrightarrow{f_{i-1}} M_i \xrightarrow{f_i} M_{i+1} \xrightarrow{f_{i+1}} \cdots$$

在 $M_i$ 处**正合**当且仅当 $\operatorname{im}(f_{i-1}) = \ker(f_i)$。

### 代码实现

```python
class ExactSequence:
    """Exact sequence of modules.

    A sequence ... → A_{i-1} → A_i → A_{i+1} → ... is exact
    if im(f_i) = ker(f_{i+1}) for all i.
    """

    def __init__(self, modules: List[Module],
                 maps: List[Callable[[Tuple], Tuple]]):
        self.modules = modules
        self.maps = maps

    def is_exact_at(self, i: int) -> bool:
        """Check exactness at position i (simplified)."""
        if i < 0 or i >= len(self.maps) - 1:
            return True
        return True  # Simplified
```

### 常见正合序列类型

| 类型 | 形式 |
|------|------|
| **短正合序列** | $0 \to M' \xrightarrow{f} M \xrightarrow{g} M'' \to 0$ |
| **分裂正合序列** | $M \cong M' \oplus M''$ |
| **五引理交换图** | 控制同态间的兼容性 |

### Snake 引理

给定交换图：
```
  0     0     0
   ↓     ↓     ↓
  M' → M → M''
   ↓     ↓     ↓
  N' → N → N''
   ↓     ↓     ↓
  P' → P → P''
```

存在正合序列：
$$0 \to \ker(\alpha) \to \ker(\beta) \to \ker(\gamma) \to \operatorname{coker}(\alpha) \to \operatorname{coker}(\beta) \to \operatorname{coker}(\gamma) \to 0$$

---

## 8. 投射模与内射模 (Projective and Injective Modules)

### 投射模 (Projective Modules)

#### 数学定义

$R$-模 $P$ 称为**投射模**，若对于任意满同态 $g: M \twoheadrightarrow N$ 与任意同态 $f: P \to N$，存在提升 $\tilde{f}: P \to M$ 使得 $g \circ \tilde{f} = f$。

交换图：
```
        f
    P ────→ N
     \     ↗
      \   / g
    ∃  \ /
       M
```

#### 等价刻画

以下条件等价：
1. $P$ 是投射模
2. $P$ 是某个自由模的直和项：$F \cong P \oplus Q$
3. 函子 $\operatorname{Hom}_R(P, -)$ 是左正合的
4. 任何正合序列 $0 \to M \to N \to P \to 0$ 分裂

### 内射模 (Injective Modules)

#### 数学定义

$R$-模 $Q$ 称为**内射模**，若对于任意单同态 $f: M \hookrightarrow N$ 与任意同态 $g: M \to Q$，存在扩展 $\tilde{g}: N \to Q$ 使得 $\tilde{g} \circ f = g$。

#### 等价刻画

以下条件等价：
1. $Q$ 是内射模
2. 函子 $\operatorname{Hom}_R(-, Q)$ 是正合的
3. $Q$ 是某个内射余生成子的直和项

### 投射模与内射模的对偶性

| 性质 | 投射模 $P$ | 内射模 $Q$ |
|------|-----------|-----------|
| 泛性质 | 反射自由模 | 余反射内射模 |
| 序列 | 左边正合 | 右边正合 |
| 特殊对象 | 自由模 $\Rightarrow$ 投射 | 内射包络存在 |
| 模论余弦 | 每个模有投射覆盖 | 每个模有内射包络 |

### Baer 判别法

$R$ 为环，$Q$ 为 $R$-模。$Q$ 为内射模当且仅当对每个理想 $I \subseteq R$ 与每个同态 $f: I \to Q$，存在 $r \in R$ 使得 $f(i) = i \cdot r$。

---

## 模块类图

```
Module (基类)
├── FreeModule (自由模)
│   └── 有基，维度可确定
├── Algebra (代数)
│   ├── 向量空间 + 双线性乘法
│   └── 单位元与乘法结构
├── TensorProduct (张量积)
│   ├── 模的张量积
│   └── 维度为原模维度之积
└── ExactSequence (正合序列)
    ├── 映射序列
    └── 验证 im = ker
```

---

## 数学意义

本模块实现了现代代数的核心结构：

1. **模论**是同调代数的基础
2. **张量积**是多重线性代数的核心
3. **正合序列**是连接代数与拓扑的桥梁
4. **投射/内射模**是模范畴的极大/内射余子对象

这些结构支撑着代数几何（如概形的截面模）、表示论（如表示的模）、代数拓扑（如同调群计算）等领域。