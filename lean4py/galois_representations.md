# Galois 表示论 (Galois Representations)

本模块实现 Galois 表示论的核心概念，对应 mathlib4 的 `Mathlib.NumberTheory.GaloisRepresentation` 模块。

## 1. Galois 表示的基本定义

**Galois 表示**是连续群同态：

```
ρ : Gal(K̄/K) → GL_n(ℂ)  （复表示）
ρ : Gal(K̄/K) → GL_n(ℚ_p) （p-adic 表示）
```

其中 `Gal(K̄/K)` 是域 K 的绝对 Galois 群，配备 Krull 拓扑。

### 类：`GaloisRepresentation`

```python
class GaloisRepresentation:
    """Galois representation ρ: Gal(K̄/K) → GL(V)."""

    def __init__(self, galois_group: str, dimension: int):
        self.galois_group = galois_group  # 基域 K 的 Galois 群
        self.dim = dimension               # 表示的维度 n
```

**连续性条件**：Galois 群配备Krull拓扑，表示必须为连续同态。

**字符**：表示 ρ 的字符定义为 `χ(σ) = Tr(ρ(σ))`，即迹函数。

---

## 2. ℓ-adic 表示

设 ℓ 为素数。**ℓ-adic 表示**是形如：

```
ρ : Gal(K̄/K) → GL_n(ℚ_ℓ)
```

的连续同态，其中 ℚ_ℓ 是 ℓ-adic 数域。

### 类：`LAdicRepresentation`

```python
class LAdicRepresentation:
    """l-adic Galois representation (ρ: G_K → GL_n(Q̄_l))."""
```

**权重 (Weight)**：ℓ-adic 表示的权重决定了其行列式表示的复杂度。权重的概念来自 Weight Conjecture 和 Ramanujan-Petersson 理论。

**ℓ-adic 刚性与局部-整体兼容**：ℓ-adic 表示在不同 ℓ 之间存在强烈的约束关系，受制于 Saito-Kato 等深刻结果。

---

## 3. 局部 Galois 表示（位于 p）

对于固定的素数 p，域 K 的**局部 Galois 群** `G_K = Gal(K̄/K)` 的表示称为局部表示。

### Fontaine 理论 (p-adic Hodge 理论)

**类：`FontaineTheory`**

Fontaine 建立了 p-adic Hodge 理论，将 p-adic Galois 表示分类到不同的 cohomology 域：

```python
class FontaineTheory:
    """Fontaine's theory: p-adic Hodge theory."""
```

**de Rham 条件**：表示 ρ 是 de Rham 的，当且仅当其在 p 处的 Frobenius 特征值满足特定条件。

** Crystalline 条件**：每个 crystalline 表示都是 de Rham 的，但反之不成立。

**Fontaine 的戒指理论**：
- `B_{dR}`：p-adic 时期的 de Rham 戒指
- `B_{cris}`：crystalline 戒指
- `B_{st}`：semi-stable 戒指
- `B_{HT}`：Hodge-Tate 戒指

---

## 4. Weil-Deligne 表示

Weil-Deligne 表示是局部 Galois 表示的另一种描述方式，特别适用于需要处理 monodromy 的情形。

### 类：`WeilDeligneRepresentation`

```python
class WeilDeligneRepresentation:
    """Weil-Deligne representation (π, N, ρ)."""

    def __init__(self, pi: str, N: Optional[List[List[float]]] = None):
        self.pi = pi  # 平滑表示 (smooth representation)
        self.N = N    # Monodromy 算子（nilpotent）
```

**结构**：三元组 `(π, N, ρ)` 包含：
- `π`：Weil 群的平滑表示
- `N`：满足 `N^p = 0` 的幂零算子
- `ρ`：wild inertia 的表示

**表示条件**：和平滑性条件确保表示在紧开子群作用下代数。

---

## 5. Grothendieck 的 ℓ-adic Galois 表示

Grothendieck 将 Galois 表示与代数几何联系起来，通过 **ℓ-adic 上同调**：

```
H^i(X̄, ℚ_ℓ)  →  Gal(K̄/K) 的 ℓ-adic 表示
```

这是 Weil 猜想的核心思想。

**ℓ-adic 上同调的基本性质**：
- 勒雷特上同调给出 Galois 表示
- Frobenius 元的作用产生 Hasse-Weil ζ-函数
- 互反律 (Reciprocity) 连接局部与整体表示

---

## 6. 动机与 motivic Galois 群

**动机** (Motive) 是代数圈类的统一对象，介于代数簇与 Galois 表示之间。

### motivic Galois 群

**绝对 motivic Galois 群** `G_{mot}` 定义为：

```
G_{mot} = Aut(Mot_K)
```

其中 `Mot_K` 是域 K 上的混合动机范畴。

**标准猜测**：
- 每一个混合动机产生一个 Galois 表示
- 每一个 Galois 表示（满足一定条件）来自一个动机
- Langlands 猜测是这个对应的一般化

**period 戒指**：Grothendieck 的 period 概念揭示了 motivic Galois 群与 p-adic Galois 表示之间的深刻联系。

---

## 7. Langlands 对应

Langlands 对应描述了 Galois 表示与自守形式之间的对应关系。

### 局部 Langlands 对应

对于局部域 K 和素数 ℓ：

```
局部 Galois 表示 (ℓ-adic)  ←→  局部 Lanlands 参数 (π, ω)
```

**包络表示**：Langlands 猜测每个局部的 Galois 表示对应一个光滑表示的包络（envelope）。

### 全局 Langlands 对应

对于数域 K：

```
全局 Galois 表示  ←→  自守尖点形式（GL_n）
```

**Functoriality**：Langlands 传递性允许在不同的约化群之间传递表示。

**端点 (Endoscopy)**：稳定迹公式是证明 Langlands 对应的核心工具。

---

## 8. Serre 猜测

**Serre 模性猜测**（已由 Khare-Wintenberger 证明）指出：

每个奇异的 2 维 mod p Galois 表示
```
ρ : Gal(Q̄/Q) → GL_2(F_p)
```
在满足一定条件时，均来自模形式。

### 关键定理

- **Khare-Wintenberger (2009)**：证明了 Serre 的所有猜测
- **Landfix-Serre**：针对低权重情形的早期结果
- **p-adic Langlands**：p-adic 表示空间与 p-adic 自守形式的对应

---

## 模块结构总结

| 类 | 对应的数学概念 |
|-----|---------------|
| `GaloisRepresentation` | 基础 Galois 表示 ρ: Gal(K̄/K) → GL_n |
| `LAdicRepresentation` | ℓ-adic Galois 表示 |
| `WeilDeligneRepresentation` | Weil-Deligne 三元组 (π, N, ρ) |
| `FontaineTheory` | p-adic Hodge 理论（de Rham, crystalline） |

## 数学背景

本模块的设计参考了以下数学文献：

1. **Deligne**: Les constantes des équations fonctionnelles
2. **Fontaine**: Sur certainesclasses de représentations λ-adiques
3. **Tate**: Number theoretic background
4. **Bernstein-Zelevinsky**: Induced representations of p-adic groups

## 与 mathlib4 的对应

本模块对应 mathlib4 中的：
- `Mathlib.NumberTheory.GaloisRepresentation.Basic`
- `Mathlib.NumberTheory.GaloisRepresentation.LAdicRep`
- `Mathlib.RepresentationTheory.FiniteDimensional`

---

*文档版本：1.27.0*