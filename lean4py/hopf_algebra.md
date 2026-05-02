# Hopf 代數模組文檔

本模組實現了 Hopf 代數、雙代數、余代數及量子群的數學結構。

## 1. 餘代數 (Coalgebra)

餘代數是代數的對偶概念。設 $k$ 為域，餘代數 $C$ 是配備以下結構的向量空間：

- **餘乘法 (Comultiplication)**: $\Delta: C \to C \otimes C$
- **餘單位 (Counit)**: $\varepsilon: C \to k$

這些映射滿足以下公理：

- **餘結合性 (Coassociativity)**: $(\Delta \otimes \text{id}) \circ \Delta = (\text{id} \otimes \Delta) \circ \Delta$
- **餘單位條件**: $(\varepsilon \otimes \text{id}) \circ \Delta = \text{id} = (\text{id} \otimes \varepsilon) \circ \Delta$

```python
class Coalgebra:
    """Coalgebra: vector space C with coassociative comultiplication.

    Δ: C → C ⊗ C, ε: C → k (counit)
    """
```

### Sweedler 記號

餘乘法的結果通常使用 **Sweedler 記號** 表示：
$$\Delta(x) = x^{(1)} \otimes x^{(2)}$$

對於多次應用餘乘法：
$$\Delta^2(x) = x^{(1)} \otimes x^{(2)} \otimes x^{(3)}$$

```python
def Sweedler_notation(self, x: Any) -> str:
    """Return Sweedler notation Δ(x) = x^{(1)} ⊗ x^{(2)}."""
    return f"{x}^{(1)} ⊗ {x}^{(2)}"
```

## 2. 雙代數 (Bialgebra)

雙代數同時具備代數和餘代數結構，兩者滿足兼容性條件。

### 代數結構
- **乘法**: $m: A \otimes A \to A$
- **單位**: $\eta: k \to A$

### 餘代數結構
- **餘乘法**: $\Delta: A \to A \otimes A$
- **餘單位**: $\varepsilon: A \to k$

### 兼容性條件

對於所有 $a, b \in A$：
$$\Delta(ab) = \Delta(a)\Delta(b)$$
$$\varepsilon(ab) = \varepsilon(a)\varepsilon(b)$$

```python
class Bialgebra(Coalgebra):
    """Bialgebra: algebra + coalgebra compatible.

    (B, m, η, Δ, ε) where m, η make B an algebra
    and Δ, ε make B a coalgebra, with compatibility.
    """
```

## 3. Hopf 代數

Hopf 代數是配備**對蹤 (Antipode)** $S$ 的雙代數。

### 對蹤映射

對蹤 $S: H \to H$ 是满足以下條件的唯一線性映射：
$$S(x^{(1)})x^{(2)} = \varepsilon(x)1 = x^{(1)}S(x^{(2)})$$

### Hopf 代數公理

1. $(H, m, \eta)$ 是代數
2. $(H, \Delta, \varepsilon)$ 是餘代數
3. $\Delta$ 和 $\varepsilon$ 是代數同態（反之亦然）
4. 存在對蹤 $S$

```python
class HopfAlgebra(Bialgebra):
    """Hopf algebra: bialgebra with antipode S: H → H.

    S(x) = x^{(1)} S(x^{(2)}) = ε(x)1 = S(x^{(1)}) x^{(2)}
    """
```

## 4. 實例：群代數

群代數 $k[G]$ 是最經典的 Hopf 代數例子。

對於群 $G$ 的元素 $g \in G$：
- **餘乘法**: $\Delta(g) = g \otimes g$
- **餘單位**: $\varepsilon(g) = 1$
- **對蹤**: $S(g) = g^{-1}$

```python
class GroupAlgebra:
    """Group algebra k[G]: twisted group ring of G over field k.

    As Hopf algebra: Δ(g) = g ⊗ g, ε(g) = 1, S(g) = g^{-1}
    """
```

## 5. 量子群 (Quantum Group)

量子群是經典 enveloping 代數或李群的**非交換形變**。

### Drinfeld-Jimbo 量子群

對於根系 $\mathfrak{g}$ 和參數 $q \neq 1$：
$$U_q(\mathfrak{g})$$

當 $q \to 1$ 時，量子群收斂到經典的李代數。

```python
class QuantumGroup:
    """Quantum group: noncommutative deformation of enveloping algebra.

    U_q(g) for q ≠ 1: Drinfeld-Jimbo quantum group.
    """
```

### R-矩陣

量子群配備 **R-矩陣** $R \in H \otimes H$，滿足 Yang-Baxter 方程：
$$R_{12}R_{13}R_{23} = R_{23}R_{13}R_{12}$$

### 量化 sl(2)

```python
def sl2_quantized(q: float) -> HopfAlgebra:
    """Quantized sl(2) quantum group.

    U_q(sl2) with generators E, F, K satisfying:
    KK^{-1} = K^{-1}K = 1
    KEK^{-1} = q^{1/2}E, KFK^{-1} = q^{-1/2}F
    EF - FE = (K - K^{-1})/(q^{1/2} - q^{-1/2})
    """
```

## 6. 表示理論

### Hopf 代數的表示

Hopf 代數 $H$ 的表示是配備 $H$ 作用的向量空間 $V$：

$$h \cdot (v + w) = h \cdot v + h \cdot w$$
$$(gh) \cdot v = g \cdot (h \cdot v)$$
$$1 \cdot v = v$$

作用满足：
$$h \cdot (vw) = (h^{(1)} \cdot v)(h^{(2)} \cdot w)$$

```python
class RepresentationOfHopfAlgebra:
    """Representation of Hopf algebra (left module)."""
```

### 模代數 (Module Algebra)

模代數是同時具備代數和 $H$-模結構的空間：

對於所有 $h \in H$, $a, b \in A$：
$$h \cdot (ab) = (h^{(1)} \cdot a)(h^{(2)} \cdot b)$$

```python
class ModuleAlgebra:
    """Module algebra: representation of Hopf algebra on algebra.

    For action of Hopf algebra on commutative algebra.
    """
```

### 不變理論

固定子代數：
$$A^G = \{a \in A \mid g \cdot a = a, \forall g \in G\}$$

```python
class InvariantTheory:
    """Invariant theory: fixed subalgebra under group action.

    A^G = {a ∈ A | g·a = a for all g ∈ G}
    """
```

## 7. 餘模 (Comodule)

餘模是餘代數的對偶概念。

向量空間 $M$ 是餘代數 $C$ 的**右餘模**，若配備映射：
$$\rho: M \to M \otimes C$$

滿足餘結合性和餘單位條件。

## 8. 代數與餘代數的對偶性

代數和餘代數之間存在優雅的對偶關係。

### 有限維情形

若 $H$ 是有限維的，則其對偶空間 $H^*$ 自動構成代數：
$$(f * g)(x) = f(x^{(1)})g(x^{(2)})$$

### 對偶 Hopf 代數

有限維 Hopf 代數的對偶仍是 Hopf 代數。

```python
class DualHopfAlgebra:
    """Dual of finite-dimensional Hopf algebra."""

    def dual_multiplication(self) -> Callable:
        """Convolution product on dual."""
        return lambda x, y: f"({x} * {y})"
```

## 9. 編織範疇 (Braided Category)

Hopf 代數的表示範疇是**編織張量範疇**，配有 braiding：
$$\sigma_{V,W}: V \otimes W \to W \otimes V$$

```python
class braided_category:
    """Category of braided Hopf algebras."""

    def braiding(self, a: HopfAlgebra, b: HopfAlgebra) -> Callable:
        """Get braiding R: a ⊗ b → b ⊗ a."""
        return lambda x, y: (y, x)
```

## 10. 數學背景總結

| 結構 | 映射 | 公理數量 |
|------|------|----------|
| 代數 | $m: A \otimes A \to A$, $\eta: k \to A$ | 2 |
| 餘代數 | $\Delta: C \to C \otimes C$, $\varepsilon: C \to k$ | 2 |
| 雙代數 | 以上全部 | 4 |
| Hopf 代數 | 雙代數 + $S: H \to H$ | 5 |

### 關鍵性質

1. **餘交換 (Cocommutative)**: $\tau \circ \Delta = \Delta$，其中 $\tau(x \otimes y) = y \otimes x$
2. **交換 (Commutative)**: $ab = ba$
3. **自對偶**: $H \cong H^*$

## API 參考

### 核心類

| 類名 | 描述 |
|------|------|
| `Coalgebra` | 餘代數基類 |
| `Bialgebra` | 雙代數基類 |
| `HopfAlgebra` | Hopf 代數基類 |
| `GroupAlgebra` | 群代數 $k[G]$ |
| `QuantumGroup` | Drinfeld-Jimbo 量子群 |
| `ModuleAlgebra` | 模代數 |
| `RepresentationOfHopfAlgebra` | Hopf 代數表示 |
| `DualHopfAlgebra` | 對偶 Hopf 代數 |
| `braided_category` | 編織 Hopf 代數範疇 |

### 輔助函數

| 函數 | 描述 |
|------|------|
| `sl2_hopf()` |經典 sl(2) Hopf 代數 |
| `sl2_quantized(q)` | 量化 sl(2) 量子群 |