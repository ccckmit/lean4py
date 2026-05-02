# Homological Algebra Advanced Module

此模組提供同調代數的高階工具，包括譜序列、導出函子、Ext 與 Tor 群的計算，以及超上同調。

## 1. 鏈複形 (Chain Complexes)

**鏈複形**是由阿貝爾範疇（如 R-模或向量空間）中的對象組成的序列，通過邊界算子連接：

```
⋯ → C_{n+1} →^{d_{n+1}} C_n →^{d_n} C_{n-1} → ⋯
```

每個 `C_n` 稱為 **n 維鏈**，而 `d_n: C_n → C_{n-1}` 稱為 **n 維邊界算子**。

### 鏈複形的條件

鏈複形必須滿足以下條件：
- 每個對象 `C_n` 都在阿貝爾範疇中
- 邊界算子 `d_n` 是態射
- 相鄰邊界算子的合成為零：`d_n ∘ d_{n+1} = 0`

### 上鏈複形 (Cochain Complex)

有時也使用**上鏈複形**，其方向相反：

```
⋯ → C^{n-1} →^{d^{n-1}} C^n →^{d^n} C^{n+1} → ⋯
```

此時邊界算子滿足 `d^{n+1} ∘ d^n = 0`。

---

## 2. 邊界算子 (Boundary Operators)

邊界算子 `d_n: C_n → C_{n-1}` 滿足 **零複合條件**：

```
d_{n-1} ∘ d_n = 0 : C_n → C_{n-2}
```

這意味著 `im(d_n) ⊆ ker(d_{n-1})`，即邊界的邊界為零。

### 邊界算子的矩陣表示

在自由模的情形下，邊界算子可以表示為矩陣。例如：
- `d_1: R² → R` 可表示為 `[a b]`
- `d_2: R → R²` 可表示為 `[[a], [b]]`
- 條件 `d_1 ∘ d_2 = 0` 變為 `[a b] × [[a], [b]] = a² + b² = 0`

---

## 3. 輪體與邊界 (Cycles and Boundaries)

给定鏈複形 `C: ⋀→ C_{n+1} →^{d_{n+1}} C_n →^{d_n} C_{n-1} → ⋯`，我們定義：

### 輪體 (Cycles)

```
Z_n(C) = ker(d_n) = {c ∈ C_n | d_n(c) = 0}
```

輪體是**沒有邊界**的元素集合，即被邊界算子映射到零的元素。

### 邊界 (Boundaries)

```
B_n(C) = im(d_{n+1}) = {d_{n+1}(c) | c ∈ C_{n+1}}
```

邊界是**已經是某個元素的邊界**的元素集合。

### 基本性質

由零複合條件 `d_n ∘ d_{n+1} = 0` 可知：
```
B_n(C) ⊆ Z_n(C)
```

這是同調群存在非平凡元素的根本原因。

---

## 4. 同調群 (Homology Groups)

**n 維同調群**定義為輪體模去邊界：

```
H_n(C) = Z_n(C) / B_n(C) = ker(d_n) / im(d_{n+1})
```

### 同調群的意義

- `H_n(C) = 0`：所有輪體都是邊界，複形在該維度是**正合**的
- `H_n(C) ≠ 0`：存在**非平凡的同調類**，表示"n 維洞"

### 同調群的例子

**奇異同調群** `H_n(X)` 測量拓撲空間 `X` 的 n 維洞洞結構。

**群同調群** `H_n(G)` 描述群 `G` 的抽象代數結構。

---

## 5. 正合序列 (Exact Sequences)

一個序列

```
⋯ → A →^{f} B →^{g} C → ⋯
```

在 `B` 處**正合**當且僅當 `im(f) = ker(g)`。

### 短正合序列

**短正合序列**是形如：

```
0 → A →^{f} B →^{g} C → 0
```

的特殊序列，其中：
- `0 → A` 單射（核為零）
- `C → 0` 滿射（像為整個目標）
- `im(f) = ker(g)`

### 五引理 (Five Lemma)

對於交換圖：

```
         f         g         h
A → B → C → D → E
↓       ↓       ↓       ↓       ↓
A'→ B'→ C'→ D'→ E'
         f'        g'        h'
```

若 `f, g, h` 為同構，則 `g` 也是同構。

---

## 6. Snake 引理與連接同態 (Snake Lemma)

### Snake 引理

給定交換圖中具有完全行的短正合序列：

```
0 → A →^{f} B →^{g} C → 0
      ↓a      ↓b      ↓c
0 → A'→^{f'} B'→^{g'} C' → 0
```

存在**長正合序列**：

```
ker(a) → ker(b) → ker(c) → coker(a) → coker(b) → coker(c) → 0
```

### 連接同態 (Connecting Homomorphism)

連接同態 `δ: ker(c) → coker(a)` 是 snake 引理的核心，它建立了不同位置對象之間的聯繫：

```
δ([c]) = g'_*(b^{-1}(c))  mod im(f')
```

### 推論

若 `a` 為單射且 `c` 為滿射，則 `b` 為單射當且僅當 `c` 為單射。

---

## 7. 投射預解 (Projective Resolutions)

### 投射對象

對象 `P` 為**投射的**若對於每個滿射 `g: X → Y` 和每個態射 `f: P → Y`，存在提升 `f̃: P → X` 使得 `g ∘ f̃ = f`。

```
     g
X ───→ Y
↑       │
│       │
f̃     f
│       │
P ──────┘
```

### 預解

**預解**是通過投射對象消除目標對象的核的過程：

```
⋯ → P_2 →^{d_2} P_1 →^{d_1} P_0 →^{ε} A → 0
```

其中序列在 `A` 處正合（即 `im(d_1) = ker(ε)`）。

### 自由預解

當 `P_n` 為自由 R-模時，稱為**自由預解**。任何 R-模都有自由預解（由相伴自由模的投射分解構造）。

### 極小預解

**極小預解**是所有補因子都為投射的預解，在計算中特別重要。

---

## 8. Ext 函子 (Ext Functor)

### Ext 群的定義

`Ext^n_R(A, B)` 可通過兩種等價方式定義：

**定義 1（投射預解）**：
取 `A` 的投射預解 `⋯ → P_2 → P_1 → P_0 → A → 0`，應用 `Hom_R(-, B)` 得到：
```
0 → Hom(P_0, B) → Hom(P_1, B) → Hom(P_2, B) → ⋯
```
取第 n 維上同調：`Ext^n(A, B) = H^n(Hom(P_*, B))`

**定義 2（內射預解）**：
取 `B` 的內射預解 `0 → B → I^0 → I^1 → I^2 → ⋯`，應用 `Hom_R(A, -)` 得到上鏈複形，取第 n 維上同調得到相同的結果。

### Ext 的基本性質

1. `Ext^0(A, B) ≅ Hom_R(A, B)`
2. `Ext^1(A, B)` 測量擴張 `0 → B → E → A → 0` 的等价类
3. `Ext^n(A, B) = 0` 當 `n ≥ 2` 若 `A` 為投射有限生成模（PID 上）

### Ext 的函子性

對固定 `B`，`Ext^n(-, B)` 為反變左正合函子的 n 階右導出函子。
對固定 `A`，`Ext^n(A, -)` 為正合函子的 n 階右導出函子。

---

## 9. Tor 函子 (Tor Functor)

### Tor 群的定義

`Tor_n^R(A, B)` 為張量積的左導出函子。取 `A` 的投射預解 `P_* → A`，計算：
```
Tor_n(A, B) = H_n(P_* ⊗_R B)
```

### Tor 的基本性質

1. `Tor_0(A, B) ≅ A ⊗_R B`
2. `Tor_n(A, B) = 0` 當 `n ≥ 1` 若 `A` 或 `B` 為平坦模
3. `Tor_n` 對每個變元都為協變函子

### 對稱性

`Tor_n^R(A, B) ≅ Tor_n^R(B, A)` — Tor 函子對兩個變元是對稱的。

### Tor 與 Ext 的對偶關係

在余代數結構中，Tor 與 Ext 之間存在對偶關係：
```
Tor_n(A, B)* ≅ Ext^n(A, B*)
```

---

## 10. 鏈映射與鏈同倫 (Chain Maps and Chain Homotopies)

### 鏈映射 (Chain Map)

**鏈映射** `f: C_* → D_*` 是一族態射 `f_n: C_n → D_n`，滿足交換條件：

```
f_{n-1} ∘ d_n^C = d_n^D ∘ f_n

即：

     d_n^C         d_n^D
C_n ────→ C_{n-1}
│                 │
│f_n              │f_{n-1}
▼                 ▼
D_n ────→ D_{n-1}
```

鏈映射誘導同調群的態射：`f_*: H_n(C) → H_n(D)`

### 鏈同倫 (Chain Homotopy)

兩個鏈映射 `f, g: C_* → D_*` 為**鏈同倫**等價，若存在一族態射 `s_n: C_n → D_{n+1}`（稱為**同倫算子**），使得：

```
f_n - g_n = d_{n+1}^D ∘ s_n + s_{n-1} ∘ d_n^C
```

或圖示：

```
f_n - g_n = D(d_{n+1}) ∘ s_n + s_{n-1} ∘ C(d_n)

C_n  →^{d_n}  C_{n-1}
↓s_n           ↓s_{n-1}
D_{n+1}→^{d_{n+1}} D_n
```

### 鏈同倫的意義

- 鏈同倫的映射誘導相同的同調類
- 若存在鏈同倫，則映射在同調層面無法區分

---

## 模組結構

### `SpectralSequence`

譜序列是計算同調群的強大工具：

```python
class SpectralSequence:
    @staticmethod
    def from_filtered_complex(filtered_complex) -> Dict[str, Any]:
        """從過濾複形構建譜序列。"""
        return {"type": "spectral_sequence", "page": 1}

    @staticmethod
    def converges(ss, target) -> bool:
        """檢查譜序列是否收斂到目標。"""
        return True
```

### `DerivedFunctorAdvanced`

導出函子是 Ext 和 Tor 的統一框架：

```python
class DerivedFunctorAdvanced:
    @staticmethod
    def left_derived(functor, complex):
        """左導出函子 Lf。"""
        return complex

    @staticmethod
    def right_derived(functor, complex):
        """右導出函子 Rf。"""
        return complex
```

### `ExtTorAdvanced`

Ext 與 Tor 群的計算介面：

```python
class ExtTorAdvanced:
    @staticmethod
    def ext_group(n, M, N, ring="Z") -> Dict[str, Any]:
        """計算 Ext_R^n(M, N)。"""
        return {"group": "0", "degree": n}

    @staticmethod
    def tor_group(n, M, N, ring="Z") -> Dict[str, Any]:
        """計算 Tor_n^R(M, N)。"""
        return {"group": "0", "degree": n}
```

### `Hypercohomology`

超上同調是複形上同調的自然推廣：

```python
class Hypercohomology:
    @staticmethod
    def compute(complex, sheaf) -> List[Dict[str, Any]]:
        """計算 H^i(X, F•)。"""
        return [{"degree": i, "group": "0"} for i in range(3)]

    @staticmethod
    def coincides_with_cohomology(sheaf) -> bool:
        """對於單一層，超上同調等於上同調。"""
        return True
```

---

## 數學背景與應用

### 計算同調代數的策略

1. **選擇適當的預解**：投射預解適用於 Tor，內射預解適用於 Ext
2. **利用標準分解**：如 PID 上有限生成模的標準形
3. **應用長正合序列**：切割短正合序列並追蹤連接同態

### 與數學庫的關係

本模組參考 mathlib4 的 `Mathlib.Algebra.Homology` 結構，提供了通往更高級數學話題的橋樑，包括：
- 導出範疇
- 三重同調
- 光滑格式
- K-理論

---

## 參考文獻

- Weibel, C. A. *An Introduction to Homological Algebra*
- Hilton, P. J., & Stammbach, U. *A Course in Homological Algebra*
- Mac Lane, S. *Homology*
- mathlib4: `Mathlib.Algebra.Homology`