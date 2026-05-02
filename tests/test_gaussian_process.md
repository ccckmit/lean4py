# Gaussian Process 测试文档

本文档说明 `test_gaussian_process.py` 中测试用例的数学原理。

## 1. 测试验证内容概述

测试套件验证高斯过程回归器的三个核心功能：

| 测试类 | 验证内容 |
|--------|----------|
| `TestRBFKernel` | 径向基函数核函数的数学性质 |
| `TestGaussianProcessRegressor` | 高斯过程回归器的拟合与预测能力 |
| `TestPredictGP` | 便捷预测函数的行为 |

---

## 2. 核函数测试 (TestRBFKernel)

### 2.1 RBF 核函数的数学定义

$$k(x_1, x_2) = \exp\left(-\frac{\|x_1 - x_2\|^2}{2\ell^2}\right)$$

其中 $\ell$ 是长度尺度参数，$\|x_1 - x_2\|^2$ 是欧几里得距离的平方。

### 2.2 测试用例分析

#### `test_same_points` - 相同点测试

```python
k = rbf_kernel(x, x)
assert abs(k - 1.0) < 0.01
```

**数学原理**：当 $x_1 = x_2$ 时，$\|x_1 - x_2\|^2 = 0$，代入公式得：
$$k(x, x) = \exp(0) = 1$$

因此相同点的核函数值应接近 1，表示完全相似。

#### `test_different_points` - 不同点测试

```python
k = rbf_kernel(x1, x2)
assert 0 < k < 1
```

**数学原理**：当 $x_1 \neq x_2$ 时，距离平方 $\|x_1 - x_2\|^2 > 0$，指数函数值为正但小于 1。核函数值在 (0,1) 区间内，表示部分相似性。

#### `test_length_scale` - 长度尺度测试

```python
k_small = rbf_kernel(x1, x2, length_scale=0.1)
k_large = rbf_kernel(x1, x2, length_scale=10.0)
assert k_small < k_large
```

**数学原理**：长度尺度 $\ell$ 控制函数的"平滑程度"：
- 小 $\ell$：指数分母小，核函数值快速衰减，两点相似性迅速降至接近 0
- 大 $\ell$：指数分母大，核函数值衰减缓慢，远处点仍保持较高相似性

公式变换：
$$k(x_1, x_2) = \exp\left(-\frac{\|x_1 - x_2\|^2}{2\ell^2}\right)$$

当 $\ell_1 = 0.1, \ell_2 = 10.0$，固定距离 $\|x_1 - x_2\| = 1$：
- $\ell = 0.1$：$k = \exp(-50) \approx 1.9 \times 10^{-22}$
- $\ell = 10$：$k = \exp(-0.005) \approx 0.995$

因此 $k_{small} < k_{large}$。

---

## 3. 预测测试 (TestGaussianProcessRegressor)

### 3.1 高斯过程回归的数学框架

高斯过程是在函数空间上的联合高斯分布：

$$f(x) \sim \mathcal{GP}(m(x), k(x, x'))$$

对于观测 $y = f(x) + \epsilon$，后验预测分布为：

$$f^* | X, y, x^* \sim \mathcal{N}(\mu(x^*), \sigma^2(x^*))$$

### 3.2 后验均值公式

$$\mu(x^*) = k(x^*, X)^T K^{-1} y$$

其中 $k(x^*, X)$ 是测试点与训练点之间的核向量，$K$ 是训练数据的核矩阵。

### 3.3 后验方差公式

$$\sigma^2(x^*) = k(x^*, x^*) - k(x^*, X)^T K^{-1} k(X, x^*)$$

### 3.4 测试用例分析

#### `test_fit_predict` - 拟合与预测测试

```python
X_train = [[0.0], [1.0], [2.0]]
y_train = [0.0, 1.0, 2.0]
means, variances = gp.predict(X_test)
assert min(y_train) - 1 <= means[0] <= max(y_train) + 1
```

**数学原理**：
- 训练数据为线性 $y = x$
- 预测点 $x = 0.5, 1.5$ 位于训练点之间
- 后验均值应接近真实函数值
- 验证均值落在训练值范围内（加减1的容差）

#### `test_empty_fit` - 空数据测试

```python
means, variances = gp.predict([[1.0]])
assert means == []
assert variances == []
```

**数学原理**：未进行拟合时，模型没有训练数据，无法进行预测，返回空列表。

---

## 4. 后验分布测试 (TestPredictGP)

### 4.1 预测不确定性

```python
means, stds = predict_gp(X_train, y_train, X_test)
assert stds[0] > 0
```

**数学原理**：高斯过程的核心优势之一是提供不确定性估计。方差的正平方根（标准差）$\sigma = \sqrt{\sigma^2}$ 必须为正，反映预测的置信度。

### 4.2 单训练点行为

```python
X_train = [[0.0]]
y_train = [1.0]
gp.fit(X_train, y_train)
means, variances = gp.predict([[1.0]])
```

**数学原理**：
- 单训练点时，核矩阵 $K = [k(x_1, x_1) + \noise] \approx [1]$
- 预测公式简化为：$\mu(x^*) = k(x^*, x_1) \cdot K^{-1} \cdot y_1 = k(x^*, x_1) \cdot y_1$
- 方差由 $k(x^*, x^*) - k(x^*, x_1)^2 \cdot K^{-1}$ 决定

---

## 5. 核矩阵与矩阵求逆

### 5.1 核矩阵定义

$$K_{ij} = k(X_i, X_j)$$

对于 n 个训练点，$K$ 是 $n \times n$ 的对称正定矩阵。

### 5.2 对角线噪声正则化

```python
for i in range(n):
    K[i][i] += self.noise
```

**数学原理**：加入小的噪声项 $\sigma_n^2$ 到对角线，确保矩阵条件数良好，数值计算稳定。

### 5.3 矩阵求逆实现

使用高斯消元法求逆矩阵，复杂度为 $O(n^3)$，适用于小规模数据集。

---

## 6. 测试覆盖总结

| 数学概念 | 测试验证 |
|----------|----------|
| RBF 核函数值域 | 相同点 = 1，不同点 ∈ (0,1) |
| 长度尺度影响 | 小尺度 → 低相似度，大尺度 → 高相似度 |
| 后验均值计算 | 预测值在训练数据合理范围内 |
| 后验方差非负 | 方差必须为正 |
| 边界情况 | 空训练数据返回空预测 |