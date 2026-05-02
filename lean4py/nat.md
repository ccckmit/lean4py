# 自然数模块 (nat.py) 数学原理文档

## 1. Peano 公理体系

自然数是数学中最基础的概念之一。Peano 公理为自然数提供了严格的公理化定义：

1. **0 是自然数**
2. **每个自然数有一个唯一的后继 (successor)**
3. **0 不是任何自然数的后继**
4. **不同的自然数有不同的后继**（若 $n \neq m$，则 $S(n) \neq S(m)$）
5. **数学归纳法**：若某性质对 0 成立，且蕴含对后继也成立，则对所有自然数成立

在本模块中，`Nat` 类实现了这一公理体系：

```python
class Nat:
    def __init__(self, n: int):
        if n < 0:
            raise ValueError("自然数必须非负")
        self.n = n
```

自然数存储为内部整数 `n`，通过 `succ()` 和 `pred()` 函数实现后继和前驱操作。

---

## 2. 后继函数 (Successor Function)

**定义**: $\text{succ}(n) = n + 1$

后继函数是 Peano 公理的核心，它将任意自然数映射到其"下一个"数。

**实现** (`lean4py/nat.py:60-62`):

```python
def succ(n: Nat) -> Nat:
    """返回 n 的后继 (n + 1)。"""
    return Nat(n.n + 1)
```

数学性质：
- $\text{succ}(0) = 1$
- $\text{succ}(1) = 2$
- $\text{succ}(n) > n$（严格单调性）

---

## 3. 前驱函数 (Predecessor Function)

**定义**: $\text{pred}(n) = \max(0, n-1)$

前驱函数是后继函数的"逆运算"，但对于 0 的前驱需要特殊处理（0 没有前驱，约定返回 0）。

**实现** (`lean4py/nat.py:65-67`):

```python
def pred(n: Nat) -> Nat:
    """返回 n 的前驱 (max(0, n-1))。"""
    return Nat(max(0, n.n - 1))
```

数学性质：
- $\text{pred}(0) = 0$（约定）
- $\text{pred}(1) = 0$
- $\text{pred}(n) < n$（当 $n > 0$ 时）

---

## 4. 数学归纳法 (Mathematical Induction)

**原理**：设 $P(n)$ 为关于自然数 $n$ 的命题。欲证 $P(n)$ 对所有 $n \in \mathbb{N}$ 成立，只需证明：
1. **基例**：$P(0)$ 成立
2. **归纳步**：若 $P(k)$ 成立，则 $P(k+1)$ 也成立

**实现** (`lean4py/nat.py:75-81`):

```python
class NatInduction:
    """自然数的结构归纳法。"""
    @staticmethod
    def prove(P: callable, n: Nat) -> bool:
        if n.n == 0:
            return P(Nat(0))
        return NatInduction.prove(P, pred(n)) and P(n)
```

**递归结构**：
- 当 $n = 0$ 时，验证 $P(0)$
- 当 $n > 0$ 时，先递归验证 $P(\text{pred}(n))$，再验证 $P(n)$

这实际上验证了从 0 到 $n$ 的所有命题。

---

## 5. 基本算术运算

### 5.1 加法 (Addition)

**定义**：加法可以通过后继函数递归定义：
- $a + 0 = a$
- $a + \text{succ}(b) = \text{succ}(a + b)$

**实现** (`lean4py/nat.py:21-22`):

```python
def __add__(self, other):
    return Nat(self.n + other.n)
```

### 5.2 乘法 (Multiplication)

**定义**：乘法定义为重复加法：
- $a \times 0 = 0$
- $a \times \text{succ}(b) = a + (a \times b)$

**实现** (`lean4py/nat.py:24-25`):

```python
def __mul__(self, other):
    return Nat(self.n * other.n)
```

### 5.3 减法（带钳位）

**定义**：由于自然数不存在负数，减法需要"钳位"到 0：
- $a - b = \max(0, a - b)$

**实现** (`lean4py/nat.py:27-29`):

```python
def __sub__(self, other):
    result = self.n - other.n
    return Nat(result if result >= 0 else 0)
```

**数学意义**：这对应于自然数的"截断减法"，确保结果仍在 $\mathbb{N}$ 中。

---

## 6. 比较运算

自然数的大小关系基于整数比较：

| 运算 | 方法 | 数学含义 |
|------|------|----------|
| $\leq$ | `__le__` | $a \leq b$ |
| $<$ | `__lt__` | $a < b$ |
| $\geq$ | `__ge__` | $a \geq b$ |
| $>$ | `__gt__` | $a > b$ |

**实现** (`lean4py/nat.py:31-41`):

```python
def __le__(self, other): return self.n <= other.n
def __lt__(self, other): return self.n < other.n
def __ge__(self, other): return self.n >= other.n
def __gt__(self, other): return self.n > other.n
```

---

## 7. 阶乘与斐波那契数列

### 7.1 阶乘 (Factorial)

**定义**：
$$n! = \begin{cases} 1 & \text{if } n = 0 \\ n \times (n-1)! & \text{if } n > 0 \end{cases}$$

**数学性质**：
- $0! = 1$（空积）
- $n!$ 表示 $n$ 个元素的全排列数

**实现** (`lean4py/nat.py:114-119`):

```python
def factorial(n: Nat) -> Nat:
    """返回 n! (n 的阶乘)。"""
    result = 1
    for i in range(2, n.n + 1):
        result *= i
    return Nat(result)
```

### 7.2 斐波那契数列 (Fibonacci Sequence)

**定义**：
$$\text{fib}(n) = \begin{cases} 0 & \text{if } n = 0 \\ 1 & \text{if } n = 1 \\ \text{fib}(n-1) + \text{fib}(n-2) & \text{if } n > 1 \end{cases}$$

**数学性质**：
- 前几个值：$0, 1, 1, 2, 3, 5, 8, 13, 21, 34, \ldots$
- 斐波那契数与黄金比例有关：$\lim_{n \to \infty} \frac{\text{fib}(n+1)}{\text{fib}(n)} = \varphi = \frac{1+\sqrt{5}}{2}$

**实现** (`lean4py/nat.py:122-129`):

```python
def fibonacci(n: Nat) -> Nat:
    """返回第 n 个斐波那契数 (0-indexed: fib(0)=0, fib(1)=1)。"""
    if n.n <= 1:
        return n
    a, b = Nat(0), Nat(1)
    for _ in range(2, n.n + 1):
        a, b = b, Nat(a.n + b.n)
    return b
```

此实现使用迭代而非递归，时间复杂度为 $O(n)$。

---

## 8. 欧几里得算法（求最大公约数）

**欧几里得算法**：给定两数 $a, b$，求 $\gcd(a, b)$。

**原理**（辗转相除法）：
$$\gcd(a, b) = \begin{cases} a & \text{if } b = 0 \\ \gcd(b, a \bmod b) & \text{if } b \neq 0 \end{cases}$$

**数学性质**：
- $\gcd(a, b)$ 是 $a$ 和 $b$ 的最大公约数
- 贝祖定理：$\gcd(a, b)$ 可以表示为 $ax + by$（$x, y \in \mathbb{Z}$）

**实现** (`lean4py/nat.py:132-137`):

```python
def nat_gcd(a: Nat, b: Nat) -> Nat:
    """使用欧几里得算法计算两个自然数的最大公约数。"""
    a_val, b_val = a.n, b.n
    while b_val != 0:
        a_val, b_val = b_val, a_val % b_val
    return Nat(a_val)
```

**正确性证明思路**：
- 若 $b = 0$，则 $\gcd(a, 0) = a$
- 若 $b \neq 0$，设 $r = a \bmod b$，则 $a = bq + r$，其中 $0 \leq r < b$
- 任何 $a$ 和 $b$ 的公约数也是 $b$ 和 $r$ 的公约数，反之亦然
- 故 $\gcd(a, b) = \gcd(b, r)$

---

## 9. 素数判定

**定义**：素数是大于 1 的自然数，且只有 1 和自身两个正因数。

**判定算法** (`lean4py/nat.py:140-152`):

```python
def nat_is_prime(n: Nat) -> bool:
    """判断 n 是否为素数。"""
    v = n.n
    if v < 2:
        return False
    if v == 2:
        return True
    if v % 2 == 0:
        return False
    for i in range(3, int(v ** 0.5) + 1, 2):
        if v % i == 0:
            return False
    return True
```

**数学原理**：
1. $n < 2$：不是素数（0 和 1 既不是素数也不是合数）
2. $n = 2$：唯一的偶素数
3. $n$ 为偶数：不是素数（除了 2）
4. 只需检查到 $\sqrt{n}$：
   - 若 $n$ 是合数，则 $n = a \times b$，其中 $a \leq b$
   - 若 $a > \sqrt{n}$，则 $b < \sqrt{n}$，矛盾
   - 故合数必有一个因子 $\leq \sqrt{n}$
5. 只需检查奇数（偶数已被排除）

**时间复杂度**：$O(\sqrt{n})$，是朴素的素数判定算法。

---

## 模块 API 速查表

| 函数/类 | 说明 |
|---------|------|
| `Nat(n)` | 创建自然数 $n$ |
| `succ(n)` | 返回 $n + 1$ |
| `pred(n)` | 返回 $\max(0, n-1)$ |
| `NatInduction.prove(P, n)` | 验证命题 $P(0)$ 到 $P(n)$ |
| `factorial(n)` | 返回 $n!$ |
| `fibonacci(n)` | 返回第 $n$ 个斐波那契数 |
| `nat_gcd(a, b)` | 返回 $\gcd(a, b)$ |
| `nat_is_prime(n)` | 判断 $n$ 是否为素数 |
| `nat_even(n)` | 判断 $n$ 是否为偶数 |
| `nat_odd(n)` | 判断 $n$ 是否为奇数 |

---

*本文档对应 lean4py 版本 1.34.0*