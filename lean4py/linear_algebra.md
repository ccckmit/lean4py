# Linear Algebra Module Documentation

本文件介紹 `lean4py/linear_algebra.py` 模組的數學原理與使用方法。該模組提供向量、矩陣運算以及主成分分析等線性代數核心功能。

---

## 1. 向量運算 (Vector Operations)

### 1.1 向量表示

向量是由 `Vector` 類別表示，包含維度 `dim` 和元素列表 `elements`。

```python
v = Vector(3, [1.0, 2.0, 3.0])
```

### 1.2 向量加法與減法

**數學原理**：
- 加法：若 $\mathbf{u} = (u_1, u_2, \ldots, u_n)$，$\mathbf{v} = (v_1, v_2, \ldots, v_n)$，則
  $$\mathbf{u} + \mathbf{v} = (u_1 + v_1, u_2 + v_2, \ldots, u_n + v_n)$$
- 減法：$\mathbf{u} - \mathbf{v} = (u_1 - v_1, u_2 - v_2, \ldots, u_n - v_n)$

**代碼實現**：
```python
def __add__(self, other):
    return Vector(self.dim, [a + b for a, b in zip(self.elements, other.elements)])
```

### 1.3 標量乘法

**數學原理**：若 $c$ 為標量，$\mathbf{v} = (v_1, v_2, \ldots, v_n)$，則
$$c\mathbf{v} = (cv_1, cv_2, \ldots, cv_n)$$

```python
def __mul__(self, scalar):
    return Vector(self.dim, [x * scalar for x in self.elements])
```

### 1.4 點積 (Dot Product)

**數學原理**：兩個同維度向量的點積定義為
$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^{n} u_i v_i = \|\mathbf{u}\| \|\mathbf{v}\| \cos\theta$$

其中 $\theta$ 為兩向量夾角。

```python
def dot_product(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u.elements, v.elements))
```

### 1.5 向量範數 (Norm)

**數學原理**：向量的歐幾里得範數（2-範數）定義為
$$\|\mathbf{v}\| = \sqrt{\sum_{i=1}^{n} v_i^2}$$

```python
def norm(self) -> float:
    import math
    return math.sqrt(sum(x * x for x in self.elements))
```

---

## 2. 矩陣運算 (Matrix Operations)

### 2.1 矩陣表示

矩陣由 `Matrix` 類別表示，包含行數 `rows`、列數 `cols` 和二維數據 `data`。

```python
A = Matrix(2, 2, [[1, 2], [3, 4]])
```

### 2.2 矩陣加法與減法

**數學原理**：同型矩陣的加法為對應元素相加
$$(A + B)_{ij} = A_{ij} + B_{ij}$$

減法同理。

### 2.3 矩陣乘法

**數學原理**：若 $A$ 為 $m \times n$ 矩陣，$B$ 為 $n \times p$ 矩陣，則積 $C = AB$ 為 $m \times p$ 矩陣，定義為
$$C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$$

```python
def matrix_mul(A: Matrix, B: Matrix) -> Matrix:
    result = zero_matrix(A.rows, B.cols)
    for i in range(A.rows):
        for j in range(B.cols):
            total = 0
            for k in range(A.cols):
                total += A.data[i][k] * B.data[k][j]
            result.data[i][j] = total
    return result
```

### 2.4 矩陣轉置 (Transpose)

**數學原理**：矩陣 $A$ 的轉置 $A^T$ 滿足 $(A^T)_{ij} = A_{ji}$

```python
def transpose(self):
    return Matrix(self.cols, self.rows, [
        [self.data[j][i] for j in range(self.rows)]
        for i in range(self.cols)
    ])
```

---

## 3. 矩陣-向量乘法 (Matrix-Vector Multiplication)

**數學原理**：若 $A$ 為 $m \times n$ 矩陣，$\mathbf{v}$ 為 $n$ 維向量，則
$$(A\mathbf{v})_i = \sum_{j=1}^{n} A_{ij} v_j$$

結果為 $m$ 維向量。

```python
def matrix_vector_mul(A: Matrix, v: Vector) -> Vector:
    result = []
    for i in range(A.rows):
        total = sum(A.data[i][j] * v.elements[j] for j in range(A.cols))
        result.append(total)
    return Vector(A.rows, result)
```

---

## 4. 行列式 (Determinant)

**數學原理**：行列式是方陣的重要不變量。

- 1×1 矩陣：$\det(A) = a_{11}$
- 2×2 矩陣：$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$
- 遞迴計算（拉普拉斯展開）：
  $$\det(A) = \sum_{j=1}^{n} (-1)^{1+j} a_{1j} \cdot \det(M_{1j})$$
  其中 $M_{ij}$ 為移除第 $i$ 行第 $j$ 列後的子矩陣。

```python
def det(A: Matrix) -> float:
    n = A.rows
    if n == 1:
        return A.data[0][0]
    if n == 2:
        return A.data[0][0] * A.data[1][1] - A.data[0][1] * A.data[1][0]
    # 遞迴 cofactor 展開
    result = 0.0
    for j in range(n):
        minor = matrix_minor(A, 0, j)
        cofactor = ((-1) ** j) * det(minor)
        result += A.data[0][j] * cofactor
    return result
```

---

## 5. 特徵值與特徵向量 (Eigenvalues and Eigenvectors)

### 5.1 定義

**數學原理**：對於方陣 $A$，若存在非零向量 $\mathbf{v}$ 和純量 $\lambda$ 使得
$$A\mathbf{v} = \lambda\mathbf{v}$$

則稱 $\lambda$ 為特徵值，$\mathbf{v}$ 為對應的特徵向量。

### 5.2 計算方法

- **1×1 矩陣**：特徵值即為該元素
- **2×2 矩陣**：使用特徵方程
  $$\lambda^2 - \text{tr}(A)\lambda + \det(A) = 0$$
- **更大矩陣**：使用 NumPy 的 `np.linalg.eigvals`

```python
def eigenvalues(M: Matrix) -> List[float]:
    if M.rows != M.cols:
        raise ValueError("Eigenvalues only for square matrices")
    if n == 1:
        return [M.data[0][0]]
    if n == 2:
        trace = a + d
        det_val = a * d - b * c
        disc = trace * trace - 4 * det_val
        return [(trace + disc ** 0.5) / 2, (trace - disc ** 0.5) / 2]
```

### 5.3 特徵向量計算

透過求解 $(A - \lambda I)\mathbf{v} = \mathbf{0}$ 的零空間來獲得。

```python
def eigenvectors(M: Matrix, eigenvalue: float) -> List[Vector]:
    shifted = M + Matrix(n, n, [[-eigenvalue if i == j else 0 for j in range(n)] for i in range(n)])
    r = rank(shifted)
    null_dim = n - r
    # 計算零空間的基向量
```

---

## 6. 特徵多項式 (Characteristic Polynomial)

**數學原理**：特徵多項式定義為
$$p(\lambda) = \det(A - \lambda I)$$

其根即為矩陣 $A$ 的特徵值。

對於 2×2 矩陣：
$$p(\lambda) = \lambda^2 - \text{tr}(A)\lambda + \det(A)$$

```python
def characteristic_polynomial(M: Matrix) -> List[float]:
    """返回係數 [a_n, a_{n-1}, ..., a_0]"""
    if n == 2:
        trace_val = sum(M.data[i][i] for i in range(2))
        det_val = det(M)
        return [1.0, -trace_val, det_val]
```

---

## 7. 奇異值分解 (Singular Value Decomposition, SVD)

**數學原理**：任意 $m \times n$ 矩陣 $A$ 可分解為
$$A = U \Sigma V^T$$

其中：
- $U$ 為 $m \times m$ 正交矩陣（，左奇異向量）
- $\Sigma$ 為 $m \times n$ 對角矩陣（奇異值）
- $V$ 為 $n \times n$ 正交矩陣（右奇異向量）

**特性**：
- 奇異值 $\sigma_i$ 為 $AA^T$ 或 $A^TA$ 特徵值的平方根
- 用於降維、去噪、壓縮等應用

本模組透過 NumPy 提供 SVD 功能：
```python
import numpy as np
U, S, Vt = np.linalg.svd(A.data)
```

---

## 8. 主成分分析 (Principal Component Analysis, PCA)

### 8.1 目標

找到數據中方差最大的正交方向，將數據投影到這些方向上以實現降維。

### 8.2 數學原理

1. **數據中心化**：$\tilde{x}_i = x_i - \bar{x}$
2. **計算協方差矩陣**：$C = \frac{1}{n-1} \tilde{X}^T \tilde{X}$
3. **特徵分解**：求解 $C\mathbf{v} = \lambda\mathbf{v}$
4. **投影**：$Y = \tilde{X} V_k$

其中 $V_k$ 為前 $k$ 個最大特徵值對應的特徵向量組成的矩陣。

### 8.3 代碼實現

```python
def pca(data, n_components=2):
    # 1. 中心化數據
    mean = compute_mean_vector(data)
    centered = [[data[i][d] - mean[d] for d in range(dim)] for i in range(len(data))]

    # 2. 計算協方差矩陣
    cov = compute_covariance_matrix(centered)

    # 3. 計算特徵向量
    components = _compute_eigenvectors_cov(cov, n_components)

    # 4. 投影數據
    transformed = []
    for point in centered:
        projected = [sum(point[d] * comp[d] for d in range(dim)) for comp in components]
        transformed.append(projected)

    return transformed, explained_variance, components
```

---

## 9. 線性系統求解 (Solving Linear Systems)

### 9.1 矩陣的秩與零度

**數學原理**：
- 秩 (Rank)：矩陣行/列空間的維度
- 零度 (Nullity)：$A\mathbf{x} = \mathbf{0}$ 解空間的維度
- 維度定理：$\text{rank}(A) + \text{nullity}(A) = n$（列數）

```python
def rank(A: Matrix) -> int:
    # 高斯消去法
    r = 0
    for c in range(n):
        # 選主元
        pivot_row = r
        for i in range(r, m):
            if abs(data[i][c]) > abs(data[pivot_row][c]):
                pivot_row = i
        # 消元
        for i in range(m):
            if i != r:
                factor = data[i][c]
                for j in range(c, n):
                    data[i][j] -= factor * data[r][j]
        r += 1
    return r

def nullity(A: Matrix) -> int:
    return A.cols - rank(A)
```

### 9.2 線性獨立性判斷

向量組 $\\{\mathbf{v}_1, \ldots, \mathbf{v}_k\\}$ 線性獨立當且僅當矩陣 $[v_1, \ldots, v_k]$ 的秩為 $k$。

```python
def is_linearly_independent(vectors: List[Vector]) -> bool:
    A = Matrix(len(vectors), n, [v.elements for v in vectors]).transpose()
    return rank(A) == len(vectors)
```

### 9.3 矩陣求逆

當 $\det(A) \neq 0$ 時，$A$ 可逆：
$$A^{-1} = \frac{1}{\det(A)} \text{adj}(A)$$

其中 $\text{adj}(A)$ 為伴隨矩陣。

```python
def matrix_inverse(A: Matrix) -> Optional[Matrix]:
    d = det(A)
    if abs(d) < 1e-10:
        return None
    adj = matrix_adjoint(A)
    return adj * (1.0 / d)
```

---

## 10. 均值向量與協方差矩陣 (Mean Vector and Covariance Matrix)

### 10.1 均值向量

**數學原理**：對於數據集 $X = \\{\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_n\\}$，樣本均值定義為
$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

```python
def compute_mean_vector(data: List[List[float]]) -> List[float]:
    n = len(data)
    dim = len(data[0])
    return [sum(data[i][d] for i in range(n)) / n for d in range(dim)]
```

### 10.2 協方差矩陣

**數學原理**：協方差矩陣 $C$ 為對稱半正定矩陣，定義為
$$C_{ij} = \frac{1}{n-1} \sum_{k=1}^{n} (x_{ki} - \bar{x}_i)(x_{kj} - \bar{x}_j)$$

當 $i = j$ 時，$C_{ii}$ 為第 $i$ 維的方差。

```python
def compute_covariance_matrix(data: List[List[float]]) -> List[List[float]]:
    n = len(data)
    dim = len(data[0])
    mean = compute_mean_vector(data)

    cov = [[0.0] * dim for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            cov[i][j] = sum((data[k][i] - mean[i]) * (data[k][j] - mean[j])
                           for k in range(n)) / (n - 1)
    return cov
```

---

## 附錄：主要函數索引

| 函數 | 說明 |
|------|------|
| `Vector(dim, elements)` | 建立向量 |
| `Matrix(rows, cols, data)` | 建立矩陣 |
| `dot_product(u, v)` | 向量點積 |
| `matrix_mul(A, B)` | 矩陣乘法 |
| `matrix_vector_mul(A, v)` | 矩陣-向量乘法 |
| `det(A)` | 行列式 |
| `eigenvalues(M)` | 特徵值 |
| `eigenvectors(M, lambda)` | 特徵向量 |
| `characteristic_polynomial(M)` | 特徵多項式 |
| `pca(data, n_components)` | 主成分分析 |
| `compute_mean_vector(data)` | 均值向量 |
| `compute_covariance_matrix(data)` | 協方差矩陣 |
| `rank(A)` | 矩陣秩 |
| `matrix_inverse(A)` | 矩陣逆 |
| `identity_matrix(n)` | $n \times n$ 單位矩陣 |

---

*本文件對應版本：lean4py v1.34.0*