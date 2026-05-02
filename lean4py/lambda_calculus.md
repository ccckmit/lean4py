# Lambda Calculus 數學原理

Lambda 演算是一套由 Alonzo Church 在 1930 年代建立的形式系統，作為計算的數學模型。本模組 imitates mathlib4 Mathlib.Logic.LambdaCalculus，實現了 Lambda 演算的核心概念。

## 1. Lambda 演算語法

Lambda 項（Lambda Term）由三種結構組成：

### 1.1 變量 (Variable)
```
x, y, z, ...
```
變量是最基本的項，表示一個未指定的值。

### 1.2 Lambda 抽象 (Abstraction)
```
λx.M
```
表示一個函數，其中 `x` 是約束變量（bound variable），`M` 是函數體（body）。

### 1.3 應用 (Application)
```
M N
```
表示將函數 `M` 應用於參數 `N`。

## 2. 自由變量與約束變量

### 2.1 自由變量 (Free Variables)

在表達式中，**自由變量**是不被任何 λ 約束的變量。

```
FV(x) = {x}
FV(λx.M) = FV(M) \ {x}
FV(M N) = FV(M) ∪ FV(N)
```

### 2.2 約束變量 (Bound Variables)

**約束變量**是被 λ 綁定的變量。

```
BV(λx.M) = BV(M) ∪ {x}
```

### 2.3 封閉項 (Closed Term / Combinator)

沒有自由變量的項稱為**封閉項**或**組合子**。

## 3. β-歸約 (β-Reduction)

β-歸約是 Lambda 演算的核心計算規則。

### 3.1 定義

```
(λx.M) N → M[x:=N]
```

含義：將抽象 `λx.M` 應用於參數 `N` 時，將函數體中的所有自由變量 `x` 替換為 `N`。

### 3.2 替換規則 (Substitution)

替換 `M[x:=N]` 需要小心處理：

1. 替換時不能捕獲自由變量
2. 需要時須先進行 α-轉換

```
x[x:=N] = N
y[x:=N] = y  (若 x ≠ y)
(M1 M2)[x:=N] = M1[x:=N] M2[x:=N]
(λy.M)[x:=N] = λy.(M[x:=N])  (若 x ≠ y 且 y 不在 FV(N) 中)
```

## 4. α-轉換 (α-Conversion)

α-轉換允許重命名約束變量。

### 4.1 定義

```
λx.M ≡ λy.M[x:=y]
```

前提：`y` 不在 `FV(M)` 中。

### 4.2 目的

避免替換時的**變量捕捉**（Variable Capture）問題。

例如：
```
(λx.λy.x) y  →  不直接替換
(λx.λz.x) y  →  α-轉換後再 β-歸約
```

## 5. η-轉換 (η-Conversion)

η-轉換描述擴展外延性：

```
λx. (M x) ≡ M   當 x ∉ FV(M)
```

左邊是「接受一個參數 x 並應用 M」的函數，右邊是 M 本身（前提是 x 不在 M 的自由變量中）。

## 6. Church-Rosser 定理與合併性

### 6.1 Church-Rosser 定理

若 `M →* N₁` 且 `M →* N₂`，則存在項 `P` 使得：
```
N₁ →* P  且  N₂ →* P
```

即：無論沿哪條歸約路徑，最終都會匯聚到同一個項。

### 6.2 合併性 (Confluence)

Church-Rosser 定理保證了 β-歸約的**合併性**：從同一項出發的不同歸約序列，最終會收斂。

### 6.3 正規形式 (Normal Form)

若一個項不能再進行任何 β-歸約，則稱其為**正規形式**。

## 7. 不動點組合子 Y

Y 組合子提供了解決遞歸問題的方法。

### 7.1 定義

```
Y = λf.(λx.f(x x)) (λx.f(x x))
```

### 7.2 性質

```
Y F
= (λf.(λx.f(x x)) (λx.f(x x))) F
→ (λx.F(x x)) (λx.F(x x))
→ F((λx.F(x x)) (λx.F(x x)))
= F(Y F)
```

因此 `Y F` 是 `F` 的**最小不動點**。

### 7.3 應用：實現遞歸

```
fact = Y (λf.λn. if n=0 then 1 else n * f(n-1))
```

## 8. Church 編碼

Church 編碼使用 Lambda 演算表示常見的數據結構。

### 8.1 布爾值

```
true = λa.λb.a
false = λa.λb.b
if = λp.λa.λb.p a b
```

### 8.2 自然數（Church 數）

```
0 = λf.λx.x
1 = λf.λx.f x
2 = λf.λx.f(f x)
3 = λf.λx.f(f(f x))
...
n = λf.λx.fⁿ(x)
```

### 8.3 後繼函數

```
succ = λn.λf.λx.f(n f x)
```

### 8.4 加法與乘法

```
add = λm.λn.λf.λx.m f (n f x)
mul = λm.λn.λf.m (n f)
```

### 8.5 遞歸與階乘

使用 Y 組合子實現：
```
fact = Y (λf.λn. (iszero n) 1 (mul n (f (pred n))))
```

## 9. 正規形式與求值策略

### 9.1 正規形式

項不能再進行 β-歸約時達到的形式。

### 9.2 求值策略

| 策略 | 描述 |
|------|------|
| **正規順序** (Normal Order) | 最左最外最先，總是找到正規形式（若存在） |
| **應用順序** (Applicative Order) | 最左最先，先求值參數再應用 |
| **惰性求值** (Lazy Evaluation) | 按需計算，避免重複計算 |

### 9.3 終止性

並非所有項都有正規形式：

```
Ω = (λx.x x) (λx.x x) → (λx.x x) (λx.x x) → ...
```

這個項會無限期地進行 β-歸約。

## 模組結構

本模組 `lean4py/lambda_calculus.py` 包含以下類：

| 類 | 功能 |
|----|------|
| `LambdaTerm` | 創建變量、抽象、應用的工廠方法 |
| `BetaReduction` | β-歸約與 Church-Rosser 性質 |
| `SimplyTypedLambda` | 簡單類型 Lambda 演算 |
| `ChurchNumerals` | Church 數字編碼與解碼 |

## 參考文獻

1. Church, A. (1936). An Unsolvable Problem of Elementary Number Theory.
2. Barendregt, H.P. (1984). The Lambda Calculus: Its Syntax and Semantics.
3. Hindley, J.R. & Seldin, J.P. (2008). Lambda-Calculus and Combinators.