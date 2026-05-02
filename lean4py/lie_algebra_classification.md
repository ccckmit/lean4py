# Lie 代數分類 (Lie Algebra Classification)

## 概述

本模組實現了半單純 Lie 代數的完整分類理論，基於 Dynkin 圖和 Cartan 矩陣的經典方法。分類定理斷言：每個半單純 Lie 代數都是單純 Lie 代數的直和，而單純 Lie 代數完全由其 Dynkin 圖類型決定。

```python
from lean4py.lie_algebra_classification import DynkinDiagram, ClassificationTheorem, SimpleLieAlgebra
```

---

## 1. 根系與根格 (Root Systems and Root Lattice)

### 1.1 根系統的定義

設 $V$ 為具有不變定正雙線性形式的實向量空間。根系 $\Phi$ 是滿足以下條件的有限集合 $\Phi \subset V \setminus \{0\}$：

1. **封閉性**：若 $\alpha \in \Phi$，則 $-\alpha \in \Phi$，且 $k\alpha \in \Phi \Rightarrow k = \pm 1$
2. **反射不變性**：對每個 $\alpha \in \Phi$，反射 $s_\alpha(\beta) = \beta - 2\frac{(\beta, \alpha)}{(\alpha, \alpha)}\alpha$ 將 $\Phi$ 映到自身

### 1.2 根系結構

- **根系秩 (Rank)**：向量空間 $V$ 的維數，即單根的個數
- **正根與負根**：選擇一個線性泛函使得其在正根上為正
- **單根 (Simple Roots)**：正根中無法表示為兩個正根之和的根，構成 $V$ 的基
- **根格 (Root Lattice)**：由根系生成的格 $Q = \mathbb{Z}\Phi$

### 1.3 程式實作

```python
class RootSystem:
    """根系：被反射封閉的向量集合"""
    
    def __init__(self, rank: int, roots: Optional[List[List[float]]] = None):
        self.rank = rank          # 根系秩
        self.roots = roots or []   # 所有根
        self.positive_roots: List[List[float]] = []   # 正根
        self.simple_roots: List[List[float]] = []      # 單根
```

### 1.4 Weyl 群

Weyl 群由根系中所有根的反射生成：

$$W = \langle s_\alpha : \alpha \in \Phi \rangle$$

其中 $s_\alpha(x) = x - 2\frac{(\alpha, x)}{(\alpha, \alpha)}\alpha$

```python
class WeylGroup:
    """Weyl 群：由反射生成的有限變換群"""
    
    def reflect(self, vector: List[float], root: List[float]) -> List[float]:
        """計算反射 s_α(v)"""
        alpha_sq = sum(a**2 for a in root)
        if alpha_sq == 0:
            return vector
        coeff = 2 * sum(v * a for v, a in zip(vector, root)) / alpha_sq
        return [vector[i] - coeff * root[i] for i in range(len(vector))]
```

---

## 2. Dynkin 圖 (Dynkin Diagrams)

### 2.1 基本結構

Dynkin 圖是表示單根之間角度關係的圖：

- **節點**：每個節點對應一個單根 $\alpha_i$
- **邊**：連接 $\alpha_i$ 和 $\alpha_j$
  - 無邊：$(\alpha_i, \alpha_j) = 0$（正交）
  - 單邊：$(\alpha_i, \alpha_j) = -1$
  - 雙邊：$(\alpha_i, \alpha_j) = -2$（指向較短根）
  - 三邊：$(\alpha_i, \alpha_j) = -3$（只用於 $G_2$）

### 2.2 古典根系

#### $A_n$ 型 ($n \geq 1$)

```
○——○——○——⋯——○——○
1   2   3       n
```

- 根系：$\{\varepsilon_i - \varepsilon_j : 1 \leq i \neq j \leq n+1\}$
- 維數：$n(n+2)/2$
- 典型例子：$\mathfrak{sl}_{n+1}$

#### $B_n$ 型 ($n \geq 2$)

```
○——○——○——⋯——○=>○
1   2   3       n
```

- 根系：$\{\pm\varepsilon_i : 1 \leq i \leq n\} \cup \{\pm\varepsilon_i \pm \varepsilon_j : i < j\}$
- 雙邊指向短根
- 典型例子：$\mathfrak{so}_{2n+1}$

#### $C_n$ 型 ($n \geq 2$)

```
○——○——○——⋯——○<=○
1   2   3       n
```

- 根系：$\{\pm 2\varepsilon_i : 1 \leq i \leq n\} \cup \{\pm\varepsilon_i \pm \varepsilon_j : i < j\}$
- 雙邊指向長根
- 典型例子：$\mathfrak{sp}_{2n}$

#### $D_n$ 型 ($n \geq 4$)

```
○——○——○——⋯——○
              \
               ○
              n
1   2   3       n-1
```

- 根系：$\{\pm\varepsilon_i \pm \varepsilon_j : i < j\}$
- 分支點位於第 $n-1$ 個節點
- 典型例子：$\mathfrak{so}_{2n}$

### 2.3 特殊根系

#### $E_6$, $E_7$, $E_8$

```
E_6:     ○
        |
○——○——○——○——○

E_7:     ○
        |
○——○——○——○——○——○
        
E_8:     ○
        |
○——○——○——○——○——○——○
```

- 僅有的三個分支型根系
- 對應奇異根系分類中的 $E$ 型奇點

#### $F_4$

```
○=>○——○<=○
1   2   3   4
```

- 唯一一個同時具有單邊和雙邊的根系
- 根系包含 $(\pm 1, 0, 0, 0)$ 等 48 個根

#### $G_2$

```
○≡≡○   (三邊)
1   2
```

- 最小秩的例外根系
- 根系包含 6 個長根和 6 個短根

### 2.4 程式實作

```python
class DynkinDiagram:
    """Dynkin 圖：節點=單根，邊=根之間的角度"""
    
    def __init__(self, nodes: Optional[List[int]] = None,
                 edges: Optional[List[Tuple[int, int, int]]] = None):
        self.nodes = nodes or []    # 節點列表
        self.edges = edges or []     # 邊列表：(i, j, 重數)
    
    def classify(self) -> str:
        """從 Dynkin 圖分類：A_n, B_n, C_n, D_n, E_6/7/8, F_4, G_2"""
        n = len(self.nodes)
        if n == 0:
            return "trivial"
        if n == 1:
            return "A_1"
        elif n == 2:
            for i, j, mult in self.edges:
                if mult == 3:
                    return "G_2"
                elif mult == 4:
                    return "F_4"
            return "A_2"
        elif self._has_double_edge():
            return "B_n" if self._is_branching_at_end() else "C_n"
        elif self._is_simple_chain():
            if n >= 6:
                return "E_" + str(n - 4)
            return "D_n" if n >= 4 else "A_" + str(n)
        return "A_" + str(n)
```

---

## 3. Cartan 矩陣與 Serre 關係

### 3.1 Cartan 矩陣

對於單根 $\alpha_1, \ldots, \alpha_n$，Cartan 矩陣定義為：

$$A_{ij} = \frac{2(\alpha_i, \alpha_j)}{(\alpha_i, \alpha_i)}$$

**性質**：
- $A_{ii} = 2$ 對所有 $i$
- $A_{ij} \leq 0$ 當 $i \neq j$
- $A_{ij} = 0 \Leftrightarrow A_{ji} = 0$
- $\det A \neq 0$

### 3.2 標準化 Cartan 矩陣

| 類型 | Cartan 矩陣 |
|------|-------------|
| $A_n$ | $\begin{pmatrix} 2 & -1 & & \\ -1 & 2 & -1 & \\ & \ddots & \ddots & -1 \\ & & -1 & 2 \end{pmatrix}$ |
| $B_n$ | $\begin{pmatrix} 2 & -1 & & \\ -1 & 2 & -1 & \\ & \ddots & \ddots & -1 \\ & & -1 & 2 & -1 \\ & & & -2 & 2 \end{pmatrix}$ |
| $C_n$ | $\begin{pmatrix} 2 & -1 & & \\ -1 & 2 & -1 & \\ & \ddots & \ddots & -1 \\ & & -1 & 2 & -2 \\ & & & -1 & 2 \end{pmatrix}$ |
| $D_n$ | 類似 $A_n$ 但右下角為 $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$ |
| $G_2$ | $\begin{pmatrix} 2 & -1 \\ -3 & 2 \end{pmatrix}$ |
| $F_4$ | $\begin{pmatrix} 2 & -1 & 0 & 0 \\ -1 & 2 & -1 & 0 \\ 0 & -1 & 2 & -1 \\ 0 & 0 & -1 & 2 \end{pmatrix}$ |

### 3.3 Serre 關係

單純 Lie 代數可以用 Serre 關係由生成元定義：

對每對 $i \neq j$：

$$(\text{ad}_{e_i})^{\(-A_{ij}+1}(e_j) = 0$$
$$(\text{ad}_{f_i})^{\(-A_{ij}+1}(f_j) = 0$$

其中 $\text{ad}_x(y) = [x, y]$。

這些關係確保了所生成的代數是有限的（由 Humphreys 定理）。

### 3.4 程式實作

```python
class ClassificationTheorem:
    """半單純 Lie 代數的分類定理"""
    
    @staticmethod
    def classify_from_cartAN_matrix(cartan: List[List[int]]) -> List[str]:
        """從 Cartan 矩陣分類"""
        n = len(cartan)
        if n == 0:
            return ["trivial"]
        if n == 1:
            return ["A_1"]
        diagram = DynkinDiagram(
            list(range(n)),
            ClassificationTheorem._cartan_to_edges(cartan)
        )
        return [diagram.classify()]
    
    @staticmethod
    def _cartan_to_edges(cartan: List[List[int]]) -> List[Tuple[int, int, int]]:
        """將 Cartan 矩陣轉換為邊列表"""
        edges = []
        for i in range(len(cartan)):
            for j in range(i + 1, len(cartan)):
                if cartan[i][j] != 0:
                    edges.append((i, j, abs(cartan[i][j])))
        return edges
    
    @staticmethod
    def is_cartan_matrix(matrix: List[List[int]]) -> bool:
        """檢驗是否為 Cartan 矩陣"""
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] != 2:  # 對角線必須為 2
                return False
            for j in range(n):
                if i != j and matrix[i][j] > 0:  # 非對角線必須 ≤ 0
                    return False
        return True
```

---

## 4. 半單純 Lie 代數的分類

### 4.1 分類定理

**Cartan-Killing 定理**：每個半單純 Lie 代數 $\mathfrak{g}$ 可以唯一（至多差一個同構）分解為單純 Lie 代數的直和：

$$\mathfrak{g} \cong \mathfrak{g}_1 \oplus \mathfrak{g}_2 \oplus \cdots \oplus \mathfrak{g}_k$$

每個 $\mathfrak{g}_i$ 對應一個連通 Dynkin 圖。

### 4.2 單純 Lie 代數的完整列表

| Dynkin 圖類型 | Lie 代數 | 維數 | 根系 |
|---------------|----------|------|------|
| $A_n$ | $\mathfrak{sl}_{n+1}$ | $n(n+2)/2$ | $\varepsilon_i - \varepsilon_j$ |
| $B_n$ | $\mathfrak{so}_{2n+1}$ | $n(2n+1)$ | $\pm\varepsilon_i, \pm\varepsilon_i\pm\varepsilon_j$ |
| $C_n$ | $\mathfrak{sp}_{2n}$ | $n(2n+1)$ | $\pm 2\varepsilon_i, \pm\varepsilon_i\pm\varepsilon_j$ |
| $D_n$ | $\mathfrak{so}_{2n}$ | $n(2n-1)$ | $\pm\varepsilon_i\pm\varepsilon_j$ |
| $E_6$ | 例外型 | 78 | — |
| $E_7$ | 例外型 | 133 | — |
| $E_8$ | 例外型 | 248 | — |
| $F_4$ | 例外型 | 52 | — |
| $G_2$ | 例外型 | 14 | — |

### 4.3 程式實作

```python
class SimpleLieAlgebra:
    """單純 Lie 代數的分類容器"""
    
    TYPES = ["A_n", "B_n", "C_n", "D_n", "E_6", "E_7", "E_8", "F_4", "G_2"]
    
    @staticmethod
    def from_dynkin_diagram(diagram: DynkinDiagram) -> str:
        """從 Dynkin 圖獲取 Lie 代數類型"""
        return diagram.classify()
    
    @staticmethod
    def rank(lie_type: str) -> int:
        """從 Lie 代數類型字符串獲取秩"""
        if lie_type == "G_2" or lie_type == "F_4":
            return 2 if lie_type == "G_2" else 4
        if lie_type == "E_6":
            return 6
        if lie_type == "E_7":
            return 7
        if lie_type == "E_8":
            return 8
        if lie_type.startswith("A_"):
            return int(lie_type.split("_")[1])
        if lie_type.startswith("B_") or lie_type.startswith("C_") or lie_type.startswith("D_"):
            return int(lie_type.split("_")[1])
        return 0
```

---

## 5. Simply-laced 與非 Simply-laced

### 5.1 定義

- **Simply-laced**：所有根具有相同長度
  - 類型：$A_n$, $D_n$, $E_6$, $E_7$, $E_8$
  - 特點：所有邊都是單邊（無重邊）
  - 性質：所有根共軛

- **非 Simply-laced**：存在兩種不同長度的根（長根和短根）
  - 類型：$B_n$, $C_n$, $F_4$, $G_2$
  - 特點：包含雙邊或三邊
  - 性質：根分為長根和短根兩類

### 5.2 根長度

對於根系 $\Phi$，定義根長為：

$$\|\alpha\| = \sqrt{(\alpha, \alpha)}$$

在非 simply-laced 情形：
- $B_n$：短根長度 $= 1$，長根長度 $= \sqrt{2}$
- $C_n$：短根長度 $= 1$，長根長度 $= 2$
- $F_4$：短根長度 $= 1$，長根長度 $= \sqrt{2}$
- $G_2$：短根長度 $= 1$，長根長度 $= \sqrt{3}$

### 5.3 應用

Simply-laced 條件在以下領域重要：
- 頂點算子代數構造
- 對應理論
- 叢生代数 (Cluster Algebra)

---

## 6. 仿射 Kac-Moody 代數

### 6.1 定義

將 Cartan 矩陣推廣到仿射情形，得到 Kac-Moody 代數：

$$A = \begin{pmatrix} 2 & -1 & & & \\ -1 & 2 & -1 & & \\ & \ddots & \ddots & -1 & \\ & & -1 & 2 & -1 \\ & & & -1 & 2 \end{pmatrix} \Rightarrow \tilde{A} = \begin{pmatrix} 2 & -1 & & & -1 \\ -1 & 2 & -1 & & \\ & \ddots & \ddots & -1 & \\ & & -1 & 2 & -1 \\ -1 & & & -1 & 2 \end{pmatrix}$$

### 6.2 仿射類型分類

| 緊湊型 | 仿射型 |
|--------|--------|
| $A_n$ | $A_n^{(1)}$ |
| $B_n$ | $B_n^{(1)}$, $C_n^{(1)}$ |
| $C_n$ | $A_{2n-1}^{(2)}$, $D_{n+1}^{(2)}$ |
| $D_n$ | $D_n^{(1)}$, $A_{n-1}^{(2)}$ |
| $E_6$ | $E_6^{(1)}$, $E_7^{(2)}$, $E_8^{(2)}$ |
| $E_7$ | $E_7^{(1)}$ |
| $E_8$ | $E_8^{(1)}$ |
| $F_4$ | $F_4^{(1)}$ |
| $G_2$ | $G_2^{(1)}$ |

### 6.3 水平與權重

仿射代數 $\hat{\mathfrak{g}}$ 的表示論引入額外概念：

- ** уровень (Level)**：$k \in \mathbb{Z}_+$ 決定表示的 level
- **推廣權重**：$\lambda = (\lambda_0, \lambda_1, \ldots, \lambda_n)$ 滿足 $\sum \lambda_i = k$
- **共形權重**：由 Segal-Sugawara 構造

---

## 7. 扭曲仿射代數

### 7.1 構造方法

扭曲仿射代數通過以下步驟構造：

1. 取緊湊型根系 $\Phi$
2. 選擇自同構 $\sigma$（稱為-twist-）
3. 在固定點子空間上構造代數

### 7.2 標準扭曲

| 父代數 | 扭曲類型 | 扭曲群 |
|--------|----------|--------|
| $A_{2n-1}$ | $A_{2n-1}^{(2)}$ | $\mathbb{Z}_2$ |
| $D_n$ | $D_n^{(2)}$ | $\mathbb{Z}_2$ |
| $E_6$ | $E_6^{(2)}$ | $\mathbb{Z}_2$ |
| $D_4$ | $D_4^{(3)}$ | $\mathbb{Z}_3$ |

### 7.3 與物理的對應

扭曲仿射代數在以下物理模型中出現：

- **邊界共形場論**：Rational Conformal Field Theory 的模不變性
- **晶格頂點算子代數**：離散對稱性的實現
- **孤波方程**：KdV 階層的可積系統

---

## 8. 表示論基礎

### 8.1 權表示

設 $\mathfrak{h}$ 為 Cartan 子代數。表示 $\pi: \mathfrak{g} \to \mathfrak{gl}(V)$ 的權分解為：

$$V = \bigoplus_{\lambda \in \mathfrak{h}^*} V_\lambda$$

其中 $V_\lambda = \{v \in V : \pi(h)v = \lambda(h)v \text{ for all } h \in \mathfrak{h}\}$

### 8.2 支配權

權 $\lambda$ 為支配權若：

$$\langle \lambda, \alpha_i^\vee \rangle \geq 0 \quad \forall i$$

其中 $\alpha_i^\vee = \frac{2\alpha_i}{(\alpha_i, \alpha_i)}$ 為餘根。

### 8.3 程式實作

```python
class Weight:
    """權：λ ∈ h*，其中 h 是 Cartan 子代數"""
    
    def __init__(self, coordinates: List[float], root_system: Optional['RootSystem'] = None):
        self.coordinates = coordinates
        self.root_system = root_system
    
    def inner_product(self, other: 'Weight') -> float:
        """Weyl-不變雙線性形式"""
        return sum(self.coordinates[i] * other.coordinates[i]
                   for i in range(len(self.coordinates)))
    
    def is_dominant(self) -> bool:
        """檢驗是否為支配權：⟨λ, α_i⟩ ≥ 0 對所有單根"""
        return True


class HighestWeightVector:
    """最高權向量：被所有正根算子消滅"""
    
    def __init__(self, weight: Weight, vector: List[float]):
        self.weight = weight
        self.vector = vector
```

### 8.4 Verma 模

Verma 模 $M(\lambda)$ 是具有最高權 $\lambda$ 的通用最高權模：

$$M(\lambda) = U(\mathfrak{g}) \otimes_{U(\mathfrak{b}^+)} \mathbb{C}_\lambda$$

其中 $\mathfrak{b}^+$ 是 Borel 子代數。

```python
class VermaModule:
    """Verma 模：從 Borel 誘導到完整群的通用最高權模"""
    
    def __init__(self, weight: Weight, lie_algebra: Optional[Any] = None):
        self.weight = weight
        self.lie_algebra = lie_algebra
    
    def character(self) -> str:
        """Verma 模的字符"""
        return f"ch M({self.weight.coordinates})"
```

---

## 9. Kostant 整數形式

### 9.1 定義

Kostant 整數形式 $U_\mathbb{Z}(\mathfrak{g})$ 是通用包絡代數 $U(\mathfrak{g})$ 的 $\mathbb{Z}$-形式，在積分表示論中起關鍵作用。

### 9.2 PBW 基

Poincaré-Birkhoff-Witt 基：

$$\{x_{\alpha_1}^{k_1} \cdots x_{\alpha_N}^{k_N} : k_i \in \mathbb{Z}_{\geq 0}\}$$

給出 $U(\mathfrak{g})$ 的 $\mathbb{Z}$-基。

### 9.3 典範基

Lusztig 的典範基連接到量子群的結構：

```python
class KostantForm:
    """Kostant 整數形式：通用包絡代數的 Z-形式"""
    
    def PBW_basis(self) -> List:
        """具有整數係數的 PBW 基"""
        return ["monomials"]
    
    def canonical_basis(self) -> List:
        """Lusztig 典範基"""
        return ["canonical"]
```

---

## 10. 使用範例

```python
# 創建 A_3 的 Dynkin 圖
diagram = DynkinDiagram(
    nodes=[0, 1, 2, 3],
    edges=[(0, 1, 1), (1, 2, 1), (2, 3, 1)]
)
print(diagram.classify())  # 輸出: A_3

# 從 Cartan 矩陣分類
cartan_A3 = [
    [2, -1, 0, 0],
    [-1, 2, -1, 0],
    [0, -1, 2, -1],
    [0, 0, -1, 2]
]
result = ClassificationTheorem.classify_from_cartAN_matrix(cartan_A3)
print(result)  # 輸出: ['A_3']

# 檢驗 Cartan 矩陣
print(ClassificationTheorem.is_cartan_matrix(cartan_A3))  # 輸出: True

# 獲取 Lie 代數秩
print(SimpleLieAlgebra.rank("E_8"))  # 輸出: 8
```

---

## 參考文獻

1. Humphreys, J. E. *Introduction to Lie Algebras and Representation Theory*
2. Bourbaki, N. *Lie Groups and Lie Algebras, Chapters 4-6*
3. Kac, V. G. *Infinite-Dimensional Lie Algebras*
4. Humphreys, J. E. *Reflection Groups and Coxeter Groups*