# 局部域測試文檔 (test_local_fields.py)

## 概述

本測試模組基於 `lean4py/local_fields.py` 實現，模仿 mathlib4 的 `Mathlib.NumberTheory.LocalFields` 結構。測試對象為 $\mathbb{Q}_p$ 的有限擴張（即局部域）。

---

## 1. 局部域 (Local Field) 測試

### 1.1 創建測試 (`test_creation`)

**數學原理：**

局部域是離散賦值域的完整化，特別是 $\mathbb{Q}_p$ 的有限擴張。一個局部域 $K$ 由兩個參數確定：
- **p**：特徵為 $p$ 的質數（有理數域 $\mathbb{Q}$ 的 p-進局部域基礎）
- **degree**：擴張次數 $[K : \mathbb{Q}_p]$

**驗證內容：**
- 檢查 `LocalField(5, 2)` 是否正確存儲 `p = 5` 和 `degree = 2`

### 1.2 局部域判定測試 (`test_is_local_field`)

**數學原理：**

局部域 $K$ 是滿足以下條件的域：
1. $K$ 是離散賦值域的交換環
2. $K$ 在其剩餘域上局部域是有限的

對於 $\mathbb{Q}_p$ 的有限擴張，總是滿足局部域的定義。

### 1.3 剩餘域測試 (`test_residue_field`)

**數學原理：**

$$k_K = \mathcal{O}_K / \pi\mathcal{O}_K \cong \mathbb{F}_{p^f}$$

其中：
- $\mathcal{O}_K$ 是估值環（整數環）
- $\pi$ 是一致化元（uniformizer）
- $f$ 是慣性度（inertia degree）

對於 $\mathbb{Q}_p$ 本身，$f = 1$，所以剩餘域是 $\mathbb{F}_p$。對於擴張，$k_K \cong \mathbb{F}_{p^f}$。

---

## 2. 估值環 (Valuation Ring) 測試

### 2.1 計算估值環 (`test_compute`)

**數學原理：**

估值環定義為：
$$\mathcal{O}_K = \{x \in K : v(x) \geq 0\}$$

這是局部域中所有非負 valuation 的元素組成的環。對於 $\mathbb{Q}_p$，估值環是 $\mathbb{Z}_p$（p-進整數環）。

**驗證內容：**
- 返回包含 "ring" 鍵的字典
- 結構為 `{"ring": "O_K", "maximal_ideal": "πO_K"}`

### 2.2 局部環判定 (`test_is_local_ring`)

**數學原理：**

估值環 $\mathcal{O}_K$ 是局部環，意味著它只有唯一一個最大理想 $\mathfrak{m} = \pi\mathcal{O}_K$。這是局部域的核心性質之一。

**驗證內容：**
- 確認 $\mathcal{O}_K$ 是局部環

---

## 3. 一致化元 (Uniformizer) 測試

### 3.1 尋找一致化元 (`test_find`)

**數學原理：**

一致化元 $\pi$ 是滿足 $v(\pi) = 1$ 的元素，其中 $v: K^* \to \mathbb{Z}$ 是離散賦值。對於 $\mathbb{Q}_p$，一致化元就是 $p$ 本身。

**重要性質：**
- $v(\pi) = 1$
- $\pi$ 生成最大理想 $\mathfrak{m}$
- 剩餘域 $k_K = \mathcal{O}_K / (\pi)$

### 3.2 一致化元判定 (`test_is_uniformizer`)

**數學原理：**

一個元素 $\pi \in \mathcal{O}_K$ 是一致化元當且僅當 $v(\pi) = 1$，即它是最大理想的生成元。

**驗證內容：**
- 確認 "p" 被判定為一致化元

---

## 4. 分歧指數 (Ramification Index) 測試

### 4.1 計算分歧指數 (`test_compute`)

**數學原理：**

分歧指數 $e$ 是 valuator groups 的擴張指數：
$$e = [v(K^*) : v(\mathbb{Q}_p^*)]$$

對於 $\mathbb{Q}_p$，$v(\mathbb{Q}_p^*) = \mathbb{Z}$。對於 $K/\mathbb{Q}_p$，$v(K^*)$ 是 $\mathbb{Z}$ 的 $e$ 倍子群。

**基本關係：**
$$[K : \mathbb{Q}_p] = e \cdot f$$

其中 $e$ 是分歧指數，$f$ 是慣性度。

### 4.2 完全分歧判定 (`test_is_totally_ramified`)

**數學原理：**

擴張 $K/\mathbb{Q}_p$ 是**完全分歧**的當且僅當：
$$e = [K : \mathbb{Q}_p]$$

此時 $f = 1$，即剩餘域等於基礎剩餘域 $\mathbb{F}_p$。

---

## 5. 慣性度 (Inertia Degree) 測試

### 5.1 計算慣性度 (`test_compute`)

**數學原理：**

慣性度 $f$ 是剩餘域的擴張次數：
$$f = [k_K : k_{\mathbb{Q}_p}] = [k_K : \mathbb{F}_p]$$

這測量了剩餘域擴張的大小。

**基本關係：**
$$[K : \mathbb{Q}_p] = e \cdot f$$

當 $e = 1$ 時，擴張稱為**非分歧**（unramified）。

### 5.2 完全慣性判定 (`test_is_totally_inert`)

**數學原理：**

擴張 $K/\mathbb{Q}_p$ 是**完全慣性**的當且僅當：
$$f = [K : \mathbb{Q}_p]$$

此時 $e = 1$，即 valuation ring 沒有分歧。

---

## 數學結構總結

```
局部域 K / ℚ_p
├── 分歧指數 e = [v(K*) : v(ℚ_p*)]
├── 慣性度 f = [k_K : k_{ℚ_p}]
└── 擴張次數 [K : ℚ_p] = e × f

估值環 O_K
├── 最大理想 πO_K
├── 一致化元 π (v(π) = 1)
└── 剩餘域 k_K = O_K / πO_K ≅ 𝔽_{p^f}
```

---

## 參考

- mathlib4: `Mathlib.NumberTheory.LocalFields`
- 局部域理論：Neukirch, "Algebraic Number Theory"