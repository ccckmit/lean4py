# 图论算法文档 (Graph Algorithms)

> 本文档解释 lean4py/graph_algorithms.py 模块中图算法的数学原理。

## 1. 图的表示方法 (Graph Representations)

### 1.1 邻接表 (Adjacency List)

邻接表是表示图的最常用方式，每个顶点维护一个列表存储其相邻顶点。

```
对于图 G = (V, E):
    Adj[u] = {v | (u,v) ∈ E}
```

**优点**: 节省空间，O(V+E) 复杂度遍历
**缺点**: 检查边是否存在需要 O(deg(u)) 时间

### 1.2 邻接矩阵 (Adjacency Matrix)

一个 V×V 的布尔矩阵 A，其中 A[i][j] = 1 当且仅当边 (i,j) 存在。

```
A[i][j] = { 1, 如果 (i,j) ∈ E
          { 0, 否则
```

**优点**: O(1) 时间检查边存在
**缺点**: O(V²) 空间复杂度

### 1.3 边列表 (Edge List)

简单列出所有边的集合：

```
E = {(u₁,v₁), (u₂,v₂), ..., (uₘ,vₘ)}
```

**优点**: 简单，空间复杂度 O(E)
**缺点**: 遍历邻居需要 O(E) 时间

---

## 2. 广度优先搜索 (BFS)

### 2.1 算法原理

BFS 从源点开始，按层次遍历图中所有可达顶点。

```python
BFS(G, s):
    for each v ∈ V:
        dist[v] = ∞
        parent[v] = nil
    dist[s] = 0
    Q = {s}
    while Q ≠ ∅:
        u = dequeue(Q)
        for each v ∈ Adj[u]:
            if dist[v] == ∞:
                dist[v] = dist[u] + 1
                parent[v] = u
                enqueue(Q, v)
```

**时间复杂度**: O(V + E)
**空间复杂度**: O(V)

### 2.2 BFS 的应用

1. **最短路径**: 在无权图中，BFS 提供从 s 到所有顶点的最短路径
2. **二分图检测**: 着色验证
3. **连通分量**: 分离图的连通分量
4. **网络爬虫**: 层序抓取网页

---

## 3. 深度优先搜索 (DFS) 与拓扑排序

### 3.1 DFS 算法原理

DFS 沿着一条路径走到底，然后回溯探索其他分支。

```python
DFS(G):
    for each v ∈ V:
        color[v] = WHITE
        parent[v] = nil
    time = 0
    for each v ∈ V:
        if color[v] == WHITE:
            DFS-Visit(v)

DFS-Visit(u):
    color[u] = GRAY
    time = time + 1
    d[u] = time
    for each v ∈ Adj[u]:
        if color[v] == WHITE:
            parent[v] = u
            DFS-Visit(v)
    color[u] = BLACK
    time = time + 1
    f[u] = time
```

**时间复杂度**: O(V + E)
**括号定理**: DFS 的发现时间和完成时间形成嵌套区间

### 3.2 拓扑排序

对于 DAG（有向无环图），拓扑排序是所有边的方向一致的顶点序列。

**Kahn 算法** (基于入度):
```python
L = []
in_degree[v] = 0 for all v
for each (u,v) ∈ E:
    in_degree[v]++

Q = {v | in_degree[v] == 0}
while Q ≠ ∅:
    v = dequeue(Q)
    L.append(v)
    for each u ∈ Adj[v]:
        in_degree[u]--
        if in_degree[u] == 0:
            enqueue(Q, u)
```

**DFS 方法**: 按完成时间的逆序输出顶点

**应用**:
- 课程安排
- 任务调度
- 依赖解析

---

## 4. Dijkstra 算法

### 4.1 算法原理

Dijkstra 算法在带非负权边的图中计算单源最短路径。

```python
Dijkstra(G, w, s):
    for each v ∈ V:
        dist[v] = ∞
        parent[v] = nil
    dist[s] = 0
    S = ∅
    Q = V (按 dist 值最小堆实现)
    while Q ≠ ∅:
        u = extract-min(Q)
        S = S ∪ {u}
        for each v ∈ Adj[u]:
            if dist[v] > dist[u] + w(u,v):
                dist[v] = dist[u] + w(u,v)
                parent[v] = u
```

### 4.2 正确性证明思路

**不变式**: 当顶点 u 被加入集合 S 时，dist[u] 是 s 到 u 的最短路径长度。

**证明**:
假设存在更短的路径 P，其第一个在 S 外发现的顶点为 x。
当 x 的前驱 y 被加入 S 时，会relax边 (y,x)。
由于所有边权非负，dist[y] ≤ dist[x]，最终矛盾。

### 4.3 复杂度分析

| 实现 | 时间复杂度 |
|------|-----------|
| 数组 | O(V²) |
| 二叉堆 | O((V+E) log V) |
| 斐波那契堆 | O(E + V log V) |

---

## 5. Bellman-Ford 算法

### 5.1 算法原理

处理可能存在负权边的单源最短路径问题，并检测负环。

```python
Bellman-Ford(G, w, s):
    for each v ∈ V:
        dist[v] = ∞
        parent[v] = nil
    dist[s] = 0
    for i = 1 to |V|-1:
        for each edge (u,v) ∈ E:
            if dist[v] > dist[u] + w(u,v):
                dist[v] = dist[u] + w(u,v)
                parent[v] = u
    for each edge (u,v) ∈ E:
        if dist[v] > dist[u] + w(u,v):
            return FALSE  # 存在负环
    return TRUE
```

### 5.2 负环检测

如果第 |V|-1 次迭代后仍能松弛边，则图中存在负环。
从该边起点可到达的所有顶点距离为 -∞。

**时间复杂度**: O(VE)

---

## 6. Floyd-Warshall 算法

### 6.1 算法原理

计算所有顶点对之间的最短路径。

```python
Floyd-Warshall(W):
    n = |V|
    D = W  # 初始距离矩阵
    for k in range(1, n+1):
        for i in range(1, n+1):
            for j in range(1, n+1):
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])
    return D
```

### 6.2 动态规划解释

令 d_ij^(k) 表示允许经过前 k 个顶点时的最短路径。

```
d_ij^(k) = min(d_ij^(k-1), d_ik^(k-1) + d_kj^(k-1))
```

**传递闭包**: 将 min 替换为 OR，+ 替换为 AND

**时间复杂度**: O(V³)
**空间优化**: 原地更新

---

## 7. 并查集 (Union-Find) 与环检测

### 7.1 并查集数据结构

支持两种操作：
- **Find(x)**: 找出元素 x 所属集合的代表
- **Union(x, y)**: 合并两个集合

### 7.2 路径压缩与按秩合并

```python
Find(x):
    if parent[x] ≠ x:
        parent[x] = Find(parent[x])  # 路径压缩
    return parent[x]

Union(x, y):
    rx = Find(x)
    ry = Find(y)
    if rx ≠ ry:
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx]++
```

**时间复杂度**: 几乎 O(α(n))，α 为 Ackermann 函数的反函数

### 7.3 环检测应用

无向图中，添加边 (u,v) 时：
- 如果 Find(u) == Find(v)，则存在环
- 否则，Union(u, v)

---

## 8. 强连通分量 (SCC)

### 8.1 Kosaraju 算法

**两遍 DFS** 方法：

```python
Kosaraju(G):
    # 第一遍: 计算完成时间
    visited = ∅
    finish_order = []
    DFS-1(s):
        visited.add(s)
        for each v ∈ Adj[s]:
            if v ∉ visited:
                DFS-1(v)
        finish_order.append(s)

    # 第二遍: 在转置图上按逆序遍历
    G_T = transpose(G)
    visited = ∅
    components = []
    for s in reversed(finish_order):
        if s ∉ visited:
            component = []
            DFS-2(s, component)
            components.append(component)

    return components
```

**时间复杂度**: O(V + E)

### 8.2 Tarjan 算法

**单遍 DFS** 方法，使用低链接值：

```python
Tarjan(G):
    index = 0
    S = []  # 栈
    on_stack = {}
    index = {}
    lowlink = {}
    sccs = []

    DFS(u):
        index[u] = index[v] = ++index
        lowlink[u] = index[u]
        S.push(u)
        on_stack[u] = True

        for each (u,v) ∈ E:
            if v not in index:
                DFS(v)
                lowlink[u] = min(lowlink[u], lowlink[v])
            elif on_stack[v]:
                lowlink[u] = min(lowlink[u], index[v])

        if lowlink[u] == index[u]:
            component = []
            repeat:
                w = S.pop()
                on_stack[w] = False
                component.append(w)
            until w == u
            sccs.append(component)

    for each u ∈ V:
        if u not in index:
            DFS(u)
```

**性质**: u 是 SCC 根当且仅当 lowlink[u] == index[u]

---

## 9. 最大流算法

### 9.1 基本概念

**网络**: 有向图 G = (V, E)，带源点 s 和汇点 t，每条边有容量 c(e) ≥ 0。

**流**: 函数 f: E → ℝ，满足：
1. **容量约束**: 0 ≤ f(e) ≤ c(e)
2. **流量守恒**: 对所有中间顶点，∑f(e_in) = ∑f(e_out)

**最大流问题**: 最大化从 s 到 t 的总流量 |f|。

### 9.2 Ford-Fulkerson 方法

**残存网络**: G_f 中，边 (u,v) 的容量为 c_f(u,v) = c(u,v) - f(u,v) + f(v,u)。

```python
Ford-Fulkerson(G, s, t):
    for each e ∈ E:
        f[e] = 0
    while exists path P in G_f from s to t:
        cf = min(c_f(e) for e in P)
        for each e ∈ P:
            if (u,v) ∈ E:
                f[u,v] += cf
            else:
                f[v,u] -= cf
    return f
```

**缺点**: 依赖增广路径选择，可能不终止于整数容量；时间复杂度 O(E·|f|*)

### 9.3 Edmonds-Karp 算法

使用 **BFS** 找增广路径（最短路径）。

**时间复杂度**: O(VE²)

### 9.4 Dinic 算法

**阻塞流** + **层次图** 方法：

```python
Dinic(G, s, t):
    max_flow = 0
    while BFS(s, t):
        level = BFS(s, t)
        while flow = blocking_flow(G, s, level):
            max_flow += flow
    return max_flow

blocking_flow(G, s, level):
    # 在层次图上发送尽可能多的流
```

**时间复杂度**: O(V²E)（一般），O(min(V^(2/3), E^(1/2))·E) 单位容量的特殊情况

### 9.5 Push-Relabel 算法

**前置-重贴标签** 算法更高效：

```python
gap heuristic: 如果某个高度值没有顶点，则所有高于该值的顶点高度+∞

relabel(u):
    h[u] = 1 + min{h[v] | (u,v) ∈ E_f}

push(u, v):
    delta = min(c_f(u,v), e[u])
    if u is the left side:
        f[u,v] += delta
    else:
        f[v,u] -= delta
```

**最高标记优先**: O(V³)
**FIFO**: O(V²E)

---

## 10. lean4py 实现类对应

| 类名 | 功能 |
|------|------|
| `GraphIsomorphism` | 图同构检测 |
| `Treewidth` | 树宽计算 (NP困难) |
| `PlanarGraph` | 平面图检测 (Euler公式, Kuratowski) |
| `EulerianCircuit` | 欧拉回路 (Hierholzer算法) |
| `HamiltonianCycle` | 哈密顿回路 (NP完全) |
| `GraphColoring` | 图着色 (染色数) |
| `Matching` | 最大匹配 |
| `VertexCover` | 顶点覆盖 (2-近似) |
| `NetworkFlow` | 最大流 (Ford-Fulkerson, Edmonds-Karp) |
| `GraphCentrality` | 中心性度量 (PageRank等) |

---

## 参考资料

1. Cormen, T. H., et al. *Introduction to Algorithms* (CLRS), 3rd Edition
2. Diestel, R. *Graph Theory*, 5th Edition
3. Tarjan, R. E. "Depth-First Search and Linear Graph Algorithms"
4. Edmonds, J. & Karp, R. M. "Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems"