# Fourier 分析模块测试文档

## 概述

本测试文件验证 `lean4py.fourier_analysis` 模块的核心功能，涵盖傅里叶变换、逆傅里叶变换、傅里叶级数、卷积、Plancherel 定理、Riemann-Lebesgue 引理和 Poisson 求和公式。

---

## 1. 傅里叶变换测试 (Fourier Transform)

### 测试内容

| 测试方法 | 测试函数 | 频率参数 |
|---------|---------|---------|
| `test_fourier_transform` | 矩形窗函数 $f(x) = 1_{-0.5 \leq x \leq 0.5}$ | $\xi = 0.0$ |
| `test_fourier_transform_sin` | 正弦函数 $f(x) = \sin(x)$ | $\xi = 1.0$ |

### 数学原理

**傅里叶变换**将时域函数转换为频域表示：

$$\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} \, dx$$

矩形窗函数的傅里叶变换结果是 sinc 函数：

$$\text{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$$

### 验证内容

- 变换结果返回复数类型
- 矩形窗函数在 $\xi = 0$ 处取得最大值（信号总能量）
- 正弦函数的变换对应频域中的 Dirac delta 分布

---

## 2. 逆傅里叶变换测试 (Inverse Fourier Transform)

### 测试内容

| 测试方法 | 频域函数 | 求值点 |
|---------|---------|-------|
| `test_inverse` | $F(\xi) = e^{-\pi \xi^2}$ (高斯函数) | $x = 0.0$ |

### 数学原理

**逆傅里叶变换**从频域恢复时域信号：

$$f(x) = \int_{-\infty}^{\infty} F(\xi) e^{2\pi i x \xi} \, d\xi$$

高斯函数的特殊性质：其傅里叶变换仍是高斯函数。

### 验证内容

- 逆变换返回复数类型
- 高斯函数 $e^{-\pi \xi^2}$ 的逆变换仍为高斯函数本身

---

## 3. 傅里叶级数测试 (Fourier Series)

### 测试内容

| 测试方法 | 功能 |
|---------|-----|
| `test_coefficients` | 计算傅里叶系数 |
| `test_reconstruct` | 从系数重建信号 |

### 数学原理

**傅里叶级数**将周期函数展开为正弦和余弦的叠加：

$$f(x) = \sum_{n=-\infty}^{\infty} c_n e^{inx}$$

其中系数：

$$c_n = \frac{1}{2\pi} \int_{0}^{2\pi} f(x) e^{-inx} \, dx$$

### 测试分析

- `test_coefficients`: 测试函数 $f(x) = x$ 在周期 $2\pi$ 下的 5 次谐波（从 -5 到 5，共 11 个系数）
- `test_reconstruct`: 使用常数系数 $[1.0, 1.0, ..., 1.0]$ 重建信号

### 验证内容

- 系数数量正确：$n\_terms = 5$ 返回 $2 \times 5 + 1 = 11$ 个系数
- 重建结果返回复数类型（复数形式支持更一般的信号）

---

## 4. 卷积测试 (Convolution)

### 测试内容

| 测试方法 | 说明 |
|---------|-----|
| `test_convolve` | 计算两个函数的卷积 |
| `test_convolution_theorem` | 验证卷积定理 |

### 数学原理

**卷积**定义：

$$(f * g)(x) = \int_{-\infty}^{\infty} f(t) g(x-t) \, dt$$

**卷积定理**：两个函数卷积的傅里叶变换等于它们各自傅里叶变换的乘积：

$$\mathcal{F}\{f * g\} = \mathcal{F}\{f\} \cdot \mathcal{F}\{g\}$$

### 测试分析

- 测试使用两个相同的矩形窗函数（宽度为 1）
- 卷积结果是三角波函数（梯形形状）
- 验证在 $\xi = 0.0$ 处卷积定理成立

### 验证内容

- 卷积计算返回复数类型
- 卷积定理在指定频率点成立（返回 `True`）

---

## 5. Plancherel 定理测试

### 测试内容

| 测试方法 | 测试函数 |
|---------|---------|
| `test_plancherel_holds` | 矩形窗函数 |

### 数学原理

**Plancherel 定理**（也称 Parseval 定理）是傅里叶变换的能量守恒定理：

$$\int_{-\infty}^{\infty} |f(x)|^2 \, dx = \int_{-\infty}^{\infty} |\hat{f}(\xi)|^2 \, d\xi$$

该定理表明：信号在时域的总能量等于其在频域的总能量。

### 测试分析

矩形窗函数：

$$f(x) = \begin{cases} 1 & |x| \leq 0.5 \\ 0 & |x| > 0.5 \end{cases}$$

- 时域能量：$\int_{-0.5}^{0.5} 1^2 \, dx = 1$
- 频域能量：$\int_{-\infty}^{\infty} |\text{sinc}(\xi)|^2 \, d\xi = 1$

### 验证内容

- 验证 Plancherel 定理对矩形窗函数成立（返回 `True`）

---

## 6. 其他测试

### Riemann-Lebesgue 引理

| 测试方法 | 说明 |
|---------|-----|
| `test_holds` | 验证引理对矩形窗函数成立 |

**数学原理**：若 $f \in L^1(\mathbb{R})$，则其傅里叶变换 $\hat{f}(\xi)$ 在无穷远处趋于零：

$$\lim_{|\xi| \to \infty} \hat{f}(\xi) = 0$$

这意味着高频分量逐渐衰减。

---

### Poisson 求和公式

| 测试方法 | 测试函数 |
|---------|---------|
| `test_poisson_summation` | 高斯函数 $e^{-x^2}$ |

**数学原理**：Poisson 求和公式连接离散求和与连续积分：

$$\sum_{n=-\infty}^{\infty} f(x + n) = \sum_{k=-\infty}^{\infty} \hat{f}(k) e^{2\pi i k x}$$

高斯函数的特殊性质使其满足精确的 Poisson 求和公式。

### 验证内容

- 验证 Poisson 求和公式对高斯函数成立（返回 `True`）

---

## 测试函数对应关系表

| 测试类 | 测试方法 | 验证的数学概念 |
|-------|---------|--------------|
| `TestFourierTransform` | `test_fourier_transform` | 傅里叶变换定义 |
| `TestFourierTransform` | `test_fourier_transform_sin` | 正弦函数的频域表示 |
| `TestInverseFourierTransform` | `test_inverse` | 逆傅里叶变换 |
| `TestFourierSeries` | `test_coefficients` | 傅里叶系数计算 |
| `TestFourierSeries` | `test_reconstruct` | 信号重建 |
| `TestConvolution` | `test_convolve` | 卷积运算 |
| `TestConvolution` | `test_convolution_theorem` | 卷积定理 |
| `TestPlancherelTheorem` | `test_plancherel_holds` | 能量守恒 |
| `TestRiemannLebesgueLemma` | `test_holds` | 高频衰减 |
| `TestPoissonSummation` | `test_poisson_summation` | 离散-连续对偶 |

---

## 关键数学性质总结

1. **线性性**：傅里叶变换是线性运算
2. **卷积定理**：时域卷积对应频域乘积
3. **能量守恒**：Plancherel 定理保证能量在变换中不变
4. **对称性**：高斯函数是傅里叶变换的不变函数
5. **Riemann-Lebesgue**：$L^1$ 函数的变换在无穷远处衰减