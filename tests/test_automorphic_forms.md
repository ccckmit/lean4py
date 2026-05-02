# 自動化形式測試文檔 (test_automorphic_forms.md)

## 概述

本測試文件用於驗證 `lean4py.automorphic_forms` 模塊的數學對象，包括自動化形式、Hecke 算子、Langlands 函子性猜想和 L-函數。

---

## 1. 測試驗證內容

### 1.1 AutomorphicForm 類別測試

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建指定 weight 的 GL(2) 群上的自動化形式 |
| `test_evaluate` | 在純虛數點 z = i 處求值，返回複數類型 |
| `test_is_automorphic` | 驗證變換定律是否滿足自動化條件 |

---

## 2. 模塊形式測試 (Modular Form Tests)

### 數學原理

模塊形式是滿足特定變換定律的全純函數，定義在上半平面上：

```
f(az + b / cz + d) = (cz + d)^k f(z)
```

其中矩陣 $\begin{pmatrix} a & b \\ c & d \end{pmatrix} \in SL(2, \mathbb{Z})$，權重為 $k$。

### 測試 `test_is_automorphic`

此測試驗證 `AutomorphicForm.is_automorphic()` 方法返回 `True`，確認對象滿足自動化形式的定義條件。

---

## 3. Hecke 算子測試 (Hecke Operator Tests)

### 數學原理

Hecke 算子 $T_n$ 是模塊形式空間上的重要線性算子，定義為：

```
T_n(f)(z) = n^{k-1} ∑_{d|n} ∑_{b=0}^{d-1} f((az + b)/d)
```

其中求和遍歷所有 $ad = n$ 的因子對。

### 測試 `test_apply`

驗證 `HeckeOperatorGeneral.apply(n, f)` 返回包含 `operator` 鍵的字典，表示 $T_n$ 作用於形式 $f$。

### 測試 `test_eigenvalues`

驗證 `HeckeOperatorGeneral.eigenvalues(f, n)` 返回特徵值列表。Hecke 算子的特徵形式構成模空間的基底。

---

## 4. L-函數測試 (L-Series Tests)

### 數學原理

L-函數是將模塊形式與解析數論聯繫起來的橋樑。對於權重為 $k$ 的尖點形式 $f$，其 L-函數定義為：

```
L(s, f) = ∑_{n=1}^∞ a_n / n^s
```

其中 $a_n$ 為 Fourier 係數。

### 測試 `test_compute`

驗證 `LFunction.compute(f, s)` 在給定複參數 $s$ 處計算 L-函數值，返回複數結果。

### 測試 `test_analytic_continuation`

驗證 `LFunction.analytic_continuation(f)` 返回 `True`。L-函數的解析延拓是數論中的核心定理（Riemann ζ 函數的解析延拓）。

---

## 5. Langlands 函子性測試 (Langlands Functoriality Tests)

### 數學原理

Langlands 猜想是現代數論的核心統一理論，斷言：

> 從低維群到高維群的保持局部與全局特性的對應關係

對於 GL(2) 到 GL(3) 的提升，存在確切的構造和驗證方法。

### 測試 `test_transfer`

驗證 `LanglandsFunctioriality.transfer(source, target, form)` 返回包含源群、目標群信息的字典。

### 測試 `test_holds`

驗證 `LanglandsFunctioriality.holds()` 返回 `True`，確認函子性原理成立。

---

## 測試執行

```bash
pytest tests/test_automorphic_forms.py -v
```

---

## 模塊結構

```
lean4py/
└── automorphic_forms.py    # 包含 AutomorphicForm, HeckeOperatorGeneral,
                             # LanglandsFunctioriality, LFunction 四個類別
```