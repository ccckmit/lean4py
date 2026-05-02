# test_ml_basics.py 测试文档

## 概述

本测试文件验证 `lean4py/ml_basics.py` 模块中机器学习基础算法的正确性，涵盖线性回归、逻辑回归等核心算法的基本功能测试。

---

## 1. 测试验证内容

本测试文件主要验证以下机器学习基础算法的正确性：

| 测试类 | 测试方法 | 验证内容 |
|--------|----------|----------|
| `TestLinearRegressionML` | `test_perfect_fit` | 线性回归在完美线性关系下的拟合能力 |
| `TestLogisticRegression` | `test_separable` | 逻辑回归对线性可分数据的分类能力 |
| `TestLogisticRegression` | `test_constant_features` | 逻辑回归处理常数特征的稳定性 |

---

## 2. 分类测试（Classification）

### 2.1 逻辑回归（Logistic Regression）

#### 数学原理

逻辑回归是一种经典的二分类算法，其核心思想基于** sigmoid 函数**：

$$p = \sigma(z) = \frac{1}{1 + e^{-z}}$$

其中 $z = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n$

**损失函数**采用对数似然损失（Log-Loss）：

$$L(\beta) = -\sum_{i=1}^{n} [y_i \log(p_i) + (1 - y_i) \log(1 - p_i)]$$

**梯度下降**更新规则：

$$\beta_j := \beta_j + \alpha \cdot \frac{1}{n} \sum_{i=1}^{n} (y_i - p_i) \cdot x_{ij}$$

#### 测试用例分析

**test_separable（线性可分数据）**

```python
X = [[1.0], [2.0], [3.0], [100.0], [200.0]]
y = [0, 0, 0, 1, 1]
```

- 数据特点：两类样本完全线性可分
- 小值（1, 2, 3）对应类别 0
- 大值（100, 200）对应类别 1
- 验证点：算法能否正确收敛，输出 intercept + 1 个系数

**test_constant_features（常数特征）**

```python
X = [[1.0], [1.0], [1.0]]
y = [0, 0, 0]
```

- 数据特点：所有特征值相同
- 验证点：处理边界情况时不会崩溃

---

## 3. 回归测试（Regression）

### 3.1 线性回归（Linear Regression）

#### 数学原理

线性回归寻找最佳拟合直线：

$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n$$

**最小二乘法**目标是最小化均方误差（MSE）：

$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

**梯度下降**更新规则：

$$\beta_j := \beta_j - \alpha \cdot \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i) \cdot x_{ij}$$

#### 测试用例分析

**test_perfect_fit（完美拟合）**

```python
X = [[1.0], [2.0], [3.0], [4.0], [5.0]]
y = [2.0, 4.0, 6.0, 8.0, 10.0]
```

- 完美线性关系：$y = 2x$
- 验证点：
  - 系数数量正确（1个特征 → 1个系数）
  - 系数接近 2.0（误差 < 0.5）
  - 截距接近 0（误差 < 0.5）

---

## 4. 聚类测试（Clustering）

> **注意**：当前测试文件未直接包含聚类测试，但 `ml_basics.py` 模块提供了 K-means 聚类实现。

### 4.1 K-means 聚类

#### 数学原理

K-means 是一种无监督聚类算法，目标是将 $n$ 个数据点划分为 $k$ 个簇。

**目标函数**（惯性/Inertia）：

$$J = \sum_{j=1}^{k} \sum_{i \in C_j} \| x_i - \mu_j \|^2$$

其中 $\mu_j$ 是第 $j$ 个簇的中心点。

**算法步骤**：

1. **初始化**：随机选择 $k$ 个中心点
2. **分配**：将每个点分配给最近的中心点
3. **更新**：重新计算每个簇的中心点
4. **重复**：直到收敛或达到最大迭代次数

**欧几里得距离**：

$$d(a, b) = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}$$

---

## 5. 算法实现要点

### 5.1 线性回归实现

```python
def linear_regression_ml(x, y):
    # 添加偏置项
    X = [[1.0] + row for row in x]
    beta = [0.0] * (m + 1)

    for _ in range(max_iter):
        grad = [0.0] * (m + 1)
        for i in range(n):
            pred = sum(beta[j] * X[i][j] for j in range(m + 1))
            error = pred - y[i]
            for j in range(m + 1):
                grad[j] += error * X[i][j]
        beta = [beta[j] - learning_rate * grad[j] / n for j in range(m + 1)]
```

关键点：
- 使用批量梯度下降
- 学习率 $\alpha = 0.01$
- 最大迭代次数 1000

### 5.2 逻辑回归实现

```python
def logistic_regression(x, y, learning_rate=0.01, max_iter=1000):
    X = [[1.0] + row for row in x]
    beta = [0.0] * (m + 1)

    for _ in range(max_iter):
        grad = [0.0] * (m + 1)
        for i in range(n):
            z = sum(beta[j] * X[i][j] for j in range(m + 1))
            p = 1 / (1 + math.exp(-z))  # sigmoid
            error = y[i] - p
            for j in range(m + 1):
                grad[j] += error * X[i][j]
        beta = [beta[j] + learning_rate * grad[j] / n for j in range(m + 1)]
```

关键点：
- sigmoid 函数将输出映射到 [0, 1]
- 使用梯度上升最大化对数似然
- 返回包含截距的系数向量

---

## 6. 测试设计原则

| 原则 | 说明 |
|------|------|
| **边界条件** | 测试常数特征等边界情况 |
| **完美情况** | 验证算法在理想数据下的表现 |
| **收敛性** | 确保迭代能正确收敛 |
| **稳定性** | 验证输出的维度正确性 |

---

## 7. 相关数学概念

### 7.1 梯度下降

梯度下降是一种优化算法，用于找到函数的局部最小值：

$$\theta := \theta - \alpha \nabla J(\theta)$$

其中 $\alpha$ 是学习率，$\nabla J(\theta)$ 是目标函数的梯度。

### 7.2 收敛性

算法收敛条件：
- 梯度接近零
- 损失函数变化小于阈值
- 达到最大迭代次数

### 7.3 过拟合与欠拟合

- **欠拟合**：模型过于简单，无法捕捉数据模式
- **过拟合**：模型过于复杂，记住噪声而非信号

---

## 8. 扩展测试建议

当前测试覆盖了基础功能，可考虑增加以下测试：

1. **线性回归**：
   - 多特征回归
   - 噪声数据测试
   - 正则化效果

2. **逻辑回归**：
   - 多类分类
   - 概率校准
   - 决策边界可视化

3. **聚类**：
   - K-means 收敛性测试
   - 不同初始化效果
   - 簇数选择（肘部法则）