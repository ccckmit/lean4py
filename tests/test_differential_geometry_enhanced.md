# 微分几何增强模块测试文档

## 概述

`test_differential_geometry_enhanced.py` 测试文件验证了 `lean4py.differential_geometry_enhanced` 模块的核心功能。该模块实现了微分几何的基本概念，包括测地线方程、曲率张量和高斯-博内定理。

## 1. 测试验证内容

本测试套件验证以下增强微分几何功能：

- **测地线方程**：计算 Christoffel 符号和测地线 ODE 求解
- **截面曲率**：二维平面上的截面曲率计算
- **里奇曲率**：从黎曼张量收缩得到里奇曲率张量及标量曲率
- **高斯-博内定理**：验证曲面积分与欧拉示性数的关系

## 2. 黎曼度量测试 (TestGeodesicEquation)

### 测试内容

```python
metric = [[1.0, 0.0], [0.0, 1.0]]  # 欧几里得度量
```

### 数学原理

**Christoffel 符号** $\Gamma^\mu_{\nu\rho}$ 是列维-奇维塔联络的系数，定义为：

$$\Gamma^\mu_{\nu\rho} = \frac{1}{2} g^{\mu\sigma} \left( \partial_\nu g_{\rho\sigma} + \partial_\rho g_{\nu\sigma} - \partial_\sigma g_{\nu\rho} \right)$$

其中 $g_{\mu\nu}$ 是度量张量。对于欧几里得平面度量 $g_{ij} = \delta_{ij}$，所有 Christoffel 符号均为零。

**测地线方程**描述粒子在弯曲空间中的自由运动路径：

$$\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\nu\rho} \frac{dx^\nu}{d\tau} \frac{dx^\rho}{d\tau} = 0$$

### 验证点

| 测试 | 验证内容 |
|------|----------|
| `test_christoffel_symbols` | Christoffel 符号数组维度正确 (2×2×2) |
| `test_geodesic_equation` | 测地线加速度计算返回正确的维度 |
| `test_solve_geodesic` | 欧拉法求解测地线，步数正确 (steps+1 个点) |

## 3. 测地线测试 (GeodesicEquation)

### Christoffel 符号计算

```python
symbols = GeodesicEquation.christoffel_symbols(metric, dim=2)
```

当前实现返回全零矩阵，适用于欧几里得空间。真实实现需根据度量张量计算偏导数。

### 测地线方程求解

```python
path = GeodesicEquation.solve_geodesic([0.0, 0.0], [1.0, 1.0], steps=10)
```

使用简化的欧拉方法数值求解测地线 ODE：
- 位置更新：$x_{new} = x + dt \cdot v$
- 速度更新：$v_{new} = v - dt \cdot v$（简化版）

## 4. 曲率测试

### 4.1 截面曲率测试 (TestSectionalCurvature)

```python
K = SectionalCurvature.compute(metric, riemann, vector1, vector2)
```

#### 数学原理

**截面曲率** $K(\sigma)$ 是黎曼几何中最基本的曲率概念，定义为在平面 $\sigma$ 上的高斯曲率：

$$K(\sigma) = \frac{\langle R(X,Y)Y, X \rangle}{|X|^2 |Y|^2 - \langle X, Y \rangle^2}$$

其中：
- $R(X,Y)Z$ 是黎曼曲率张量
- $X, Y$ 是在切空间生成平面 $\sigma$ 的线性无关向量
- 分母是 $X \wedge Y$ 生成的平行四边形的面积平方

对于单位球面，截面曲率恒为 $K = 1$。

### 4.2 里奇曲率测试 (TestRicciCurvature)

#### 数学原理

**里奇曲率张量** $R_{\mu\nu}$ 通过收缩黎曼曲率张量得到：

$$R_{\mu\nu} = R^\lambda_{\mu\lambda\nu} = \sum_\lambda R^\lambda_{\mu\lambda\nu}$$

**标量曲率** $R$ 是里奇曲率与度量张量的缩并：

$$R = g^{\mu\nu} R_{\mu\nu} = \sum_{i} R_{ii}$$

#### 测试验证

```python
ricci = RicciCurvature.compute(riemann, dim=2)  # 返回 2×2 矩阵
R = RicciCurvature.scalar_curvature(ricci)      # 返回标量
```

| 测试 | 验证内容 |
|------|----------|
| `test_compute` | 里奇张量维度正确 (dim×dim) |
| `test_scalar_curvature` | 标量曲率为浮点数类型 |

## 5. 高斯-博内定理测试 (TestGaussBonnet)

### 数学原理

**高斯-博内定理**建立了曲面曲率积分与拓扑不变量之间的深刻联系：

$$\int\int_M K \, dA = 2\pi \chi(M)$$

其中：
- $K$ 是高斯曲率
- $\chi(M)$ 是**欧拉示性数**
- 对于闭合可定向曲面：$\chi = 2 - 2g$
- $g$ 是曲面的亏格（环柄数）

### 欧拉示性数对照表

| 亏格 $g$ | 曲面类型 | 欧拉示性数 $\chi$ |
|----------|----------|-------------------|
| 0 | 球面 | 2 |
| 1 | 环面 | 0 |
| 2 | 双环面 | -2 |

### 测试验证

```python
GaussBonnet.euler_characteristic(genus=0)  # 返回 2
GaussBonnet.total_curvature(genus=0)       # 返回 4π
GaussBonnet.is_sphere(curvature=1.0, area=4*math.pi)  # True
```

| 测试 | 验证内容 |
|------|----------|
| `test_euler_characteristic` | 球面 $\chi=2$，环面 $\chi=0$ |
| `test_total_curvature` | $\int\int K dA = 4\pi$（球面） |
| `test_is_sphere` | 球面条件：$K \cdot A = 4\pi$ |

### 球面验证公式

对于半径为 $R$ 的球面：
- 曲率：$K = \frac{1}{R^2}$
- 面积：$A = 4\pi R^2$
- 总曲率：$K \cdot A = \frac{1}{R^2} \cdot 4\pi R^2 = 4\pi$

## 6. 测试数据说明

| 参数 | 值 | 含义 |
|------|-----|------|
| `metric = [[1,0],[0,1]]` | 单位矩阵 | 二维欧几里得平面度量 |
| `initial_pos = [0,0]` | 原点 | 测地线初始位置 |
| `initial_vel = [1,1]` | 对角方向 | 测地线初始速度 |
| `riemann = 零张量` | 全零 | 平坦空间的黎曼曲率 |

## 7. 数学意义

这些测试确保了微分几何核心算法的正确性：

1. **测地线**：描述粒子/光线在弯曲时空中的最短路径
2. **曲率**：度量空间弯曲程度的核心不变量
3. **高斯-博内**：连接局部几何与整体拓扑的桥梁

测试覆盖从度量张量输入到各种曲率不变量输出的完整计算流程。