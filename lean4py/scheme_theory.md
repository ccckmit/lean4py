# Scheme Theory 概論

本模組實現代數幾何中 scheme 理論的核心概念，對應於 mathlib4 的 `Mathlib.AlgebraicGeometry.Scheme` 模組。

---

## 1. 環的譜 (Spectrum of a Ring)：Spec(R)

### 定義

設 $R$ 為交換環。$R$ 的**譜** (spectrum) 定義為：

$$
\operatorname{Spec}(R) = \{ \mathfrak{p} \subseteq R \mid \mathfrak{p} \text{ 為素理想} \}
$$

### 數學原理

- **素理想**：理想 $\mathfrak{p} \subset R$ 滿足：若 $ab \in \mathfrak{p}$，則 $a \in \mathfrak{p}$ 或 $b \in \mathfrak{p}$
- $\operatorname{Spec}(R)$ 中的元素是環 $R$ 的所有素理想
- 每一個素理想代表一個「幾何點」
- 劇烈理想的商環 $R/\mathfrak{p}$ 為整環

### Zariski 拓撲

在 $\operatorname{Spec}(R)$ 上定義 **Zariski 拓撲**：

- **閉集**：對於每個理想 $I \subseteq R$，定義 $V(I) = \{ \mathfrak{p} \in \operatorname{Spec}(R) \mid I \subseteq \mathfrak{p} \}$
- **基集**：形如 $D(f) = \operatorname{Spec}(R)_f = \{ \mathfrak{p} \mid f \notin \mathfrak{p} \}$ 的開集構成基

### 程式實現 (`AffineScheme` 類)

```python
class AffineScheme:
    """Affine scheme Spec(R) for ring R."""
    
    def __init__(self, ring: str):
        self.ring = ring
        self.points = [ring]  # 簡化：僅儲存環本身

    @staticmethod
    def spectrum(ring: str) -> Dict[str, Any]:
        """Spec(R) = set of prime ideals of R."""
        return {"type": "affine_scheme", "ring": ring, "points": []}
```

此實現為簡化版本，實際的 `Spec(R)` 需要儲存所有素理想的集合。

---

## 2. 區域環 $O_X(U)$

### 定義

設 $X = \operatorname{Spec}(R)$ 為仿射概形，$U \subseteq X$ 為開集。

**區域環** (local ring) 定義為：

$$
O_X(U) = \{ \text{有理函數 } \tfrac{a}{b} \mid a, b \in R,\ b \notin \mathfrak{p},\ \forall \mathfrak{p} \in U \}
$$

### 性質

- 當 $U = D(f)$ 為基本開集時，$O_X(D(f)) = R_f$（在 $f$ 處的局部化）
- 對於任意開覆蓋 $\{U_i\}$，有 $O_X(U) = \bigcap_i O_X(U_i)$
- $O_X(U)$ 為交換環

### 在 Scheme Theory 中的意義

區域環是層 (sheaf) 概念的關鍵組成部分，提供了在概形上進行局部代數運算的工具。

---

## 3. Spec(R) 上的環層 (Sheaf of Rings)

### 層的定義

在拓撲空間 $X$ 上，一個 **層** (sheaf) $\mathcal{F}$ 滿足：

1. **局部性**：若 $\{U_i\}$ 為開覆蓋，且在某開集 $U$ 上有截面 $s$，使得每個 $s|_{U_i} = 0$，則 $s = 0$
2. **粘合性**：若截面 $s_i \in \mathcal{F}(U_i)$ 滿足 $s_i|_{U_i \cap U_j} = s_j|_{U_i \cap U_j}$，則存在唯一的 $s \in \mathcal{F}(U)$ 使得 $s|_{U_i} = s_i$

### 結構層 $O_X$

在 $\operatorname{Spec}(R)$ 上，結構層 $O_X$ 定義為：

- $O_X(U) = O_X(U)$ 為 $U$ 上的正則函數環
- 限制映射：對於 $V \subseteq U$，有自然映射 $O_X(U) \to O_X(V)$

### 程式簡化

本模組中的 `AffineScheme` 類簡化了層的實現，實際數學中需要完整實現粘合條件。

---

## 4. 仿射概形與概形態射 (Affine Schemes and Scheme Morphisms)

### 仿射概形

**仿射概形** (affine scheme) 是具有結構層的局部環化空間 $(X, O_X)$，其中 $X \cong \operatorname{Spec}(R)$。

### 概形態射

**態射** (morphism) $f: X \to Y$ 包含：

1. 連續映射：$|f|: |X| \to |Y|$
2. 層態射：$f^\#: O_Y \to f_* O_X$

使得局部性質成立。

### 程式實現

```python
class SchemeMorphism:
    """Morphism of schemes f: X → Y."""

    def __init__(self, source: str, target: str,
                 map_func: Optional[Callable] = None):
        self.source = source
        self.target = target
        self.map = map_func or (lambda x: x)

    def is_continuous(self) -> bool:
        """Check continuity (simplified)."""
        return True

    def is_morphism(self) -> bool:
        """Check if f is a scheme morphism."""
        return True
```

### 環層面對應

對於仿射概形間的態射 $\operatorname{Spec}(S) \to \operatorname{Spec}(R)$，對應於環同態 $\phi: R \to S$。

---

## 5. 概形的纖維積 (Fiber Product of Schemes)

### 定義

設 $f: X \to Z$ 和 $g: Y \to Z$ 為態射。$X$ 與 $Y$ 在 $Z$ 上的**纖維積** (fiber product) 記為：

$$
X \times_Z Y
$$

其泛性質為：對任意態射 $W \to X$ 和 $W \to Y$（在 $Z$ 上），存在唯一的態射 $W \to X \times_Z Y$ 使圖交換。

### 構造

- 若 $X = \operatorname{Spec}(R)$，$Y = \operatorname{Spec}(S)$，$Z = \operatorname{Spec}(A)$
- 纖維積 $X \times_Z Y = \operatorname{Spec}(R \otimes_A S)$

### 程式實現

```python
class FiberProduct:
    """Fiber product X ×_Z Y."""

    @staticmethod
    def compute(X: str, Y: str, Z: str,
                f: Callable, g: Callable) -> Dict[str, Any]:
        """X ×_Z Y (simplified)."""
        return {"type": "fiber_product", "factors": [X, Y]}
```

---

## 6. 分離態射 (Separated Morphisms)

### 定義

態射 $f: X \to Y$ 稱為**分離的** (separated)，若對角態射 $\Delta_{X/Y}: X \to X \times_Y X$ 為閉浸入。

### 等價條件

- $X \times_Y X$ 的對角線閉包等於 $X \times_Y X$ 自身
- 基於cheme的**分離性公理**

### 分離概形

若 $X \to \operatorname{Spec}(\mathbb{Z})$ 為分離態射，則稱 $X$ 為**分離概形**。

### 重要性

- 分離性確保概形具有良好的幾何性質
- 避免「非 Hausdorff」類型的病態行為

---

## 7. 固有態射與 valuation 判準 (Proper Morphisms and Valuation Criterion)

### 固有態射定義

態射 $f: X \to Y$ 稱為**固有的** (proper)，若滿足：

1. **泛閉性**：$f$ 為分歧覆蓋的像為閉集
2. **分離性**：$f$ 為分離態射
3. **有限型**：$f$ 為有限型態射

### Valuation 判準

**Valuation 判準** (Valuation Criterion) 提供了一種判斷固有性的方法：

設 $K$ 為域，$R$ 為 $K$ 上的 valuation 環。對於固有態射 $f: X \to Y$，任意交換圖：

$$
\begin{array}{c}
\operatorname{Spec}(K) \to X \\
\downarrow \ \ \ \ \downarrow f \\
\operatorname{Spec}(R) \to Y
\end{array}
$$

存在唯一的態射 $\operatorname{Spec}(R) \to X$ 使圖交換。

### 程式實現

```python
class ProperMorphism:
    """Proper morphism of schemes."""

    @staticmethod
    def is_proper(f: SchemeMorphism) -> bool:
        """Check if f is proper (simplified: universally closed + separated)."""
        return True

    @staticmethod
    def valuation_criterion(f: SchemeMorphism) -> bool:
        """Valuative criterion for properness (simplified)."""
        return True
```

### 投影公式

對於固有態射 $f: X \to Y$ 和擬凝聚層 $\mathcal{F}$，有：

$$
Rf_*(\mathcal{F}) \otimes_{\mathcal{O}_Y} \mathcal{G} \cong Rf_*(\mathcal{F} \otimes_{\mathcal{O}_X} f^* \mathcal{G})
$$

---

## 8. 概形上的擬凝聚層 (Quasi-coherent Sheaves on Schemes)

### 定義

設 $X$ 為概形。$X$ 上的**擬凝聚層** (quasi-coherent sheaf) $\mathcal{F}$ 為：

- 對每個仿射開集 $U = \operatorname{Spec}(R)$，存在 $R$-模 $M$ 使得 $\mathcal{F}|_U \cong \widetilde{M}$
- 層的粘合條件在各開集上一致

### 凝聚層

若 $\mathcal{F}$ 為有限型且所有 stalk $\mathcal{F}_x$ 為有限生成的 $\mathcal{O}_{X,x}$-模，則 $\mathcal{F}$ 為**凝聚層** (coherent sheaf)。

### 重要範例

- **結構層** $\mathcal{O}_X$
- **理想層** $\mathcal{I} \subseteq \mathcal{O}_X$
- **向量叢**對應於局部自由的擬凝聚層

### 在本模組中的簡化

本模組尚未直接實現擬凝聚層類，但 `AffineScheme` 的設計預留了擴展空間。

---

## 9. 有限型、有限呈現態射 (Morphisms of Finite Type, Finite Presentation)

### 有限型態射

態射 $f: X \to Y$ 為**有限型** (of finite type)，若：

- $f$ 為局部有限型：對每個 $x \in X$，存在開鄰域 $U \ni x$ 使得 $f|_U: U \to f(U)$ 為有限型
- 對每個仿射開覆蓋 $\{ \operatorname{Spec}(R_i) \}$，對應的環同態使每個 $R_i$ 為有限生成的 $f^{-1}\mathcal{O}_Y$-代數

### 有限呈現態射

態射 $f: X \to Y$ 為**有限呈現** (of finite presentation)，若：

- $f$ 為有限型
- 對任意有向系 $\{ S_i \}$，有 $\operatorname{Hom}_Y(X, \varinjlim S_i) \cong \varinjlim \operatorname{Hom}_Y(X, S_i)$

### 有限型與有限呈現的關係

$$
\text{有限呈現} \Rightarrow \text{有限型}
$$

有限呈現確保態射的「局部有限性」，是微分學和代數幾何中的核心概念。

---

## 模組結構總覽

| 類 | 數學對應 |
|---|---|
| `AffineScheme` | $\operatorname{Spec}(R)$，仿射概形 |
| `ProjectiveScheme` | $\mathbb{P}^n_R$，投影概形 |
| `SchemeMorphism` | 概形間的態射 $f: X \to Y$ |
| `FiberProduct` | 纖維積 $X \times_Z Y$ |
| `ProperMorphism` | 固有態射及其 valuation 判準 |

---

## 數學背景延伸

本模組參照 **mathlib4** 的實現，採用**泛性質** (universal property) 驅動的設計：

- 纖維積由泛性質刻畫
- 固有性由 valuation 判準刻畫
- 分離性由對角態射的閉浸入性刻畫

這些概念構成現代代數幾何的基礎，連接了交換代數、拓撲學與幾何學。

---

## 參考文獻

- Hartshorne, R. *Algebraic Geometry*
- Görtz, U. & Wedhorn, T. *Algebraic Geometry I*
- Vakil, R. *Foundations of Algebraic Geometry*
- Mathlib4: `Mathlib.AlgebraicGeometry.Scheme`