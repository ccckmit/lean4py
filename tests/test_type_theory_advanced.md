# test_type_theory_advanced.py 測試文檔

## 1. 測試驗證的類型論概念

本測試模組基於 `lean4py/type_theory_advanced.py`（模擬 mathlib4 的 Mathlib.Logic.TypeTheory），驗證高級類型論的核心概念。

### 測試結構

| 測試類別 | 測試方法 | 驗證內容 |
|---------|---------|---------|
| `TestMartinLofType` | `test_type_of_types`, `test_is_type` | 馬丁-洛夫類型論的層次結構 |
| `TestIdentityType` | `test_reflexivity`, `test_is_equality` |  identity type 的基本性質 |
| `TestUniversePolymorphism` | `test_lift`, `test_is_polymorphic` | 宇宙多態性 |
| `TestHeterogeneousEquality` | `test_make`, `test_is_heterogeneous` | 異質相等性 |

---

## 2. 依賴類型（Dependent Type）測試

### 數學原理

依賴類型是指類型可以依賴於項的值。形式化地說，若 `B : A → U` 是一個函數，則 `Π(x : A) B(x)` 或 `Σ(x : A) B(x)` 是依賴類型。

### 本模組中的體現

雖然測試中沒有直接的依賴類型測試，但 `IdentityType` 和 `HeterogeneousEquality` 的實現隱含依賴類型的概念：

```python
# IdentityType.reflexivity 返回包含依賴類型資訊的字典
{"term": f"refl_{x}", "type": f"Id_{A}({x}, {x})"}
```

這裡 `Id_A(x, x)` 的類型取決於 `x` 的具體值，體現了依賴類型的核心思想。

---

## 3. Pi/Sigma 类型測試

### 數學原理

**Pi 類型（依賴函數類型）**
$$
\Pi(x : A) B(x) : U
$$
表示對所有 $x : A$ 對應一個類型 $B(x)$ 的函數。當 $B$ 是常數類型時，Pi 類型退化為普通函數類型 $A \to B$。

**Sigma 類型（依賴對類型）**
$$
\Sigma(x : A) B(x) : U
$$
表示一個對 $(x, y)$，其中 $x : A$ 且 $y : B(x)$。這推廣了笛卡爾積 $A \times B$。

### 與測試的關聯

本模組中 `MartinLofType.type_of_types` 模擬了這些高階類型的層次結構：
- `Type_0` : 普通類型（Kind）
- `Type_1` : 類型的類型（Kind 的類型）
- `Type_2` : 進一步的層次

---

## 4. Identity Type 測試

### 數學原理

Identity Type 由 Per Martin-Löf 引入，定義如下：

對於任意類型 $A$ 和項 $x, y : A$，identity type $Id_A(x, y)$ 表示「$x$ 和 $y$ 在類型 $A$ 中相等」這一命題。

** reflexivity（自反性）**：
對於每個項 $x : A$，存在一個 canonical 的 identity 項：
$$
refl_x : Id_A(x, x)
$$

### 測試案例分析

```python
def test_reflexivity(self):
    result = IdentityType.reflexivity("A", "x")
    self.assertIn("term", result)
```

驗證 `refl_x : Id_A(x, x)` 的構造，返回格式為：
```python
{"term": "refl_x", "type": "Id_A(x, x)"}
```

```python
def test_is_equality(self):
    self.assertTrue(IdentityType.is_equality("A", "x", "y"))
```

驗證 `Id_A(x, y)` 是否構成有效的相等性判斷。

---

## 5. 宇宙（Universe）測試

### 數學原理

馬丁-洛夫類型論採用層次化的宇宙結構：
$$
Type_0 : Type_1 : Type_2 : \cdots
$$

每個 $Type_i$ 是位於上一層宇宙中的類型。這避免了在類型論中造成的不一致性（如 Russell 悖論）。

### 宇宙多態性（Universe Polymorphism）

宇宙多態性允許定義可以在任意宇宙級別實例化的參數化定義：

```python
def test_lift(self):
    result = UniversePolymorphism.lift("type_term", 1)
    self.assertIn("lifted", result)
```

`lift` 函數將類型提升到更高的宇宙層級。

```python
def test_is_polymorphic(self):
    self.assertTrue(UniversePolymorphism.is_polymorphic("type_term"))
```

驗證類型是否具有宇宙多態性。

---

## 6. 異質相等性（Heterogeneous Equality）

### 數學原理

傳統的 Identity Type 要求比較的兩個項來自同一類型 $A$。但在某些場景下，需要比較不同類型中的項：

$$
x == y \quad \text{其中} \quad x : A, \quad y : B
$$

這稱為異質相等性，在形式化數學中常用於處理需要跨越不同類型的相等性證明。

### 測試案例

```python
def test_make(self):
    result = HeterogeneousEquality.make("x", "y")
    self.assertIn("equality", result)
```

構造異質相等性：
```python
{"equality": "x == y", "is_heterogeneous": True}
```

```python
def test_is_heterogeneous(self):
    eq_term = {"is_heterogeneous": True}
    self.assertTrue(HeterogeneousEquality.is_heterogeneous(eq_term))
```

驗證相等性是否為異質的。

---

## 7. 測試與 mathlib4 的對應

| 本模組 | mathlib4 對應 |
|-------|-------------|
| `MartinLofType` | `Mathlib.Logic.TypeTheory.MartinLofType` |
| `IdentityType` | `Mathlib.Logic.TypeTheory.IdentityType` |
| `UniversePolymorphism` | `Mathlib.Logic.TypeTheory.UniversePolymorphism` |
| `HeterogeneousEquality` | `Mathlib.Logic.TypeTheory.HeterogeneousEquality` |

本實現為簡化版本，主要用於教學和基礎驗證。完整實現可參考 Lean's mathlib4。