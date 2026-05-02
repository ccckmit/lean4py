# prover.py 數學原理文檔

本文檔解釋命題邏輯證明器 `prover.py` 的數學基礎與實現原理。

## 1. 命題邏輯的真值表法

真值表法是判定命題邏輯公式有效性的最基本方法。對於含有 $n$ 個命題變元的公式，共有 $2^n$ 種可能的真值分配。

### 1.1 公式求值

```python
def _eval_prop(prop, assignment: Dict[str, bool]) -> bool:
```

該函數根據給定的真值分配計算公式的真值：
- 變元：返回分配的值
- $A \land B$：返回 `left_val and right_val`
- $A \lor B$：返回 `left_val or right_val`
- $A \to B$：返回 `not left_val or right_val`（實質蘊涵）
- $\neg A$：返回 `not operand_val`

### 1.2 有效性與可滿足性

```python
def is_valid(prop) -> bool:      # 有效性：所有分配都為真
def is_satisfiable(prop) -> bool: # 可滿足性：存在至少一個分配為真
```

- **有效性 (Valid)**: 公式在**所有**真值分配下都為真
- **可滿足性 (Satisfiable)**: 存在**至少一個**真值分配使公式為真

兩者關係：$\phi$ 有效當且僅當 $\neg\phi$ 不可滿足。

### 1.3 反例尋找

```python
def find_counterexample(prop) -> Optional[Dict[str, bool]]:
```

遍歷所有可能的真值分配，返回第一個使公式為假的分配作為反例。如果找不到，則公式有效。

## 2. 語義 tableau（分析 tableau）

Tableau 方法是一種反駁方法，通過系統性地分解公式來檢查是否存在使原命題為假的模型。

### 2.1 核心思想：反駁原理

要證明 $\vdash \phi$，我們轉而證明 $\neg\phi$ 是**不可滿足**的。如果 $\neg\phi$ 的 tableau 完全封閉（每個分支都包含互補對），則 $\phi$ 有效。

```python
def tableau_prove(prop) -> bool:
    initial = TableauBranch([_negate_formula(prop)])  # 初始分支包含 ¬φ
```

### 2.2 Tableau 結構

- **TableauNode**: 表示 tableau 樹中的節點
- **TableauBranch**: 表示一個未封閉的分支，包含一組尚未完全分解的公式

## 3. Alpha 規則（合取規則）

對於合取公式 $\phi \land \psi$，將其分解為兩個子公式 $\phi$ 和 $\psi$，放在**同一分支**上。

代碼實現 (`prover.py:160-164`):
```python
if op == '∧':
    new_formulas = [f for f in branch.formulas if f is not formula]
    new_formulas.append(formula.left)
    new_formulas.append(formula.right)
    new_branches.append(TableauBranch(new_formulas))
```

示例：
- $p \land q$ → 分支包含 $[p, q]$

## 4. Beta 規則（析取/蘊涵規則）

對於析取公式或蘊涵公式，分別展開為**兩個分支**。

### 4.1 析取規則 ($A \lor B$)

代碼實現 (`prover.py:166-171`):
```python
elif op == '∨':
    branch1 = TableauBranch([...])
    branch2 = TableauBranch([...])
    branch1.add(formula.left)
    branch2.add(formula.right)
    new_branches.extend([branch1, branch2])
```

### 4.2 蘊涵規則 ($A \to B$)

代碼實現 (`prover.py:173-178`):
```python
elif op == '→':
    branch1 = TableauBranch([...])
    branch2 = TableauBranch([...])
    branch1.add(_negate_formula(formula.left))   # 添加 ¬A
    branch2.add(formula.right)                    # 添加 B
    new_branches.extend([branch1, branch2])
```

## 5. 否定規則：¬(A → B) 的特殊處理

**關鍵實現細節**：`¬(A → B)` 被視為 alpha 規則，只展開為**一個分支**，包含 $[A, \neg B]$，而不是兩個分支。

代碼實現 (`prover.py:187-192`):
```python
if inner.op == '→':
    new_formulas.append(inner.left)
    new_formulas.append(_negate_formula(inner.right))
    new_branches.append(TableauBranch(new_formulas))
```

數學解釋：
- $\neg(A \to B) \equiv A \land \neg B$（蘊涵的否定等价）
- 由於外層已有否定，合取規則展開為單一分支

## 6. 互補對檢測與分支封閉

當分支中同時包含 $p$ 和 $\neg p$（或 $p$ 和 $\neg p$ 的變形）時，該分支封閉。

```python
def _is_complementary(prop1, prop2) -> bool:
    if hasattr(prop1, 'op') and prop1.op == '¬' and prop1.operand == prop2:
        return True
    if hasattr(prop2, 'op') and prop2.op == '¬' and prop2.operand == prop1:
        return True
    return False
```

注意：使用 `==`（而非 `is`）進行 Prop 對象的相等性比較，因為 `Prop('p') == Prop('p')` 為 `True`，而 `Prop('p') is Prop('p')` 為 `False`。

```python
def _close_branch(branch: TableauBranch) -> bool:
    for i, f1 in enumerate(branch.formulas):
        for f2 in branch.formulas[i+1:]:
            if _is_complementary(f1, f2):
                return True
    return False
```

## 7. 完整 tableau 證明流程

```python
def tableau_prove(prop) -> bool:
    initial = TableauBranch([_negate_formula(prop)])  # 從 ¬φ 開始
    branches = [initial]
    
    while branches and iteration < max_iterations:
        for branch in branches:
            if _close_branch(branch):
                continue
            expanded = _expand_branch(branch)
            # ... 處理擴展後的分支
        
        if not new_branches:
            branches = []
            break
        branches = new_branches
    
    # 所有分支都封閉 → φ 有效
    for branch in branches:
        if not _close_branch(branch):
            return False
    return True
```

## 8. Prover 類接口

```python
class Prover:
    def __init__(self):
        self.theorems = {}  # 存儲已證明的定理
    
    def add_theorem(self, name: str, prop, proof: Optional[list] = None):
        """添加定理到知識庫"""
        
    def prove(self, prop, method: str = 'truth_table') -> Theorem:
        """
        證明公式，可選方法：
        - 'truth_table': 真值表法
        - 'tableau': 語義 tableau 法
        """
        
    def prove_with_steps(self, prop) -> tuple:
        """返回 (證明結果, 反例) 的元組"""
```

### 使用示例

```python
from lean4py.prover import Prover, Prop, and_, or_, not_, implies

prover = Prover()
p, q = Prop('p'), Prop('q')

# 證明 p → (q → p)
formula = implies(p, implies(q, p))
result = prover.prove(formula, method='tableau')
```

## 9. 數學原理總結

| 概念 | 描述 |
|------|------|
| **有效性** | 公式在所有解釋下為真 |
| **可滿足性** | 存在至少一個解釋使公式為真 |
| **反駁原理** | 證明 $\phi$ 有效 ⟺ 證明 $\neg\phi$ 不可滿足 |
| **Alpha 規則** | 合取公式在同分支展開 |
| **Beta 規則** | 析取/蘊涵公式分支展開 |
| **分支封閉** | 包含互補對時封閉 |
| ** tableau 證明** | 所有分支封閉 ⟹ 公式有效 |