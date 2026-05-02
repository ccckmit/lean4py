# 非交換幾何測試文檔

本文檔說明 `test_noncommutative_geometry.py` 中測試用例的數學原理。

## 1. 測試驗證概述

這些測試涵蓋非交換幾何的核心組件，包括：
- 非交換空間的基本結構
- 譜三元組（ spectral triple ）與 Dirac 算子
- 循環（上）同調與 Hochschild （上）同調
- Fredholm 指數與指標理論
- K-同調與 Fredholm 模
- Connes-Chern 字元

## 2. 譜三元組測試（Spectral Triple）

### 數學背景

譜三元組是非交換幾何的核心對象，由 Alain Connes 引入，定義為：

```
(A, H, D)
```

其中：
- **A** 是 C*-代數
- **H** 是希爾伯特空間
- **D** 是 Dirac 算子（自伴算子，封閉且稠密定義）

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 創建譜三元組並驗證其組件 | 確保 (代數，希爾伯特空間，Dirac算子) 三元組正確構建 |
| `test_dimension` | 維度計算 | 譜三元組的維數由與 D 的交換子性質決定 |
| `test_order_one_condition` | [a, D] 的有界性 | 對於有限維摩爾斯理論，交換子 [a, D] 必須是有界算子 |
| `test_finiteness_condition` | 有限性條件 | Tr(a[D, b]) 的有限性 |
| `test_absolute_continuity` | 絕對連續性 | D 的譜必須絕對連續 |
| `test_zeta_function` | ζ函數計算 | ζ_D(s) = Σ λ_i^{-s}，用於計算維數譜 |

### 核心性質測試

```python
# 交換子測試：st.commutator(a)
# [a, D]ψ = a(Dψ) - D(aψ)
# 當 D 為乘法算子時，[a, D] 測量 a 與 D 的非交換程度
```

## 3. 循環同調測試（Cyclic Cohomology）

### 數學背景

循環同調是對偶於循環（上）同調的理論，在非交換幾何中起關鍵作用。

**Connes 邊界映射 B**：
```
B: C^n(A) → C^{n-1}(A)
```

**週期循環複形**：
```
... → C^{2n} → C^{2n+1} → C^{2n+2} → ...
```

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_connes_boundary_map` | Connes 邊界映射 B | B 映射是高維循環同調與低維循環同調之間的橋樑 |
| `test_periodic_cyclic_complex` | 週期循環複形 | HH 對偶於週期循環同調 |
| `test_is_cyclic` | 循環性條件 | 循環上鏈滿足 λ(a^0,...,a^n) = (-1)^n λ(a^n,a^0,...,a^{n-1}) |
| `test_chern_character` | Chern 字元 | ch: K^*(A) → HF^*(A) 將 K-理論映射到循環同調 |

## 4. 指數定理測試（Index Theorem）

### 數學背景

Fredholm 指數定理是非交換幾何與指標理論的核心連接。

**Fredholm 指標**：
```
ind(D) = dim(ker D) - dim(coker D)
     = dim(ker D) - dim(ker D*)
```

**Atkinson 定理**：D 是 Fredholm 算子當且僅當 D 在 B(H) 中可逆 modulo 緊算子。

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | FredholmIndex 對象創建 | 存儲待計算指數的算子 |
| `test_compute` | 指數計算 | ind(D) = dim(ker D) - dim(coker D) |
| `test_is_fredholm` | Fredholm 性判定 | 算子具有有限維核與餘核 |
| `test_Atkinson_theorem` | Atkinson 定理驗證 | D 可逆 modulo 緊算子 |
| `test_perturbation_invariance` | 擾動不變性 | 指數在緊算子擾動下不變 |

### 數學公式

```
Atkinson 定理：D 是 Fredholm ⇔ ∃R, K 使得 DR = I + K 或 RD = I + K
其中 R 是 D 的正則化逆，K 是緊算子
```

## 5. Hochschild 同調測試

### 數學背景

Hochschild 同調是研究代數結構的基本工具。

**Hochschild 邊界算子**：
```
b: C^n(A) → C^{n+1}(A)
b(φ)(a^0,...,a^{n+1}) = Σ (-1)^i φ(a^0,...,a^i a^{i+1},...,a^{n+1})
```

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_n_chains` | n-鏈的生成 | C^n(A) = Hom(A^{⊗n}, A) |
| `test_coboundary` | 餘邊界計算 | b(φ) 測量 φ 的「邊界」性質 |
| `test_is_cocycle` | 上循環判定 | φ 是上循環當且僅當 b(φ) = 0 |
| `test_is_coboundary` | 上餘邊界判定 | φ 是上餘邊界當且僅當存在 ψ 使得 φ = b(ψ) |
| `test_hh_class` | 同調類計算 | 提取 HH 類用於分類 |

## 6. K-同調與 Fredholm 模測試

### 數學背景

K-同調是 K-理論的對偶理論，在指標理論中至關重要。

**Fredholm 模**：(A, H, F) 其中 F 是 Fredholm 算子

**指標配對**：
```
<[x], [F]> ∈ Z  或  Z/2
```

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_add_fredholm_module` | 添加 Fredholm 模 | K-同調由 Fredholm 模生成 |
| `test_index_pairing` | 指標配對 | K_0(A) 與 K-同調類的配對 |
| `test_thorn_equality` | ⊙平等性 | 偶與奇 K-同調的關係 |

### Fredholm 模測試

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_is_even` | 偶性判定 | even module: Γ ⊗ A → End(H) 可交換 |
| `test_is_odd` | 奇性判定 | odd module: Γ 是反交換 |
| `test_index` | 指數計算 | Fredholm 模的指數 |
| `test_pair_with_k_theory` | K-理論配對 | K_0 或 K_1 與模的配對 |

## 7. 偽微分算子測試

### 數學背景

偽微分算子是非交換幾何中分析的核心工具。

**符號類**：
```
S^m: 階為 m 的符號
S^{-1}: 緊致算子（Hilbert-Schmidt 之類）
```

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_symbol_class` | 符號類判定 | 符號的階決定算子的漸近行為 |
| `test_compose_with_elliptic` | 橢圓複合 | 符號複合公式：σ(PQ) ~ σ(P)σ(Q) |
| `test_transposed_operator` | 轉置算子 | 轉置不改變階數 |

## 8. Connes-Chern 字元測試

### 數學背景

Connes-Chern 字元將 K-理論與循環同調連接起來：

```
ch: K_*(A) → HC_*(A)
```

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_compute_character` | 字元計算 | 從 Fredholm 模計算循環上同調類 |
| `test_bounded_perturbation` | 有界擾動不變性 | 有界擾動不改變指標 |
| `test_morita_invariance` | Morita 不變性 | Morita 等價代數有相同的循環同調 |

## 9. Dirac 算子測試

### 數學背景

Dirac 算子是流形上橢圓微分算子，在指標理論中核心地位。

**核與餘核**：
```
ker D = {ψ ∈ H : Dψ = 0}
coker D ≅ ker D*
```

### 測試內容

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_kernel_dim` | 核維數 | 零模的維數 |
| `test_cokernel_dim` | 餘核維數 | 補空間維數 |
| `test_apply` | 算子作用 | Dψ 的計算 |

## 10. 測試數學原理總結

```
┌─────────────────────────────────────────────────────────────────┐
│                    非交換幾何測試架構                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Spectral Triple (A, H, D)                                     │
│         │                                                       │
│         ├──→ Dirac Operator D ──→ Fredholm Index               │
│         │         │                    │                        │
│         │         ↓                    ↓                        │
│         │    kernel/coker         index theorem                 │
│         │                                                       │
│   Hochschild Cohomology ←── Connes Chern Character ──→ Cyclic  │
│         │                          │                    Cohomology│
│         ↓                          ↓                    │       │
│   HH Complex              K-Theory ←──→ K-Homology        │       │
│                                               ↓               │       │
│                                          Fredholm Module ─────┘   │
│                                                                 │
│   Pseudodifferential Operators (分析工具)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 核心數學關係

1. **譜三元組 → 指標**：ind(D) ∈ K_*(A)
2. **指標 → 循環同調**：Connes-Chern 字元 ch(ind(D)) ∈ HC_*
3. **循環同調 ↔ Hochschild**：HH_* ≅ HC_*（週期）
4. **K-理論 ↔ K-同調**：配對產生指數
5. **Fredholm 模 → K-同調**：由算子 F 定義

---

*本文件自動生成自測試代碼分析*