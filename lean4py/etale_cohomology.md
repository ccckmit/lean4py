# Étale 上同调 (Étale Cohomology)

## 概述

Étale 上同调是代数几何中的一种上同调理论，用于研究概形（scheme）的拓扑性质。它是代数几何与现代数论的核心工具，由格罗滕迪克在 1960 年代建立，目标是解决代数几何中的拓扑问题，特别是在特征 p 的情形下，经典拓扑学方法失效的场景。

本模块实现了以下核心类：
- `EtaleSite`：Étale 拓扑
- `EtaleCohomologyGroup`：Étale 上同调群
- `BaseChange`：基变换定理
- `WeilConjectures`：Weil 猜想（Deligne 定理）

---

## 1. Étale 态射 (Étale Morphisms)

### 定义

设 $f: X \to Y$ 是概形之间的有限型态射。如果 $f$ 是平坦的且其相对微分为零（即 $\Omega_{X/Y} = 0$），则称 $f$ 为 **étale 态射**。

等价地，$f$ 是 étale 态射当且仅当它在平展局部同构（étale local isomorphism）的意义下是局部同构。

### 性质

- Étale 态射是万有开态射（universally open）
- 对于局部诺特概形，étale 态射局部有限呈现（locally of finite presentation）
- 若 $X \to Y$ 是光滑态射且 $\dim X = \dim Y$，则该光滑态射是 étale 的

### 数学意义

Étale 态射可以视为代数几何中的"局部同构"，类似于拓扑空间之间的覆盖映射。这使得我们能够在代数几何的框架下建立类似复分析中的覆盖空间理论。

---

## 2. Étale 基本群 (Étale Fundamental Group)

### 定义

设 $X$ 是连通、局部诺特、几何连通概形。$X$ 的 **Étale 基本群** 记为 $\pi_1^{\text{ét}}(X)$，是 $X$ 上有限 étale 覆盖的分类群。

具体而言，对于 $X$ 的任何有限覆盖 $Y \to X$，$Y$ 在代数闭域上给出有限集合上的连续作用，这诱导了 $\pi_1^{\text{ét}}(X)$ 的商群。

### 函子性

对于任意态射 $f: X \to Y$，存在自然的群同态：
$$f_*: \pi_1^{\text{ét}}(X) \to \pi_1^{\text{ét}}(Y)$$

### 与经典基本群的关系

对于复数域 $\mathbb{C}$ 上的代数簇 $X$，其 étale 基本群与经典拓扑基本群有如下关系：
$$\pi_1^{\text{ét}}(X \times_{\mathbb{C}} \mathbb{C}) \cong \hat{\pi}_1(X^{\text{top}})$$
其中 $\hat{\pi}_1$ 表示拓扑基本群的投射完备化。

---

## 3. Galois 范畴 (Galois Categories)

### 定义

**Galois 范畴** 是与某个群 $G$ 的有限离散集合范畴等价的范畴。典型例子包括：

1. 有限 Galois 扩张的范畴（带 Galois 群作用）
2. 有限 étale 覆盖的范畴
3. 有限 $G$-集的范畴

### 基本定理

设 $\mathcal{C}$ 是 Galois 范畴，$G = \text{Aut}(\mathcal{C})$。则存在自然等价：
$$\mathcal{C} \cong \text{Fin}(G)$$
其中 $\text{Fin}(G)$ 表示有限 $G$-集的范畴。

### 在 Étale 理论中的应用

étale 覆盖的范畴构成一个 Galois 范畴。给定连通概形 $X$，其基本群 $\pi_1^{\text{ét}}(X)$ 完全决定了有限 étale 覆盖的范畴：
$$(\text{有限 étale 覆盖}/X) \cong \text{Fin}(\pi_1^{\text{ét}}(X))$$

这使得我们能够使用群论方法研究代数几何问题。

---

## 4. Étale 上同调群 (Étale Cohomology Groups)

### 定义

设 $X$ 是概形，$F$ 是 $X$ 上的阿贝尔层（abelian sheaf）。$X$ 的 **étale 上同调群** 定义为：
$$H^i_{\text{ét}}(X, F) = \text{Ext}^i_{X_{\text{ét}}}(1_F, F)$$

其中 $X_{\text{ét}}$ 表示 $X$ 的 étale 位（site），$1_F$ 是 $F$ 的单位对象。

### 性质

1. **局部性**：对于任意 étale 覆盖 $\mathcal{U} = \{U_i \to X\}$，有：
   $$H^i_{\text{ét}}(X, F) \cong \check{H}^i(\mathcal{U}, F)$$

2. **同伦不变性**：若 $X$ 是局部诺特的，则：
   $$H^i_{\text{ét}}(X \times \mathbb{A}^1, F) \cong H^i_{\text{ét}}(X, F)$$

3. **Poincaré 对偶**：对于光滑、紧致、几何连通簇 $X$：
   $$H^i_{\text{ét}}(X, \mathbb{Q}_\ell) \cong H^{2d-i}_{\text{ét}}(X, \mathbb{Q}_\ell(d))^\vee$$

### 常见计算

- $H^0_{\text{ét}}(X, \mathbb{G}_m) \cong \mathcal{O}_X(X)^\times$
- 对于有限平坦群 $G$，$H^1_{\text{ét}}(X, G)$ 分类 $G$-torsor

### 与经典上同调的比较

| 维度 | 经典上同调 | Étale 上同调 |
|------|------------|--------------|
| 定义域 | 复拓扑空间 | Étale site |
| 系数 | 整数/有理数 | $\ell$-进整数 $\mathbb{Z}_\ell$，$\mathbb{Q}_\ell$ |
| 计算复杂度 | 较简单 | 需要 Galois 作用 |

---

## 5. 基变换与proper基变换定理 (Base Change and Proper Base Change Theorem)

### 平坦基变换

设 $f: X \to Y$ 是平坦态射，$g: Y' \to Y$ 是任意态射。考虑拉回图表：

```
X' = X ×_Y Y'  →  X
  ↓              ↓
Y'        →     Y
```

则对于 $X$ 上的任意层 $F$，有**平坦基变换**：
$$g^* R^i f_* F \cong R^{i} f'_* (g'^* F)$$

### Proper 基变换定理

设 $f: X \to Y$ 是紧合态射（proper morphism），$g: Y' \to Y$ 是任意态射。则对于 $Y$ 上的任意层 $F$（在适当条件下），有 **proper 基变换**：
$$g^* R^i f_* F \cong R^i f'_* (g'^* F)$$

### cdh 下降

**cdh 拓扑**（经典挠脱拓扑）是比 étale 拓扑更粗的拓扑。在 cdh 下降下，K-理论、摩尔根-斯蒂克斯上同调等具有良好的性质。

### 类比

基变换定理在 étale 上同调中的地位，等价于谱序列中的 Leray 序列在经典拓扑中的地位。它们都是将上同调计算"基变换"的工具。

---

## 6. 光滑层 (Smooth Sheaves)

### 定义

设 $X$ 是光滑概形（smooth scheme）。层 $F$ 称为 **光滑层**，如果对于任意光滑态射 $U \to X$，层 $F|_U$ 是局部常值层（local system）。

### 性质

1. 光滑层在平展下是局部同构的
2. 紧支上同调与光滑层的上同调有特殊关系
3. 庞加莱引理（Poincaré lemma）成立：
   $$H^i_{\text{ét}}(X, \mathbb{Q}_\ell) \cong H^i_{\text{Smooth}}(X, \mathbb{Q}_\ell)$$

### 与局部系统的类比

在复几何中，局部系统是局部常值层的上同调。在 étale 几何中，光滑层扮演类似角色，但需要考虑 Galois 作用。

---

## 7. 迹公式 (Trace Formula)

### Lefschetz 迹公式

设 $f: X \to X$ 是光滑、紧致簇上的态射。则其不动点集 $X^f$ 的结构由迹公式描述：

$$\sum_{i=0}^{2d} (-1)^i \text{Tr}(f^* | H^i_{\text{ét}}(X, \mathbb{Q}_\ell)) = \sum_{x \in X^f} \text{Tr}(T_x f | \Omega_{X,x})$$

### Weil 猜想与 Deligne 定理

**Weil 猜想**（1949）关于代数簇上 zeta 函数：
$$\zeta(X, t) = \frac{P_1(t) P_3(t) \cdots P_{2d-1}(t)}{P_0(t) P_2(t) \cdots P_{2d}(t)}$$

其中 $P_i(t) = \det(1 - t \cdot \text{Frob}_q | H^i_{\text{ét}}(X, \mathbb{Q}_\ell))$。

**Deligne 的贡献**（1974）包括：
1. **有理性**：$\zeta(X, t)$ 是有理函数
2. **函数方程**：存在泛函方程 $\zeta(X, q^{-d} t^{-1}) = \pm q^{d \chi/2} \zeta(X, t)$
3. **黎曼假设**：$\zeta(X, t)$ 的零点和极点满足 $|t| = q^{-i/2}$

### 迹公式的计算

在实际计算中，迹公式将全局上同调信息（难以计算）与局部不动点信息（相对容易计算）联系起来。

---

## 模块使用示例

```python
from lean4py.etale_cohomology import (
    EtaleSite, EtaleCohomologyGroup, BaseChange, WeilConjectures
)

# 创建 étale site
site = EtaleSite("Spec(k)")
print(site.topology())  # {"type": "etale_topology"}

# 计算 étale 上同调群
H = EtaleCohomologyGroup.compute("X", "F", 1)
print(H)  # {"group": "0", "degree": 1, "scheme": "X"}

# 检查有限性
EtaleCohomologyGroup.is_finite("X", "F", 2)  # True

# 基变换检查
BaseChange.flat_base_change("X", "f")  # True
BaseChange.is_cdh_descendable()  # True

# Weil 猜想验证
WeilConjectures.rationality("X", "zeta")  # True
WeilConjectures.riemann_hypothesis("X")  # True
```

---

## 参考资料

- Grothendieck, A., et al. *Théorie des Topos et Cohomologie Étale des Schémas*. SGA 4. Springer, 1972.
- Milne, J. S. *Étale Cohomology*. Princeton University Press, 1980.
- Deligne, P. *La conjecture de Weil*. Publications Mathématiques de l'IHÉS, 1974.
- Hartshorne, R. *Algebraic Geometry*. Springer, 1977.

---

*本文档由 lean4py 自动生成，对应 mathlib4 的 `Mathlib.AlgebraicGeometry.EtaleCohomology` 模块。*