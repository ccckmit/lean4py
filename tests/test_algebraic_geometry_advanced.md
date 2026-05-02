# 代數幾何進階測試文檔

## 概述

本測試文件 (`test_algebraic_geometry_advanced.py`) 驗證 `lean4py.algebraic_geometry_advanced` 模組的核心功能，該模組模仿 mathlib4 的 `Mathlib.AlgebraicGeometry`，涵蓋除子、線叢、黎曼-羅赫定理等進階代數幾何概念。

---

## 1. 除子 (Divisor) 測試

### 數學原理

**除子**是代數幾何中的基本概念。設 $C$ 為一條射影曲線，則除子 $D$ 是 $C$ 上有限個點的線性組合：

$$D = \sum_{P \in C} n_P \cdot P$$

其中係數 $n_P \in \mathbb{Z}$。除子的**次數** (degree) 定義為所有係數之和：

$$\deg(D) = \sum_{P \in C} n_P$$

### 測試驗證內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 檢查除子創建是否正確計算次數 |
| `test_is_effective` | 有效除子 ($n_P \geq 0$) 的判定 |

```python
D = Divisor({"P1": 1, "P2": -1})
D.degree()  # 返回 0
D.is_effective()  # True 當所有係數 >= 0
```

---

## 2. 線叢 (LineBundle) 測試

### 數學原理

**線叢** $L$ 是曲線上的扭元層，其與除子緊密相關。给定除子 $D$，可以構造**典範層**：

$$\mathcal{O}_C(D) = \{ f \in K(C)^* \mid (f) + D \geq 0 \} \cup \{0\}$$

兩個線叢 $L_1, L_2$ 同構當且僅當它們的次數相等：

$$L_1 \cong L_2 \iff \deg(L_1) = \deg(L_2)$$

### 測試驗證內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_from_divisor` | 從除子構造線叢 $\mathcal{O}(D)$ |
| `test_is_isomorphic` | 線叢同構判定（次數相同則同構）|

---

## 3. 黎曼-羅赫定理 (Riemann-Roch) 測試

### 數學原理

黎曼-羅赫定理是曲線理論的核心結果。對於 genus 為 $g$ 的射影曲線 $C$ 上的除子 $D$：

$$l(D) = \deg(D) + 1 - g + l(K - D)$$

其中：
- $l(D) = \dim H^0(C, \mathcal{O}_C(D))$ 是線叢 $\mathcal{O}(D)$ 的整體截面空間維數
- $K$ 是**典範除子** (canonical divisor)
- $K - D$ 是除子的減法

當 $D$ 為有效除子且 $\deg(D) > 2g - 2$ 時，有 $l(K - D) = 0$，此時：

$$l(D) = \deg(D) + 1 - g$$

### 測試驗證內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_compute` | 計算 $l(D)$ 的近似值 |
| `test_holds` | 驗證黎曼-羅赫定理的成立 |

---

## 4.  genus (虧格) 測試

### 數學原理

**虧格** $g$ 是曲線的拓撲不變量，描述曲線的「孔洞數」。

對於平面射影曲線 $C \subset \mathbb{P}^2$，若其次數為 $d$，則 genus 為：

$$g = \frac{(d-1)(d-2)}{2}$$

這是 genus 公式的特殊情況。

### 測試驗證內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_of_curve` | 計算光滑平面曲線的 genus |
| `test_of_riemann_surface` | 黎曼曲面 genus 的確定 |

---

## 5. 典範除子 (Canonical Divisor) 測試

### 數學原理

**典範除子** $K$ 是曲線上微分 1-形式的除子。它具有重要性質：

1. **次數公式**：$\deg(K) = 2g - 2$
2. **Clifford 定理**：對於特殊除子 $D$，$l(K - D) \geq 0$

典範除子在黎曼-羅赫定理中扮演核心角色，是連接幾何與拓撲的橋樑。

### 測試驗證內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_compute` | 構造 genus $g$ 曲線的典範除子 |
| `test_degree` | 驗證 $\deg(K) = 2g - 2$ |

---

## 測試覆蓋範圍圖

```
algebraic_geometry_advanced
├── Divisor (除子)
│   ├── degree() → deg(D)
│   └── is_effective() → n_P ≥ 0
├── LineBundle (線叢)
│   ├── from_divisor(D) → O(D)
│   └── is_isomorphic(L1, L2) → deg(L1) = deg(L2)
├── RiemannRoch (黎曼-羅赫)
│   ├── compute(D, g) → l(D) = max(0, deg(D) + 1 - g)
│   └── holds(D, g) → True
├── Genus (虧格)
│   ├── of_curve(d) → (d-1)(d-2)/2
│   └── of_riemann_surface(g) → g
└── CanonicalDivisor (典範除子)
    ├── compute(g) → K
    └── degree(g) → 2g - 2
```

---

## 數學意義

這些測試驗證了代數幾何中幾個核心概念：

1. **除子**提供了解析函數零點與極點的代數描述
2. **線叢**是幾何與代數之間的接口
3. **黎曼-羅赫定理**連接了除子的次數與其截面空間維數
4. **虧格**刻畫了曲線的複雜度
5. **典範除子**是曲線的內在幾何不變量

這些概念共同構成了現代代數幾何的基礎框架，廣泛應用於數論、複幾何與數學物理中。