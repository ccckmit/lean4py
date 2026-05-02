# 代數結構測試文檔

本文檔說明 `test_algebraic_structures.py` 中測試用例的數學原理。

## 1. 測試概述

本模組測試代數結構的核心概念，包括：
- **模 (Module)**：向量空間的推廣
- **代數 (Algebra)**：具有乘法運算的向量空間
- **張量積 (Tensor Product)**：模的積
- **正合序列 (Exact Sequence)**：模同態的精確性
- **自由模 (Free Module)**：具有基底的模
- **單模 (Simple Module)**：沒有非平凡子模的模

---

## 2. 模 (Module) 測試

### 數學原理

模是環上的向量空間推廣。設 $R$ 為環，則 $R$-模 $M$ 滿足：
- $(M, +)$ 為阿貝爾群
- 標量乘法 $R \times M \to M$ 滿足分配律等公理

當 $R$ 為域時，模即為向量空間。

### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建環 $R=0$，維度為 3 的模，確認 `dim == 3` |
| `test_is_module` | 驗證加法和標量乘法運算是否滿足模公理（零元封閉性）|
| `test_basis` | 生成標準基底，維度為 $n$ 的模具有 $n$ 個基向量 |
| `test_linear_combination` | 計算線性組合 $\sum_i c_i v_i$ |

---

## 3. 代數 (Algebra) 測試

### 數學原理

代數是域 $F$ 上的向量空間 $A$，配備雙線性乘法：
$$A \times A \to A, \quad (x, y) \mapsto x \cdot y$$

雙線性性要求乘法對每個分量分別線性。

### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建域 $F=0$，維度為 2 的代數 |
| `test_multiply` | 執行代數乘法（分量積），輸出維度為 2 的向量 |
| `test_is_algebra` | 驗證代數公理，維度 $> 0$ 時成立 |
| `test_unit` | 獲取乘法單位元，如維度為 0 返回 None |

---

## 4. 張量積 (Tensor Product) 測試

### 數學原理

兩個 $R$-模 $M$ 和 $N$ 的張量積 $M \otimes_R N$ 是滿足泛性質的 $R$-模。對於張量積 $v \otimes w$：
- 維數公式：$\dim(M \otimes N) = \dim(M) \cdot \dim(N)$
- 雙線性性：$(v_1 + v_2) \otimes w = v_1 \otimes w + v_2 \otimes w$

### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建維度 2×3=6 的張量積，確認維度為 6 |
| `test_tensor` | 計算向量張量積 $v_1 \otimes v_2$，生成平坦化向量 |
| `test_is_bilinear` | 驗證張量積的雙線性性 |
| `test_dimension` | 確認維度公式：$\dim(M_1 \otimes M_2) = \dim(M_1) \times \dim(M_2)$ |

---

## 5. 正合序列 (Exact Sequence) 測試

### 數學原理

設 ... $\to A_{i-1} \xrightarrow{f_{i-1}} A_i \xrightarrow{f_i} A_{i+1} \to ...$ 為模同態序列。

序列在 $A_i$ 處**正合**當且僅當：
$$\operatorname{im}(f_{i-1}) = \ker(f_i)$$

正合性表示每個同態的像正好是下一個同態的核。

### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建兩個模和兩個映射的序列 |
| `test_is_exact_at` | 驗證指定位置的正合性 |
| `test_is_exact` | 驗證整個序列的正合性 |

---

## 6. 自由模 (Free Module) 測試

### 數學原理

自由模是具有基底的模。設 $R$ 為環，$R^n$ 是典型的自由模：
$$R^n = \{(r_1, \ldots, r_n) \mid r_i \in R\}$$

自由模的秩 (rank) 等於其維度。

### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建環 $R=0$，維度為 3 的自由模 |
| `test_is_free` | 確認模是自由的（基底元素個數等於維度）|
| `test_rank` | 返回自由模的秩（等於維度）|

---

## 7. 單模 (Simple Module) 測試

### 數學原理

單模是沒有非平凡子模的模。即若 $0 \neq S \subseteq M$ 為子模，則 $S = M$。

單模也稱為既約模，類似於單群的概念。單模的子模只有 $\{0\}$ 和 $M$ 自身。

### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_is_simple_true` | 當子模列表僅包含空集和全集合時為單模 |
| `test_is_simple_false` | 當存在非平凡真子模時不為單模 |

---

## 測試與 mathlib4 對應

本模組對應於 mathlib4 中的：
- `Mathlib.Algebra.Module.Basic` - 模理論
- `Mathlib.Algebra.Algebra.Basic` - 代數理論
- `Mathlib.TensorProduct` - 張量積
- `Mathlib.LinearAlgebra.ExactSequence` - 正合序列