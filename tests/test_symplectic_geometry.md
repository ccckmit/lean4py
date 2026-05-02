# 辛几何测试文档 (test_symplectic_geometry.py)

本文档解释 `test_symplectic_geometry.py` 中测试用例的数学原理。

## 1. 测试概述

本模块测试辛几何的核心概念，包括辛流形、辛形式、哈密顿向量场、矩映射、辛同胚、拉格朗日子流形等。辛几何是处理辛流形上几何与动力系统的数学分支，在经典力学和数学物理中具有重要地位。

测试文件位置：`tests/test_symplectic_geometry.py`
源模块：`lean4py/symplectic_geometry.py`

---

## 2. 辛流形测试 (TestSymplecticManifold)

### 数学原理

辛流形是带有辛形式 ω 的光滑偶数维流形。辛形式是非退化的闭2-形式，局部上可表示为：

$$\omega = \sum_{i=1}^{n} dp_i \wedge dq^i$$

其中 (q^i, p_i) 为达布坐标系。

### 测试验证内容

| 测试方法 | 验证内容 | 数学意义 |
|---------|---------|---------|
| `test_creation` | 流形维数为4，半维数为2 | 辛流形需满足 dim M = 2n |
| `test_even_dimension_required` | 奇数维流形抛出 ValueError | 辛流形必须是偶数维 |
| `test_add_chart` | 成功添加达布坐标卡 | 添加局部坐标系 |
| `test_is_symplectic` | 流形具有辛结构 | 验证辛形式存在且非退化 |
| `test_dimension_of` | 返回正确的维数 | 维度计算正确性 |

---

## 3. 辛形式测试 (TestSymplecticForm)

### 数学原理

辛形式 ω 是流形上的2-形式，具有两个关键性质：
1. **闭性**：dω = 0（外微分等于零）
2. **非退化性**：若对所有 Y 都有 ω(X, Y) = 0，则 X = 0

在达布坐标下，标准辛形式为：
$$\omega = \sum_{i=1}^{n} dp_i \wedge dq^i$$

其分量可表示为：
$$\omega_{ij} = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$$

### 测试验证内容

```python
# 评估 ω(X, Y) 的计算
X = [1.0, 0.0, 0.0, 0.0]
Y = [0.0, 0.0, 1.0, 0.0]
val = omega.evaluate(X, Y)  # 结果应为 1.0
```

| 测试方法 | 验证内容 | 数学意义 |
|---------|---------|---------|
| `test_creation` | 辛形式正确关联到流形 | 对象关系正确 |
| `test_components` | 辛形式具有非零分量 | 标准形式初始化成功 |
| `test_evaluate` | ω(X, Y) 计算正确 | 2-形式作用在两个向量上 |
| `test_is_closed` | dω = 0 | 辛形式的闭性条件 |
| `test_is_nondegenerate` | ω^n ≠ 0 | 辛形式的非退化性 |

**关键数学事实**：辛形式的分量矩阵是反对称矩阵，其行列式为 1（当维数为 2n 时）。

---

## 4. 哈密顿向量场测试 (TestHamiltonianVectorField)

### 数学原理

给定哈密顿函数 H，流形上的哈密顿向量场 X_H 由下式定义：

$$\omega(X_H, Y) = Y(H) \quad \forall Y \in TM$$

在达布坐标中，哈密顿方程为：
$$\frac{dq^i}{dt} = \frac{\partial H}{\partial p_i}, \quad \frac{dp_i}{dt} = -\frac{\partial H}{\partial q^i}$$

哈密顿向量场的流保持辛形式，即辛同胚。

### 测试验证内容

```python
# 创建哈密顿向量场
H = lambda x: x[0]  # H = x₀
Hvf = HamiltonianVectorField(sm, H)

# 在指定点计算向量场
vec = Hvf.vector_at([1.0, 2.0, 3.0, 4.0])  # 返回4维向量

# 哈密顿 flow 计算
result = Hvf.flow([1.0, 2.0, 3.0, 4.0], 0.5)  # exp(tX_H)(x)
```

| 测试方法 | 验证内容 | 数学意义 |
|---------|---------|---------|
| `test_creation` | X_H 正确关联到流形和哈密顿量 | 对象构造正确 |
| `test_vector_at` | 在给定点返回正确维数的向量 | X_H(p) 的计算 |
| `test_flow` | t=0 时流返回原位置 | 辛流的定义性质 |

**关键数学事实**：哈密顿向量场的积分曲线是哈密顿系统的相流。

---

## 5. 矩映射测试 (TestMomentMap)

### 数学原理

矩映射是辛流形到李代数对偶的映射：

$$\Phi: M \to \mathfrak{g}^*$$

对于紧李群 G 在辛流形上的作用，若满足：

$$\langle d\Phi, \xi \rangle = \alpha_\xi$$

其中 α_ξ 是对应李代数元 ξ 的 Killing 向量场生成的1形式，则称 Φ 为矩映射。

等变性条件：
$$\Phi(g \cdot x) = \text{Ad}_g^*(\Phi(x))$$

### 测试验证内容

```python
# 创建 SU(2) 群的矩映射
mm = MomentMap(sm, "SU2")

# 在给定点求矩映射值
val = mm.at_point([1.0, 2.0, 3.0, 4.0])  # 返回 "momentum"

# 检查等变性
mm.is_equivariant()  # 验证群作用等变性

# 求像的维数 (SU(2) 的对偶李代数为 3 维)
img = mm.image_of_point([1.0, 2.0, 3.0, 4.0])  # 返回3维向量
```

| 测试方法 | 验证内容 | 数学意义 |
|---------|---------|---------|
| `test_creation` | 矩映射正确关联到流形和群 | 对象构造正确 |
| `test_at_point` | 返回映射值 | Φ(x) 的计算 |
| `test_is_equivariant` | 群等变性条件 | equivariance 验证 |
| `test_image_of_point` | 像的维数正确 | SU(2) 对应 3 维 |

**关键数学事实**：矩映射在辛约化中起核心作用，用于构造约化流形。

---

## 6. 泊松括号测试 (TestPoissonBracket)

### 数学原理

泊松括号是流形上函数代数 C^∞(M) 的反对称双线性运算：

$$\{f, g\} = \omega(X_f, X_g) = \sum_{i=1}^{n} \left( \frac{\partial f}{\partial q^i} \frac{\partial g}{\partial p_i} - \frac{\partial f}{\partial p_i} \frac{\partial g}{\partial q^i} \right)$$

满足雅可比恒等式：
$$\{f, \{g, h\}\} + \{g, \{h, f\}\} + \{h, \{f, g\}\} = 0$$

### 测试验证内容

```python
pb = PoissonBracket(sm)
f = lambda x: x[0]
g = lambda x: x[1]

# 计算泊松括号
pb.compute(f, g, [1.0, 2.0, 3.0, 4.0])  # {x₀, x₁} = 0

# 验证雅可比恒等式
pb.jacobi_identity(f, g, h)  # 应返回 True
```

---

## 7. 辛同胚测试 (TestSymplectomorphism)

### 数学原理

辛同胚是保持辛形式的微分同胚：

$$\phi^* \omega = \omega$$

即对所有向量 X, Y 和点 p：
$$\omega_p(d\phi(X), d\phi(Y)) = \omega_p(X, Y)$$

### 测试验证内容

```python
# 恒等映射是辛同胚
phi = Symplectomorphism(sm, lambda x: x)

# 函数拉回
f = lambda x: x[0]
pulled = phi.pullback_function(f)
pulled([1.0, 2.0, 3.0, 4.0]) == 3.0  # φ*(f) = f ∘ φ

# 向量推送
phi.pushforward_vector([1.0, 2.0, 3.0, 4.0], [0.0, 0.0, 0.0, 0.0])
```

---

## 8. 拉格朗日子流形测试 (TestLagrangianSubmanifold)

### 数学原理

拉格朗日子流形 L ⊂ M 满足：
1. dim L = dim M / 2
2. ω|_L = 0（辛形式限制为零）

局部上，拉格朗日子流形可表示为图像 y = ∂S/∂x（势函数 S）。

### 测试验证内容

```python
L = LagrangianSubmanifold(sm, 2)  # 4维流形上的2维子流形
L.is_lagrangian()  # 检查 dim M = 2 × dim L
L1.intersection_with(L2)  # 典型交点为有限个点
```

---

## 9. 哈密顿系统测试 (TestHamiltonianSystem)

### 数学原理

哈密顿系统 (M, ω, H) 由辛流形和哈密顿函数组成。哈密顿方程描述系统的动力学：

$$\frac{dx}{dt} = X_H(x)$$

系统具有能量守恒：H(φ_t(x)) = H(x)

### 测试验证内容

```python
hs = HamiltonianSystem(sm, H=lambda x: x[0]**2 + x[1]**2)

# 哈密顿方程
hs.hamilton_equations([1.0, 2.0, 3.0, 4.0])  # 返回4个导数

# 数值求解
traj = hs.solve([0.0, 0.0, 0.0, 0.0], 0.0, 1.0, 10)  # 11个点

# 能量守恒检验
hs.energy_conservation(traj)  # 应接近0
```

---

## 10. 接触流形测试 (TestContactManifold, TestReebVectorField)

### 数学原理

接触流形是奇数维流形 (2n+1)，带有接触1形式 α 满足：
$$\alpha \wedge (d\alpha)^n \neq 0$$

里夫向量场 R 满足：
$$\alpha(R) = 1, \quad d\alpha(R, \cdot) = 0$$

---

## 测试套件总结

| 测试类 | 核心验证对象 | 关键性质 |
|-------|-------------|---------|
| TestSymplecticManifold | 辛流形结构 | 偶数维、辛形式存在 |
| TestSymplecticForm | 辛2-形式 | 闭性、非退化性 |
| TestHamiltonianVectorField | 哈密顿向量场 | 由哈密顿函数生成 |
| TestPoissonBracket | 泊松括号 | 雅可比恒等式 |
| TestMomentMap | 矩映射 | 群等变性 |
| TestSymplectomorphism | 辛同胚 | 保辛结构 |
| TestLagrangianSubmanifold | 拉格朗日子流形 | 维数减半、限制消失 |
| TestHamiltonianSystem | 哈密顿动力系统 | 能量守恒 |
| TestContactManifold | 接触结构 | 奇数维、接触条件 |
| TestReebVectorField | 里夫向量场 | α(R)=1, dα(R,·)=0 |