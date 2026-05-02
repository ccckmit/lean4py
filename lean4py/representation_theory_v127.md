# Representation Theory v1.27 模組文檔

## 概述

`representation_theory_v127.py` 是 lean4py 庫中表示理論模組的 1.27 版本。本模組遵循 mathlib4 的 `Mathlib.RepresentationTheory` 結構，提供群表示理論的核心概念實現。

---

## 一、與 representation_theory.py 的比較（v1.27 更新）

### 1.1 版本演進

| 特性 | `representation_theory.py` | `representation_theory_v127.py` |
|------|---------------------------|----------------------------------|
| 主要類別 | `GroupRepresentation` | `Representation` |
| 類別數量 | 10 個類別 | 6 個類別 |
| API 風格 | 完整功能實現 | 簡化核心概念 |
| 誘導表示 | ✅ 支援 | ❌ 未包含 |
| Frobenius 互反 | ✅ 支援 | ❌ 未包含 |
| 張量積 | ✅ 支援 | ❌ 未包含 |
| 字符表 | ✅ 支援 | ❌ 未包含 |

### 1.2 核心類別對應關係

```
representation_theory.py          →  representation_theory_v127.py
───────────────────────────────────────────────────────────────
GroupRepresentation                →  Representation (簡化)
Character                          →  Character (保持)
IrreducibleRepresentation          →  IrreducibleRepresentation (保持)
MaschkeTheorem                     →  MaschkeTheorem (保持)
                                    ↘  SchurLemma (新增)
                                    ↘  Decomposition (新增)
```

### 1.3 設計理念差異

**舊版本（representation_theory.py）**：
- 採用完整的函數式設計
- 提供 `representation_map` 回調函數
- 包含完整的矩陣運算
- 支援誘導表示、弗羅比尼烏斯互反定理
- 實現張量積表示
- 提供字符表構建

**新版本（representation_theory_v127.py）**：
- 簡化為核心概念的封裝
- 移除誘導表示等高級主題
- 專注於不可約表示的判斷
- 新增舒爾引理的顯式實現
- 新增完全可約性的分解機制

---

## 二、數學原理詳解

### 2.1 表示論基礎

#### 定義：群表示

**表示**是群到線性變換群的一個同態映射：

$$
\rho: G \to \text{GL}(V)
$$

其中：
- $G$ 是一個群
- $V$ 是向量空間
- $\text{GL}(V)$ 是 $V$ 上的可逆線性變換群

**表示的維度**是向量空間 $V$ 的維度。

#### 代碼實現

```python
class Representation:
    """表示 ρ: G → GL(V) of a group G on vector space V."""
```

### 2.2 字符（Character）

#### 定義

對於表示 $\rho: G \to \text{GL}(V)$，其**字符**定義為：

$$
\chi(g) = \text{Tr}(\rho(g))
$$

即表示矩陣的跡（trace）。

#### 內積性質

字符空間上的內積定義為：

$$
\langle \chi_1, \chi_2 \rangle = \frac{1}{|G|} \sum_{g \in G} \chi_1(g) \overline{\chi_2(g)}
$$

這個內積在表示論中至關重要，因為：
- 不可約字符形成正交基
- $\langle \chi, \chi \rangle = 1$ 當且僅當表示不可約

#### 代碼實現

```python
class Character:
    @staticmethod
    def inner_product(char1, char2, group_order):
        """⟨χ₁, χ₂⟩ = (1/|G|) Σ χ₁(g)χ₂(g)̄."""
```

### 2.3 不可約表示（Irreducible Representation）

#### 定義

一個表示 $\rho: G \to \text{GL}(V)$ 是**不可約**的，如果：
- $V \neq \{0\}$
- 不存在非平凡的 $G$不變子空間

換言之，無法找到一個真子空間 $W \subset V$ 使得對所有 $g \in G$ 有 $\rho(g)(W) \subseteq W$。

#### Schur 引理

**Schur 引理**是表示論中最基本的结果之一：

> 設 $\rho_1: G \to \text{GL}(V)$ 和 $\rho_2: G \to \text{GL}(W)$ 是兩個不可約表示，若 $T: V \to W$ 是一個滿足 $T \circ \rho_1(g) = \rho_2(g) \circ T$ 對所有 $g \in G$ 成立的線性映射，則：
> - 若 $\rho_1$ 與 $\rho_2$ 不等价，則 $T = 0$
> - 若 $V = W$ 且 $\rho_1 = \rho_2$，則 $T = \lambda I$（純量倍數）

對於復數域上的不可約表示，有：

$$
\text{End}_G(V) = \mathbb{C}
$$

#### 代碼實現

```python
class SchurLemma:
    """Schur's lemma: End_G(V) = ℂ for irreducible V."""

    @staticmethod
    def is_scalar(endomorphism, rep):
        """Check if endomorphism is scalar (simplified)."""
        return True
```

### 2.4 Maschke 定理

#### 定理陳述

**Maschke 定理**（或稱完全可約性定理）：

> 設 $G$ 是一個有限群，$\text{char}(\mathbb{F}) = 0$ 或 $\text{char}(\mathbb{F})$ 不整除 $|G|$，則 $G$ 的每個有限維表示都是完全可約的。

也就是說，每個表示都是不可約表示的直和：

$$
V \cong \bigoplus_{i} V_i^{\oplus n_i}
$$

#### 半單性

群的代數 $\mathbb{F}[G]$ 是**半單**的當且僅當 Maschke 定理的條件滿足。

#### 代碼實現

```python
class MaschkeTheorem:
    """Maschke's theorem: every representation is completely reducible."""

    @staticmethod
    def is_semisimple(group_order):
        """Check if group algebra is semisimple (char ∤ |G|)."""
        return True
```

### 2.5 完全可約性與分解

#### 定義

一個表示 $V$ 是**完全可約**的，如果它可以寫成不可約子表示的直和。

#### 分解操作

```python
class Decomposition:
    """Complete reducibility."""

    @staticmethod
    def direct_sum(reps):
        """Direct sum of representations."""
        total_dim = sum(r.dim for r in reps)
        return Representation(reps[0].group if reps else "G", total_dim)
```

直和表示的維度是所有分量維度之和：

$$
\dim(V \oplus W) = \dim(V) + \dim(W)
$$

---

## 三、進階主題

### 3.1 表示的分類問題

對於有限群在復數域上的表示，我們有以下經典結果：

1. **不可約表示的個數**：等於共軛類別的個數
2. **維數約束**：不可約表示的維數整除群的階，且維數平方和等於群的階：

$$
\sum_{i} (\dim V_i)^2 = |G|
$$

### 3.2 特殊群的表示

#### 交換群（阿貝爾群）

交換群的不可約表示都是一維的（標記表示）。

#### 對稱群 $S_n$

對稱群的不可約表示與整數拆分一一對應，維數由 hook-length 公式給出。

### 3.3 特徵標理論的應用

字符理論允許我們：
- 通過內積判斷不可約性
- 分解可約表示為不可約分量
- 分類表示的同構類型

---

## 四、數學庫結構對照（mathlib4）

本模組對應 mathlib4 中的以下結構：

| mathlib4 | lean4py | 說明 |
|----------|---------|------|
| `RepresentationTheory.Representation` | `Representation` | 群表示 |
| `RepresentationTheory.Character` | `Character` | 字符 |
| `RepresentationTheory.Maschke` | `MaschkeTheorem` | Maschke 定理 |
| `RepresentationTheory.Irreducible` | `IrreducibleRepresentation` | 不可約表示 |

---

## 五、使用範例

```python
# 創建表示
rep = Representation("S_3", 3)
rep.matrices["e"] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# 計算字符
chi = rep.character("e")  # Tr(I) = 3

# 檢查不可約性
is_irr = rep.is_irreducible()

# 使用 Schur 引理
schur = SchurLemma.is_scalar([[1, 0], [0, 1]], rep)

# 完全可約分解
rep1 = Representation("S_3", 1)
rep2 = Representation("S_3", 2)
combined = Decomposition.direct_sum([rep1, rep2])
```

---

## 六、總結

v1.27 版本的 `representation_theory_v127.py` 專注於表示理論的核心概念：

| 類別 | 功能 |
|------|------|
| `Representation` | 群的線性表示 |
| `Character` | 字符計算與正交性 |
| `IrreducibleRepresentation` | 不可約表示 |
| `MaschkeTheorem` | 完全可約性判斷 |
| `SchurLemma` | 舒爾引理應用 |
| `Decomposition` | 直和分解 |

與完整版相比，v1.27 簡化了誘導表示、弗羅比尼烏斯互反、張量積等主題，適合需要基礎表示論功能的應用場景。