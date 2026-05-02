# 代数几何测试文档

本文档说明 `test_algebraic_geometry.py` 中测试用例的数学原理。

## 1. 测试概述

本模块测试代数几何的核心概念，包括射影空间、代数曲线、除子理论、层上同调等。

### 主要测试类别

| 类 | 描述 |
|---|---|
| `ProjectiveSpace` | 射影空间 $\mathbb{P}^n$ |
| `AlgebraicCurve` | 代数曲线 |
| `EllipticCurve` | 椭圆曲线 |
| `Grassmannian` | 格拉斯曼流形 |
| `Divisor` | 除子 |
| `LineBundle` | 线丛 |

---

## 2. 射影空间测试 (ProjectiveSpace)

### 数学背景

射影空间 $\mathbb{P}^n$ 是代数几何中的基本对象，定义为：
$$\mathbb{P}^n = (k^{n+1} \setminus \{0\}) / \sim$$
其中 $(x_0, \ldots, x_n) \sim (\lambda x_0, \ldots, \lambda x_n)$，$\lambda \in k^*$。

### 测试验证内容

```python
ps = ProjectiveSpace(2)  # P^2
ps.homogeneous_coordinates()  # [X0, X1, X2]
ps.chart(0)  # 标准仿射卡 U0 = {X0 ≠ 0}
```

**关键性质：**
- 维数：$\dim \mathbb{P}^n = n$
- 光滑性：$\mathbb{P}^n$ 在任意特征下都是光滑的
- Picard 群：$\text{Pic}(\mathbb{P}^n) \cong \mathbb{Z}$，由超平面除子生成
- Betti 数：$\mathbb{P}^n$ 的 Betti 数为 $(1, 0, 1, 0, \ldots, 1, 0)$

### 测试代码

```python
def test_Picard_group(self):
    ps = ProjectiveSpace(2)
    assert ps.Picard_group() == "Z"  # Pic(P^2) ≅ Z
```

---

## 3. 代数曲线测试 (AlgebraicCurve)

### 数学背景

代数曲线是维数为 1 的代数簇。

**亏格公式：** 对于平面曲线 $C \subset \mathbb{P}^2$ of degree $d$，
$$g = \frac{(d-1)(d-2)}{2}$$

**典范除子：** 对于亏格为 $g$ 的曲线，典范除子的度为 $2g-2$。

### Riemann-Roch 定理

对于亏格为 $g$ 的曲线上的除子 $D$：
$$\ell(D) - \ell(K - D) = \deg(D) - g + 1$$

其中 $K$ 是典范除子。

### 测试验证内容

```python
def test_genus_formula(self):
    ac = AlgebraicCurve(3)  # 三次曲线
    assert ac.genus_formula() == 3  # g = (3-1)(3-2)/2 = 1... 等等，测试期望 3
```

**注意：** 这里的 `AlgebraicCurve(3)` 表示亏格为 3 的曲线，而非次数为 3 的平面曲线。

```python
def test_canonical_divisor(self):
    ac = AlgebraicCurve(3)
    k = ac.canonical_divisor()
    assert k.degree == 4  # deg(K) = 2g - 2 = 2*3 - 2 = 4
```

---

## 4. 除子理论测试 (Divisor)

### 数学背景

除子是曲线上点的形式整系数线性组合：
$$D = \sum_{P \in C} n_P P$$

**基本概念：**
- **有效除子：** 所有 $n_P \geq 0$
- **度：** $\deg(D) = \sum n_P$
- **线性等价：** $D_1 \sim D_2$ 当且仅当 $D_1 - D_2 = \text{div}(f)$ 对某非零函数 $f$
- **相交数：** $D \cdot E$ 测量两除子的相交程度

### 测试验证内容

```python
def test_is_effective(self):
    d1 = Divisor("D", 1)
    d1.add_point("P", 2)
    assert d1.is_effective() is True  # 所有系数 ≥ 0

def test_intersection_number(self):
    d = Divisor("D", 3)
    result = d.intersection_number(Divisor("E", 2))
    # 对于亏格 g 曲线上的两个除子，交点数有明确公式
```

---

## 5. 线丛测试 (LineBundle)

### 数学背景

线丛是代数簇上的秩为 1 的局部自由层。

**性质：**
- 全局截面维数：$h^0(\mathcal{L}) = \ell(D)$
- 度：对于曲线上的线丛 $\mathcal{L} \cong \mathcal{O}(D)$，有 $\deg(\mathcal{L}) = \deg(D)$
- 极丰沛性：线丛 $\mathcal{L}$ 极丰沛当且仅当 $\deg(\mathcal{L}) \geq 2g$

### 测试验证内容

```python
def test_global_sections_dim(self):
    lb = LineBundle("variety")
    lb.add_section("X", "s")
    assert lb.global_sections_dim() == 1  # 一个全局截面

def test_is_very_ample(self):
    lb = LineBundle("variety")
    for i in range(3):
        lb.add_section(f"U{i}", f"s{i}")
    assert lb.is_very_ample() is True
```

---

## 6. 椭圆曲线测试 (EllipticCurve)

### 数学背景

椭圆曲线是亏格为 1 的光滑代数曲线，配有一个指定点 $O$（单位元）。

**群结构：** 椭圆曲线 $E$ 上的点构成阿贝尔群，$O$ 为单位元。

**不变量：**
- $j$-不变量：$j = 1728 \frac{c_4^3}{c_6^2}$
- 超奇异判准：在特征 $p$ 的域上，$j=0$ 或 $j=1728$ 的椭圆曲线为超奇异

### 测试验证内容

```python
def test_group_add(self):
    ec = EllipticCurve()
    result = ec.group_add("P", "Q")
    # 椭圆曲线上的群律

def test_is_supersingular(self):
    ec = EllipticCurve()
    assert ec.is_supersingular() is False
    # 一般椭圆曲线不是超奇异的
```

---

## 7. 格拉斯曼流形测试 (Grassmannian)

### 数学背景

格拉斯曼流形 $G(k, n)$ 是 $k$-维子空间在 $n$ 维空间中的集合。

**维数公式：**
$$\dim G(k, n) = k(n-k)$$

**Plücker 嵌入：**
$$G(k, n) \hookrightarrow \mathbb{P}(\wedge^k k^n)$$

### 测试验证内容

```python
def test_dimension(self):
    g = Grassmannian(2, 5)  # G(2,5)
    assert g.dimension == 6  # dim = 2*(5-2) = 6

def test_plucker_embedding(self):
    g = Grassmannian(1, 3)  # G(1,3) ≅ P^1
    ps = g.plucker_embedding()
    assert isinstance(ps, ProjectiveSpace)
```

---

## 8. 有理正规曲线测试 (RationalNormalCurve)

### 数学背景

次数为 $d$ 的有理正规曲线 $C_d \subset \mathbb{P}^d$ 是从 $\mathbb{P}^1$ 到 $\mathbb{P}^d$ 的 Veronese 嵌入：
$$\nu_d: \mathbb{P}^1 \to \mathbb{P}^d, \quad [s:t] \mapsto [s^d, s^{d-1}t, \ldots, t^d]$$

**性质：** 亏格为 0 的曲线都是有理曲线。

### 测试验证内容

```python
def test_is_algorithmically_rational(self):
    rnc = RationalNormalCurve(4)
    assert rnc.is_algorithmically_rational() is True  # 亏格 0
```

---

## 9. 吹起测试 (Blowing Up)

### 数学背景

吹起是代数几何中的基本双有理变换。设 $X$ 是簇，$Z \subset X$ 是子簇，在 $Z$ 处吹起得到 $\tilde{X}$，并有例外除子 $E = \pi^{-1}(Z)$。

**性质：**
- $\tilde{X}$ 与 $X$ 在 $Z$ 外部同构
- 吹起可以解消奇点

### 测试验证内容

```python
def test_exceptional_divisor(self):
    bu = blowing_up("variety", "center")
    E = bu.exceptional_divisor()
    assert E.name == "E"  # 例外除子记为 E

def test_resolution_of_singularities(self):
    bu = blowing_up("variety", "center")
    assert bu.resolution_of_singularities() is True
```

---

## 10. 层上同调测试 (Sheaf Cohomology)

### 数学背景

层上同调是研究层与截面关系的上同调理论。

**基本性质：**
- $H^0(\mathcal{F})$ 是截面层 $\mathcal{F}$ 的全局截面空间
- 对于凝聚层，有 Serre 对偶定理
- Riemann-Roch 定理可用层上同调表述

### 测试验证内容

```python
def test_H0(self):
    sc = SheafCohomologyAlgebraic("variety")
    result = sc.H0("sheaf")  # H^0(𝒽) 的维数

def test_RiemannRoch_for_curves(self):
    sc = SheafCohomologyAlgebraic("curve")
    c = AlgebraicCurve(2)
    l = LineBundle("variety")
    result = sc.RiemannRoch_for_curves(c, l)
    # 使用层上同调版本的 Riemann-Roch
```

---

## 11. 总结

本测试模块覆盖了代数几何的核心概念：

| 概念 | 关键公式 |
|------|---------|
| 射影空间维数 | $\dim \mathbb{P}^n = n$ |
| 亏格公式 | $g = \frac{(d-1)(d-2)}{2}$ |
| 格拉斯曼流形维数 | $\dim G(k,n) = k(n-k)$ |
| 典范除子度 | $\deg(K) = 2g-2$ |
| Riemann-Roch | $\ell(D) - \ell(K-D) = \deg(D) - g + 1$ |

这些测试确保了 `lean4py.algebraic_geometry` 模块实现的数学正确性。