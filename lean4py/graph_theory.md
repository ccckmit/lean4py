# 圖論模組 (graph_theory.py) 數學原理文檔

本文件解釋 `lean4py/graph_theory.py` 模組中實現的圖論算法的數學原理。

---

## 1. 圖的基本定義 G = (V, E)

圖是由頂點集合 V（Vertices）和邊集合 E（Edges）組成的數學結構，記作 **G = (V, E)**。

- **頂點（Vertex）**：圖中的基本元素，代表討論的對象。在本模組中，`Vertex` 類封裝頂點ID和可選的附加數據。
- **邊（Edge）**：連接兩個頂點的線段，記作 (u, v)，表示從頂點 u 到頂點 v 的連接。
- **度（Degree）**：與頂點相連的邊數。對於無向圖，入度等於出度等於度。

```python
class Vertex:
    def __init__(self, id: Any, data: Optional[Any] = None):
        self.id = id
        self.data = data

class Edge:
    def __init__(self, u: Any, v: Any, weight: float = 1.0):
        self.u = u
        self.v = v
        self.weight = weight
```

---

## 2. 有向圖與無向圖

### 無向圖（Undirected Graph）
- 邊沒有方向性，(u, v) 等價於 (v, u)
- 添加邊時自動雙向添加：`adjacency[u].add(v)` 且 `adjacency[v].add(u)`

### 有向圖（Directed Graph / Digraph）
- 邊具有方向性，(u, v) 表示從 u 指向 v 的弧
- 僅添加單向連接：`adjacency[u].add(v)`

```python
def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
    self.add_vertex(u)
    self.add_vertex(v)
    self.adjacency[u].add(v)
    self.weights[(u, v)] = weight
    if not self.directed:
        self.adjacency[v].add(u)
        self.weights[(v, u)] = weight
```

---

## 3. 加權圖（Weighted Graph）

邊具有權重值，用於表示距離、成本、容量等度量。

- 默認權重為 1.0
- 權重存儲在 `weights` 字典中，鍵為 (u, v) 元組

```python
def dijkstra(g: Graph, start: Any, end: Any) -> Optional[Tuple[List[Any], float]]:
    # ...
    for neighbor in g.neighbors(v):
        weight = g.weights.get((v, neighbor), 1.0)  # 獲取邊權重
        alt = dist + weight
```

---

## 4. 圖的表示方法

### 4.1 鄰接表（Adjacency List）

每個頂點維護一個列表，存儲與其相鄰的所有頂點。

**數學定義**：對於每個頂點 v ∈ V，adjacency[v] = {u | (v, u) ∈ E}

```python
def adjacency_list(g: Graph) -> Dict[Any, List[Any]]:
    return {v: list(g.neighbors(v)) for v in g.vertices}
```

**空間複雜度**：O(V + E)

### 4.2 鄰接矩陣（Adjacency Matrix）

一個 n × n 的矩陣 M，其中 M[i][j] = 1 當且僅當 (v_i, v_j) ∈ E。

```python
def adjacency_matrix(g: Graph) -> Tuple[List[Any], List[List[int]]]:
    vertices = list(g.vertices)
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    matrix = [[0] * n for _ in range(n)]
    for u in g.vertices:
        for v in g.neighbors(u):
            matrix[idx[u]][idx[v]] = 1
    return vertices, matrix
```

**空間複雜度**：O(V²)

---

## 5. 圖遍歷算法

### 5.1 廣度優先搜索（BFS - Breadth-First Search）

**原理**：使用佇列（Queue）實現，先訪問距離起點較近的頂點，再訪問較遠的頂點。

**數學性質**：
- 從起點到任意頂點的路徑是最短路徑（邊數最少）
- 時間複雜度：O(V + E)

```python
def bfs(g: Graph, start: Any) -> List[Any]:
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        v = queue.popleft()
        if v not in visited:
            visited.add(v)
            result.append(v)
            for neighbor in g.neighbors(v):
                if neighbor not in visited:
                    queue.append(neighbor)

    return result
```

### 5.2 深度優先搜索（DFS - Depth-First Search）

**原理**：使用堆疊（Stack）或遞歸實現，沿着分支深入直到無法繼續再回溯。

**時間複雜度**：O(V + E)

```python
def dfs(g: Graph, start: Any) -> List[Any]:
    visited = set()
    result = []

    def dfs_rec(v):
        visited.add(v)
        result.append(v)
        for neighbor in g.neighbors(v):
            if neighbor not in visited:
                dfs_rec(neighbor)

    dfs_rec(start)
    return result
```

---

## 6. 最短路徑算法

### 6.1 Dijkstra 算法

**適用條件**：邊權重非負的有向或無向圖

**原理**：
1. 維護距離字典 `distances`，初始為無窮大，起點為 0
2. 使用最小優先隊列（堆）選擇當前未訪問頂點中距離最小的
3. 鬆弛（Relaxation）：若通過中間頂點路徑更短，則更新距離

**數學表述**：
```
dist(v) = min(dist(u) + w(u,v))，對所有 u ∈ V
```

**時間複雜度**：O((V + E) log V)（使用二叉堆）

```python
def dijkstra(g: Graph, start: Any, end: Any) -> Optional[Tuple[List[Any], float]]:
    distances = {v: float('inf') for v in g.vertices}
    distances[start] = 0
    previous = {v: None for v in g.vertices}
    pq = [(0, start)]

    while pq:
        dist, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)

        for neighbor in g.neighbors(v):
            weight = g.weights.get((v, neighbor), 1.0)
            alt = dist + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = v
                heapq.heappush(pq, (alt, neighbor))
```

### 6.2 Bellman-Ford 算法

**適用條件**：可以處理負權邊，檢測負權環

**原理**：
- 對所有邊進行 V-1 次鬆弛操作
- 第 V-1 次迭代後，若仍能更新距離，則存在負權環

**時間複雜度**：O(VE)

```python
def bellman_ford(g: Graph, start: Any) -> Optional[Dict[Any, float]]:
    distances = {v: float('inf') for v in g.vertices}
    distances[start] = 0

    for _ in range(len(g.vertices) - 1):
        for u in g.vertices:
            for v in g.neighbors(u):
                weight = g.weights.get((u, v), 1.0)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    # 檢測負權環
    for u in g.vertices:
        for v in g.neighbors(u):
            weight = g.weights.get((u, v), 1.0)
            if distances[u] + weight < distances[v]:
                return None  # 存在負權環

    return distances
```

---

## 7. 圖的性質判定

### 7.1 連通性（Connected）

**定義**：在無向圖中，任意兩個頂點間都存在路徑。

**算法**：從任意頂點開始 DFS/BFS，若能訪問所有頂點則連通。

```python
def is_connected(g: Graph) -> bool:
    if not g.vertices:
        return True
    start = next(iter(g.vertices))
    visited = set()
    stack = [start]
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            stack.extend(g.neighbors(v) - visited)
    return len(visited) == len(g.vertices)
```

### 7.2 二分圖（Bipartite）

**定義**：圖的頂點可以分為兩個互不相交的集合，使得每條邊都連接兩個不同集合的頂點。

**充分必要條件**：圖不包含奇數長度的環。

**算法**：BFS 染色法，用兩種顏色交替給相鄰頂點染色，若衝突則非二分圖。

```python
def is_bipartite(g: Graph) -> bool:
    color = {}
    queue = deque([next(iter(g.vertices))])
    color[queue[0]] = 0

    while queue:
        v = queue.popleft()
        for neighbor in g.neighbors(v):
            if neighbor not in color:
                color[neighbor] = 1 - color[v]
                queue.append(neighbor)
            elif color[neighbor] == color[v]:
                return False
    return True
```

### 7.3 環檢測（Cycle Detection）

**原理**：DFS 過程中維護遞歸棧（rec_stack），若發現相鄰頂點在棧中且非父節點，則存在環。

```python
def has_cycle(g: Graph) -> bool:
    visited = set()
    rec_stack = set()

    def dfs_cycle(v, parent=None):
        visited.add(v)
        rec_stack.add(v)
        for neighbor in g.neighbors(v):
            if neighbor not in visited:
                if dfs_cycle(neighbor, v):
                    return True
            elif neighbor in rec_stack and neighbor != parent:
                return True
        rec_stack.remove(v)
        return False

    for v in g.vertices:
        if v not in visited:
            if dfs_cycle(v):
                return True
    return False
```

---

## 8. 拓撲排序（Topological Sort）與 Kahn 算法

**適用條件**：有向無環圖（DAG）

**定義**：對有向圖的頂點線性排序，使得對於每條有向邊 (u, v)，u 都在 v 之前。

**Kahn算法原理**：
1. 計算所有頂點的入度
2. 將入度為 0 的頂點加入隊列（這些頂點沒有前置依賴）
3. 不斷取出隊列中的頂點，將其從圖中移除，更新相鄰頂點的入度
4. 若最終所有頂點都被移除，則存在拓撲排序；否則圖中有環

```python
def topological_sort(g: Graph) -> Optional[List[Any]]:
    if g.directed:
        in_degree = {v: g.in_degree(v) for v in g.vertices}
        queue = deque([v for v in g.vertices if in_degree[v] == 0])
        result = []

        while queue:
            v = queue.popleft()
            result.append(v)
            for neighbor in g.neighbors(v):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(g.vertices):
            return None
        return result
    return None
```

---

## 9. 歐拉路徑/迴路（Eulerian Path/Circuit）

**定義**：
- **歐拉迴路**：遍歷每一條邊恰好一次並返回起點
- **歐拉路徑**：遍歷每一條邊恰好一次，但不必返回起點

**必要充分條件**：
- 連通（忽略孤立頂點）
- **歐拉迴路**：所有頂點度均為偶數（0 或 2 個奇度頂點的結論針對路徑）
- **歐拉路徑**：恰好有 0 或 2 個奇度頂點

**本模組中的條件檢查**：
```python
def eulerian_path(g: Graph) -> Optional[List[Any]]:
    odd_degree = [v for v in g.vertices if g.degree(v) % 2 == 1]
    if len(odd_degree) not in [0, 2]:
        return None  # 必要條件：0 或 2 個奇度頂點
```

**Hierholzer 算法**：使用堆疊模擬 Fleury 算法，時間複雜度 O(V + E)。

---

## 10. 生成樹與最小生成樹

### 10.1 生成樹（Spanning Tree）

**定義**：包含圖中所有頂點的無環連通子圖。

```python
def spanning_tree(g: Graph, start: Optional[Any] = None) -> Optional[Graph]:
    visited = set()
    edges = []
    stack = [start]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        for neighbor in g.neighbors(v):
            if neighbor not in visited:
                w = g.weights.get((v, neighbor), 1.0)
                edges.append((v, neighbor, w))
                stack.append(neighbor)
```

### 10.2 最小生成樹（Minimum Spanning Tree, MST）

**定義**：在加權無向圖中，邊權重之和最小的生成樹。

**Prim 算法思想**（本模組採用）：
1. 從任意頂點開始
2. 維護已訪問頂點集合，將與集合相鄰的最小權邊加入
3. 重複直到包含所有頂點

```python
def minimum_spanning_tree(g: Graph) -> Optional[Graph]:
    visited = set()
    edges = []
    start = next(iter(g.vertices))
    visited.add(start)
    edge_heap = [(g.weights.get((start, v), 1.0), start, v) for v in g.neighbors(start)]

    while edge_heap and len(visited) < len(g.vertices):
        weight, u, v = heapq.heappop(edge_heap)
        if v in visited:
            continue
        visited.add(v)
        edges.append((u, v, weight))
        for neighbor in g.neighbors(v):
            if neighbor not in visited:
                w = g.weights.get((v, neighbor), 1.0)
                heapq.heappush(edge_heap, (w, v, neighbor))

    return Graph(vertices=list(g.vertices), weighted_edges=edges, directed=g.directed)
```

**時間複雜度**：O((V + E) log V)

---

## 11. 圖著色（Graph Coloring）

**定義**：為每個頂點分配顏色，使得相鄰頂點顏色不同。

**貪心算法策略**：
1. 按任意順序遍歷頂點
2. 對於每個頂點，選擇當前相鄰頂點未使用的最小顏色編號

```python
def graph_coloring(g: Graph, strategy: str = 'greedy') -> Dict[Any, int]:
    colors = {}
    for v in g.vertices:
        neighbor_colors = {colors.get(n) for n in g.neighbors(v) if n in colors}
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[v] = color
    return colors
```

**注意**：貪心算法不保證使用最少顏色，但對順序足夠好的圖可以使用 Δ+1 種顏色（Δ 為最大度）。

---

## 12. 團（Clique）與 Bron–Kerbosch 算法

**定義**：團是圖中的一個頂點集合，集合內任意兩個頂點都有邊相連（即完全子圖）。

**Bron–Kerbosch 算法**：基於回溯的極大團枚舉算法。

**算法思想**：
- 維護三個集合：R（當前團）、P（候選頂點）、X（排除頂點）
- 若 P 和 X 都為空，則 R 是極大團
- 递归擴展 R，並從 P 中移除已訪問頂點

```python
def bron_kerbosch(r: set, p: set, x: set) -> set:
    if not p and not x:
        return r
    max_clique = set()
    for v in list(p):
        new_r = r | {v}
        new_p = p & g.neighbors(v)
        new_x = x & g.neighbors(v)
        clique = bron_kerbosch(new_r, new_p, new_x)
        if len(clique) > len(max_clique):
            max_clique = clique
        p = p - {v}
        x = x | {v}
    return max_clique
```

**時間複雜度**：在最壞情況下為 O(3^(V/3))，但實際通常快得多。

---

## 13. 最大流 / 最小割（Max Flow / Min Cut）

### 13.1 Ford-Fulkerson 方法

**最大流問題**：在網絡中找到從源點到匯點的最大可能流量。

**殘留網絡**：包含原始邊的剩餘容量和反向邊。

**增廣路徑**：從源到匯的，路徑上所有邊的剩餘容量都大於 0 的路徑。

```python
def max_flow(g: Graph, source: Any, sink: Any) -> Tuple[float, Graph]:
    residual = Graph(g.vertices, directed=True)
    # 初始化殘留網絡
    for u in g.vertices:
        for v in g.adjacency.get(u, set()):
            cap = g.weights.get((u, v), 1.0)
            residual.weights[(u, v)] = cap

    while True:
        parent = {}
        queue = deque([source])
        parent[source] = None

        # BFS 找增廣路徑
        while queue:
            u = queue.popleft()
            if u == sink:
                break
            for v in residual.adjacency.get(u, set()):
                cap = residual.weights.get((u, v), 0.0)
                if cap > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            break  # 沒有增廣路徑

        # 找瓶頸容量
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            cap = residual.weights.get((u, v), 0.0)
            path_flow = min(path_flow, cap)
            v = u

        # 更新殘留容量
        v = sink
        while v != source:
            u = parent[v]
            residual.weights[(u, v)] -= path_flow
            residual.weights[(v, u)] += path_flow
            v = u

        total_flow += path_flow

    return total_flow, residual
```

**時間複雜度**：O(E · f)，其中 f 是最大流量。使用 BFS 尋找增廣路徑稱為 Edmonds-Karp 算法，時間複雜度 O(VE²)。

### 13.2 最小割定理

**最大流最小割定理**：網絡中的最大流量等於最小割的容量。

**最小割求法**：在最大流計算完成後，在殘留網絡中從源點出發可達的所有頂點構成集合 S，其餘頂點構成集合 T，(S, T) 即為最小割。

```python
def min_cut(g: Graph, source: Any, sink: Any) -> Tuple[float, set, set]:
    flow_value, residual = max_flow(g, source, sink)

    visited = set()
    queue = deque([source])

    # 在殘留網絡中找可達頂點
    while queue:
        u = queue.popleft()
        if u in visited:
            continue
        visited.add(u)
        for v in residual.adjacency.get(u, set()):
            cap = residual.weights.get((u, v), 0.0)
            if cap > 0 and v not in visited:
                queue.append(v)

    S = visited
    T = set(g.vertices) - S

    return flow_value, S, T
```

---

## 14. 哈密爾頓路徑與 Dirac 定理

**哈密爾頓路徑**：經過每個頂點恰好一次的路徑。

**哈密爾頓迴路**：經過每個頂點恰好一次並返回起點的環。

**Dirac 定理（1952年）**：

若圖 G 有 n ≥ 3 個頂點，且對於所有頂點 v，都有 deg(v) ≥ n/2，則圖 G 存在哈密爾頓迴路（因此也存在哈密爾頓路徑）。

**注意**：這是**充分條件**，不是必要條件。

```python
def has_hamiltonian_path(g: Graph) -> bool:
    n = len(g.vertices)
    if n < 2:
        return True
    # Dirac 條件：所有頂點度 >= n/2
    for v in g.vertices:
        if g.degree(v) < n / 2:
            return False
    return True
```

---

## 附錄：算法複雜度總結

| 算法/操作 | 時間複雜度 | 空間複雜度 |
|-----------|-----------|-----------|
| BFS/DFS | O(V + E) | O(V) |
| Dijkstra | O((V + E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| 拓撲排序 | O(V + E) | O(V) |
| 最小生成樹 | O((V + E) log V) | O(V) |
| Bron–Kerbosch | O(3^(V/3)) | O(V) |
| 最大流 (Edmonds-Karp) | O(VE²) | O(E) |
| 圖著色（貪心） | O(VE) | O(V) |
| 歐拉路徑 | O(V + E) | O(V) |

---

*文檔基於 lean4py v1.34.0 版本的 graph_theory.py 模組生成*