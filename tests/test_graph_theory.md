# 圖論測試文檔 (test_graph_theory.py)

本文檔說明 `lean4py` 中圖論模組的測試案例及其背後的數學原理。

---

## 1. 測試驗證概述

測試案例涵蓋圖論的核心概念與算法，包括：
- 圖的結構與基本操作
- 圖的遍歷（遍歷與搜索）
- 連通性分析
- 最短路徑算法
- 圖的性質判定
- 高級圖算法

---

## 2. 圖結構測試 (TestGraphInit, TestGraphOperations)

### 2.1 圖的初始化

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
g = Graph(weighted_edges=[(1, 2, 3.0), (2, 3, 4.0)])
```

**數學原理：**
- **圖 (Graph)** 由頂點集 $V$ 和邊集 $E$ 組成
- **有權邊** 表示為三元組 $(u, v, w)$，其中 $w$ 為權重
- 圖可以是有向或無向

### 2.2 基本操作

| 操作 | 數學含義 |
|------|----------|
| `add_vertex(v)` | $V = V \cup \{v\}$ |
| `add_edge(u, v)` | $E = E \cup \{(u,v)\}$ |
| `remove_vertex(v)` | $V = V \setminus \{v\}$，同時移除所有與 $v$ 相關的邊 |
| `degree(v)` | 計算頂點 $v$ 的度（無向圖）或出度/入度（有向圖）|

### 2.3 有向圖的度

```python
g = Graph(vertices=[1, 2], edges=[(1, 2)], directed=True)
assert g.out_degree(1) == 1  # 出度：從該頂點指出的邊數
assert g.in_degree(2) == 1   # 入度：指向該頂點的邊數
```

**數學原理：**
- **出度 (out-degree)**：$d^+(v) = |\{(v, u) \in E\}|$（有向邊起點）
- **入度 (in-degree)**：$d^-(v) = |\{(u, v) \in E\}|$（有向邊終點）

---

## 3. 遍歷測試 (TestBFS, TestDFS)

### 3.1 廣度優先搜索 (BFS)

```python
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
result = bfs(g, 1)
assert result == [1, 2, 3, 4]
```

**數學原理：**
- BFS 使用**隊列 (Queue)** 數據結構
- 按「層級」遍歷：先訪問距離起點為 $d$ 的所有頂點，再訪問距離為 $d+1$ 的頂點
- 時間複雜度：$O(V + E)$
- **最短路徑性質**：在無權圖中，BFS 找到的路徑是最短路徑

### 3.2 深度優先搜索 (DFS)

```python
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
result = dfs(g, 1)
assert result == [1, 2, 3, 4]
```

**數學原理：**
- DFS 使用**棧 (Stack)** 或遞歸實現
- 沿着一條路徑深入直到盡頭，然後回溯
- 時間複雜度：$O(V + E)$
- 可用於：**環檢測、拓撲排序、連通分量**

### 3.3 離散圖遍歷

```python
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (3, 4)])
result = bfs(g, 1)
assert result == [1, 2]  # 只訪問與起點連通的部分
```

---

## 4. 連通性測試 (TestIsConnected, TestConnectedComponents)

### 4.1 連通性判定

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
assert is_connected(g)  # True

g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (3, 4)])
assert not is_connected(g)  # False
```

**數學原理：**
- **連通圖**：無向圖中，任意兩個頂點之間都存在路徑
- **連通分量 (Connected Component)**：極大的連通子圖
- 算法：使用 BFS/DFS 從任意頂點出發，能訪問到的所有頂點構成一個連通分量

### 4.2 連通分量計數

```python
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (3, 4)])
components = connected_components(g)
assert len(components) == 2
```

---

## 5. 最短路徑測試 (TestShortestPath, TestDijkstra, TestBellmanFord)

### 5.1 無權最短路徑

```python
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
result = shortest_path(g, 1, 4)
assert result == [1, 2, 3, 4]
```

**數學原理：**
- 在無權圖中，最短路徑 = 邊數最少的路徑
- 可用 BFS 直接計算

### 5.2 Dijkstra 算法

```python
g = Graph(weighted_edges=[(1, 2, 1.0), (2, 3, 2.0), (1, 3, 4.0)])
path, dist = dijkstra(g, 1, 3)
assert path == [1, 2, 3]
assert abs(dist - 3.0) < 1e-10
```

**數學原理：**
- 解決**單源最短路徑**問題（正權邊）
- 使用**優先隊列 (Min-Heap)** 優化
- 貪心算法：每次選擇當前距離最小的未處理頂點
- 時間複雜度：$O((V + E) \log V)$
- 正確性：基於「最優子結構」—— 最短路徑的子路徑也是最短路徑

### 5.3 Bellman-Ford 算法

```python
g = Graph(weighted_edges=[(1, 2, 1.0), (2, 3, 2.0)])
dist = bellman_ford(g, 1)
assert dist[1] == 0.0   # 源點距離為 0
assert dist[2] == 1.0   # 1→2 權重 1
assert dist[3] == 3.0   # 1→2→3 權重 1+2=3
```

**數學原理：**
- 動態規劃算法
- 迭代 $|V| - 1$ 次，每次對所有邊進行「鬆弛」操作
- 時間複雜度：$O(VE)$
- **可檢測負權環**：如果第 $|V|$ 次迭代仍能鬆弛，則存在負權環
- 適用於：**負權邊**場景

---

## 6. 圖性質測試 (TestIsBipartite, TestHasCycle, TestTopologicalSort)

### 6.1 二分圖判定

```python
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 3), (2, 4)])
assert is_bipartite(g)  # True

g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
assert not is_bipartite(g)  # False（包含奇環）
```

**數學原理：**
- **二分圖**：頂點集可劃分為兩個互不相交的集合 $V_1, V_2$，使得所有邊都連接 $V_1$ 中的頂點和 $V_2$ 中的頂點
- **奇環檢測**：如果圖包含長度為奇數的環，則不是二分圖
- 算法：BFS 著色 — 相鄰頂點着不同顏色，若發現衝突則非二分圖
- **應用**：匹配問題、工作分配、染色問題

### 6.2 環檢測

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
assert has_cycle(g)  # True

g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
assert not has_cycle(g)  # False
```

**數學原理：**
- **環**：起點和終點相同且長度 ≥ 3 的路徑
- 算法：DFS 期間如果遇到「訪問中」的頂點，則存在環
- 在有向圖中：使用三色標記（白、灰、黑）

### 6.3 拓撲排序

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (1, 3)], directed=True)
result = topological_sort(g)
assert result.index(1) < result.index(2)
assert result.index(1) < result.index(3)
```

**數學原理：**
- **拓撲排序**：有向無環圖 (DAG) 中所有頂點的一種線性排序
- 滿足：對於每條有向邊 $(u, v)$，$u$ 都在 $v$ 之前
- **DAG 判定定理**：有向圖有拓撲排序 ⟺ 圖是無環的
- 算法：Kahn 算法（使用入度隊列）或 DFS 後序逆序
- **應用**：任務調度、課程先修關係、構建依賴

---

## 7. 其他算法測試

### 7.1 歐拉路徑/迴路 (TestEulerian)

```python
# 三角形：所有頂點度數都為 2
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
result, type_ = is_eulerian(g)
assert result is True
assert type_ == "circuit"

# 路徑：1-2-3-4
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
result, type_ = is_eulerian(g)
assert result is True
assert type_ == "path"
```

**數學原理：**
- **歐拉迴路**：經過每條邊恰好一次的閉路徑
- **歐拉路徑**：經過每條邊恰好一次的開放路徑
- **歐拉定理（無向圖）**：
  - 歐拉迴路存在 ⟺ 圖連通且所有頂點度數為偶數
  - 歐拉路徑存在 ⟺ 圖連通且恰好有 0 或 2 個奇度頂點
- **應用**：一笔画问题、郵遞員問題、電路板走線

### 7.2 生成樹與最小生成樹 (TestSpanningTree, TestMST)

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (1, 3)])
tree = spanning_tree(g, 1)
assert len(tree.vertices) == len(g.vertices)

g = Graph(weighted_edges=[(1, 2, 1.0), (2, 3, 2.0), (1, 3, 5.0)])
mst = minimum_spanning_tree(g)
assert len(mst.vertices) == len(g.vertices)
```

**數學原理：**
- **生成樹 (Spanning Tree)**：包含圖中所有頂點的樹（無環连通子圖）
- **最小生成樹 (MST)**：邊權重之和最小的生成樹
- **MST 算法**：
  - **Kruskal**：貪心選擇最小邊，使用並查集檢測環
  - **Prim**：從某頂點出發，貪心擴展最小邊
- **應用**：網絡設計、電纜布線、聚類分析

### 7.3 完全圖判定 (TestIsComplete)

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (1, 3)])
assert is_complete(g)  # True

g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
assert not is_complete(g)  # False
```

**數學原理：**
- **完全圖 (Complete Graph)**：任意兩個不同頂點之間都有邊的圖
- 記為 $K_n$，其中 $n$ 是頂點數
- 邊數：$|E| = \frac{n(n-1)}{2}$（無向圖）

### 7.4 圖著色 (TestGraphColoring)

```python
# 二分圖 K2,2
g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 3), (1, 4), (2, 3), (2, 4)])
colors = graph_coloring(g)
assert len(set(colors.values())) <= 2  # 只需 2 色

# 完全圖 K3
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
colors = graph_coloring(g)
assert len(set(colors.values())) == 3  # 需要 3 色
```

**數學原理：**
- **圖著色**：為每個頂點分配顏色，相鄰頂點顏色不同
- **色數 (Chromatic Number)**：使著色有效的最少顏色數 $\chi(G)$
- **重要結論**：
  - 二分圖：$\chi(G) = 2$（除非是空圖或單一頂點）
  - 完全圖 $K_n$：$\chi(K_n) = n$
- **應用**：時間表排程、寄存器分配、航班調度

### 7.5 團 (TestGraphClique)

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
result = graph_clique(g)
assert len(result) == 3  # 三角形是一個 3-團
```

**數學原理：**
- **團 (Clique)**：圖中兩兩相鄰的頂點集合
- **最大團**：頂點數最多的團
- **團數 (Clique Number)** $\omega(G)$：最大團的頂點數
- **關係**：$\omega(G) = \chi(\overline{G})$（團數 = 補圖的色數）

### 7.6 補圖 (TestComplementGraph)

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2)])
comp = complement_graph(g)
# 補圖中原本不相連的頂點現在相連
```

**數學原理：**
- **補圖 $\overline{G}$**：包含原圖所有頂點，邊集為「原圖邊集的補」
- $(u, v) \in \overline{E} \iff (u, v) \notin E$（且 $u \neq v$）

### 7.7 哈密爾頓路徑 (TestHamiltonianPath)

```python
# 完全圖一定有哈密爾頓路徑
g = Graph(["A", "B", "C"])
g.add_edge("A", "B"); g.add_edge("B", "C"); g.add_edge("A", "C")
assert has_hamiltonian_path(g) == True

# 線圖（路徑圖）沒有哈密爾頓路徑
g = Graph([1, 2, 3, 4])
for i in range(3):
    g.add_edge(i+1, i+2)
assert has_hamiltonian_path(g) == False
```

**數學原理：**
- **哈密爾頓路徑**：經過每個頂點恰好一次的路徑
- **哈密爾頓迴路**：經過每個頂點恰好一次的閉路徑
- **Dirac 定理（充分條件）**：對於 $n \geq 3$ 的簡單圖，如果每個頂點度數 $\geq n/2$，則存在哈密爾頓迴路
- **Ore 定理（充分條件）**：對於 $n \geq 3$，如果對每對不相鄰頂點 $u, v$，都有 $deg(u) + deg(v) \geq n$，則存在哈密爾頓迴路
- **NP-完全問題**：目前沒有已知的多項式時間算法

---

## 8. 鄰接表與鄰接矩陣 (TestAdjacency)

```python
g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
adj = adjacency_list(g)
assert 1 in adj[2]
assert 3 in adj[2]

vertices, matrix = adjacency_matrix(g)
assert matrix[0][1] == 1  # 頂點 1 和 2 相鄰
assert matrix[1][0] == 1  # 對稱矩陣（無向圖）
```

**數學原理：**
- **鄰接表**：對每個頂點存儲其相鄰頂點列表
  - 空間：$O(V + E)$
  - 適用於：稀疏圖
- **鄰接矩陣**：$n \times n$ 矩陣 $A$，$A_{ij} = 1$ 如果 $(i,j) \in E$
  - 空間：$O(V^2)$
  - 適用於：稠密圖、O(1) 鄰接查詢

---

## 9. 測試覆蓋總結

| 類別 | 測試內容 | 核心算法/概念 |
|------|----------|---------------|
| 結構 | 頂點、邊、加權邊、有向/無向 | 圖的表示 |
| 操作 | 添加/刪除頂點邊、度數計算 | 基本變動 |
| 遍歷 | BFS、DFS | 隊列/棧實現 |
| 連通性 | 連通判定、連通分量 | BFS/DFS |
| 最短路徑 | Dijkstra、Bellman-Ford | 貪心/動態規劃 |
| 圖性質 | 二分圖、環檢測、拓撲排序 | 著色/DFS |
| 高級算法 | 歐拉路徑、生成樹、MST、圖著色、團、哈密爾頓路徑 | 各種圖算法 |

---

## 10. 數學術語對照表

| 英文 | 中文 |
|------|------|
| Graph | 圖 |
| Vertex / Node | 頂點 / 節點 |
| Edge | 邊 |
| Directed | 有向 |
| Undirected | 無向 |
| Weighted | 加權 |
| Degree | 度數 |
| BFS (Breadth-First Search) | 廣度優先搜索 |
| DFS (Depth-First Search) | 深度優先搜索 |
| Connected | 連通 |
| Connected Component | 連通分量 |
| Shortest Path | 最短路徑 |
| Dijkstra Algorithm | Dijkstra 算法 |
| Bellman-Ford Algorithm | Bellman-Ford 算法 |
| Bipartite Graph | 二分圖 |
| Cycle | 環 |
| Topological Sort | 拓撲排序 |
| Eulerian Path / Circuit | 歐拉路徑 / 迴路 |
| Spanning Tree | 生成樹 |
| Minimum Spanning Tree (MST) | 最小生成樹 |
| Complete Graph | 完全圖 |
| Graph Coloring | 圖著色 |
| Clique | 團 |
| Hamiltonian Path | 哈密爾頓路徑 |
| Adjacency List | 鄰接表 |
| Adjacency Matrix | 鄰接矩陣 |