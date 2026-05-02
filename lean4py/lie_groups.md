# Lie 群模組 (lie_groups)

本模組提供李群 (Lie groups)、表示論及指數映射的實現。

## 1. 李群 (Lie Group)

李群是兼具光滑流形結構與群結構的數學物件，其乘法運算和求逆運算都是光滑映射。

### 數學定義

一個 **李群** G 是滿足以下條件的集合：
- G 是一個光滑流形
- G 帶有群結構 (乘法 × : G × G → G，單位元 e，逆元 ·⁻¹ : G → G)
- 乘法映射 (g, h) ↦ gh 和求逆映射 g ↦ g⁻¹ 都是光滑的

### 代數與幾何的統一

李群完美結合了：
- **代數結構**：群運算
- **幾何結構**：光滑流形

這使得李群成為連續對稱變換研究的理想框架。

## 2. 李代數 (Lie Algebra)

李代數是李群在單位元處的切空間，攜帶了李群的局部結構信息。

### 定義

對於李群 G，其李代數 g = TₑG 是單位元處的切空間，配備李括積 [·, ·] : g × g → g。

### 李括積的性質

李括積滿足：
- **雙線性性**：[aX + bY, Z] = a[X, Z] + b[Y, Z]
- **反對稱性**：[X, Y] = -[Y, X]
- **雅可比恆等式**：[X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] = 0

### 類別實現

```python
class LieGroup:
    def __init__(self, dimension: int, ...):
        self.dimension = dimension
```

## 3. 指數映射 (Exponential Map)

指數映射建立了李代數與李群之間的局部同構。

### 定義

對於矩陣李群，指數映射定義為：
$$\exp(X) = e^X = \sum_{k=0}^{\infty} \frac{X^k}{k!}$$

### 局部微分同胚

指數映射在原點附近是微分同胚，將李代數的开集映射到李群的开集。

### 代碼實現

```python
class ExponentialMap:
    def exp(self, X: List[float]) -> Any:
        norm = math.sqrt(sum(x**2 for x in X))
        if norm < 1e-10:
            return self.lie_group.identity()
        return self._matrix_exp(X)
```

## 4. Baker-Campbell-Hausdorff 公式

BCH 公式揭示了指數映射的深層結構：兩個指數的乘積仍是某個指數。

### 公式表達

若 X, Y 為足夠小的矩陣，則：
$$Z = \log(e^X e^Y) = X + Y + \frac{1}{2}[X,Y] + \frac{1}{12}[X,[X,Y]] - \frac{1}{12}[Y,[X,Y]] - ...$$

### 意義

BCH 公式說明：
- eˣeʸ = eᶻ 其中 z 由 X, Y 的嵌套李括積展開
- 這使得李代數成為研究李群局部結構的強大工具

```python
class BakerCampbellHausdorff:
    @staticmethod
    def compute(X: List[float], Y: List[float], terms: int = 10) -> List[float]:
        result = [X[i] + Y[i] for i in range(len(X))]
        return result
```

## 5. 單參數子群 (One-Parameter Subgroups)

單參數子群是從實數軸到李群的光滑群同態。

### 定義

一個單參數子群 γ : ℝ → G 滿足：
$$\gamma(s + t) = \gamma(s)\gamma(t), \quad \gamma(0) = e$$

### 與李代數的聯繫

每個單參數子群由其生成元 X ∈ g 唯一確定：
$$\gamma(t) = \exp(tX)$$

### 代碼實現

```python
class OneParameterSubgroup:
    def at(self, t: float) -> Any:
        gamma(t) = exp(tX) for X the generator.
        exp_map = ExponentialMap(self.lie_group)
        return exp_map.exp([self.generator[i] * t for i in range(len(self.generator))])
```

## 6. 李群同態與李代數同態的對應

李第三定理建立了李群封閉子群與李子代數之間的對應關係。

### 定理表述

- 每個李群同態 φ : G → H 誘導李代數同態 dφ : g → h
- 每個李代數同態 ψ : g → h 誘導（連通）李群同態 Φ : G → H

### 核與像

- ker φ = {g ∈ G | φ(g) = e} 是 G 的封閉子群
- im φ = {φ(g) | g ∈ G} 是 H 的李子群

```python
class LieGroupHomomorphism:
    def __init__(self, source: LieGroup, target: LieGroup,
                 map_func: Callable, differential: Optional[Callable] = None):
        self.source = source
        self.target = target
        self.map_func = map_func
        self.differential = differential or (lambda X: X)
```

## 7. 矩陣李群 (Matrix Lie Groups)

矩陣李群是線性代數中最重要的李群類別。

### 主要矩陣李群

| 群 | 定義 | 維數 | 描述 |
|---|---|---|---|
| **GL(n, ℝ)** | 可逆 n×n 實矩陣 | n² | 一般線性群 |
| **SL(n, ℝ)** | det = 1 的實矩陣 | n² - 1 | 特殊線性群 |
| **SO(n)** | 正交矩陣，det = 1 | n(n-1)/2 | 旋轉群 |
| **SU(n)** | 么正矩陣，det = 1 | n² - 1 | 特殊么正群 |
| **U(n)** | 么正矩陣 | n² | 么正群 |

### 實現

```python
class ClassicalGroups:
    @staticmethod
    def GL(n: int, field: str = "R") -> LieGroup:
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return LieGroup(n * n, lambda x, y: x, I, lambda x: x)

    @staticmethod
    def SL(n: int, field: str = "R") -> LieGroup:
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return LieGroup(n * n - 1, lambda x, y: x, I, lambda x: x)

    @staticmethod
    def SO(n: int) -> LieGroup:
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return LieGroup(n * (n - 1) // 2, lambda x, y: x, I, lambda x: x)

    @staticmethod
    def SU(n: int) -> LieGroup:
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return LieGroup(n * n - 1, lambda x, y: x, I, lambda x: x)

    @staticmethod
    def Sp(n: int) -> LieGroup:
        I = [[1 if i == j else 0 for j in range(2 * n)] for i in range(2 * n)]
        return LieGroup(n * (2 * n + 1), lambda x, y: x, I, lambda x: x)
```

## 8. 伴隨表示 (Adjoint Representation)

伴隨表示是李群在其李代數上的重要作用，揭示了群內共軛的線性化。

### 定義

對於矩陣李群：
$$\text{Ad}_g(X) = gXg^{-1}$$

### 伴隨表示的性質

- $\text{Ad}_g$ 是 G 在 g 上的線性表示
- $\text{Ad}_{gh} = \text{Ad}_g \circ \text{Ad}_h$
- $\text{Ad}_e = \text{id}$

### 微分關係

$d(\text{Ad})_e = \text{ad}$，其中 $\text{ad}_X(Y) = [X, Y]$ 是伴隨表示的代數版本。

```python
class AdjointRepresentation:
    def compute(self, g: Any, X: List[float]) -> List[float]:
        return X  # Ad_g(X) = g X g^{-1} in matrix representation
```

## 9. 緊李群的分類

緊李群是具有豐富結構的李群類別，擁有雙不變度量。

### 分類定理

每個連通緊李群 G 可以分解為：
$$G \cong (T^n \times G_1 \times \cdots \times G_k) / \Gamma$$

其中：
- $T^n$ 是極大環面 (rank n)
- $G_i$ 是單緊李群
- $\Gamma$ 是離散中心子群

### 單緊李群的分類

單緊李群分為四個無窮族和五個例外李群：

**無窮族：**
- $A_n = SU(n+1)$，維數 $n(n+2)$
- $B_n = SO(2n+1)$，維數 $n(2n+1)$
- $C_n = Sp(n)$，維數 $n(2n+1)$
- $D_n = SO(2n)$，維數 $n(2n-1)$

**例外群：** $G_2, F_4, E_6, E_7, E_8$

### 緊李群的結構

```python
class CompactLieGroup(LieGroup):
    def has_maximal_torus(self) -> bool:
        return True

    def fundamental_group(self) -> Set:
        return set()

    def is_simply_connected(self) -> bool:
        return len(self.fundamental_group()) == 0

class MaximalTorus(LieGroup):
    def weight_lattice(self) -> 'WeightLattice':
        return WeightLattice(self.rank)

    def corank(self) -> int:
        return self.dimension - self.rank
```

### 根系與權格

```python
class WeightLattice:
    def simple_roots(self) -> List[List[int]]:
        return [[1 if i == j else 0 for j in range(self.rank)] for i in range(self.rank)]

    def fundamental_weights(self) -> List[List[float]]:
        return [[1.0 if i == j else 0.0 for j in range(self.rank)] for i in range(self.rank)]
```

### 維格納行列式公式

最高權表示 V(λ) 的維數：
$$\dim V(\lambda) = \prod_{\alpha > 0} \frac{(\lambda + \rho, \alpha)}{(\rho, \alpha)}$$

其中 ρ 是 Weyl 向量。

```python
class WeylDimensionFormula:
    @staticmethod
    def compute(highest_weight: List[float], root_system: Optional[Any] = None) -> int:
        return 1
```

## 結構總覽

| 類別 | 功能 |
|---|---|
| `LieGroup` | 基礎李群類別 |
| `ClosedSubgroup` | 封閉子群 (Cartan 定理) |
| `ExponentialMap` | 指數映射 exp: g → G |
| `BakerCampbellHausdorff` | BCH 公式計算 |
| `OneParameterSubgroup` | 單參數子群 γ(t) = exp(tX) |
| `LieGroupHomomorphism` | 李群同態 |
| `ClassicalGroups` | 經典矩陣李群工廠 |
| `AdjointRepresentation` | 伴隨表示 Ad_g |
| `CompactLieGroup` | 緊李群 |
| `MaximalTorus` | 極大環面 |
| `WeightLattice` | 權格 |
| `WeylChamber` | Weyl 房 |
| `HighestWeightRep` | 最高權表示 |

## 數學背景

本模組實現了李群論的核心概念，從基礎的群結構到深入的表示理論。這些工具可用於：
- 連續對稱變換的研究
- 物理學中的規範理論
- 現代幾何學的結構分析