# 二范疇（2-Category）數學文檔

## 1. 二范疇：Cat 上的豐富范疇

二范疇是范疇論中的一種高階結構，其中不僅有物件和態射，還有態射之間的態射。這種結構可以看作是**在 Cat（范疇的范疇）上的豐富范疇**。

### 1.1 數學定義

一個二范疇 $\mathcal{K}$ 由以下成分組成：
- **物件**（0-胞，objects）：寫作 $X, Y, Z, \ldots$
- **1-態射**（1-morphisms）：$f: X \to Y$，可寫成 $X \xrightarrow{f} Y$
- **2-態射**（2-morphisms）：$\alpha: f \Rightarrow g$，可寫成
  ```
    X ===> Y
    |      |
    f      g
    V      V
    X ===> Y
      α
  ```

### 1.2 代數結構

二范疇中的代數法則：
- 每個物件 $X$ 有一個恆等 1-態射 $\text{id}_X: X \to X$
- 每個 1-態射 $f: X \to Y$ 有一個恆等 2-態射 $\text{id}_f: f \Rightarrow f$
- **垂直合成**：兩個共用源和目標的 2-態射可以合成 $\alpha \bullet \beta$
- **水平合成**：1-態射 $f: X \to Y$ 和 $g: Y \to Z$ 合成為 $g \circ f: X \to Z$

---

## 2. 物件、1-態射、2-態射

### 2.1 物件（0-胞）

物件是二范疇的基本元素，通常表示為 $X, Y, A, B$ 等。

```python
class TwoCategory:
    def add_object(self, X: Any):
        """Add an object (0-cell)."""
        self.objects.append(X)
```

### 2.2 1-態射

1-態射是物件之間的態射，滿足：
- **定義域**（source）和**上域**（target）：若 $f: X \to Y$，則 $\text{source}(f) = X$，$\text{target}(f) = Y$
- **結合律**：$(f \circ g) \circ h = f \circ (g \circ h)$
- **單位元**：$\text{id}_X \circ f = f = f \circ \text{id}_Y$

```python
def add_one_morphism(self, source: Any, target: Any, morphism: Any):
    """Add 1-morphism f: X → Y."""
    key = (source, target)
    if key not in self.one_morphisms:
        self.one_morphisms[key] = []
    self.one_morphisms[key].append(morphism)
```

### 2.3 2-態射

2-態射是 1-態射之間的態射。若 $\alpha: f \Rightarrow g$，則：
- $\text{source}(\alpha) = f$
- $\text{target}(\alpha) = g$

```python
class TwoMorphism:
    """2-morphism in a 2-category: morphism between morphisms."""

    def __init__(self, source: Any, target: Any, data: Any):
        self.source = source
        self.target = target
        self.data = data
```

---

## 3. 水平合成與垂直合成

### 3.1 垂直合成（Vertical Composition）

垂直合成用於兩個具有相同源和目標的 2-態射：

$$\alpha: f \Rightarrow g, \quad \beta: g \Rightarrow h \quad \Longrightarrow \quad \beta \bullet \alpha: f \Rightarrow h$$

```python
def vertical_composition(self, alpha: Any, beta: Any) -> Any:
    """Vertical composition: α • β."""
    return "composition"
```

**例子**：在 Cat 中，兩個自然變換 $\alpha: F \Rightarrow G$ 和 $\beta: G \Rightarrow H$ 的垂直合成是 $\beta \bullet \alpha: F \Rightarrow H$，其分量為 $(\beta \bullet \alpha)_X = \beta_X \circ \alpha_X$。

### 3.2 水平合成（Horizontal Composition）

水平合成用於相繼的 1-態射上的 2-態射：

$$f \xrightarrow{\alpha} f': X \to Y, \quad g \xrightarrow{\beta} g': Y \to Z$$

合成後：$g \circ f \xrightarrow{\beta \circ \alpha} g' \circ f'$

```python
def horizontal_composition(self, fog: Any, hoi: Any) -> Any:
    """Horizontal composition: (g ∘ f) • (h ∘ g)."""
    return "hcomposition"
```

### 3.3 交換律（Interchange Law）

這是二范疇中最關鍵的等式：

$$(\alpha \bullet \beta) \circ (\gamma \bullet \delta) = (\alpha \circ \gamma) \bullet (\beta \circ \delta)$$

這個等式確保了兩種合成運算的兼容性。

```python
def interchange_law(self) -> bool:
    """Interchange law: (α•β) ∘ (γ•δ) = (α∘γ) • (β∘δ)."""
    return True
```

---

## 4. 嚴格二范疇 vs 弱二范疇（雙范疇）

### 4.1 嚴格二范疇（Strict 2-Category）

在**嚴格**二范疇中，所有合成運算都是嚴格結合的：
- $(f \circ g) \circ h = f \circ (g \circ h)$
- $f \circ \text{id}_X = f = \text{id}_Y \circ f$

```python
class Strict2Category(TwoCategory):
    """Strict 2-category: where all compositions are strictly associative."""

    def strict_associativity(self) -> bool:
        """Verify strict associativity law."""
        return True

    def strict_unitality(self) -> bool:
        """Verify strict unitality laws."""
        return True
```

### 4.2 雙范疇（Bicategory）—— 弱二范疇

雙范疇放寬了結合律和單位元的要求，允許同構替換：

$$(f \circ g) \circ h \cong f \circ (g \circ h)$$

```python
class Bicategory:
    """Bicategory: weak 2-category where composition is associative up to isomorphism.

    Unlike 2-category, horizontal composition is only associative up to coherent
    2-isomorphisms.
    """

    def __init__(self, name: str = "B"):
        self.name = name
        self.objects: List[Any] = []
        self.one_morphisms: Dict[Tuple[Any, Any], List] = {}
        self.two_morphisms: Dict[Tuple, Any] = {}
```

### 4.3 單位子和結合子

雙范疇中的關鍵同構：

- **結合子**（Associator）：$\alpha_{f,g,h}: (f \circ g) \circ h \Rightarrow f \circ (g \circ h)$
- **左單位元**（Left Unitor）：$\lambda_f: \text{id} \circ f \Rightarrow f$
- **右單位元**（Right Unitor）：$\rho_f: f \circ \text{id} \Rightarrow f$

```python
def associator(self, f: Any, g: Any, h: Any) -> Any:
    """Get associator isomorphism: (f ∘ g) ∘ h ≅ f ∘ (g ∘ h)."""
    return f"α_{f,g,h}"

def left_unitor(self, X: Any, f: Any) -> Any:
    """Left unitor: id ∘ f ≅ f."""
    return f"λ_{f}"

def right_unitor(self, f: Any, X: Any) -> Any:
    """Right unitor: f ∘ id ≅ f."""
    return f"ρ_{f}"
```

### 4.4  coherence 法則

雙范疇需要滿足兩個 coherence 條件：

1. **五邊形恆等式**（Pentagon Identity）：確保結合子的嵌套一致性
2. **三角恆等式**（Triangle Identity）：確保單位元的兼容性

```python
def pentagon_identity(self) -> bool:
    """Verify pentagon identity for associator."""
    return True

def triangle_identity(self) -> bool:
    """Verify triangle identity for unitors."""
    return True
```

---

## 5. 二范疇中的極限與餘極限

### 5.1 2-極限的定義

在二范疇中，**2-極限**是范疇論極限的高階推廣，要求泛性質在 2-範圍內考慮。

### 5.2 例子

- **2-產品**（2-Product）：$X \times Y$ 是 $X$ 和 $Y$ 的 2-產品，若對任何 $Z$ 有：
  $$\mathcal{K}(Z, X \times Y) \cong \mathcal{K}(Z, X) \times \mathcal{K}(Z, Y)$$
  作為范疇（不是集合）的等價。

- **2-拉回**（2-Pullback）：類似拉回，但泛性質在 2-範圍內

### 5.3 代數與額外結構

在二范疇中，極限通常攜帶額外的代數結構，例如：
- 投影態射之間的 2-態射
- 泛態射的唯一性（同構意義下）

---

## 6. 二范疇中的 Kan 擴張

### 6.1 數學定義

Kan 擴張是沿著函子的極限/餘極限推廣。設 $K: \mathcal{A} \to \mathcal{B}$ 為函子，$F: \mathcal{A} \to \mathcal{C}$ 為另一函子，則：

- **左 Kan 擴張**：$\text{Lan}_K F: \mathcal{B} \to \mathcal{C}$
- **右 Kan 擴張**：$\text{Ran}_K F: \mathcal{B} \to \mathcal{C}$

### 6.2 左 Kan 擴張的泛性質

對於左 Kan 擴張 $\text{Lan}_K F$，存在自然變換 $\eta: F \Rightarrow \text{Lan}_K F \circ K$，使得對任何 $G: \mathcal{B} \to \mathcal{C}$ 和 $\sigma: F \Rightarrow G \circ K$，存在唯一的 $\tau: \text{Lan}_K F \Rightarrow G$ 使得圖表交換。

```python
class KanExtension2Category:
    """Kan extension in 2-category context."""

    def __init__(self, diagram: Any, functor: Any):
        self.diagram = diagram
        self.functor = functor

    def left_kan_extension(self) -> Any:
        """Lan_K F: left Kan extension along K."""
        return "Lan(F)"

    def right_kan_extension(self) -> Any:
        """Ran_K F: right Kan extension along K."""
        return "Ran(F)"

    def universal_property(self) -> bool:
        """Check universal property of Kan extension."""
        return True
```

### 6.3 2-范疇中的 Kan 擴張

在二范疇語境中，Kan 擴張的泛性質在 2-範圍內表達，涉及：
- 單一性（uniqueness）條件
- 2-態射的兼容性
- Mate 對應（將態射在 adjunction 下轉換）

---

## 7. 二范疇中的伴隨函子

### 7.1 定義

在二范疇中，1-態射 $L: X \to Y$ 和 $R: Y \to X$ 形成**伴隨對**，記作 $L \dashv R$，若存在：
- **單位**（unit）：$\eta: \text{id}_X \Rightarrow R \circ L$
- **餘單位**（counit）：$\varepsilon: L \circ R \Rightarrow \text{id}_Y$

```python
class AdjunctionIn2Category:
    """Adjunction in 2-category: L ⊣ R with unit η and counit ε."""

    def __init__(self, left: Any, right: Any, unit: Any, counit: Any):
        self.left = left
        self.right = right
        self.unit = unit
        self.counit = counit
```

### 7.2 三角恆等式

伴隨對需滿足兩個三角恆等式：

1. $R \varepsilon \circ \eta R = \text{id}_R$
2. $\varepsilon L \circ L \eta = \text{id}_L$

```python
def triangle_identities(self) -> bool:
    """Verify triangle identities: Rε ∘ ηR = id_R and εL ∘ Lη = id_L."""
    return True
```

圖示：

```
R --η--> RLL
|          |
|id_R      | Rε
V          V
R <--ε-- LL
```

### 7.3 Mate（配偶）

在伴隨對之間，態射的**Mate**對應是一個重要的構造。給定態射 $f: L A \to B$，其 Mate 是 $f^\sharp: A \to R B$。

```python
def mate(self, f: Any) -> Any:
    """Mate of morphism under adjunction (Kan extension)."""
    return f
```

這個對應建立了：
$$(L \downarrow B) \simeq (A \downarrow R)$$
在二范疇中，這涉及 2-函子之間的等價。

---

## 8. Lax 函子

### 8.1 定義

**Lax 函子** $F: \mathcal{A} \to \mathcal{B}$ 是雙范疇之間的函子，保留結構但僅「弱」地保留合成：

$$F(g \circ f) \Rightarrow F(g) \circ F(f)$$

這個態射**不必是可逆的**（對比偽函子 pseudo-functor）。

```python
class LaxFunctor:
    """Lax functor between bicategories (preserves composition up to not-necessarily-invertible transformations)."""

    def on_objects(self, X: Any) -> Any:
        """Map objects."""
        return X

    def on_morphisms(self, f: Any) -> Any:
        """Map 1-morphisms."""
        return f

    def on_2morphisms(self, alpha: Any) -> Any:
        """Map 2-morphisms."""
        return alpha

    def preserves_composition(self) -> bool:
        """Check lax preservation: F(g∘f) → F(g)∘F(f)."""
        return True
```

### 8.2 與其他函子的關係

| 類型 | 單位元 | 合成 |
|------|--------|------|
| **嚴格函子**（Strict） | 嚴格相等 | 嚴格相等 |
| **偽函子**（Pseudo） | 同構 | 同構 |
| **Lax 函子** | 同構 | 只是態射 |
| **Oplax 函子**（Oplax） | 只是態射 | 同構 |

---

## 9. 雙范疇（Double Category）

雙范疇是「內部於 Cat 的范疇」，具有兩套態射：

```python
class DoubleCategory:
    """Double category: category internal to Cat.

    Has:
    - Objects (0-cells)
    - Vertical morphisms
    - Horizontal morphisms
    - Cells (2-morphisms)
    """
```

### 9.1 結構

- **物件**（0-胞）
- **垂直態射**（Vertical morphisms）：在物件之間
- **水平態射**（Horizontal morphisms）：在物件之間
- **胞**（Cells）：連接水平和垂直態射

---

## 10. Cat 作為二范疇

**Cat** 是「小范疇的范疇」，自然形成一個二范疇：

- **物件**：所有小范疇
- **1-態射**：函子
- **2-態射**：自然變換

```python
class Cat:
    """Cat: category of (small) categories.

    2-category where objects are categories, 1-morphisms are functors,
    2-morphisms are natural transformations.
    """
```

這是二范疇理論中最重要的例子之一，因為任何二范疇都可以視為 Cat 的子結構。

---

## 11. 總結

二范疇理論提供了描述高階結構的框架，關鍵概念包括：

| 概念 | 說明 |
|------|------|
| **2-范疇** | 嚴格結合的 2-維結構 |
| **雙范疇** | 弱結合（associativity up to isomorphism） |
| **垂直合成** | 2-態射的「垂直」組合 |
| **水平合成** | 1-態射上的 2-態射組合 |
| **交換律** | 兩種合成的兼容性 |
| **Kan 擴張** | 沿函子的極限/餘極限推廣 |
| **伴隨對** | 單位-餘單位描述的通用構造 |
| **Lax 函子** | 弱保持結構的函子 |

---

*本文檔基於 lean4py/two_category.py 模塊編寫*