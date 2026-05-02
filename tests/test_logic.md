# 命題邏輯測試文檔

本文檔說明 `/Users/Shared/ccc/project/lean4py/tests/test_logic.py` 中測試案例的數學原理。

## 1. 測試驗證的命題邏輯性質

本測試套件驗證命題邏輯（Propositional Logic）的核心概念實現：

- **語法有效性**：命題變數、邏輯連接詞的正確表示
- **語義一致性**：邏輯運算的數學性質
- **對象相等性**：Prop 對象的相等判斷和哈希行為
- **操作符重載**：Python 運算符與邏輯運算的對應關係

## 2. Prop 類測試

### 2.1 命題變數創建 (`test_prop_var`)

```python
p = Prop('p')
assert p.name == 'p'
assert repr(p) == "Prop('p')"
```

**數學原理**：命題邏輯的最基本單位是**命題變數**（Propositional Variable），用小寫字母如 `p`, `q`, `r` 表示。`Prop` 類封裝一個命題變數，其 `name` 屬性存储變數名稱。

### 2.2 相等性測試 (`test_prop_equality`)

```python
p1 = Prop('p')
p2 = Prop('p')
p3 = Prop('q')
assert p1 == p2   # 相同名稱的命題相等
assert p1 != p3   # 不同名稱的命題不相等
```

**數學原理**：
- **外延性原則**（Extensionality）：兩個命題邏輯表達式當且僅當它們具有相同的真值時相等
- 對於原子命題 `Prop('p')`，相等關係定義為名稱相同
- `p1 == p2` 為 `True`（名稱相同），`p1 != p3` 為 `True`（名稱不同）

### 2.3 哈希測試 (`test_prop_hash`)

```python
p1 = Prop('p')
p2 = Prop('p')
assert hash(p1) == hash(p2)
```

**數學原理**：若兩個對象相等（`a == b`），則它們的哈希值必須相同（`hash(a) == hash(b)`）。這是 Python 對象用於字典鍵和集合元素的基礎要求。此測試確保 `Prop` 對象可以作為字典鍵或集合元素使用。

## 3. 邏輯運算

### 3.1 蘊含 (Implication) - `implies`

```python
p = Prop('p')
q = Prop('q')
imp = implies(p, q)
assert '→' in imp.name
assert imp.left == p
assert imp.right == q
```

**數學原理**：
- 蘊含 `p → q` 讀作「若 p 則 q」
- 真值表：僅當 p 為真且 q 為假時為假，其餘情況均為真
- 數學意義：當前件 p 為真時，后件 q 必為真

### 3.2 合取 (Conjunction) - `and_`

```python
p = Prop('p')
q = Prop('q')
a = and_(p, q)
assert '∧' in a.name
assert a.left == p
assert a.right == q
```

**數學原理**：
- 合取 `p ∧ q` 讀作「p 且 q」
- 真值表：僅當 p 和 q 都為真時為真，其餘為假
- 是命題邏輯的**乘法運算**

### 3.3 析取 (Disjunction) - `or_`

```python
p = Prop('p')
q = Prop('q')
o = or_(p, q)
assert '∨' in o.name
assert o.left == p
assert o.right == q
```

**數學原理**：
- 析取 `p ∨ q` 讀作「p 或 q」
- 真值表：僅當 p 和 q 都為假時為假，其餘為真
- 是命題邏輯的**加法運算**

### 3.4 否定 (Negation) - `not_`

```python
p = Prop('p')
n = not_(p)
assert '¬' in n.name
assert n.operand == p
```

**數學原理**：
- 否定 `¬p` 讀作「非 p」
- 真值表：p 為真時 ¬p 為假，p 為假時 ¬p 為真
- 是一元運算，運算元稱為 `operand`

### 3.5 雙蘊含 (Iff/Biconditional) - `iff`

```python
p = Prop('p')
q = Prop('q')
i = iff(p, q)
assert '∧' in i.name
```

**數學原理**：
- 雙蘊含 `p ↔ q` 讀作「p 當且僅當 q」
- 定義為 `(p → q) ∧ (q → p)`
- 真值表：p 和 q 真值相同時為真，不同時為假

## 4. 運算符重載測試

### 4.1 右移運算符 `>>` (蘊含)

```python
p = Prop('p')
q = Prop('q')
imp = p >> q
assert imp.left == p
assert imp.right == q
```

**設計原理**：`>>` 在程序設計中表示「流向」，邏輯上對應蘊含關係 `p → q`。

### 4.2 按位與 `&` (合取)

```python
p = Prop('p')
q = Prop('q')
a = p & q
assert '∧' in a.name
```

**設計原理**：借用 Python 的 `&` 運算符表示邏輯合取，與布爾代數中的「與」運算含義一致。

### 4.3 按位或 `|` (析取)

```python
p = Prop('p')
q = Prop('q')
o = p | q
assert '∨' in o.name
```

**設計原理**：借用 Python 的 `|` 運算符表示邏輯析取，與布爾代數中的「或」運算含義一致。

### 4.4 取反 `~` (否定)

```python
p = Prop('p')
n = ~p
assert '¬' in n.name
```

**設計原理**：借用 Python 的 `~` 運算符表示邏輯否定，與位運算中的取反含義對應。

## 5. Theorem 和 ProofStep 類

### 5.1 Theorem 類 (`TestTheorem`)

```python
p = Prop('p')
t = Theorem('trivial', p)
assert t.name == 'trivial'
assert t.prop == p
assert t.proof == []
```

**數學原理**：
- **定理**（Theorem）是已經證明為真的命題
- `Theorem` 類包含：
  - `name`：定理名稱（如 `'trivial'`）
  - `prop`：定理的命題內容
  - `proof`：證明步驟列表

### 5.2 ProofStep 類 (`TestProofSteps`)

`ProofStep` 是證明過程中的基本構建模塊：

| 策略 | 函數 | 數學意義 |
|------|------|----------|
| assume | `assume('h', p)` | 引入假設，將命題 p 命名為假設 h |
| have | `have('h', p, from_='h1')` | 引入輔助命題，從 h1 推導得到 |
| exact | `exact(p)` | 宣告 p 為當前目標的證明 |
| apply | `apply('h1')` | 應用假設 h1 進行推理 |
| rfl | `rfl()` | 反射性（ reflexivity），用於相等證明 |
| simp | `simp()` | 簡化和重寫 |

## 6. 測試方法及其驗證的數學性質

| 測試類 | 測試方法 | 驗證的數學性質 |
|--------|----------|----------------|
| `TestProp` | `test_prop_var` | 命題變數的正確表示 |
| `TestProp` | `test_prop_equality` | 命題外延相等性 |
| `TestProp` | `test_prop_hash` | 哈希一致性（相等對象哈希相等） |
| `TestPropOps` | `test_implies` | 蘊含關係的結構正確性 |
| `TestPropOps` | `test_and` | 合取運算的結構正確性 |
| `TestPropOps` | `test_or` | 析取運算的結構正確性 |
| `TestPropOps` | `test_not` | 否定運算的結構正確性 |
| `TestPropOps` | `test_iff` | 雙蘊含的結構正確性 |
| `TestPropOps` | `test_rshift` | `>>` 重載正確性 |
| `TestPropOps` | `test_and_op` | `&` 重載正確性 |
| `TestPropOps` | `test_or_op` | `\|` 重載正確性 |
| `TestPropOps` | `test_invert` | `~` 重載正確性 |
| `TestTheorem` | `test_theorem_init` | 定理對象初始化正確性 |
| `TestTheorem` | `test_theorem_with_proof` | 帶證明的定理對象正確性 |
| `TestProofSteps` | 各方法 | 各證明步驟類型的創建正確性 |
| `TestProve` | `test_prove_creates_theorem` | `prove` 函數返回定理對象 |

## 7. 核心設計思想

1. **符號表示**：使用 Unicode 符號（`→`, `∧`, `∨`, `¬`, `↔`）直觀表示邏輯運算
2. **運算符重載**：借用 Python 內置運算符提供直觀的邏輯表達式書寫方式
3. **外延相等性**：基於命題名稱（而非對象標識）判斷相等性
4. **證明對象化**：將證明步驟建模為對象，便於結構化處理