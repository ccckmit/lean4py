# 自由概率測試文檔

本文檔說明 `test_free_probability.py` 中測試用例的數學原理。

## 1. 測試驗證的內容

本模組測試自由概率（Free Probability）與非交換幾何的核心概念，包括：
- 自由概率空間的創建與基本運算
- 自由隨機變量的構建與累積量計算
- 自由中心極限定理與半圓分布
- Marchenko-Pastur 分布（自由泊松分布）
- 自由卷積運算
- 非交換空間與譜三元組

---

## 2. 自由隨機變量測試

### 測試類別：`TestFreeRandomVariable`

### 數學原理

自由隨機變量是自由概率論中的基本對象。對於給定的分布函數和累積量序列：

```
X ~ FreeRandomVariable(distribution, [κ₁, κ₂, ..., κₙ])
```

**自由累積量（Free Cumulants）** 是自由概率論的核心工具：
- κ₁ = E[X]（一階累積量 = 期望值）
- κ₂ = Var(X)（二階累積量 = 方差）

測試驗證：
- `test_creation`：確認自由隨機變量可通過分布函數和累積量列表創建
- `test_free_cumulants`：確認 `free_cumulants()` 方法返回正確的累積量序列 `[0, 1]`

---

## 3. 自由卷積測試

### 測試類別：`TestFreeConvolution`

### 數學原理

**自由卷積（Free Convolution）** ⊞ 是獨立自由隨機變量之和的分布運算：

若 X ⊥ Y（自由獨立），則 X + Y 的分布為 μ ⊞ ν

自由卷積的計算通過**R-變換（R-transform）**實現：
- R_X(z) 為自由累積量的生成函數
- R_{X⊞Y}(z) = R_X(z) + R_Y(z)

測試 `test_convolve` 驗證 `FreeConvolution.convolve(mu, nu)` 方法存在且可執行。

---

## 4. R-變換測試

### 測試覆蓋範圍

R-變換的相關測試體現在以下類別中：

#### `TestFreeCentralLimitTheorem`

**自由中心極限定理（Free CLT）**

在經典概率論中，n 個獨立同分布隨機變量之和趨近於正態（高斯）分布。

在自由概率論中，對應的極限分布是**半圓分布（Semicircle Distribution）**：

```
density(x) = (1/2π)√(4 - x²),  for |x| ≤ 2
```

數學表述：對於自由獨立的.centered隨機變量 X₁, X₂, ..., Xₙ（具有有限方差），
當 n → ∞ 時，(X₁ + ... + Xₙ)/√n 的分布趨近於參數為 [0, 1] 的半圓分布。

測試驗證：
- `test_limit_distribution`：確認 `limit_distribution()` 返回 `FreeRandomVariable` 類型
- 半圓分布的支撐區間為 [-2, 2]

#### `TestMarchenkoPastur`（隱式 R-變換測試）

**Marchenko-Pastur 分布**是自由概率論中對應經典泊松分布的極限分布，也稱為**自由泊松分布（Free Poisson Distribution）**。

參數：
- λ：泊松參數（arrival rate）
- λ ≤ 1 時：分布集中在 [0, (1+√λ)²]
- λ > 1 時：點 mass 在 0 處

支撐區間：
```
a = λ(1 - √r)²,  b = λ(1 + √r)²
其中 r = λ_param / ratio
```

密度函數：
```
f(x) = √((b-x)(x-a)) / (2πλx),  for a < x < b
```

測試驗證：
- `test_support`：確認支撐區間左端點 ≥ 0，右端點 > 左端點
- `test_density_inside`：區間內部密度 > 0
- `test_density_outside`：區間外部密度 = 0

---

## 5. 自由獨立性測試

### 測試類別：`TestFreeProbabilitySpace`

### 數學原理

**自由概率空間** 記為 (A, φ)，其中：
- A：非交換代數（類似於隨機變量的集合）
- φ：線性泛函（跡 / 期待值）

**自由獨立（Free Independence）** 的定義：

對於 A 中的子代數 A₁, A₂, ..., Aₙ，若對所有滿足：
- a₁ ∈ A_{i₁}, a₂ ∈ A_{i₂}, ..., a_k ∈ A_{i_k}
- φ(a_j) = 0
- i₁ ≠ i₂, i₂ ≠ i₃, ..., i_{k-1} ≠ i_k

均有 φ(a₁a₂...a_k) = 0，則稱這些子代數是**自由獨立**的。

這與經典概率論中的獨立性不同，基於累積量的加性：
- 經典獨立 → 累積量相乘
- 自由獨立 → R-變換相加

測試驗證：
- `test_creation`：確認空間可通過代數和態（state）創建
- `test_expectation`：確認 φ(x) 返回正確的期待值
- `test_variance`：確認 Var(x) = φ(x²) - φ(x)² 計算正確

---

## 6. 非交換幾何與譜三元組測試

### 測試類別：`TestSpectralTriple`, `TestConnesDifferential`, `TestSpectralFlow`, `TestFredholmModule`

### 數學原理

**譜三元組（Spectral Triple）** (A, H, D) 是非交換幾何的基本結構：
- A：光滑代數（作用在希爾伯特空間上的表示）
- H：希爾伯特空間
- D：狄拉克算子（自伴算子，帶有緊致預解式）

**Connes 微分**：
對於譜三元組，元素 a 的微分定義為：
```
da = [D, a]
```

**zeta 函數**：
```
ζ_D(s) = Tr(|D|^{-s})
```
用於定義非交換幾何中的距離和熱核。

**譜流（Spectral Flow）**：
沿著希爾伯特空間中算子族的譜缺口穿越的代數不變量。

**Fredholm 模**：
滿足 [F, a] 緊致的 Fredholm 算子，用於定義指標理論。

---

## 7. 總結

| 測試類別 | 驗證內容 | 核心數學概念 |
|---------|---------|------------|
| TestFreeProbabilitySpace | 概率空間的創建與基本運算 | (A, φ) 結構 |
| TestFreeRandomVariable | 自由隨機變量的累積量 | 自由累積量 κₙ |
| TestFreeCentralLimitTheorem | 自由CLT與半圓分布 | 半圓定律 |
| TestMarchenkoPastur | 自由泊松分布 | MP分布、支撐區間、密度 |
| TestFreeConvolution | 自由卷積運算 | R-變換加性 |
| TestNoncommutativeSpace | 非交換空間結構 | 譜三元組 |
| TestSpectralTriple | 譜三元組與zeta函數 | Connes- Moscovici 局部指標公式 |

---

## 參考文獻

- Voiculescu, D.V. (1986). Addition of certain noncommuting random variables. *J. Funct. Anal.*
- Marchenko, V.A.; Pastur, L.A. (1967). Distribution of eigenvalues for some sets of random matrices. *Mat. Sb.*
- Connes, A. (1994). *Noncommutative Geometry*. Academic Press.