# Local Fields - 局部域

本模块实现有限扩展 $\mathbb{Q}_p$ 的局部域结构，模仿 mathlib4 的 `Mathlib.NumberTheory.LocalFields`。

## 1. 局部域：完备离散赋值域

**局部域**是域 $K$ 的一种分类，具有以下等价性质：

- $K$ 是完备的离散赋值域
- $K$ 是 $\mathbb{Q}_p$ 的有限扩张
- $K$ 是某个有限域上离散赋值域的完备化

### 基本性质

| 性质 | 描述 |
|------|------|
| 特征 | $\text{char}(K) = 0$（局部域的特征为 0） |
| 剩余域特征 | $\text{char}(\kappa) = p$（剩余域特征为 $p$） |
| 非阿基米德范数 | $K$ 上存在唯一的非阿基米德绝对值 |

```python
class LocalField:
    """局部域：ℚ_p 的有限扩张。"""
    def __init__(self, p: int, degree: int):
        self.p = p                          # 素数 p
        self.degree = degree                # 扩张次数 [K:ℚ_p]
```

---

## 2. 正规化赋值 $v: K^* \to \mathbb{Z}$

### 定义

离散赋值是满足以下条件的映射 $v: K^* \to \mathbb{Z}$：

1. **正定性**：$v(x) \geq 0$ 当且仅当 $x \in \mathcal{O}_K$
2. **可加性**：$v(xy) = v(x) + v(y)$
3. **精细性**：$v(x + y) \geq \min(v(x), v(y))$

### 标准化

对于 $\mathbb{Q}_p$ 的扩张，标准化赋值定义为：

$$v_K(x) = e \cdot v_{\mathbb{Q}_p}(x) = e \cdot v_p(x)$$

其中 $e = e(K/\mathbb{Q}_p)$ 是分歧指数。

---

## 3. 整数环 $\mathcal{O}_K = \{x \in K : v(x) \geq 0\}$

### 定义

局部域 $K$ 的**整数环**（或 valuation ring）为：

$$\mathcal{O}_K = \{x \in K : v(x) \geq 0\}$$

### 性质

- $\mathcal{O}_K$ 是局部环
- $\mathcal{O}_K$ 是主理想环
- 唯一的极大理想为 $\mathfrak{m}_K = \{x : v(x) > 0\}$

```python
class ValuationRing:
    """赋值环 O_K = {x ∈ K : v(x) ≥ 0}。"""
    @staticmethod
    def compute(field: LocalField) -> Dict[str, Any]:
        return {"ring": "O_K", "maximal_ideal": "πO_K"}
```

---

## 4. 极大理想与剩余域

### 极大理想

设 $\pi$ 是 **一致元**（uniformizer），即 $v(\pi) = 1$，则：

$$\mathfrak{m}_K = \pi \mathcal{O}_K$$

### 剩余域

$$k_K = \mathcal{O}_K / \mathfrak{m}_K \cong \mathbb{F}_{p^f}$$

其中 $f = f(K/\mathbb{Q}_p)$ 是惯性次数。

```python
class Uniformizer:
    """一致元 π：v(π) = 1。"""
    @staticmethod
    def find(field: LocalField) -> str:
        return "p"  # 在 Q_p 上，p 即为一致元

class InertiaDegree:
    """惯性次数 f = [k_K : k_{ℚ_p}]。"""
    @staticmethod
    def compute(field: LocalField) -> int:
        return field.inertia_degree
```

### 剩余域的性质

| 量 | 公式 |
|----|------|
| 分歧指数 | $e = v_K(p)$ |
| 惯性次数 | $f = [k_K : \mathbb{F}_p]$ |
| 扩张次数 | $n = ef$ |

---

## 5. 分歧扩张：非分歧、弱分歧、完全分歧

设 $K/\mathbb{Q}_p$ 是有限扩张。

### 5.1 非分歧扩张 (Unramified)

若 $e = 1$，则称 $K/\mathbb{Q}_p$ 为**非分歧扩张**。

**性质**：
- $K$ 可由一个原根生成
- Galois 群 $\text{Gal}(K/\mathbb{Q}_p) \cong \mathbb{Z}/f\mathbb{Z}$
- 由 Frobenius 自同构生成

### 5.2 弱分歧 (Ramified)

若 $e > 1$，则称 $K/\mathbb{Q}_p$ 为**分歧扩张**。

**性质**：
- $p$ 在 $\mathcal{O}_K$ 中的分解：$(p) = \mathfrak{p}^e$
- 分歧群 $G_i = \{g \in G : v_K(g(\pi) - \pi) \geq i + 1\}$

### 5.3 完全分歧 (Totally Ramified)

若 $e = n = [K:\mathbb{Q}_p]$，则称 $K/\mathbb{Q}_p$ 为**完全分歧扩张**。

```python
class RamificationIndex:
    """分歧指数 e = [v(K*) : v(ℚ_p*)]。"""
    @staticmethod
    def is_totally_ramified(field: LocalField) -> bool:
        return field.ramification_index == field.degree
```

---

## 6. Frobenius 自同构

在非分歧扩张 $K/\mathbb{Q}_p$ 中，**Frobenius 自同构**定义为：

$$\text{Frob}_K(x) \equiv x^p \pmod{\mathfrak{m}_K}, \quad \forall x \in \mathcal{O}_K$$

### 性质

- $\text{Frob}_K$ 生成 Galois 群 $\text{Gal}(K/\mathbb{Q}_p)$
- $\text{Frob}_K^n = \text{id}$，其中 $n = f$
- 提升的 Frobenius：$\tilde{\text{Frob}}(x) = x^p$

### Artin 映射与 Frobenius

$$\text{Frob}_{K/\mathbb{Q}_p} = \left(\frac{K/\mathbb{Q}_p}{\cdot}\right)^{-1}$$

---

## 7. 不同与判别式

### 7.1 差分 (Different)

设 $K/\mathbb{Q}_p$ 是有限扩张，其**差分**定义为：

$$\mathfrak{D}_{K/\mathbb{Q}_p} = \{x \in K : \text{Tr}_{K/\mathbb{Q}_p}(xy) \in \mathcal{O}_{\mathbb{Q}_p}, \forall y \in \mathcal{O}_K\}$$

### 7.2 判别式 (Discriminant)

$$\text{disc}(K/\mathbb{Q}_p) = N_{K/\mathbb{Q}_p}(\mathfrak{D}_{K/\mathbb{Q}_p})$$

### 性质

- $v_{\mathbb{Q}_p}(\text{disc}(K/\mathbb{Q}_p)) = \sum_{i=1}^{\infty} (|G_i| - 1)$
- 局部域的判别式与整体判别式通过分解公式关联

---

## 8. 局部 Artin 映射与局部类域论

### 8.1 局部 Artin 映射

设 $K/\mathbb{Q}_p$ 是有限 Galois 扩张，**局部 Artin 映射**为：

$$\text{Art}_K : \mathbb{A}_K^\times \to \text{Gal}(K^{\text{ab}}/K)$$

满足：
- $\text{Art}_K(\pi) = \text{Frob}_K^{-1}$
- $\text{Art}_K(u) = \text{id}$（$u \in \mathcal{O}_K^\times$ 为单位）

### 8.2 局部类域论

局部类域论建立了 $K$ 的 Abel 扩张与 $K^\times$ 的商群之间的对应：

$$K^\times / (K^\times)^n \cong \text{Gal}(K^{\text{ab}}/K)$$

### 8.3 互反律

对于 $x \in K^\times$：

$$\text{Art}_K(x) = \prod_{v} \text{Art}_{K_v}(x_v)$$

### 分歧与 Artin 映射

$$\text{Art}_K(\pi_K) = \text{Frob}_K^{-1}$$

其中 $\pi_K$ 是一致元。

---

## 模块结构

```python
# 核心类
LocalField(p, degree)           # 局部域 K = ℚ_p 的 n 次扩张
ValuationRing                   # 赋值环 O_K
Uniformizer                     # 一致元 π
RamificationIndex               # 分歧指数 e
InertiaDegree                   # 惯性次数 f
```

## 与 mathlib4 的对应

| lean4py | mathlib4 |
|---------|----------|
| `LocalField` | `LocalField` |
| `ValuationRing` | `ValuationRing` |
| `Uniformizer` | `Uniformizer` |
| `RamificationIndex` | `RamificationIndex` |
| `InertiaDegree` | `InertiaDegree` |

## 参考文献

1. Neukirch, J. *Algebraic Number Theory*
2. Serre, J.-P. *Local Fields*
3. Washington, L. *Introduction to Cyclotomic Fields*
4. mathlib4: `Mathlib.NumberTheory.LocalFields`