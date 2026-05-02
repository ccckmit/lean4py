# 微分幾何測試文檔 (Differential Geometry Testing Documentation)

## 概述

本文檔說明 `lean4py` 項目中微分幾何模塊的測試案例，涵蓋從基礎流形概念到高級曲率理論的完整測試體系。測試套件位於 `tests/` 目錄下，分為三個層次：

- `test_differential_geometry.py` - 基礎與核心功能測試
- `test_differential_geometry_enhanced.py` - 增強功能測試
- `test_differential_geometry_advanced.py` - 高級理論測試

---

## 1. 流形測試 (Manifold Tests)

### 測試位置
`test_differential_geometry.py` - `TestManifold` 類 (第10-27行)

### 數學原理

流形 (Manifold) 是微分幾何中的核心概念，是一類在局部與歐氏空間同胚的 Hausdorff 空間。n 維流形 M 的每個點 p 都有一個開鄰域與 ℝⁿ 開集同胚，這使得我們可以在流形上建立局部坐標系。

**測試驗證內容：**

```python
def test_creation(self):
    m = Manifold(3, "S^3")
    assert m.dimension == 3
    assert m.name == "S^3"
```

- **維度 (Dimension)**：流形的維度是定義流形結構的基本參數。3 維流形 S³ 是拓撲學中重要的例子
- **名稱 (Name)**：便於識別和調試的流形標識

```python
def test_add_chart(self):
    m = Manifold(2)
    m.add_chart({1, 2}, lambda x: x)
    assert len(m.charts) == 1
```

- **圖冊 (Atlas)**：流形的圖冊是覆蓋整個流形的坐標圖的集合。每個 chart 將流形上的開集映射到 ℝⁿ 的開集

```python
def test_is_smooth(self):
    m = Manifold(2)
    assert m.is_smooth() is True
```

- **光滑性 (Smoothness)**：光滑流形是可以進行微分運算的流形，是黎曼幾何研究的基礎

### 測試數學意義

流形測試確保了 `Manifold` 類能夠正確存儲和管理流形的基本結構，包括維度、圖冊和光滑性等核心屬性。這些是進行所有後續微分幾何運算的基礎。

---

## 2. 切空間測試 (Tangent Space Tests)

### 測試位置
`test_differential_geometry.py` - `TestTangentSpace` 類 (第30-52行)

### 數學原理

設 M 為 n 維光滑流形，p ∈ M 為一點。過點 p 的切空間 TₚM 是流形上所有切向量組成的向量空間。切向量可以理解為流形上通過 p 点的曲線的切方向，或者作為作用於光滑函數的導子。

**切空間的維度**：
對於 n 維流形上的任意點 p，有 dim(TₚM) = n。這是因為在局部坐標系下，切空間與 ℝⁿ 同構。

**測試驗證內容：**

```python
def test_creation(self):
    m = Manifold(2)
    ts = TangentSpace(m, "p")
    assert ts.manifold == m
    assert ts.point == "p"
```

- 切空間是與特定流形上的特定點關聯的數學結構
- 每個切空間記錄其基於哪個流形以及哪個點

```python
def test_dimension_of(self):
    m = Manifold(3)
    ts = TangentSpace(m, "p")
    assert ts.dimension_of() == 3
```

- 切空間的維度等於其所在流形的維度

```python
def test_add_basis_vector(self):
    m = Manifold(2)
    ts = TangentSpace(m, "p")
    ts.add_basis_vector([1.0, 0.0])
    assert len(ts.basis) == 1
```

- 基底向量是切空間的生成元集合
- 流形的維度決定了切空間的基底向量個數

```python
def test_get_basis(self):
    m = Manifold(2)
    ts = TangentSpace(m, "p")
    basis = ts.get_basis()
    assert len(basis) == 2
```

- 標準基底的維度為 2（對於 2 維流形的切空間）

---

## 3. 切叢與向量場測試 (Tangent Bundle & Vector Field Tests)

### 測試位置
`test_differential_geometry.py` - `TestTangentBundle` 類 (第55-76行) 和 `TestVectorField` 類 (第78-100行)

### 數學原理

**切叢 (Tangent Bundle)**：
切叢 TM 是流形 M 上所有切空間的并集：
```
TM = ∐_{p∈M} TₚM
```
TM 本身是一個 2n 維光滑流形。存在自然投影 π: TM → M 將每個切向量映射到其基點。

**向量場 (Vector Field)**：
向量場 X 是流形上每一點都關聯一個切向量的光滑映射：
```
X: M → TM,  π(X(p)) = p
```
向量場可以看作切叢的光滑截面。

**測試驗證內容：**

```python
def test_dimension(self):
    m = Manifold(2)
    tb = TangentBundle(m)
    assert tb.dimension() == 4
```

- 對於 n 維流形 M，切叢 TM 的維度為 2n
- 這是因為切叢是流形與其切空間的「復合」結構

```python
def test_projection(self):
    m = Manifold(3)
    tb = TangentBundle(m)
    assert tb.projection("v") == m
```

- 投影映射將切叢中的向量映射回基流形

```python
def test_lie_bracket(self):
    m = Manifold(2)
    X = VectorField(m)
    Y = VectorField(m)
    Z = X.lie_bracket(Y)
    assert Z.manifold == m
```

- 李括號 [X, Y] 定義了向量場間的非交換乘法
- [X, Y] = XY - YX 也是一個向量場
- 李括號滿足雅可比恆等式，構成李代數結構

---

## 4. 聯絡測試 (Connection Tests)

### 測試位置
`test_differential_geometry.py` - `TestConnection` 類 (第103-134行)

### 數學原理

聯絡 (Connection) 是在切叢上定義平行移動的數學結構。協變導數 ∇ₓY 表示沿向量場 X 對向量場 Y 求導。

**克里斯托費爾符號 (Christoffel Symbols)**：
在局部坐標系中，聯絡由克里斯托費爾符號 Γᵏᵢⱼ 確定：
```
∇_{∂/∂xᵢ} ∂/∂xⱼ = Γᵏ_{ij} ∂/∂x_k
```

**撓率 (Torsion)**：
聯絡的撓率張量 T 定義為：
```
T(X, Y) = ∇ₓY - ∇ᵧX - [X, Y]
```

**協變導數 (Covariant Derivative)**：
協變導數推廣了歐氏空間中偏導數的概念到流形上，確保導數運算與坐標系無關。

**測試驗證內容：**

```python
def test_set_christoffel(self):
    m = Manifold(2)
    c = Connection(m)
    c.set_christoffel(0, 1, 0, 0.5)
    assert c.get_christoffel(0, 1, 0) == 0.5
```

- 克里斯托費爾符號存儲聯絡的系數
- Γ¹₀₀ = 0.5 表示坐標信息

```python
def test_covariant_derivative(self):
    m = Manifold(2)
    c = Connection(m)
    X = VectorField(m)
    Y = VectorField(m)
    result = c.covariant_derivative(X, Y)
    assert result.manifold == m
```

- 協變導數的結果仍然是流形上的向量場

```python
def test_torsion(self):
    m = Manifold(2)
    c = Connection(m)
    X = VectorField(m)
    Y = VectorField(m)
    T = c.torsion(X, Y)
    assert T.manifold == m
```

- 撓率張量也是流形上的張量場

---

## 5. 黎曼度量與測地線測試 (Riemannian Metric & Geodesic Tests)

### 測試位置
`test_differential_geometry.py` - `TestRiemannianMetric` 類 (第137-164行) 和 `TestGeodesic` 類 (第167-193行)

### 數學原理

**黎曼度量 (Riemannian Metric)**：
黎曼度量 g 是在流形每點的切空間上定義的內積：
```
gₚ: TₚM × TₚM → ℝ
```
度量給流形帶來了長度、角度和面積的概念。

**測地線 (Geodesic)**：
測地線是測地線方程的解，曲線的切向量沿自身平行移動：
```
∇_{γ̇}γ̇ = 0
```

**能量與長度**：
- 曲線長度：L(γ) = ∫√(g(γ̇,γ̇)) dt
- 曲線能量：E(γ) = ½∫g(γ̇,γ̇) dt

**測試驗證內容：**

```python
def test_inner_product_at(self):
    m = Manifold(2)
    rm = RiemannianMetric(m)
    rm.set_metric("p", [[1, 0], [0, 1]])  # 歐氏度量
    assert rm.inner_product_at("p", [1, 0], [0, 1]) == 0
```

- 正交性：標準基向量互相垂直

```python
def test_norm(self):
    m = Manifold(2)
    rm = RiemannianMetric(m)
    rm.set_metric("p", [[1, 0], [0, 1]])
    assert abs(rm.norm("p", [3.0, 4.0]) - 5.0) < 1e-6
```

- ||(3,4)|| = √(9+16) = 5（勾股定理）

```python
def test_length(self):
    m = Manifold(2)
    rm = RiemannianMetric(m)
    g = Geodesic(rm, [0.0, 0.0], [1.0, 0.0])
    result = g.length(0, 1)
    assert result == 1.0
```

- 從 (0,0) 到 (1,0) 的測地線長度為 1

```python
def test_energy(self):
    m = Manifold(2)
    rm = RiemannianMetric(m)
    g = Geodesic(rm, [0.0, 0.0], [1.0, 0.0])
    result = g.energy(0, 1)
    assert result == 0.5
```

- 能量 = ½ × 速度² × 時間 = ½ × 1² × 1 = 0.5

---

## 6. 萊布尼茲-奇塔聯絡與曲率測試 (Levi-Civita Connection & Curvature Tests)

### 測試位置
`test_differential_geometry.py` - `TestLeviCivitaConnection` 類 (第196-207行) 和 `TestCurvatureTensor` 類 (第210-243行)

### 數學原理

**萊布尼茲-奇塔聯絡 (Levi-Civita Connection)**：
萊布尼茲-奇塔聯絡是黎曼流形上唯一的無撓率且與度量兼容的協變導數。它滿足：
1. T(∇) = 0（無撓率）
2. ∇g = 0（度量兼容）

**黎曼曲率張量 (Riemann Curvature Tensor)**：
```
R(X,Y)Z = ∇ₓ∇ᵧZ - ∇ᵧ∇ₓZ - ∇_{[X,Y]}Z
```
曲率張量描述了流形的內稟曲率。

**里奇曲率 (Ricci Curvature)**：
Ric(X, Y) = tr(g)(R(X, ·)Y·) 是曲率張量的收縮。

**數量曲率 (Scalar Curvature)**：
R = g^{ij}Ric_{ij} 是里奇曲率的進一步收縮。

**截面曲率 (Sectional Curvature)**：
K(σ) = ⟨R(e₁, e₂)e₂, e₁⟩ 描述二維切平面的曲率。

**測試驗證內容：**

```python
def test_is_metric_compatible(self):
    m = Manifold(2)
    rm = RiemannianMetric(m)
    lc = LeviCivitaConnection(rm)
    assert lc.is_metric_compatible() is True
```

- 萊布尼茲-奇塔聯絡與度量始終兼容

```python
def test_compute_riemann(self):
    m = Manifold(2)
    c = Connection(m)
    ct = CurvatureTensor(c)
    result = ct.compute_riemann(0, 1, 0, 1)
    assert isinstance(result, float)
```

- 黎曼曲率分量 R¹₀₁⁰ 是實數

```python
def test_section_curvature(self):
    m = Manifold(2)
    c = Connection(m)
    ct = CurvatureTensor(c)
    result = ct.section_curvature([1, 0], [0, 1])
    assert isinstance(result, float)
```

- 截面曲率是標量值

---

## 7. 黎曼流形與子流形測試 (Riemannian Manifold & Submanifold Tests)

### 測試位置
`test_differential_geometry.py` - `TestRiemannianManifold` 類 (第246-268行) 和 `TestSubmanifold` 類 (第271-287行)

### 數學原理

**黎曼流形 (Riemannian Manifold)**：
配備了黎曼度量的光滑流形，可用於定義距離、拉普拉斯算子和梯度。

**距離函數**：
d(p, q) = inf{ L(γ) | γ 連接 p 和 q }

**梯度 (Gradient)**：
grad f 是使 g(grad f, X) = X(f) 成立的向量場。

**拉普拉斯算子 (Laplacian)**：
Δf = div(grad f)

**子流形 (Submanifold)**：
子流形是嵌入到環境流形中的流形。其第二基本形式描述了子流形如何彎曲於環境流形中。

**餘維數 (Codimension)**：
codim(N) = dim(M) - dim(N)

**測試驗證內容：**

```python
def test_distance(self):
    rm = RiemannianManifold(2)
    result = rm.distance([0, 0], [3, 4])
    assert abs(result - 5.0) < 1e-6
```

- 歐氏平面上 (0,0) 到 (3,4) 的距離為 5

```python
def test_laplacian(self):
    rm = RiemannianManifold(2)
    f = lambda x: x[0]**2
    Lf = rm.laplacian(f)
    assert callable(Lf)
```

- 拉普拉斯算子作用於函數仍為函數

```python
def test_codimension(self):
    m = Manifold(3)
    sm = Submanifold(m, lambda x: [1, 2])
    result = sm.codimension()
    assert isinstance(result, int)
```

- 餘維數是整數

---

## 8. 增強測試 - 測地線方程與截面曲率

### 測試位置
`test_differential_geometry_enhanced.py`

### 數學原理

**測地線方程 (Geodesic Equation)**：
在局部坐標系下，測地線滿足：
```
d²xᵏ/dτ² + Γᵏ_{ij}(dxⁱ/dτ)(dxʲ/dτ) = 0
```

**克里斯托費爾符號計算**：
從度量張量 gᵢⱼ 計算克里斯托費爾符號：
```
Γᵏ_{ij} = ½g^{kl}(∂ᵢg_{jl} + ∂ⱼg_{il} - ∂ₗg_{ij})
```

**高斯-博内定理 (Gauss-Bonnet Theorem)**：
對於緊致 2 維黎曼流形 M：
```
∫ₘ K dA = 2π χ(M) = 2π(2 - 2g)
```
其中 g 是流形的 genus（虧格）。

**歐拉示性數 (Euler Characteristic)**：
- 球面 (g=0)：χ = 2
- 環面 (g=1)：χ = 0

**測試驗證內容：**

```python
def test_christoffel_symbols(self):
    metric = [[1.0, 0.0], [0.0, 1.0]]  # 歐氏度量
    symbols = GeodesicEquation.christoffel_symbols(metric, dim=2)
    assert len(symbols) == 2  # 2 個指標
```

- 歐氏空間的克里斯托費爾符號恆為零

```python
def test_euler_characteristic(self):
    assert GaussBonnet.euler_characteristic(genus=0) == 2
    assert GaussBonnet.euler_characteristic(genus=1) == 0
```

- χ(S²) = 2, χ(T²) = 0

```python
def test_total_curvature(self):
    assert GaussBonnet.total_curvature(genus=0) == pytest.approx(4 * math.pi, abs=1e-10)
```

- ∫K dA = 4π（對於單位球面，K=1, A=4π）

---

## 9. 高級測試 - 曲率與特徵類

### 測試位置
`test_differential_geometry_advanced.py`

### 數學原理

**指數映射 (Exponential Map)**：
expₚ: TₚM → M 將切向量映射到沿測地線移動單位參數後的點。

**雅可比場 (Jacobi Field)**：
雅可比場是沿測地線滿足雅可比方程的向量場：
```
J'' + R(J, γ̇)γ̇ = 0
```
它描述了測地線族的變分。

**和樂群 (Holonomy Group)**：
沿所有閉路平行移動形成的線性變換群。對於 n 維黎曼流形，和樂群是 O(n) 的子群。

**陳類 (Chern Class)**：
復向量叢的示性類，定義為：
```
c_k(E) ∈ H^{2k}(M, ℤ)
```

**龐特里亞金類 (Pontryagin Class)**：
實向量叢的示性類：
```
p_k(E) ∈ H^{4k}(M, ℤ)
```

**歐拉類 (Euler Class)**：
與方向可定向性相關的示性類，僅當歐拉示性數非零時存在。

**測試驗證內容：**

```python
def test_exponential_map(self):
    result = GeodesicAdvanced.exponential_map("M", (0, 0), (1, 0))
    assert isinstance(result, tuple)
```

- 指數映射返回一個點坐標元組

```python
def test_jacobi_field(self):
    result = GeodesicAdvanced.jacobi_field("γ")
    assert "field" in result
```

- 雅可比場是向量場的一種

```python
def test_chern_class(self):
    result = CharacteristicClass.chern_class("E", 1)
    assert "class" in result
```

- 陳類返回帶 "class" 標識的結果

---

## 10. 測試套件的數學完整性

### 測試覆蓋範圍

測試套件覆蓋了微分幾何的核心主題：

| 主題 | 測試類 | 主要驗證 |
|------|--------|----------|
| 流形 | TestManifold | 維度、圖冊、光滑性 |
| 切空間 | TestTangentSpace | 維度、基底 |
| 切叢 | TestTangentBundle | 2n 維結構、投影 |
| 向量場 | TestVectorField | 值設置、李括號 |
| 聯絡 | TestConnection | 克里斯托費爾、協變導數、撓率 |
| 黎曼度量 | TestRiemannianMetric | 內積、范數 |
| 測地線 | TestGeodesic | 曲線、長度、能量 |
| 萊布尼茲-奇塔 | TestLeviCivitaConnection | 度量兼容性 |
| 曲率張量 | TestCurvatureTensor | 黎曼、里奇、數量、截面曲率 |
| 黎曼流形 | TestRiemannianManifold | 距離、梯度、拉普拉斯 |
| 子流形 | TestSubmanifold | 餘維數、第二基本形式 |
| 測地線方程 | TestGeodesicEquation | 克里斯托費爾計算、方程求解 |
| 高斯-博内 | TestGaussBonnet | 歐拉示性數、總曲率 |
| 高級理論 | TestCurvature, TestHolonomy, TestCharacteristicClass | 指數映射、雅可比場、和樂群、特徵類 |

### 數學驗證原則

1. **結構保持**：驗證運算結果的類型和結構正確
2. **維度一致**：確保維度關係始終成立
3. **特殊值驗證**：使用已知結果（如歐氏空間、球面）進行驗證
4. **數值精度**：使用浮點容差確保數值計算的準確性

---

## 附錄：主要數學公式速查

- 切叢維度：dim(TM) = 2 dim(M)
- 測地線方程：γ̈ᵏ + Γᵏ_{ij}γ̇ⁱγ̇ʲ = 0
- 黎曼曲率：R(X,Y)Z = ∇ₓ∇ᵧZ - ∇ᵧ∇ₓZ - ∇_{[X,Y]}Z
- 高斯-博內：∫ₘ K dA = 2π χ(M)
- 歐拉示性數：χ = 2 - 2g（對於緊致曲面）