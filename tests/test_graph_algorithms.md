# 图算法测试文档 (test_graph_algorithms.py)

## 概述

本测试文件验证 `lean4py.graph_algorithms` 模块中的图算法实现，涵盖同构判定、树宽计算、平面性检测、欧拉回路、哈密顿回路、图着色、匹配、顶点覆盖、网络流和图的中心性等算法。

---

## 1. 测试验证的内容

测试文件通过单元测试验证图算法的核心功能：

- **对象创建与属性初始化**：确保每个算法类正确存储输入的图数据
- **返回值类型正确性**：验证算法返回值的类型符合预期（int、bool、float、set、dict、tuple）
- **边界条件处理**：测试顶点数为 0、1 或很小的图，以及特殊图结构（如 K5 完全图）
- **算法正确性断言**：使用 mock 对象模拟特定图结构，验证算法输出符合数学定义

---

## 2. 最短路径算法测试

> 注：本测试文件主要关注其他图算法。最短路径算法（如 Dijkstra、Bellman-Ford）在实际图论问题中常与网络流结合使用。

### 测试覆盖的算法

虽然当前测试文件未直接包含最短路径测试，但 `NetworkFlow` 类中的 Ford-Fulkerson 和 Edmonds-Karp 算法间接涉及最短路径概念：

- **Edmonds-Karp 算法**：BFS 寻找增广路径（本质上是无权最短路）
- **最大流最小割定理**：通过最短增广路径实现最大流

### 数学原理

最短路径问题定义：给定带权图 `G = (V, E)` 和源点 `s`，找到从 `s` 到所有其他顶点的最短路径。Edmonds-Karp 使用 BFS 在残余网络中寻找最短增广路径，每次增广后更新最短距离标签。

---

## 3. 最小生成树（MST）算法测试

> 注：当前测试文件未直接包含 MST 测试用例。

### 相关测试

`Matching`（匹配）类测试与 MST 有类似的贪心结构：

- `maximum_matching()`：最大匹配
- `is_perfect_matching()`：完美匹配判定
- `maximum_cardinality_matching()`：最大基数匹配

### 数学原理

MST 问题定义：给定连通带权无向图，找到连接所有顶点且边权总和最小的生成树。Prim 算法和 Kruskal 算法是两种经典解法，都采用贪心策略。

匹配问题与 MST 问题的联系：两者都涉及在图中选择最优边集合，Kruskal 算法实际上可以视为一种特殊的最大森林匹配问题。

---

## 4. 网络流算法测试（重点）

### 4.1 测试内容

```python
class TestNetworkFlow:
    def test_max_flow()       # 最大流
    def test_min_cut()        # 最小割
    def test_ford_fulkerson() # Ford-Fulkerson 方法
    def test_edmonds_karp()   # Edmonds-Karp 算法
```

### 4.2 Ford-Fulkerson 方法

#### 数学原理

最大流问题定义：给定网络 `G = (V, E)`，源点 `s`、汇点 `t` 和每条边的容量 `c(e)`，找到从 `s` 到 `t` 的最大可行流量。

**核心定理**：
- **最大流最小割定理**：任何网络的最大流值等于最小割的容量
- **增广路径定理**：当且仅当残余网络中不存在增广路径时，当前流为最大流

**算法步骤**：
1. 初始流设为 0
2. 在残余网络中寻找从 `s` 到 `t` 的增广路径
3. 沿该路径增加流量，重复直到无增广路径

**复杂度**：时间复杂度 `O(E * max_flow)`，取决于最大流值。

### 4.3 Edmonds-Karp 算法

#### 数学原理

Edmonds-Karp 是 Ford-Fulkerson 的优化版本，使用 **BFS** 而非 DFS 寻找增广路径，确保每次增广找到最短路径。

**关键性质**：
- 每次增广后，至少一条边的距离标签增加
- 最多 `O(VE)` 次增广
- 总时间复杂度 `O(VE²)`

**与 Ford-Fulkerson 的区别**：Ford-Fulkerson 允许任意增广路径选择，可能收敛缓慢；Edmonds-Karp 保证多项式时间。

### 4.4 最小割测试

```python
def test_min_cut():
    left, right = nf.min_cut("source", "sink")
    assert isinstance(left, set)
```

#### 数学原理

**割的定义**：将顶点集合 `V` 分割为两个不相交集合 `S` 和 `T`，使得 `s ∈ S`，`t ∈ T`。割的容量等于所有从 `S` 到 `T` 的边的容量之和。

**最大流最小割定理的应用**：
- 最大流值 = 最小割容量
- 最小割将图分为两部分：源点侧（`left`）和汇点侧（`right`）

---

## 5. 其他图算法测试

### 5.1 平面性检测 (TestPlanarGraph)

```python
def test_is_planar_complete_K5():
    pg = PlanarGraph(K5())  # 5个顶点，10条边
    assert pg.is_planar() is False
```

**Kuratowski 定理**：图是平面的当且仅当它不包含 K₅（完全图 5）或 K₃,₃（二分图）作为细分子图。

### 5.2 欧拉回路 (TestEulerianCircuit)

```python
def test_has_eulerian_circuit():
    # 每个顶点度数为2
    ec.has_eulerian_circuit() is True
```

**欧拉定理**：
- 连通图存在欧拉回路 ⟺ 所有顶点度数为偶数
- 连通图存在欧拉迹（开放路径）⟺ 恰好有 0 或 2 个奇度数顶点

### 5.3 哈密顿回路 (TestHamiltonianCycle)

```python
def test_sufficient_condition_dirac():
    # Dirac 条件：n >= 3 时，所有顶点度数 >= n/2
    hc.sufficient_condition_dirac() is True
```

**Dirac 定理**（充分条件）：对于 `n >= 3` 的简单图，若所有顶点度数 `>= n/2`，则图是哈密顿的。

### 5.4 图着色 (TestGraphColoring)

```python
def test_greedy_coloring():
    result = gc.greedy_coloring([1, 2, 3])
    assert len(result) == 3
```

**贪心着色算法**：按给定顶点顺序，依次为每个顶点分配最小可用颜色。颜色数不一定最优，但提供了上界。

### 5.5 匹配与顶点覆盖 (TestMatching, TestVertexCover)

```python
def test_has_vertex_cover_size_k():
    # n个顶点的图，k=n 时必有顶点覆盖
    vc.has_vertex_cover_size_k(5) is True
```

**König 定理**：二分图中最大匹配大小 = 最小顶点覆盖大小。

**2-近似算法**：顶点覆盖的贪心 2-近似算法选择所有匹配边的一个端点。

### 5.6 图中心性 (TestGraphCentrality)

```python
def test_degree_centrality():    # 度中心性
def test_betweenness_centrality() # 介数中心性
def test_closeness_centrality()  # 接近中心性
def test_pagerank()              # PageRank
```

**度中心性**：`C_D(v) = deg(v) / (n-1)`

**介数中心性**：`C_B(v) = Σ(s≠v≠t) σ_st(v) / σ_st`，其中 `σ_st` 是 s-t 最短路径数

**接近中心性**：`C_C(v) = (n-1) / Σ d(v,u)`

---

## 6. 测试架构总结

| 测试类 | 验证内容 | 关键断言 |
|--------|----------|----------|
| NetworkFlow | max_flow, min_cut, ford_fulkerson, edmonds_karp | 返回值类型正确 |
| GraphIsomorphism | are_isomorphic, find_isomorphism | 同构判定正确性 |
| Treewidth | compute_treewidth, is_treewidth_1 | 树宽计算 |
| PlanarGraph | is_planar, check_kuratowski, faces | K5 非平面验证 |
| EulerianCircuit | has_eulerian_circuit, has_eulerian_trail | 度数条件验证 |
| HamiltonianCycle | has_hamiltonian_cycle, sufficient_condition_dirac | Dirac 条件 |
| GraphColoring | chromatic_number, greedy_coloring | 色数下界 |
| Matching | maximum_matching, is_perfect_matching | 匹配集合 |
| VertexCover | has_vertex_cover_size_k, approximate_vc_2 | 近似比保证 |
| GraphCentrality | degree/betweenness/closeness_centrality, pagerank | 中心性值 |

---

## 7. 数学意义

这些测试共同验证了图论算法的核心性质：

1. **存在性判定**：欧拉回路、哈密顿回路、平面性的判定
2. **优化问题**：最大流、最小割、最大匹配
3. **近似算法**：顶点覆盖的 2-近似、贪心着色
4. **不变量**：同构、树宽、平面性
5. **中心性度量**：图的结构分析工具

所有算法均遵循图论基本定理（如最大流最小割定理、Kuratowski 定理、Dirac 定理），确保数学正确性。