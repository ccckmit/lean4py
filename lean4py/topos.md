# Topos 理論文檔

## 概述

本模塊實現了 Topos 理論的核心概念，包括基本 topoi、子對象分類器、阿貝爾範疇等。Topos 理論是範疇論的重要分支，連接了幾何學、邏輯學和拓撲學。

---

## 1. 基本拓撲斯（Elementary Topos）

### 定義

**基本拓撲斯**是一個滿足以下條件的範疇：

1. **有限極限存在**：包括終對象、初始對象、乘積、纖維積等
2. **指數對象存在**：作為笛卡爾封閉範疇，對任意對象 $X, Y$，指數對象 $[X, Y]$ 存在
3. **子對象分類器**：存在對象 $\Omega$ 和通用子對象 characteristic 映射 $\chi: S \rightarrow \Omega$

### 代數結構

```python
class Topos:
    def __init__(self, sheaves=None):
        self.sheaves = sheaves or []
        self.subobject_classifier = self._compute_subobject_classifier()

    def has_exponentials(self) -> bool:
        return True

    def is_cartesian_closed(self) -> bool:
        return True
```

### 冪對象（Power Objects）

在拓撲斯中，冪對象定義為：
$$P(X) = \Omega^X$$

這對應於集合的冪集概念，推廣了子對象的內部表示。

```python
def power_object(self, obj: T) -> T:
    """Power object P(X) = Ω^X."""
    return obj
```

---

## 2. 子對象分類器（Subobject Classifier）

### 定義

子對象分類器 $\Omega$ 是拓撲斯的核心結構。它是一個特殊對象，使得：
- 每個子對象 $S \hookrightarrow X$ 對應唯一的 characteristic 映射 $\chi_S: X \rightarrow \Omega$
- 對於任意映射 $f: X \rightarrow \Omega$，其 fiber $\chi^{-1}(true)$ 是一個子對象

### 布爾值解釋

在經典集合論中，$\Omega = \{true, false\}$，characteristic 函數返回命題的真假值。

```python
def _compute_subobject_classifier(self) -> Set:
    """Compute subobject classifier Ω."""
    return {True, False}
```

### 通用映射

子對象分類器滿足以下交換圖的通用性質：
```
X ──χ_S──→ Ω
│          │
│          ↓ true
S ────────→ 1
```

---

## 3. 拓撲斯的內部邏輯（Internal Logic）

### 直覺主義邏輯

拓撲斯的內部邏輯是**直覺主義命題邏輯**。這意味著：
- **排中律不普遍成立**：$p \vee \neg p$ 不一定為真
- **雙重否定消除不成立**：$\neg\neg p \rightarrow p$ 不一定成立
- **蘊含是軟性的**：$p \rightarrow q$ 等價於 $\forall x: (p(x) \rightarrow q(x))$

### 邏輯連接詞的範疇論實現

| 邏輯連接詞 | 範疇論實現 |
|-----------|-----------|
| $\top$ (真) | 終對象 $1$ |
| $\bot$ (假) | 初始對象 $0$ |
| $A \wedge B$ | 纖維積 $A \times B$ |
| $A \vee B$ | 餘纖維積 $A + B$ |
| $A \rightarrow B$ | 指數對象 $B^A$ |
| $\neg A$ | $A \rightarrow \bot$ |

### 布爾拓撲斯

```python
class BooleanTopos(Topos):
    """Boolean topos: subobject classifier is {0, 1}."""

    def is_boolean(self) -> bool:
        return True

    def law_of_excluded_middle(self) -> bool:
        """Check if every proposition is either true or false."""
        return True
```

布爾拓撲斯中排中律成立，內部邏輯是經典邏輯。

---

## 4. 層作為拓撲斯（Sheaves as a Topos）

### 層的定義

層是滿足局部粘合條件的預層：
- **局部性**：如果 $\{U_i\}$ 覆蓋 $U$，且片段 $s, t$ 在每個 $U_i$ 上相等，則 $s = t$
- **粘合性**：局部定義的片段可以唯一粘合成整體片段

### 層拓撲斯

```python
class SheafTopos(Topos):
    """Topos of sheaves on a topological space."""

    def __init__(self, space=None):
        self.space = space
        self.sheaves = self._compute_all_sheaves()
        super().__init__(self.sheaves)

    def is_grothendieck_topos(self) -> bool:
        """Sheaf topos on site is Grothendieck topos."""
        return True
```

### Grothendieck 拓撲斯

層拓撲斯是 **Grothendieck 拓撲斯** 的典型例子，滿足額外的 grothendieck 假設：
- 有生成元
- 所有小余極限存在
- 層範疇是 sheaves on a site

---

## 5. 自然數對象（Natural Number Object, NNO）

### 定義

自然數對象 $N$ 是拓撲斯中滿足以下遞歸原理的對象：

對任意對象 $X$ 和 morphism $s: X \rightarrow X$，存在唯一 morphism $f: N \times X \rightarrow X$ 使得：
- $f(0, x) = x$
- $f(n+1, x) = s(f(n, x))$

### 實現

在 Set 中，$N$ 是普通自然數集合。在其他拓撲斯中，$N$ 可能具有不同的結構。

### 有限性

自然數對象保證拓撲斯是 **自然數對象生成的有限類型範疇**，這是數學歸納法成立的基礎。

---

## 6. 幾何態射（Geometric Morphisms）

### 定義

幾何態射 $f: \mathcal{E} \rightarrow \mathcal{F}$ 是一對相伴函子：
- $f_*: \mathcal{E} \rightarrow \mathcal{F}$（direct image / 順像函子）
- $f^*: \mathcal{F} \rightarrow \mathcal{E}$（inverse image / 逆像函子）

滿足：
1. $f^*$ 是左正合的（ preserves finite limits）
2. $f^*$ 與有限餘極限交換
3. $f^*$ 是餘單子的（comonadic）

### 幾何態射的類型

| 類型 | 描述 |
|------|------|
| 開嵌入 | 開子空間的層 |
| 閉嵌入 | 閉子空間的層 |
| 層的像 | 順像函子是 reflectivity |
| 平坦態射 | 逆像函子保持有限極限 |

### 幾何邏輯

幾何態射對應於**幾何邏輯**的結構保存，這是摩爾語義學的核心：
- 幾何蘊含 $p \rightarrow q$ 使用covering
- 幾何命題是有限合取和任意析取的組合

---

## 7. Kripke-Joyal 語義學（Kripke-Joyal Semantics）

### 背景

Kripke-Joyal 語義學是將拓撲斯中的內部邏輯與模態邏輯聯繫起來的框架。

### 語義學條款

對於在拓撲斯 $\mathcal{E}$ 中解釋的命題 $\phi$：

| 語法 | Kripke-Joyal 語義 |
|------|------------------|
| $x \in A$ | $x$ 的值在對象 $A$ 中 |
| $\phi \wedge \psi$ | 在所有世界中 $\phi$ 和 $\psi$ 同時成立 |
| $\phi \vee \psi$ | 存在覆蓋使得局部成立 |
| $\exists x. \phi$ | 存在局部截面滿足 $\phi$ |
| $\forall x. \phi$ | 所有局部截面滿足 $\phi$ |

### 局部真

在拓撲斯中，真值是**局部」的：
- $\phi$ 在對象 $A$ 上成立 means $A \Vdash \phi$
- 這推廣了 Kripke 框架中「在世界中成立」的概念

### 語義學與層

對於層拓撲斯：
- $\exists x: U \rightarrow X$ 表示存在開覆蓋上的局部截面
- $\forall x: U \rightarrow X$ 表示截面在整個開集上一致成立

---

## 8. 阿貝爾範疇（Abelian Categories）

本模塊還包含阿貝爾範疇的實現：

```python
class AbelianCategory:
    """Abelian category: additive category with kernels and cokernels.

    Axioms:
    1. Abelian group structure on morphisms
    2. Zero object
    3. Biproducts
    4. Kernels and cokernels
    5. Every monomorphism is kernel, every epimorphism is cokernel
    """
```

### 核心結構

- **核（Kernel）**：$\ker(f) \rightarrow A$
- **餘核（Cokernel）**：$A \rightarrow \operatorname{coker}(f)$
- **像（Image）**：$\operatorname{im}(f) = \ker(\operatorname{coker}(f))$
- **正合序列**：$\operatorname{im}(f) = \ker(g)$

### 投射對象與內射對象

```python
class ProjectiveObject:
    """Projective object: Hom(P, -) preserves epimorphisms."""

class InjectiveObject:
    """Injective object: Hom(-, I) preserves monomorphisms."""
```

---

## 9. 極限與餘極限

### 纖維積（Pullback）

```python
class Pullback(Limit):
    """Pullback (fiber product): limit over span A → C ← B."""

    def universal_property(self) -> bool:
        """Pullback: A ×_C B with π_1∘f = π_2∘g."""
        return True
```

### 纖維餘積（Pushout）

```python
class Pushout(Colimit):
    """Pushout (fiber coproduct): colimit over cospan A ← C → B."""

    def universal_property(self) -> bool:
        """Pushout: A ∨_C B with f∘i_1 = g∘i_2."""
        return True
```

### 等化子與餘等化子

```python
class Equalizer(Limit):
    """Equalizer: limit over parallel morphisms f, g: A → B."""

    def universal_property(self) -> bool:
        """Equalizer: {x ∈ A | f(x) = g(x)}."""
        return True
```

---

## 10. Kan 擴展（Kan Extensions）

```python
class KanExtension:
    """Kan extension: limits and colimits in functor categories."""

    def left_kan_extension(self) -> Callable:
        """Lan_K F: C → D for diagram K: I → C."""
        return lambda x: f"Lan({x})"

    def right_kan_extension(self) -> Callable:
        """Ran_K F: C → D for diagram K: I → C."""
        return lambda x: f"Ran({x})"
```

### 左 Kan 擴展

$Lan_K F$ 是沿著 $K: I \rightarrow C$ 的左 Kan 擴展，滿足：
$$\mathcal{D}(Lan_K F(c), d) \cong \mathcal{C}(c, Kd)$$

### 右 Kan 擴展

$Ran_K F$ 是沿著 $K$ 的右 Kan 擴展，滿足：
$$\mathcal{D}(d, Ran_K F(c)) \cong \mathcal{C}(c, Kd)$$

---

## 數學背景

### 拓撲斯理論的起源

拓撲斯理論由 Lawvere、Tierney 等人在 1970 年代發展，核心洞察是：
- **拓撲斯 = 層範疇**（對於 site）
- **拓撲斯 = 幾何學的語境**
- **拓撲斯 = 直覺主義邏輯的語義框架**

### 與集合論的關係

- **Set** 是經典集合論的範疇，是布爾拓撲斯
- 所有拓撲斯都有「集合的對象」，但內部邏輯可能非經典
- 拓撲斯提供了研究「不同數學世界」的框架

### 應用領域

| 領域 | 應用 |
|------|------|
| 幾何學 | 層理論，推廣流形概念 |
| 數理邏輯 | 直覺主義邏輯，構造主義數學 |
| 拓撲學 | 無限維拓撲斯，shape 理論 |
| 代數幾何 | Grothendieck topos，motives |
| 理論物理 | 量子邏輯，態射的語義學 |

---

## 參考文獻

1. Mac Lane, S. and Moerdijk, I. - *Sheaves in Geometry and Logic*
2. Johnstone, P. - *Sketches of an Elephant*
3. Lawvere, F.W. - *Quantifiers and Sheaves*
4. Goldblatt, R. - *Topoi: The Categorial Analysis of Logic*

---

*本文件使用中文編寫，解釋 lean4py 中 topos.py 模塊的數學原理。*