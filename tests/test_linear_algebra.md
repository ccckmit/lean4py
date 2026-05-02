# 線性代數測試文檔

本文檔說明 `test_linear_algebra.py` 中測試用例的數學原理。

## 1. 測試總覽

本測試模組驗證了線性代數的核心概念，包括向量運算、矩陣運算、行列式、特徵值與特徵向量、秩與零度、線性獨立性、正交性等。

## 2. 向量運算測試

### 2.1 向量基本操作

| 測試 | 數學原理 |
|------|----------|
| `test_vector_init` | 向量是 n 維空間中的有序數組，記為 $\mathbf{v} = (v_1, v_2, ..., v_n)$ |
| `test_vector_add` | 向量加法：$\mathbf{u} + \mathbf{v} = (u_1+v_1, u_2+v_2, ..., u_n+v_n)$ |
| `test_vector_sub` | 向量減法：$\mathbf{u} - \mathbf{v} = (u_1-v_1, u_2-v_2, ..., u_n-v_n)$ |
| `test_vector_mul` | 標量乘法：$c \cdot \mathbf{v} = (c \cdot v_1, c \cdot v_2, ..., c \cdot v_n)$ |
| `test_vector_neg` | 向量取負：$-\mathbf{v} = (-v_1, -v_2, ..., -v_n)$ |

### 2.2 向量範數與标准化

**測試：`test_vector_norm`**

範數（Norm）是向量長度的推廣：
$$\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}$$

對於向量 $(3, 4, 0)$：
$$\|(3, 4, 0)\| = \sqrt{3^2 + 4^2 + 0^2} = \sqrt{9 + 16} = 5$$

**測試：`test_vector_normalize`**

標準化是將向量轉換為單位向量：
$$\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|}$$

### 2.3 點積（內積）

**測試：`test_dot_product`**

點積定義為：
$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^{n} u_i v_i$$

對於 $\mathbf{u} = (1, 2, 3)$ 和 $\mathbf{v} = (4, 5, 6)$：
$$\mathbf{u} \cdot \mathbf{v} = 1 \times 4 + 2 \times 5 + 3 \times 6 = 32$$

**測試：`test_dot_product_orthogonal`**

當 $\mathbf{u} \cdot \mathbf{v} = 0$ 時，兩向量正交。

### 2.4 叉積（外積）

**測試：`test_cross_product`**

叉積定義為：
$$\mathbf{u} \times \mathbf{v} = (u_2 v_3 - u_3 v_2, u_3 v_1 - u_1 v_3, u_1 v_2 - u_2 v_1)$$

對於 $\mathbf{i} \times \mathbf{j} = \mathbf{k}$，驗證了右手定則。

## 3. 矩陣運算測試

### 3.1 矩陣基本操作

| 測試 | 數學原理 |
|------|----------|
| `test_matrix_init` | 矩陣是 $m \times n$ 的數值排列 |
| `test_matrix_add` | 矩陣加法：對應元素相加 |
| `test_matrix_sub` | 矩陣減法：對應元素相減 |
| `test_matrix_mul` | 標量乘法：每個元素乘以常數 |
| `test_matrix_transpose` | 轉置：$(A^T)_{ij} = A_{ji}$ |

### 3.2 矩陣乘法

**測試：`test_matrix_mul`**

矩陣乘法 $C = AB$ 定義為：
$$C_{ij} = \sum_{k=1}^{n} A_{ik} \cdot B_{kj}$$

例如：
$$\begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix} \times \begin{pmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{pmatrix} = \begin{pmatrix} 22 & 28 \\ 49 & 64 \end{pmatrix}$$

驗證：$22 = 1\times1 + 2\times3 + 3\times5 = 22$

### 3.3 矩陣-向量乘法

**測試：`test_matrix_vector_mul`**

對於矩陣 $A$ 和向量 $\mathbf{v}$：
$$(A\mathbf{v})_i = \sum_{j} A_{ij} \cdot v_j$$

### 3.4 單位矩陣

**測試：`test_identity`**

單位矩陣 $I_n$ 滿足 $AI = IA = A$：
$$I_n = \begin{pmatrix} 1 & 0 & \cdots & 0 \\ 0 & 1 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & 1 \end{pmatrix}$$

### 3.5 矩陣的跡

**測試：`test_trace_2x2`, `test_trace_3x3`**

跡是主對角線元素的和：
$$\text{tr}(A) = \sum_{i=1}^{n} A_{ii}$$

對於 $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$，$\text{tr}(A) = 1 + 4 = 5$

### 3.6 矩陣的伴隨

**測試：`test_adjoint_2x2`**

矩陣的伴隨矩陣是餘因子矩陣的轉置。

## 4. 行列式測試

### 4.1 行列式定義

| 測試 | 數學原理 |
|------|----------|
| `test_det_1x1` | $\det([a]) = a$ |
| `test_det_2x2` | $\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$ |
| `test_det_3x3` | 上三角矩陣的行列式為對角線元素之積 |

### 4.2 行列式計算

**測試：`test_det_2x2`**

$$\det\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} = 1 \times 4 - 2 \times 3 = 4 - 6 = -2$$

**測試：`test_det_3x3`**

上三角矩陣的行列式：
$$\det\begin{pmatrix} 1 & 2 & 3 \\ 0 & 4 & 5 \\ 0 & 0 & 6 \end{pmatrix} = 1 \times 4 \times 6 = 24$$

### 4.3 奇異矩陣

**測試：`test_inverse_singular`**

當 $\det(A) = 0$ 時，矩陣不可逆（奇異矩陣）。

## 5. 矩陣逆運算測試

### 5.1 2x2 矩陣求逆

**測試：`test_inverse_2x2`**

對於 $A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$：
$$A^{-1} = \frac{1}{ad - bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$

驗證方法：$A \cdot A^{-1} = I$

## 6. 秩與零度測試

### 6.1 秩（Rank）

**測試：`test_rank_full`**

單位矩陣的秩等於其維度：$\text{rank}(I_3) = 3$

**測試：`test_rank_deficient`**

$$\begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$$

此矩陣的秩為 2，因為第二行和第三行是第一行的倍數（線性相關）。

### 6.2 零度（Nullity）

**測試：`test_nullity`**

秩-零度定理：
$$\text{rank}(A) + \text{nullity}(A) = n$$

對於 $3 \times 3$ 矩陣：$\text{nullity} = 3 - 2 = 1$

## 7. 特徵值與特徵向量測試

### 7.1 特徵值定義

**測試：`test_eigenvalues_2x2`**

特徵值滿足：
$$A\mathbf{v} = \lambda \mathbf{v}$$

即 $(A - \lambda I)\mathbf{v} = 0$ 有非零解，當且僅當 $\det(A - \lambda I) = 0$

### 7.2 單位矩陣的特徵值

**測試：`test_eigenvalues_identity`**

$$I\mathbf{v} = 1 \cdot \mathbf{v}$$

故單位矩陣的所有特徵值都為 1。

## 8. 特徵多項式測試

### 8.1 特徵多項式

**測試：`test_char_poly_1x1`, `test_char_poly_2x2`**

特徵多項式：
$$p(\lambda) = \det(A - \lambda I)$$

對於 $1 \times 1$ 矩陣 $[5]$：$p(\lambda) = 5 - \lambda = -\lambda + 5$

對於 $2 \times 2$ 矩陣：
$$p(\lambda) = \lambda^2 - \text{tr}(A)\lambda + \det(A)$$

## 9. 線性獨立性測試

### 9.1 線性獨立

**測試：`test_independent_vectors`**

向量 $\mathbf{v}_1, \mathbf{v}_2, ..., \mathbf{v}_k$ 線性獨立當且僅當：
$$c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + ... + c_k \mathbf{v}_k = 0$$

僅當所有 $c_i = 0$ 時成立。

### 9.2 線性相關

**測試：`test_dependent_vectors`**

$\mathbf{v}_1 = (1, 0, 0)$ 和 $\mathbf{v}_2 = (2, 0, 0)$ 線性相關，因為 $\mathbf{v}_2 = 2\mathbf{v}_1$。

**測試：`test_too_many_vectors`**

在 $n$ 維空間中，超過 $n$ 個向量必定線性相關。

## 10. 生成空間測試

### 10.1 生成空間維度

**測試：`test_span_basis`**

span 運算返回生成空間的維度，即基的向量個數。

## 11. 正交性測試

### 11.1 正交

**測試：`test_is_orthogonal`**

當 $\mathbf{u} \cdot \mathbf{v} = 0$ 時，$\mathbf{u}$ 與 $\mathbf{v}$ 正交。

### 11.2 標準正交

**測試：`test_is_orthonormal`**

一組向量同時滿足：
1. 兩兩正交：$\mathbf{e}_i \cdot \mathbf{e}_j = 0$（當 $i \neq j$）
2. 每個向量都是單位向量：$\|\mathbf{e}_i\| = 1$

例如：$(1,0,0)$、$(0,1,0)$、$(0,0,1)$ 是標準正交基。

## 12. 線性映射測試

### 12.1 線性映射

**測試：`test_linear_map`**

線性映射 $T: \mathbb{R}^n \to \mathbb{R}^m$ 滿足：
1. $T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$
2. $T(c\mathbf{v}) = cT(\mathbf{v})$

矩陣乘法定義了線性映射：$T(\mathbf{v}) = A\mathbf{v}$