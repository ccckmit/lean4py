# 模型範疇測試文檔 (test_model_category.py)

## 1. 概述

本測試文件驗證 `lean4py.model_category` 模組中的模型範疇（Model Category）相關功能。模型範疇是同倫論中的核心概念，由 Daniel Quillen 提出，為處理同倫類別提供了公理化框架。

---

## 2. 模型範疇基本結構測試

### 2.1 測試內容

- **建立空模型範疇**：`ModelCategory()` 建立無物件的範疇
- **建立含物件的模型範疇**：`ModelCategory(["A", "B"])` 可容納多個物件
- **添加弱等價關係**：`add_weak_equivalence("A", "B")` 記錄物件間的弱等價
- **添加餘纖維結構**：餘纖維（余纖維）關係的建立與驗證
- **添加纖維結構**：纖維結構的添加與查詢
- **提升性質測試**：`has_lifting_property` 測試特定提升性質是否成立
- **因子分解**：`factorize` 將任意態射分解為餘纖維→弱等價→纖維的形式
- **同倫範疇構造**：從模型範疇構造其同倫範疇 `HomotopyCategory`

### 2.2 數學原理

模型範疇是一個帶有三類特殊態射的範疇：

1. **弱等價（Weak Equivalences）** - 在同倫論中「本質相同」的態射
2. **餘纖維（Cofibrations）** - 可視為「子物件」的嵌入
3. **纖維（Fibrations）** - 可視為「投影」的推廣

這三者滿足**提升性質**與**因子分解公理**：
- 任意態射可以唯一（ up to homotopy）分解為 餘纖維 → 弱等價 → 纖維
- 餘纖維與弱等價、弱等價與纖維、餘纖維與纖維之間存在適當的提升性質

---

## 3. 餘纖維（Cofibration）測試

### 3.1 測試內容 (`TestCofibration`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 餘纖維的建立，確認 `source` 和 `target` 屬性正確 |
| `test_is_cofibration` | 確認對象確實被識別為餘纖維 |
| `test_is_acyclic` | 檢測餘纖維是否為**非循環**（acyclic）的 |

### 3.2 數學原理

**餘纖維**的直觀意義是「單純嵌入」：

```
i: A → B
```

在拓撲範疇中，餘纖維對應於閉包嵌入（如 CW 複形的子複形粘貼）。

**循環餘纖維（acyclic cofibration）** 同時是弱等價的餘纖維，代表「可收縮的子結構」。在模型範疇的語境中：

- **餘纖維 + 弱等價 = 循環餘纖維**
- 餘纖維保持「下層結構」
- 循環餘纖維可以在同倫意義下「壓縮」掉

**左提升性質**：對於任意交換圖
```
A → X
↓     ↓
B → Y
```
其中上方為餘纖維、右侧為弱等價，則存在提升態射填補該圖。

---

## 4. 纖維（Fibration）測試

### 4.1 測試內容 (`TestFibration`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 纖維的建立，確認 `source` 和 `target` 屬性 |
| `test_is_fibration` | 確認對象被正確識別為纖維 |
| `test_is_acyclic` | 檢測纖維是否為**非循環**的 |

### 4.2 數學原理

**纖維**的直觀意義是「局部平凡的投影」：

```
p: E → B
```

在拓撲範疇中，纖維是局部平凡的覆疊推廣（如 Serre 纖維化）。

**循環纖維（acyclic fibration）** 同時是弱等價的纖維：

- **纖維 + 弱等價 = 循環纖維**
- 纖維保證「整體結構可由纖維重建」
- 循環纖維是可縮去的「冗餘」纖維結構

**右提升性質**：對於任意交換圖
```
A → X
↓     ↓
B → Y
```
其中左侧為弱等價、下方為纖維，則存在提升態射填補該圖。

---

## 5. 弱等價（Weak Equivalence）測試

### 5.1 測試內容 (`TestWeakEquivalence`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 弱等價的建立，確認 `source` 和 `target` 屬性 |
| `test_is_weak_equivalence` | 確認對象被正確識別為弱等價 |

### 5.2 數學原理

**弱等價**是同倫論中最核心的概念——它標識了在同倫意義下「相同」的物件。

在同倫範疇中，我們並不比較物件本身，而是比較它們的同倫類型。兩個物件 $A$ 和 $B$ 弱等價意味著：

$$\exists \text{ path-connected space } W: A \xleftarrow{\sim} W \xrightarrow{\sim} B$$

其中 $\xleftarrow{\sim}$ 和 $\xrightarrow{\sim}$ 都是弱等價。

**弱等價的關鍵特性**：

1. **同倫不變性**：若 $A \sim B$（同倫等價），則必為弱等價
2. **2-out-of-3 性質**：若其中兩個態射合成是弱等價，則第三個也是
3. **局部化**：在同倫範疇中，弱等價被反轉為同構

**Whitehead 定理**（測試中有驗證）：在 CW 複形範疇中，弱等價蘊含同倫等價。

---

## 6. Quillen 伴隨函子測試

### 6.1 測試內容 (`TestQuillenAdjunction`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 建立左右伴隨函子對 |
| `test_preserves_cofibrations` | 驗證左伴隨保持餘纖維 |
| `test_is_quillen_adjunction` | 確認為合法的 Quillen 伴隨 |
| `test_derived_left_adjoint` | 構造左導出函子 |
| `test_derived_right_adjoint` | 構造右導出函子 |

### 6.2 數學原理

**Quillen 伴隨**是模型範疇間的「好」函子對：

$$F \dashv G: \mathcal{C} \to \mathcal{D}$$

稱為 Quillen 伴隨，若：
- $F$（左伴隨）保持餘纖維和弱等價（或者...
- $G$（右伴隨）保持纖維和弱等價）

導出函子是「推過局部化」的函子：
- **左導出函子** $LF$: 先因子分解再套用 $F$
- **右導出函子** $RG$: 先因子分解再套用 $G$

---

## 7. 同倫範疇與同倫等價測試

### 7.1 同倫範疇 (`TestHomotopyCategory`)

- **建立**：從模型範疇構造同倫範疇
- **局部化**：`localize_at_W()` 在弱等價類別 $W$ 處局部化
- **同倫集**：`hom_set` 計算同倫類別中的態射集

### 7.2 同倫等價 (`TestHomotopyEquivalence`)

- 檢驗一對態射是否互為同倫逆
- `inverse()` 構造同倫逆

---

## 8. 弱因子分解系統測試 (`TestWeakFactorizationSystem`)

任意態射 $f: A → B$ 可唯一分解為：

$$A \xrightarrow{i} W \xrightarrow{p} B$$

其中 $i$ 是餘纖維，$p$ 是纖維，且至少有一者是弱等價。

測試驗證：
- **建立**：左右類別（餘纖維/纖維）的建立
- **因子分解**：任意態射可分解
- **提升性質**：左右類別之間的提升性質

---

## 9. CW 複形與胞腔同倫測試

### 9.1 CW 複形 (`TestCWComplex`)

- **胞腔添加**：`add_cell(dim, label)` 添加 $n$ 胞腔
- **胞腔粘貼**：`attach_cell` 定義粘貼映射
- **同調群**：`homology(n)` 計算 $n$ 維同調群
- **歐拉示性數**：`euler_characteristic()` 計算 $\chi = \sum (-1)^n f_n$

### 9.2 同倫正合擴張 (`TestHomotopyCoherent`)

- **$n$ 骨架**：`n_skeleton(n)` 計算 $n$ 骨架
- **幾何實現**：`geometric_realization()` 將單純集合實現為拓撲空間

### 9.3 無擴張 (`TestAnodyneExtension`)

驗證「無擴張」——可由基本無擴張生成的相對胞腔複合

---

## 10. 單純模型範疇測試 (`TestSimplicialModelCategory`)

單純模型範疇同時是單純集合豐富的：

- **映射空間**：`mapping_space(X, Y)` 計算内部 Hom
- **張量積**：`tensor(X, K)` 與單純集合的協同作用
- **余張量積**：`cotensor(X, K)` 對偶於張量

---

## 11. Whitehead 定理測試

`TestWhiteheadTheorem.from_CW_to_CW`

**Whitehead 定理**：在 CW 複形範疇中，弱等價 ⟹ 同倫等價

此定理說明 CW 複形的同倫類型由其同倫群完全決定。

---

## 12. 測試架構總結

```
test_model_category.py
├── TestModelCategory          # 基本結構
├── TestCofibration            # 餘纖維
├── TestFibration              # 纖維
├── TestWeakEquivalence        # 弱等價
├── TestQuillenAdjunction      # Quillen 伴隨
├── TestHomotopyCategory       # 同倫範疇
├── TestHomotopyEquivalence    # 同倫等價
├── TestWeakFactorizationSystem # 因子分解系統
├── TestCWComplex              # CW 複形
├── TestHomotopyCoherent       # 同倫正合
├── TestAnodyneExtension        # 無擴張
├── TestSimplicialModelCategory # 單純豐富結構
└── TestWhiteheadTheorem        # Whitehead 定理
```

---

## 參考數學背景

- **Quillen, D.** *Homotopical Algebra*, Springer LNMA 43, 1967
- **Hovey, M.** *Model Categories*, AMS 1999
- **Goerss, P. & Jardine, J.** *Simplicial Homotopy Theory*, Birkhäuser 2009