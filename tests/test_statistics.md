# test_statistics.py 测试文档

## 概述

本测试文件验证 `lean4py.statistics` 模块中的统计计算函数，涵盖描述性统计、分布特性、相关性分析和回归分析等核心概念。

## 1. 描述性统计测试

### 1.1 均值 (Mean)

**数学原理：** 均值是数据中心趋势的度量，计算公式为：

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

**测试用例说明：**
- `test_mean_empty`：空数据集返回 0.0（约定俗成的处理方式）
- `test_mean_single`：单元素数据集，均值等于该元素本身
- `test_mean_multiple`：标准均值计算，验证 [1,2,3,4,5] 的均值为 3.0
- `test_mean_negative`：正负值相互抵消，[-1, 1] 的均值为 0.0

### 1.2 中位数 (Median)

**数学原理：** 中位数将数据集按大小排序后位于中间位置的值：

$$median = \begin{cases} x_{\frac{n+1}{2}} & \text{n 为奇数} \\ \frac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2} & \text{n 为偶数} \end{cases}$$

**测试用例说明：**
- `test_median_odd`：奇数个元素 [1,3,2] 排序后为 [1,2,3]，中位数是 2.0
- `test_median_even`：偶数个元素 [1,2,3,4] 的中位数是 (2+3)/2 = 2.5

### 1.3 众数 (Mode)

**数学原理：** 众数是数据集中出现频率最高的值，可能存在零个、一个或多个众数。

**测试用例说明：**
- `test_mode_empty`：空数据集返回空列表 []
- `test_mode_single`：单元素数据集的众数是该元素本身
- `test_mode_multiple`：[1,2,2,3] 的众数唯一为 [2.0]
- `test_mode_multi_modal`：多峰数据 [1,1,2,2]，众数同时包含 1.0 和 2.0

### 1.4 方差 (Variance)

**数学原理：** 方差衡量数据离散程度，是各数据与均值差的平方和的平均值。

样本方差（分母为 n-1）：
$$s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2$$

总体方差（分母为 n）：
$$\sigma^2 = \frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2$$

**测试用例说明：**
- `test_variance_sample`：数据 [1,2,3,4,5] 的样本方差为 2.5（使用 n-1）
- `test_variance_population`：同一数据集的总体方差为 2.0（使用 n）

## 2. 标准差与分布特性测试

### 2.1 标准差 (Standard Deviation)

**数学原理：** 标准差是方差的平方根，与原始数据具有相同单位：

$$s = \sqrt{s^2}, \quad \sigma = \sqrt{\sigma^2}$$

**测试用例说明：**
- `test_std_dev_normal`：数据 [1,2,3,4,5] 的标准差约为 1.581

### 2.2 偏度 (Skewness)

**数学原理：** 偏度衡量数据分布的对称性：

$$\text{Skewness} = \frac{n}{(n-1)(n-2)}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^3$$

- skewness = 0：分布对称
- skewness > 0：右偏（正偏）
- skewness < 0：左偏（负偏）

**测试用例说明：**
- `test_skewness_symmetric`：[1,2,3,4,5] 是对称分布，偏度接近 0
- `test_skewness_positive`：[1,1,1,2,5] 右偏（少数大值拉高均值），偏度 > 0

### 2.3 峰度 (Kurtosis)

**数学原理：** 峰度描述分布的尖峭程度和尾部厚度，通常使用超额峰度：

$$\text{Excess Kurtosis} = \frac{n(n+1)}{(n-1)(n-2)(n-3)}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^4 - \frac{3(n-1)^2}{(n-2)(n-3)}$$

**测试用例说明：**
- `test_kurtosis_normal`：[1,2,3,4,5] 的超额峰度在 (-2, 1) 范围内

## 3. 相关性分析测试

### 3.1 协方差 (Covariance)

**数学原理：** 协方差衡量两个变量共同变化的趋势：

$$\text{Cov}(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})$$

**测试用例说明：**
- `test_covariance_simple`：x=[1,2,3], y=[2,4,6] 完美线性关系，协方差为 2.0
- `test_covariance_mismatch`：长度不匹配时返回 0.0

### 3.2 相关系数 (Correlation)

**数学原理：** 皮尔逊相关系数标准化了协方差，范围固定在 [-1, 1]：

$$r = \frac{\text{Cov}(X,Y)}{s_X \cdot s_Y}$$

- r = 1：完全正相关
- r = -1：完全负相关
- r = 0：无相关性

**测试用例说明：**
- `test_correlation_perfect`：x=[1,2,3], y=[2,4,6] 的 r = 1.0
- `test_correlation_negative`：x=[1,2,3], y=[6,4,2] 的 r = -1.0

## 4. 回归分析测试

### 4.1 线性回归 (Linear Regression)

**数学原理：** 线性回归拟合模型 y = β₀ + β₁x，找到使残差平方和最小的参数：

$$\beta_1 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n}(x_i - \bar{x})^2}, \quad \beta_0 = \bar{y} - \beta_1\bar{x}$$

**测试用例说明：**
- `test_regression_perfect`：y = 2x 完全线性关系，斜率 = 2.0，截距 ≈ 0
- `test_regression_negative`：y = -2x + 8，斜率 = -2.0，截距 = 8.0

## 5. 边界情况处理

测试文件覆盖了以下边界情况：

| 边界情况 | 预期行为 |
|---------|---------|
| 空数据集 | 均返回 0.0 或空列表 |
| 单元素 | 正常计算，返回该元素相关值 |
| 长度不匹配 | 返回 0.0 |

## 6. 测试覆盖的数学概念总结

```
描述性统计 ─── 均值、中位数、众数、方差、标准差
     │
分布特性 ─── 偏度、峰度
     │
相关性 ───── 协方差、皮尔逊相关系数
     │
回归分析 ─── 简单线性回归（斜率、截距）
```

这些测试共同验证了统计模块在处理各种数据集时的正确性和健壮性。