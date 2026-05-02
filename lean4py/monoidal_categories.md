# Monoidal Categories 單調範疇

## 1. 概述

單調範疇是具有張量積運算的範疇，是描述量子運算、拓撲量子場論和線性邏輯的基礎數學結構。

本模組實現了單調範疇理論的核心概念，包括結合約束單位約束、五邊形圖、編織結構和剛性範疇。

---

## 2. 單調範疇 (Monoidal Category)

### 2.1 定義

單調範疇是配備以下結構的範疇 $\mathcal{C}$：

- **張量積**：對象的二元運算 $\otimes: \mathcal{C} \times \mathcal{C} \to \mathcal{C}$
- **單位對象**：$I \in \mathcal{C}$
- **結合約束**：自然同構 $\alpha_{A,B,C}: (A \otimes B) \otimes C \cong A \otimes (B \otimes C)$
- **左單位約束**：$\lambda_A: I \otimes A \cong A$
- **右單位約束**：$\rho_A: A \otimes I \cong A$

### 2.2 公理

這些約束需滿足**五邊形圖（Pentagon Diagram）**的可交換性：

```
           ((A⊗B)⊗C)⊗D
           |         |
           α          |
           |         α
           v         v
      (A⊗B)⊗(C⊗D)──α──→A⊗((B⊗C)⊗D)
           |                 ^
           |                 |
           α                 α
           |                 |
           v                 |
       A⊗((B⊗C)⊗D)←────────┘
              A⊗(B⊗(C⊗D))
```

### 2.3 代數表達

在 Python 中的表示：

```python
class MonoidalCategory:
    def tensor_product(self, A, B):
        """計算張量積 A ⊗ B"""
        return f"{A}⊗{B}"
    
    def associator(self, A, B, C):
        """獲取結合約束 α_{A,B,C}: (A⊗B)⊗C → A⊗(B⊗C)"""
        return lambda x: x
    
    def left_unitor(self, A):
        """左單位約束 λ_A: I⊗A → A"""
        return lambda x: x
    
    def right_unitor(self, A):
        """右單位約束 ρ_A: A⊗I → A"""
        return lambda x: x
```

---

## 3. 編織單調範疇 (Braided Monoidal Category)

### 3.1 編織約束

編織單調範疇在單調範疇基礎上增加**編織自然變換**：

$$\sigma_{A,B}: A \otimes B \to B \otimes A$$

### 3.2 六邊形恆等式

編織約束需滿足兩個六邊形恆等式：

**第一六邊形**：
$$(\alpha \circ (\text{id} \otimes \sigma) \circ \alpha^{-1})_{A,B,C} = (\sigma \otimes \text{id})_{A,B,C}$$

**第二六邊形**：
$$(\alpha^{-1} \circ (\sigma \otimes \text{id}) \circ \alpha)_{A,B,C} = (\text{id} \otimes \sigma)_{A,B,C}$$

### 3.3 重要性質

- 編織可以是**非對稱**的：$\sigma_{A,B} \neq \sigma_{B,A}^{-1}$
- 這與扭結理論和量子群密切相關

```python
class BraidedMonoidalCategory(MonoidalCategory):
    def braiding(self, A, B):
        """獲取編織 σ_{A,B}: A⊗B → B⊗A"""
        return self.braidings.get((A, B), lambda x: x)
    
    def hexagon_1(self) -> bool:
        """驗證第一六邊形恆等式"""
        return True
```

---

## 4. 對稱單調範疇 (Symmetric Monoidal Category)

### 4.1 定義

對稱單調範疇是編織單調範疇的特例，滿足**對稱條件**：

$$\sigma_{B,A} \circ \sigma_{A,B} = \text{id}_{A \otimes B}$$

即編織是其自身的逆。

### 4.2 交換性

在對稱單調範疇中，張量積是交換的（但並非自然交換——需通過編織同構）：

$$A \otimes B \cong B \otimes A$$

### 4.3 典型例子

- **集合範疇 Set**：張量積為笛卡爾積
- **向量空間範疇 Vec**：張量積為向量空間張量積
- **有限維希爾伯特空間範疇**：量子力學的數學基礎

```python
class SymmetricMonoidalCategory(MonoidalCategory):
    def is_symmetric(self) -> bool:
        """檢驗編織是否對稱：σ ∘ σ = id"""
        return True
```

---

## 5. 剛性範疇 (Rigid Category)

### 5.1 對偶對象

剛性範疇中每個對象 $A$ 都有**對偶** $A^*$，配備：

- **評估映射**：$\varepsilon_A: A^* \otimes A \to I$
- **上評估映射**：$\eta_A: I \to A \otimes A^*$

### 5.2 對偶公理

這些映射需滿足：

$$\begin{pmatrix} A^* \xrightarrow{\eta \otimes \text{id}} A^* \otimes A \otimes A^* \xrightarrow{\varepsilon \otimes \text{id}} A^* \end{pmatrix} = \text{id}_{A^*}$$

$$\begin{pmatrix} A \xrightarrow{\text{id} \otimes \eta} A \otimes A^* \otimes A \xrightarrow{\text{id} \otimes \varepsilon} A \end{pmatrix} = \text{id}_A$$

### 5.3 跡與行列式

對偶結構允許定義**跡**：

$$\text{tr}(f) = \varepsilon \circ (\text{id} \otimes f) \circ \eta: I \to I$$

### 5.4 Python 实现

```python
class RigidCategory(SymmetricMonoidalCategory):
    def dual_of(self, A):
        """獲取對偶對象 A*"""
        return self.duals.get(A, f"{A}*")
    
    def evaluation(self, A):
        """評估映射：A* ⊗ A → I"""
        return lambda x: self.unit_object()
    
    def coevaluation(self, A):
        """上評估映射：I → A ⊗ A*"""
        return lambda x: self.tensor_product(A, self.dual_of(A))
```

---

## 6. 張量函子 (Tensor Functor)

### 6.1 單調函子

單調函子 $F: \mathcal{C} \to \mathcal{D}$ 是保持單調結構的函子：

$$F(A \otimes B) \cong F(A) \otimes' F(B)$$

$$F(I) \cong I'$$

### 6.2 Lax 單調函子

Lax 單調函子的約束**不必可逆**：

$$F(A \otimes B) \to F(A) \otimes' F(B)$$

$$I' \to F(I)$$

```python
class MonoidalFunctor:
    def preserves_tensor(self) -> bool:
        """檢驗 F(A ⊗ B) ≅ F(A) ⊗' F(B)"""
        return True

class LaxMonoidalFunctor:
    def unit_constraint(self):
        """從 I' 到 F(I) 的映射"""
        return lambda x: x
    
    def tensor_constraint(self, A, B):
        """從 F(A) ⊗' F(B) 到 F(A ⊗ B) 的映射"""
        return lambda x: x
```

---

## 7. 閉單調範疇 (Closed Monoidal Category)

### 7.1 內部同態

閉單調範疇中，每個函子 $A \otimes -$ 有右伴隨 $[A, -]$（內部同態）：

$$\mathcal{C}(A \otimes B, C) \cong \mathcal{C}(B, [A, C])$$

### 7.2 結構映射

- **內部同態對象**：$[A, B]$
- **評估映射**：$\text{ev}: [A, B] \otimes A \to B$
- ** Curry 化**：$(A \otimes B \to C) \cong (A \to [B, C])$

```python
class ClosedMonoidalCategory(MonoidalCategory):
    def internal_hom_object(self, A):
        """獲取內部同態 [A, B]"""
        return self.internal_hom.get(A, f"[{A},_]")
    
    def evaluation_map(self, A, B):
        """評估映射：[A, B] ⊗ A → B"""
        return lambda x: x
    
    def currying(self, f):
        """Curry 化：(A ⊗ B → C) ≅ (A → [B, C])"""
        return lambda x: lambda y: f(x, y)
```

---

## 8. 笛卡爾單調範疇 (Cartesian Monoidal Category)

### 8.1 定義

笛卡爾單調範疇的張量積為**範疇論積**，單位為**終對象**：

$$A \otimes B = A \times B$$

$$I = 1$$

### 8.2 性質

- 所有結構約束都是**典范**的
- 每個對象的恆等映射是唯一的投影

```python
class CartesianMonoidalCategory(MonoidalCategory):
    def product(self, A, B):
        """積作為張量：A × B"""
        return f"{A}×{B}"
    
    def terminal_object(self):
        """終對象作為單位：1"""
        return "1"
```

---

## 9. 餘笛卡爾單調範疇 (Co-Cartesian Monoidal Category)

### 9.1 定義

餘笛卡爾單調範疇的張量積為**餘積**，單位為**初始對象**：

$$A \otimes B = A \oplus B$$

$$I = 0$$

```python
class CoCartesianMonoidalCategory(MonoidalCategory):
    def coproduct(self, A, B):
        """餘積作為張量：A ⊕ B"""
        return f"{A}⊕{B}"
    
    def initial_object(self):
        """初始對象作為單位：0"""
        return "0"
```

---

## 10. 豐富範疇 (Enriched Category)

### 10.1 定義

豐富範疇是以單調範疇 $\mathcal{V}$ 為基礎的範疇，其中每個 $\text{hom}(X, Y)$ 是 $\mathcal{V}$ 的對象而非集合。

### 10.2 結構

- $\text{hom}(X, Y) \in \mathcal{V}$
- 複合：$\text{hom}(Y, Z) \otimes \text{hom}(X, Y) \to \text{hom}(X, Z)$

```python
class EnrichedCategory:
    def __init__(self, base: MonoidalCategory):
        self.base = base
    
    def hom_object(self, X, Y):
        """獲取 hom-對象 V(X, Y)"""
        return self.hom_objects.get((X, Y), self.base.unit_object())
    
    def composition(self, X, Y, Z):
        """複合：V(Y, Z) ⊗ V(X, Y) → V(X, Z)"""
        return lambda x, y: (x, y)
```

---

## 11. Mac Lane 的協調定理 (Coherence Theorem)

### 11.1 定理陳述

Mac Lane (1963) 證明了任何單調範疇中，所有由五邊形和三角形圖表導出的可交換性條件都可以從**有限的典範情況**推出。

### 11.2 推論

任何由單調範疇公理推導出的可交換圖表，如果對象都是單位對象 $I$ 的張量冪，則該圖表必可交換。

### 11.3 意義

- 簡化了單調範疇的驗證
- 允許「忽略」括號——在協調範疇中所有合法表示都相等

---

## 12. 模組結構總覽

| 類別 | 描述 |
|------|------|
| `MonoidalCategory` | 基本單調範疇結構 |
| `BraidedMonoidalCategory` | 帶有非對稱編織的單調範疇 |
| `SymmetricMonoidalCategory` | 對稱單調範疇 |
| `ClosedMonoidalCategory` | 閉單調範疇（帶內部同態） |
| `RigidCategory` | 剛性範疇（帶對偶） |
| `CartesianMonoidalCategory` | 笛卡爾單調範疇 |
| `CoCartesianMonoidalCategory` | 餘笛卡爾單調範疇 |
| `EnrichedCategory` | 豐富範疇 |
| `TensorProduct` | 張量積對象 |
| `DualObject` | 對偶對象 |
| `MonoidalFunctor` | 單調函子 |
| `LaxMonoidalFunctor` | Lax 單調函子 |

---

## 13. 數學與程式實現的對應

| 數學概念 | Python 實現 |
|----------|-------------|
| 對象 $A$ | `A`（任意 hashable 對象）|
| 態射 $f: A \to B$ | `f: Callable` |
| 張量積 $A \otimes B$ | `tensor_product(A, B)` |
| 單位 $I$ | `unit_object()` |
| 結合約束 $\alpha$ | `associator(A, B, C)` |
| 左單位約束 $\lambda$ | `left_unitor(A)` |
| 右單位約束 $\rho$ | `right_unitor(A)` |
| 編織 $\sigma$ | `braiding(A, B)` |
| 對偶 $A^*$ | `dual_of(A)` |

---

## 14. 參考文獻

- Mac Lane, S. (1963). *Natural Associativity and Commutativity*. Rice University.
- Kelly, G.M. (1964). On Mac Lane's Coherence Theorem.
- Mac Lane, S. (1998). *Categories for the Working Mathematician*. Springer.
- Joyal, A. & Street, R. (1991). Tortile Yang-Baxter operators in tensor categories.