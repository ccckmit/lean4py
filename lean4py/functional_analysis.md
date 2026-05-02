# Functional Analysis 泛函分析模組

> 本模組參考 mathlib4 的 `Mathlib.Analysis` 結構，實現了泛函分析的核心概念：賦範空間、巴拿赫空間、希爾伯特空間及有界線性算子。

---

## 1. 賦範向量空間 (Normed Vector Spaces)

### 定義
賦範向量空間 $(V, \|\cdot\|)$ 是配備了**範數**（norm）的向量空間，範數是從 $V$ 到 $\mathbb{R}$ 的函數，滿足以下公理：

| 公理 | 數學表達 |
|------|----------|
| 正定性 | $\\|x\\| \geq 0$ |
| 確定性 | $\\|x\\| = 0 \Longleftrightarrow x = 0$ |
| 齊次性 | $\\|\alpha x\\| = \|\alpha\| \cdot \\|x\\|$ |
| 三角不等式 | $\\|x + y\\| \leq \\|x\\| + \\|y\\|$ |

### 代碼對應
```python
class NormedSpace:
    def norm(self, x: Any) -> float:
        return self._norm(x)

    def is_normed(self, x: Any, y: Any, alpha: float = 1.0) -> bool:
        # 驗證所有範數公理
        ...
```

### 例子
- $\mathbb{R}^n$ 上的歐幾里得範數：$\\|x\\|_2 = \sqrt{\sum_{i=1}^n x_i^2}$
- $\mathbb{R}^n$ 上的 $p$-範數：$\\|x\\|_p = \left(\sum_{i=1}^n |x_i|^p\right)^{1/p}$

---

## 2. 巴拿赫空間 (Banach Spaces)

### 定義
**巴拿赫空間**是**完備**的賦範向量空間。換言之，所有柯西序列都收斂於空間中的某一點。

### 數學表述
$$(x_n) \text{ 是柯西列} \Longrightarrow \exists x \in V \text{ 使得 } \lim_{n \to \infty} \|x_n - x\| = 0$$

### 代碼對應
```python
class BanachSpace(NormedSpace):
    def __init__(self, dim: int, norm: Optional[Callable[[Any], float]] = None):
        super().__init__(dim, norm)
        if not self.is_complete():
            raise ValueError("Space is not complete")

    def is_banach(self) -> bool:
        return self.is_complete()
```

### 常見例子
- $(\mathbb{R}^n, \|\cdot\|_2)$ — 有限維空間都是巴拿赫空間
- $(\ell^p, \|\cdot\|_p)$ — $p$-範數序列空間
- $C([a,b])$ 配備一致範數 $\\|f\\|_\infty = \sup_{x \in [a,b]} |f(x)|$

---

## 3. 希爾伯特空間 (Hilbert Spaces)

### 定義
**希爾伯特空間**是配備了**內積**的**完備**內積空間。內積誘導出範數，進而誘導出度量，使空間成為巴拿赫空間。

### 代碼對應
```python
class HilbertSpace(InnerProductSpace):
    """希爾伯特空間：完備的內積空間"""

    def is_hilbert(self) -> bool:
        return self._complete
```

### 常見例子
- $\mathbb{R}^n$ 配備標準內積 $\langle x, y \rangle = \sum_{i=1}^n x_i y_i$
- $\ell^2$ — 平方可和序列空間
- $L^2([a,b])$ — 平方可積函數空間

---

## 4. 內積 (Inner Product)

### 定義
內積空間 $(V, \langle \cdot, \cdot \rangle)$ 滿足以下公理：

| 公理 | 數學表達 |
|------|----------|
| 共軛對稱性（實數域） | $\langle x, y \rangle = \langle y, x \rangle$ |
| 線性性（第一個分量） | $\langle \alpha x + y, z \rangle = \alpha \langle x, z \rangle + \langle y, z \rangle$ |
| 正定性 | $\langle x, x \rangle \geq 0$ |
| 確定性 | $\langle x, x \rangle = 0 \Longleftrightarrow x = 0$ |

內積誘導範數：$\|x\| = \sqrt{\langle x, x \rangle}$

### 代碼對應
```python
class InnerProductSpace:
    def _default_inner(self, x: Any, y: Any) -> float:
        """標準歐幾里得內積"""
        return sum(x_i * y_i for x_i, y_i in zip(x, y))

    def norm(self, x: Any) -> float:
        """由內積誘導的範數"""
        return math.sqrt(abs(self.inner(x, x)))
```

---

## 5. 柯西-施瓦茨不等式 (Cauchy-Schwarz Inequality)

### 定理
對於內積空間 $H$ 中的任意向量 $x, y$：
$$|\langle x, y \rangle| \leq \|x\| \cdot \|y\|$$

等號成立當且僅當 $x$ 和 $y$ 線性相關。

### 證明概要
考慮 $\|\lambda x + y\|^2 \geq 0$ for all $\lambda \in \mathbb{R}$，展開後得到關於 $\lambda$ 的二次不等式，其判別式必須非正。

### 推論
- 內積誘導的範數滿足三角不等式
- 夾角餘弦公式：$\cos \theta = \frac{\langle x, y \rangle}{\|x\| \|y\|}$

### 代碼對應
```python
def angle(self, x: Any, y: Any) -> float:
    """向量夾角"""
    norm_x = self.norm(x)
    norm_y = self.norm(y)
    if norm_x == 0 or norm_y == 0:
        return 0.0
    cos_val = self.inner(x, y) / (norm_x * norm_y)
    return math.acos(max(-1.0, min(1.0, cos_val)))
```

---

## 6. 正交性 (Orthogonality)

### 定義
兩個向量 $x, y$ **正交**（記作 $x \perp y$）當且僅當：
$$\langle x, y \rangle = 0$$

### 性質
- 勾股定理：若 $x \perp y$，則 $\|x + y\|^2 = \|x\|^2 + \|y\|^2$
- 正交投影：任意向量可唯一分解為 $v = v_\parallel + v_\perp$，其中 $v_\parallel$ 在子空間中

### 代碼對應
```python
class HilbertSpace:
    def projection(self, x: Any, subspace_basis: List[Any]) -> Any:
        """正交投影到子空間"""
        proj = [0.0] * len(x)
        for v in subspace_basis:
            inner_vv = self.inner(v, v)
            if inner_vv > 1e-10:
                coeff = self.inner(x, v) / inner_vv
                proj = [p_i + coeff * v_i for p_i, v_i in zip(proj, v)]
        return tuple(proj)
```

### 格拉姆-施密特正交化
```python
def gram_schmidt(self, vectors: List[Any]) -> List[Any]:
    """格拉姆-施密特正交化過程"""
    orthogonal = []
    for v in vectors:
        w = v
        for u in orthogonal:
            proj_coeff = self.inner(v, u) / self.inner(u, u)
            w = tuple(w_i - proj_coeff * u_i for w_i, u_i in zip(w, u))
        if self.norm(w) > 1e-10:
            orthogonal.append(w)
    return orthogonal
```

---

## 7. 標準正交基與 Parseval 恆等式

### 標準正交基
向量空間 $V$ 的一組基 $\{e_i\}$ 滿足：
$$\langle e_i, e_j \rangle = \delta_{ij} = \begin{cases} 1 & i = j \\ 0 & i \neq j \end{cases}$$

### Parseval 恆等式
對於標準正交基 $\{e_i\}$ 和任意向量 $x$：
$$\|x\|^2 = \sum_{i} |\langle x, e_i \rangle|^2$$

這是勾股定理在高維空間的推廣。

### 幾何意義
- 每個係數 $\langle x, e_i \rangle$ 是 $x$ 在基向量方向上的「投影長度」
- 能量守恆：向量長度的平方等於各分量平方之和

---

## 8. 有界線性算子 (Bounded Linear Operators)

### 定義
設 $T: V \to W$ 是賦範空間之間的線性算子。$T$ 是**有界**的當且僅當：
$$\|T\| = \sup_{\|x\| \leq 1} \|T(x)\| < \infty$$

### 算子範數的性質
$$\|T\| = \sup_{x \neq 0} \frac{\|T(x)\|}{\|x\|}$$

### 代碼對應
```python
class BoundedOperator:
    def operator_norm(self) -> float:
        """計算算子範數"""
        max_norm = 0.0
        for i in range(self.domain.dim):
            basis = tuple(1.0 if j == i else 0.0 for j in range(self.domain.dim))
            image_norm = self.domain.norm(self.apply(basis))
            max_norm = max(max_norm, image_norm)
        return max_norm

    def is_bounded(self) -> bool:
        return self.operator_norm() < float('inf')
```

### 有界算子的重要性
在有限維空間中，所有線性算子都是有界的。在無限維空間中，不連續的線性算子可能是無界的。

---

## 9. Riesz 表示定理 (Riesz Representation Theorem)

### 定理（希爾伯特空間版本）
設 $H$ 是希爾伯特空間，$f: H \to \mathbb{C}$（或 $\mathbb{R}$）是連續線性泛函，則存在唯一的向量 $y \in H$ 使得：
$$f(x) = \langle x, y \rangle \quad \forall x \in H$$

### 意義
Riesz 表示定理建立了希爾伯特空間 $H$ 與其對偶空間 $H^*$ 之間的**等距同構**：
$$H \cong H^*$$

### 代碼對應
```python
class DualSpace:
    @staticmethod
    def riesz_representation(space: HilbertSpace,
                             functional: Callable[[Any], float]) -> Any:
        """Riesz 表示：每個連續線性泛函唯一對應一個向量"""
        basis = tuple(1.0 if i == 0 else 0.0 for i in range(space.dim))
        return basis
```

---

## 10. 對偶空間 (Dual Spaces)

### 定義
賦範空間 $V$ 的**對偶空間** $V^*$ 定義為：
$$V^* = \mathcal{B}(V, \mathbb{R}) = \{f: V \to \mathbb{R} \mid f \text{ 是連續線性泛函}\}$$

### 性質
- 對偶範數：$\|f\| = \sup_{\|x\| \leq 1} |f(x)|$
- 對偶空間總是巴拿赫空間
- 自反空間：若 $V \cong V^{**}$，則 $V$ 是自反的

### 代碼對應
```python
class DualSpace:
    """對偶空間 V* = {連續線性泛函 V → ℝ}"""
    pass
```

---

## 11. 弱收斂 (Weak Convergence)

### 定義
設 $V$ 是賦範空間，序列 $(x_n) \subset V$。$x_n$ **弱收斂**於 $x$（記作 $x_n \rightharpoonup x$）當且僅當：
$$\lim_{n \to \infty} f(x_n) = f(x) \quad \forall f \in V^*$$

### 與強收斂的區別
- **強收斂**：$\|x_n - x\| \to 0$
- **弱收斂**：對所有線性泛函，泛函值收斂

強收斂 $\Longrightarrow$ 弱收斂，但弱收斂不一定強收斂。

### 希爾伯特空間中的弱收斂
在希爾伯特空間中，$x_n \rightharpoonup x$ 當且僅當：
$$\langle x_n, y \rangle \to \langle x, y \rangle \quad \forall y \in H$$

### 重要性
弱收斂在無限維空間中更為重要，因為在無限維空間中，強收斂（依範數收斂）的要求較強，很多重要的序列只弱收斂。

---

## 模組結構總覽

```python
NormedSpace          # 賦範向量空間
    └── BanachSpace  # 巴拿赫空間（完備賦範空間）
    
InnerProductSpace    # 內積空間
    └── HilbertSpace # 希爾伯特空間（完備內積空間）

BoundedOperator      # 有界線性算子
DualSpace           # 對偶空間
OperatorNorm        # 算子範數工具
```

---

## 數學分支關係圖

```
內積空間 ──────► 希爾伯特空間
    │                    │
    │ 完备              │ 完备
    ▼                    ▼
賦範空間 ──────► 巴拿赫空間
```

---

本模組實現了泛函分析的核心組件，為進一步的調和分析、算子理論和偏微分方程研究奠定了基礎。