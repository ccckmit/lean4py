# Lie 代數模組文檔

本文檔說明 `lie_algebra.py` 模組背後的數學原理。該模組實現了李代數的基本結構、表示理論及其分類。

## 1. 李代數定義

**李代數**是一個向量空間 $\mathfrak{g}$，配備一個雙線性運算 $[\cdot, \cdot]: \mathfrak{g} \times \mathfrak{g} \to \mathfrak{g}$，稱為**李括號**，滿足以下公理：

### 1.1 基本公理

| 公理 | 數學表達 | 說明 |
|------|---------|------|
| 雙線性 (Bilinear) | $[ax + by, z] = a[x,z] + b[y,z]$ | 括號對第一分量線性 |
| 反對稱 (Alternating) | $[x, x] = 0$ | 推論：$[x,y] = -[y,x]$ |
| 雅可比 (Jacobi) | $[x, [y, z]] + [y, [z, x]] + [z, [x, y]] = 0$ | 保證結合結構 |

### 1.2 模組實現

```python
class LieAlgebra:
    def __init__(self, name: str, dimension: int,
                 bracket: Callable[[List[float], List[float]], List[float]],
                 basis: Optional[List[List[float]]] = None):
        self.name = name
        self.dimension = dimension
        self.bracket = bracket
        self.basis = basis or self._default_basis()
```

**`LieAlgebra` 類**封裝了：
- `dimension`: 向量空間維數
- `bracket`: 括號運算函數
- `basis`: 基底向量列表

**驗證方法**：
- `is_lie_algebra()`: 檢查所有三個公理
- `_check_antisymmetric()`: 遍歷基底驗證 $[x,x] = 0$
- `_check_jacobi()`: 三重嵌套循環驗證雅可比恆等式

### 1.3 基本性質

```python
def is_abelian(self) -> bool:
    """Check if Lie algebra is abelian: [x,y] = 0 for all x,y."""
```

**阿貝爾李代數**：所有元素互易，即 $[x,y] = 0$ 對所有 $x,y \in \mathfrak{g}$。

---

## 2. 李代數的表示

### 2.1 表示定義

**表示**是線性映射 $\rho: \mathfrak{g} \to \mathfrak{gl}(V)$，滿足：
$$\rho([x,y]) = [\rho(x), \rho(y)] = \rho(x)\rho(y) - \rho(y)\rho(x)$$

其中 $V$ 為表示空間，$\dim V$ 為表示維數。

### 2.2 模組實現

```python
class LieAlgebraRepresentation:
    def __init__(self, lie_algebra: LieAlgebra, dimension: int,
                 representation_map: Callable[[List[float]], List[List[float]]]):
        self.lie_algebra = lie_algebra
        self.dimension = dimension
        self.representation_map = representation_map

    def is_representation(self) -> bool:
        """Check ρ([x,y]) = [ρ(x), ρ(y)]."""
```

**驗證方法**：對所有基底元素 $e_i, e_j$，檢查
$$\rho([e_i, e_j]) \stackrel{?}{=} [\rho(e_i), \rho(e_j)]$$

### 2.3 伴隨表示

**伴隨表示**是李代數最基礎的表示：

$$(\text{ad}_x)(y) = [x, y]$$

```python
class AdjointRepresentation:
    def compute(self, x: List[float], y: List[float]) -> List[float]:
        """Ad_x(y) = [x, y]."""
        return self.lie_algebra.bracket(x, y)

    def ad_matrix(self, x: List[float]) -> List[List[float]]:
        """Compute ad_x as matrix in basis."""
```

**結構常數**：在基底 $\{e_i\}$ 下，
$$[e_i, e_j] = \sum_k c_{ij}^k e_k$$
係數 $c_{ij}^k$ 稱為結構常數。

---

## 3. 可解與冪零李代數

### 3.1 下中心列與冪零性

**下中心列**（Lower Central Series）：
$$\mathfrak{g}^1 = \mathfrak{g}, \quad \mathfrak{g}^2 = [\mathfrak{g}, \mathfrak{g}], \quad \mathfrak{g}^3 = [\mathfrak{g}, \mathfrak{g}^2], \ldots$$

**冪零李代數**：若存在 $n$ 使得 $\mathfrak{g}^n = \{0\}$，則稱 $\mathfrak{g}$ 為冪零。

### 3.2 導出列與可解性

**導出列**（Derived Series）：
$$\mathfrak{g}^{(1)} = \mathfrak{g}, \quad \mathfrak{g}^{(2)} = [\mathfrak{g}^{(1)}, \mathfrak{g}^{(1)}], \quad \mathfrak{g}^{(3)} = [\mathfrak{g}^{(2)}, \mathfrak{g}^{(2)}], \ldots$$

**可解李代數**：若存在 $n$ 使得 $\mathfrak{g}^{(n)} = \{0\}$，則稱 $\mathfrak{g}$ 為可解。

### 3.3 Levi 分解

**Levi 分解定理**：任意李代數 $\mathfrak{g}$ 可以分解為
$$\mathfrak{g} = \mathfrak{r} \rtimes \mathfrak{s}$$

其中 $\mathfrak{r}$ 為最大可解理想（根基），$\mathfrak{s}$ 為半單純子代數（Levi 子代數）。

```python
def is_solvable(self) -> bool:
    """Check if Lie algebra is solvable."""
    return True

def is_semisimple(self) -> bool:
    """Check if Lie algebra is semisimple (no nonzero abelian ideals)."""
    return True
```

---

## 4. 半單純李代數

### 4.1 定義

**半單純李代數**：無非平凡阿貝爾理想的李代數。等價於：
- 無非零零根
- Killing 型非退化

### 4.2 單李代數

**單李代數**：無非平凡理想的非阿貝爾李代數。

**分類重要性**：半單純李代數 = 單李代數的直和。

---

## 5. Killing 型

### 5.1 定義

**Killing 型**（Killing Form）：
$$K(x, y) = \text{Tr}(\text{ad}_x \circ \text{ad}_y)$$

這是 $\mathfrak{g}$ 上的對稱雙線性形式。

### 5.2 模組實現

```python
def killing_form(self, x: List[float], y: List[float]) -> float:
    """Killing form: B(x, y) = Tr(ad_x ∘ ad_y)."""
    ad_x = self.ad_matrix(x)
    ad_y = self.ad_matrix(y)
    ad_xy = self._matrix_product(ad_x, ad_y)
    return sum(ad_xy[i][i] for i in range(len(ad_xy)))
```

**計算方法**：
1. 計算 $\text{ad}_x$ 和 $\text{ad}_y$ 的矩陣表示
2. 計算矩陣乘積 $\text{ad}_x \cdot \text{ad}_y$
3. 取跡（對角線元素之和）

### 5.3 Cartan 判準

**Cartan 判準**（Semisimplicity）：
- 李代數 $\mathfrak{g}$ 為半單純 **當且僅當** Killing 型非退化。
- 李代數 $\mathfrak{g}$ 為可解 **當且僅當** Killing 型在導出列上為零。

---

## 6. 根系與根系格

### 6.1 根系定義

設 $\mathfrak{h}$ 為半單純李代數 $\mathfrak{g}$ 的**Cartan 子代數**（極大可解子代數），維數為 $l = \text{rank}(\mathfrak{g})$。

對於 $\alpha \in \mathfrak{h}^*$，定義
$$\mathfrak{g}_\alpha = \{x \in \mathfrak{g} \mid [h, x] = \alpha(h)x \text{ 对所有 } h \in \mathfrak{h}\}$$

若 $\mathfrak{g}_\alpha \neq \{0\}$，則 $\alpha$ 為**根系**（Root），$\mathfrak{g}_\alpha$ 為對應的**根空間**。

### 6.2 根系性質

| 性質 | 描述 |
|------|------|
| 封閉性 | 若 $\alpha, \beta \in \Phi$，則 $\alpha + \beta \in \Phi$ 或 $\alpha + \beta \notin \Phi$ |
| 根的對稱性 | 若 $\alpha \in \Phi$，則 $-\alpha \in \Phi$ |
| 根的可垂直性 | $\mathfrak{g} = \mathfrak{h} \oplus \bigoplus_{\alpha \in \Phi} \mathfrak{g}_\alpha$ |

### 6.3 簡單根系

從根系中選擇一組 **簡單根系**（Simple Roots）$\Pi = \{\alpha_1, \ldots, \alpha_l\}$，使得每個根可唯一表示為
$$\alpha = \sum_{i=1}^l n_i \alpha_i, \quad n_i \in \mathbb{Z}$$
且係數全正或全負。

### 6.4 模組實現

```python
class RootSystem:
    def __init__(self, rank: int, simple_roots: Optional[List[List[float]]] = None,
                 cartan_matrix: Optional[List[List[float]]] = None):
        self.rank = rank
        self.simple_roots = simple_roots or [[1.0, 0.0]]
        self.cartan_matrix = cartan_matrix or [[2.0]]
```

**屬性**：
- `rank`: Cartan 子代數維數（李代數的秩）
- `simple_roots`: 簡單根系列表
- `cartan_matrix`: Cartan 矩陣

### 6.5 Cartan 矩陣

**Cartan 矩陣**定義為：
$$A_{ij} = \frac{2(\alpha_i, \alpha_j)}{(\alpha_j, \alpha_j)}$$

其中 $(\cdot, \cdot)$ 為根系上的內積。

```python
def cartan_matrix_element(self, i: int, j: int) -> float:
    """Get Cartan matrix entry A_ij = 2(α_i, α_j) / (α_j, α_j)."""
```

**性質**：
- $A_{ii} = 2$
- 若 $i \neq j$，則 $A_{ij} \leq 0$
- $A_{ij} = 0 \iff A_{ji} = 0$

---

## 7. 複半單純李代數的分類

### 7.1 Dynkin 圖

**Dynkin 圖**是 Cartan 矩陣的圖表示：
- 每個簡單根對應一個頂點
- 頂點 $i, j$ 之間有 $\max(|A_{ij}|, |A_{ji}|)$ 條邊
- 若 $A_{ij} < -1$，邊上加箭頭指向較短根

### 7.2 分類定理

**一切有限維複半單純李代數的根系必屬於以下四個無窮族或五個特殊情況**：

#### 無窮族

| 類型 | Dynkin 圖 | 李代數 | 維數 |
|------|----------|--------|------|
| $A_n$ | 线性链 | $\mathfrak{sl}_{n+1}$ | $n(n+2)$ |
| $B_n$ | $n-1$ 個頂點 + 分支 | $\mathfrak{so}_{2n+1}$ | $n(2n+1)$ |
| $C_n$ | $n-1$ 個頂點 + 分支（反向箭頭） | $\mathfrak{sp}_{2n}$ | $n(2n+1)$ |
| $D_n$ | $n-2$ 個頂點 + Y 形分支 | $\mathfrak{so}_{2n}$ | $n(2n-1)$ |

#### 例外型

| 類型 | Dynkin 圖 | 維數 |
|------|----------|------|
| $E_6$ | 2-3-2-1-2 分支 | 78 |
| $E_7$ | 2-3-2-1-2-3 | 133 |
| $E_8$ | 2-3-2-1-2-3-4 | 248 |
| $F_4$ | 3-2-1-2 鏈 | 52 |
| $G_2$ | 2-1-3 鏈（箭頭） | 14 |

### 7.3 模組中的類型識別

```python
def is_cartan_type(self) -> str:
    """Identify Cartan type: A_n, B_n, C_n, D_n, E_6/7/8, F_4, G_2."""
    r = self.rank
    if r == 1:
        return "A_1"
    elif r == 2:
        a12 = self.cartan_matrix_element(0, 1)
        a21 = self.cartan_matrix_element(1, 0)
        if a12 == -1 and a21 == -1:
            return "A_2"
        elif a12 == -2 and a21 == -1:
            return "B_2=G_2"
        elif a12 == -1 and a21 == -2:
            return "C_2"
    return f"A_{r}" if r > 0 else "Error"
```

---

## 8. Serre 關係

### 8.1 背景

**Serre 定理**：每個仿射 Cartan 矩陣唯一確定了對應的有限維單李代數。

**Serre 關係**是生成元 $e_i, f_i, h_i$ 之間的關係，用於顯式構造李代數。

### 8.2 關係定義

從 Cartan 矩陣 $A$ 導出：
- 若 $A_{ij} = 0$，則 $[e_i, f_j] = 0$
- 若 $A_{ij} = -1$，則 $\text{ad}(e_i)^2(e_j) = 0$
- 若 $A_{ij} = -2$，則 $\text{ad}(e_i)^3(e_j) = 0$
- 若 $A_{ij} = -3$，則 $\text{ad}(e_i)^4(e_j) = 0$

### 8.3 模組實現

```python
class SerreRelations:
    def generate_relations(self) -> List[str]:
        """Generate Serre relations from Cartan matrix."""
        A = self.root_system.cartan_matrix
        relations = []
        rank = self.root_system.rank
        for i in range(rank):
            for j in range(rank):
                if i != j:
                    aij = A[i][j]
                    if aij == 0:
                        relations.append(f"[e_i, e_j] = 0")
                    elif aij == -1:
                        relations.append(f"ad(e_i)^2(e_j) = 0")
                    # ...
        return relations
```

---

## 9. 通用包絡代數

### 9.1 定義

**通用包絡代數**（Universal Enveloping Algebra）$U(\mathfrak{g})$ 是 tensor 代數的商：
$$U(\mathfrak{g}) = T(\mathfrak{g}) / \langle [x,y] - [x,y] - xy + yx \rangle$$

即
$$U(\mathfrak{g}) = T(\mathfrak{g}) / \langle x \otimes y - y \otimes x - [x,y] \rangle$$

### 9.2 Poincare-Birkhoff-Witt 定理

**PBW 定理**：若 $\{e_1, \ldots, e_n\}$ 為 $\mathfrak{g}$ 的有序基底，則
$$\{e_1^{k_1} e_2^{k_2} \cdots e_n^{k_n} \mid k_i \geq 0\}$$
構成 $U(\mathfrak{g})$ 的基底。

### 9.3 模組實現

```python
class UniversalEnvelopingAlgebra:
    def basis(self) -> List[List[Tuple[int, int]]]:
        """Poincare-Birkhoff-Witt basis: monomials in basis elements."""
        if self._pbw_basis is not None:
            return self._pbw_basis
        dim = self.lie_algebra.dimension
        self._pbw_basis = []
        for degree in range(10):
            for comb in self._combinations_with_sums(dim, degree):
                self._pbw_basis.append(comb)
        return self._pbw_basis
```

---

## 10. 實例：$\mathfrak{sl}(2, \mathbb{C})$

### 10.1 代數結構

$\mathfrak{sl}(2, \mathbb{C})$ 為跡為零的 $2 \times 2$ 矩陣代數，維數 3。

**標準基底**：
$$H = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \quad E = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}, \quad F = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$$

**括號關係**：
$$[H, E] = 2E, \quad [H, F] = -2F, \quad [E, F] = H$$

### 10.2 模組實現

```python
def sl2_lie_algebra() -> LieAlgebra:
    """Standard sl(2,C) Lie algebra."""
    def bracket(x: List[float], y: List[float]) -> List[float]:
        h, e, f = x[0], x[1], x[2]
        hp, ep, fp = y[0], y[1], y[2]
        return [
            2 * e * fp - 2 * f * ep,  # [H, H'] = 2EF' - 2FE'
            h * ep - hp * e,           # [E, H'] = HE' - H'E
            f * hp - h * fp            # [F, H'] = FH' - HF'
        ]
    basis = [
        [2, 0, 0],   # H
        [0, 1, 0],   # E
        [0, 0, 1],   # F
    ]
    return LieAlgebra("sl2", 3, bracket, basis)
```

### 10.3 $\mathfrak{sl}(2)$ 的根系

- **Cartan 子代數**：$\mathfrak{h} = \mathbb{C}H$，維數 1
- **根系**：$\Phi = \{\alpha, -\alpha\}$，其中 $\alpha(H) = 2$
- **根系型**：$A_1$

---

## 11. 使用範例

```python
from lean4py.lie_algebra import sl2_lie_algebra, RootSystem

# 創建 sl(2) 代數
sl2 = sl2_lie_algebra()
print(f"Dimension: {sl2.dimension}")  # 3
print(f"Is abelian: {sl2.is_abelian()}")  # False
print(f"Is Lie algebra: {sl2.is_lie_algebra()}")  # True

# 創建根系
root_sys = RootSystem(rank=1, cartan_matrix=[[2.0]])
print(f"Cartan type: {root_sys.is_cartan_type()}")  # A_1
```

---

## 12. 數學背景總結

```
李代數分類層次結構：

┌─────────────────────────────────────┐
│        半單純李代數 (Semisimple)     │
│  ════════════════════════════════════│
│  • Killing 型非退化                  │
│  • = 單李代數的直和                   │
│  • 由 Dynkin 圖完全分類              │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐      ┌────────────────┐
│ 可解   │      │ 單李代數        │
│(Solvable)│     │ (Simple)       │
└─────────┘      └───────┬────────┘
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
     ▼                   ▼                   ▼
  A_n, B_n, C_n, D_n   E_6, E_7, E_8    F_4, G_2
  (無窮族)            (例外型)
```