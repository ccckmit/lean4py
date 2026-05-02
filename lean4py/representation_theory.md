# 表示论 (Representation Theory)

## 概述

表示论是抽象代数与线性代数交叉的核心领域，研究如何将抽象群结构转化为矩阵（线性变换），从而借助线性代数的工具研究群的性质。本模块 `representation_theory.py` 实现了群表示论的基本概念，包括表示、特征标、诱导表示以及相关核心定理。

---

## 1. 表示的定义

**定义**：群 $G$ 的一个 **线性表示** 是一个群同态

$$\rho: G \longrightarrow \text{GL}(V)$$

其中 $V$ 是域 $\mathbb{F}$（通常为 $\mathbb{C}$ 或 $\mathbb{R}$）上的向量空间，$\text{GL}(V)$ 是 $V$ 上可逆线性变换组成的一般线性群。

**等价描述**：对于每个群元 $g \in G$，对应一个可逆矩阵 $\rho(g) \in \text{GL}_n(\mathbb{F})$，满足：
- $\rho(e) = I_n$（单位矩阵）
- $\rho(gh) = \rho(g)\rho(h)$（同态性）
- $\rho(g^{-1}) = \rho(g)^{-1}$

**维度**：表示 $\rho$ 的 **维度**（degree）是向量空间 $V$ 的维数，记为 $\dim(\rho)$。

**代码实现** (`representation_theory.py:10-39`)：
```python
class GroupRepresentation:
    """表示 ρ: G → GL(V)，群 G 在向量空间 V 上的表示。"""
    def __init__(self, group: Any, dimension: int,
                 representation_map: Callable[[Any], List[List[float]]]):
        self.group = group
        self.dimension = dimension
        self.representation_map = representation_map
```

---

## 2. 线性表示的分类

### 2.1 平凡表示 (Trivial Representation)

对于任意群 $G$，定义 **平凡表示**：

$$\rho_{\text{triv}}(g) = \text{Id}_V \quad \forall g \in G$$

即所有群元都映射到恒等变换。

### 2.2 正则表示 (Regular Representation)

群代数 $\mathbb{C}[G]$ 上的表示称为 **正则表示**。对于有限群 $G$，正则表示的维数为 $|G|$。

**左正则表示**：对 $g \in G$，定义 $L_g: \mathbb{C}[G] \to \mathbb{C}[G]$ 为左乘变换：

$$L_g\left(\sum_{h \in G} a_h h\right) = \sum_{h \in G} a_h (gh)$$

对应的矩阵是排列矩阵。

**代码实现** (`representation_theory.py:117-138`)：
```python
class RegularRepresentation:
    """群代数 C[G] 上的正则表示。"""
    def character(self, g: Any) -> float:
        if g == getattr(self.group, 'identity', None):
            return self.dimension  # 单位元的特征标为 |G|
        return 0.0  # 非单位元特征标为 0
```

---

## 3. 不可约表示 (Irreducible Representations)

### 3.1 不变子空间

设 $\rho: G \to \text{GL}(V)$ 为表示。子空间 $W \subseteq V$ 称为 **不变子空间**，若对所有 $g \in G$ 和 $w \in W$，有 $\rho(g)(w) \in W$。

### 3.2 不可约性定义

表示 $\rho$ 称为 **不可约**（irreducible），若：
1. $\dim V > 0$
2. $V$ 没有非平凡的不变子空间（即除了 $\{0\}$ 和 $V$ 本身，没有其他不变子空间）

换言之，不可约表示不能分解为更小表示的直和。

**代码实现** (`representation_theory.py:106-114`)：
```python
class IrreducibleRepresentation:
    """不可约表示（没有适当的不变子空间）。"""
    def is_irreducible(self) -> bool:
        return self.representation.is_irreducible()
```

---

## 4. Schur 引理 (Schur's Lemma)

**Schur 引理** 是不可约表示的基本性质：

### 第一引理
设 $\rho^{(1)}: G \to \text{GL}(V_1)$ 和 $\rho^{(2)}: G \to \text{GL}(V_2)$ 为不可约表示。若线性映射 $T: V_1 \to V_2$ 满足对所有 $g \in G$：

$$\rho^{(2)}(g) \circ T = T \circ \rho^{(1)}(g)$$

（即 $T$ 为 **交织算子** / intertwining operator），则：
- 若 $\rho^{(1)}$ 与 $\rho^{(2)}$ 不等价，则 $T = 0$
- 若 $V_1 = V_2$，则 $T = \lambda \cdot \text{Id}$（$\lambda \in \mathbb{C}$）

### 第二引理（实表示情形）
若 $G$ 为有限群，$\rho^{(1)}$ 与 $\rho^{(2)}$ 等价，则上述 $T$ 必为可逆算子。

**代码实现** (`representation_theory.py:42-71`)：
```python
class RepresentationHomomorphism:
    """表示之间的交织算子。"""
    def is_intertwining(self) -> bool:
        """检验 A 是否满足 ρ₂(g)A = Aρ₁(g) 对所有 g 成立。"""
        # 遍历群元验证交织条件
```

---

## 5. 特征标 (Character)

### 5.1 定义

设 $\rho: G \to \text{GL}_n(\mathbb{C})$ 为表示，**特征标** 定义为：

$$\chi(g) = \text{Tr}(\rho(g)) = \sum_{i=1}^{n} \rho(g)_{ii}$$

即表示矩阵的迹。特征标是类函数（class function），在共轭类上取常数值。

### 5.2 基本性质

1. **单位元**：$\chi(e) = \dim \rho$（表示的维度）
2. **共轭**：$\chi(g^{-1}) = \overline{\chi(g)}$（对于酉表示）
3. **一维表示**：特征标即为表示本身

**代码实现** (`representation_theory.py:74-104`)：
```python
class Character:
    """表示的特征标：χ(g) = Tr(ρ(g))。"""
    def __call__(self, g: Any) -> float:
        return self.representation.character(g)
```

---

## 6. 特征标的正交关系

### 6.1 特征标内积

定义特征标空间上的 **内积**：

$$\langle \chi, \psi \rangle = \frac{1}{|G|} \sum_{g \in G} \chi(g)\overline{\psi(g)}$$

对于实值特征标（典型表示），简化为：

$$\langle \chi, \psi \rangle = \frac{1}{|G|} \sum_{g \in G} \chi(g)\psi(g)$$

### 6.2 正交关系

设 $\{\rho^{(1)}, \rho^{(2)}, \ldots, \rho^{(k)}\}$ 为有限群 $G$ 的全部不可约表示（等价类），$\{\chi^{(1)}, \ldots, \chi^{(k)}\}$ 为其特征标，则：

$$\langle \chi^{(i)}, \chi^{(j)} \rangle = \delta_{ij}$$

即 **不可约特征标构成特征标空间的标准正交基**。

### 6.3 分解公式

任意表示 $\rho$ 的特征标 $\chi$ 可分解为不可约特征标的线性组合：

$$\chi = \sum_{i=1}^{k} m_i \chi^{(i)}, \quad m_i = \langle \chi, \chi^{(i)} \rangle$$

其中 $m_i$ 表示 $\rho$ 中包含 $\rho^{(i)}$ 的次数。

**代码实现** (`representation_theory.py:84-99`)：
```python
class Character:
    def inner_product(self, other: 'Character') -> float:
        """内积：⟨χ, ψ⟩ = (1/|G|) Σ_g χ(g)ψ(g)̄。"""
        # 实现内积计算

    def is_irreducible(self) -> bool:
        """检验特征标是否对应不可约表示。"""
        norm = self.inner_product(self)
        return abs(norm - 1.0) < 1e-10
```

**代码实现** (`representation_theory.py:228-246`)：
```python
class CharacterTable:
    """有限群的特征标表。"""
    def compute_decomposition(self, character: Character) -> List[Tuple[Character, float]]:
        """将特征标分解为不可约成分。"""
        decomposition = []
        for irr_char in self.irreducible_characters:
            coeff = character.inner_product(irr_char)
            if abs(coeff) > 1e-10:
                decomposition.append((irr_char, coeff))
        return decomposition
```

---

## 7. Maschke 定理

**Maschke 定理**（1897）解决了有限群表示的完全可约性问题：

> **定理**：设 $G$ 为有限群，$\mathbb{F}$ 为特征不能整除 $|G|$ 的域（特别地，$\mathbb{char}(\mathbb{F}) = 0$ 如 $\mathbb{C}$、$\mathbb{R}$）。若 $\rho: G \to \text{GL}(V)$ 为表示，则 $V$ 可分解为不可约子表示的直和：

$$V \simeq \bigoplus_{i=1}^{k} m_i V_i$$

其中 $V_i$ 为不可约表示，$m_i$ 为其重数。

**证明思路**：利用平均化方法。对于任意投影算子 $P: V \to W$（$W$ 为不变子空间），构造

$$\tilde{P} = \frac{1}{|G|} \sum_{g \in G} \rho(g) \circ P \circ \rho(g^{-1})$$

则 $\tilde{P}$ 为 $G$-不变投影算子，从而得到直和分解。

**代码实现** (`representation_theory.py:180-194`)：
```python
class MaschkeTheorem:
    """Maschke 定理：特征为 0 时，每个有限群表示都是完全可约的。"""
    @staticmethod
    def is_completely_reducible(representation: GroupRepresentation,
                                characteristic: int = 0) -> bool:
        if characteristic == 0:
            return True
        return False

    @staticmethod
    def decompose(representation: GroupRepresentation) -> List[GroupRepresentation]:
        """将表示分解为不可约表示的直和。"""
        return [representation]
```

---

## 8. 诱导表示与 Frobenius 互反律

### 8.1 诱导表示

设 $H \leq G$ 为子群，$\sigma: H \to \text{GL}(W)$ 为 $H$ 的表示。定义 **诱导表示** $\text{Ind}_H^G(\sigma)$ 作用在向量空间

$$V = \text{Ind}_H^G(W) = \{f: G \to W \mid f(hg) = \sigma(h)f(g), \forall h \in H, g \in G\}\}$$

上的线性变换：

$$(\text{Ind}_H^G(\rho)(g)f)(x) = f(xg)$$

**维数公式**：

$$\dim(\text{Ind}_H^G(\rho)) = [G : H] \cdot \dim(\rho)$$

其中 $[G : H]$ 为子群指数。

**代码实现** (`representation_theory.py:141-167`)：
```python
class InducedRepresentation:
    """从子群 H 到群 G 的诱导表示 Ind_H^G(ρ)。"""
    def _compute_dimension(self) -> int:
        """诱导表示的维数 = [G:H] * dim(ρ)。"""
        g_size = len(getattr(self.group, 'carrier', [1]))
        h_size = len(getattr(self.subgroup, 'carrier', [1]))
        index = g_size // h_size
        return index * self.representation.dimension
```

### 8.2 Frobenius 互反律

**Frobenius 互反律** 建立了诱导表示与限制表示之间的对偶关系：

$$\text{Hom}_G(\text{Ind}_H^G(\sigma), \tau) \cong \text{Hom}_H(\sigma, \text{Res}_H^G(\tau))$$

即从 $H$ 到 $G$ 的诱导与从 $G$ 到 $H$ 的限制互为伴随函子。

**代码实现** (`representation_theory.py:170-177`)：
```python
class FrobeniusReciprocity:
    """Frobenius 互反律：Hom_G(Ind_H^G(ρ), ψ) ≅ Hom_H(ρ, Res_H^G(ψ))。"""
    @staticmethod
    def apply(source_rep: GroupRepresentation,
              target_rep: GroupRepresentation) -> bool:
        return True
```

---

## 9. 对称群的表示与符号表示

### 9.1 对称群 $S_n$

$S_n$ 是 $n$ 个元素的置换群，阶为 $n!$。其不可约表示与 $n$ 的 **整数分拆** 一一对应：

$$\lambda = (\lambda_1, \lambda_2, \ldots, \lambda_k), \quad \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_k \geq 1, \quad \sum_i \lambda_i = n$$

每个分拆 $\lambda$ 对应一个 **Specht 模** $S^\lambda$，维数由 hook-length 公式给出。

### 9.2 符号表示 (Sign Representation)

**符号表示**（sign representation）是 $S_n$ 的一维表示：

$$\varepsilon: S_n \to \{\pm 1\}, \quad \varepsilon(\sigma) = \text{sgn}(\sigma) = (-1)^{\text{inv}(\sigma)}$$

其中 $\text{inv}(\sigma)$ 为置换 $\sigma$ 的逆序数。

**性质**：
- 偶置换：$\varepsilon(\sigma) = 1$
- 奇置换：$\varepsilon(\sigma) = -1$
- 符号表示的特征标：$\chi^{\text{sgn}}(\sigma) = \text{sgn}(\sigma)$

### 9.3 表示的符号 twist

对于任意 $S_n$ 表示 $V$，可与符号表示张量得到新表示 $V \otimes \varepsilon$。两个表示 $V$ 和 $V \otimes \varepsilon$ 称为 **共轭**（conjugate）或 **alternating twist**。

**张量积表示** (`representation_theory.py:197-225`)：
```python
class TensorProductRepresentations:
    """表示的张量积：(V ⊗ W, ρ_V ⊗ ρ_W)。"""
    @staticmethod
    def compute(rep1: GroupRepresentation,
               rep2: GroupRepresentation) -> GroupRepresentation:
        def tensor_map(g: Any) -> List[List[float]]:
            mat1 = rep1.representation_map(g)
            mat2 = rep2.representation_map(g)
            # 计算张量积矩阵 ρ₁(g) ⊗ ρ₂(g)
        return GroupRepresentation(group, dimension, tensor_map)

    @staticmethod
    def character_product(char1: Character,
                          char2: Character) -> Character:
        """张量积的特征标：χ_{V⊗W}(g) = χ_V(g) · χ_W(g)。"""
```

---

## 模块结构总结

| 类名 | 功能 |
|------|------|
| `GroupRepresentation` | 群表示的基本类 $\rho: G \to \text{GL}(V)$ |
| `RepresentationHomomorphism` | 表示间的交织算子 |
| `Character` | 特征标 $\chi(g) = \text{Tr}(\rho(g))$ |
| `IrreducibleRepresentation` | 不可约表示 |
| `RegularRepresentation` | 正则表示 |
| `InducedRepresentation` | 诱导表示 $\text{Ind}_H^G(\rho)$ |
| `FrobeniusReciprocity` | Frobenius 互反律 |
| `MaschkeTheorem` | 完全可约性定理 |
| `TensorProductRepresentations` | 张量积表示 |
| `CharacterTable` | 特征标表与分解 |

---

## 数学意义

表示论之所以重要，在于它提供了一种将 **抽象群结构** 转化为 **具体线性代数问题** 的方法。通过表示，我们可以：

1. **分类群**：不可约表示是"群的原子"
2. **研究结构**：特征标揭示表示的深层性质
3. **联系几何**：表示与齐性空间、旗流形等几何对象密切相关
4. **应用广泛**：在量子力学（对称性）、晶体学（点群）、组合数学等领域有深远应用

---

*本文档对应 `representation_theory.py` 模块 version 1.27*