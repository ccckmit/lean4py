# 代數拓撲測試文檔 (test_algebraic_topology.py)

## 概述

本測試文件驗證 `lean4py/algebraic_topology.py` 模塊的核心功能，該模塊模擬 mathlib4 的 `Mathlib.AlgebraicTopology`。測試涵蓋基本群、同倫、同調群、貝蒂數等代數拓撲核心概念。

---

## 1. 測試驗證的代數拓撲內容

代數拓撲透過代數工具（如群、環、同態）研究拓撲空間的性質。本模塊專注於：

- **同倫論**：連續映射的同倫類別
- **同調論**：從鏈複形計算同調群
- **基本群**：基於閉路的拓撲不變量

---

## 2. 基本群測試 (FundamentalGroup)

### 測試用例

| 測試方法 | 測試內容 |
|---------|---------|
| `test_compute` | 計算基本群，返回群類型和生成元 |
| `test_is_trivial` | 判斷空間是否單連通 |

### 數學原理

**基本群 π₁(X, x₀)** 是拓撲空間 X 中基於點 x₀ 的閉路同倫類別組成的群。

- **單連通空間**：基本群為平凡群（僅含單位元）
- **S¹**：基本群為 ℤ（整數群）
- **S²**：基本群為平凡群

```python
space = [(0, 0), (1, 0), (0, 1)]  # 三角形（單連通）
result = FundamentalGroup.compute(space, (0, 0))
# result["group_type"] == "trivial"
```

---

## 3. 同倫群測試 (Homotopy)

### 測試用例

| 測試方法 | 測試內容 |
|---------|---------|
| `test_are_homotopic` | 判斷兩映射是否同倫 |
| `test_homotopy_class` | 返回映射的同倫類 |

### 數學原理

**同倫**：若兩連續映射 f, g: X → Y 存在連續變形，則 f ≃ g。

- 同倫是映射空間上的等價關係
- 同倫類別構成同倫群
- 恆等映射的同倫類別為 "identity"

```python
f = lambda x: x
g = lambda x: x
Homotopy.are_homotopic(f, g, [(0, 0)])  # True
Homotopy.homotopy_class(f)  # "identity"
```

---

## 4. 單形複形測試 (SimplicialComplex)

### 測試用例

| 測試方法 | 測試內容 |
|---------|---------|
| `test_creation` | 建立單形複形，驗證頂點數量 |
| `test_dimension` | 計算複形維數 |
| `test_euler_characteristic` | 計算歐拉示性數 |

### 數學原理

**單形複形 K** 是滿足以下條件的單形集合：
- 任意單形的面仍在複形中
- 兩單形的交集是它們的公共面

**維數**：複形中最大維單形的維數

**歐拉示性數**：
$$\chi(K) = \sum_{i=0}^{n} (-1)^i f_i$$

其中 f_i 為 i-單形的個數。

```python
vertices = [(0, 0), (1, 0), (0, 1)]
simplices = [[0, 1], [1, 2], [0, 2]]  # 三條邊
k = SimplicialComplex(vertices, simplices)
k.dimension()  # 1 (邊為1-單形)
k.euler_characteristic()  # 3 - 3 = 0
```

---

## 5. CW 複形測試 (CWComplex)

### 測試用例

| 測試方法 | 測試內容 |
|---------|---------|
| `test_build_sphere` | 建立 n 維球面的 CW 結構 |

### 數學原理

**CW 複形**：由黏合細胞構成的拓撲空間

- **骨架 (skeleton)**：n維骨架為 n 維以下細胞的並集
- **Sⁿ**：有 n+1 個細胞（0 細胞 + n 個 n 維細胞）

```python
result = CWComplex.build_sphere(2)
# result["skeleton"] == 2, result["cells"] == 3
```

---

## 6. 同調群測試 (Homology)

### 測試用例

| 測試方法 | 測試內容 |
|---------|---------|
| `test_compute` | 計算指定維數的同調群 |
| `test_is_trivial` | 判斷同調群是否平凡 |

### 數學原理

**同調群 Hₙ(X)**：從鏈複形計算

$$H_n(K) = \ker(\partial_n) / \operatorname{im}(\partial_{n+1})$$

- **0-同調群 H₀**：連通分量數量的自由 Abel 群
- **H₀ = 0** 表示無頂點
- **平凡同調群** 表示無 n 維「洞」

```python
vertices = [(0, 0), (1, 0)]
simplices = [[0], [1]]  # 兩個孤點
result = Homology.compute(k, 0)
# result["group"] == "0" (H₀ = 0 對兩個不連通點)
```

---

## 7. 貝蒂數測試 (BettiNumber)

### 測試用例

| 測試方法 | 測試內容 |
|---------|---------|
| `test_compute` | 計算所有維數的貝蒂數 |

### 數學原理

**貝蒂數 bₙ**：Hₙ 的 rank（自由部分）

$$b_n = \operatorname{rank}(H_n(X))$$

- **b₀**：連通分量數量
- **b₁**：一維「洞」的數量（如環面的洞）
- **b₂**：二維空洞數量

```python
vertices = [(0, 0), (1, 0)]
simplices = [[0], [1]]
k = SimplicialComplex(vertices, simplices)
BettiNumber.compute(k)  # [0, 0] (dim=1, 兩個分量)
```

---

## 測試覆蓋矩陣

| 類別 | compute | is_trivial | dimension | euler_characteristic |
|------|---------|------------|-----------|---------------------|
| FundamentalGroup | ✓ | ✓ | | |
| Homotopy | ✓ | | | |
| SimplicialComplex | | | ✓ | ✓ |
| CWComplex | ✓ | | | |
| Homology | ✓ | ✓ | | |
| BettiNumber | ✓ | | | |

---

## 數學術語對照

| 英文 | 中文 |
|-----|-----|
| Fundamental Group | 基本群 |
| Homotopy | 同倫 |
| Simplicial Complex | 單形複形 |
| CW Complex | CW 複形 |
| Homology | 同調 |
| Betti Number | 貝蒂數 |
| Euler Characteristic | 歐拉示性數 |
| Simply Connected | 單連通 |
| Chain Complex | 鏈複形 |
| Skeleton | 骨架 |