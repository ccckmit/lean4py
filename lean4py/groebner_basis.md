# Gröbner 基底数学原理

本文档解释 `groebner_basis.py` 模块中实现的 Gröbner 基底算法的数学原理。

## 1. 单项式序 (Monomial Orderings)

单项式序是多变量多项式环中定义单项式比较规则的数学基础。

### 1.1 字典序 (Lexicographic Order)

**定义**：对于两个单项式 $x^\alpha = x_1^{\alpha_1} \cdots x_n^{\alpha_n}$ 和 $x^\beta = x_1^{\beta_1} \cdots x_n^{\beta_n}$，若存在索引 $k$ 使得：
$$\alpha_1 = \beta_1, \ldots, \alpha_{k-1} = \beta_{k-1}, \alpha_k < \beta_k$$
则 $x^\alpha <_{lex} x^\beta$。

**代码实现** (`groebner_basis.py:36-46`)：
```python
def _lex_compare(self, mon1: Tuple[int, ...], mon2: Tuple[int, ...]) -> int:
    """Lexicographic comparison."""
    max_len = max(len(mon1), len(mon2))
    e1 = list(mon1) + [0] * (max_len - len(mon1))
    e2 = list(mon2) + [0] * (max_len - len(mon2))
    for a, b in zip(e1, e2):
        if a < b:
            return -1
        if a > b:
            return 1
    return 0
```

**应用**：用于消元理论（elimination theory），按字典序计算的 Gröbner 基底可直接读出解。

### 1.2 次数字典序 (Degree Lexicographic Order)

**定义**：先比较总次数 $\deg(\alpha) = \sum \alpha_i$，次数高者优先；若次数相同，再按字典序比较。

**代码实现** (`groebner_basis.py:63-68`)：
```python
def _dlex_compare(self, mon1: Tuple[int, ...], mon2: Tuple[int, ...]) -> int:
    """Degree lexicographic."""
    total1, total2 = sum(mon1), sum(mon2)
    if total1 != total2:
        return -1 if total1 < total2 else 1
    return self._lex_compare(mon1, mon2)
```

### 1.3 次数反字典序 (Graded Reverse Lexicographic Order)

**定义**：先比较总次数；若次数相同，从最后一个变量开始比较（反向字典序）。

**代码实现** (`groebner_basis.py:48-61`)：
```python
def _grevlex_compare(self, mon1: Tuple[int, ...], mon2: Tuple[int, ...]) -> int:
    """Graded reverse lexicographic."""
    total1, total2 = sum(mon1), sum(mon2)
    if total1 != total2:
        return -1 if total1 < total2 else 1
    max_len = max(len(mon1), len(mon2))
    e1 = list(mon1) + [0] * (max_len - len(mon1))
    e2 = list(mon2) + [0] * (max_len - len(mon2))
    for a, b in reversed(list(zip(e1, e2))):
        if a < b:
            return -1
        if a > b:
            return 1
    return 0
```

## 2. 多变量多项式除法

### 2.1 除法算法

给定多项式 $f$ 和多项式列表 $G = (g_1, \ldots, g_s)$，除法算法将 $f$ 表示为：
$$f = q_1 g_1 + q_2 g_2 + \cdots + q_s g_s + r$$
其中 $r$ 是余式，$q_i$ 是商。

**算法步骤**：
1. 令 $f_0 = f$
2. 对 $i = 1, \ldots, s$ 重复：若 $LM(g_i)$ 整除 $f_{i-1}$ 的首项，则执行除法并更新
3. 直到 $f_{i-1}$ 的任何项都无法被任何 $LM(g_j)$ 整除
4. 余式 $r = f_k$

### 2.2 代码实现

`_reduce_polynomial` 方法 (`groebner_basis.py:236-258`) 实现了多项式约化：
```python
def _reduce_polynomial(self, p: Polynomial, G: List[Polynomial]) -> Polynomial:
    """Reduce polynomial by Groebner basis G."""
    result = p
    for _ in range(len(G)):
        changed = False
        for g in G:
            lm_g = g.leading_monomial()
            if not lm_g:
                continue
            for m, c in result.coeffs.items():
                if all(m[i] >= lm_g[i] for i in range(len(lm_g))):
                    # 执行约化步骤
                    ...
                    changed = True
                    break
            if changed:
                break
        if not changed:
            break
    return result
```

**关键性质**：当 $G$ 是 Gröbner 基底时，余式 $r$ 是唯一的，与除法顺序无关。

## 3. S-多项式与 S-对 (S-Polynomials and S-Pairs)

### 3.1 S-多项式定义

设 $p_1, p_2$ 为两个非零多项式，$LM(p_1) = x^\alpha$，$LM(p_2) = x^\beta$。令 $x^\gamma = \text{lcm}(x^\alpha, x^\beta)$，则：
$$\text{SPoly}(p_1, p_2) = \frac{x^\gamma}{LM(p_1)} \cdot \frac{p_1}{LC(p_1)} - \frac{x^\gamma}{LM(p_2)} \cdot \frac{p_2}{LC(p_2)}$$

### 3.2 代码实现

`S_polynomial` 方法 (`groebner_basis.py:187-209`)：
```python
def S_polynomial(self, p1: Polynomial, p2: Polynomial) -> Polynomial:
    """Compute S-polynomial of two polynomials."""
    lm1 = p1.leading_monomial()
    lm2 = p2.leading_monomial()
    if not lm1 or not lm2:
        return p1

    lcm = []
    for a, b in zip(lm1, lm2):
        lcm.append(max(a, b))
    lcm = tuple(lcm)

    m1 = tuple(lcm[i] - lm1[i] for i in range(len(lm1)))
    m2 = tuple(lcm[i] - lm2[i] for i in range(len(lm2)))

    lc1, lc2 = p1.leading_coefficient(), p2.leading_coefficient()
    denom = math.gcd(int(abs(lc1)), int(abs(lc2))) if lc1 and lc2 else 1

    term1 = Polynomial({m1: lc2 // denom}, self.order)
    term2 = Polynomial({m2: lc1 // denom}, self.order)

    sp = p1.multiply(term1).add(p2.multiply(term2))
    return sp
```

### 3.3 S-多项式的意义

S-多项式的设计使得 $LM(\text{SPoly}(p_1, p_2))$ 的首项严格小于 $\max(LM(p_1), LM(p_2))$ 的首项，这保证了 Buchberger 算法中首项的"消除"。

## 4. Buchberger 算法

### 4.1 算法描述

**输入**：多项式集合 $F = \{f_1, \ldots, f_s\}$
**输出**：$F$ 生成的理想 $I$ 的 Gröbner 基底 $G$

**算法**：
1. 令 $G = F$
2. 重复以下步骤直到稳定：
   - 对 $G$ 中每对多项式 $(p, q)$，计算 $\text{SPoly}(p, q)$
   - 将 $\text{SPoly}(p, q)$ 对 $G$ 求余得到 $h$
   - 若 $h \neq 0$，则 $G = G \cup \{h\}$

### 4.2 代码实现

`compute_basis` 方法 (`groebner_basis.py:211-234`)：
```python
def compute_basis(self, polynomials: List[Polynomial],
                 max_iterations: int = 100) -> GroebnerBasis:
    """Compute Groebner basis using Buchberger algorithm."""
    G = list(polynomials)
    for _ in range(max_iterations):
        pairs = []
        for i in range(len(G)):
            for j in range(i + 1, len(G)):
                pairs.append((G[i], G[j]))

        changed = False
        for p1, p2 in pairs:
            sp = self.S_polynomial(p1, p2)
            if sp.is_zero():
                continue
            remainder = self._reduce_polynomial(sp, G)
            if not remainder.is_zero():
                G.append(remainder)
                changed = True

        if not changed:
            break

    return GroebnerBasis(G, self.order)
```

### 4.3 算法复杂度

Buchberger 算法在最坏情况下是双指数级的。但在实践中，对于典型问题效果良好。

## 5. Gröbner 基底的性质

### 5.1 基本性质

**定义**：$G$ 是理想 $I$ 的 Gröbner 基底，当且仅当：
$$\langle LM(I) \rangle = \langle LM(G) \rangle$$
其中 $LM(I)$ 表示 $I$ 中所有多项式首项生成的单项式理想。

**等价条件**（Buchberger 判据）：
$$I = \langle G \rangle \text{ 且 } \forall p, q \in G, \text{SPoly}(p, q) \xrightarrow{G} 0$$

### 5.2 唯一性

对于固定的单项式序，理想 $I$ 的约化 Gröbner 基底是唯一的。

### 5.3 理想成员判定

设 $G$ 是 $I$ 的 Gröbner 基底，则：
$$f \in I \iff f \xrightarrow{G} 0$$

代码中 `PolynomialIdeal.contains` 方法 (`groebner_basis.py:267-269`) 目前返回 False，待实现。

## 6. 应用

### 6.1 多项式方程组求解

给定方程组：
$$\begin{cases}
f_1(x_1, \ldots, x_n) = 0 \\
f_2(x_1, \ldots, x_n) = 0 \\
\vdots \\
f_m(x_1, \ldots, x_n) = 0
\end{cases}$$

1. 计算理想 $I = \langle f_1, \ldots, f_m \rangle$ 的 Gröbner 基底 $G$
2. 选择适当的单项式序（如字典序）得到消元形式
3. 从 $G$ 的第一个非零多项式（仅含少量变量）开始求解
4. 逐步回代求解其余变量

### 6.2 消元理论 (Elimination Theory)

**定理**：设 $I \subset k[x_1, \ldots, x_n]$ 是多项式理想，$G$ 是按字典序计算的 Gröbner 基底。则：
$$G \cap k[x_1, \ldots, x_k]$$
是消元理想 $I \cap k[x_1, \ldots, x_k]$ 的 Gröbner 基底。

`EliminationIdeal` 类 (`groebner_basis.py:280-290`) 实现了消元理想计算：
```python
class EliminationIdeal:
    """Elimination ideal for eliminating variables."""

    def __init__(self, ideal: PolynomialIdeal, eliminate_vars: List[int]):
        self.ideal = ideal
        self.eliminate_vars = eliminate_vars

    def compute_groebner_basis(self, order: MonomialOrder) -> GroebnerBasis:
        """Compute Groebner basis in elimination order."""
        algo = BuchbergerAlgorithm(order)
        return algo.compute_basis(self.ideal.generators)
```

### 6.3 其他应用

- **代数几何**：研究代数簇的性质
- **机器人学**：运动规划与逆运动学
- **编码理论**：译码算法
- **定理机器证明**：自动几何定理证明

## 7. 模块结构

```
groebner_basis.py
├── MonomialOrder        # 单项式序（lex, grevlex, dlex）
├── Polynomial           # 多项式表示
├── PolynomialRing       # 多项式环 k[x_1, ..., x_n]
├── GroebnerBasis        # Gröbner 基底容器
├── BuchbergerAlgorithm  # Buchberger 算法实现
├── PolynomialIdeal      # 多项式理想
├── EliminationIdeal      # 消元理想
└── IdealOperations       # 理想运算（交、和、积、根）
```

## 8. 数学背景

### 8.1 Hilbert 基定理

每个多项式理想的 Gröbner 基底存在，这是 Hilbert 基定理的构造性证明。

### 8.2 Dickson's 引理

任何单项式理想的升链都终止，这是 Gröbner 基底算法终止性的基础。

### 8.3 参考文献

- Buchberger, B. (1965). An Algorithm for Finding the Basis Elements of the Residue Class Ring. In Proceedings of EUROCAM.
- Cox, D., Little, J., O'Shea, D. (1997). Ideals, Varieties, and Algorithms.