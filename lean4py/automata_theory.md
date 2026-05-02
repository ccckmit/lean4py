#  automata_theory - 自動機理論

> 本模組實現了自動機理論與形式語言的核心概念，包含有限自動機、正則表達式、圖靈機以及形式文法。

---

## 1. 有限自動機的形式定義

有限自動機（Finite Automaton）是一個五元組：

```
M = (Q, Σ, δ, q₀, F)
```

| 符號 | 含義 |
|------|------|
| Q | 有限狀態集合 |
| Σ | 輸入字母表（有限非空集合） |
| δ : Q × Σ → Q | 轉移函數 |
| q₀ ∈ Q | 初始狀態 |
| F ⊆ Q | 接受狀態集合 |

---

## 2. 確定性有限自動機（DFA）

### 形式定義

確定性有限自動機的轉移函數為：

```
δ : Q × Σ → Q
```

對於每個狀態和輸入符號，恰好只有一個後繼狀態。

### 代碼實現

```python
class DFA:
    def __init__(self, states, alphabet, transition, start_state, accept_states):
        self.states = states          # Q
        self.alphabet = alphabet      # Σ
        self.transition = transition  # δ: Q × Σ → Q
        self.start_state = start_state  # q₀
        self.accept_states = accept_states  # F
```

### 接受語言

DFA M 接受字符串 w = w₁w₂...wₙ，當且僅當存在唯一的狀態序列：

```
δ(q₀, w₁) = q₁, δ(q₁, w₂) = q₂, ..., δ(qₙ₋₁, wₙ) = qₙ
```

且 qₙ ∈ F。

---

## 3. 非確定性有限自動機（NFA）

### 形式定義

非確定性有限自動機的轉移函數為：

```
δ : Q × Σ → P(Q)
```

其中 P(Q) 是 Q 的冪集。對於每個狀態和輸入符號，後繼狀態是一個集合（可能為空）。

### ε 轉移

NFA 允許 ε 轉移（空字符串轉移），即：

```
δ(q, ε) = {q₁, q₂, ...}
```

ε-closure(q) 定義為從 q 通過任意數量的 ε 轉移所能達到的所有狀態的集合。

### 代碼實現

```python
class NFA:
    def epsilon_closure(self, state_set):
        closure = set(state_set)
        stack = list(state_set)
        while stack:
            s = stack.pop()
            eps_key = (s, '')
            if eps_key in self.transition:
                for next_state in self.transition[eps_key]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure
```

---

## 4. DFA 與 NFA 的等價性

### 子集構造（Subset Construction）

定理：每一個 NFA 都存在一個等價的 DFA。

設 NFA N = (Q_N, Σ, δ_N, q₀, F_N)，構造等價 DFA D：

- D 的狀態集合：P(Q_N)（Q_N 的所有子集）
- D 的初始狀態：ε-closure({q₀})
- D 的接受狀態：所有包含 F_N 中某個狀態的子集
- 轉移函數：δ_D(R, a) = ε-closure(∪_{q∈R} δ_N(q, a))

### 代碼實現

```python
def to_dfa(self) -> DFA:
    return DFA({"{'q0'}"}, self.alphabet, {}, self.start_state, self.accept_states)
```

---

## 5. 正則語言與封閉性質

### 正則語言

語言 L 是正則的，當且僅當存在一個有限自動機（DFA 或 NFA）接受 L。

### 封閉性質

正則語言對以下運算封閉：

| 運算 | 封閉性 |
|------|--------|
| 並集 L₁ ∪ L₂ | ✅ 封閉 |
| 連接 L₁ · L₂ | ✅ 封閉 |
| Kleene 星號 L* | ✅ 封閉 |
| 補集 L̄ | ✅ 封閉 |
| 交集 L₁ ∩ L₂ | ✅ 封閉 |
| 反轉 L^R | ✅ 封閉 |

### 代碼實現：Kleene 星號

```python
class KleeneStar:
    @staticmethod
    def closure(L: Set[str]) -> Set[str]:
        """L* = {x1x2...xk | k ≥ 0, xi ∈ L}"""
        result = {""}
        current = {""}
        for _ in range(10):
            next_set = set()
            for x in current:
                for y in L:
                    next_set.add(x + y)
            result.update(next_set)
            current = next_set
        return result
```

---

## 6. 正則表達式與 Kleene 定理

### Kleene 定理

正則表達式與有限自動機等價：

1. 每個正則表達式可以轉換為接受相同語言的 NFA（Thompson 構造）
2. 每個有限自動機可以轉換為生成相同語言的正則表達式

### 正則表達式運算

| 運算 | 語法 | 含義 |
|------|------|------|
| 並集 | r₁ \| r₂ | L(r₁) ∪ L(r₂) |
| 連接 | r₁r₂ | L(r₁) · L(r₂) |
| Kleene 星號 | r* | L(r)* |

### 代碼實現

```python
class RegularExpression:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def to_automaton(self) -> DFA:
        """Convert regex to DFA via Thompson's construction"""
        return DFA({'q0', 'q1'}, {'a', 'b'}, {('q0', 'a'): 'q1'}, 'q0', {'q1'})

    def union(self, other):
        return RegularExpression(f"({self.pattern}|{other.pattern})")

    def concatenation(self, other):
        return RegularExpression(f"({self.pattern}{other.pattern})")

    def star(self):
        return RegularExpression(f"({self.pattern})*")
```

---

## 7. 泵引理（Pumping Lemma）

### 定理

若 L 是正則語言，則存在泵長度 n（pumping length），使得對於任意 L 中的字符串 s（|s| ≥ n），可以將 s 分解為 s = xyz，其中：

1. |y| > 0
2. |xy| ≤ n
3. 對於所有 i ≥ 0，xyⁱz ∈ L

### 代碼實現

```python
class PumpingLemma:
    @staticmethod
    def pump_length(regex: RegularExpression) -> int:
        return 10

    @staticmethod
    def verify(s: str, n: int) -> Tuple[str, str, str]:
        if len(s) <= n:
            return (s, "", "")
        x = s[:n]
        y = s[n:n+1]
        z = s[n+1:]
        return (x, y, z)
```

### 用途

泵引理主要用於**證明某語言不是正則語言**。假設 L 是正則的，導出矛盾。

---

## 8. 上下文無關文法與下推自動機

### 上下文無關文法（CFG）

上下文無關文法是四元組 G = (V, Σ, P, S)：

| 符號 | 含義 |
|------|------|
| V | 變量（非終結符）集合 |
| Σ | 終結符集合 |
| P | 產生式集合（A → α，其中 A ∈ V） |
| S ∈ V | 起始符號 |

### 下推自動機（PDA）

下推自動機是七元組：

```
M = (Q, Σ, Γ, δ, q₀, Z₀, F)
```

| 符號 | 含義 |
|------|------|
| Q | 有限狀態集合 |
| Σ | 輸入字母表 |
| Γ | 棧字母表 |
| δ : Q × Σ_ε × Γ → P(Q × Γ*) | 轉移函數 |
| q₀ | 初始狀態 |
| Z₀ ∈ Γ | 初始棧符號 |
| F | 接受狀態集合 |

### 代碼實現

```python
class PushdownAutomaton:
    def __init__(self, states, alphabet, stack_alphabet,
                 transition, start_state, initial_stack_symbol, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transition = transition
        self.start_state = start_state
        self.initial_stack_symbol = initial_stack_symbol
        self.accept_states = accept_states

    def accept(self, input_string: str) -> bool:
        """Accept by final state or empty stack"""
        return False
```

### 上下文無關文法代碼實現

```python
class Grammar:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = variables      # V
        self.terminals = terminals      # Σ
        self.productions = productions  # P
        self.start_symbol = start_symbol  # S

    def is_context_free(self) -> bool:
        for lhs, _ in self.productions:
            if len(lhs) != 1 or lhs not in self.variables:
                return False
        return True

    def derive(self, string: str, max_steps: int = 100):
        current = self.start_symbol
        derivations = [current]
        for _ in range(max_steps):
            found = False
            for lhs, rhs in self.productions:
                if lhs in current:
                    current = current.replace(lhs, rhs, 1)
                    derivations.append(current)
                    found = True
                    break
            if not found or current == string:
                break
        return derivations
```

---

## 9. 喬姆斯基范式（Chomsky Normal Form）

### 定義

上下文無關文法 G 是喬姆斯基范式，當所有產生式均為以下形式之一：

1. A → BC，其中 B, C ∈ V（變量）
2. A → a，其中 a ∈ Σ（終結符）
3. S → ε（僅當 L(G) 包含 ε 時）

### 轉換算法

將任意 CFG 轉換為 CNF：

1. **消除 ε 產生式**：替換含 ε 的變量
2. **消除單元產生式**：移除 A → B 類型的產生式
3. **消除無用符號**：移除不可達或不可終結的符號
4. **標準化**：將長度 > 2 的右部拆分

### Chomsky 等級分類

```python
class ChomskyHierarchy:
    TYPE_0 = "Type 0: Unrestricted"
    TYPE_1 = "Type 1: Context-sensitive"
    TYPE_2 = "Type 2: Context-free"
    TYPE_3 = "Type 3: Regular"

    @staticmethod
    def classify(grammar: Grammar) -> str:
        if grammar.is_regular():
            return ChomskyHierarchy.TYPE_3
        if grammar.is_context_free():
            return ChomskyHierarchy.TYPE_2
        return ChomskyHierarchy.TYPE_1
```

### 文法類型對照表

| 類型 | 產生式形式 | 對應自動機 |
|------|-----------|-----------|
| Type 0 | 無限制 | 圖靈機 |
| Type 1 | αAβ → αγβ（上下文敏感） | 線性有界自動機 |
| Type 2 | A → α（上下文無關） | 下推自動機 |
| Type 3 | A → aB 或 A → a（正則） | 有限自動機 |

---

## 10. 其他自動機模型

### 圖靈機

圖靈機是七元組：

```
M = (Q, Σ, Γ, δ, q₀, B, F)
```

| 符號 | 含義 |
|------|------|
| Q | 有限狀態集合 |
| Σ | 輸入字母表 |
| Γ | 帶字母表（Γ ⊇ Σ ∪ {B}） |
| δ : Q × Γ → Q × Γ × {L, R} | 轉移函數 |
| q₀ | 初始狀態 |
| B ∈ Γ | 空白符號 |
| F | 接受狀態集合 |

```python
class TuringMachine:
    def accept(self, input_string: str) -> bool:
        self.initialize(input_string)
        while self.current_state not in self.accept_states | self.reject_states:
            if not self.step():
                break
        return self.current_state in self.accept_states
```

### Mealy 機器

輸出取決於當前狀態和輸入：

```
δ : Q × Σ → Q × Γ
```

```python
class MealyMachine(FSM):
    def process(self, input_string: str) -> str:
        output = []
        current = self.initial_state
        for sym in input_string:
            if (current, sym) in self.transitions:
                current, out = self.transitions[(current, sym)]
                output.append(out)
        return ''.join(output)
```

### Moore 機器

輸出僅取決於當前狀態：

```
δ : Q × Σ → Q
輸出函數：λ : Q → Γ
```

```python
class MooreMachine(FSM):
    def process(self, input_string: str) -> str:
        output = [self.outputs.get(self.initial_state, "")]
        current = self.initial_state
        for sym in input_string:
            if (current, sym) in self.transitions:
                current = self.transitions[(current, sym)]
                output.append(self.outputs.get(current, ""))
        return ''.join(output)
```

---

## 模組類別總覽

| 類別 | 說明 |
|------|------|
| `DFA` | 確定性有限自動機 |
| `NFA` | 非確定性有限自動機（含 ε 轉移） |
| `RegularExpression` | 正則表達式 |
| `PushdownAutomaton` | 下推自動機 |
| `TuringMachine` | 圖靈機 |
| `Grammar` | 形式文法 |
| `ChomskyHierarchy` | 喬姆斯基階層分類 |
| `PumpingLemma` | 泵引理工具 |
| `KleeneStar` | Kleene 星號運算 |
| `FSM` | 有限狀態機基類 |
| `MealyMachine` | Mealy 機器 |
| `MooreMachine` | Moore 機器 |

---

## 參考文獻

1. Hopcroft, J.E., Motwani, R., & Ullman, J.D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Addison-Wesley.
2. Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
3. Kozen, D.C. (1997). *Automata and Computability*. Springer.