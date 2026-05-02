# 形式語言理論 (Formal Languages)

本文件說明 lean4py 形式語言模組背後的數學原理。該模組參考 mathlib4 的 `Mathlib.Computability.Language` 設計，涵蓋正規語言、上下文無關語言等核心概念。

---

## 1. 字母表與字串 (Alphabets and Strings)

### 1.1 字母表 (Alphabet)

**定義**：字母表 Σ 是一個有窮非空集合，其元素稱為符號 (symbols)。

```
Σ = {a, b, c, ...}
```

例如：
- 二進制字母表：Σ = {0, 1}
- 英文字母表：Σ = {a, b, c, ..., z}

### 1.2 字串 (String)

**定義**：字串是由字母表中的符號組成的有窮序列。

- 空字串：ε (長度為 0 的字串)
- 字串長度：|w| 表示字串 w 中符號的個數
- 字串連接：uv 表示將字串 u 和 v 首尾相連

### 1.3 語言 (Language)

**定義**：語言 L 是字母表 Σ 上字串的有窮或無窮集合。

```
L ⊆ Σ*    (其中 Σ* 表示所有可能字串的集合)
```

---

## 2. 喬姆斯基層級結構 (Chomsky Hierarchy)

喬姆斯基層級將形式語言分為四類，從最廣義到最狹義：

| 層級 | 類型 | 文法 | 自動機 | 示例 |
|------|------|------|--------|------|
| Type 0 | 遞迴枚舉語言 | 無限制文法 | 圖靈機 | 通用語言 |
| Type 1 | 上下文相關語言 | 上下文相關文法 | 線性有界自動機 | aⁿbⁿcⁿ |
| Type 2 | 上下文無關語言 | 上下文無關文法 | 下推自動機 | aⁿbⁿ |
| Type 3 | 正規語言 | 正規文法 | 有窮自動機 (DFA/NFA) | a*b+ |

### 2.1 Type 0：無限制文法 (Recursively Enumerable Languages)

**定義**：由無限制文法生成的語言，可被圖靈機枚舉。

**文法形式**：
```
α → β
```
其中 α ∈ (V ∪ Σ)* 且 α 非終結符，β ∈ (V ∪ Σ)*

**特點**：
- 最廣義的語言類別
- 存在判定問題不可判定

### 2.2 Type 1：上下文相關文法 (Context-Sensitive Languages)

**定義**：由上下文相關文法生成的語言。

**文法形式**：
```
αAβ → αγβ
```
其中 A 是終結符，α, β, γ ∈ (V ∪ Σ)*，且 |αAβ| ≤ |αγβ|

**特點**：
- 語言長度單調遞增
- 可被線性有界自動機識別
- 封閉於交集、反轉、同態運算

### 2.3 Type 2：上下文無關文法 (Context-Free Languages)

**定義**：由上下文無關文法生成的語言。

**文法形式**：
```
A → β
```
其中 A 是單一非終結符，β ∈ (V ∪ Σ)*

**特點**：
- 可被下推自動機 (PDA) 識別
- 是程式語言語法的基礎
- 巴克斯-瑙爾形式 (BNF) 的理論基礎

### 2.4 Type 3：正規語言 (Regular Languages)

**定義**：由正規文法生成的語言。

**文法形式**：
```
A → aB  (右線性)
A → Ba  (左線性)
```
其中 A, B 是非終結符，a 是終結符

**特點**：
- 可被有窮自動機 (DFA/NFA) 識別
- 可用正規表達式表示
- 具有良好的封閉性質

---

## 3. 正規表達式與正規語言 (Regular Expressions and Regular Languages)

### 3.1 正規表達式 (Regular Expression)

正規表達式由以下運算構成：

| 運算 | 符號 | 含義 |
|------|------|------|
| 聯集 | a \| b | a 或 b |
| 連接 | ab | a 跟隨 b |
| 克林閉包 | a* | a 重複零次或多次 |

### 3.2 正規語言的封閉性質

正規語言對以下運算封閉：

- 聯集 (Union)
- 連接 (Concatenation)
- 克林閉包 (Kleene star)
- 交集 (Intersection)
- 補集 (Complement)
- 反轉 (Reversal)
- 同態 (Homomorphism)
- 逆同態 (Inverse homomorphism)

### 3.3 有窮自動機 (Finite Automata)

**確定型有窮自動機 (DFA)**：
```
M = (Q, Σ, δ, q₀, F)
```
- Q：狀態集
- Σ：輸入字母表
- δ：轉換函數 Q × Σ → Q
- q₀：初始狀態
- F：接受狀態集

**非確定型有窮自動機 (NFA)**：
```
M = (Q, Σ, δ, q₀, F)
```
其中 δ：Q × Σ → 2^Q (冪集)

**定理**：每個 NFA 都可以轉換為等價的 DFA（子集構造法）。

---

## 4. 上下文無關文法與下推自動機 (Context-Free Grammars and Pushdown Automata)

### 4.1 上下文無關文法 (CFG)

**定義**：文法 G = (V, Σ, R, S)，其中：
- V：非終結符集合
- Σ：終結符集合
- R：產生式規則集合
- S：起始符號

**範例**：
```
G: S → aSb | ε
生成語言：L(G) = {aⁿbⁿ | n ≥ 0}
```

### 4.2 下推自動機 (Pushdown Automata, PDA)

**定義**：
```
P = (Q, Σ, Γ, δ, q₀, Z₀, F)
```
- Q：狀態集
- Σ：輸入字母表
- Γ：堆疊字母表
- δ：轉換函數
- Z₀：初始堆疊符號
- F：接受狀態集

**接受方式**：
- 空堆疊接受
- 最終狀態接受

### 4.3 喬姆斯基正規形式 (CNF)

每個上下文無關語言都可以轉換為喬姆斯基正規形式：

1. 消除 ε-產生式
2. 消除單位產生式
3. 消除無用符號
4. 將產生式化為 A → BC 或 A → a

---

## 5. 剖析樹與歧義性 (Parse Trees and Ambiguity)

### 5.1 剖析樹 (Parse Tree)

給定文法 G，剖析樹是句型推導的樹狀表示：

- 內部節點：非終結符
- 葉節點：終結符或 ε
- 根節點：起始符號 S

### 5.2 歧義性 (Ambiguity)

**定義**：若一個字串有兩棵或以上的不同剖析樹，則稱該文法對此字串是歧義的。

**範例**：
```
文法：E → E + E | E * E | (E) | id
字串：id + id * id
```
此文法無法確定運算的優先順序，導致歧義。

### 5.3 消除歧義

- 重新設計文法（引入優先順序規則）
- 使用歧義性消除技術
- 並非所有歧義都可判定

### 5.4 固有歧義 (Inherent Ambiguity)

存在語言 L，使得所有生成 L 的文法都是歧義的（例如：{aⁿbⁿcᵐdᵐ | n, m ≥ 1} ∪ {aⁿbᵐcᵐdⁿ | n, m ≥ 1}）。

---

## 6. 泵引理 (Pumping Lemma)

### 6.1 正規語言的泵引理

**定理**：若 L 是正規語言，則存在常數 n（泵長度），使得對於任意 w ∈ L 且 |w| ≥ n，可以將 w 分解為 w = xyz：
1. |y| ≥ 1
2. |xy| ≤ n
3. 對所有 i ≥ 0，xyⁱz ∈ L

**用途**：證明某語言不是正規的。

**反例**：證明 L = {aⁿbⁿ | n ≥ 0} 不是正規語言。

### 6.2 上下文無關語言的泵引理

**定理**：若 L 是上下文無關語言，則存在常數 n，使得對於任意 w ∈ L 且 |w| ≥ n，可以將 w 分解為 w = uvxyz：
1. |vy| ≥ 1
2. |vxy| ≤ n
3. 對所有 i ≥ 0，uvⁱxyⁱz ∈ L

**用途**：證明某語言不是上下文無關的。

**反例**：證明 L = {aⁿbⁿcⁿ | n ≥ 0} 不是上下文無關語言。

---

## 7. 語言家族的封閉性質 (Closure Properties of Language Families)

### 7.1 正規語言的封閉性

| 運算 | 是否封閉 |
|------|----------|
| 聯集 | ✓ |
| 交集 | ✓ |
| 補集 | ✓ |
| 連接 | ✓ |
| 克林閉包 | ✓ |
| 反轉 | ✓ |
| 同態 | ✓ |
| 逆同態 | ✓ |

### 7.2 上下文無關語言的封閉性

| 運算 | 是否封閉 |
|------|----------|
| 聯集 | ✓ |
| 交集 | ✗ (與正規語言交集) |
| 補集 | ✗ |
| 連接 | ✓ |
| 克林閉包 | ✓ |
| 反轉 | ✓ |
| 同態 | ✓ |
| 逆同態 | ✓ |

### 7.3 上下文相關語言的封閉性

| 運算 | 是否封閉 |
|------|----------|
| 聯集 | ✓ |
| 交集 | ✓ |
| 補集 | ✓ |
| 連接 | ✓ |
| 克林閉包 | ✓ |
| 反轉 | ✓ |
| 同態 | ✓ |
| 逆同態 | ✓ |

### 7.4 遞迴枚舉語言的封閉性

| 運算 | 是否封閉 |
|------|----------|
| 聯集 | ✓ |
| 交集 | ✓ |
| 補集 | ✗ |
| 連接 | ✓ |
| 克林閉包 | ✓ |
| 反轉 | ✓ |
| 同態 | ✓ |
| 逆同態 | ✓ |

---

## 8. lean4py 模組使用範例

```python
from lean4py.formal_languages import (
    RegularLanguage,
    ContextFreeGrammar,
    ChomskyHierarchy,
    PumpingLemma
)

# 正規語言
lang = RegularLanguage.from_regex("a*b+")
print(RegularLanguage.is_regular("a*b+"))  # True

# 上下文無關文法
cfg = ContextFreeGrammar(
    variables=['S'],
    terminals=['a', 'b'],
    rules={'S': ['aSb', '']},
    start='S'
)
print(cfg.generates('aabb'))  # True

# 喬姆斯基層級
print(ChomskyHierarchy.level("aⁿbⁿ"))  # 2 (上下文無關)

# 泵引理
print(PumpingLemma.for_regular("a*b+"))  # True
print(PumpingLemma.for_context_free("aⁿbⁿ"))  # True
```

---

## 參考文獻

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
2. Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
3. Kozen, D. C. (1997). *Automata and Computability*. Springer.
4. mathlib4 Documentation: Mathlib.Computability.Language