# 伴隨表示理論 (Adjunction Representation Theory)

本文件解釋 `adjunction_representation.py` 模組的數學原理，涵蓋李群表示論中的伴隨作用、軌道理論及相關代數結構。

---

## 目錄

1. [伴隨作用與餘伴隨表示](#1-伴隨作用與餘伴隨表示)
2. [軌道理論](#2-軌道理論)
3. [拋物子代數與旗簇](#3-拋物子代數與旗簇)
4. [根系統與正根系](#4-根系統與正根系)
5. [Borel 子代數與拋物子代數](#5-borel-子代數與拋物子代數)
6. [Verma 模與指標公式](#6-verma-模與指標公式)
7. [軌道方法 (Kirillov 方法)](#7-軌道方法-kirillov-方法)
8. [數學關係圖](#8-數學關係圖)

---

## 1. 伴隨作用與餘伴隨表示

### 1.1 伴隨作用 (Adjoint Action)

對於李群 $G$ 及其李代數 $\mathfrak{g}$，**伴隨作用**定義為：

$$\text{Ad}: G \to \text{Aut}(\mathfrak{g}), \quad \text{Ad}_g(X) = gXg^{-1}$$

在矩陣群中，這對應於共軛作用。伴隨作用將群的元素映射到李代數的自同構。

```python
class AdjointAction:
    """Adjoint action of group on its Lie algebra.

    Ad: G → Aut(g), Ad_g(X) = gXg^{-1}.
    """
```

### 1.2 餘伴隨表示 (Coadjoint Representation)

餘伴隨作用是伴隨作用的對偶概念。對於 $\xi \in \mathfrak{g}^*$（餘伴隨空間）：

$$\kappa_g(\xi)(X) = \xi(\text{Ad}_{g^{-1}}(X))$$

這定義了 $G$ 在 $\mathfrak{g}^*$ 上的作用，是表示論研究的核心工具。

```python
class CoadjointRepresentation:
    """Coadjoint representation: G → Aut(g*)."""
```

### 1.3 中心化子 (Centralizer)

元素或子群的核心化子定義為：

$$C_G(H) = \{g \in G \mid gh = hg, \forall h \in H\}$$

這是穩定化子的推廣，在分類軌道時很重要。

```python
class Centralizer:
    """Centralizer of element/subgroup in Lie group."""
```

---

## 2. 軌道理論

### 2.1 伴隨軌道 (Adjoint Orbit)

在伴隨作用下，一個元素 $X \in \mathfrak{g}$ 的軌道為：

$$O_X = \{ \text{Ad}_g(X) \mid g \in G \}$$

軌道的拓撲性質反映了元素的分類：
- **半單元素**：封閉軌道
- **冪零元素**：有界軌道

```python
class AdjointOrbit:
    """Orbit in Lie algebra under adjoint action."""

    def is_nilpotent(self) -> bool:
        """X is nilpotent if orbit is bounded."""
        return False

    def is_semisimple(self) -> bool:
        """X is semisimple if orbit is closed."""
        return False
```

### 2.2 餘伴隨軌道 (Kirillov 軌道)

**Kirillov 軌道方法**建立了餘伴隨空間中的軌道與單式表示之間的對應：

$$O_\xi \subset \mathfrak{g}^*$$

對於冪零李群，每個餘伴隨軌道都對應一個唯一的基本單式表示。

```python
class KirillovOrbit:
    """Kirillov orbit: orbit in g* under coadjoint action."""

    def dimension(self) -> int:
        """dim O_ξ = dim G - dim stabilizer."""
        return 0

    def is_integral(self) -> bool:
        """Check if orbit corresponds to unitary representation."""
        return True
```

### 2.3 冪零軌道 (Nilpotent Orbit)

在半單李代數中，冪零軌道具有特別重要的地位。Jacobson-Morozov 定理允許我們將每個冪零元素嵌入到一个 $\mathfrak{sl}_2$-三元素組。

```python
class NilpotentOrbit:
    """Nilpotent orbit in semisimple Lie algebra."""

    def associated_graded(self) -> List[List[float]]:
        """Associated graded of orbit under Jacobson-Morozov."""
        return [self.nilpotent_element]
```

---

## 3. 拋物子代數與旗簇

### 3.1 Borel 子群 (Borel Subgroup)

**Borel 子群** $B$ 是李群 $G$ 的最大可解子群。它具有Levi分解：

$$B = U \rtimes T$$

其中 $U = [B, B]$ 是冪么根基，$T$ 是極大環面。

```python
class BorelSubgroup:
    """Borel subgroup: maximal solvable subgroup B ⊆ G."""

    def levi_decomposition(self) -> Tuple[Any, Any]:
        """B = U ⋊ T (semidirect product)."""
        return (None, None)

    def unipotent_radical(self) -> Any:
        """U = [B, B] (unipotent)."""
        return None
```

### 3.2 旗簇 (Flag Variety)

旗簇是齊性空間 $G/B$，其維度為：

$$\dim(G/B) = \dim G - \dim B$$

旗簇在幾何表示論中起核心作用，其上層的 Schubert 胞腔構成了胞腔分解。

```python
class FlagVariety:
    """Flag variety: G/P for parabolic subgroup P."""

    def dimension(self) -> int:
        """dim G/P = dim G - dim P."""
        return 0

    def cohomology_ring(self) -> str:
        """H*(G/P, Z) via Schubert calculus."""
        return "cohomology_ring"
```

---

## 4. 根系統與正根系

### 4.1 根空間分解

關於 Cartan 子代數 $\mathfrak{h}$ 的根空間分解為：

$$\mathfrak{g} = \mathfrak{h} \oplus \bigoplus_{\alpha \in \Delta} \mathfrak{g}_\alpha$$

其中每個根空間 $\mathfrak{g}_\alpha = \{X \in \mathfrak{g} \mid [H, X] = \alpha(H)X, \forall H \in \mathfrak{h}\}$。

```python
class RootDecomposition:
    """Root space decomposition relative to torus.

    g = t ⊕ ⊕_{α∈Δ} g_α.
    """
```

### 4.2 正根系 (Positive System)

正根系 $\Delta^+$ 選擇一組「正半空間」，其中**單根**構成其基底。

```python
class PositiveSystem:
    """Positive system of roots.

    Δ^+ = {positive roots} with total order.
    """
```

---

## 5. Borel 子代數與拋物子代數

### 5.1 Borel 子代數

Borel 子代數 $\mathfrak{b}$ 是李代數的最大可解子代數，具有標準分解：

$$\mathfrak{g} = \mathfrak{n}_- \oplus \mathfrak{h} \oplus \mathfrak{n}_+$$

其中 $\mathfrak{n}_\pm = \bigoplus_{\alpha \in \Delta^\pm} \mathfrak{g}_\alpha$ 是冪零根空間。

```python
class BorelSubalgebra:
    """Borel subalgebra: maximal solvable subalgebra b ⊂ g.

    g = n_- ⊕ h ⊕ n_+ where n_± are nilpotent.
    """

    def nilpotent_radical(self) -> Any:
        """n = [b, b] (upper nilpotent)."""
        return None

    def cartan_subalgebra(self) -> Any:
        """h = maximal torus in b."""
        return None
```

### 5.2 拋物子代數

拋物子代數 $\mathfrak{p}$ 包含 Borel 子代數，標準形式為：

$$\mathfrak{p} = \mathfrak{b} \oplus \bigoplus_{\alpha \in \Delta^+, \alpha \notin \Pi} \mathfrak{g}_{-\alpha}$$

其中 $\Pi$ 是單根的子集。

```python
class ParabolicSubalgebra:
    """Parabolic subalgebra: p ⊃ b.

    p = b ⊕ ⊕_{α∈Δ^+, α not simple} g_{-α}.
    """

    def levi_decomposition(self) -> Tuple[Any, Any]:
        """p = (l ⊕ u) where l contains Cartan."""
        return (None, None)

    def unipotent_radical(self) -> Any:
        """u = nilpotent radical of p."""
        return None
```

---

## 6. Verma 模與指標公式

### 6.1 Verma 模指標

Verma 模由最高權 $\lambda \in \mathfrak{h}^*$ 參數化，其幾何結構由 Weyl 群作用下的軌道決定：

$$\lambda \in \mathfrak{h}^* / W$$

在 walls（牆）上會出现奇點。

```python
class VermaModuleIndex:
    """Index for Verma modules: character and extension groups.

    Parametrized by λ ∈ h* / W (with singularities at walls).
    """

    def is_regular(self) -> bool:
        """λ is regular: ⟨λ, α⟩ ≠ 0 for all roots α."""
        return True

    def is_dominant(self) -> bool:
        """λ is dominant: ⟨λ, α_i⟩ ≥ 0 for simple α_i."""
        return True

    def chamber(self) -> str:
        """Get Weyl chamber containing λ."""
        return "fundamental"
```

### 6.2 Weyl 特徵公式

有限維不可約表示 $V(\lambda)$ 的特徵由 **Weyl 特徵公式**給出：

$$\text{ch}\, V(\lambda) = \frac{\sum_{w \in W} \text{sign}(w) e^{w(\lambda + \rho)}}{\prod_{\alpha > 0} (1 - e^{-\alpha})}$$

其中 $\rho$ 是半總和。

```python
class CharacterFormula:
    """Weyl character formula for finite-dimensional representations.

    ch V(λ) = Σ_{w∈W} sign(w) e^{w(λ+ρ)} / ∏_{α>0} (1 - e^{-α}).
    """

    @staticmethod
    def compute(highest_weight: List[float], root_system: Optional[Any] = None) -> str:
        """Compute character of irreducible representation."""
        return "character_expression"

    @staticmethod
    def multiplicity(highest_weight: List[float], weight: List[float],
                     root_system: Optional[Any] = None) -> int:
        """Compute multiplicity of weight in representation."""
        return 1 if highest_weight == weight else 0
```

---

## 7. 軌道方法 (Kirillov 方法)

**Kirillov 的軌道方法**建立了李群表示論與餘伴隨空間拓撲之間的基本對應：

$$O_\xi \leftrightarrow \pi_\xi$$

對於冪零李群，這给出了從餘伴隨軌道到單式表示的精確構造。對於更一般的群，這是一個指導原則。

```python
class OrbitMethod:
    """Kirillov's orbit method: orbits ↔ representations.

    For nilpotent groups, unitary representations from orbits.
    """

    @staticmethod
    def orbit_to_representation(orbit: 'KirillovOrbit') -> Any:
        """Get unitary representation from coadjoint orbit."""
        return None

    @staticmethod
    def representation_to_orbit(rep: Any) -> Optional['KirillovOrbit']:
        """Get orbit from representation (when possible)."""
        return None
```

---

## 8. 數學關係圖

```
                    李群 G
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    伴隨作用        餘伴隨表示       Borel子群 B
        │              │              │
        ▼              ▼              ▼
    伴隨軌道      Kirillov軌道      Levi分解
    O_X ⊂ g       O_ξ ⊂ g*         B = U ⋊ T
        │              │
        ▼              ▼
    半單元素      單式表示
    冪零軌道      (Orbit Method)
```

---

## 類別總覽

| 類別 | 數學對象 | 關係 |
|------|----------|------|
| `AdjointAction` | 伴隨作用 $\text{Ad}: G \to \text{Aut}(\mathfrak{g})$ | 群作用 |
| `CoadjointRepresentation` | 餘伴隨作用 $G \to \text{Aut}(\mathfrak{g}^*)$ | 對偶作用 |
| `KirillovOrbit` | 餘伴隨軌道 $O_\xi \subset \mathfrak{g}^*$ | 軌道幾何 |
| `FlagVariety` | 旗簇 $G/B$ | 齊性空間 |
| `BorelSubgroup` | Borel子群 $B \subset G$ | 極大可解 |
| `RootDecomposition` | 根空間分解 $\mathfrak{g} = \mathfrak{h} \oplus \bigoplus_{\alpha \in \Delta} \mathfrak{g}_\alpha$ | 代數結構 |
| `PositiveSystem` | 正根系 $\Delta^+$ | 根的分類 |
| `VermaModuleIndex` | Verma模指標 $\lambda \in \mathfrak{h}^* / W$ | 表示參數化 |
| `CharacterFormula` | Weyl特徵公式 | 表示字符 |

---

## 參考文獻

1. Knapp, A. W. - *Representation Theory of Semisimple Groups*
2. Kirillov, A. A. - *Elements of the Theory of Representations*
3. Collingwood, D. H. - *Nilpotent Orbits in Semisimple Lie Algebras*
4. Humphreys, J. E. - *Introduction to Lie Algebras and Representation Theory*

---

*本文件由 lean4py 自動生成，基於 adjunction_representation.py (v1.34.0)*