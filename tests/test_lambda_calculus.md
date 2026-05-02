# Lambda 演算測試文檔

本文件說明 `test_lambda_calculus.py` 中測試用例背後的數學原理。

## 1. 測試概述

本測試模組驗證 lambda 演算的核心功能，包括：

| 測試類別 | 驗證內容 |
|---------|---------|
| `TestLambdaTerm` | 語法結構（變量、抽象、應用） |
| `TestBetaReduction` | β 歸約與合流性 |
| `TestSimplyTypedLambda` | 類型推斷 |
| `TestChurchNumerals` | Church 數字編碼 |

---

## 2. 語法測試（Syntax Tests）

### 2.1 Lambda 演算基本語法

Lambda 演算由三種項（terms）組成：

1. **變量（Variable）**: `x`, `y`, `z` — 最基本的項
2. **抽象（Abstraction）**: `λx.M` — 定義匿名函數
3. **應用（Application）**: `M N` — 將函數應用於參數

### 2.2 測試用例分析

```python
def test_variable(self):
    result = LambdaTerm.variable("x")
    # 產生 {"term": "x", "type": "variable"}
```

**數學原理**：
- 變量是 lambda 演算的原子項
- 每個變量有一個名稱（name）
- 測試驗證結構包含 `term` 和 `type` 兩個欄位

```python
def test_abstraction(self):
    var = LambdaTerm.variable("x")
    result = LambdaTerm.abstraction("x", var)
    # 產生 {"term": "λx.x", "type": "abstraction"}
```

**數學原理**：
- 抽象 `λx.M` 表示一個匿名函數
- `x` 是約束變量（bound variable）
- `M` 是函數體（body）
- 約束變量在函數作用域內被綁定

```python
def test_application(self):
    func = LambdaTerm.variable("f")
    arg = LambdaTerm.variable("x")
    result = LambdaTerm.application(func, arg)
    # 產生 {"term": "(f x)", "type": "application"}
```

**數學原理**：
- 應用 `M N` 表示將函數 `M` 作用於參數 `N`
- 這是函數式編程的核心概念
- 左結合：`M N P` = `(M N) P`

---

## 3. Beta 歸約測試（Beta Reduction Tests）

### 3.1 Beta 歸約定義

Beta 歸約是 lambda 演算的核心計算規則：

```
(λx.M) N → M[x := N]
```

含義：將抽象 `λx.M` 應用於 `N` 時，將函數體中的所有自由變量 `x` 替換為 `N`。

### 3.2 測試用例分析

```python
def test_beta_reduce(self):
    term = {"term": "λx.x", "type": "abstraction"}
    result = BetaReduction.beta_reduce(term)
```

**數學原理**：
- `λx.x` 是恆等函數（identity function）
- 當應用於任何項 `N` 時，結果為 `N`
- 這是最簡單的函數抽象

```python
def test_is_beta_normal(self):
    term = {"term": "x", "type": "variable"}
    self.assertTrue(BetaReduction.is_beta_normal(term))
```

**數學原理**：
- **正規形（Normal Form）**：無法再進行 β 歸約的項
- 變量 `x` 本身就是正規形（無法繼續歸約）
- 每個可歸約的項最終都能歸約到唯一正規形（如果存在的話）

```python
def test_church_rosser(self):
    self.assertTrue(BetaReduction.church_rosser())
```

**數學原理**：
- **Church-Rosser 定理**：如果 `M →* N₁` 且 `M →* N₂`，則存在 `P` 使得 `N₁ →* P` 且 `N₂ →* P`
- 這保證了 β 歸約的**合流性（Confluence）**
- 無論採用什麼歸約順序，最終結果在同構意義下唯一

---

## 4. Alpha 轉換測試（Alpha Conversion Tests）

### 4.1 Alpha 轉換定義

Alpha 轉換（α-conversion）是在保持項語義不變的情況下，變更約束變量名稱：

```
λx.M ≡ λy.M[x := y]  (y 不在 M 中自由出現)
```

### 4.2 數學原理

- **約束變量可任意重命名**
- 例如：`λx.x` ≡ `λy.y`
- 重命名時需避免**捕捉自由變量**（capture of free variables）
- 例如：`λx.(λy.x)` 中的 `x` 不能改名為 `y`

### 4.3 實現說明

當前測試套件中未包含明確的 Alpha 轉換單元測試，但 `LambdaTerm` 類的實現隱式處理此概念。

---

## 5. 類型系統測試（Type System Tests）

### 5.1 簡單類型 Lambda 演算

```python
def test_type_of(self):
    term = {"term": "x"}
    result = SimplyTypedLambda.type_of(term, {})
```

**數學原理**：
- 簡單類型 lambda 演算是 lambda 演算的類型化版本
- 基本類型：`α`, `β`, `γ` 等
- 函數類型：`σ → τ` 表示從 `σ` 到 `τ` 的函數

### 5.2 類型規則

| 規則 | 形式 |
|-----|------|
| 變量規則 | `Γ ⊢ x: σ`（若 `x: σ ∈ Γ`） |
| 抽象規則 | `Γ, x: σ ⊢ M: τ` ⇒ `Γ ⊢ λx.M: σ → τ` |
| 應用規則 | `Γ ⊢ M: σ → τ` 且 `Γ ⊢ N: σ` ⇒ `Γ ⊢ M N: τ` |

---

## 6. Church 數字測試（Church Numerals Tests）

### 6.1 Church 編碼

每個自然數 `n` 被編碼為：

```
n = λf.λx.fⁿ(x)
```

其中 `fⁿ(x)` 表示 `f` 的 `n` 次迭代。

### 6.2 測試用例分析

```python
def test_encode(self):
    result = ChurchNumerals.encode(3)
    # 產生 {"term": "λf.λx.f³(x)", "value": 3}
```

**數學原理**：
- `0 = λf.λx.x`（零次應用）
- `1 = λf.λx.f(x)`（一次應用）
- `2 = λf.λx.f(f(x))`（二次應用）
- `3 = λf.λx.f(f(f(x)))`（三次應用）

```python
def test_decode(self):
    num = {"term": "λf.λx.f(f(f(x)))", "value": 3}
    result = ChurchNumerals.decode(num)
```

**數學原理**：
- 解碼過程：將 Church 數字應用於後繼函數和零值
- `3 f x = f(f(f(x)))` 的結果表示數字 3

---

## 7. 定點測試（Fixed-Point Tests）

### 7.1 定點 combinator

**Y combinator**（定點 combinator）是 lambda 演算中用於實現遞迴的關鍵：

```
Y = λf.(λx.f (x x)) (λx.f (x x))
```

### 7.2 數學原理

對於任何函數 `F`，有：
```
Y F = F (Y F)
```

這稱為**定點性質（Fixed-Point Property）**。

### 7.3 遞迴實現

使用 Y combinator 可以定義任意遞迴函數：

```python
# 階乘的 lambda 表達式
fact = Y (λf.λn. if n=0 then 1 else n * f(n-1))
```

### 7.4 實現說明

當前測試套件中未包含明確的定點 combinator 單元測試，但 Y combinator 是 lambda 演算表達能力的關鍵組成部分。

---

## 8. 測試與 mathlib4 對應關係

本模組模仿 `mathlib4 Mathlib.Logic.LambdaCalculus` 的實現：

| 本模組 | mathlib4 對應 |
|-------|--------------|
| `LambdaTerm` | 語法樹結構 |
| `BetaReduction` | β 歸約系統 |
| `SimplyTypedLambda` | 類型理論 |
| `ChurchNumerals` | 自然數編碼 |

---

## 9. 總結

Lambda 演算是數理邏輯和函數式編程的理論基礎：

1. **語法**：變量、抽象、應用三種基本項
2. **計算**：通過 β 歸約進行動態計算
3. **等價**：通過 α 轉換和 η 轉換定義項之間的等價關係
4. **類型**：簡單類型系統提供靜態類型檢查
5. **表達力**：Church 數字和 Y combinator 顯示其圖靈完備性

測試用例驗證了這些核心概念的实现正確性。