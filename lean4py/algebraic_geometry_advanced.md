# 代数几何进阶 / Advanced Algebraic Geometry

本文档介绍 lean4py 代数几何进阶模块的数学原理，涵盖从概形理论到 Riemann-Roch 定理的核心内容。

---

## 1. 概形 (Schemes)

### 1.1 定义

**概形**是代数几何中最基本的对象，是一种**局部赋环空间 (locally ringed space)**，局部地同构于某个交换环的谱 $\operatorname{Spec}(R)$。

一个局部赋环空间 $(X, \mathcal{O}_X)$ 满足：
- $X$ 是一个拓扑空间
- $\mathcal{O}_X$ 是 $X$ 上的环层
- 对每个点 $x \in X$，茎 $\mathcal{O}_{X,x}$ 是局部环

### 1.2 仿射概形

仿射概形 $\operatorname{Spec}(R)$ 具有以下性质：

| 组成元素 | 描述 |
|---------|------|
| 拓扑空间 | 素理想的集合，Zariski 拓扑 |
| 结构层 | 茎为局部化 $R_f$ 的层 |
| 函子性 | $\operatorname{Spec}$ 给出 $\mathbf{CRing} \to \mathbf{LRS}$ 的反变函子 |

### 1.3 模范畴与概形范畴的对偶性

**Gelfand 对偶**的代数几何类比：

$$R\text{-模} \longleftrightarrow X = \operatorname{Spec}(R)\text{上的拟凝聚层}$$

---

## 2. 概形上的层 (Sheaves on Schemes)

### 2.1 层的定义

设 $X$ 为拓扑空间。层 $\mathcal{F}$ 满足：

1. **局部性**：若 $\{U_i\}$ 是开覆盖，$s|_U = t|_U$ 对所有 $U$ 成立，则 $s = t$
2. **粘合性**：局部截面可以唯一粘合

### 2.2 茎与截面

- **茎** $\mathcal{F}_x$：在点 $x$处的所有芽的集合
- **截面** $\Gamma(U, \mathcal{F})$：开集 $U$ 上的整体截面

### 2.3 正合列

层的正合性通过茎来刻画：

$$0 \to \mathcal{F} \to \mathcal{G} \to \mathcal{H} \to 0$$

在每点茎处正合 $\iff$ 层正合。

---

## 3. 拟凝聚层 (Quasi-coherent Sheaves)

### 3.1 定义

层 $\mathcal{F}$ 为**拟凝聚层**当且仅当对每个点 $x$，存在邻域 $U = \operatorname{Spec}(A)$ 使得：

$$\mathcal{F}|_U \cong \widetilde{M}$$

其中 $M$ 是某个 $A$-模。

### 3.2 凝聚层 vs 拟凝聚层

| 类型 | 定义 | 性质 |
|-----|------|------|
| 拟凝聚 | 局部同构于某个模的相伴层 | 模范畴的层化 |
| 凝聚 | 拟凝聚 + 有限生成 + 局部由有限展示 | 类似于流形上的向量丛 |

### 3.3 Serre 定理（投影概形情形）

对于射影概形 $X = \operatorname{Proj}(S)$：

$$\Gamma_*(X, \mathcal{O}_X(1)) = \bigoplus_{d \geq 0} H^0(X, \mathcal{O}_X(d))$$

构成一个分次 $S$-代数。

---

## 4. 射影概形与 Proj 构造 (Projective Schemes & Proj)

### 4.1 Proj 构造

给定分次环 $S = \bigoplus_{d \geq 0} S_d$（$S_0 = A$，$S$ 为有限生成 $S_0$-代数），定义：

$$\operatorname{Proj}(S) = \{\mathfrak{p} \in \operatorname{Proj}(S) \mid \mathfrak{p} \text{ 为齐次素理想且不包含 } S_+\}$$

### 4.2 射影空间的层结构

$\mathbb{P}^n_A = \operatorname{Proj}(A[x_0, \ldots, x_n])$ 带有：

- **丰沛层** $\mathcal{O}(1)$
- **Serre 扭曲层** $\mathcal{O}(d)$
- 截面层 $\mathcal{O}(m)$ 的整体截面由齐次多项式给出

### 4.3 本模块中的实现

在 `algebraic_geometry_advanced.py` 中，`LineBundle` 类模拟了射影空间上的线丛：

```python
class LineBundle:
    """Line bundle O(D) associated to divisor D."""
    
    @staticmethod
    def from_divisor(D: Divisor) -> Dict[str, Any]:
        return {"bundle": "O(D)", "degree": D.degree()}
```

---

## 5. 丰沛线丛与Very Ampleness (Ample & Very Ample Line Bundles)

### 5.1 丰沛层 (Ample Sheaf)

层 $\mathcal{L}$ 为**丰沛 (ample)** 当且仅当：

$$\mathcal{L}^{\otimes n} \text{ 为整体生成，且 } X = \bigcup_{i} D^+(s_i)$$

其中 $s_i \in \Gamma(X, \mathcal{L}^{\otimes n})$ 为截面。

**判别准则**：$\mathcal{L}$ 丰沛 $\iff$ $\mathcal{O}_X(1)$ 丰沛（相对紧情形）。

### 5.2 非常丰沛层 (Very Ample Sheaf)

$\mathcal{L}$ 为**非常丰沛 (very ample)** 当且仅当：

$$\phi_{\mathcal{L}}: X \to \mathbb{P}^n$$

为闭浸入。

### 5.3 关系

$$\text{Very Ample} \implies \text{Ample} \implies \text{Nef + Big}$$

---

## 6. Serre 亲合性判别法 (Serre's Criterion for Affineness)

### 6.1 定理陈述

设 $X$ 为诺特概形。以下条件等价：

1. $X$ 是仿射的
2. $H^i(X, \mathcal{F}) = 0$ 对所有 $i > 0$ 和所有凝聚层 $\mathcal{F}$ 成立
3. $H^1(X, \mathcal{I}) = 0$ 对每个有限型理想层 $\mathcal{I}$ 成立

### 6.2 推论

- $\mathbb{A}^n$ 是仿射的（Cartan 定理 A/B）
- 射影空间 $\mathbb{P}^n$ 不是仿射的（$H^n \neq 0$）

### 6.3 应用

检验概形的仿射性：
```python
# Serre's criterion: check cohomology vanishing
def is_affine_serres_criterion(X, F):
    # For affine X: H^i(X, F) = 0 for all i > 0
    pass
```

---

## 7. 平坦态射与纤维维数 (Flat Morphisms & Fiber Dimensions)

### 7.1 平坦态射

态射 $f: X \to Y$ 为**平坦的**当且仅当：

$$\mathcal{O}_X \text{ 作为 } f^{-1}\mathcal{O}_Y\text{-模是平坦的}$$

### 7.2 等维纤维性质

若 $f$ 为平坦且局部有限型，则：

- 纤维维数局部常数（维数平坦性定理）
- 基变换公式成立：
$$R^i f_*(\mathcal{F} \otimes f^* \mathcal{E}) \cong R^i f_*(\mathcal{F}) \otimes \mathcal{E}$$

### 7.3 维数平坦性定理

若 $f: X \to Y$ 平坦，$X$ 局部等维，则：

$$\dim_x X = \dim_{f(x)} Y + \dim \text{ 纤维}(x)$$

---

## 8. 平滑态射与平展态射 (Smooth & Étale Morphisms)

### 8.1 平滑态射

态射 $f: X \to Y$ 为**$k$-光滑**当且仅当：
1. 局部有限型
2. 对每个点，存在邻域使得
$$X \cong \operatorname{Spec}(A[x_1,\ldots,x_n]/(f_1,\ldots,f_m))$$
满足 $\operatorname{rank}(\frac{\partial f_i}{\partial x_j}) = m$

### 8.2 平展态射

态射为**平展 (étale)** 当且仅当：
1. 平滑
2. 相对维数为 $0$

或等价地：
- $\Omega_{X/Y} = 0$
- $f$ 为平展 $\iff$ $f$ 为平展覆盖的局部同构

### 8.3 性质比较

| 性质 | 平滑 | 平展 |
|------|------|------|
| 定义 | Jacobi 矩阵满秩 | Jacobi 矩阵可逆 |
| 纤维 | 光滑簇 | 离散有限纤维 |
| 覆盖理论 | 一般覆盖论的基础 | Galois 覆盖论的基础 |
| 例子 | $\mathbb{A}^n \to \mathbb{A}^n$ | $\operatorname{Spec}(L) \to \operatorname{Spec}(K)$ |

---

## 9. 除子与线丛 (Divisors & Line Bundles) — 本模块核心

### 9.1 除子的定义

**除子**是余维度 1 子簇的 Weil 除子，或曲线上点的形式整系数线性组合：

$$D = \sum_{P \in X} n_P P$$

- $D$ **有效** $\iff$ 所有 $n_P \geq 0$
- **次数** $\deg(D) = \sum_P n_P$

### 9.2 线丛与除子的对应

在光滑曲线上，除子与线丛有一一对应：

$$\text{Div}(X) / \text{Prin}(X) \cong \operatorname{Pic}(X)$$

线丛 $\mathcal{O}_X(D)$ 满足：
- 截面 $s \in H^0(X, \mathcal{O}_X(D))$ 对应除子 $(s) + D \geq 0$

### 9.3 本模块实现

```python
class Divisor:
    """Divisor D = Σ n_P P on a curve."""
    
    def __init__(self, coefficients: Optional[Dict[str, int]] = None):
        self.coeffs = coefficients or {}
    
    def degree(self) -> int:
        """deg(D) = Σ n_P."""
        return sum(self.coeffs.values())
    
    def is_effective(self) -> bool:
        """All n_P ≥ 0."""
        return all(n >= 0 for n in self.coeffs.values())

class LineBundle:
    """Line bundle O(D) associated to divisor D."""
    
    @staticmethod
    def from_divisor(D: Divisor) -> Dict[str, Any]:
        """O(D) (simplified)."""
        return {"bundle": "O(D)", "degree": D.degree()}
    
    @staticmethod
    def is_isomorphic(L1: Dict, L2: Dict) -> bool:
        """L1 ≅ L2 if deg(L1) = deg(L2) (simplified)."""
        return L1.get("degree") == L2.get("degree")
```

---

## 10. Riemann-Roch 定理 (Riemann-Roch Theorem)

### 10.1 定理陈述

设 $X$ 为亏格 $g$ 的光滑射影曲线，$D$ 为除子，$K$ 为典范除子：

$$l(D) = \deg(D) + 1 - g + l(K - D)$$

其中：
- $l(D) = \dim H^0(X, \mathcal{O}_X(D))$
- $l(K - D) = \dim H^0(X, \mathcal{O}_X(K - D))$

### 10.2 几何意义

Riemann-Roch 定理给出了：
1. **截面个数的下界**：$l(D) \geq \deg(D) + 1 - g$
2. **特殊除子的分类**：当 $l(K - D) > 0$ 时 $D$ 为特殊除子

### 10.3 推论

1. **Riemann 不等式**：$l(D) \geq \deg(D) + 1 - g$
2. **Clifford 定理**：若 $0 \leq \deg(D) \leq 2g - 2$，则 $l(D) \leq \lfloor \deg(D)/2 \rfloor + 1$
3. **典范嵌入**：亏格 $g \geq 2$ 的曲线可由 $|K|$ 嵌入

### 10.4 本模块实现

```python
class RiemannRoch:
    """Riemann-Roch theorem: l(D) = deg(D) + 1 - g + l(K-D)."""
    
    @staticmethod
    def compute(D: Divisor, genus: int,
                canonical_degree: Optional[int] = None) -> int:
        """l(D) = dim L(D) (simplified: ignore l(K-D))."""
        return max(0, D.degree() + 1 - genus)
    
    @staticmethod
    def holds(D: Divisor, genus: int) -> bool:
        """Riemann-Roch holds (simplified)."""
        return True

class CanonicalDivisor:
    """Canonical divisor K = divisor of differential 1-form."""
    
    @staticmethod
    def compute(genus: int) -> Divisor:
        """K has degree 2g - 2."""
        return Divisor({f"P_{i}": 1 for i in range(2 * genus - 2)})
    
    @staticmethod
    def degree(genus: int) -> int:
        """deg(K) = 2g - 2."""
        return 2 * genus - 2

class Genus:
    """Genus of a curve."""
    
    @staticmethod
    def of_curve(degree: int) -> int:
        """g = (d-1)(d-2)/2 for smooth plane curve of degree d."""
        return (degree - 1) * (degree - 2) // 2
    
    @staticmethod
    def of_riemann_surface(genus: int) -> int:
        """g = 1 for elliptic curve, etc."""
        return genus
```

---

## 参考文献

1. Hartshorne, R. *Algebraic Geometry*. Springer, 1977.
2. Grothendieck, A. & Dieudonné, J. *Éléments de Géométrie Algébrique*. IHES, 1960-1967.
3. Liu, Q. *Algebraic Geometry and Arithmetic Curves*. Oxford, 2002.
4. Vakil, R. *Rising Sea: Foundations of Algebraic Geometry*. 2023+.
5. mathlib4 Documentation: `Mathlib/AlgebraicGeometry/`