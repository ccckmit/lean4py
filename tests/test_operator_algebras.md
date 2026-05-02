# 算子代數測試文檔

本文檔說明 `test_operator_algebras.py` 中測試用例背後的數學原理。

## 1. 測試概述

本測試文件驗證了算子代數模組的核心功能，涵蓋賦範空間、Hilbert 空間、有界算子、C*-代數、von Neumann 代數、譜理論、泛函演算、K-理論和指標理論。

## 2. C*-代數測試 (`TestCStarAlgebra`)

### 數學原理

C*-代數是具有以下結構的Banach代數：

1. **Banach 空間結構**：配備範數，關於範數完備
2. **代數結構**：封閉於加法、純量乘法和乘法
3. **對合結構**：存在對合運算 `*`，滿足 `(a*)* = a`、`(ab)* = b*a*`、`(a+b)* = a* + b*`
4. **C*-性子**：滿足 `||a*a|| = ||a||²`

### 測試驗證

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | C*-代數的基本 creation，包含載體集合、乘法、範數和對合 |
| `test_is_cstar` | 驗證代數滿足 C*-條件 |
| `test_is_commutative` | 驗證代數是否為交換的 |

## 3. Von Neumann 代數測試 (`TestVonNeumannAlgebra`)

### 數學原理

von Neumann 代數是作用於 Hilbert 空間上的 *-代數的弱閉子集，也稱為「算子代數」。

**雙交換子定理**：對於 Hilbert 空間 H 上的有界算子代數 M，有：
```
M = M''
```
其中 M' 為 M 的交換子（與 M 中所有算子交換的算子集合），M'' 為 M' 的交換子。

**基本性質**：
- von Neumann 代數在弱算子拓撲下閉合
- 也是強算子拓撲下閉合
- 包含單位元

### 測試驗證

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證 von Neumann 代數的 creation，包含算子集合和底層 Hilbert 空間 |
| `test_commutant` | 驗證交換子運算 `commutant()` 的正確性 |
| `test_is_vonneumann` | 驗證代數是否為 von Neumann 代數 |

## 4. 正元素測試 (`TestPositiveElement`)

### 數學原理

在 C*-代數中，正元素的定義基於譜性質：

**定義**：C*-代數 A 中的元素 a 稱為正元素，記作 a ≥ 0，若 a = b*b 對某個 b ∈ A 成立。

**等價條件**：
- a 是正元素
- a 的譜 σ(a) 包含於 [0, ∞)
- 存在唯一的正平方根 a^(1/2)
- 對所有狀態 φ，有 φ(a) ≥ 0

**正元素 ordering**：對於 Hermitian 元素 a, b，a ≤ b 當且僅當 b - a 是正元素。

### 測試驗證

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證正元素物件的 creation，包含元素值和所屬 C*-代數 |
| `test_is_positive` | 驗證 `is_positive()` 方法正確判斷元素是否為正 |

## 5. 其他重要測試類別

### 賦範空間 (`TestNormedSpace`)

賦範空間是配備範數的向量空間，測試驗證：
- 範數的定義和計算 (`norm`)
- 空間的完備性 (`is_complete`)
- 範數的可加性 (`norm_of_sum`)

### Hilbert 空間 (`TestHilbertSpace`)

Hilbert 空間是配備內積的完備向量空間，測試驗證：
- 內積結構的正確性
- Hilbert 空間公理的滿足 (`is_hilbert`)

### 有界算子 (`TestBoundedOperator`)

有界線性算子是 Banach 空間之間的連續線性映射，測試驗證：
- 算子的 creation 和矩陣表示
- 算子範數的計算 (`norm`)
- 伴隨算子的存在性 (`adjoint`)

### 譜定理 (`TestSpectralTheorem`)

譜定理將自伴算子與乘法算子聯繫起來，測試驗證：
- 譜的計算 (`spectrum`)
- 泛函演算 (`functional_calculus`)

### K-理論 (`TestK0Group`, `TestK1Group`)

K-理論是 C*-代數的拓撲不變量，測試驗證：
- K0 群包含投射元的等价類
- K1 群包含單元元的等价類

### 指數理論 (`TestIndexTheory`)

指數理論研究 Fredholm 算子的指標，測試驗證：
- 核空間維度 (`kernel_dimension`)
- 餘核空間維度 (`cokernel_dimension`)
- Fredholm 性 (`is_fredholm`)

## 6. 測試設計原則

測試採用**最小範例**策略：
- 使用最簡單的集合（如 `{1}`）和最基本的結構
- 集中驗證核心接口和方法的存在性
- 不過度關注計算結果的數值精確性

這與形式化數學的測試方法一致，確保每個數學對象的基本性質得到驗證。