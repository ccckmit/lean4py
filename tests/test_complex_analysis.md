# 复分析测试文档 (test_complex_analysis.py)

本文档解释 `test_complex_analysis.py` 中测试用例的数学原理。

## 1. 测试概述

本测试文件验证复分析模块的核心定理和公式，涵盖：

| 测试类 | 测试内容 |
|--------|----------|
| `TestComplexFunction` | 复变函数的基本运算 |
| `TestCauchyRiemann` | Cauchy-Riemann 方程 |
| `TestCauchyIntegralFormula` | Cauchy 积分公式 |
| `TestLiouvilleTheorem` | Liouville 定理 |
| `TestMaximumModulusPrinciple` | 最大模原理 |
| `TestResidueTheorem` | 留数定理 |
| `TestLaurentSeries` | Laurent 级数 |
| `TestArgumentPrinciple` | 辐角原理 |

---

## 2. 复数函数测试 (TestComplexFunction)

### 数学原理

复变函数是定义在复平面上的函数 $f: \mathbb{C} \to \mathbb{C}$。对于 $z = x + iy$，函数 $f(z)$ 可以写成：
$$f(z) = u(x,y) + iv(x,y)$$

其中 $u$ 和 $v$ 是实值函数。

### 测试用例

```python
def test_evaluate(self):
    f = lambda z: z * z
    cf = ComplexFunction(f)
    result = cf.evaluate(1+1j)
    assert abs(result - 2j) < 1e-10
```

**数学验证**：当 $z = 1 + i$ 时，$z^2 = (1+i)^2 = 1 + 2i + i^2 = 2i$。测试验证复数运算的正确性。

---

## 3. 全纯函数测试 (TestCauchyRiemann)

### 数学原理

Cauchy-Riemann 方程是判断函数是否全纯的充要条件。设 $f(z) = u(x,y) + iv(x,y)$，则在点 $z$ 全纯当且仅当：
$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \quad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$

这组方程也可以写成复形式：
$$\frac{\partial f}{\partial \bar{z}} = 0$$

其中 $\frac{\partial}{\partial \bar{z}} = \frac{1}{2}\left(\frac{\partial}{\partial x} + i\frac{\partial}{\partial y}\right)$。

### 测试用例

```python
def test_check(self):
    f = lambda z: z * z
    assert CauchyRiemann.check(f, 0+0j) is True
```

**数学验证**：$f(z) = z^2$ 是多项式函数，在整个复平面上全纯。对于 $z^2 = (x+iy)^2 = x^2 - y^2 + 2ixy$，有 $u = x^2 - y^2$，$v = 2xy$。直接计算可得 CR 方程成立。

---

## 4. Cauchy 积分公式测试 (TestCauchyIntegralFormula)

### 数学原理

**Cauchy 积分公式**：设 $f$ 在简单闭合曲线 $\gamma$ 内部全纯，则对内部任意点 $z_0$：
$$f(z_0) = \frac{1}{2\pi i} \oint_\gamma \frac{f(z)}{z - z_0} \, dz$$

**Cauchy 导数公式**：对 $n$ 阶导数：
$$f^{(n)}(z_0) = \frac{n!}{2\pi i} \oint_\gamma \frac{f(z)}{(z - z_0)^{n+1}} \, dz$$

### 测试用例

```python
def test_cauchy_integral(self):
    f = lambda z: z * z
    result = CauchyIntegralFormula.cauchy_integral(f, z0=0+0j, radius=1.0)
```

**数值实现**：通过对单位圆 $\gamma(t) = z_0 + re^{it}$，$t \in [0, 2\pi]$ 进行参数化：
$$\oint_\gamma \frac{f(z)}{z-z_0} dz = \int_0^{2\pi} \frac{f(z_0 + re^{it})}{re^{it}} ire^{it} dt = i\int_0^{2\pi} f(z_0 + re^{it}) dt$$

---

## 5. Liouville 定理测试 (TestLiouvilleTheorem)

### 数学原理

**Liouville 定理**：如果整函数（在整个复平面上全纯）$f$ 是有界的，即存在常数 $M$ 使得 $|f(z)| \leq M$ 对所有 $z \in \mathbb{C}$ 成立，则 $f$ 必为常数函数。

这一定理是复分析与实分析的本质区别——实轴上的有界可微函数不一定是常数。

---

## 6. 最大模原理测试 (TestMaximumModulusPrinciple)

### 数学原理

**最大模原理**：设 $f$ 在区域 $D$ 内全纯，则 $|f|$ 在 $D$ 的内部不能取得最大值，除非 $f$ 是常数。

等价表述：如果 $f$ 在有界区域 $D$ 内全纯，在 $\bar{D}$ 上连续，则 $|f|$ 的最大值必在边界 $\partial D$ 上取得。

### 数值验证

```python
def test_max_on_boundary(self):
    f = lambda z: z
    assert MaximumModulusPrinciple.max_on_boundary(f, center=0+0j, radius=1.0) is True
```

**数学验证**：对于 $f(z) = z$ 和单位圆盘 $|z| \leq 1$，有 $|f(z)| = |z|$。最大值 $|f| = 1$ 发生在边界 $|z| = 1$ 上，内部值均小于 1。

---

## 7. 留数定理测试 (TestResidueTheorem)

### 数学原理

**留数定理**：设 $f$ 在简单闭合曲线 $\gamma$ 内部除了孤立奇点外全纯，则：
$$\oint_\gamma f(z) \, dz = 2\pi i \sum_k \text{Res}(f, z_k)$$

其中 $\text{Res}(f, z_k)$ 是 $f$ 在奇点 $z_k$ 处的留数。

**留数计算**：对于简单极点 $z_0$：
$$\text{Res}(f, z_0) = \lim_{z \to z_0} (z - z_0) f(z)$$

### 测试用例

```python
def test_residue(self):
    f = lambda z: 1.0 / z  # Simple pole at 0
    result = ResidueTheorem.residue(f, z0=0+0j)
    assert isinstance(result, complex)
```

**数学验证**：对于 $f(z) = \frac{1}{z}$，在 $z_0 = 0$ 处有简单极点：
$$\text{Res}(f, 0) = \lim_{z \to 0} z \cdot \frac{1}{z} = 1$$

---

## 8. Laurent 级数测试 (TestLaurentSeries)

### 数学原理

**Laurent 级数**：在圆环域 $R_1 < |z - z_0| < R_2$ 内全纯的函数可以展开为：
$$f(z) = \sum_{n=-\infty}^{\infty} a_n (z - z_0)^n$$

其中系数：
$$a_n = \frac{1}{2\pi i} \oint_\gamma \frac{f(z)}{(z - z_0)^{n+1}} \, dz$$

Laurent 级数包含正幂部分（全纯部分）和负幂部分（主要部分）。

---

## 9. 辐角原理测试 (TestArgumentPrinciple)

### 数学原理

**辐角原理**：设 $f$ 在闭合曲线 $\gamma$ 内部只有有限个零点 $N$ 和极点 $P$（计重数），且 $f$ 在 $\gamma$ 上无零点无极点，则：
$$\frac{1}{2\pi i} \oint_\gamma \frac{f'(z)}{f(z)} \, dz = N - P$$

左边的值称为**卷绕数**，表示 $f \circ \gamma$ 绕原点的圈数。

---

## 10. 总结

本测试文件覆盖了复分析的核心定理：

| 定理 | 核心结论 |
|------|----------|
| Cauchy-Riemann | 全纯函数的等价判别条件 |
| Cauchy 积分公式 | 从边界值确定内部值 |
| Liouville | 有界整函数必为常数 |
| 最大模原理 | 全纯函数模的最大值在边界 |
| 留数定理 | 积分等于 $2\pi i$ 乘留数和 |
| Laurent 级数 | 含负幂项的级数展开 |
| 辐角原理 | 零点与极点的计数关系 |

这些定理相互关联，构成了复分析理论的基石，在数学物理和工程领域有广泛应用。