# 計算複雜度 (Computational Complexity) - 數學原理文檔

## 概述

本模組 `computational_complexity_v134.py` 實現了計算複雜性理論的基本框架，對應 mathlib4 的 `Mathlib.Computability.Complexity` 模組。

---

## 1. 時間複雜度類別

### 1.1 P 類（多項式時間）

**定義**：若存在圖靈機 M 和多項式 p(n)，使得語言 L = {x ∈ Σ* | M(x) 在 p(|x|) 步內接受}，則 L ∈ **P**。

**數學表示**：
```
P = ∪_{k≥0} TIME(nᵏ)
```

**意義**：
- P 代表「容易求解」的問題類別
- 多項式時間 f(n) = nᵏ 是增長速度可控的算法
- 實例：排序 O(n log n)、矩陣乘法 O(n^2.37)、最短路徑 O(n²)

### 1.2 NP 類（非確定性多項式時間）

**定義**：若存在非確定性圖靈機 M 和多項式 p(n)，使得：
```
L = {x | ∃y ∈ Σ*^p(|x|) 使得 M(x,y) 接受}
```
則 L ∈ **NP**。

**另一視角**：存在多項式時間驗證器 V(x, c) 使得：
- x ∈ L ⇒ ∃c: V(x, c) = 接受
- x ∉ L ⇒ ∀c: V(x, c) = 拒絕

### 1.3 PSPACE 類

**定義**：可在多項式空間內判定的語言類別：
```
PSPACE = ∪_{k≥0} SPACE(nᵏ)
```

**重要關係**：
- P ⊆ NP ⊆ PSPACE = NP ∪ co-NP（上界）

---

## 2. NP-完全性

### 2.1 NP-完全定義

**定義**：語言 L 是 **NP-完全**（NPC）當且僅當：
1. L ∈ NP（屬於該類）
2. ∀L' ∈ NP，L' ≤_P L（所有 NP 問題可多項式時間歸約到 L）

### 2.2 NP-難（NP-Hard）

**定義**：若 ∀L' ∈ NP，L' ≤_P L，則 L 是 **NP-難**。

### 2.3 Cook-Levin 定理

**定理（Cook, 1971）**：
> **SAT（布林可滿足性）是 NP-完全的**

**證明思路**：將任意 NP 問題的驗證器模擬為布林電路

---

## 3. 歸約 (Reductions)

### 3.1 多項式時間歸約

**定義**：語言 L₁ 可多項式時間歸約到 L₂（L₁ ≤_P L₂），當存在多項式時間可計算函數 f，使得：
```
x ∈ L₁ ⟺ f(x) ∈ L₂
```

**性質**：
- 自反性：L ≤_P L
- 傳遞性：L₁ ≤_P L₂ 且 L₂ ≤_P L₃ ⇒ L₁ ≤_P L₃

### 3.2 傳遞性

```python
@staticmethod
def is_transitive(L1: str, L2: str, L3: str) -> bool:
    """≤_P is transitive (simplified)."""
    return True
```

---

## 4. 經典 NP-完全問題

### 4.1 SAT（布林可滿足性）

**問題**：給定布林公式 φ，是否存在賦值使得 φ 為真？

### 4.2 3-SAT（三元可滿足性）

**問題**：每個子句恰好包含 3 個文字的 CNF 公式是否可滿足？

### 4.3 其他經典 NPC 問題

| 問題 | 描述 |
|------|------|
| **CLIQUE** | 是否存在大小為 k 的完全子圖？ |
| **VERTEX COVER** | 是否存在大小 ≤ k 的頂點覆蓋？ |
| **HAM-CYCLE** | 是否存在哈密爾頓圈？ |
| **SUBSET SUM** | 是否存在子集和為目標值？ |

---

## 5. 複雜度類層級

```
                    ┌─────────────┐
                    │     NPC     │
                    │ (NP-Complete)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │     NP      │
                    │(Non-det. P) │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │      P      │
                    │ (Poly-time) │
                    └─────────────┘
```

---

## 6. 模組結構

| 類 | 方法 | 功能 |
|----|------|------|
| **ComplexityClass** | P(), NP(), PSPACE() | 複雜度類別成員判定 |
| **NPCompleteness** | is_np_complete(), cook_levin() | NP-完全性驗證 |
| **Reduction** | polynomial_time(), is_transitive() | 多項式時間歸約 |
| **CookLevin** | holds(), reduction_to_sat() | Cook-Levin 定理相關 |

---

## 7. 與 mathlib4 的對應

本模組模仿 mathlib4 的 `Computability.Complexity` 結構：
- `ComplexityClass` 對應複雜度類別定義
- `NPCompleteness` 對應 NP-完全性理論
- `Reduction` 對應多項式時間歸約
- `CookLevin` 對應 Cook-Levin 定理

---

## 8. 參考文獻

1. Cook, S. A. (1971). "The Complexity of Theorem Proving Procedures". STOC.
2. Karp, R. M. (1972). "Reducibility Among Combinatorial Problems".
3. Sipser, M. "Introduction to the Theory of Computation".
4. Arora, S. & Barak, B. "Computational Complexity: A Modern Approach".

---

*本檔案說明 `computational_complexity_v134.py` 的數學原理*