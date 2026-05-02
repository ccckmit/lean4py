# 代數拓撲進階模組文檔

本文檔說明 `lean4py.algebraic_topology_advanced` 模組的數學原理。

## 1. 譜序列與同調計算（Serre 譜序列）

### 基本概念

譜序列（Spectral Sequence）是計算同調群的強大工具，由 Jean Leray 引入，後由 Serre 系統化。

**定義**：一個譜序列是餘鏈複形的過濾，其逐步逼近最終的同調。

對於任意纖維化 $F \rightarrow E \rightarrow B$，Serre 譜序列給出：

$$E^2_{p,q} = H_p(B; H_q(F)) \Rightarrow H_{p+q}(E)$$

### 代數拓撲實現

```python
class EilenbergMacLane:
    @staticmethod
    def classification(n: int) -> str:
        """[X, K(G, n)] ≅ Hⁿ(X; G)"""
        return f"H^{n}(X; G)"
```

這個分類定理是 Serre 譜序列的關鍵應用。Eilenberg-MacLane 空間 $K(G, n)$ 是譜序列計算的終點。

---

## 2. 向量叢與特徵類

### 向量叢

**定義**：向量叢是局部平凡的纖維化，其纖維為向量空間。

- 切叢 $TM$：流形 $M$ 的切空間
- 標架叢 $F(M)$：所有標架的空間

### 特徵類

特徵類是向量叢的整體不變量，測量叢的「扭曲」程度。

**重要的特徵類**：

| 特徵類 | 定義空間 | 取值 |
|--------|----------|------|
| Stiefel-Whitney 類 | $w_i \in H^i(X; \mathbb{Z}_2)$ | $\mathbb{Z}_2$ 係數 |
| Chern 類 | $c_i \in H^{2i}(X; \mathbb{Z})$ | 整係數 |
| Pontryagin 類 | $p_i \in H^{4i}(X; \mathbb{Z})$ | 整係數 |
| Euler 類 | $\chi \in H^n(X; \mathbb{Z})$ | 當定向叢時 |

---

## 3. 陳類（Chern Classes）

### 定義

對於複向量叢 $\xi \rightarrow X$，陳類 $c_i(\xi) \in H^{2i}(X; \mathbb{Z})$ 定義為：

1. **總陳類**：$c(\xi) = 1 + c_1 + c_2 + \cdots$
2. **可乘性**：$c(\xi \oplus \eta) = c(\xi) c(\eta)$
3. **法叢性質**：對於複化實向量叢 $c_1(\xi_{\mathbb{C}}) = 0$

### 性質

- $c_0 = 1$
- $c_i$ 限制於每點為第 $i$ 個 elementary symmetric polynomial
- **Whitney 求和公式**：$c(\xi \oplus \eta) = c(\xi) \cup c(\eta)$

---

## 4. Pontryagin 類

### 定義

實向量叢 $\xi$ 的 Pontryagin 類由複化定義：

$$p_i(\xi) = (-1)^i c_{2i}(\xi_{\mathbb{C}}) \in H^{4i}(X; \mathbb{Z})$$

### 性質

- $p_1(\xi) = c_1(\xi_{\mathbb{C}})^2$ 實際上
- Pontryagin 類測量實向量叢的定向無關扭曲

---

## 5. Euler 類

### 定義

對於定向實向量叢 $\xi \rightarrow X$，Euler 類 $\chi(\xi) \in H^n(X; \mathbb{Z})$ 是最高維特徵類。

### 幾何意義

- 當叢是切叢時，Euler 類即為流形的 Euler 示性數
- $\chi(M) = \int_M \chi(TM)$

---

## 6. Thom 同構

### 定理敘述

令 $\xi: E \rightarrow B$ 為定向向量叢，$i: B \hookrightarrow E$ 為零截面。則：

$$Ph^{-1}: H^*(E, E \setminus B) \cong H^{*-d}(B)$$

其中 $d$ 為叢的維數。

### 應用

- **Gysin 序列**：Thom 同構導出的長正合序列
- **配邊理論**：Thom 空間是配邊理論的核心

---

## 7. Steenrod 運算

### 定義

Steenrod 運算是 $\mathbb{Z}_2$ 係數上同調的額外代數結構：

$$Sq^i: H^n(X; \mathbb{Z}_2) \rightarrow H^{n+i}(X; \mathbb{Z}_2)$$

### 公理（Steenrod 公理）

1. **維數公理**：$Sq^0 = \text{id}$
2. **平方公式**：$Sq^k(x y) = \sum_{i+j=k} Sq^i(x) Sq^j(y)$
3. **自然性**：對連續映射 $f^* \circ Sq^i = Sq^i \circ f^*$
4. **懸崖公理**：$Sq^1$ 即為 Bockstein 同態

---

## 8. 高階同倫群

### 基本定義

$$\pi_n(X, x_0) = [S^n, X]_*$$

同倫群測量從 $n$ 維球面到 $X$ 的連續映射的變形類。

### 性質

```python
class HomotopyGroup:
    @staticmethod
    def is_abelian_for_n_ge_2(n: int) -> bool:
        """πₙ(X) is abelian for n ≥ 2."""
        return n >= 2
```

- $\pi_1$ 是群（非交換）
- $\pi_n$ ($n \geq 2$) 是交換群

### 同倫群的計算困難

大部分高階同倫群仍未知的，例如：
- $\pi_4(S^2) = \mathbb{Z}_2$
- $\pi_5(S^2) = \mathbb{Z}_2$
- $\pi_6(S^2) = \mathbb{Z}_{12}$

---

## 9. 球面的同倫群

### 穩定同倫群

球面同倫群隨維數增加呈現複雜模式。

**穩定化**：對於 $n \geq 2$：

$$\pi_{n+k}(S^n) \cong \pi_{n+k+1}(S^{n+1}) \cong \cdots$$

這個穩定化後的群稱為穩定同倫群 $\pi_k^s$。

### 穩定同倫群的週期性

Adams 譜序列揭示了穩定同倫群的週期性：

$$\pi_{2k}^s \cong \mathbb{Z}_2$$
$$\pi_{2k-1}^s \cong \mathbb{Z}_2 \text{ 對於 } k \geq 1$$

---

## 10. 穩定同倫理論

### 核心思想

穩定同倫論研究隨維數增加而穩定化的現象。

** suspension 同構**：

$$\Sigma: \pi_n(X) \rightarrow \pi_{n+1}(SX)$$

穩定化後：

$$\pi_n^{stable}(X) = \varinjlim_k \pi_{n+k}(S^k \wedge X)$$

### 譜與表示

穩定同倫類別於譜的同倫群：

- **MUS 譜**（Moore-Smith 收斂）：處理收斂性
- **環譜**：乘法結構（如 $MU$, $BP$, $K$ 理論）

---

## 11. 配邊理論（Cobordism Theory）

### 基本定義

**配邊**：兩個 $n$ 維流形 $M, N$ 若存在 $(n+1)$ 維流形 $W$ 使得 $\partial W = M \cup N$，則稱 $M$ 與 $N$ 配邊。

### 配邊環

- **Thom 配邊環** $\Omega_*^{O}$：未定向配邊
- **定向配邊環** $\Omega_*^{SO}$：帶定向結構
- **複配邊環** $\Omega_*^{U}$：複結構

### Pontryagin-Thom 構造

將配邊問題轉化為穩定同倫問題：

$$M \mapsto THH(M) = \text{Thom space of normal bundle}$$

---

## 與本模組的關聯

### FundamentalGroupoid

基本群胚 $\Pi_1(X)$ 是處理路徑同倫的代數工具：

```python
class CoveringSpace:
    @staticmethod
    def universal_cover(X: str) -> Dict[str, Any]:
        """Universal cover Ẋ → X (simplified)."""
        return {"cover": f"Ũ({X})", "is_simply_connected": True}
```

萬有覆蓋空間的存在性與基本群胚的平坦性密切相關。

### CW 複形

```python
class CellComplex:
    @staticmethod
    def build(cells: Dict[int, int]) -> Dict[str, Any]:
        """Build CW complex with cells (dimension → count)."""
        return {"type": "CW", "cells": cells, "euler": sum((-1)**d * c for d, c in cells.items())}
```

胞腔複形是進行同倫論計算的基礎工具。Euler 特徵數：

$$\chi(X) = \sum (-1)^i c_i$$

是 CW 複形的基本不變量。

### Eilenberg-MacLane 空間

```python
class EilenbergMacLane:
    @staticmethod
    def construct(G: str, n: int) -> Dict[str, Any]:
        """K(G, n) (simplified)."""
        return {"space": f"K({G}, {n})", "homotopy": f"π_{n} = {G}"}
```

$Eilenberg-MacLane$ 空間是同倫論的核心構造，用於分類上同調運算。

---

## 延伸閱讀

- Hatcher, A. - *Algebraic Topology*（第 5 章：同倫群，第 4 章：譜序列）
- Whitehead, G.W. - *Elements of Homotopy Theory*
- Adams, J.F. - *Stable Homotopy and Generalised Homology*
- Milnor, Stasheff - *Characteristic Classes*