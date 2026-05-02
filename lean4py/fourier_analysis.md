# Fourier 分析模块 (fourier_analysis.py)

## 概述

本模块实现了傅里叶分析的核心概念，包括傅里叶级数、傅里叶变换、卷积定理、Plancherel 定理等，模仿了 mathlib4 的 `Mathlib.Analysis.Fourier` 设计。

---

## 1. 傅里叶级数 (Fourier Series)

### 1.1 定义

对于周期为 $2\pi$ 的周期函数 $f(x)$，其傅里叶级数展开为：

$$f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty} \left( a_n \cos(nx) + b_n \sin(nx) \right)$$

### 1.2 傅里叶系数

系数通过以下公式计算：

$$a_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \cos(nx) \, dx \quad (n \geq 0)$$

$$b_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \sin(nx) \, dx \quad (n \geq 1)$$

其中：
- $a_0 = \frac{1}{\pi} \int_{-\pi}^{\pi} f(x) \, dx$

### 1.3 类实现：`FourierSeries`

```python
class FourierSeries:
    @staticmethod
    def coefficients(f, period=2.0*math.pi, n_terms=10) -> List[complex]
    @staticmethod
    def reconstruct(coeffs, x, period=2.0*math.pi) -> complex
```

- `coefficients`: 计算复数形式的傅里叶系数 $c_n = \frac{1}{T} \int_0^T f(x) e^{-2\pi i n x/T} dx$
- `reconstruct`: 从系数重构原函数

---

## 2. 复数形式的傅里叶级数

周期为 $T$ 的函数可以表示为复数形式：

$$f(x) = \sum_{n=-\infty}^{\infty} c_n e^{2\pi i n x / T}$$

其中系数：

$$c_n = \frac{1}{T} \int_0^T f(x) e^{-2\pi i n x / T} \, dx$$

复数形式等价于实数形式，且自动满足正交性条件。

---

## 3. Parseval 恒等式 (Parseval's Identity)

对于周期为 $2\pi$ 的函数，其傅里叶级数满足：

$$\frac{1}{\pi} \int_{-\pi}^{\pi} |f(x)|^2 \, dx = \frac{a_0^2}{2} + \sum_{n=1}^{\infty} (a_n^2 + b_n^2)$$

复数形式：

$$\int_{-\pi}^{\pi} |f(x)|^2 \, dx = 2\pi \sum_{n=-\infty}^{\infty} |c_n|^2$$

这表明傅里叶变换保持能量（$L^2$ 范数）。

---

## 4. 傅里叶变换 (Fourier Transform)

### 4.1 定义

对于非周期函数 $f(t)$，其傅里叶变换为：

$$F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} \, dt$$

本模块采用 $2\pi$ 归一化版本：

$$F(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} \, dx$$

### 4.2 类实现：`FourierTransform`

```python
class FourierTransform:
    @staticmethod
    def fourier_transform(f, xi, x_range=(-10.0, 10.0)) -> complex
```

数值计算使用矩形法则：

$$F(\xi) \approx \sum_{x} f(x) e^{-2\pi i x \xi} \Delta x$$

---

## 5. 逆傅里叶变换 (Inverse Fourier Transform)

### 5.1 定义

由频域恢复原函数：

$$f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} F(\omega) e^{i\omega t} \, d\omega$$

采用 $2\pi$ 归一化：

$$f(x) = \int_{-\infty}^{\infty} F(\xi) e^{2\pi i x \xi} \, d\xi$$

### 5.2 类实现：`InverseFourierTransform`

```python
class InverseFourierTransform:
    @staticmethod
    def evaluate(F, x) -> complex
```

数值上使用相同的矩形法则近似积分。

---

## 6. 卷积定理 (Convolution Theorem)

### 6.1 卷积定义

$$(f * g)(x) = \int_{-\infty}^{\infty} f(t) g(x - t) \, dt$$

### 6.2 卷积定理

傅里叶变换将卷积转化为乘积：

$$\mathcal{F}(f * g) = \mathcal{F}(f) \cdot \mathcal{F}(g)$$

即在频域中，卷积变为简单的乘法。

### 6.3 类实现：`Convolution`

```python
class Convolution:
    @staticmethod
    def convolve(f, g, x, dx=0.01) -> complex
    @staticmethod
    def convolution_theorem(f, g, xi) -> bool
```

---

## 7. Plancherel 定理 (Plancherel Theorem)

### 7.1 定理内容

傅里叶变换是 $L^2$ 空间上的等距映射：

$$\|f\|_2 = \|F(f)\|_2$$

即：

$$\int_{-\infty}^{\infty} |f(x)|^2 \, dx = \int_{-\infty}^{\infty} |F(f)(\xi)|^2 \, d\xi$$

### 7.2 类实现：`PlancherelTheorem`

```python
class PlancherelTheorem:
    @staticmethod
    def plancherel_holds(f, x_range=(-10.0, 10.0)) -> bool
```

该定理表明傅里叶变换保持能量，是量子力学和信号处理的基础。

---

## 8. Parseval 定理（变换形式）

对于傅里叶变换，有：

$$\int_{-\infty}^{\infty} f(x) \overline{g(x)} \, dx = \int_{-\infty}^{\infty} F(f)(\xi) \overline{F(g)(\xi)} \, d\xi$$

特例（能量守恒）：

$$\int_{-\infty}^{\infty} |f(x)|^2 \, dx = \int_{-\infty}^{\infty} |F(f)(\xi)|^2 \, d\xi$$

这与 Plancherel 定理等价。

---

## 9. Riemann-Lebesgue 引理

### 9.1 定理内容

若 $f \in L^1(\mathbb{R})$，则其傅里叶变换满足：

$$\lim_{|\xi| \to \infty} F(f)(\xi) = 0$$

即高频成分逐渐消失，$F(f)(\xi)$ 在无穷远处趋于零。

### 9.2 类实现：`RiemannLebesgueLemma`

```python
class RiemannLebesgueLemma:
    @staticmethod
    def holds(f) -> bool
```

---

## 10. Poisson 求和公式 (Poisson Summation)

### 10.1 公式内容

$$\sum_{n \in \mathbb{Z}} f(n) = \sum_{k \in \mathbb{Z}} F(f)(k)$$

即将时域采样点的和等于频域采样点的和。

### 10.2 类实现：`PoissonSummation`

```python
class PoissonSummation:
    @staticmethod
    def poisson_summation(f, period=1.0) -> bool
```

该公式连接了连续和离散的傅里叶分析。

---

## 类关系图

```
FourierTransform          傅里叶变换
       ↓
InverseFourierTransform   逆变换

FourierSeries             傅里叶级数
       ↓
Convolution               卷积定理
       ↓
PlancherelTheorem         能量守恒

RiemannLebesgueLemma      引理
PoissonSummation          求和公式
```

---

## 使用示例

```python
from lean4py.fourier_analysis import FourierTransform, FourierSeries

# 傅里叶变换
F = FourierTransform.fourier_transform(lambda x: math.e ** (-x**2), xi=1.0)

# 傅里叶级数
coeffs = FourierSeries.coefficients(lambda x: x, n_terms=20)
reconstructed = FourierSeries.reconstruct(coeffs, x=0.5)
```