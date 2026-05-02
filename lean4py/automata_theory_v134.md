# 自動機理論 v1.34 (automata_theory_v134)

## 概述

本模組基於 mathlib4 的 `Mathlib.Computability.Automaton`，提供確定的有限自動機 (DFA)、非確定有限自動機 (NFA)、下推自動機 (PDA) 和圖靈機 (TM) 的基本實現。

---

## v1.34 版本與原版 (automata_theory.py) 的差異

### 設計簡化

| 特性 | 原版 automata_theory.py | v1.34 版本 |
|------|------------------------|-----------|
| 資料結構 | `Set[str]` | `List[str]` |
| 轉換函數 | `Dict[Tuple[str, str], str]` | 相同 |
| 實現完整性 | 完整可運行的邏輯 | 簡化骨架實現 (返回 `True`) |
| 類數量 | 13 個類 | 4 個類 |

### v1.34 精簡的類

原版包含以下擴展類，v1.34 版本未包含：

1. **FSM** - 有限狀態機基類
2. **MealyMachine** - Mealy 機（輸出依賴於狀態和輸入）
3. **MooreMachine** - Moore 機（輸出僅依賴於狀態）
4. **RegularExpression** - 正則表達式類
5. **Grammar** - 形式文法類
6. **ChomskyHierarchy** - Chomsky 文法層級分類
7. **PumpingLemma** - 泵引理（正則語言）
8. **KleeneStar** - Kleene 星號運算

### v1.34 保留的類

| 類名 | 形式定義 | 說明 |
|------|---------|------|
| DFA | (Q, Σ, δ, q₀, F) | 確定有限自動機 |
| NFA | (Q, Σ, δ, q₀, F) | 非確定有限自動機 |
| PushdownAutomaton | (Q, Σ, Γ, δ, q₀, Z₀, F) | 下推自動機 |
| TuringMachine | (Q, Σ, Γ, δ, q₀, q_accept, q_reject) | 圖靈機 |

---

## 自動機類型數學定義

### 1. 確定有限自動機 (DFA)

**定義：** 五元組 M = (Q, Σ, δ, q₀, F)

- Q：有限狀態集
- Σ：輸入字母表
- δ：Q × Σ → Q 轉換函數
- q₀ ∈ Q：起始狀態
- F ⊆ Q：接受狀態集

**語言識別：** M 接受字符串 w 當且僅當從 q₀ 開始，依次應用 δ 後到達接受狀態。

### 2. 非確定有限自動機 (NFA)

**定義：** 五元組 M = (Q, Σ, δ, q₀, F)

- δ：Q × Σ → 2^Q（冪集）轉換函數
- 接受字符串 w 當存在某條計算路徑到達接受狀態

**ε-閉包：** 用於處理空字符串轉換
```
ε-closure(S) = S ∪ {從 S 中狀態經過任意數量 ε 轉換可達的狀態}
```

### 3. 下推自動機 (PDA)

**定義：** 七元組 M = (Q, Σ, Γ, δ, q₀, Z₀, F)

- Γ：堆疊字母表
- Z₀ ∈ Γ：初始堆疊符號
- δ：Q × (Σ ∪ {ε}) × Γ → Q × Γ* 轉換函數

**兩種接受方式：**
- 按最終狀態接受：到達 F 中的狀態
- 按空堆疊接受：堆疊為空

### 4. 圖靈機 (TM)

**定義：** 八元組 M = (Q, Σ, Γ, δ, q₀, B, F_accept, F_reject)

- B ∈ Γ：空白符號
- δ：Q × Γ → Q × Γ × {L, R} 轉換函數
- F_accept：接受狀態集
- F_reject：拒絕狀態集

---

## 形式語言理論進階主題

### Chomsky 層級

```
Type 0 (無限制文法)     ⊇  Type 1 (上下文敏感)
                                     ⊇  Type 2 (上下文無關)
                                             ⊇  Type 3 (正則文法)
```

| 類型 | 文法規則形式 | 對應自動機 |
|------|------------|-----------|
| Type 0 | α → β (α, β ∈ (V∪Σ)*) | 圖靈機 |
| Type 1 | αAβ → αγβ | 線性界限自動機 |
| Type 2 | A → γ | 下推自動機 |
| Type 3 | A → aB 或 A → a | 有限自動機 |

### 正則語言性質

1. **封閉性：** 並集、交集、補集、連接、Kleene 星號
2. **泵引理：** 存在 n，任意長度 ≥ n 的字符串可分解為 xyz
3. **Myhill-Nerode 定理：** 右不变等价關係與狀態數的關係

### 上下文無關語言

1. **泵引理：** 適用於上下文無關語言
2. **Greibach 范式：** 消除左遞歸
3. **CYK 算法：** O(n³) 句法分析

### 可計算性理論

1. **通用圖靈機：** 可類比任何其他圖靈機
2. **停機問題：** 不可判定
3. **Church-Turing 論題：** 算法直觀概念與圖靈機等价

---

## 使用範例

```python
# DFA 示例
dfa = DFA(
    states=['q0', 'q1', 'q2'],
    alphabet=['0', '1'],
    transition={('q0', '0'): 'q0', ('q0', '1'): 'q1', ...},
    start='q0',
    accept=['q2']
)

# NFA 轉換為 DFA
nfa = NFA(...)
equivalent_dfa = nfa.to_dfa()

# 圖靈機
tm = TuringMachine(...)
if tm.halts(tm, input_str):
    # 處理停機情況
```

---

## 參考

- mathlib4: `Mathlib.Computability.Automaton`
- Hopcroft-Ullman: *Introduction to Automata Theory, Languages, and Computation*
- Sipser: *Introduction to the Theory of Computation*