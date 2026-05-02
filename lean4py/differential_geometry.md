# 微分幾何模塊 (Differential Geometry)

本文件說明 `lean4py/differential_geometry.py` 模塊的數學原理。該模塊提供了光滑流形、切空間、聯絡以及黎曼幾何的基本構建。

---

## 1. 流形 (Manifolds)

### 數學定義

**流形**是可局部同胚於 $\mathbb{R}^n$ 的拓撲空間。具體來說：

- 若 $M$ 為 Hausdorff、第二可數的拓撲空間
- 對每一點 $p \in M$，存在開集 $U \subset M$ 和開集 $V \subset \mathbb{R}^n$
- 使得存在同胚 $\varphi: U \to V$

則稱 $M$ 為 **$n$ 維光滑流形**。

### 圖冊與坐標卡

流形上的**坐標卡** (chart) 為二元組 $(U, \varphi)$，其中：
- $U \subset M$ 為開集，稱為**定義域**
- $\varphi: U \to \mathbb{R}^n$ 為連續雙射

**圖冊** (atlas) 為一組相容的坐標卡，覆蓋整個流形。兩張坐標卡 $(U_i, \varphi_i)$ 和 $(U_j, \varphi_j)$ **相容**當轉移函數

$$\varphi_j \circ \varphi_i^{-1}: \varphi_i(U_i \cap U_j) \to \varphi_j(U_i \cap U_j)$$

為光滑函數。

### 代碼對應

```python
class Manifold:
    """光滑流形：局部同胚於 R^n 的拓撲空間"""
    def __init__(self, dimension: int, name: str = "M"):
        self.dimension = dimension      # 流形維數 n
        self.name = name
        self.charts: List[Dict] = []     # 坐標卡列表
        self.atlas: List[Dict] = []      # 圖冊
```

---

## 2. 切空間 $T_pM$ (Tangent Space)

### 數學定義

設 $M$ 為 $n$ 維光滑流形，$p \in M$ 為一點。**切空間** $T_pM$ 是在 $p$ 點所有切向量的集合，維數為 $n$。

在 $\mathbb{R}^n$ 中，點 $p$ 處的切空間 $T_p\mathbb{R}^n \cong \mathbb{R}^n$ 為所有從 $p$ 出發的有向線段。

### 幾何直觀

切空間是流形在 $p$ 點的**線性近似**。如同曲面在某一點的切平面，推廣到高維流形即為切空間。

### 代碼對應

```python
class TangentSpace:
    """流形上一點 p 的切空間 T_p M"""
    def __init__(self, manifold: Manifold, point: Any):
        self.manifold = manifold
        self.point = point               # 基點 p
        self.basis: List = []            # 基底向量
```

**關鍵性質**：
- $\dim T_pM = \dim M = n$
- 基底可選為 $\left\{\frac{\partial}{\partial x^1}\bigg|_p, \ldots, \frac{\partial}{\partial x^n}\bigg|_p\right\}$

---

## 3. 切向量作為導數 (Tangent Vectors as Derivations)

### 數學定義

光滑流形上，$p$ 點的切向量可定義為**導數**：

$$v: C^\infty(M) \to \mathbb{R}$$

滿足線性性與 Leibniz 律：
1. $v(f + g) = v(f) + v(g)$
2. $v(fg) = f(p) v(g) + g(p) v(f)$

### 與曲線的對應

每條光滑曲線 $\gamma: (-\varepsilon, \varepsilon) \to M$，$\gamma(0) = p$，定義切向量：

$$v_{\gamma}(f) = \frac{d}{dt}\bigg|_{t=0} f(\gamma(t))$$

### 物理意義

切向量代表**無窮小位移**或**方向導數」。在物理中，速度向量即為流形上的切向量。

---

## 4. 餘切空間 $T_p^*M$ (Cotangent Space)

### 數學定義

**餘切空間** $T_p^*M$ 為切空間的對偶空間：

$$T_p^*M = (T_pM)^* = \mathrm{Hom}(T_pM, \mathbb{R})$$

維數同樣為 $n$，其元素稱為**餘切向量**或**1-形式**。

### 餘切向量的具體形式

若 $(x^1, \ldots, x^n)$ 為坐標，則餘切空間基底為：

$$dx^1|_p, \ldots, dx^n|_p$$

滿足 $dx^i\left(\frac{\partial}{\partial x^j}\bigg|_p\right) = \delta_j^i$。

### 重要性質

- 餘切向量是**線性泛函**，輸入切向量輸出實數
- 在相變換下服從協變變換規則
- 可視為「標量函數的微分」

---

## 5. 向量場 (Vector Fields)

### 數學定義

**向量場** $X$ 是流形上每點指定一個切向量：

$$X: M \to TM, \quad p \mapsto X_p \in T_pM$$

向量場是切叢的**光滑截面** (section)。

### 光滑性條件

向量場 $X$ 光滑當且僅當對所有光滑函數 $f \in C^\infty(M)$，複合函數 $p \mapsto X(f)$ 光滑。

### 局部表示

在坐標 $(x^1, \ldots, x^n)$ 下：

$$X = X^i \frac{\partial}{\partial x^i}$$

其中 $X^i: U \to \mathbb{R}$ 為光滑函數。

### 代碼對應

```python
class VectorField:
    """流形上的向量場：切叢的光滑截面"""
    def __init__(self, manifold: Manifold):
        self.manifold = manifold
        self.value_at: Dict[Any, List[float]] = {}  # 每點的值
```

---

## 6. 光滑映射 (Smooth Maps)

### 數學定義

設 $F: M \to N$ 為流形間的連續映射。$F$ 為**光滑**當且僅當：

- 對每點 $p \in M$，存在坐標卡 $(U, \varphi)$ 和 $(V, \psi)$
- 使得 $p \in U$，$F(U) \subset V$
- 組合 $\psi \circ F \circ \varphi^{-1}: \mathbb{R}^m \to \mathbb{R}^n$ 為光滑函數

### 光滑函數

標量函數 $f: M \to \mathbb{R}$ 光滑即其在局部坐標下為光滑函數。

### 向量值函數

$F = (F^1, \ldots, F^n): M \to \mathbb{R}^n$ 光滑當每個分量 $F^i$ 光滑。

---

## 7. 前推 (Pushforward / Differential)

### 數學定義

光滑映射 $F: M \to N$ 在 $p$ 點的**前推** (或微分) 為線性映射：

$$dF_p: T_pM \to T_{F(p)}N$$

定義為：

$$dF_p(v)(f) = v(f \circ F)$$

其中 $v \in T_pM$，$f \in C^\infty(N)$。

### 坐標表示

在局部坐標下，若 $F = (F^1, \ldots, F^n)$，則：

$$dF_p\left(\frac{\partial}{\partial x^j}\bigg|_p\right) = \frac{\partial F^i}{\partial x^j}(p) \frac{\partial}{\partial y^i}\bigg|_{F(p)}$$

### Jacobian 矩陣

前推映射的矩陣表示為 Jacobian：

$$[dF_p] = \begin{pmatrix} \frac{\partial F^1}{\partial x^1} & \cdots & \frac{\partial F^1}{\partial x^m} \\ \vdots & \ddots & \vdots \\ \frac{\partial F^n}{\partial x^1} & \cdots & \frac{\partial F^n}{\partial x^m} \end{pmatrix}$$

---

## 8. 餘向量的拉回 (Pullback of Covectors)

### 數學定義

設 $F: M \to N$ 為光滑映射，$\omega \in T_{F(p)}^*N$ 為餘切向量。**拉回** $\omega$ 得到 $F^*\omega \in T_p^*M$：

$$(F^*\omega)_p(v) = \omega_{F(p)}(dF_p(v))$$

其中 $v \in T_pM$。

### 微分形式的拉回

對於 $k$-形式 $\omega \in \Omega^k(N)$：

$$(F^*\omega)_p(v_1, \ldots, v_k) = \omega_{F(p)}(dF_p(v_1), \ldots, dF_p(v_k))$$

### 坐標變換

拉回運算將餘切向量從目標流形「拉回」到原流形，服從**協變**變換規則。

---

## 9. 外微分 (Exterior Derivative)

### 數學定義

**外微分** $d: \Omega^k(M) \to \Omega^{k+1}(M)$ 是定義在微分形式上的算子。

對 $k$-形式 $\omega$，$d\omega$ 為 $(k+1)$-形式，定義為：

$$d\omega(X_0, \ldots, X_k) = \sum_{i=0}^k (-1)^i X_i(\omega(X_0, \ldots, \hat{X}_i, \ldots, X_k))$$

$$+ \sum_{i < j} (-1)^{i+j} \omega([X_i, X_j], X_0, \ldots, \hat{X}_i, \ldots, \hat{X}_j, \ldots, X_k)$$

### 局部坐標公式

若 $\omega = \omega_{i_1 \ldots i_k} dx^{i_1} \wedge \cdots \wedge dx^{i_k}$，則：

$$d\omega = \sum_{j} \frac{\partial \omega_{i_1 \ldots i_k}}{\partial x^j} dx^j \wedge dx^{i_1} \wedge \cdots \wedge dx^{i_k}$$

### 基本性質

1. **封閉性**: $d \circ d = 0$
2. **導出性質**: $d(\alpha \wedge \beta) = d\alpha \wedge \beta + (-1)^k \alpha \wedge d\beta$

---

## 10. 李括積 $[X, Y]$ (Lie Bracket)

### 數學定義

兩個向量場 $X, Y$ 的**李括積** $[X, Y]$ 定義為：

$$[X, Y](f) = X(Y(f)) - Y(X(f))$$

對所有 $f \in C^\infty(M)$。

### 坐標表示

在局部坐標下：

$$X = X^i \frac{\partial}{\partial x^i}, \quad Y = Y^i \frac{\partial}{\partial x^i}$$

$$[X, Y] = \left(X^j \frac{\partial Y^i}{\partial x^j} - Y^j \frac{\partial X^i}{\partial x^j}\right) \frac{\partial}{\partial x^i}$$

### 代碼對應

```python
class VectorField:
    def lie_bracket(self, other: 'VectorField') -> 'VectorField':
        """向量場的 Lie 括積 [X, Y]"""
        return VectorField(self.manifold)
```

### 關鍵性質

1. **反對稱性**: $[X, Y] = -[Y, X]$
2. **Jacobi 恆等式**: $[X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] = 0$
3. $[X, Y]$ 衡量向量場的**非交換性**

---

## 11. 聯絡 (Connection / Levi-Civita Connection)

### 數學定義

**仿射聯絡** $\nabla$ 是映射：

$$\nabla: \Gamma(TM) \times \Gamma(TM) \to \Gamma(TM), \quad (X, Y) \mapsto \nabla_X Y$$

滿足：
1. $\nabla_{fX} Y = f \nabla_X Y$（$C^\infty$-線性）
2. $\nabla_X (fY) = X(f)Y + f \nabla_X Y$（Leibniz 律）

### Christoffel 符號

在局部坐標下：

$$\nabla_{\frac{\partial}{\partial x^j}} \frac{\partial}{\partial x^k} = \Gamma^i_{jk} \frac{\partial}{\partial x^i}$$

$\Gamma^i_{jk}$ 為 **Christoffel 符號**（聯絡係數）。

### 代碼對應

```python
class Connection:
    """仿射聯絡：∇: Γ(TM) × Γ(TM) → Γ(TM)"""
    def __init__(self, manifold: Manifold):
        self.christoffel_symbols: Dict[Tuple, float] = {}  # Γ^i_{jk}
```

### Levi-Civita 聯絡

在黎曼流形 $(M, g)$ 上，存在**唯一**的聯絡滿足：
1. **撓率為零**: $T(X, Y) = \nabla_X Y - \nabla_Y X - [X, Y] = 0$
2. **度量相容**: $\nabla g = 0$

此聯絡即為 **Levi-Civita 聯絡**。

### 代碼對應

```python
class LeviCivitaConnection(Connection):
    """Levi-Civita 聯絡：唯一的無撓率、度量相容聯絡"""
    def is_metric_compatible(self) -> bool:
        """檢查 ∇g = 0 (Levi-Civita 條件)"""
        return True
```

---

## 模塊結構總覽

| 類別 | 數學對象 | 維數 |
|------|----------|------|
| `Manifold` | 光滑流形 $M$ | $n$ |
| `TangentSpace` | 切空間 $T_pM$ | $n$ |
| `TangentBundle` | 切叢 $TM = \bigsqcup_{p \in M} T_pM$ | $2n$ |
| `VectorField` | 向量場 $\Gamma(TM)$ | $n$ |
| `Connection` | 仿射聯絡 $\nabla$ | — |
| `RiemannianMetric` | 黎曼度量 $g$ | $n(n+1)/2$ |
| `Geodesic` | 測地線 $\gamma$ | — |
| `LeviCivitaConnection` | Levi-Civita 聯絡 | — |
| `CurvatureTensor` | 曲率張量 $R$ | $n^4$ |
| `RiemannianManifold` | 黎曼流形 $(M, g)$ | — |
| `Submanifold` | 子流形 | — |

---

## 延伸主題

### 測地線 (Geodesics)

測地線是滿足**測地線方程**的曲線：

$$\nabla_{\dot{\gamma}} \dot{\gamma} = 0$$

即「加速度為零」的曲線。測地線是**局部最短路徑**。

### 曲率張量 (Curvature Tensor)

**黎曼曲率張量**定義為：

$$R(X, Y)Z = \nabla_X \nabla_Y Z - \nabla_Y \nabla_X Z - \nabla_{[X, Y]} Z$$

衡量空間的**內稟曲率**。從它可導出：
- **Ricci 曲率**: $R_{ij} = R^k_{ikj}$
- **純量曲率**: $R = g^{ij}R_{ij}$

### 子流形 (Submanifolds)

設 $i: S \hookrightarrow M$ 為流形的浸入或嵌入。**第二基本形式** II 衡量子流形如何彎曲於周圍流形中：

$$\mathrm{II}(X, Y) = (\nabla_X Y)^\perp$$

---

## 參考文獻

- John M. Lee, *Introduction to Smooth Manifolds* (第2版)
- Manfredo do Carmo, *Riemannian Geometry*
- Boothby, *An Introduction to Differentiable Manifolds and Riemannian Geometry*