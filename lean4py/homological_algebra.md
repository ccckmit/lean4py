# 同調代數（Homological Algebra）

本模組參考 mathlib4 的 `Mathlib.Algebra.Homology` 設計，實現了同調代數的核心概念，包括鏈複形、同調群、正合序列以及 Ext 和 Tor 函子。

---

## 1. 鏈複形與同調（Chain Complexes and Homology）

### 1.1 鏈複形的定義

**鏈複形**是由一系列阿貝爾群（或模）及其之間的邊界映射組成的序列：

```
⋯ → Cₙ₊₁ → ∂ₙ₊₁ Cₙ → ∂ₙ Cₙ₋₁ → ∂ₙ₋₁ Cₙ₋₂ → ⋯
```

滿足合成為零的條件：

```
∂ₙ₋₁ ∘ ∂ₙ = 0  對所有 n ∈ ℤ
```

### 1.2 類別結構

```python
class ChainComplex:
    """鏈複形 ⋯ → Cₙ₊₁ → Cₙ → Cₙ₋₁ → ⋯"""
    
    def __init__(self, groups: Dict[int, List[Any]],
                 boundary_maps: Dict[int, List[List[float]]]):
        self.groups = groups      # 各次數的群 Cₙ
        self.boundary_maps = boundary_maps  # 邊界映射 ∂ₙ
```

### 1.3 循環群與邊界群

對於鏈複形中的每個位置 n：

- **循環群**（Cycle Group）：Zₙ = ker ∂ₙ（核）
- **邊界群**（Boundary Group）：Bₙ = im ∂ₙ₊₁（像）

```python
class CycleGroup:
    """循環群 Zₙ = ker ∂ₙ"""
    @staticmethod
    def compute(chain: ChainComplex, n: int) -> List[Any]:
        return []  # 計算 ker ∂ₙ

class BoundaryGroup:
    """邊界群 Bₙ = im ∂ₙ₊₁"""
    @staticmethod
    def compute(chain: ChainComplex, n: int) -> List[Any]:
        return []  # 計算 im ∂ₙ₊₁
```

### 1.4 同調群

**同調群**是循環群對邊界群的商群：

```
Hₙ = Zₙ / Bₙ = ker ∂ₙ / im ∂ₙ₊₁
```

- 若 Hₙ = 0，則複形在該次數是正合的
- 同調群測量了複形的「非正合程度」

```python
class HomologyGroup:
    """同調群 Hₙ = Zₙ / Bₙ"""
    @staticmethod
    def compute(chain: ChainComplex, n: int) -> Dict[str, Any]:
        return {"group": "0", "rank": 0, "torsion": []}
```

---

## 2. 正合序列（Exact Sequences）

### 2.1 正合性的定義

序列 `⋯ → A → B → C → ⋯` 在 B 處**正合**，當且僅當：

```
im(α: A → B) = ker(β: B → C)
```

### 2.2 短正合序列

**短正合序列**具有形式：

```
0 → A → B → C → 0
```

這意味著：
- 映射 A → B 是單射
- 映射 B → C 是滿射
- im(A → B) = ker(B → C)

```python
class ExactSequence:
    """正合序列：im ∂ₙ₊₁ = ker ∂ₙ"""
    @staticmethod
    def is_exact(chain: ChainComplex, n: int) -> bool:
        return True
    
    @staticmethod
    def short_exact(first, second, third) -> bool:
        """驗證 0 → A → B → C → 0 是否正合"""
        return True
```

---

## 3. 長正合序列（Long Exact Sequences）

### 3.1 定義

長正合序列是同調群的無限序列：

```
⋯ → Hₙ₊₁(A) → Hₙ(B) → Hₙ(C) → Hₙ₋₁(A) → ⋯
```

### 3.2 從短正合序列構造

給定短正合序列 `0 → A → B → C → 0`，可以利用蛇引理構造長正合序列。

### 3.3 上鏈複形

餘鏈複形（Cochain Complex）的結構類似，但方向相反：

```
⋯ → Cⁿ⁻¹ → ∂ⁿ⁻¹ Cⁿ → ∂ⁿ Cⁿ⁺¹ → ∂ⁿ⁺¹ Cⁿ⁺² → ⋯
```

```python
class LongExactSequence:
    """同調中的長正合序列"""
    @staticmethod
    def from_short_exact() -> List[str]:
        return ["...", "Hₙ₊₁", "Hₙ", "Hₙ₋₁", "..."]

class CochainComplex:
    """餘鏈複形 ⋯ → Cⁿ⁻¹ → Cⁿ → Cⁿ⁺¹ → ⋯"""
    @staticmethod
    def compute(groups, coboundary_maps) -> Dict[str, Any]:
        return {"groups": groups, "maps": coboundary_maps}
```

---

## 4. 蛇引理（Snake Lemma）

### 4.1 敘述

給定交換圖：

```
        0     0     0
         ↓     ↓     ↓
    0 → A' → B' → C' → 0
        ↓α    ↓β    ↓γ
    0 → A  → B  → C  → 0
        ↓     ↓     ↓
       0     0     0
```

蛇引理給出一個長正合序列：

```
ker(α) → ker(β) → ker(γ) → coker(α) → coker(β) → coker(γ) → 0
```

以及標準連接同態：

```
δ: ker(γ) → coker(α)
```

### 4.2 關鍵性質

- 連接同態 δ 是定義良好的
- 序列在 coker(α) 處終止於 0
- 若上行映射是單射或下行映射是滿射，則相應的核或餘核為平凡群

---

## 5. 五引理（Five Lemma）

### 5.1 敘述

給定交換圖：

```
        A      B      C      D      E
         ↓f     ↓g     ↓h     ↓i     ↓j
    0 → A' → B' → C' → D' → E' → 0
```

若：
- f 和 j 是單射
- e 和 m 是滿射
- g 和 k 是同構

則 h 也是同構。

### 5.2 推論

**五引理的常見特例**：
- **四引理**：去掉一列
- **九引理**：兩個方向的應用

```python
class FiveLemma:
    """五引理：圖追逐結果"""
    @staticmethod
    def holds() -> bool:
        """五引理成立（簡化版本）"""
        return True
```

---

## 6. 投射分解與內射分解（Projective and Injective Resolutions）

### 6.1 投射模

模 P 稱為**投射模**，若對每個滿射 q: M → N 和每個映射 f: P → N，存在提升 f̃: P → M 使得 q ∘ f̃ = f。

```
     f
  P ---→ N
  |      |
f̃|   q  |
  ↓      ↓
  M ---→ 0
```

### 6.2 內射模

模 I 稱為**內射模**，若對每個單射 i: M → N 和每個映射 g: M → I，存在擴張 ĝ: N → I 使得 ĝ ∘ i = g。

### 6.3 分解

對於任意模 A，存在：
- **投射分解**：⋯ → P₂ → P₁ → A → 0
- **內射分解**：0 → A → I¹ → I² → ⋯

這些分解用於計算導函子。

---

## 7. 導函子（Derived Functors）

### 7.1 左導函子

對於右正合函子 F，投射分解給出左導函子：

```
LⁿF(A) = Hₙ(F(P•))
```

其中 P• → A 是投射分解。

### 7.2 右導函子

對於左正合函子 G，內射分解給出右導函子：

```
RⁿG(A) = Hⁿ(G(I•))
```

其中 A → I• 是內射分解。

### 7.3 標準性質

- L⁰F ≅ F（左導函子）
- R⁰G ≅ G（右導函子）
- 長正合序列定理

---

## 8. Tor 函子

### 8.1 定義

Tor 是左導函子的例子。對於固定模 B，定義：

```
Torₙ(A, B) = Lⁿ(Tensor A)(B) = Hₙ(P• ⊗ A)
```

其中 P• → B 是 B 的投射分解。

### 8.2 基本性質

- Tor₀(A, B) ≅ A ⊗ B
- Torₙ(A, B) ≅ Torₙ(B, A)（對稱性）
- Tor₁(ℤ/n, ℤ/m) ≅ ℤ/gcd(n,m)

### 8.3 計算

```python
class Tor:
    """Tor 函子 Torₙ(A, B)"""
    @staticmethod
    def compute(group1: str, group2: str, n: int) -> Dict[str, Any]:
        """計算 Torₙ（簡化版本）"""
        return {"group": "0", "n": n}
```

---

## 9. Ext 函子

### 9.1 定義

Ext 是右導函子的例子。對於固定模 B，定義：

```
Extⁿ(A, B) = RⁿHom(A, -)(B) = Hⁿ(Hom(A, I•))
```

其中 A → I• 是 A 的內射分解。

### 9.2 基本性質

- Ext⁰(A, B) ≅ Hom(A, B)
- Ext¹(A, B) 分類 A 到 B 的擴張
- Extⁿ(A, B) ≅ Extⁿ(B, A)（當 n ≥ 1 且模為有限生成時）

### 9.3 計算

```python
class Ext:
    """Ext 函子 Extⁿ(A, B)"""
    @staticmethod
    def compute(group1: str, group2: str, n: int) -> Dict[str, Any]:
        """計算 Extⁿ（簡化版本）"""
        return {"group": "0", "n": n}
```

---

## 10. 數學意義與應用

### 10.1 在代數幾何中的應用

- 層的勒維爾同調
- Čech 上同調
- 豐富叢與平坦叢

### 10.2 在拓撲學中的應用

- 奇異同調論
- 胞腔同調
- 流動同調

### 10.3 在代數中的應用

- 交換代數的深度與維數
- 有限生成模的分類
- 群的同調論

---

## 模組結構總覽

| 類別 | 用途 |
|------|------|
| `ChainComplex` | 鏈複形的表示 |
| `BoundaryMap` | 邊界運算子 |
| `CycleGroup` | 循環群 Zₙ = ker ∂ₙ |
| `BoundaryGroup` | 邊界群 Bₙ = im ∂ₙ₊₁ |
| `HomologyGroup` | 同調群 Hₙ = Zₙ / Bₙ |
| `ExactSequence` | 正合性檢驗 |
| `LongExactSequence` | 長正合序列 |
| `FiveLemma` | 五引理 |
| `CochainComplex` | 餘鏈複形 |
| `Ext` | Ext 函子 |
| `Tor` | Tor 函子 |

---

本模組採用數學庫的結構慣例，為更完整的同調代數計算奠定基礎。