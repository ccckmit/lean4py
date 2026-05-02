# test_statistics_v11.py 测试文档

## 概述

本测试文件验证统计学模块中的假设检验和置信区间计算功能，主要测试：

- 单样本 t 检验 (`t_test_one_sample`)
- 均值置信区间 (`confidence_interval_mean`)

---

## 1. 单样本 t 检验 (TestTTestOneSample)

### 1.1 数学原理

单样本 t 检验用于检验样本均值是否与已知的总体均值 μ₀ 存在显著差异。

**检验统计量公式：**

```
t = (x̄ - μ₀) / (s / √n)
```

其中：
- x̄：样本均值
- μ₀：假设的总体均值
- s：样本标准差
- n：样本量

**p 值计算：**

```python
z = |t| / √2
p = 2 × (1 - 0.5 × (1 + erf(z)))
```

这使用了误差函数 (erf) 的正态分布近似来计算双尾 p 值。

### 1.2 测试用例说明

#### test_basic（基本测试）

```python
data = [1, 2, 3, 4, 5]
t_stat, p_value = t_test_one_sample(data, mu0=0.0)
```

- **验证内容**：t 统计量 > 0（样本均值大于假设均值 0），p 值在 (0, 1) 区间内
- **数学原理**：数据 [1,2,3,4,5] 的均值为 3，明显大于 μ₀=0，因此 t > 0

#### test_fail_to_reject（不拒绝原假设）

```python
data = [0.1, -0.1, 0.05, -0.05, 0.02]
t_stat, p_value = t_test_one_sample(data, mu0=0.0)
```

- **验证内容**：p 值 > 0.05
- **数学原理**：该数据围绕 0 波动，均值接近 0（约为 0.02），与原假设 μ₀=0 无显著差异
- **意义**：在 α=0.05 显著性水平下，无法拒绝原假设

#### test_empty_data（空数据处理）

```python
t_test_one_sample([], mu0=0.0) → (0.0, 1.0)
```

- **验证内容**：空数据返回 t=0.0, p=1.0
- **数学原理**：无数据时无法进行统计推断，返回最保守的结果（不拒绝原假设）

---

## 2. 均值置信区间 (TestConfidenceInterval)

### 2.1 数学原理

置信区间给出了总体均值的可能范围估计。

**公式：**

```
CI = (x̄ - margin, x̄ + margin)

其中 margin = z × s / √n
```

**常用 z 值：**

| 置信水平 | z 值 |
|---------|------|
| 90% | 1.645 |
| 95% | 1.96 |
| 99% | 2.576 |

### 2.2 测试用例说明

#### test_basic（基本置信区间）

```python
data = [1, 2, 3, 4, 5]
lower, upper = confidence_interval_mean(data, confidence=0.95)
```

- **验证内容**：下界 < 样本均值 < 上界
- **数学原理**：95% 置信区间以 95% 的概率包含真实总体均值，样本均值作为点估计必然位于区间内

#### test_90_vs_95（置信水平与区间宽度）

```python
ci_90 = confidence_interval_mean(data, confidence=0.90)
ci_95 = confidence_interval_mean(data, confidence=0.95)
```

- **验证内容**：width_90 < width_95（90% 置信区间更窄）
- **数学原理**：置信水平越高，需要更大的 margin 来确保区间包含总体均值的概率更高
- **数学表达**：margin 与 z 值成正比，z_95 > z_90，因此区间更宽

---

## 3. 边界条件测试

所有测试都包含空数据处理验证：

| 函数 | 空数据返回值 |
|------|-------------|
| t_test_one_sample | (0.0, 1.0) |
| confidence_interval_mean | (0.0, 0.0) |

---

## 4. 测试覆盖的统计方法汇总

| 测试类 | 测试方法数 | 验证内容 |
|--------|-----------|---------|
| TestTTestOneSample | 3 | t 检验计算、空数据处理、p 值性质 |
| TestConfidenceInterval | 3 | 区间覆盖、置信水平与宽度关系、空数据处理 |