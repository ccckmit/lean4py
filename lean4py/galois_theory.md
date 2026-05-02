# Galois Theory 文檔

## 概述

Galois 理論是抽象代數的核心分支，由法國數學家 Évariste Galois 創立。該模組 imitates mathlib4 的 `Mathlib.FieldTheory.Galois`，提供域擴張、Galois 群與可解性等基本概念。

---

## 1. 域擴張 (Field Extensions)

### 定義

若域 $K$ 包含域 $F$ 為子域，則稱 $K/F$ 為**域擴張**，記作 $K/F$ 或 $K \supseteq F$。

在 `FieldExtension` 類別中：
```python
class FieldExtension:
    def __init__(self, base_field: str, extension_field: str, degree: int = 1):
        self.base = base_field      # 基域 F
        self.extension = extension_field  # 擴張域 K
        self.degree = degree        # 擴張次數 [K:F]
```

---

## 2. 擴張次數 (Degree of Extension) $[K:F]$

### 定義

$[K:F]$ 是 $K$ 作為 $F$ 上的向量空間的維數。當 $[K:F] < \infty$ 時，稱為**有限擴張**。

### 性質

- $[K:F] = 1 \iff K = F$
- 若 $F \subseteq E \subseteq K$，則 $[K:F] = [K:E] \cdot [E:F]$（次數積公式）
- 若 $[K:F] = n$，則 $K$ 中每個元素可由 $n$ 個基元素生成

---

## 3. 代數元與超越元 (Algebraic vs Transcendental Elements)

### 代數元

若 $\alpha \in K$ 是 $F$ 擴張中的元素，若存在非零多項式 $f(x) \in F[x]$ 使得 $f(\alpha) = 0$，則稱 $\alpha$ 為 $F$ 上的**代數元**。

### 超越元

若 $\alpha$ 不是代數元，則稱為**超越元**（如 $\pi, e$ 在 $\mathbb{Q}$ 上）。

### 純超越擴張

若擴張 $K/F$ 中每個元素都是代數元，則為**代數擴張**；否則為**純超越擴張**。

---

## 4. 最小多項式 (Minimal Polynomial)

### 定義

設 $\alpha$ 為 $F$ 上的代數元，則存在唯一的首一不可約多項式 $m_\alpha(x) \in F[x]$，使得：
- $m_\alpha(\alpha) = 0$
- 若 $f(\alpha) = 0$ 且 $f$ 首一，則 $m_\alpha \mid f$

### 性質

- $\deg(m_\alpha) = [F(\alpha):F]$
- $F(\alpha) \cong F[x]/(m_\alpha)$

---

## 5. 分裂域 (Splitting Fields)

### 定義

設 $f(x) \in F[x]$ 為多項式，$K$ 為包含 $F$ 的域。若：
1. $f$ 在 $K$ 中可完全分解為線性因子：$f(x) = a \prod_{i=1}^{n}(x - \alpha_i)$
2. $K = F(\alpha_1, \alpha_2, \ldots, \alpha_n)$

則稱 $K$ 為 $f$ 在 $F$ 上的**分裂域**。

### 性質

- 分裂域是包含所有根的最小域
- 分裂域在同構意義下唯一
- $[K:F] \leq n!$，其中 $n = \deg(f)$

---

## 6. Galois 群 $\text{Gal}(K/F)$

### 定義

$\text{Gal}(K/F)$ 為所有保持 $F$ 不動的 $K$ 自同構的集合：

$$\text{Gal}(K/F) = \{\sigma \in \text{Aut}(K) \mid \sigma|_F = \text{id}_F\}$$

### 性質

- $|\text{Gal}(K/F)| = [K:F]$（有限 Galois 擴張）
- 若 $K/F$ 為 Galois 擴張，則 $\text{Gal}(K/F)$ 為有限群

在 `GaloisGroup` 類別中：
```python
class GaloisGroup:
    @staticmethod
    def compute(extension: FieldExtension) -> Dict[str, Any]:
        return {"group": "trivial", "order": 1, "generators": []}

    @staticmethod
    def is_abelian(extension: FieldExtension) -> bool:
        return True
```

---

## 7. Galois 基本定理 (Fundamental Theorem of Galois Theory)

### 定理陳述

設 $K/F$ 為有限 Galois 擴張，$G = \text{Gal}(K/F)$。則存在如下**雙射對應**：

$$\{\text{中間域 } E \mid F \subseteq E \subseteq K\} \leftrightarrow \{\text{G 的子群 } H \leq G\}$$

對應關係為：
- $E \mapsto \text{Gal}(K/E)$
- $H \mapsto K^H = \{x \in K \mid \forall \sigma \in H: \sigma(x) = x\}$

### 性質

| 條件 | 對應 |
|------|------|
| $E/F$ 為正規擴張 | $\text{Gal}(K/E) \trianglelefteq G$ |
| $E/F$ 為 Galois 擴張 | $\text{Gal}(K/E)$ 為正規子群 |
| $[E:F] = [G:\text{Gal}(K/E)]$ | |
| $|\text{Gal}(K/E)| = [K:E]$ | |

在 `FundamentalTheorem` 類別中：
```python
class FundamentalTheorem:
    @staticmethod
    def intermediate_fields(extension: FieldExtension) -> List[str]:
        return [extension.base, extension.extension]

    @staticmethod
    def correspondence(extension: FieldExtension) -> Dict[str, Any]:
        return {"fields": [], "subgroups": []}
```

---

## 8. 根式可解性 (Solvability by Radicals)

### 定義

多項式 $f(x)$ 若其根可以通過有限次加、減、乘、除、開方（即根式）表示，則稱 $f$ 為**根式可解**。

### Galois 理論判準

**定理**：設 $f \in F[x]$ 為多項式，$K$ 為其分裂域，$G = \text{Gal}(K/F)$。則：

$$f \text{ 根式可解} \iff G \text{ 為可解群}$$

### 可解群

群 $G$ 為**可解群**若存在子群鏈：

$$\{e\} = G_0 \trianglelefteq G_1 \trianglelefteq \cdots \trianglelefteq G_n = G$$

使得每個商群 $G_{i+1}/G_i$ 為阿貝爾群。

### 歷史意義

Galois 證明：五次及以上一般多項式的 Galois 群為 $S_n$，而 $S_n$ (n ≥ 5) 不可解，故一般五次方程無根式解。

在 `SolvabilityByRadicals` 類別中：
```python
class SolvabilityByRadicals:
    @staticmethod
    def is_solvable(polynomial_degree: int) -> bool:
        return polynomial_degree <= 4
```

---

## 9. 直尺圓規作圖 (Straightedge and Compass Constructibility)

### 問題背景

古希臘三大作圖難題：
1. 圓化方（化圓為方）
2. 三等分任意角
3. 倍立方（立方倍積）

### Galois 理論解釋

平面上可用直尺圓規構造的點對應於**次數為 2 的冪**的域擴張。

**定理**：點 $\alpha$ 可用直尺圓規從給定點構造 $\iff$ 在某個域擴張鏈中：

$$[\mathbb{Q}(\alpha):\mathbb{Q}] = 2^k \quad (k \in \mathbb{N})$$

### 可構造性條件

- 可構造群的階數為 $2^k$（2-群）
- 擴張次數每次至多翻倍
- 故若 $[K:F] = 2^k$ 且為 Galois，則 Galois 群為 2-群

### 應用

| 問題 | Galois 群/擴張 | 結論 |
|------|----------------|------|
| 三等分角 | 非 2-群擴張 | 一般不可構造 |
| 倍立方 | $[\mathbb{Q}(\sqrt[3]{2}):\mathbb{Q}] = 3$ | 不可構造 |
| 化圓為方 | $\pi$ 超越 | 不可構造 |

---

## 10. 割圓擴張與阿貝爾擴張 (Cyclotomic and Abelian Extensions)

### 割圓多項式

$n$ 次**割圓多項式**為：

$$\Phi_n(x) = \prod_{\substack{1 \leq k \leq n \\ \gcd(k,n)=1}} \left(x - e^{2\pi i k/n}\right)$$

其中 $e^{2\pi i k/n}$ 為 $n$ 次本原單位根。

### 割圓域

$\mathbb{Q}(\zeta_n)$，其中 $\zeta_n = e^{2\pi i/n}$，稱為第 $n$ 個割圓域。

### 性質

- $[\mathbb{Q}(\zeta_n):\mathbb{Q}] = \phi(n)$（歐拉函數）
- $\text{Gal}(\mathbb{Q}(\zeta_n)/\mathbb{Q}) \cong (\mathbb{Z}/n\mathbb{Z})^\times$
- 割圓擴張為阿貝爾擴張（Galois 群為阿貝爾群）

### Kronecker-Weber 定理

有理數域 $\mathbb{Q}$ 的有限阿貝爾擴張必包含在某個割圓域中：

$$E/\mathbb{Q} \text{ 為阿貝爾擴張} \iff E \subseteq \mathbb{Q}(\zeta_n) \text{ 對某個 } n$$

### 阿貝爾擴張

若 $K/F$ 為 Galois 擴張且 $\text{Gal}(K/F)$ 為阿貝爾群，則稱 $K/F$ 為**阿貝爾擴張**。

在 `SeparableExtension`、`NormalExtension`、`GaloisExtension` 類別中：
```python
class SeparableExtension:
    @staticmethod
    def is_separable(extension: FieldExtension) -> bool:
        return True

class NormalExtension:
    @staticmethod
    def is_normal(extension: FieldExtension) -> bool:
        return True

class GaloisExtension:
    @staticmethod
    def is_galois(extension: FieldExtension) -> bool:
        sep = SeparableExtension.is_separable(extension)
        norm = NormalExtension.is_normal(extension)
        return sep and norm
```

---

## 類別關係圖

```
FieldExtension
    ├── GaloisGroup (compute, is_abelian)
    ├── SeparableExtension (is_separable)
    ├── NormalExtension (is_normal)
    ├── GaloisExtension (is_galois) = separable + normal
    ├── FundamentalTheorem (intermediate_fields, correspondence)
    └── SolvabilityByRadicals (is_solvable)
```

---

## 數學意義

Galois 理論以其深刻的**對應原理**著稱，將域擴張的代數結構與群論結構完美結合：

1. **域的性質** ↔ **群的不變量**
2. **正規擴張** ↔ **正規子群**
3. **可解群** ↔ **根式可解**

這使得許多古典代數問題（如五大作圖難題）得以徹底解決，並為現代代數數論、類域論等領域奠定基礎。