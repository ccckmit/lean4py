# 算子代數 (Operator Algebras)

本模組提供 C*-代數、馮·諾伊曼代數以及 K-理論的數學基礎。

## 1. 賦範代數與巴納赫代數 (Normed Algebras and Banach Algebras)

### 賦範空間 (Normed Space)

**定義**：賦範空間是一個配備了範數的向量空間 $(X, \|\cdot\|)$，其中範數滿足：
- 正定性：$\|x\| \geq 0$，且 $\|x\| = 0 \iff x = 0$
- 齊次性：$\|\alpha x\| = |\alpha| \|x\|$
- 三角不等式：$\|x + y\| \leq \|x\| + \|y\|$

```python
class NormedSpace(Generic[T]):
    """Normed vector space: vector space with norm ||·||."""
```

### 巴納赫代數 (Banach Algebra)

**定義**：巴納赫代數是一個完全的賦範代數，即它是個代數，同時配備了 Compatible 的範數使得空間作為賦範空間是完備的，且滿足：

$$\|ab\| \leq \|a\| \|b\|$$

對於交換巴納赫代數，Gel'fand  transform 提供了同構於 $C_0(\Delta(A))$，其中 $\Delta(A)$ 為極大理想空間。

## 2. C*-代數 (C*-algebras)

**定義**：C*-代數是一個完全的巴納赫 *-代數，滿足 **C* 恆等式**：

$$\|a^* a\| = \|a\|^2$$

對於所有 $a \in A$ 成立。

```python
class CStarAlgebra:
    """C*-algebra: Banach *-algebra with ||a*a|| = ||a||²."""
```

### C*-代數的基本性質

1. **自伴隨性**：若 $a^* = a$，則 $a$ 為自伴隨元 (self-adjoint)
2. **正規性**：$aa^* = a^*a$ 的元素稱為正規元 (normal)
3. **么元**：若存在單位元 $1$，則 $\|1\| = 1$
4. **交換子**：$[a,b] = ab - ba$

### C*-代數的範例

- $B(H)$：希爾伯特空間上有界線性算子全體
- $C(X)$：緊豪斯多夫空間 $X$ 上的連續函數
- $M_n(\mathbb{C})$：$n \times n$ 矩陣代數
- 群 C*-代數 $C^*(G)$
- 約化 C*-代數 $C^*_r(G)$

## 3. 馮·諾伊曼代數 (Von Neumann Algebras)

**定義**：馮·諾伊曼代數是希爾伯特空間 $H$ 上有界算子代數 $B(H)$ 的 *-子代數，且在**弱算子拓撲** (Weak Operator Topology, WOT) 下閉包等於自身。

```python
class VonNeumannAlgebra:
    """Von Neumann algebra: *-subalgebra of B(H) closed in weak operator topology."""
```

### 雙交換子定理 (Bicommutant Theorem)

馮·諾伊曼基本定理指出：

$$\mathcal{M} = \mathcal{M}''$$

其中 $\mathcal{M}'$ 為交換子：

$$\mathcal{M}' = \{T \in B(H) : TA = AT, \forall A \in \mathcal{M}\}$$

### 因子 (Factors)

**定義**：中心僅包含純量倍的馮·諾伊曼代數稱為**因子**。因子分為三類：
- **類型 I**：包含 minimal 投影
- **類型 II**：無 minimal 投影但存在有限投影
- **類型 III**：僅有無限投影

### 弱算子拓撲

在 $B(H)$ 上，弱算子拓撲由以下收斂定義：

$$T_\alpha \xrightarrow{\text{WOT}} T \iff \langle T_\alpha \xi, \eta \rangle \to \langle T \xi, \eta \rangle, \forall \xi, \eta \in H$$

## 4. 正定元與態 (Positive Elements and States)

### 正定元 (Positive Elements)

**定義**：在 C*-代數中，元素 $a$ 稱為**正定**的，若 $a = b^* b$ 對某個 $b$ 成立。記為 $a \geq 0$。

```python
class PositiveElement:
    """Positive element in C*-algebra: a = b*b for some b."""
```

### 正定元的判準

對於自伴隨元 $a \in A_{\text{sa}}$，以下條件等價：
1. $a \geq 0$（即 $a$ 正定）
2. $\sigma(a) \subseteq [0, \infty)$（譜在非負實數軸上）
3. 存在 $b \in A$ 使得 $a = b^* b$

### 態 (States)

**定義**：C*-代數 $A$ 上的**態**是滿足以下條件的線性泛函 $\omega$：
1. 正性：$\omega(a^* a) \geq 0, \forall a \in A$
2. 規範化：$\|\omega\| = 1$（或 $\omega(1) = 1$ 當有單位元時）

GNS 建構 (Gel'fand–Naimark–Segal) 建立了態與表示之間的對應關係。

## 5. 譜理論 (Spectrum Theory)

### 譜的定義

**定義**：元素 $a \in A$ 的**譜** (spectrum) 為：

$$\sigma(a) = \{\lambda \in \mathbb{C} : a - \lambda I \text{ 在 } A \text{ 中不可逆}\}$$

```python
class SpectralTheorem:
    """Spectral theorem for self-adjoint operators."""

    def spectrum(self) -> Set[complex]:
        """σ(A) = {λ : A - λI is not invertible}."""
```

### 譜性質

1. **非空性**：$\sigma(a) \neq \emptyset$（對於巴納赫代數）
2. **譜半徑**：$r(a) = \max |\lambda| = \lim_{n \to \infty} \|a^n\|^{1/n}$
3. **預解函數**：$R_\lambda(a) = (a - \lambda I)^{-1}$ 在 $\mathbb{C} \setminus \sigma(a)$ 全純

### 譜映射定理

對於多項式 $p$：

$$p(\sigma(a)) = \sigma(p(a))$$

### 自伴隨算子的譜定理

若 $T = T^*$ 為希爾伯特空間上的自伴隨算子，則存在投影值測度 $E$ 使得：

$$T = \int_{\sigma(T)} \lambda \, dE(\lambda)$$

## 6. 函數計算 (Functional Calculus)

### 連續函數計算 (Continuous Functional Calculus)

對於 C*-代數中的正規元 $a$，存在唯一的 *-同態：

$$\phi_a : C(\sigma(a)) \to A$$

使得 $\phi_a(f) = f(a)$，且 $\|f(a)\| = \|f\|_\infty$。

```python
class FunctionalCalculus:
    """Continuous functional calculus in C*-algebra."""

    def continuous_functional_calculus(self, f: Callable) -> Any:
        """f(a) for f ∈ C(σ(a))."""
```

### Borel 函數計算

對於自伴隨算子，譜定理推廣到 Borel 函數：

$$f(T) = \int_{\sigma(T)} f(\lambda) \, dE(\lambda)$$

對於有界 Borel 函數 $f$。

### 可測函數與算子值測度

譜投影 $E(\Delta)$ 對任意 Borel 集 $\Delta$ 有定義，滿足：
- $E(\emptyset) = 0$
- $E(\mathbb{R}) = I$
- $E(\bigcup E_n) = \sum E_n$（對互不相交可測集）

## 7. Gelfand 變換 (Gelfand Transform)

### Gelfand 表示

對於交換巴納赫代數 $A$，定義**Gel'fand 變換**：

$$\hat{} : A \to C(\Delta(A)), \quad \hat{a}(\varphi) = \varphi(a)$$

其中 $\Delta(A)$ 為 $A$ 的**極大理想空間**（即非零 *-特徵標的集合）。

### 交換 C*-代數的結構

**定理**（Gel'fand–Naimark）：對於交換 C*-代數 $A$，Gel'fand 變換是等距 *-同構：

$$A \cong C(\Delta(A))$$

### 應用

1. 正定元的順序結構
2. 交換子的譜計算
3. 無理旋轉 C*-代數

## 8. 算子代數的 K-理論 (K-Theory for Operator Algebras)

### K₀-群

**定義**：對於 C*-代數 $A$，$K_0(A)$ 由 Murray-von Neumann 等價類的投影生成。

```python
class K0Group:
    """K₀-group: topological K-theory for C*-algebras."""
```

投影 $p, q \in M_n(A)$ 的 Murray-von Neumann 等價 $p \sim q$ 表示存在 $v, w \in M_n(A)$ 使得：

$$p = v^* v, \quad q = v v^*$$

### K₁-群

**定義**：$K_1(A)$ 由么正元的等價類生成（模掉平凡連通分支）。

```python
class K1Group:
    """K₁-group: K-theory for formal differences of unitaries."""
```

對於酉元 $u \in GL_n(A)$，其 K₁ 类為 $[u]$。

### 六宮圖 (Six-Term Exact序列)

對於短正合列：

$$0 \to J \to A \to A/J \to 0$$

有六宮圖：

```
K₀(J) → K₀(A) → K₀(A/J) → K₁(J)
  ↓         ↓         ↓         ↓
K₁(A/J) → K₁(J) → K₁(A) → K₁(A/J)
```

### Bott 週期性

$$K_i(A) \cong K_{i+2}(A), \quad i \geq 0$$

這使得六宮圖簡化為二年週期理論。

## 9. KK-理論與 Kasparov 積 (KK-Theory and Kasparov Product)

### KK-理論

**定義**（Kasparov）：$KK(A, B)$ 為從 $A$ 到 $B$ 的 **Fredholm 模** (Fredholm modules) 的拓撲。

```python
class IndexTheory:
    """Index theory: Fredholm index for elliptic operators."""
```

### Fredholm 模

一個從 $A$ 到 $B$ 的 Fredholm 模包含：
1.  Hilbert $B$-模 $\mathcal{E}$
2.  $A$ 的表示 $\pi: A \to \mathcal{L}(\mathcal{E})$
3.  滿足 $F^* F - 1, F F^* - 1 \in \mathcal{K}(\mathcal{E})$ 的算子 $F$

其中 $\mathcal{K}(\mathcal{E})$ 為 compact 算子。

### Kasparov 積

$KK$-理論，配備了雙線性配對（Kasparov 積）：

$$KK(A, B) \times KK(B, C) \to KK(A, C)$$

這使得 $KK$ 成為範疇論意義下的合成函子。

### 指標理論

Fredholm 算子 $T$ 的指標：

$${\rm ind}(T) = \dim \ker T - \dim {\rm coker} T = \dim \ker T - \dim \ker T^*$$

```python
class IndexTheory:
    """Index theory: Fredholm index for elliptic operators."""

    def index(self) -> int:
        """ind(T) = dim ker(T) - dim coker(T)."""
```

### 與 K-理論的關係

Atiyah–Singer 指標定理建立了拓撲指標與分析指標的聯繫：

$${\rm ind}(D) = {\rm dim}_\Gamma \ker D - {\rm dim}_\Gamma {\rm coker} D \in K^0(B)$$

對於流形上的橢圓算子 $D$。

## 模組結構

```python
# 核心類
NormedSpace           # 賦範空間
HilbertSpace          # 希爾伯特空間
BoundedOperator       # 有界算子
CStarAlgebra          # C*-代數
VonNeumannAlgebra     # 馮·諾伊曼代數
PositiveElement       # 正定元

# 譜理論
SpectralTheorem       # 譜定理
FunctionalCalculus    # 函數計算

# K-理論
K0Group               # K₀-群
K1Group               # K₁-群
IndexTheory           # 指標理論
```

## 數學背景與應用

1. **非交換幾何**：Connes 的非交換幾何使用算子代數研究非交換拓撲
2. **量子物理**：B(H) 為量子力學的算子代數框架
3. **表示理論**：群 C*-代數與 von Neumann 代數在表示論中核心
4. **拓撲K-理論**：與拓撲學的深刻聯繫（Bott 週期性）
5. **指標理論**：橢圓算子與流形拓撲的橋樑

## 參考文獻

1. Kadison, R. V., & Ringrose, J. R. - *Fundamentals of the Theory of Operator Algebras*
2. Arveson, W. - *An Invitation to C*-Algebras*
3. Connes, A. - *Noncommutative Geometry*
4. Blackadar, B. - *K-Theory for Operator Algebras*
5. Kasparov, G. G. - *Topological Invariants of Elliptic Operators*