# 模形式測試文檔 (test_modular_forms.py v1.29)

本文檔說明 `test_modular_forms.py` 中測試案例的數學原理。

---

## 1. 測試驗證的內容概述

本測試文件驗證 `lean4py.modular_forms` 模塊的核心功能，包括：

- **模形式（ModularForm）**：權重為 k 的複變函數，在上半平面具有良好的全純性與變換性質
- **權重（Weight）**：模形式的基本不變量
- **Hecke 算子**：保持模形式空間結構的線性算子
- **模曲線（ModularCurve）**：由模群作用商掉的緊湊化曲面
- **尖點形式（CuspForm）**：在所有尖點處消失的模形式

---

## 2. 模群測試（TestModularForm）

### 數學原理

模形式是定義在上半平面 $\mathbb{H} = \{z \in \mathbb{C} : \text{Im}(z) > 0\}$ 上的全純函數，需滿足模群 $SL(2, \mathbb{Z})$ 的變換法則：

$$f\left(\frac{az + b}{cz + d}\right) = (cz + d)^k f(z)$$

其中 $k \in \mathbb{Z}$ 為權重，矩陣 $\begin{pmatrix} a & b \\ c & d \end{pmatrix} \in SL(2, \mathbb{Z})$。

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 建立權重為 12 的模形式對象，確認 `weight` 屬性正確 |
| `test_evaluate` | 在純虛數點 $z = i$ 處求值，返回複數類型 |
| `test_is_modular` | 檢驗模形式的變換性質是否成立 |

---

## 3. Eisenstein 級數測試（TestWeight）

### 數學原理

權重 $k$ 是模形式的核心不變量。對於偶數權重 $k \geq 4$，Eisenstein 級數定义为：

$$G_k(z) = \sum_{(c,d) \neq (0,0)} \frac{1}{(cz + d)^k}$$

其 Fourier 展開係數涉及除數函數 $\sigma_{k-1}(n)$。權重必須為偶數是因為模形式空間的基本性質。

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_get` | 從模形式對象提取權重值 |
| `test_is_even` | 判斷權重是否為偶數：12 返回 True，13 返回 False |

---

## 4. 尖點形式測試（TestCuspForm）

### 數學原理

尖點形式是特殊的模形式，在所有尖點處趨於零。對於權重為 $k$ 的尖點形式空間 $S_k(SL(2,\mathbb{Z}))$，其維數公式為：

$$\dim S_k(SL(2,\mathbb{Z})) = \begin{cases} \lfloor k/12 \rfloor & \text{若 } k \not\equiv 2 \pmod{12} \\ \lfloor k/12 \rfloor - 1 & \text{若 } k \equiv 2 \pmod{12} \end{cases}$$

著名的 Ramanujan tau 函數即為權重 12 尖點形式 $\Delta(z)$ 的 Fourier 係數。

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_is_cusp_form` | 判斷模形式是否為尖點形式（即在各尖點處為零） |
| `test_dimension` | 計算權重 12 尖點形式空間的維數 |

---

## 5. Hecke 算子測試（TestHeckeOperator）

### 數學原理

對於權重為 $k$ 的模形式 $f$，Hecke 算子 $T_n$ 的作用定義為：

$$(T_n f)(z) = n^{k-1} \sum_{ad=n} \sum_{b=0}^{d-1} f\left(\frac{az + b}{d}\right)$$

Hecke 算子是自伴算子（對於 Petersson 內積），其本徵形式構成 Hecke 基。$T_n$ 的本徵值滿足乘法性：
$$T_m T_n = T_{mn} \quad \text{若 } (m,n) = 1$$

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_apply` | 對模形式施加 $T_5$ 算子，返回包含算子名稱和權重的字典 |
| `test_eigenvalues` | 計算 $T_5$ 的本徵值列表 |

---

## 6. 模曲線測試（TestModularCurve）

### 數學原理

模曲線是模群 $\Gamma$ 作用於上半平面的商空間：

$$X(\Gamma) = \Gamma \setminus \mathbb{H}^*$$

其中 $\mathbb{H}^* = \mathbb{H} \cup \mathbb{Q} \cup \{\infty\}$ 為紧化上半平面。尖點對應於有理點。$SL(2,\mathbb{Z})$ 的情形：
- $Y(SL(2,\mathbb{Z})) = SL(2,\mathbb{Z}) \setminus \mathbb{H}$ 同構於仿射直線
- $X(SL(2,\mathbb{Z}))$ 緊化後為 Riemann 球面，虧格為 0

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_compactification` | 返回緊化模曲線的名稱（如 $X(SL_2\mathbb{Z})$） |
| `test_genus` | 計算模曲線的虧格（對於 $SL(2,\mathbb{Z})$ 為 0） |

---

## 測試架構

```
TestModularForm      → 模形式基本性質
TestWeight           → 權重處理與奇偶性
TestHeckeOperator    → Hecke 算子作用與本徵值
TestModularCurve     → 模曲線幾何不變量
TestCuspForm         → 尖點形式判別與維數
```

所有測試均基於 `lean4py.modular_forms` 模塊實現，反映 mathlib4 中 `Mathlib.ModularForms` 的核心結構。