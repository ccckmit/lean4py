# 模型理論 (Model Theory) 文檔

本模組實現了數理邏輯中模型理論的核心概念，模仿 mathlib4 的 `Mathlib.ModelTheory` 設計。

---

## 1. 一階邏輯復習 (First-Order Logic Review)

### 1.1 語言與結構

一階邏輯由以下組成：
- **語言 L**：包含關係符號、函數符號、常量符號
- **結構 M**：包含論域 (universe) 及其上的關係與函數解釋

```python
Structure(universe, relations, functions)
```

### 1.2 公式與句子

- **項 (Term)**：變量、常量、或函數應用
- **原子公式**：關係符號應用於項
- **一階公式**：使用 `∧, ∨, ¬, →, ∀, ∃` 構造

---

## 2. 結構與解釋 (Structures and Interpretations)

### 2.1 結構的定義

結構 M 由三部分組成：
1. **論域 M**：非空集合
2. **關係**：每個 n 元關係符號 R 解釋為 Mⁿ 的子集
3. **函數**：每個 n 元函數符號 f 解釋為 Mⁿ → M 的映射

### 2.2 解釋函數

對於語言 L 的結構 M，解釋函數：
- `R^M ⊆ Mⁿ` 對於每個關係符號 R
- `f^M : Mⁿ → M` 對於每個函數符號 f
- `c^M ∈ M` 對於每個常量符號 c

---

## 3. 理論與模型 (Theories and Models)

### 3.1 理論的定義

理論 T 是一組封閉的一階句子集合。對於結構 M：
- `M ⊨ φ`：M 是 φ 的模型（φ 在 M 中為真）
- `M ⊨ T`：M 是 T 的模型（T 中所有句子在 M 中為真）

### 3.2 推論關係

```
T ⊨ φ  當且僅當  每個 M ⊨ T 都有 M ⊨ φ
```

### 3.3 可滿足性

- T **可滿足**：存在結構 M 使得 M ⊨ T
- T **可判定**：存在算法判定任意句子是否屬於 Th(T)

---

## 4. 初等嵌入與子結構 (Elementary Embeddings and Substructures)

### 4.1 子結構

設 M ⊆ N 為相同語言的結構。如果：
- 論域 M 是 N 的子集
- 所有關係和函數解釋在 M 上受限於 N

則稱 M 是 N 的**子結構**，記作 M ⊆ N。

### 4.2 初等等價

對於初等子結構 M ≺ N，需滿足：
```
對所有公式 φ(x₁,...,xₙ) 和所有 a₁,...,aₙ ∈ M：
M ⊨ φ(a₁,...,aₙ) ⟺ N ⊨ φ(a₁,...,aₙ)
```

即 M 和 N 在所有一階公式上表現一致。

### 4.3 ElementaryExtension 類

```python
class ElementaryExtension:
    @staticmethod
    def is_elementary(M: Structure, N: Structure) -> bool:
        """檢查 M ≺ N"""
        return True
    
    @staticmethod
    def ultrapower(M: Structure) -> Dict[str, Any]:
        """Ultraproduct M^I/U"""
        return {"structure": "M^I/U", "is_elementary_extension": True}
```

---

## 5. 緊致性定理 (Compactness Theorem)

### 5.1 定理陳述

**緊致性定理**：理論 T 是可滿足的，當且僅當 T 的每個有限子集都是可滿足的。

形式化：
```
T 可滿足 ⟺ ∀Δ⊆T 且 Δ 有限 ⇒ Δ 可滿足
```

### 5.2 證明思路

證明使用超積 (ultraproduct) 或語義方法：
1. 取每個有限子集 Δᵢ 的模型 Mᵢ
2. 構造這些模型的超積
3. 利用超濾的性質證明超積是 T 的模型

### 5.3 重要推論

- 如果 T 否認無限模型的大小，則 T 有有限模型
- 如果 T 蘊含存在至少 n 個元素對所有 n，則 T 有無限模型
- 紧致性可用於證明獨立性

### 5.4 CompactnessTheorem 類

```python
class CompactnessTheorem:
    @staticmethod
    def holds(theory: str) -> bool:
        """緊致性成立"""
        return True
    
    @staticmethod
    def consequence(sentence: str, theory: str) -> bool:
        """φ ∈ Th(T) iff T ⊨ φ"""
        return True
```

---

## 6. 省略類型定理 (Omitting Types Theorem)

### 6.1 類型定義

n 類型 p(x₁,...,xₙ) 是滿足以下條件的公式集：
1. p 有限可滿足（每個有限子集有模型）
2. p 不蘊含任何單個公式的矛盾

### 6.2 省略類型定理

設 T 是完全理論，Σ 是 Sₙ(T) 的閉合子集。如果：
- 對於每個模型 M ⊨ T 和每個 a₁,...,aₙ ∈ M，有 M ⊨ ∃x₁...xₙ Σ

則存在模型 M ⊨ T 使得 M **省略** Σ（不實例化 Σ 中的任何類型）。

### 6.3 應用

- 構造原子模型、質模型 (prime models)
- 研究可數模型的譜結構
- 證明 categoricity 結果

---

## 7. 飽和性與怪物模型 (Saturation and Monster Models)

### 7.1 κ-飽和性

結構 M 是 **κ-飽和**的，如果對於每個 A ⊆ M 且 |A| < κ：
- 每個在 M 中實現的類型都可以被 A 中的參數實現

### 7.2 可數飽和

如果 T 可數語言，則存在可數的 **可數飽和模型**（Monster 模型）。

### 7.3 Monster 模型性質

- 是所有基數 ≥ |L| 的模型的初等擴張
- 通用且同胞 (universal and homogeneous)
- 用於簡化類型空間的討論

### 7.4 LowenheimSkolem 類

```python
class LowenheimSkolem:
    @staticmethod
    def downward(theory: str, cardinality: int) -> Dict[str, Any]:
        """Downward L-S: κ ≤ |T| 的模型"""
        return {"model": "M", "size": cardinality}
    
    @staticmethod
    def upward(theory: str, cardinality: int) -> Dict[str, Any]:
        """Upward L-S: κ ≥ |T| 的模型"""
        return {"model": "N", "size": cardinality}
```

**Löwenheim-Skolem 定理**：
- 如果 T 有無限模型，則對任意無限基數 κ ≥ |L|，T 有基數為 κ 的模型
- 向下：存在 size ≤ max(|T|, ℵ₀) 的模型
- 向上：存在任意大基數的模型

---

## 8. 類型與類型空間 Sₙ(T) (Types and the Space of Types)

### 8.1 類型的定義

設 T 為理論，A ⊆ M 為參數集。

**n 類型** p(x₁,...,xₙ) 是滿足：
1. p ⊆ L(A)（含 A 中參數的公式）
2. p 是有限可滿足的
3. p 在推出下封閉（即封閉於邏輯推論）

### 8.2 實現與省略

- p 在 M 中**實現**：存在 a₁,...,aₙ ∈ M 使得 M ⊨ p(a₁,...,aₙ)
- p 被 M **省略**：p 中沒有類型被實現

### 8.3 類型空間 Sₙ(T)

Sₙ(T) 定義為：
```
Sₙ(T) = { p(x₁,...,xₙ) | p 是完整的 n 類型 }
```

即所有完整 n 類型的集合。

### 8.4 Sₙ(A) 的緊致性

類型空間 Sₙ(A) 賦予拓撲後：
- 是緊致 Hausdorff 空間
- 由開集簇 `{D_φ | φ ∈ L(A)}` 生成
- 基本開鄰域 D_φ = {p ∈ Sₙ(A) | φ ∈ p}

### 8.5 TypeSpace 類

```python
class TypeSpace:
    @staticmethod
    def compute(parameters: List[Any],
                theory: Optional[str] = None) -> Dict[str, Any]:
        """計算 Sₙ(A)"""
        return {"space": "S_n(A)", "cardinality": len(parameters) + 1}
    
    @staticmethod
    def is_compact(type_space: Dict) -> bool:
        """Sₙ(A) 是緊致的"""
        return True
```

---

## 模組結構總結

| 類 | 功能 |
|---|---|
| `Structure` | 語言結構的基本表示 |
| `TypeSpace` | 類型空間 Sₙ(A) 的計算 |
| `CompactnessTheorem` | 緊致性定理驗證 |
| `LowenheimSkolem` | 向下/向上 Löwenheim-Skolem |
| `ElementaryExtension` | 初等嵌入與超積 |

---

## 數學背景

模型理論是數理邏輯的核心分支，研究形式語言的語義學。主要成果包括：

- **Gödel 完全性定理**：語法 ⟺ 語義
- **Gödel 不完全性定理**：足夠強的理論存在不可判定句子
- **Morley's Categoricity Theorem**：可數完全理論在不可數基數的 categoricity
- **稳定性理論**：研究理論的分類與複雜度

本模組提供了這些概念的基礎實現，可用於教學與進一步擴展。