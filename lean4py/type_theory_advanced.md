# Type Theory Advanced — 進階類型論

本模組模擬 mathlib4 的 `Mathlib.Logic.TypeTheory`，涵蓋 Martin-Löf 類型論、同一性類型與宇宙多態性。

---

## 1. 依賴類型（Dependent Types）

### 1.1 定義

依賴類型是指**由項索引的類型家族**。傳統類型論中，類型 `A → B` 的函數，其返回值類型 `B` 與輸入無關。但在依賴類型論中，返回類型可以依賴於輸入值。

形式化地，對於每個 `x : A`，存在一個類型 `B(x)`。這種「類型家族」記為：

```
B : A → Type
```

或使用 Π 類型寫成 `Π(x : A) B(x)`。

### 1.2 數學直觀

設 `A = ℕ`，則 `B` 是一個由自然數索引的類型家族：
- `B(0) = ℝ`（實數）
- `B(1) = 複數）
- `B(n) = n×n 矩陣`

這允許構建**依賴於具體值的類型**，這是跡式記法（dependent typing）的核心。

### 1.3 代碼對應

`MartinLofType` 類別提供最基礎的類型論框架：

```python
class MartinLofType:
    @staticmethod
    def type_of_types(universe_level: int = 0) -> str:
        """Type₀ : Type₁ : Type₂ : ..."""
        return f"Type_{universe_level}"
```

---

## 2. Π 類型（Dependent Function Types）

### 2.1 定義

Π 類型表示**依賴函數類型**，即返回值類型依賴於輸入參數的函數：

```
Π(x : A) B(x)
```

非依賴函數 `A → B` 是 Π 類型的特例（當 `B(x)` 與 `x` 無關時）。

### 2.2 語義

- **類型層面**：`Π(x : A) B(x)` 是所有函數 `f` 的類型，對每個 `x : A`，`f(x) : B(x)`
- **項層面**：對每個 `x : A`，應用 `f x : B(x)`

### 2.3 範例

向量空間的線性映射：
- 輸入：`v : V`（向量空間 `V` 的元素）
- 輸出：取決於 `v` 所在的空間

```python
# 依賴函數的類型簽名示例
linear_map : Π(V : VectorSpace) (v : V) → LinearMap(V, Field)
```

---

## 3. Σ 類型（Dependent Pair Types）

### 3.1 定義

Σ 類型表示**依賴對類型**，也稱為「存在類型」或「依賴總類型」：

```
Σ(x : A) B(x)
```

直觀理解：這是所有對 `⟨x, b⟩` 的類型，其中 `x : A` 且 `b : B(x)`。

### 3.2 與笛卡爾積的關係

當 `B(x)` 與 `x` 無關時，Σ 類型退化為普通的笛卡爾積：
- `Σ(x : A) B ≅ A × B`

### 3.3 數學直觀

Σ 類型對應於**纖維積**（fiber product）的概念。對於投影 `π₁ : Σ(x : A) B(x) → A`，每個 `a : A` 的纖維正好是 `B(a)`。

---

## 4. 同一性類型（Identity Types）與相等性

### 4.1 定義

Martin-Löf 同一性類型是類型論中表示**相等性**的核心概念。對於類型 `A` 和項 `x, y : A`：

```
Id_A(x, y) : Type
```

若存在 `p : Id_A(x, y)`，則 `x` 和 `y` 在類型 `A` 中相等。

### 4.2 自反性（Reflexivity）

每個項都與自身相等，這通過**反射項**（ref term）表達：

```python
class IdentityType:
    @staticmethod
    def reflexivity(A: str, x: str) -> Dict[str, Any]:
        """refl_x : Id_A(x, x)."""
        return {"term": f"refl_{x}", "type": f"Id_{A}({x}, {x})"}
```

對每個 `x : A`，存在項 `refl_x : Id_A(x, x)`。

### 4.3 同一性類型的消去規則

通過路徑消去（path induction），若要證明對所有 `x, y : A` 和 `p : Id_A(x, y)` 性質 `C(x, y, p)` 成立，只需證明對所有 `x : A`，`C(x, x, refl_x)` 成立。

### 4.4 同元異質相等性（Heterogeneous Equality）

標準同一性類型要求比較的兩個項屬於**同一類型**。同元異質相等性放寬這一限制：

```python
class HeterogeneousEquality:
    @staticmethod
    def make(x: Any, y: Any) -> Dict[str, Any]:
        """Construct heterogeneous equality (simplified)."""
        return {"equality": "x == y", "is_heterogeneous": True}
```

允許 `x : A` 與 `y : B` 的相等性比較，在某些元理論論證中非常有用。

---

## 5. 類型宇宙與宇宙多態性

### 5.1 類型宇宙

為避免羅素悖論，類型論引入**宇宙層級**（universe levels）：

```
Type₀ : Type₁ : Type₂ : ...
```

每個 `Typeᵤ` 是下一層宇宙中所有類型的類型。

```python
class MartinLofType:
    @staticmethod
    def type_of_types(universe_level: int = 0) -> str:
        """Type₀ : Type₁ : Type₂ : ..."""
        return f"Type_{universe_level}"
```

### 5.2 宇宙多態性（Universe Polymorphism）

宇宙多態性允許定義**與宇宙無關**的類型和函數。相同的定義可以在任意宇宙級別實例化：

```python
class UniversePolymorphism:
    @staticmethod
    def lift(type_term: str, target_universe: int) -> Dict[str, Any]:
        """Lift type to higher universe (simplified)."""
        return {"lifted": type_term, "universe": target_universe}
```

### 5.3 提升操作

將較低宇宙的類型提升到較高宇宙：

```
lift : Type₀ → Type₁ → Type₂ → ...
```

這使得像 `Id` 這樣的類型構造器可以宇宙多態地定義。

---

## 6. 歸納類型與餘歸納類型

### 6.1 歸納類型（Inductive Types）

歸納類型由以下元素定義：
- **建構子**：生成該類型項的函數
- **消去規則**：從該類型推導命題的函數
- **遞歸原理**：定義從該類型到任意類型的函數

經典例子：
- **自然數**：`0 : ℕ`, `succ : ℕ → ℕ`
- **列表**：`[] : List(A)`, `cons : A → List(A) → List(A)`
- **二叉樹**：`leaf : Tree(A)`, `node : Tree(A) → Tree(A) → Tree(A)`

### 6.2 餘歸納類型（Coinductive Types）

餘歸納類型通過**觀察器**（observers）定義，對應於**無窮數據結構**：

```lean
-- 余歸納流的定義示例
coinductive Stream (α : Type) : Type
| head : Stream α → α
| tail : Stream α → Stream α
```

### 6.3 歸納 vs 餘歸納

| 特徵 | 歸納類型 | 餘歸納類型 |
|------|----------|------------|
| 語義 | 有限結構 | 無窮/潛無窮結構 |
| 原則 | 結構歸納 | 余歸納（最終性） |
| 例子 | 自然數、列表、樹 | 流、部門、進展 |

---

## 7. 同倫類型論（Homotopy Type Theory, HoTT）原則

### 7.1 核心思想

HoTT 將類型解釋為**拓撲空間**（或 ∞-群胚），項解釋為**點**，同一性類型 `Id_A(x, y)` 解釋為從 `x` 到 `y` 的**路徑空間**。

### 7.2 關鍵原則

#### 7.2.1 路徑空間

對 `x, y : A`，`Id_A(x, y)` 本身是一個類型，其項可以進一步有同一性類型：

```
p : Id_A(x, y)
q : Id_{Id_A(x, y)}(p, refl_x)
```

這產生了**高階路徑**的概念。

#### 7.2.2 等價性

HoTT 定義**等價**為具有收斂性的函數：

```lean
is_equivalence (f : A → B) := (has_inverse f) × (has_inverse (inverse f)) × ...
```

這比傳統的雙射更精細，考慮了路徑空間的結構。

#### 7.2.3 Univalence 公理

Univalence 公理表明**路徑相等性等價於等價**：

```
ua : (A ≅ B) → (A = B)
```

即：若兩個類型等價，則它們在類型論中相等。這數學上意味著「數學對象由其結構唯一確定」。

#### 7.2.4 高階群胚結構

每個類型攜帶層次結構：
- **0-類型**：集合（所有路徑可識別）
- **1-類型**： Groupoid（對象的路徑是等價）
- **n-類型**：n-Groupoid

### 7.3 計算解釋

在 HoTT 中，類型檢查對應於空間中的連續變形，這為計算提供了新的幾何直觀。

---

## 8. 規范性（Canonicity）與正規化（Normalization）

### 8.1 規范性定理

**規范性**（Canonicity）指出：每個閉合項（在無自由變量的語境中）都歸約到一個**規範形式**（canonical form）。

對於自然數，規範形式是 `0`, `succ(0)`, `succ(succ(0))`, ...

### 8.2 正規化

**正規化**（Normalization）更強：每個項都歸約到唯一的規範形式，不依賴於歸約策略的選擇。

```
∀ t : T, ∃! c. t →* c ∧ is_canonical(c)
```

### 8.3 類型論中的意義

規范性保證了：
- **決定性**：類型檢查是算法可行的
- **一致性**：沒有歸約到矛盾項的途徑
- **安全性**：計算總是終止

### 8.4 強規范性與弱規范性

- **強規范性**：所有歸約序列都終止
- **弱規范性**：每個項至少有 one 個終止的歸約序列

---

## 模組結構

本模組提供以下核心類別：

| 類別 | 功能 |
|------|------|
| `MartinLofType` | Martin-Löf 類型論基礎，宇宙層級 |
| `IdentityType` | 同一性類型的建構與反射 |
| `UniversePolymorphism` | 宇宙多態性與提升操作 |
| `HeterogeneousEquality` | 同元異質相等性 |

---

## 數學庫對應

本模組對應於 mathlib4 的：
- `Mathlib.Logic.TypeTheory`
- `Mathlib.Logic.DefsAndEquations`
- `Mathlib.Logic.HeterogeneousEquality`

---

## 參考文獻

1. Martin-Löf, P. (1975). *Intuitionistic Type Theory*
2. Awodey, S. (2013). *Homotopy Type Theory* (HoTT Book)
3. The Univalent Foundations Program (2013). *Homotopy Type Theory: Univalent Foundations of Mathematics*
4. Norell, U. (2007). *Towards a practical programming language based on dependent type theory*