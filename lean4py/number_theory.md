# Number Theory Module (數論模組)

本模組實現了數論的基礎概念與演算法，支援整數運算、最大公因數、質數測試、同餘運算等功能。

---

## 1. 可除性 (Divisibility)

**定義**：對於整數 a 和 b，若存在整數 q 使得 b = qa，則稱 a 能整除 b，記為 a | b。

```python
def divides(d: Integer, n: Integer) -> bool:
    if n.n == 0:
        return True
    if d.n == 0:
        return False
    return n.n % d.n == 0
```

**性質**：
- 若 a | b 且 b | c，則 a | c（傳遞性）
- 若 a | b 且 a | c，則 a | (b ± c)
- 若 a | b，則 a | bc（對任意整數 c）

---

## 2. 除法演算法 (Division Algorithm)

**定理**：對於任意整數 a 和正整數 b，存在唯一的商 q 和餘數 r，使得：
$$a = bq + r, \quad 0 \leq r < b$$

```python
# Integer 類的 __truediv__ 實現
def __truediv__(self, other):
    if isinstance(other, Integer):
        if other.n == 0:
            raise ZeroDivisionError("division by zero")
        return Integer(self.n // other.n)
```

---

## 3. 最大公因數與歐幾里得演算法 (GCD & Euclidean Algorithm)

**定義**：最大公因數 gcd(a, b) 是同時整除 a 和 b 的最大正整數。

**歐幾里得演算法**：基於 gcd(a, b) = gcd(b, a mod b)

```python
def gcd(a: Integer, b: Integer) -> Integer:
    a_abs, b_abs = abs(a.n), abs(b.n)
    while b_abs != 0:
        a_abs, b_abs = b_abs, a_abs % b_abs
    return Integer(a_abs)
```

**最小公倍數**：$$\text{lcm}(a, b) = \frac{|ab|}{\gcd(a, b)}$$

```python
def lcm(a: Integer, b: Integer) -> Optional[Integer]:
    if a.n == 0 or b.n == 0:
        return Integer(0)
    return Integer(abs(a.n * b.n) // gcd(a, b).n)
```

---

## 4. 擴展歐幾里得演算法與貝祖定理 (Extended Euclidean Algorithm & Bezout's Identity)

**貝祖定理**：若 d = gcd(a, b)，則存在整數 x, y 使得：
$$ax + by = d$$

特別地，當 a, b 互質時，ax + by = 1。

```python
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return (1, 0, a)
    x1, y1, g = extended_gcd(b, a % b)
    return (y1, x1 - (a // b) * y1, g)

def bezout_identity(a: Integer, b: Integer) -> Tuple[Integer, Integer, Integer]:
    x, y, d = extended_gcd(a.n, b.n)
    return (Integer(x), Integer(y), Integer(d))
```

---

## 5. 質數與算術基本定理 (Prime Numbers & Fundamental Theorem of Arithmetic)

**質數定義**：大於 1 的正整數，除了 1 和自身外無法被其他正整數整除。

**算術基本定理**：每個大於 1 的整數都可以唯一分解為質數的乘積（順序除外）。

**Miller-Rabin 質數測試**（概率演算法）：

```python
def is_prime(n: Integer, k: int = 5) -> bool:
    """Miller-Rabin probabilistic primality test."""
    v = n.n
    if v < 2:
        return False
    if v == 2 or v == 3:
        return True
    if v % 2 == 0:
        return False
    
    # Write v-1 = d * 2^r
    d = v - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    import random
    for _ in range(k):
        a = random.randrange(2, v-1)
        x = pow(a, d, v)
        if x == 1 or x == v-1:
            continue
        for _ in range(r-1):
            x = (x * x) % v
            if x == v-1:
                break
        else:
            return False
    return True
```

**質因數分解**：

```python
def prime_factors(n: Integer) -> List[Integer]:
    v = n.n
    if v == 0:
        return []
    if v == 1:
        return []
    factors = []
    d = 2
    temp = abs(v)
    while d * d <= temp:
        while temp % d == 0:
            factors.append(Integer(d))
            temp //= d
        d += 1
    if temp > 1:
        factors.append(Integer(temp))
    return factors
```

---

## 6. 同餘關係 (Congruences)

**定義**：對於整數 a, b 和正整數 n，若 n | (a - b)，則稱 a 與 b 模 n 同餘，記為：
$$a \equiv b \pmod{n}$$

**基本性質**：
- 若 a ≡ b (mod n)，則 a + c ≡ b + c (mod n)
- 若 a ≡ b (mod n)，則 ac ≡ bc (mod n)
- 若 a ≡ b (mod n) 且 b ≡ c (mod n)，則 a ≡ c (mod n)

**模指數運算**：

```python
def mod_exp(base: Integer, exp: Integer, mod: Integer) -> Integer:
    if mod.n == 0:
        raise ValueError("modulus cannot be zero")
    result = 1
    b = base.n % mod.n
    e = exp.n
    if e < 0:
        raise ValueError("exponent must be non-negative")
    while e > 0:
        if e % 2 == 1:
            result = (result * b) % mod.n
        e //= 2
        b = (b * b) % mod.n
    return Integer(result)
```

**模逆元**：

```python
def mod_inverse(a: Integer, m: Integer) -> Optional[Integer]:
    if m.n <= 0:
        return None
    x, y, g = extended_gcd(a.n, m.n)
    if g != 1:
        return None
    return Integer((x % m.n + m.n) % m.n)
```

---

## 7. 歐拉函數 (Euler's Totient Function)

**定義**：φ(n) 定義為 1 到 n 中與 n 互質的整數個數。

**計算公式**：若 n 的質因數分解為 $n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$，則：
$$\phi(n) = n \prod_{i=1}^{k} \left(1 - \frac{1}{p_i}\right)$$

```python
def phi(n: Integer) -> Integer:
    v = n.n
    if v <= 0:
        return Integer(0)
    if v == 1:
        return Integer(1)
    factors = prime_factors(n)
    result = v
    seen = set()
    for p in factors:
        if p.n not in seen:
            seen.add(p.n)
            result -= result // p.n
    return Integer(result)
```

---

## 8. 歐拉定理 (Euler's Theorem)

**定理**：若 gcd(a, n) = 1，則：
$$a^{\phi(n)} \equiv 1 \pmod{n}$$

**應用**：可用於計算大數的模指數和密碼學中的 RSA 演算法。

---

## 9. 費馬小定理 (Fermat's Little Theorem)

**定理**：若 p 為質數，則對任意整數 a：
$$a^p \equiv a \pmod{p}$$

若 p ∤ a，則：
$$a^{p-1} \equiv 1 \pmod{p}$$

**Miller-Rabin 測試**基於此定理的逆否命題。

---

## 10. 中國剩餘定理 (Chinese Remainder Theorem)

**定理**：若 $m_1, m_2, \ldots, m_k$ 兩兩互質，則對任意整數 $a_1, a_2, \ldots, a_k$，同餘方程組：
$$x \equiv a_i \pmod{m_i}, \quad i = 1, 2, \ldots, k$$

必有唯一解（模 $M = m_1 m_2 \cdots m_k$）。

```python
def chinese_remainder(r1: Integer, m1: Integer, r2: Integer, m2: Integer) -> Optional[Integer]:
    s, t, g = extended_gcd(m1.n, m2.n)
    if g != 1:
        return None
    n = r1.n + m1.n * ((r2.n - r1.n) * s % m2.n)
    return Integer(n % (m1.n * m2.n))
```

---

## 11. Diffie-Hellman 密鑰交換（應用）

**原理**：基於離散對數問題的困難性。

雙方約定大質數 p 和原根 g：
1. Alice 選秘密值 a，發送 $A = g^a \mod p$
2. Bob 選秘密值 b，發送 $B = g^b \mod p$
3. 雙方計算共享密鑰：$K = B^a \mod p = A^b \mod p = g^{ab} \mod p$

本模組的 `mod_exp` 函數提供了模指數運算能力。

---

## 12. 威爾遜定理 (Wilson's Theorem)

**定理**：p 為質數的充要條件是：
$$(p-1)! \equiv -1 \pmod{p}$$

**逆否命題**：若 $(p-1)! \equiv -1 \pmod{p}$，則 p 為質數。

**應用**：可用於質數判定，但計算階層的成本較高。

---

## 補充內容

### 勒讓德符號 (Legendre Symbol)

對於奇質數 p，勒讓德符號 $\left(\frac{a}{p}\right)$ 定義為：
- 0：若 p | a
- 1：若 a 是模 p 的二次剩餘
- -1：若 a 是模 p 的二次非剩餘

根據歐拉準則：
$$\left(\frac{a}{p}\right) \equiv a^{\frac{p-1}{2}} \pmod{p}$$

```python
class LegendreSymbol:
    @staticmethod
    def legendre_symbol(a: int, p: int) -> int:
        if p <= 2 or p % 2 == 0:
            raise ValueError("p must be an odd prime")
        a = a % p
        if a == 0:
            return 0
        result = pow(a, (p - 1) // 2, p)
        if result == 1:
            return 1
        elif result == p - 1:
            return -1
        return result
```

### 二次互反律 (Quadratic Reciprocity)

**高斯互反律**：對於兩個奇質數 p, q：
$$\left(\frac{p}{q}\right) \left(\frac{q}{p}\right) = (-1)^{\frac{(p-1)(q-1)}{4}}$$

```python
class QuadraticReciprocity:
    @staticmethod
    def reciprocal(p: int, q: int) -> bool:
        if p % 2 == 0 or q % 2 == 0:
            return True
        legendre_pq = LegendreSymbol.legendre_symbol(p, q)
        legendre_qp = LegendreSymbol.legendre_symbol(q, p)
        exponent = ((p - 1) // 2) * ((q - 1) // 2)
        sign = -1 if exponent % 2 == 1 else 1
        return legendre_pq * legendre_qp == sign
```

### 質數定理 (Prime Number Theorem)

**定理**：設 π(x) 為不超過 x 的質數個數，則：
$$\lim_{x \to \infty} \frac{\pi(x)}{x / \ln x} = 1$$

即 π(x) ≈ x / ln x。

```python
class PrimeNumberTheorem:
    @staticmethod
    def pi(x: float) -> int:
        if x < 2:
            return 0
        count = 0
        for n in range(2, int(x) + 1):
            is_prime = True
            for d in range(2, int(n**0.5) + 1):
                if n % d == 0:
                    is_prime = False
                    break
            if is_prime:
                count += 1
        return count
```

### p進數 (p-adic Numbers)

p進數是數論中的重要工具，其範數定義為：
$$|x|_p = p^{-v_p(x)}$$

其中 $v_p(x)$ 是 x 的 p進賦值。

```python
class PadicNumbers:
    def __init__(self, p: int, valuation: int = 0):
        self.p = p
        self.valuation = valuation

    def norm(self) -> float:
        if self.valuation == 0:
            return 1.0
        return self.p ** (-self.valuation)
```

---

## API 速查表

| 函數 | 說明 |
|------|------|
| `Integer(n)` | 建立整數物件 |
| `gcd(a, b)` | 最大公因數 |
| `lcm(a, b)` | 最小公倍數 |
| `extended_gcd(a, b)` | 擴展歐幾里得演算法 |
| `bezout_identity(a, b)` | 貝祖恆等式 |
| `is_prime(n)` | Miller-Rabin 質數測試 |
| `prime_factors(n)` | 質因數分解 |
| `phi(n)` | 歐拉函數 |
| `mod_exp(base, exp, mod)` | 模指數運算 |
| `mod_inverse(a, m)` | 模逆元 |
| `divides(d, n)` | 可除性判斷 |
| `chinese_remainder(r1, m1, r2, m2)` | 中國剩餘定理 |
| `coprime(a, b)` | 互質判斷 |