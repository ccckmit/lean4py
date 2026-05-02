# Sparse Coding 测试文档

本文档说明 `test_sparse_coding.py` 中测试用例的数学原理。

## 1. 测试验证内容概述

测试文件验证了稀疏编码模块的三个核心功能：

- **正交匹配追踪 (OMP)**：稀疏系数求解
- **字典学习 (Dictionary Learning)**：从数据中学习过完备字典
- **稀疏编码 (Sparse Coding)**：使用字典进行数据表示与重构

## 2. 字典学习测试 (TestSparseCoding)

### 测试用例

```python
def test_sparse_coding_empty_data(self):
    dictionary, codes = sparse_coding([], n_atoms=3)
    assert dictionary == []
    assert codes == []
```

### 数学原理

字典学习的目标是从输入数据学习一个过完备字典 $D$，使得每个数据点可以表示为字典原子的稀疏线性组合。

**优化问题形式：**

$$\min_{D, \alpha} \sum_{i} \|x_i - D\alpha_i\|_2^2 \quad \text{s.t.} \quad \|\alpha_i\|_0 \leq L$$

其中：
- $D \in \mathbb{R}^{n \times k}$ 是学习到的字典 ($k > n$，过完备)
- $\alpha_i$ 是第 $i$ 个样本的稀疏系数向量
- $\|x_i - D\alpha_i\|_2^2$ 是重构误差
- $\|\alpha_i\|_0$ 是稀疏度约束（非零元素个数）

**算法流程 (K-SVD 简化版)：**

1. **稀疏编码步骤**：固定字典 $D$，用 OMP 求解每个样本的稀疏系数
2. **字典更新步骤**：依次更新每个原子 $d_j$，使用对应于该原子的非零系数样本计算残差

本测试验证空数据输入的处理——返回空字典和空系数列表。

## 3. OMP 测试 (TestOMP)

### 测试用例

```python
def test_omp_no_nonzero(self):
    x = [1.0, 2.0, 3.0]
    dictionary = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    coeffs = OMP(x, dictionary, n_nonzero=0)
    assert len(coeffs) == 3
    assert all(c == 0 for c in coeffs)
```

### 数学原理

**正交匹配追踪 (Orthogonal Matching Pursuit)** 是一种贪婪算法，用于求解稀疏逼近问题。

**核心思想：** 迭代选择与当前残差最相关的字典原子，然后通过最小二乘求解最优系数。

**算法步骤：**

给定信号 $x \in \mathbb{R}^n$、字典 $D \in \mathbb{R}^{n \times k}$、稀疏度 $L$：

1. **初始化**：残差 $r^{(0)} = x$，选中原子集合 $I = \emptyset$

2. **迭代** ($l = 1, 2, \ldots, L$)：
   - 计算相关性：$c_i = |\langle r^{(l-1)}, d_i \rangle|$，对所有 $i \notin I$
   - 选择最相关原子：$i^* = \arg\max_i c_i$，$I = I \cup \{i^*\}$
   - 求解最小二乘：$\min_\alpha \|x - D_I \alpha\|_2$
   - 更新系数：$\alpha^{(l)} = (D_I^T D_I)^{-1} D_I^T x$
   - 更新残差：$r^{(l)} = x - D_I \alpha^{(l)}$

3. **返回** 稀疏系数向量 $\alpha$

本测试验证 `n_nonzero=0` 的边界情况：不应选择任何原子，所有系数均为零。

**字典结构验证：**

测试使用标准正交基作为字典：
$$D = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

输入 $x = [1, 2, 3]$ 正好可以表示为 $x = D \cdot [1, 2, 3]$。

## 4. 重构测试

### 重构误差计算

稀疏编码模块在迭代过程中计算重构误差：

```python
approx = _mat_vec_mul(dictionary, code)
error = sum((sample[i] - approx[i])**2 for i in range(n_features))
```

**重构公式：**

$$\hat{x} = D \cdot \alpha$$

其中 $\hat{x}$ 是重构信号，$D$ 是字典，$\alpha$ 是稀疏系数。

**误差度量 (MSE)：**

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (x_i - \hat{x}_i)^2$$

### 收敛判断

```python
avg_error = total_error / n_samples
if avg_error < tol or iteration == 0:
    pass
```

当平均重构误差小于阈值 $\tau$ 时迭代终止。

## 5. 关键数学运算

### 最小二乘求解

OMP 在选择原子后求解：
$$D_I^T D_I \cdot \alpha = D_I^T x$$

对于 2×2 情况，使用闭式解：
$$\alpha = \frac{1}{\det(A)} \begin{pmatrix} A_{11} & -A_{01} \\ -A_{10} & A_{00} \end{pmatrix} b$$

其中 $A = D_I^T D_I$，$b = D_I^T x$。

### 点积与矩阵运算

模块实现了以下基础运算：
- `_dot_product`: 向量点积 $\langle a, b \rangle = \sum_i a_i b_i$
- `_mat_vec_mul`: 矩阵向量乘法
- `_mat_mat_mul`: 矩阵乘法
- `_transpose`: 矩阵转置