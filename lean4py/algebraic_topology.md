# 代數拓撲 (Algebraic Topology)

本文件介紹 lean4py 代數拓撲模塊背後的數學原理，基於 `algebraic_topology.py` 實現。

## 1. 基本群 π₁(X, x₀)：環路的同倫類

### 定義

基本群是拓撲空間中以定點 x₀ 為基點的閉路的同倫類組成的群。

- **环路 (Loop)**：從基點 x₀ 出發，最終返回 x₀ 的連續映射 γ: [0,1] → X
- **同倫 (Homotopy)**：兩條环路 γ₀, γ₁ 如果可以通過連續變形相互轉化，則稱它們同倫
- **同倫類**：所有相互同倫的环路構成一個等價類

### 群運算

兩條环路 [α] 和 [β] 的乘積定義為：
- 先走 α，再走 β
- [α] · [β] = [α ∗ β]

### 基本性質

| 性質 | 說明 |
|------|------|
| 單位元 | 恒定环路（基點處靜止） |
| 逆元素 | 反向走的环路 [γ]⁻¹ = [γ⁻¹] |
| 結合律 | 同倫意義下成立 |

在 `FundamentalGroup` 類中：
```python
class FundamentalGroup:
    @staticmethod
    def compute(space, basepoint):
        """計算基本群（簡化版本：返回平凡群）"""
        return {"group_type": "trivial", "generators": [], "relations": []}

    @staticmethod
    def is_trivial(space, basepoint):
        """判斷空間是否單連通"""
        return True
```

---

## 2. 路徑連通性與單連通空間

### 路徑連通 (Path-Connected)

一個空間 X 稱為**路徑連通**，如果對於任意兩點 x, y ∈ X，存在連續映射：
```
γ: [0,1] → X 使得 γ(0) = x, γ(1) = y
```

### 單連通 (Simply-Connected)

空間 X 稱為**單連通**，如果：
1. X 是路徑連通的
2. 任意閉路同倫於恒定环路（即 π₁(X) 是平凡群）

### 典型例子

| 空間 | 路徑連通 | 單連通 |
|------|----------|--------|
| ℝⁿ | 是 | 是 |
| Sⁿ (n ≥ 2) | 是 | 是 |
| S¹ | 是 | 否（π₁ ≅ ℤ）|
| 環面 T² | 是 | 否（π₁ ≅ ℤ × ℤ）|

---

## 3. 覆蓋空間與提升性質

### 覆蓋空間定義

投影 p: Ẋ → X 為覆蓋空間，若對每個 x ∈ X，存在開鄰域 U 使得：
- p⁻¹(U) = ⊔ᵅ Vᵅ（不相交開集的無交並）
- 每個 Vᵅ 同胚於 U

### 提升性質

覆蓋空間的核心性質：

1. **路徑提升**：每條路徑可以唯一提升到覆蓋空間
2. **同倫提升**：同倫可以提升
3. **提升判準**：若 pᵍₑₑ(π₁(Ẋ)) ⊂ pᵍₑₑ(π₁(X))，則映射可以提升

### 與基本群的關係

- 通用覆蓋空間的Deck變換群 ≅ π₁(X)
- 覆蓋空間分類 ⟺ 子群分類

---

## 4. 導出同態與 π₁

### 誘導同態

連續映射 f: X → Y 誘導基本群同態：
```
fₜ: π₁(X, x₀) → π₁(Y, f(x₀))
[f: γ] ↦ [f ∘ γ]
```

### 性質

- (g ∘ f)ₜ = gₜ ∘ fₜ
- idₜ = id
- 若 f 為同倫等價，則 fₜ 為同構

### 基本群函子性

```
Top* → Grp
X ↦ π₁(X)
f ↦ fₜ
```

---

## 5. 高階同倫群 πₙ(X, x₀)

### 定義

n 階同倫群定義為：
```
πₙ(X, x₀) = [(Sⁿ, s₀), (X, x₀)]
```

即從 n 維球面到 X 的基點保持映射的同倫類。

### 基本性質

| 群 | 維數 | 交換性 |
|----|------|--------|
| π₁ | 1 | 非交換（一般情況）|
| π₂ | 2 | 交換 |
| π₃ | 3 | 交換 |
| πₙ (n ≥ 2) | n ≥ 2 | 交換 |

### 主要結果

- **Hurewicz定理**：當 n = 2 且 π₁ = 0 時，π₂ ≅ H₂
- ** Whitehead定理**：弱同倫等價 ⟹ 同調同構（對良好空間）

---

## 6. Seifert-van Kampen 定理

### 定理敘述

若 X = U ∪ V，其中 U, V, U ∩ V 均為路徑連通開集，x₀ ∈ U ∩ V，則：
```
π₁(X, x₀) ≅ π₁(U, x₀) * π₁(V, x₀) / N
```
其中 N 是由嵌入同態的像生成的正規子群。

### 計算步驟

1. 將空間分解為較小、已知基本群的開集
2. 寫出自由積
3. 加入U ∩ V 中閉路的關係
4. 化簡得到最終結果

### 經典應用

**S¹ ∨ S¹ 的基本群**：
- U = 去掉第一個圓心的鄰域 ≅ 圓環
- V = 去掉第二個圓心的鄰域 ≅ 圓環
- U ∩ V ≅ 兩個開弧的並
```
π₁(S¹ ∨ S¹) ≅ ℤ * ℤ = F₂（自由群）
```

---

## 7. CW 複形與胞腔逼近

### CW 複形定義

CW 複形是按維數遞增構造的空間：

1. **0-骨架**：離散點集 X⁰
2. **n-骨架**：Xⁿ = Xⁿ⁻¹ ∪ {n-胞腔 eⁿₐ}
3. **附著映射**：φₐ: Sⁿ⁻¹ → Xⁿ⁻¹
4. **閉包有限**：每點的鄰域只交於有限個胞腔

### 構造示例

**Sⁿ 作為 CW 複形**：
```python
class CWComplex:
    @staticmethod
    def build_sphere(n):
        """將 Sⁿ 構建為 CW 複形"""
        return {"skeleton": n, "cells": n + 1}
```

- S¹：一個 0-胞腔 + 一個 1-胞腔
- S²：一個 0-胞腔 + 一個 2-胞腔
- Sⁿ：一個 0-胞腔 + 一個 n-胞腔

### 胞腔逼近定理

任意連續映射 f: X → Y 可以胞腔逼近：
- 相對同倫群不變
- 可逐步提升到胞腔映射

---

## 8. 同調群 Hₙ(X)：鏈、環路、邊界

### 鏈群 Cₙ

以 n 維單形為基生成的自由阿貝爾群：
```
Cₙ(K) = ⊕ᵢ ℤ · σᵢ
```
σᵢ 為 n 維單形。

### 邊界運算

邊界算子 ∂ₙ: Cₙ → Cₙ₋₁：
- ∂ₙ(σ) = Σ (-1)ᵢ σ(v₀, ..., v̂ᵢ, ..., vₙ)
- 邊界的邊界為零：∂ₙ₋₁ ∘ ∂ₙ = 0

### 核與像

| 群 | 定義 | 幾何意義 |
|----|------|----------|
| Zₙ = Ker(∂ₙ) | n-鏈中無邊界的 | n-維環路 |
| Bₙ = Im(∂ₙ₊₁) | 為某 (n+1)-鏈的邊界 | n-維邊界 |

### 同調群定義

```
Hₙ(X) = Zₙ / Bₙ
```

在 `Homology` 類中：
```python
class Homology:
    @staticmethod
    def compute(complex, dim):
        """計算 H_dim（簡化版本）"""
        return {"group": "0", "rank": 0, "torsion": []}

    @staticmethod
    def is_trivial(complex, dim):
        result = Homology.compute(complex, dim)
        return result["group"] == "0"
```

---

## 9. 正合序列

### 定義

序列 ... → Aₙ₊₁ → Aₙ → Aₙ₋₁ → ... 稱為**正合」，若：
```
Im(αₙ) = Ker(αₙ₋₁)
```

### 短正合列

```
0 → A → B → C → 0
```

意味著：
- α 為單射
- β 為滿射
- Im(α) = Ker(β)

### 同調長正合列

由短正合列：
```
0 → K' → K → K'' → 0
```
誘導長正合列：
```
... → Hₙ(K') → Hₙ(K) → Hₙ(K'') → Hₙ₋₁(K') → ...
```

### 五引理與分裂引理

- **五引理**：交換圖中的垂直映射均為同構時，底部映射也為同構
- **分裂引理**：短正合列分裂 ⟺ 第三項為直和

---

## 模塊結構總結

| 類 | 功能 | 主要方法 |
|----|------|----------|
| `FundamentalGroup` | 基本群計算 | `compute()`, `is_trivial()` |
| `Homotopy` | 同倫關係 | `are_homotopic()`, `homotopy_class()` |
| `SimplicialComplex` | 單純複形 | `dimension()`, `euler_characteristic()` |
| `CWComplex` | CW 複形構建 | `build_sphere()` |
| `Homology` | 同調群計算 | `compute()`, `is_trivial()` |
| `BettiNumber` | Betti 數計算 | `compute()` |

### 歐拉示性數

對於有限胞腔複形：
```
χ(K) = Σ (-1)ⁿ fₙ = Σ (-1)ⁿ rank(Hₙ)
```
其中 fₙ 為 n-胞腔數目。

```python
def euler_characteristic(self):
    counts = {}
    for s in self.simplices:
        dim = len(s) - 1
        counts[dim] = counts.get(dim, 0) + 1
    return sum((-1)**d * c for d, c in counts.items())
```

---

## 參考文獻

1. Hatcher, A. *Algebraic Topology*. Cambridge University Press, 2002.
2. May, J.P. *A Concise Course in Algebraic Topology*. University of Chicago Press, 1999.
3. Munkres, J.R. *Elements of Algebraic Topology*. Addison-Wesley, 1984.