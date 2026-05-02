# 數論測試文檔

本文檔說明 `test_number_theory.py` 和 `test_number_theory_enhanced.py` 中測試用例背後的數學原理。

## 1. 整數類別測試 (TestInteger)

### 測試內容
- 整數的創建、負數處理
- 相等性比較（使用 `==` 運算子）
- 基本算術運算：加、減、乘、負號
- 絕對值運算
- 大小比較運算
- 零、正數、負數的判定

### 數學原理
`Integer` 類別實現了整數環 $\mathbb{Z}$ 的基本代數結構，支援封閉的加法、減法、乘法運算。每個整數都有唯一的加法逆元（負數）和乘法性質。

---

## 2. 可整除性測試 (TestDivisibility)

### 測試內容
```python
assert divides(Integer(3), Integer(12)) == True   # 3 | 12
assert divides(Integer(5), Integer(12)) == False  # 5 ∤ 12
assert divides(Integer(0), Integer(0)) == True    # 0 | 0
assert divides(Integer(3), Integer(0)) == True    # 3 | 0
```

### 數學原理
**可整除性**（Divisibility）：若存在整數 $k$ 使得 $a = b \cdot k$，則稱 $b$ 整除 $a$，記作 $b \mid a$。

特殊情況：
- 對於任何非零整數 $a$，有 $a \mid 0$（因為 $0 = a \cdot 0$）
- $0 \mid 0$ 在數學上是有爭議的，但在計算機實現中通常定義為 True

---

## 3. GCD 與歐幾里得算法測試 (TestGcdLcm)

### 測試內容
```python
assert gcd(Integer(12), Integer(18)) == Integer(6)
assert gcd(Integer(7), Integer(5)) == Integer(1)
assert gcd(Integer(-12), Integer(18)) == Integer(6)  # 負數處理
assert lcm(Integer(4), Integer(6)) == Integer(12)
assert lcm(Integer(0), Integer(5)) == Integer(0)    # 零的特殊情況
```

### 數學原理

**最大公約數 (GCD)**： Greatest Common Divisor

兩個整數 $a$ 和 $b$ 的最大公約數是同時整除兩數的最大正整數。

**歐幾里得算法**：
$$\gcd(a, b) = \gcd(b, a \bmod b)$$

迭代直到 $b = 0$，則 $\gcd(a, 0) = |a|$。

**最小公倍數 (LCM)**：
$$\text{lcm}(a, b) = \frac{|a \cdot b|}{\gcd(a, b)}$$

**Bezout 恆等式**：存在整數 $x, y$ 使得
$$ax + by = \gcd(a, b)$$

---

## 4. 質數測試 (TestPrime)

### 測試內容
```python
assert is_prime(Integer(2)) == True
assert is_prime(Integer(17)) == True
assert is_prime(Integer(15)) == False
assert is_prime(Integer(0)) == False
assert is_prime(Integer(1)) == False
assert is_prime(Integer(-5)) == False
assert prime_factors(Integer(12)) == [Integer(2), Integer(2), Integer(3)]
assert prime_factors(Integer(1)) == []
```

### 數學原理

**質數定義**：大於 1 的正整數，除了 1 和自身外，沒有其他正因子。

**質數判定**：通常使用試除法，檢查 $2$ 到 $\sqrt{n}$ 之間的所有整數是否整除 $n$。

**算術基本定理**（Fundamental Theorem of Arithmetic）：
每個大於 1 的整數都可以唯一分解為質數的乘積（忽略順序）。

---

## 5. 歐拉 phi 函數測試 (TestEulerPhi)

### 測試內容
```python
assert phi(Integer(1)) == Integer(1)
assert phi(Integer(2)) == Integer(1)
assert phi(Integer(10)) == Integer(4)
assert phi(Integer(12)) == Integer(4)
assert phi(Integer(7)) == Integer(6)
```

### 數學原理

**歐拉 phi 函數** $\varphi(n)$：表示小於 $n$ 且與 $n$ 互質的正整數個數。

$$\varphi(n) = n \prod_{p \mid n}\left(1 - \frac{1}{p}\right)$$

其中 $p$ 遍歷 $n$ 的所有質因數。

例子：
- $\varphi(10) = 10 \cdot (1 - 1/2) \cdot (1 - 1/5) = 10 \cdot 1/2 \cdot 4/5 = 4$
- $\varphi(7) = 7 \cdot (1 - 1/7) = 6$（質數的 phi 值為 $p-1$）

---

## 6. 同餘運算測試 (TestModExp, TestModInverse)

### 測試內容
```python
# 模冪運算
assert mod_exp(Integer(2), Integer(10), Integer(1024)) == Integer(0)
assert mod_exp(Integer(2), Integer(3), Integer(7)) == Integer(1)

# 模逆元
inv = mod_inverse(Integer(3), Integer(11))
assert (3 * inv.n) % 11 == 1  # 3^(-1) ≡ 4 (mod 11)

# 不存在逆元的情況
inv = mod_inverse(Integer(2), Integer(4))  # 返回 None
```

### 數學原理

**模冪運算**：計算 $a^e \bmod m$，使用快速冪算法（重複平方法）可以在 $O(\log e)$ 時間內完成。

**模逆元**：若 $\gcd(a, m) = 1$，則存在唯一的模逆元 $a^{-1}$ 使得：
$$a \cdot a^{-1} \equiv 1 \pmod{m}$$

逆元存在的充要條件：$\gcd(a, m) = 1$（即 $a$ 和 $m$ 互質）。

---

## 7. 互質測試 (TestCoprime)

### 測試內容
```python
assert coprime(Integer(7), Integer(11)) == True   # gcd(7,11) = 1
assert coprime(Integer(12), Integer(18)) == False  # gcd(12,18) = 6 ≠ 1
```

### 數學原理

**互質**：兩個整數的最大公約數為 1，記作 $\gcd(a, b) = 1$。

---

## 8. 中國剩餘定理測試 (TestChineseRemainder)

### 測試內容
```python
result = chinese_remainder(Integer(2), Integer(3), Integer(3), Integer(5))
assert result.n % 3 == 2  # 結果 ≡ 2 (mod 3)
assert result.n % 5 == 3  # 結果 ≡ 3 (mod 5)
```

### 數學原理

**中國剩餘定理**（Chinese Remainder Theorem）：

若 $m_1, m_2, \ldots, m_k$ 兩兩互質，則同餘方程組：
$$x \equiv a_1 \pmod{m_1}$$
$$x \equiv a_2 \pmod{m_2}$$
$$\vdots$$
$$x \equiv a_k \pmod{m_k}$$

必有唯一解（模 $M = m_1 \cdot m_2 \cdots m_k$）。

---

## 9. 整數歸納法測試 (TestIntegerInduction)

### 測試內容
```python
P = lambda k: k.n >= 0
assert IntegerInduction.prove(P, Integer(10)) == True

assert IntegerInduction.prove_by_strong(P, Integer(100)) == True
```

### 數學原理

**數學歸納法**（Mathematical Induction）：
1. **基例**：證明 $P(0)$ 或 $P(1)$ 成立
2. **歸納步驟**：假設 $P(k)$ 成立，證明 $P(k+1)$ 成立

**強歸納法**（Strong Induction）：
1. **基例**：證明 $P(0)$ 或 $P(1)$ 成立
2. **歸納步驟**：假設對所有 $0 \leq i \leq k$，$P(i)$ 成立，證明 $P(k+1)$ 成立

---

## 10. 增強測試擴展內容

### 10.1 勒讓德符號 (LegendreSymbol)

測試二次剩餘判定：
- $\left(\frac{a}{p}\right) = 1$：$a$ 是模 $p$ 的二次剩餘
- $\left(\frac{a}{p}\right) = -1$：$a$ 不是二次剩餘
- $\left(\frac{a}{p}\right) = 0$：$p \mid a$

### 10.2 二次互反律 (QuadraticReciprocity)

**二次互反律**：對於奇質數 $p, q$：
$$\left(\frac{p}{q}\right) \left(\frac{q}{p}\right) = (-1)^{\frac{(p-1)(q-1)}{4}}$$

### 10.3 p 進數 (PadicNumbers)

$p$ 進數賦予整數一種新的度量方式，適用於數論研究。

### 10.4 狄利克雷特徵 (DirichletCharacter)

用於研究等差數列中的質數分布。

### 10.5 質數定理 (PrimeNumberTheorem)

質數計數函數 $\pi(x) \sim \frac{x}{\ln x}$（當 $x \to \infty$）。

---

## 測試函數對照表

| 測試類別 | 測試函數 | 數學概念 |
|---------|---------|---------|
| TestInteger | 基本運算 | 整數環 $\mathbb{Z}$ |
| TestDivisibility | `divides()` | 可整除性 |
| TestGcdLcm | `gcd()`, `lcm()` | GCD/LCM |
| TestBezoutIdentity | `bezout_identity()` | Bezout 恆等式 |
| TestPrime | `is_prime()`, `prime_factors()` | 質數、質因數分解 |
| TestEulerPhi | `phi()` | 歐拉 phi 函數 |
| TestModExp | `mod_exp()` | 模冪運算 |
| TestModInverse | `mod_inverse()` | 模逆元 |
| TestCoprime | `coprime()` | 互質 |
| TestChineseRemainder | `chinese_remainder()` | 中國剩餘定理 |
| TestIntegerInduction | `prove()`, `prove_by_strong()` | 數學歸納法 |
| TestLegendreSymbol | `legendre_symbol()` | 勒讓德符號 |
| TestQuadraticReciprocity | `reciprocal()` | 二次互反律 |
| TestPadicNumbers | p 進數運算 | p 進數 |
| TestDirichletCharacter | `evaluate()` | 狄利克雷特徵 |
| TestPrimeNumberTheorem | `pi()` | 質數定理 |