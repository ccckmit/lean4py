# 數值方法 (Numerical Methods)

本模組提供數值計算的核心演算法，包括根求解、插值、數值積分等。

---

## 1. 數值誤差 (Numerical Error)

### 1.1 捨入誤差 (Round-off Error)

由於電腦浮點數表示的精度有限而產生的誤差。

- 單精度浮點数 (float32)：約 7 位有效數字
- 雙精度浮點数 (float64)：約 15-16 位有效數字

例如：$\frac{1}{3} = 0.333333...$ 在電腦中只能近似表示。

### 1.2 截斷誤差 (Truncation Error)

用有限近似代替無限精確數學運算所產生的誤差。

例如：指數函數的泰勒展開
$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + ...$$

有限項近似後剩餘的高階項即為截斷誤差：
$$R_n(x) = \frac{e^\xi}{(n+1)!} x^{n+1}, \quad \xi \in (0, x)$$

### 1.3 誤差的關係

總誤差 ≤ 截斷誤差 + 捨入誤差

設計數值方法時需平衡兩者：加密網格可減少截斷誤差但可能增加累積捨入誤差。

---

## 2. 根求解 (Root Finding)

### 2.1 二分法 (Bisection Method)

**原理**：若連續函數 $f(x)$ 在區間 $[a,b]$ 滿足 $f(a) \cdot f(b) < 0$，則區間內必有根。

**迭代公式**：
$$c = \frac{a + b}{2}$$

**收斂性**：線性收斂，每次迭代將區間長度減半。

**誤差估計**：
$$|x - x^*| \leq \frac{b-a}{2^n}$$

```python
class BisectionMethod:
    def find_root(self, a: float, b: float, tolerance: float = 1e-10, max_iterations: int = 100):
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")
        for i in range(max_iterations):
            mid = (a + b) / 2
            fmid = f(mid)
            if abs(fmid) < tolerance or (b - a) / 2 < tolerance:
                return (mid, i + 1, True)
            if fa * fmid < 0:
                b, fb = mid, fmid
            else:
                a, fa = mid, fmid
        return ((a + b) / 2, max_iterations, False)
```

**優點**：保證收斂，收斂速率慢
**缺點**：需要初始區間端點異號

### 2.2 牛頓-拉弗森法 (Newton-Raphson Method)

**原理**：使用泰勒展開的一階近似

$$f(x) \approx f(x_n) + f'(x_n)(x - x_n) = 0$$

**迭代公式**：
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**幾何意義**：在 $(x_n, f(x_n))$ 處作切線，取其與 x 軸的交點為下一個近似。

**收斂性**：在根附近二次收斂（若 $f'(x^*) \neq 0$）

**誤差估計**：
$$|x_{n+1} - x^*| \approx \frac{|f''(x^*)|}{2|f'(x^*)|} |x_n - x^*|^2$$

```python
class NewtonRaphson:
    def __init__(self, f: Callable, f_prime: Optional[Callable] = None):
        self.f = f
        self.f_prime = f_prime or self._numerical_derivative(f)

    def find_root(self, x0: float, tolerance: float = 1e-10, max_iterations: int = 100):
        x = x0
        for i in range(max_iterations):
            fx = self.f(x)
            if abs(fx) < tolerance:
                return (x, i + 1, True)
            dfx = self.f_prime(x)
            if abs(dfx) < 1e-15:
                return (x, i + 1, False)
            x = x - fx / dfx
        return (x, max_iterations, False)
```

**優點**：收斂速度快
**缺點**：可能不收斂或收斂到錯誤的根

### 2.3 割線法 (Secant Method)

**原理**：牛頓法的導數近似版本，用差商代替導數

**迭代公式**：
$$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

**收斂性**：超線性收斂，階數約 1.618（黃金比例）

```python
class SecantMethod:
    def find_root(self, x0: float, x1: float, tolerance: float = 1e-10, max_iterations: int = 100):
        for i in range(max_iterations):
            fx0, fx1 = f(x0), f(x1)
            denom = fx1 - fx0
            if abs(denom) < 1e-15:
                return (x1, i + 1, False)
            x2 = x1 - fx1 * (x1 - x0) / denom
            if abs(x2 - x1) < tolerance:
                return (x2, i + 1, True)
            x0, x1 = x1, x2
        return (x1, max_iterations, False)
```

---

## 3. 不動點迭代 (Fixed Point Iteration)

### 3.1 基本原理

將方程 $f(x) = 0$ 改寫為 $x = g(x)$ 的形式。

**迭代公式**：
$$x_{n+1} = g(x_n)$$

不動點：滿足 $x = g(x)$ 的點。

### 3.2 收斂條件

**局部收斂定理**：若 $g$ 在不動點 $x^*$ 的某個鄰域內可導，且 $|g'(x^*)| < 1$，則迭代局部收斂。

**全局收斂**：若 $g$ 在 $[a,b]$ 上連續，且：
1. 對所有 $x \in [a,b]$，$g(x) \in [a,b]$
2. 存在常數 $L \in (0,1)$ 使得 $|g'(x)| \leq L$ 對所有 $x \in (a,b)$ 成立

則迭代對任意初始值收斂。

### 3.3 收斂階數

若 $g'(x^*) = g''(x^*) = ... = g^{(k-1)}(x^*) = 0$，但 $g^{(k)}(x^*) \neq 0$，則收斂階數為 $k$。

```python
class FixedPointIteration:
    def find_fixed_point(self, x0: float, tolerance: float = 1e-10, max_iterations: int = 100):
        x = x0
        for i in range(max_iterations):
            x_next = self.g(x)
            if abs(x_next - x) < tolerance:
                return (x_next, i + 1, True)
            x = x_next
        return (x, max_iterations, False)

    def has_convergence_guarantee(self, x: float) -> bool:
        h = 1e-8
        g_prime = (self.g(x + h) - self.g(x - h)) / (2 * h)
        return abs(g_prime) < 1
```

**收斂速率**：
- $|g'(x^*)| = 0$：超線性收斂
- $0 < |g'(x^*)| < 1$：線性收斂
- $|g'(x^*)| > 1$：發散

---

## 4. 數值積分 (Numerical Integration)

### 4.1 梯形法則 (Trapezoidal Rule)

**原理**：用梯形近似曲線下的面積。

**單區間公式**：
$$\int_a^b f(x)dx \approx \frac{b-a}{2}[f(a) + f(b)]$$

**複合梯形法則**：
將區間 $[a,b]$ 分成 $n$ 個小區間，每個區間應用梯形法則：

$$\int_a^b f(x)dx \approx \frac{h}{2}\left[f(x_0) + 2\sum_{i=1}^{n-1}f(x_i) + f(x_n)\right]$$

其中 $h = \frac{b-a}{n}$，$x_i = a + ih$。

**誤差**：複合梯形法則的誤差為 $O(h^2)$。

### 4.2 辛普森法則 (Simpson's Rule)

**原理**：用二次多項式近似被積函數。

**單區間公式**（需要三個點）：
$$\int_a^b f(x)dx \approx \frac{b-a}{6}\left[f(a) + 4f\left(\frac{a+b}{2}\right) + f(b)\right]$$

**複合辛普森法則**（$n$ 必須為偶數）：
$$\int_a^b f(x)dx \approx \frac{h}{3}\left[f(x_0) + 4\sum_{i=1,3,5,...}^{n-1}f(x_i) + 2\sum_{i=2,4,6,...}^{n-2}f(x_i) + f(x_n)\right]$$

其中 $h = \frac{b-a}{n}$。

**誤差**：複合辛普森法則的誤差為 $O(h^4)$。

```python
class SimpsonRule:
    def integrate(self, f: Callable, a: float, b: float, n: int = 100):
        if n % 2 == 1:
            n += 1
        h = (b - a) / n
        result = f(a) + f(b)
        for i in range(1, n):
            x = a + i * h
            result += 2 * f(x) if i % 2 == 0 else 4 * f(x)
        return result * h / 3
```

### 4.3 高斯求積法 (Gaussian Quadrature)

**原理**：選擇最優的節點位置和權重以最大化精度。

**n 點高斯-勒讓德公式**：
$$\int_{-1}^{1} f(x)dx \approx \sum_{i=1}^{n} w_i f(x_i)$$

其中 $x_i$ 是勒讓德多項式 $P_n(x)$ 的根，$w_i$ 是對應權重。

**勒讓德多項式遞推關係**：
$$P_0(x) = 1, \quad P_1(x) = x$$
$$(n+1)P_{n+1}(x) = (2n+1)xP_n(x) - nP_{n-1}(x)$$

**節點計算**：使用牛頓法求解 $P_n(x) = 0$
$$x_{i+1} = x_i - \frac{P_n(x_i)}{P_n'(x_i)}$$

**權重公式**：
$$w_i = \frac{2}{(1-x_i^2)[P_n'(x_i)]^2}$$

**變數變換**：
$$\int_a^b f(x)dx = \frac{b-a}{2}\int_{-1}^{1} f\left(\frac{a+b}{2} + \frac{b-a}{2}t\right)dt$$

```python
class GaussianQuadrature:
    @staticmethod
    def legendre_polynomial(n: int, x: float) -> float:
        if n == 0:
            return 1.0
        if n == 1:
            return x
        p0, p1 = 1.0, x
        for i in range(2, n + 1):
            p2 = ((2 * i - 1) * x * p1 - (i - 1) * p0) / i
            p0, p1 = p1, p2
        return p1

    def integrate(self, f: Callable, a: float, b: float, n: int = 5):
        nodes, weights = self.gauss_legendre_nodes_weights(n)
        midpoint = (b + a) / 2
        half_length = (b - a) / 2
        total = 0.0
        for x, w in zip(nodes, weights):
            t = midpoint + half_length * x
            total += w * f(t)
        return half_length * total
```

**高斯求積法的優點**：
- n 點公式精確度高達 $2n-1$ 次多項式
- 比牛頓-科茨公式效率更高

### 4.4 Romberg 積分 (Romberg Integration)

**原理**：Richardson 外推法 + 複合梯形法則

**思想**：利用兩種不同步長的結果，消除主導誤差項。

**Romberg 表格**：
$$R_{k,1} = \frac{h_k}{2}\left[f(a) + f(b) + 2\sum_{i=1}^{2^{k-1}-1}f(a + ih_k)\right]$$

$$R_{k,j} = \frac{4^j R_{k,j-1} - R_{k-1,j-1}}{4^j - 1}$$

```python
class RombergIntegration:
    def integrate(self, f: Callable, a: float, b: float, max_iterations: int = 10, tolerance: float = 1e-10):
        R = [[0.0] * max_iterations for _ in range(max_iterations)]
        R[0][0] = (b - a) * (f(a) + f(b)) / 2
        for i in range(1, max_iterations):
            h = (b - a) / (2 ** i)
            total = sum(f(a + k * h) for k in range(1, 2 ** i, 2))
            R[i][0] = h * (f(a) + f(b) + 2 * total) / 2
            for j in range(1, i + 1):
                factor = 4 ** j
                R[i][j] = (factor * R[i][j - 1] - R[i - 1][j - 1]) / (factor - 1)
            if abs(R[i][i] - R[i - 1][i - 1]) < tolerance:
                return (R[i][i], i + 1)
        return (R[max_iterations - 1][max_iterations - 1], max_iterations)
```

---

## 5. 數值微分 (Numerical Differentiation)

### 5.1 前向差分 (Forward Difference)

$$f'(x) \approx \frac{f(x+h) - f(x)}{h}$$

**誤差**：$O(h)$（一階精度）

### 5.2 後向差分 (Backward Difference)

$$f'(x) \approx \frac{f(x) - f(x-h)}{h}$$

**誤差**：$O(h)$（一階精度）

### 5.3 中央差分 (Central Difference)

$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$

**誤差**：$O(h^2)$（二階精度）

**二階導數中央差分**：
$$f''(x) \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$$

### 5.4 數值微分的誤差分析

數值微分的誤差來源：
1. **截斷誤差**：有限項近似產生的誤差
2. **捨入誤差**：浮點運算產生的誤差

總誤差 ≈ 截斷誤差 + 捨入誤差

最佳步長 $h$ 通過最小化總誤差得到：
$$h_{opt} \approx \sqrt{\frac{\epsilon}{|f''(x)|}}$$

其中 $\epsilon$ 是機器精度。

---

## 6. LU 分解 (LU Decomposition)

### 6.1 基本原理

將矩陣 $A$ 分解為下三角矩陣 $L$ 和上三角矩陣 $U$ 的乘積：
$$A = LU$$

**用途**：求解線性系統 $Ax = b$

1. 解 $Ly = b$（前向代入）
2. 解 $Ux = y$（後向代入）

### 6.2 Doolittle 分解

**分解公式**：
$$u_{ij} = a_{ij} - \sum_{k=1}^{i-1}l_{ik}u_{kj}$$
$$l_{ij} = \frac{a_{ij} - \sum_{k=1}^{j-1}l_{ik}u_{kj}}{u_{jj}}$$

### 6.3 分解的條件

**存在條件**：
- A 的所有順序主子式非零
- 或 A 是嚴格對角優勢矩陣
- 或 A 是對稱正定矩陣

### 6.4 計算複雜度

LU 分解：$O(n^3)$
前向/後向代入：$O(n^2)$
總計求解線性系統：$O(n^3)$

---

## 7. QR 分解 (QR Decomposition)

### 7.1 基本原理

將矩陣 $A$ 分解為正交矩陣 $Q$ 和上三角矩陣 $R$ 的乘積：
$$A = QR$$

其中 $Q^TQ = I$（正交矩陣）。

### 7.2 Gram-Schmidt 正交化

**經典 Gram-Schmidt**：
1. $\mathbf{u}_1 = \mathbf{a}_1$，$\mathbf{e}_1 = \mathbf{u}_1 / \|\mathbf{u}_1\|$
2. $\mathbf{u}_k = \mathbf{a}_k - \sum_{i=1}^{k-1}(\mathbf{a}_k \cdot \mathbf{e}_i)\mathbf{e}_i$
3. $\mathbf{e}_k = \mathbf{u}_k / \|\mathbf{u}_k\|$

**修正 Gram-Schmidt**（數值更穩定）：
在步驟 2 中，使用正交化後的向量而非原始向量。

### 7.3 QR 分解的用途

- 求解線性最小二乘問題
- QR 迭代求特徵值
- 計算矩陣的 QR 分解

### 7.4 Householder 變換

另一種計算 QR 分解的方法，使用 Householder 矩陣：
$$H = I - 2\frac{\mathbf{v}\mathbf{v}^T}{\mathbf{v}^T\mathbf{v}}$$

 Householder 變換能將向量特定位置以下設為零。

---

## 8. 冪迭代法 (Power Iteration)

### 8.1 基本原理

用於計算矩陣的主特徵值（絕對值最大的特徵值）。

**迭代公式**：
$$\mathbf{y}_{k+1} = \frac{A\mathbf{y}_k}{\|A\mathbf{y}_k\|}$$

或等價於：
$$\mathbf{x}^{(k+1)} = A\mathbf{x}^{(k)}, \quad \text{然後正規化}$$

### 8.2 收斂性

若 $A$ 有嚴格主導特徵值 $|\lambda_1| > |\lambda_2| \geq |\lambda_3| \geq ...$，則：

$$\lim_{k \to \infty} \mathbf{x}^{(k)} = \frac{\mathbf{v}_1}{\|\mathbf{v}_1\|}$$

其中 $\mathbf{v}_1$ 是對應 $\lambda_1$ 的特徵向量。

**收斂速率**：
$$|\lambda_1 - \lambda_1^{(k)}| \approx O\left(\left|\frac{\lambda_2}{\lambda_1}\right|^k\right)$$

### 8.3 瑞利商 (Rayleigh Quotient)

特徵值的近似：
$$\lambda^{(k)} = \frac{\mathbf{x}^{(k)T}A\mathbf{x}^{(k)}}{\mathbf{x}^{(k)T}\mathbf{x}^{(k)}}$$

### 8.4 反冪迭代法

用於計算特定特徵值（已知近似值）：

$$(A - \sigma I)^{-1}$$

可用於計算對應於接近 $\sigma$ 的特徵值的特徵向量。

---

## 9. 插值 (Interpolation)

### 9.1 拉格朗日插值 (Lagrange Interpolation)

**基本思想**：構造拉格朗日基多項式

**插值多項式**：
$$L(x) = \sum_{i=0}^{n} y_i \ell_i(x)$$

其中基函數：
$$\ell_i(x) = \prod_{j=0, j \neq i}^{n} \frac{x - x_j}{x_i - x_j}$$

**性質**：
- $\ell_i(x_j) = \delta_{ij}$（Kronecker delta）
- $L(x_i) = y_i$

```python
class LagrangeInterpolation:
    def __init__(self, x_points: List[float], y_points: List[float]):
        self.x_points = x_points
        self.y_points = y_points
        self.n = len(x_points)

    def evaluate(self, x: float) -> float:
        result = 0.0
        for i in range(self.n):
            term = self.y_points[i]
            for j in range(self.n):
                if i != j:
                    term *= (x - self.x_points[j]) / (self.x_points[i] - self.x_points[j])
            result += term
        return result
```

**優點**：公式優美
**缺點**：新增節點需重新計算所有基函數

### 9.2 牛頓均差插值 (Newton's Divided Differences)

**原理**：使用均差表格

**均差定義**：
- 零階均差：$f[x_i] = f(x_i)$
- 一階均差：$f[x_i, x_{i+1}] = \frac{f(x_{i+1}) - f(x_i)}{x_{i+1} - x_i}$
- k 階均差：$f[x_i, x_{i+1}, ..., x_{i+k}] = \frac{f[x_{i+1}, ..., x_{i+k}] - f[x_i, ..., x_{i+k-1}]}{x_{i+k} - x_i}$

**牛頓形式**：
$$P(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + ...$$

```python
class NewtonInterpolation:
    def _compute_divided_diffs(self) -> List[List[float]]:
        n = self.n
        dd = [[0.0] * n for _ in range(n)]
        for i in range(n):
            dd[i][0] = self.y_points[i]
        for j in range(1, n):
            for i in range(n - j):
                denom = self.x_points[i + j] - self.x_points[i]
                if abs(denom) < 1e-15:
                    dd[i][j] = 0.0
                else:
                    dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / denom
        return dd

    def evaluate(self, x: float) -> float:
        result = self.divided_diffs[0][0]
        product = 1.0
        for i in range(1, self.n):
            product *= (x - self.x_points[i - 1])
            result += self.divided_diffs[0][i] * product
        return result
```

**優點**：新增節點只需補充計算
**與拉格朗日的關係**：兩者是同一多項式的不同表示

### 9.3 插值誤差

**餘項公式**：
$$f(x) - P_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i=0}^{n}(x - x_i)$$

對於節點 $x_i$ 等距分布的情況，可能出現龍格現象（Runge phenomenon），即在區間邊界附近振盪。

---

## 10. 樣條插值 (Spline Interpolation)

### 10.1 基本原理

用低階多項式分段逼近，避免高階多項式插值的振盪問題。

**m 次樣條**：分段 m 次多項式，在節點處具有 m-1 階連續導數。

### 10.2 三次樣條 (Cubic Spline)

**定義**：每個小區間 $[x_i, x_{i+1}]$ 上為三次多項式，在整個區間上二階連續可導。

**邊界條件**：
1. **自然邊界**：$S''(x_0) = S''(x_n) = 0$
2. **固定邊界**：$S'(x_0) = f'(x_0)$，$S'(x_n) = f'(x_n)$
3. **週期邊界**：$S'(x_0) = S'(x_n)$，$S''(x_0) = S''(x_n)$

### 10.3 三次樣條的構造

設 $S(x)$ 在節點 $x_i$ 處的二階導數為 $M_i$。

**每個區間的表達式**：
$$S_i(x) = M_i \frac{(x_{i+1}-x)^3}{6h_i} + M_{i+1} \frac{(x-x_i)^3}{6h_i} + \left(y_i - \frac{M_i h_i^2}{6}\right)\frac{x_{i+1}-x}{h_i} + \left(y_{i+1} - \frac{M_{i+1} h_i^2}{6}\right)\frac{x-x_i}{h_i}$$

其中 $h_i = x_{i+1} - x_i$。

**M 的求解**（三對角方程組）：
$$\frac{h_{i-1}}{6}M_{i-1} + \frac{h_{i-1}+h_i}{3}M_i + \frac{h_i}{6}M_{i+1} = \frac{y_{i+1}-y_i}{h_i} - \frac{y_i - y_{i-1}}{h_{i-1}}$$

### 10.4 樣條插值的優點

- 避免了高階多項式插值的龍格現象
- 函數光滑性好（二階連續導數）
- 收斂性好（隨節點加密而收斂）

### 10.5 B-樣條 (B-spline)

更通用的樣條表示，使用基函數：

$$S(x) = \sum_{i=0}^{n} c_i B_{i,k}(x)$$

其中 $B_{i,k}(x)$ 是 k 階 B-樣條基函數，具有局部支撐性。

---

## 參考文獻

1. Burden, R. L., & Faires, J. D. - *Numerical Analysis* (第10版)
2. Quarteroni, A., Sacco, R., & Saleri, F. - *Numerical Mathematics*
3. Heath, M. T. - *Scientific Computing: An Introductory Survey*
4. Stoer, J., & Bulirsch, R. - *Introduction to Numerical Analysis*