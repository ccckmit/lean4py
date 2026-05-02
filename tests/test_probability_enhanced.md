# 高等概率论测试文档

本文档说明 `test_probability_enhanced.py` 中测试用例的数学原理。

## 1. 测试概述

本模块测试高等概率论的核心概念，包括：
- 鞅（Martingale）理论
- 停时（Stopping Time）
- 可选停止定理（Optional Stopping Theorem）
- 中心极限定理（Central Limit Theorem）
- 大数定律（Law of Large Numbers）
- 特征函数（Characteristic Function）
- 随机过程（Stochastic Process）

## 2. 鞅测试（Martingale Tests）

### 数学原理

鞅是随机过程理论的核心概念。设 $(X_n)_{n \geq 0}$ 为适应于滤波 $(\mathcal{F}_n)$ 的随机过程，若满足：
$$E[X_{n+1} \mid \mathcal{F}_n] = X_n$$
则称 $(X_n)$ 为鞅。

**测试用例：**
- `test_creation`: 验证鞅对象可正确初始化，接受浮点数序列
- `test_is_martingale`: 验证鞅性质检查功能，传入期望函数判断条件期望是否等于当前值

### 代码对应

```python
class Martingale:
    def is_martingale(self, expectations: Callable[[int, Any], float]) -> bool:
        return True  # 简化实现
```

## 3. 停时测试（Stopping Time Tests）

### 数学原理

停时 $\tau$ 是一个非负整数值随机变量，满足：
$$\{\tau \leq n\} \in \mathcal{F}_n$$
即在每个时刻 $n$，我们能够判断 $\tau$ 是否已发生。

停时的例子：
- 首次击中某点的时间
- 首次达到某水平的时间
- 固定的确定时间 $n$

**测试用例：**
- `test_creation`: 验证停时对象可接受包含 `None` 的值列表（表示无穷）
- `test_is_stopping_time`: 验证停时性质检查，传入滤波结构验证 $\{\tau \leq n\} \in \mathcal{F}_n$

## 4. 可选停止定理测试（Optional Stopping Theorem）

### 数学原理

可选停止定理（Doob's Optional Stopping Theorem）是鞅理论的核心结果。设 $M_n$ 为鞅，$\tau$ 为有界停时，则：
$$E[M_\tau] = E[M_0]$$

更一般的条件包括：
- $\tau$ 有界
- $E[\tau] < \infty$ 且 $E[|M_\tau|] < \infty$

**测试用例：**
- `test_holds`: 验证可选停止定理的成立条件检查

## 5. 中心极限定理测试（Central Limit Theorem）

### 数学原理

设 $X_1, X_2, \ldots, X_n$ 为独立同分布随机变量，均值为 $\mu$，方差为 $\sigma^2$，则：
$$\frac{S_n - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} N(0,1)$$

其中 $S_n = X_1 + \cdots + X_n$，$\xrightarrow{d}$ 表示依分布收敛。

**测试用例：**
- `test_sample_mean_var`: 验证样本均值和样本方差计算
- `test_is_approximately_normal`: 验证是否满足 CLT 近似条件（通常 $n \geq 30$）
- `test_confidence_interval`: 验证置信区间计算，95% 置信区间为 $\bar{x} \pm 1.96 \cdot SE$

### 计算公式

样本均值：$\bar{X} = \frac{1}{n}\sum_{i=1}^n X_i$

样本方差：$S^2 = \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2$

标准误差：$SE = \frac{\sigma}{\sqrt{n}}$

## 6. 大数定律测试（Law of Large Numbers）

### 数学原理

**弱大数定律：** 对独立同分布随机变量序列，样本均值依概率收敛到期望：
$$\bar{X}_n \xrightarrow{P} \mu \quad \text{即} \quad P(|\bar{X}_n - \mu| > \varepsilon) \to 0$$

**强大数定律：** 样本均值几乎必然收敛到期望：
$$\bar{X}_n \to \mu \quad \text{almost surely}$$

**测试用例：**
- `test_weak_law`: 验证弱大数定律，检查样本均值与真实均值之差是否在容差范围内
- `test_strong_law`: 验证强大数定律

## 7. 特征函数测试（Characteristic Function）

### 数学原理

随机变量 $X$ 的特征函数定义为：
$$\varphi_X(t) = E[e^{itX}]$$

特征函数完全决定了分布律。

对于正态分布 $N(\mu, \sigma^2)$：
$$\varphi_X(t) = \exp\left(i\mu t - \frac{1}{2}\sigma^2 t^2\right)$$

**测试用例：**
- `test_compute_normal`: 验证正态分布特征函数的复数计算
- `test_compute_default`: 验证默认分布处理

## 8. 随机过程测试（Stochastic Process）

### 数学原理

随机过程是随时间演化的随机变量族 $(X_t)_{t \in T}$。

**布朗运动（Brownian Motion）** 是连续时间随机过程的经典例子，具有：
- $B_0 = 0$
- 独立增量
- $B_t - B_s \sim N(0, t-s)$
- 连续路径

**随机游走（Random Walk）** 是离散时间过程：
$$S_n = S_{n-1} + \xi_n$$
其中 $\xi_n$ 为独立同分布增量。

对称随机游走是鞅：$E[S_{n+1} \mid \mathcal{F}_n] = S_n$

**测试用例：**
- `test_creation`: 验证随机过程对象可创建，指定过程类型
- `test_generate`: 验证路径生成，包含初始点 0，共 `steps + 1` 个点
- `test_is_martingale`: 验证对称随机游走满足鞅性质

## 9. 与随机微积分的联系

虽然本模块没有直接的 Ito 积分测试，但相关概念包括：

### Brownian Motion in StochasticProcess
`StochasticProcess` 使用正态增量生成路径，这正是离散化的布朗运动。

### Martingale Connection
随机游走的鞅性质是 Ito 积分理论的基础。Ito 积分定义中，被积函数需为适应过程，而积分结果也是鞅。

### Further Extensions
完整的实现可扩展包括：
- Itô 引理（Itô's Lemma）
- 随机微分方程 $dX_t = \mu_t dt + \sigma_t dB_t$
- Black-Scholes 定价公式

## 10. 测试文件结构

```
tests/test_probability_enhanced.py
├── TestMartingale           # 鞅测试
├── TestStoppingTime         # 停时测试
├── TestOptionalStoppingTheorem  # 可选停止定理测试
├── TestCentralLimitTheorem  # 中心极限定理测试
├── TestLawOfLargeNumbers    # 大数定律测试
├── TestCharacteristicFunction  # 特征函数测试
└── TestStochasticProcess    # 随机过程测试
```

## 11. 数学验证要点

| 概念 | 关键性质 | 测试验证 |
|------|---------|---------|
| 鞅 | $E[X_{n+1}\mid\mathcal{F}_n] = X_n$ | `is_martingale()` |
| 停时 | $\{\tau \leq n\} \in \mathcal{F}_n$ | `is_stopping_time()` |
| 可选停止 | $E[M_\tau] = E[M_0]$ | `OptionalStoppingTheorem.holds()` |
| CLT | $(S_n - n\mu)/(\sigma\sqrt{n}) \to N(0,1)$ | `is_approximately_normal()` |
| 特征函数 | $\varphi_X(t) = E[e^{itX}]$ | `CharacteristicFunction.compute()` |
| 随机游走 | $S_n = S_{n-1} + \xi_n$ | `StochasticProcess.generate()` |