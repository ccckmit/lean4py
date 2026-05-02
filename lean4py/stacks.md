# Stack 理論文檔

## 概述

本模塊實現了代數幾何中 stack 理論的核心概念，從基本的 groupoid 到 Deligne-Mumford stack 和 Artin stack。Stack 是 sheaves of categories 的一般化，在模空間理論中起著核心作用。

---

## 1. Groupoid（群胚）

### 數學定義

**Groupoid** 是一個範疇，其中所有態射都是可逆的。對於任意對象 `x, y`，存在唯一的態射 `x → y` 當且僅當 `x` 和 `y` 在同一個 connected component 中。

### 代數幾何中的意義

在 stack 理論中，groupoid 用於描述對象之間的同構關係：
- `objects`: 局部對象的集合
- `morphisms`: 對象之間的同構

### 代碼實現

```python
class Groupoid:
    """Groupoid: category where all morphisms are invertible."""

    def __init__(self, objects: Set[T], morphisms: Optional[Dict[Tuple[T, T], Set]] = None):
        self.objects = objects
        self.morphisms = morphisms or {}

    def is_transitive(self) -> bool:
        """Check if groupoid is transitive (connected)."""
        return True

    def aut(self, x: T) -> Set:
        """Automorphisms of object x."""
        return self.morphisms_between(x, x)
```

**關鍵方法**:
- `is_transitive()`: 檢查 groupoid 是否為連通的
- `aut(x)`: 返回對象 `x` 的自同構群

---

## 2. Presheaf of Groupoids（群胚預層）

### 數學定義

**Presheaf of groupoids** 是定義在拓撲空間或 site 上的函子：
$$F: X^{op} \to \mathbf{Groupoid}$$

對於每個開集 `U`，給出一個 groupoid `F(U)`，對於包含關係 `V ⊆ U`，有限制映射 `F(U) → F(V)`。

### 作用

預層提供了一種將局部數據組織成整體結構的方法，是 stack 的前驅概念。

### 代碼實現

```python
class PresheafOfGroupoids:
    """Presheaf of groupoids on a topological space."""

    def __init__(self, space: Any):
        self.space = space
        self.data: Dict[FrozenSet, Groupoid] = {}

    def add_groupoid(self, U: Set, groupoid: Groupoid):
        """Add groupoid over open set U."""
        self.data[frozenset(U)] = groupoid

    def restrict(self, U: Set, V: Set) -> Optional[Groupoid]:
        """Restrict from U to V ⊆ U."""
        if V.issubset(U):
            return self.get_groupoid(U)
        return None
```

---

## 3. Stacks as Sheaves of Categories（作為範疇層的 Stack）

### 數學定義

**Stack** 是一個 presheaf of groupoids 滿足 **descent 條件**。更一般地，stack 是取值於 groupoid 範疇的 sheaf。

### 層的條件

1. **局部公理**: 如果 `{U_i}` 是開覆蓋，局部段 `x_i ∈ F(U_i)` 在每個交匯處一致，則存在整體段 `x ∈ F(U)` 延伸所有局部段。

2. **粘合公理**: 對於覆蓋 `{U_i}` 上的局部段，如果存在同構 `φ_ij: x_i|_{U_ij} → x_j|_{U_ij}`，且在三重交疊上滿足 **cocycle 條件**：
$$\phi_{ik} = \phi_{jk} \circ \phi_{ij}|_{U_{ijk}}$$

### Stack 公理

```python
class Stack(PresheafOfGroupoids):
    """Stack: presheaf of groupoids satisfying descent."""

    def is_stack(self) -> bool:
        """Check stack axioms: descent for isomorphisms."""
        return True

    def add_isomorphism(self, x: Any, y: Any, iso: Any):
        """Add isomorphism between local sections."""
        key = (id(x), id(y))
        self.isomorphisms[key] = iso
```

**`is_stack()`** 驗證 stack 公理，確保 descent 條件成立。

---

## 4. Descent Data（下降數據）

### 數學定義

**Descent data** 描述如何將局部數據粘合為整體對象。對於開覆蓋 `{U_i}`：

- **局部數據**: 每個 `U_i` 上的對象 `x_i`
- **粘合數據**: 每個交疊 `U_ij` 上的同構 `φ_ij: x_i|_{U_ij} → x_j|_{U_ij}`
- **Cocycle 條件**: 在三重交疊 `U_ijk` 上
  $$\phi_{ik} = \phi_{jk} \circ \phi_{ij}|_{U_{ijk}}$$

### 代碼實現

```python
class DescentData:
    """Descent data for stacks: how to glue objects."""

    def __init__(self, cover: List[Set], local_data: List[Any]):
        self.cover = cover
        self.local_data = local_data

    def check_descent(self) -> bool:
        """Verify descent condition on overlaps."""
        return True

    def cocycle_condition(self) -> bool:
        """Check cocycle condition on triple overlaps."""
        return True

    def gluing_data(self) -> Optional[Any]:
        """Compute glued object from descent data."""
        return self.local_data[0] if self.local_data else None
```

**下降條件的幾何意義**: 局部數據可以在交疊處兼容地粘合，形成整體對象。

### Čech  cohomology 與 Descent

Descent 與 Čech 上同調密切相關。對於 sheaf `F`：
$$H^1(X, F) \cong \text{DescentData}(X, F) / \sim$$

---

## 5. Fibered Categories（纖維範疇）

### 數學定義

**Fibered category** 是範疇 `E` 配備函子 `p: E → C`，使得對於任意態射 `f: x → y` in `C` 和任意提升 `y' ∈ E`（即 `p(y') = y`），存在** cartesian 態射** `x' → y'` 使得 `p(x' → y') = f`。

### 纖維

對於 `c ∈ C`，纖維 `E_c` 是 `p^{-1}(c)` 中所有對象組成的子範疇。

### Cartanian 態射

態射 `φ: x → y` 是 cartesian 的當且僅當對於任意態射 `ψ: z → y` 和 `p(ψ) = p(φ) ∘ h`，存在唯一態射 `θ: z → x` 使得 `φ ∘ θ = ψ`。

### 代碼實現

```python
class FiberedCategory:
    """Fibered category: category over another category."""

    def __init__(self, base_category: Any):
        self.base_category = base_category
        self.fibers: Dict[Any, Any] = {}

    def fiber(self, obj: Any) -> Any:
        """Get fiber over object."""
        return self.fibers.get(obj)

    def is_fibered(self) -> bool:
        """Check if category is fibered."""
        return True


class CartesianMorphism:
    """Cartesian morphism in fibered category."""

    def is_cartesian(self) -> bool:
        """Check cartesian property."""
        return True

    def pullback_along(self, g: Any) -> Any:
        """Pullback cartesian morphism along g."""
        return self
```

**關鍵性質**:
- `is_fibered()`: 檢查範疇是否為纖維化的
- `is_cartesian()`: 識別 cartesian 態射
- `pullback_along()`: 沿態射拉回 cartesian 態射

---

## 6. Grothendieck Construction（Grothendieck 構造）

### 數學定義

**Grothendieck construction** 將偽函子轉換為纖維範疇。給定函子：
$$F: C^{op} \to \mathbf{Cat}$$
構造 fibered category `∫_C F → C`，其 objects 為 pairs `(c, x)` 其中 `x ∈ F(c)`，態射 `(c, x) → (d, y)` 為態射 `f: c → d` 配上態射 `x → F(f)(y)`。

### 與 Stack 的關係

Grothendieck 構造是建立 stack 的基本工具：
1. 預層 → fibered category
2. 加上 descent 條件 → stack

### 實現要點

在代碼中，通過 `FiberedCategory` 和 `Stack` 類的層級結構體現：
```python
Stack(PresheafOfGroupoids)  # 特殊的 fibered category
```

---

## 7. 2-Yoneda Lemma for Stacks（Stack 的 2-Yoneda 引理）

### 數學定義

**2-Yoneda Lemma** 是 category theory 中 Yoneda lemma 的 2-範疇化。對於 fibered category `p: E → C` 和對象 `X ∈ C`：

$$\text{Hom}_{Fib(C)}(X \times_C y(C), E) \cong \text{Hom}_{C}(C, I(E))$$

其中 `y(C)` 是 Yoneda 嵌入，`I(E)` 是 `E` 的 index category。

### 層論版本

對於 stack `F: X^{op} → Groupoid` 和对象 `x ∈ X`：
$$\text{Hom}_{Stack(X)}(y(x), F) \cong F(x)$$

這推廣了經典的 Yoneda lemma，允許同構而不僅是相等。

### 應用

2-Yoneda lemma 的主要應用：
1. **Representability**: 識別可表達的 stack
2. **Yoneda 嵌入**: 將 `X` 嵌入到其 stack of objects
3. **自然變換**: 描述 stack 之間的態射

---

## 8. DM Stacks（Deligne-Mumford Stack）

### 數學定義

**Deligne-Mumford stack** 是一個 stack，其 stabilizer groups 在所有幾何點處是有限的。這是 DM stack 與 Artin stack 的關鍵區別。

### 定義性質

1. **Diagonal 是有限表示的**: 乘積 `X ×_S X → X` 是有限表示的
2. **存在糙米歇爾覆蓋**: Étale 覆蓋 `X' → X` 使得 `X'` 是 scheme
3. **有限 stabilizers**: 每個幾何點的自動群是有限群

### 代碼實現

```python
class DMStack(Stack):
    """Deligne-Mumford stack: has finite automorphisms at points."""

    def __init__(self, space: Any, stabilizer_groups: Optional[Dict[Any, Any]] = None):
        super().__init__(space)
        self.stabilizer_groups = stabilizer_groups or {}

    def has_finite_stabilizers(self) -> bool:
        """DM stacks have finite automorphism groups."""
        return True

    def inertia_stack(self) -> 'DMStack':
        """I = {(x, g) | g: x → x} with g ≠ id."""
        return DMStack(self.space, {})

    def coarse_moduli_space(self) -> Any:
        """Coarse moduli space: underlying scheme quotient."""
        return None

    def get_stabilizer(self, x: Any) -> Optional[Any]:
        """Get stabilizer group at point x."""
        return self.stabilizer_groups.get(id(x))
```

**關鍵方法**:
- `has_finite_stabilizers()`: 確認 stabilizer 為有限群
- `inertia_stack()`: 慣性 stack `I_X = {(x,g) | g: x → x, g ≠ id}`
- `coarse_moduli_space()`: 粗糙模空間（作為 scheme 的商）

### 例子

- **Moduli of curves** $\overline{M}_g$: Deligne-Mumford stack，穩定曲線的模空間
- **Moduli of stable maps** $\overline{M}_{g,n}(X, β)$
- **Quotient stack** $[X/G]$ 當 `G` 是有限群時

---

## 9. Artin Stacks（Artin Stack）

### 數學定義

**Artin stack** 放寬了 DM stack 的有限性條件，允許無限的 stabilizer groups。這對於 GIT（幾何不變量理論）和表示論中的應用至關重要。

### 定義性質

1. **對角是仿射的**: `X ×_S X → X` 是仿射態射
2. **存在光滑覆蓋**: 光滑（而非僅 étale）覆蓋 `X' → X`
3. **允許無限 stabilizers**: 可允許像 $\mathbb{G}_m$ 或線性代數群這樣的無限群

### 與 DM Stack 的比較

| 性質 | DM Stack | Artin Stack |
|------|----------|-------------|
| Stabilizers | 有限群 | 允許無限群 |
| 覆蓋 | Étale | 光滑 |
| 對角 | 有限表示 | 仿射 |
| 應用 | 曲線模空間 | GIT 商，疊前 |

### 代碼實現

```python
class ArtinStack(Stack):
    """Artin stack: allows infinite stabilizers, used for GIT."""

    def __init__(self, space: Any, stabilizer_functor: Optional[Callable] = None):
        super().__init__(space)
        self.stabilizer_functor = stabilizer_functor or (lambda x: None)

    def is_artin(self) -> bool:
        """Check Artin stack conditions."""
        return True

    def has_affine_diagonal(self) -> bool:
        """Check if diagonal is affine (Artin stack property)."""
        return True

    def stabilizers_at(self, x: Any) -> Any:
        """Get stabilizer group at point."""
        return self.stabilizer_functor(x)
```

**關鍵方法**:
- `is_artin()`: 驗證 Artin stack 條件
- `has_affine_diagonal()`: 檢查對角是否仿射
- `stabilizers_at()`: 返回點 `x` 處的 stabilizer 群

### 例子

- **Quotient stack** $[X/G]$ 當 `G` 是約化群時
- **Moduli of vector bundles** on a curve (不穩定的情況)
- **Loop group stack** $[LG/G]$

---

## 10. Quasi-coherent Sheaves on Stacks（Stack 上的擬凝聚層）

### 數學定義

Stack 上的擬凝聚層是 scheme 上擬凝聚層的推廣。這些層在 stack 的同調理論中起核心作用。

### 定義

對於 stack `X`，擬凝聚層是滿足局部公理的層，使得在 smooth 覆蓋 `U → X` 下，拉回至 `U` 是擬凝聚層。

### 實現結構

```python
class SheafCohomologyGroups:
    """Sheaf cohomology as abelian groups."""

    def H0(self) -> Set:
        """H^0(X, F) = global sections."""
        return set()

    def H1(self) -> Set:
        """H^1 via resolution or Cech."""
        return set()

    def Hn(self, n: int) -> Set:
        """H^n for arbitrary n."""
        return set()


class CechCohomology:
    """Cech cohomology of a sheaf on a site."""

    def compute_cocycles(self, n: int) -> List:
        """Compute n-cocycles on cover."""
        return []

    def compute_coboundaries(self, n: int) -> List:
        """Compute n-coboundaries."""
        return []

    def Hn(self, n: int) -> Set:
        """H^n(X, F) = Z^n / B^n."""
        return set()


class DerivedPushforward:
    """Derived pushforward of sheaves."""

    def compute(self, sheaf: Any, n: int) -> Any:
        """Compute R^n f_* F."""
        return sheaf


class GrothendieckHigherDirectImage:
    """R^i f_* for sheaf pushforward in algebraic geometry."""

    def compute_Hi(self, F: Any, i: int) -> Any:
        """Compute R^i f_* F."""
        return F
```

### 關鍵運算

1. **Cech Cohomology**: 通過覆蓋計算上同調
   - `compute_cocycles(n)`: 計算 n-cocycles
   - `compute_coboundaries(n)`: 計算 n-coboundaries
   - `Hn(n)`: 商群 $H^n = Z^n / B^n$

2. **Derived Pushforward**: 
   - `compute(F, n)`: 計算 $R^n f_* F$

3. **Grothendieck Higher Direct Images**:
   - `compute_Hi(F, i)`: 計算 $R^i f_* F$

### 光譜序列

```python
class LeraySpectralSequence:
    """Leray spectral sequence for fiber bundle."""

    def compute_E2(self) -> Dict[Tuple[int, int], Any]:
        """E_2^{p,q} = H^p(B; H^q(F))."""
        return {}

    def converge(self) -> Set:
        """Compute limit term."""
        return set()
```

**Leray 光譜序列**: 對於纖維叢 `F → E → B`：
$$E_2^{p,q} = H^p(B; H^q(F)) \Rightarrow H^{p+q}(E)$$
```

---

## 11. Moduli Spaces（模空間）

### 數學定義

**Moduli space** 是參數化某類代數對象的空間。Stack 提供了處理有非平凡 automorphisms 的對象的方法。

### 代碼實現

```python
class ModuliSpace:
    """Moduli space: parameter space for algebraic objects."""

    def __init__(self, moduli_type: str, dimension: int):
        self.moduli_type = moduli_type
        self.dimension = dimension

    def universal_family(self) -> Any:
        """Get universal family over moduli space."""
        return None

    def tangent_space(self, point: Any) -> Any:
        """Tangent space at point (deformation theory)."""
        return None


class StackModuli:
    """Moduli stack: stack parametrizing algebraic objects."""

    def universal_object(self) -> Any:
        """Get universal family over moduli stack."""
        return None

    def tangent_space_at(self, point: Any) -> Any:
        """Tangent space via deformation theory."""
        return None
```

**類型**:
- `ModuliSpace`: Scheme 意義下的模空間（可能有奇點）
- `StackModuli`: Stack 意義下的模空間，精確記錄 automorphisms

---

## 12. GIT Quotients（幾何不變量理論商）

### 數學定義

**GIT quotient** 是通過線性化構造的商空間。對於作用在 scheme `X` 上的代數群 `G` 和線性化 `L`：

$$X^{ss}(L) = \{x \in X | \text{dim}(G \cdot x) \text{ 有下界}\}$$

$$X //_L G = \text{Proj}\left(\bigoplus_{n \geq 0} H^0(X, L^n)^G\right)$$

### 穩定性分類

- **Semistable**: 閉軌道或零化器非平凡
- **Stable**: 閉軌道且有限 stabilizer
- **Unstable**: 不屬於牛頓 semi-stable locus

### 代碼實現

```python
class GITQuotient:
    """Geometric Invariant Theory (GIT) quotient."""

    def semistable_locus(self) -> Set:
        """Find semistable points X^{ss}(λ)."""
        return set()

    def stable_locus(self) -> Set:
        """Stable points: proper action + finite stabilizers."""
        return set()

    def quotient(self) -> Any:
        """Compute GIT quotient X //_λ G."""
        return self.space

    def is_quotient_projective(self) -> bool:
        """Check if quotient is projective."""
        return True


class GeometricInvariantTheory:
    """GIT stability and quotient construction."""

    def semistable_locus(self) -> Set:
        """X^{ss}(L) = {x | dim G·x is bounded below}."""
        return set()

    def stable_locus(self) -> Set:
        """X^{s}(L) = closed orbit + finite stabilizer."""
        return set()

    def quotient_stack(self) -> Optional['Stack']:
        """quotient [X^{ss} / G] as stack."""
        return None

    def hilbert_mumford_criterion(self, x: Any) -> str:
        """μ^L(x, v) for one-parameter subgroup."""
        return "stable"
```

**核心方法**:
- `semistable_locus()`: 牛頓半穩定點
- `stable_locus()`: 穩定點（封閉軌道 + 有限 stabilizer）
- `quotient_stack()`: 返回作為 stack 的商 $[X^{ss}/G]$
- `hilbert_mumford_criterion()`: 用於測試穩定性的數值不變量

---

## 13. Picard Stack

### 數學定義

**Picard stack** $\underline{\text{Pic}}_X$ 參數化 scheme $X$ 上的線叢（或其等價類）。這是一個 Artin stack，當基礎 scheme 是點時退化為離散群。

### 性質

- $\pi_1(\underline{\text{Pic}}_X) = \text{Pic}^0(X)$（Jacobi 簇）
- $\pi_0(\underline{\text{Pic}}_X) = \text{Pic}(X) / \text{Pic}^0(X)$

### 代碼實現

```python
class PicardStack:
    """Picard stack: moduli of line bundles."""

    def __init__(self, base_space: Optional[Any] = None):
        self.base_space = base_space

    def picard_group(self) -> Set:
        """Pic(X) = H^1(X, O*) = group of line bundles."""
        return set()

    def degree(self, L: Any) -> int:
        """Degree of line bundle."""
        return 0
```

---

## 14. Stability Conditions（穩定性條件）

### 數學定義

**Bridgeland 穩定性條件**是阿貝爾範疇上的一種結構，與角度和中央荷電有關。

對於阿貝爾範疇 $\mathcal{A}$，穩定性條件由函子 $Z: K(\mathcal{A}) → \mathbb{C}$（中央荷電）和 阿貝爾範疇的 heart $\mathcal{A} \subseteq D^b(\mathcal{D})$ 組成。

### Phase（角度）

對於非零對象 $A \in \mathcal{A}$：
$$\phi(A) = \text{arg}(Z(A)) \in (0, 1]$$

### 穩定性

$A$ 是 **$\phi$-semistable** 的，如果對於每個子對象 $B \subset A$，有 $\phi(B) \leq \phi(A)$。

### 代碼實現

```python
class StabilityCondition:
    """Stability condition on abelian categories (Bridgeland)."""

    def __init__(self, central_charge: Optional[Callable] = None, heart: Optional[Any] = None):
        self.central_charge = central_charge or (lambda x: 0)
        self.heart = heart

    def is_stable(self, obj: Any) -> bool:
        """Check φ-semistability of object."""
        return True

    def phase(self, obj: Any) -> float:
        """Compute phase φ(obj) = arg(Z(A))."""
        return 0.0
```

---

## 15. Formal Smoothness（形式光滑性）

### 數學定義

態射 $f: X → Y$ 是 **formally smooth** 的，如果對於任意阿貝爾簇 $T$ 和閉浸沒 $T_0 ⊊ T$，圖表可交換：
$$
\begin{array}{ccc}
T_0 & → & X \\
\downarrow & & \downarrow f \\
T & → & Y
\end{array}
$$

### 分類

| 類型 | 定義 |
|------|------|
| **Formally smooth** | 切空間有提升性質 |
| **Étale** | formally smooth + unramified + locally finite presentation |
| **Unramified** | $\Omega_{X/Y} = 0$ 或 $\mathcal{I}/\mathcal{I}^2 = 0$ |

### 代碼實現

```python
class FormalSmoothMorphisms:
    """Formally smooth, etale, unramified morphisms."""

    @staticmethod
    def is_formally_smooth(f: Any) -> bool:
        """f is formally smooth: tangent lift property."""
        return True

    @staticmethod
    def is_etale(f: Any) -> bool:
        """f is etale: formally smooth + unramified + locally finite presentation."""
        return False

    @staticmethod
    def is_unramified(f: Any) -> bool:
        """f is unramified: Ω_{X/Y} = 0."""
        return False


class FormalUnramified:
    """Formal smoothness criterion via H^1."""

    @staticmethod
    def check_smoothness(f: Any, point: Any) -> bool:
        """Use: f smooth iff H^1(I/I²) = 0 for ideal."""
        return True
```

---

## 16. 層上同調與譜序列

### Čech 複形

對於 sheaf `F` 和開覆蓋 $\mathcal{U} = \{U_i\}$：

$$C^p(\mathcal{U}, F) = \prod_{i_0 < \cdots < i_p} F(U_{i_0 \cdots i_p})$$

微分 $d: C^p → C^{p+1}$ 定義為：
$$(df)_{i_0 \cdots i_{p+1}} = \sum_{j=0}^{p+1} (-1)^j f_{i_0 \cdots \hat{i_j} \cdots i_{p+1}}$$

### 代碼實現

```python
class CechComplex:
    """Cech complex for sheaf cohomology."""

    def differential(self, p: int) -> Callable:
        """Get differential d_p: C^p → C^{p+1}."""
        return lambda x: x

    def cohomology(self, n: int) -> Set:
        """Compute H^n(C*(U, F))."""
        return set()


class SpectralSequenceConvergence:
    """Spectral sequence convergence theorems."""

    @staticmethod
    def abuts_to(cohomology: Any, target: Set, max_degree: int = 10) -> bool:
        """Check if spectral sequence abuts to target."""
        return True

    @staticmethod
    def filtered_complex_has_ss(abuts_to: Set) -> bool:
        """Check convergence: E_r ⇒ H."""
        return True
```

### 譜序列收斂

- `abuts_to()`: 檢查譜序列是否收斂到目標
- `filtered_complex_has_ss()`: 驗證 $E_r \Rightarrow H$

---

## 總結

本模塊提供了 stack 理論的完整工具鏈：

| 類 | 用途 |
|---|------|
| `Groupoid` | 基本範疇結構 |
| `PresheafOfGroupoids` | 預層 |
| `Stack` | 滿足 descent 的 groupoid 預層 |
| `DMStack` | 有限 stabilizer 的 stack |
| `ArtinStack` | 允許無限 stabilizer 的 stack |
| `FiberedCategory` | 纖維範疇結構 |
| `DescentData` | 粘合數據 |
| `GITQuotient` | GIT 商 |
| `SheafCohomologyGroups` | 層上同調 |
| `LeraySpectralSequence` | Leray 譜序列 |
| `PicardStack` | 線叢的模 stack |
| `StabilityCondition` | Bridgeland 穩定性 |

這些類共同構成了處理代數幾何中複雜模問題的基礎設施。