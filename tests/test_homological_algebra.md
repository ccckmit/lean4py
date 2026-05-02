# 同調代數測試文檔 (test_homological_algebra.py)

## 1. 測試概述

本測試文件驗證 `lean4py.homological_algebra` 模塊的核心功能，涵蓋鏈複形、邊界映射、循環群、邊界群、同調群、正合序列和五引理。

---

## 2. 鏈複形測試 (ChainComplex)

### 測試內容
- `test_creation`: 驗證鏈複形的基本創建
- `test_get_group`: 驗證獲取特定維度的群
- `test_get_boundary`: 驗證獲取邊界映射

### 數學原理

**鏈複形** (Chain Complex) 是同調代數的基本結構，由一系列阿貝爾群和群同態組成：

```
... → C_{n+1} --∂_{n+1}→ C_n --∂_n→ C_{n-1} → ...
```

滿足條件：`∂_n ∘ ∂_{n+1} = 0`，即每個邊界映射的複合為零。這確保像 Im(∂_{n+1}) ⊆ Ker(∂_n)。

---

## 3. 邊界映射測試 (BoundaryMap)

### 測試內容
- `test_compose`: 驗證邊界映射的複合
- `test_is_zero`: 驗證邊界映射是否為零映射

### 數學原理

**邊界映射** (Boundary Map) ∂_n: C_n → C_{n-1} 將 n 維鏈映射到其邊界。

關鍵性質：
- `∂_{n-1} ∘ ∂_n = 0`：所有邊界的邊界為零
- 此複合為零是鏈複形定義的核心條件

---

## 4. 循環群與邊界群測試 (CycleGroup / BoundaryGroup)

### 測試內容
- `CycleGroup.compute`: 計算 n 維循環群 Z_n = Ker(∂_n)
- `BoundaryGroup.compute`: 計算 n 維邊界群 B_n = Im(∂_{n+1})

### 數學原理

**循環群** (Cycle Group)：Z_n = Ker(∂_n) = {c ∈ C_n | ∂_n(c) = 0}

**邊界群** (Boundary Group)：B_n = Im(∂_{n+1}) = {∂_{n+1}(c) | c ∈ C_{n+1}}

這兩個群滿足 B_n ⊆ Z_n（因為 ∂_n ∘ ∂_{n+1} = 0）。

---

## 5. 同調群測試 (HomologyGroup)

### 測試內容
- `test_compute`: 驗證同調群的計算，結果為 H_n = Z_n / B_n
- `test_is_trivial`: 驗證同調群是否為平凡群

### 數學原理

**同調群** (Homology Group)：

$$H_n(C) = Z_n / B_n = \text{Ker}(\partial_n) / \text{Im}(\partial_{n+1})$$

同調群度量鏈複形的「非精確程度」：
- H_n = 0 表示 C_n 是正合的
- H_n ≠ 0 表示存在非平凡的上同調類

**平凡群判斷**：當 Z_n = B_n 時（同調為零），同調群是平凡群。

---

## 6. 正合序列測試 (ExactSequence)

### 測試內容
- `test_is_exact`: 驗證序列在指定維度是否正合
- `test_short_exact`: 驗證短正合序列 0 → A → B → C → 0

### 數學原理

**正合序列** (Exact Sequence)：序列中每個映射的像等於下一個映射的核：

$$\text{Im}(\phi_n) = \text{Ker}(\phi_{n-1})$$

**短正合序列**：

$$0 \rightarrow A \xrightarrow{f} B \xrightarrow{g} C \rightarrow 0$$

滿足：
- f 是單射
- g 是滿射
- Im(f) = Ker(g)

---

## 7. 五引理測試 (FiveLemma)

### 測試內容
- `test_holds`: 驗證五引理成立

### 數學原理

**五引理** (Five Lemma)是同調代數中的基本交換圖引理：

```
          f₁         f₂         f₃         f₄         f₅
    A₁ ──────► A₂ ──────► A₃ ──────► A₄ ──────► A₅
    │         │         │         │         │
    │ α₁      │ α₂      │ α₃      │ α₄      │ α₅
    ▼         ▼         ▼         ▼         ▼
    B₁ ──────► B₂ ──────► B₃ ──────► B₄ ──────► B₅
          g₁         g₂         g₃         g₄         g₅
```

若行是短正合序列，且 f₁, f₂, f₄, f₅ 是同構，則 f₃ 也是同構。

---

## 8. 測試驗證總結

| 測試類 | 驗證內容 | 核心性質 |
|--------|----------|----------|
| ChainComplex | 結構創建與訪問 | ∂² = 0 |
| BoundaryMap | 複合與零性 | 複合封閉性 |
| CycleGroup | 核的計算 | Ker(∂) |
| BoundaryGroup | 像的計算 | Im(∂) |
| HomologyGroup | 商群計算 | Z_n/B_n |
| ExactSequence | 正合性 | Im = Ker |
| FiveLemma | 交換圖引理 | 同構保持 |