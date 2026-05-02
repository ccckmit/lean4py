# 代數幾何 (Algebraic Geometry)

本文件說明 lean4py 代數幾何模組背後的數學原理。該模組實現了射影空間、代數曲線、除子、線叢以及 Riemann-Roch 定理等核心概念。

---

## 1. 仿射簇 (Affine Varieties)

### 定義
仿射簇是由一組多項式方程定義的集合：

$$V(I) = \{x \in k^n \mid f(x) = 0 \text{ for all } f \in I\}$$

其中 $I \subseteq k[x_1, \ldots, x_n]$ 是一個理想 (ideal)。

### 基本性質
- 若 $I = (f_1, \ldots, f_m)$，則 $V(I) = V(f_1) \cap \cdots \cap V(f_m)$
- $V(I)$ 稱為由理想 $I$ 定義的代數集

---

## 2. 理想與希爾伯特基底定理 (Ideals and Hilbert Basis Theorem)

### 理想 (Ideal)
- $I \subseteq k[x_1, \ldots, x_n]$ 是理想若滿足：
  - $0 \in I$
  - 若 $f, g \in I$，則 $f + g \in I$
  - 若 $f \in I$，$h \in k[x_1, \ldots, x_n]$，則 $hf \in I$

### 希爾伯特基底定理
**定理**：每個多項式環 $k[x_1, \ldots, x_n]$ 是 Noether 環，意即每個理想都是有限生成的。

這意味著每個仿射簇都可以由有限多個多項式方程定義。

### 根理想 (Radical Ideal)
$$\sqrt{I} = \{f \mid f^m \in I \text{ for some } m \geq 1\}$$

---

## 3. 坐標環 (Coordinate Ring)

### 定義
對於仿射簇 $V \subseteq k^n$，其坐標環為：

$$k[V] = k[x_1, \ldots, x_n] / I(V)$$

這是一個有限生成的 $k$-代數。

### 性質
- $k[V]$ 是整環當且僅當 $V$ 是不可約簇
- 坐標環中的元素可視為 $V$ 上的函數

---

## 4. Zariski 拓撲 (Zariski Topology)

### 定義
在仿射空間 $k^n$ 上，Zariski 拓撲的閉集為代數集：

$$\tau = \{V(I) \mid I \subseteq k[x_1, \ldots, x_n] \text{ 是理想}\}$$

### 性質
- Zariski 閉集是有限多個多項式方程的共同零點集
- 基本開集具有形式 $D(f) = \{x \in k^n \mid f(x) \neq 0\}$
- Zariski 拓撲不是 Hausdorff dorff，但它是 Noetherian

---

## 5. 射影簇 (Projective Varieties)

### 射影空間
$$\mathbb{P}^n = (k^{n+1} \setminus \{0\}) / k^* = \{[x_0 : x_1 : \cdots : x_n]\}$$

齊次坐標 $[x_0 : \cdots : x_n]$ 允許我們處理「無窮遠點」。

### 射影簇
射影簇是由齊次多項式定義的 $\mathbb{P}^n$ 子集：

$$V_{+}(I) = \{[x] \in \mathbb{P}^n \mid f(x) = 0 \text{ for all } f \in I\}$$

### 標準仿射覆蓋
$\mathbb{P}^n$ 可被 $n+1$ 個仿射空間覆蓋：
$$U_i = \{[x_0 : \cdots : x_n] \mid x_i \neq 0\} \cong \mathbb{A}^n$$

---

## 6. 希爾伯特零點定理 (Nullstellensatz)

### 弱零點定理
若 $k$ 是代數封閉域，$I \subseteq k[x_1, \ldots, x_n]$ 是理想，則：

$$V(I) = \emptyset \iff 1 \in I$$

### 強零點定理
對於代數封閉域上的理想：

$$I(V(I)) = \sqrt{I}$$

其中 $I(V) = \{f \in k[x_1, \ldots, x_n] \mid f(x) = 0 \text{ for all } x \in V\}$

### 推論
- 仿射簇與根基理想一一對應
- 不可約簇對應於素理想

---

## 7. 簇的維度 (Dimension of a Variety)

### 維度定義
簇 $V$ 的維度 $\dim V$ 是 $V$ 中最長鏈的長度：

$$\dim V = \sup \{r \mid V_0 \subsetneq V_1 \subsetneq \cdots \subsetneq V_r \subseteq V\}$$

### 計算方法
- $\dim k[V] = \dim V$（Krull 維度）
- 若 $V = V(I)$，則 $\dim V = \dim k[x]/ \sqrt{I}$
- 對於超曲面，$\dim V(I) = n - \dim I$

### 例子
- $\mathbb{A}^n$ 和 $\mathbb{P}^n$ 的維度為 $n$
- 曲線的維度為 1
- 曲面的維度為 2

---

## 8. 正則函數與有理映射 (Regular Functions and Rational Maps)

### 正則函數
在仿射簇 $V$ 的開集 $U$ 上，正則函數是局部有理函數：

$$\mathcal{O}_V(U) = \left\{\frac{f}{g} \mid f, g \in k[V], g \neq 0 \text{ on } U\right\}$$

### 有理映射
有理映射是定義在開集上的正則函數映射：

$$\phi: V \dashrightarrow W, \quad \phi = (\phi_1, \ldots, \phi_m)$$

其中每個 $\phi_i$ 是有理函數。

### 態射
若有理映射在處處有定義，則稱為態射 (morphism)。

---

## 9. 奇點與非奇點 (Singular and Nonsingular Points)

### 奇點定義
點 $P \in V$ 是奇點若局部環 $\mathcal{O}_{V,P}$ 不是正則局部環。

### 判別方法
對於超曲面 $V = V(f)$，點 $P$ 是奇點當且僅當：

$$\frac{\partial f}{\partial x_1}(P) = \frac{\partial f}{\partial x_2}(P) = \cdots = \frac{\partial f}{\partial x_n}(P) = 0$$

### 例子
- $y^2 = x^3$ 在原點有奇點（節點或尖點）
- $y^2 = x^3 + x$ 是光滑橢圓曲線（無奇點）

### 非奇點的重要性
- 非奇點簇是光滑流形
- 奇點理論在簇的分類中至關重要

---

## 模組實現摘要

本模組實現了以下核心類：

| 類名 | 數學對應 |
|------|----------|
| `ProjectiveSpace` | 射影空間 $\mathbb{P}^n$ |
| `AlgebraicCurve` | 代數曲線（虧格 $g$ 的光滑射影曲線） |
| `Divisor` | 除子 $D = \sum n_i P_i$ |
| `LineBundle` | 線叢/可逆層 |
| `EllipticCurve` | 橢圓曲線（虧格 1 的特殊曲線） |
| `Grassmannian` | 格拉斯曼流形 $Gr(k, n)$ |
| `blowing_up` | 爆發變換 |

### 關鍵定理
**Riemann-Roch 定理**：對於虧格 $g$ 的曲線 $C$ 和除子 $D$：

$$l(D) - l(K - D) = \deg(D) + 1 - g$$

其中 $K$ 是典範除子。

---

## 參考文獻

1. Hartshorne, R. (1977). *Algebraic Geometry*. Springer-Verlag.
2. Shafarevich, I. R. (1994). *Basic Algebraic Geometry*. Springer-Verlag.
3. Harris, J. (1995). *Algebraic Geometry: A First Course*. Springer-Verlag.