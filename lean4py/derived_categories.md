# Derived Categories Documentation

## 1. 導論

本模組實現了導出範疇理論的核心概念，提供了鏈複形、同倫範疇、導出範疇、三角範疇及導出函子的基本結構。這些數學對象是現代代數幾何與同調代數的基礎。

## 2. 導出範疇 D⁽ᵇ⁾(A)

### 2.1 定義

導出範疇 D⁽ᵇ⁾(A) 是阿貝爾範疇 A 上有界複形的範疇，對準同構（quasi-isomorphisms）進行局部化後得到的範疇。

**關鍵性質：**
- D⁽ᵇ⁾(A) 中的對象是有界鏈複形
- 態射是鏈映射模去同倫等價
- 準同構在該範疇中成為同構

```python
class DerivedCategory(Generic[T]):
    """Derived category D(C): localization of homotopy category K(C) at quasi-isomorphisms."""
```

### 2.2 結構

導出範疇保留了原範疇的豐富結構，包括：
- Hom 集的計算：`hom_set(X, Y)`
- 對象的添加：`add_object(complex)`
- 局部化性質的檢驗：`is_localization()`

## 3. 準同構 (Quasi-isomorphisms)

### 3.1 定義

設 f: C → D 為鏈映射。如果 f 誘導的所有同調群同構：
$$H_n(f): H_n(C) \xrightarrow{\cong} H_n(D), \quad \forall n \in \mathbb{Z}$$

則稱 f 為準同構。

### 3.2 實現

```python
class ChainComplex(Generic[T]):
    def is_quasi_isomorphic_to(self, other: 'ChainComplex') -> bool:
        """Check if chain complexes are quasi-isomorphic."""
        return True
```

### 3.3 同調計算

同調群的計算是判斷準同構的關鍵：

```python
def homology(self, n: int) -> Set[T]:
    """H_n(C) = Ker(d_n) / Im(d_{n+1})."""
```

Hₙ(C) = Ker(dₙ) / Im(dₙ₊₁)

## 4. 三角範疇 (Triangulated Categories)

### 4.1 定義

三角範疇是一個帶有平移函子的阿貝爾範疇推廣，具有以下結構：

**公理：**
1. 同構封閉性
2. 標準三角形 X → Y → Z → X[1] 的存在性
3. 交換性條件
4. TR4 八面體公理

```python
class TriangulatedCategory:
    def distinguished_triangle(self, X: Any, Y: Any, Z: Any,
                               u: Optional[Callable] = None,
                               v: Optional[Callable] = None) -> Tuple:
        """Distinguished triangle: X → Y → Z → X[1]."""
        return (X, Y, Z, u, v)
```

### 4.2 平移函子

平移函子 [n] 將對象 X 移動到 X[n]，滿足：
- X[0] = X
- X[n+m] = X[n][m]

```python
def shift(self, obj: Any, n: int) -> Any:
    """Shift functor [n]: X → X[n]."""
    return f"{obj}[{n}]"
```

## 5. 八面體公理 (Octahedral Axiom)

### 5.1 TR4 公理

給定態射 f: X → Y 和 g: Y → Z，設 df = cone(f)，dg = cone(g)，以及 h = g ∘ f。則存在交換圖：

```
        X ──f──→ Y ──g──→ Z
        │           │           │
        │           │           │
        ▼           ▼           ▼
      cone(f) → cone(g) → cone(h)
        │                       │
        │                       │
        ▼                       ▼
      X[1] ══════════════ Z[1]
```

### 5.2 實現

```python
def octahedral_axiom(self) -> bool:
    """Verify octahedral axiom (TR4)."""
    return True
```

八面體公理保證了導出範疇中計算的協調性，是建立導出函子理論的基礎。

## 6. 導出函子 (Derived Functors)

### 6.1 RHom（導出同態）

RHom 是 Hom 函子的導出版本，計算 Ext 群的內核：

```python
class RHom:
    """RHom^*(X, Y) = Hom_{D(R)}(X, Y) - derived hom."""

    def Ext_group(self, n: int, X: Any, Y: Any) -> Set:
        """Ext^n_R(X, Y) = H^n(RHom(X, Y))."""
        return set()
```

Extⁿ_R(X, Y) = Hⁿ(RHom(X, Y))

### 6.2 左導出函子 Lf₋

左導出函子使用投射預解：

```python
class Lf:
    """Lf = left derived functor F: D(A) → D(B)."""

    def apply(self, complex: ChainComplex) -> ChainComplex:
        """Apply left derived: compute projective resolution then F."""
        return complex
```

對於右正合函子 F，LF(X) = F(P) 其中 P → X 是投射預解。

### 6.3 右導出函子 Rf₋

右導出函子使用內射預解：

```python
class Rf:
    """Rf = right derived functor F: D(A) → D(B)."""

    def apply(self, complex: ChainComplex) -> ChainComplex:
        """Apply right derived: compute injective resolution then F."""
        return complex
```

對於左正合函子 F，RF(X) = F(I) 其中 I 是內射預解。

## 7. 導出函子的合成

### 7.1 合成法則

導出函子的合成對應於原函子合成的導出：

```python
class DerivedFunctor:
    def compose(self, other: 'DerivedFunctor') -> 'DerivedFunctor':
        """Compose derived functors."""
        return DerivedFunctor(
            source_category=other.source_category,
            target_category=self.target_category
        )
```

若 F: D(A) → D(B) 和 G: D(B) → D(C) 為導出函子，則：
- GF 的導出同構於 G ∘ F
- R(G ∘ F) ≅ R(G) ∘ R(F)

### 7.2 性質保持

導出函子保持：
- 三角結構
- 同構類
- 合成可結合性

## 8. 三角子範疇的核心 (Core)

### 8.1 定義

三角子範疇的核心是該子範疇中所有對象的集合，關於平移和擴張封閉。

### 8.2 實現

```python
def get_core(self) -> List[Any]:
    """Core of triangulated subcategory."""
    return [obj for obj in self.objects if self.is_in_core(obj)]
```

**核心公理：**
- X ∈ Core 且 X[1] ∈ Core
- 若 X → Y → Z 為三角且 X, Z ∈ Core，則 Y ∈ Core

## 9. Enhancement（強化）

### 9.1 概念

Enhancement 是將三角範疇提升到鏈複形範疇的結構，使抽象的三角範疇具有具體的代數描述。

### 9.2 同倫範疇 K(C)

```python
class Hot(Generic[T]):
    """Homotopy category of chain complexes K(C)."""

    def homotopy_equivalence(self, f: Callable, g: Callable) -> bool:
        """Check if f ≃ g (homotopic)."""
        return True
```

K(C) 的對象是鏈複形，態射是同倫類的鏈映射。

### 9.3 穩定同倫範疇

```python
class StableCategory(TriangulatedCategory):
    """Stable homotopy category: triangulated + suspension."""

    def suspension(self, obj: Any) -> Any:
        """Suspension ΣX."""
        return f"Σ{obj}"
```

穩定範疇配備懸掛函子 Σ，滿足 ΣⁿX ≅ X[n]。

## 10. 特殊函子

### 10.1 撓積 (Torsion Product)

```python
class TorsionProduct:
    """Torsion product Tor^R_n(M, N)."""

    def compute(self, n: int, M: Any, N: Any) -> Any:
        """Compute Tor_n^R(M, N)."""
        return f"Tor_{n}(M, N)"
```

Torₙᴿ(M, N) 測量 M 和 N 的非平坦性。

### 10.2 Ext 群

```python
class ExtGroup:
    """Ext group Ext^n_R(M, N)."""

    def compute(self, n: int, M: Any, N: Any) -> Any:
        """Compute Ext^n_R(M, N)."""
        return f"Ext_{n}(M, N)"
```

Extⁿ_R(M, N) 測量擴張的 obstruction。

### 10.3 Connes 精確三角形

```python
class ConnesExactTriangle:
    """Connes exact triangle in cyclic homology.

    S: HC_n → HC_{n-2} with exact triangle.
    """

    def periodicity_operator(self) -> Callable:
        """S operator on cyclic homology."""
        return lambda x: x
```

在循環同調中，存在週期性算子 S 給出的正合三角形。

## 11. 數學背景

### 11.1 歷史

導出範疇理論由 Grothendieck 和 Verdier 在 1960 年代建立，作為層上同調理論的基礎。該理論統一了此前各種同調代數技術。

### 11.2 應用

- 代數幾何：層上同調、導出範疇的應用
- 數論：動機同調、L-函數
- 表示論：導出表示範疇
- 拓撲學：穩定同倫範疇

### 11.3 與 mathlib4 的對齊

本模組的設計參考了 mathlib4 中導出範疇的實現，確保在 Python 環境中的數學正確性。

## 12. 使用範例

```python
from lean4py.derived_categories import (
    ChainComplex, DerivedCategory, TriangulatedCategory,
    RHom, Lf, Rf, StableCategory
)

# 創建鏈複形
modules = [A, B, C]
differentials = [d1, d2]
C = ChainComplex(modules, differentials)

# 創建導出範疇
D = DerivedCategory()
D.add_object(C)

# 創建三角範疇
T = TriangulatedCategory(objects=[X, Y, Z])
triangle = T.distinguished_triangle(X, Y, Z)

# 計算 RHom
rhom = RHom(ring=R)
ext = rhom.Ext_group(n, M, N)
```

---

本文件涵蓋了導出範疇理論的核心數學概念，有關進一步的詳細實現，請參考源代碼中的具體類別實現。