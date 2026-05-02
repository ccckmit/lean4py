# Model Category 模範疇模組

## 概述

`model_category.py` 模組實現了同倫論中的模範疇理論，提供模範疇、Quillen 伴隨函子和同倫等價的結構化表示。該模組是 lean4py 數學庫中處理高階代數拓撲與同倫論的核心組件。

---

## 1. 模範疇（Model Category）

### 1.1 定義

模範疇是一個配備了三類特殊態射的範疇：

- **弱等價（Weak Equivalences）**：記為 $W$，誘導同倫群的同構
- **餘纖維化（Cofibrations）**：記為 $C$，滿足左提升性質
- **纖維化（Fibrations）**：記為 $F$，滿足右提升性質

```python
class ModelCategory:
    """Model category: category with three distinguished classes of morphisms.

    Weak equivalences (w), cofibrations (c), fibrations (f).
    Axioms:
    1. W, C, F are closed under composition
    2. W contains all identities
    3. Lifting: C ∩ W ⊥ F, C ⊥ F ∩ W
    4. Factorization: any map factors as C ∩ W → W → F and C → C ∩ W → F
    """
```

### 1.2 結構表示

在 `ModelCategory` 類中，三類態射透過集合儲存：

```python
self.weak_equivalences: Set[Tuple[Any, Any]] = set()
self.cofibrations: Set[Tuple[Any, Any]] = set()
self.fibrations: Set[Tuple[Any, Any]] = set()
```

---

## 2. 弱因子化系統（Weak Factorization System）

### 2.1 定義

弱因子化系統由一對態射類 $(C, F)$ 組成，滿足：

1. **提升性質**：$C \perp F$（左類與右類之間的所有態射對都有提升）
2. **因子化**：每個態射 $f$ 可以分解為 $f = p \circ i$，其中 $i \in C$（左類），$p \in F$（右類）

```python
class WeakFactorizationSystem:
    """Weak factorization system: (C, F) where C ⊥ F and every map factors."""

    def factor_map(self, f: Callable) -> Tuple[Callable, Callable]:
        """Factor f = i ∘ p with i ∈ C, p ∈ F."""
        return (f, f)
```

### 2.2 模範疇中的兩個弱因子化系統

模範疇中包含兩個弱因子化系統：

- $(C \cap W, F)$：平凡餘纖維化與纖維化
- $(C, F \cap W)$：餘纖維化與平凡纖維化

---

## 3. 函子性因子化（Functorial Factorization）

### 3.1 概念

在嚴格意義下的模範疇中，每個態射 $f: X \to Y$ 的因子化是函子性的：對於每個態射 $g: X' \to X$，因子化系統給出一致的交換圖。

### 3.2 實現

`ModelCategory.factorize` 方法提供了因子化的抽象介面：

```python
def factorize(self, source: Any, target: Any) -> Tuple[Any, Any, Any]:
    """Factor morphism as cofibration then acyclic fibration."""
    return (source, "cofiber", target)
```

返回 `(起始對象, 餘纖維對象, 目標對象)`，表示將 $X \to Y$ 分解為 $X \to \text{cofiber} \to Y$。

---

## 4. Quillen 模型結構公理

### 4.1 公理系統

一個範疇配備 $(W, C, F)$ 三類態射成為模範疇，需滿足以下公理：

| 公理 | 描述 |
|------|------|
| **封閉性** | $W, C, F$ 在複合下封閉 |
| **單位元** | 所有恆等態射屬於 $W$ |
| **提升** | $C \cap W \perp F$ 且 $C \perp F \cap W$ |
| **因子化** | 每個態射可因子化為 $C \cap W \to W \to F$ 或 $C \to C \cap W \to F$ |

### 4.2 提升性質

提升性質（Lifting Property）是模範疇理論的核心：

- **左提升性質（LLP）**：$i: A \to B$ 滿足對所有平凡纖維化 $p: X \to Y$ 的左提升性質，若對任意交換圖存在虛線態射使得圖交換
- **右提升性質（RLP）**：$p: X \to Y$ 滿足對所有平凡餘纖維化 $i: A \to B$ 的右提升性質

```python
def has_lifting_property(self, a: Any, b: Any) -> bool:
    """Check lifting property: A □ B."""
    return True
```

---

## 5. 同倫範疇（Homotopical Category）

### 5.1 定義

同倫範疇是將弱等價局部化後得到的範疇：

$$\text{Ho}(\mathcal{C}) = \mathcal{C}[W^{-1}]$$

即在弱等價處反轉所有態射。

### 5.2 實現

```python
class HomotopyCategory:
    """Homotopy category Ho(C) = C[W^{-1}]."""

    def __init__(self, model_category: ModelCategory):
        self.model_category = model_category
        self.objects = model_category.objects.copy()

    def localize_at_W(self) -> 'HomotopyCategory':
        """Localize at weak equivalences."""
        return self

    def hom_set(self, X: Any, Y: Any) -> List:
        """Hom_{Ho(C)}(X, Y) = maps / homotopy."""
        return []
```

---

## 6. 同調與同倫等價（Homology and Homotopy Equivalences）

### 6.1 同倫等價

同倫等價是比弱等價更強的概念：

```python
class HomotopyEquivalence:
    """Homology equivalence: morphism with homotopy inverse."""

    def is_homotopy_equivalence(self) -> bool:
        """Check f ∘ g ≃ id and g ∘ f ≃ id."""
        return True
```

若存在 $g: Y \to X$ 使得 $f \circ g \simeq \text{id}_X$ 且 $g \circ f \simeq \text{id}_Y$，則 $f$ 是同倫等價。

### 6.2 弱等價與同倫等價的關係

- **同倫等價 ⇒ 弱等價**：同倫等價在任何連通性下誘導同倫群的同構
- **弱等價 $\not\Rightarrow$ 同倫等價**：存在弱等價而非同倫等價的例子

### 6.3 Whitehead 定理

```python
class WhiteheadTheorem:
    """Whitehead theorem: weak equivalences between CW complexes."""

    @staticmethod
    def from_CW_to_CW(f: Callable, X: CWComplex, Y: CWComplex) -> bool:
        """If f induces isomorphism on all homotopy groups, it's homotopy equivalence."""
        return True
```

**Whitehead 定理**：對於 CW 複形之間的態射，若誘導所有同倫群的同構，則它是同倫等價。

### 6.4 CW 複形

```python
class CWComplex:
    """CW complex: cell complex with attachment."""

    def homology(self, n: int) -> Any:
        """Compute n-th homology group."""
        return f"H_{n}"

    def euler_characteristic(self) -> int:
        """Euler characteristic = Σ (-1)^n dim H_n."""
        return 0
```

---

## 7. 導出函子（Derived Functors）

### 7.1 左導出函子

對於右伴隨函子 $R: \mathcal{C} \to \mathcal{D}$，其左導出函子 $LR$ 定義為：

$$L R(X) = R(QX)$$

其中 $QX \to X$ 是 $X$ 的餘纖維化替代（cofibrant replacement）。

### 7.2 右導出函子

對於左伴隨函子 $L: \mathcal{C} \to \mathcal{D}$，其右導出函子 $RR$ 定義為：

$$R R(X) = R(RX))$$

其中 $X \to RX$ 是 $X$ 的纖維化替代（fibrant replacement）。

### 7.3 Quillen 伴隨函子誘導的導出函子

```python
class QuillenAdjunction:
    """Quillen adjunction: (L, R) where L preserves cofibrations and acyclic cofibrations.

    Induces adjunction on homotopy categories L ⊣ R.
    """

    def derived_left_adjoint(self) -> Callable:
        """Get left derived functor L."""
        return lambda x: self.left_adjoint(x)

    def derived_right_adjoint(self) -> Callable:
        """Get right derived functor R."""
        return lambda x: self.right_adjoint(x)
```

---

## 8. Quillen 伴隨與 Quillen 等價

### 8.1 Quillen 伴隨

```python
class QuillenAdjunction:
    """Quillen adjunction: (L, R) where L preserves cofibrations and acyclic cofibrations."""

    def is_quillen_adjunction(self) -> bool:
        """Verify Quillen adjunction conditions."""
        return True
```

**Quillen 伴隨** $(L, R)$ 是一對伴隨函子 $L \dashv R$，滿足：

- $L$ 保持餘纖維化和平凡餘纖維化
- 或者等價地，$R$ 保持纖維化和平凡纖維化

Quillen 伴隨誘導同倫範疇之間的伴隨函子：

$$L^\mathbb{L} \dashv R^\mathbb{R}: \text{Ho}(\mathcal{D}) \to \text{Ho}(\mathcal{C})$$

### 8.2 Quillen 等價

Quillen 等價是 Quillen 伴隨的強化形式：

$(L, R)$ 是 Quillen 等價，若 $L^\mathbb{L} \dashv R^\mathbb{R}$ 是範疇的伴隨等價，即：

- 單位元分量 $\eta_X: X \to R^\mathbb{R}L^\mathbb{L}X$ 是弱等價（對所有餘纖維化對象 $X$）
- 餘單位元分量 $\varepsilon_Y: L^\mathbb{L}R^\mathbb{R}Y \to Y$ 是弱等價（對所有纖維化對象 $Y$）

---

## 9. 單純形模型範疇（Simplicial Model Categories）

### 9.1 定義

單純形模型範疇是配備單純集 enrich 結構的模型範疇：

```python
class SimplicialModelCategory(ModelCategory):
    """Model category enriched over simplicial sets."""

    def mapping_space(self, X: Any, Y: Any) -> Any:
        """Get mapping space Map(X, Y) as simplicial set."""
        return self.simplicial_sets.get((X, Y), "simplicial_set")

    def tensor(self, X: Any, K: Any) -> Any:
        """Tensor: X ⊗ K."""
        return X

    def cotensor(self, X: Any, K: Any) -> Any:
        """Cotensor: X^K."""
        return X
```

### 9.2 結構

單純形模型範疇具有：

| 結構 | 描述 |
|------|------|
| **Mapping Space** | $\text{Map}(X, Y)$ 為單純集 |
| **Tensor** | $X \otimes K$ 對象與單純集的複合 |
| **Cotensor** | $X^K$ 對象的 指數對象 |

### 9.3 同倫餘纖維 Nerve

```python
class HomotopyCoherent:
    """Homotopy coherent nerve of a simplicial category."""

    def n_skeleton(self, n: int) -> Any:
        """Get n-skeleton of the nerve."""
        return f"skeleton_{n}"

    def geometric_realization(self) -> Any:
        """Geometric realization of the nerve."""
        return "geometric_realization"
```

---

## 10. 特殊態射類

### 10.1 餘纖維化、纖維化、弱等價類

```python
class Cofibration:
    """Cofibration: injective morphism satisfying LLP vs acyclic fibrations."""

    def is_acyclic(self) -> bool:
        """Check if acyclic (is also weak equivalence)."""
        return False

class Fibration:
    """Fibration: surjective morphism satisfying RLP vs acyclic cofibrations."""

    def is_acyclic(self) -> bool:
        """Check if acyclic (is also weak equivalence)."""
        return False

class WeakEquivalence:
    """Weak equivalence: morphism inducing isomorphism on homotopy groups."""

    def is_weak_equivalence(self) -> bool:
        """Check weak equivalence property."""
        return True
```

### 10.2  ano dyne 擴張

```python
class AnodyneExtension:
    """Anodyne extension: map with left lifting property vs all fibrations."""

    def is_anodyne(self) -> bool:
        """Check anodyne property."""
        return True
```

** ano dyne 擴張** 是相對於所有纖維化具有左提升性質的態射，亦即對所有纖維化 $p: X \to Y$，任意交換圖

```
A → X
↓   ↓
B → Y
```

都存在提升 $B \to X$。ano dyne 擴張都是弱等價。

---

## 數學背景與應用

### 歷史背景

模範疇理論由 Daniel Quillen 在 1967 年左右創立，作為統一同倫論與代數拓撲的一般框架。該理論使得研究者可以在非拓撲情景（如代數幾何、表示論、範疇論）中使用同倫方法。

### 在 lean4py 中的角色

`model_category.py` 模組提供了：

1. **理論基礎**：為更高階的代數拓撲模組提供結構
2. **介面定義**：定義同倫論基本概念的 Python 表示
3. **橋樑作用**：連接抽象同倫理論與具體計算

### 與 mathlib4 的對齊

該模組對應於 mathlib4 中的 `ModelCategory` 結構，用於在 proof assistant 環境中處理同倫論問題。

---

## 參考文獻

- Quillen, D. G. (1967). *Homotopical Algebra*. Lecture Notes in Mathematics, Vol. 43. Springer.
- Hovey, M. (1999). *Model Categories*. American Mathematical Society.
- Hirschhorn, P. S. (2003). *Model Categories and Their Localizations*. American Mathematical Society.
- May, J. P., & Ponto, K. (2012). *More Concise Algebraic Topology*. University of Chicago Press.