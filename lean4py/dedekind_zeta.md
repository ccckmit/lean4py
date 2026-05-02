# Dedekind Zeta 函数

## 概述

Dedekind zeta 函数是代数数论中的核心对象，用于研究数域的算术性质。对于数域 $K$，Dedekind zeta 函数定义为：

$$\zeta_K(s) = \sum_{I \subset \mathcal{O}_K} N(I)^{-s} = \prod_{P} \left(1 - N(P)^{-s}\right)^{-1}$$

其中求和遍历 $\mathcal{O}_K$ 的所有非零理想，积遍历所有非零素理想。

## 1. Dedekind zeta 函数 for 数域

设 $K$ 为次数 $n = r_1 + 2r_2$ 的数域，其中 $r_1$ 为实嵌入个数，$r_2$ 为复嵌入对数。

### 基本性质

- **Euler 积表示**：对于 $\text{Re}(s) > 1$，有
  $$\zeta_K(s) = \prod_{P} \left(1 - N(P)^{-s}\right)^{-1}$$
  其中 $N(P) = |\mathcal{O}_K / P|$ 为理想 $P$ 的范数。

- **Hecke L 函数**：当 $K = \mathbb{Q}$ 时，$\zeta_K(s)$ 退化为 Riemann zeta 函数 $\zeta(s)$。

### 与 Riemann zeta 的关系

| 性质 | $\zeta(s)$ | $\zeta_K(s)$ |
|------|-----------|--------------|
| 定义域 | $\mathbb{C}$（亚纯延拓） | $\mathbb{C}$（亚纯延拓） |
| 极点 | $s = 1$（单极点） | $s = 1$（单极点） |
| 留数 | $1$ | $\frac{2^{r_1}(2\pi)^{r_2} h_K R_K}{w_K \sqrt{|d_K|}}$ |

## 2. 解析延拓

### 全纯延拓

$\zeta_K(s)$ 可以解析延拓为整个复平面的亚纯函数。

**定理**：$\zeta_K(s)$ 可以延拓为全纯函数，除 $s = 1$ 处有单极点外处处全纯。

### 完成 zeta 函数

定义完成 zeta 函数：
$$\Lambda_K(s) = |d_K|^{s/2} \gamma_K(s) \zeta_K(s)$$

其中：
$$\gamma_K(s) = \begin{cases}
\pi^{-s/2} \Gamma\left(\frac{s}{2}\right)^{r_1} \Gamma(s)^{r_2} & \text{当 } r_2 > 0 \\
\pi^{-s/2} \Gamma\left(\frac{s}{2}\right)^{r_1} & \text{当 } r_2 = 0
\end{cases}$$

## 3. 函数方程

### 基本函数方程

**定理（函数方程）**：对于所有 $s \in \mathbb{C}$，
$$\Lambda_K(s) = \varepsilon_K \Lambda_K(1-s)$$

其中 $\varepsilon_K = \pm 1$ 为根数（root number），满足：
$$\varepsilon_K = \begin{cases}
+1 & \text{若 } r_2 \equiv 0 \pmod{2} \\
-1 & \text{若 } r_2 \equiv 1 \pmod{2} \text{ 且 } r_1 = 0 \\
\text{更复杂公式} & \text{其他情况}
\end{cases}$$

### 对偶性

函数方程揭示了 $\zeta_K(s)$ 在 $s$ 和 $1-s$ 之间的深刻对称性，这在研究临界线上的零点分布时至关重要。

## 4. 类数公式

### 分析类数公式

**定理（分析类数公式）**：
$$\lim_{s \to 1} (s-1)\zeta_K(s) = \frac{2^{r_1}(2\pi)^{r_2} h_K R_K}{w_K \sqrt{|d_K|}}$$

其中：
- $h_K$：类数（ideal class number）
- $R_K$： regulator
- $d_K$：判别式（discriminant）
- $w_K$：单位根个数

### 类数公式的意义

1. **算术解释**：留数公式连接了 $\zeta_K(s)$ 的解析性质与数域的代数不变量。
2. **计算应用**：可用于计算类数 $h_K$，当 $R_K$ 和 $w_K$ 已知时。
3. **解析不变量**：左边是纯分析量，右边是纯代数不变量。

## 5. $s=1$ 处的留数

### 留数计算

在 $s=1$ 处，$\zeta_K(s)$ 有单极点，其留数为：
$$\text{Res}_{s=1} \zeta_K(s) = \frac{2^{r_1}(2\pi)^{r_2} h_K R_K}{w_K \sqrt{|d_K|}}$$

### 特殊情形

| 数域 $K$ | 留数公式 |
|---------|---------|
| $\mathbb{Q}$ | $1$ |
| 虚二次域 | $\frac{2\pi h_K}{\sqrt{|d_K|}}$ |
| 实二次域 | $\frac{2^{r_1} h_K R_K}{\sqrt{|d_K|}}$ |

### 类数公式的另一种表述

$$\lim_{s \to 1} (s-1)\zeta_K(s) = \text{Res}_{s=1} \zeta_K(s)$$

这表明类数公式本质上是留数定理的特例。

## 6. Dedekind eta 函数与模形式

### Dedekind eta 函数定义

Dedekind eta 函数定义为：
$$\eta(\tau) = q^{1/24} \prod_{n=1}^{\infty} (1 - q^n), \quad q = e^{2\pi i \tau}$$

其中 $\tau \in \mathbb{H}$（上半平面）。

### 与模形式的关系

**定理**：$\eta(\tau)$ 是权 $1/2$ 的模形式（half-integral weight modular form）。

具体满足：
$$\eta\left(\frac{a\tau + b}{c\tau + d}\right) = \varepsilon(a,b,c,d) \sqrt{c\tau + d} \, \eta(\tau)$$
其中 $\varepsilon(a,b,c,d)$ 为某个 24 次单位根。

### Dedekind zeta 函数的模形式解释

1. **Gamma 因子**：$\gamma_K(s)$ 因子反映了 $\eta$ 函数的变换性质。
2. **函数方程**：$\zeta_K(s)$ 的函数方程可从 $\eta$ 函数的模不变性推导。
3. **临界线**：$\zeta_K(s)$ 的临界线研究与 $\eta$ 函数的零点分布密切相关。

### 函数方程的模形式视角

完成 zeta 函数 $\Lambda_K(s)$ 满足的函数方程
$$\Lambda_K(s) = \varepsilon_K \Lambda_K(1-s)$$
可解释为模形式的对称性：权 $n/2$ 的模形式在 $s \mapsto 1-s$ 变换下的行为。

## 模块结构

### 主要类

| 类名 | 功能 |
|-----|------|
| `DedekindZetaFunction` | Dedekind zeta 函数 $\zeta_K(s)$ 的主类 |
| `EulerProduct` | Euler 积表示及其收敛性 |
| `AnalyticClassNumber` | 分析类数公式 |
| `FunctionalEquation` | 函数方程及其完成形式 |

### 使用示例

```python
from dedekind_zeta import DedekindZetaFunction, AnalyticClassNumber, FunctionalEquation

# 创建 zeta 函数对象
zeta = DedekindZetaFunction("Q")

# 求值（Re(s) > 1 时收敛）
zeta.evaluate(complex(2, 0))

# 检查 Euler 积收敛性
EulerProduct.converges_for("Q", complex(2, 0))

# 类数公式
AnalyticClassNumber.formula("Q")

# 函数方程
FunctionalEquation.for_dedekind("Q")
FunctionalEquation.completed_zeta("Q", complex(2, 0))
```

## 数学背景

Dedekind zeta 函数是研究代数数域算术性质的终极工具：
- 连接了代数不变量（类数、判别式、regulator）与解析性质（零点、极点、留数）
- 类数公式是数论中最深刻的公式之一
- 函数方程揭示了对称性结构
- 与模形式理论有深刻联系

## 参考资料

- Neukirch, J. *Algebraic Number Theory*
- Lang, S. *Algebraic Number Theory*
- Weil, A. *Basic Number Theory*
- Diamond, F. & Shurman, J. *A First Course in Modular Forms*