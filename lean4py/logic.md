# 命题逻辑 (Propositional Logic) 模块

本文档介绍 `lean4py/logic.py` 模块背后的数学原理。

## 1. 命题逻辑基础

命题逻辑是数理逻辑的最基础分支，研究由**原子命题**和**逻辑联结词**构成的公式的真值条件。

### 原子命题

原子命题是不能再分割的简单命题，用 `Prop` 类表示。例如：

```python
p = Prop('p')  # 原子命题 p
q = Prop('q')  # 原子命题 q
```

原子命题没有内部结构，其真值（真/假）是给定的。

### 逻辑联结词

模块支持以下五种基本逻辑联结词：

| 联结词 | 符号 | Python 实现 | 数学含义 |
|--------|------|-------------|----------|
| 否定 | ¬ | `not_(a)` 或 `~a` | ¬A 为真当且仅当 A 为假 |
| 合取 | ∧ | `and_(a, b)` 或 `a & b` | A ∧ B 为真当且仅当 A 和 B 同时为真 |
| 析取 | ∨ | `or_(a, b)` 或 `a \| b` | A ∨ B 为真当且仅当 A 或 B 中至少一个为真 |
| 蕴含 | → | `implies(a, b)` 或 `a >> b` | A → B 为真当且仅当 A 为假或 B 为真 |
| 等价 | ↔ | `iff(a, b)` | A ↔ B 为真当且仅当 A 和 B 同真同假 |

## 2. 复合公式的构建

复合公式通过**二元运算**和**一元运算**从简单命题构建。

### 二元运算

`_PropBinOp` 类处理二元联结词（∧、∨、→）：

```python
implies(p, q)  # 创建 p → q
and_(p, q)      # 创建 p ∧ q
or_(p, q)       # 创建 p ∨ q
```

内部表示为：`f"({left.name} {op} {right.name})"`，例如 `"(p → q)"`。

### 一元运算

`_PropUnOp` 类处理否定联结词（¬）：

```python
not_(p)  # 创建 ¬p
```

内部表示为：`f"{op}{operand.name}"`，例如 `"¬p"`。

### 算术运算重载

为方便使用，`Prop` 类重载了 Python 运算符：

```python
p & q     # 等价于 and_(p, q)
p | q     # 等价于 or_(p, q)
p >> q    # 等价于 implies(p, q)
~p        # 等价于 not_(p)
```

## 3. 定理与证明步骤

### Theorem 类

`Theorem` 类表示一个已证明的定理：

- `name`: 定理名称
- `prop`: 命题公式
- `proof`: 证明步骤列表

### ProofStep 类

`ProofStep` 类表示证明中的单个步骤：

- `tactic`: 使用的证明策略
- `args`: 策略参数

### 证明策略函数

| 函数 | 作用 |
|------|------|
| `assume(name, prop)` | 在证明中引入假设 |
| `have(name, prop, from_)` | 声明可从已有前提推导的新命题 |
| `exact(prop)` | 使用精确匹配的命题关闭目标 |
| `apply(h)` | 应用已有假设或定理 |
| `rfl()` | 证明形如 x = x 的目标（ reflexivity） |
| `simp()` | 简化目标 |

### `prove` 函数

```python
prove(prop, tactics) -> Theorem
```

将命题和证明策略列表组合成完整定理。

## 4. 核心数学概念

### 蕴含 (Implication)

**定义**：A → B 在逻辑上等价于 ¬A ∨ B。

这意味着：
- 当 A 为真时，B 必须为真
- 当 A 为假时，蕴含式总为真（前提为假的蕴含式不传递任何信息）

**数学性质**：
- A → B 和 ¬A → ¬B 互为逆否命题
- A → B 与 ¬A ∨ B 等价

### 等价 (Biconditional)

**定义**：A ↔ B 定义为 (A → B) ∧ (B → A)。

这表示 A 和 B **同真同假**。

**真值表**：

| A | B | A ↔ B |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | T |

### 德摩根定律 (De Morgan's Laws)

德摩根定律描述了否定对合取和析取的分配：

1. ¬(A ∧ B) ⟺ (¬A) ∨ (¬B)
2. ¬(A ∨ B) ⟺ (¬A) ∧ (¬B)

这些定律可以通过组合基本联结词来验证：

```python
# ¬(p ∧ q) ≡ (¬p) ∨ (¬q)
left = not_(and_(p, q))
right = or_(not_(p), not_(q))
```

## 5. Prop 对象的名字相等性

这是一个关键实现细节：

```python
Prop('p') == Prop('p')    # 返回 True（名字相同）
Prop('p') is Prop('p')    # 返回 False（不同对象）
```

**原理**：
- `__eq__` 方法基于 `name` 属性判断相等性
- 不同调用 `Prop('p')` 创建的是不同的对象实例
- `__hash__` 方法也基于 `name`，因此 `Prop` 对象可以作为字典键

**实践意义**：
- 比较命题是否相等时**必须使用 `==`**，而非 `is`
- `Prop('p') in [Prop('p')]` 会返回 True
- 两个独立的 `Prop('p')` 对象在逻辑公式中可以互换使用

## 6. 使用示例

### 基本命题操作

```python
from lean4py.logic import *

# 创建原子命题
p = Prop('p')
q = Prop('q')

# 构建复合公式
not_p = not_(p)              # ¬p
p_and_q = p & q              # p ∧ q
p_or_q = p | q               # p ∨ q
p_implies_q = p >> q         # p → q
p_iff_q = iff(p, q)          # p ↔ q
```

### 验证德摩根定律

```python
# ¬(p ∧ q) ≡ (¬p) ∨ (¬q)
left = not_(and_(p, q))      # ¬(p ∧ q)
right = or_(not_(p), not_(q)) # (¬p) ∨ (¬q)

# left == right 验证等价性
```

### 构建证明

```python
# 证明 p → p
proof_steps = [
    assume('h', p),          # 假设 p
    exact(p)                 # 目标 p 已被假设
]
theorem = prove(p >> p, proof_steps)
```

### 组合复杂公式

```python
# ((p → q) ∧ (q → r)) → (p → r)
p, q, r = Prop('p'), Prop('q'), Prop('r')
formula = (p >> q) & (q >> r) >> (p >> r)
```

## 7. 模块结构概览

```
logic.py
├── Prop 类 - 命题表示
├── _PropBinOp 类 - 二元运算内部表示
├── _PropUnOp 类 - 一元运算内部表示
├── 逻辑函数 - not_, and_, or_, implies, iff
├── Theorem 类 - 定理表示
├── ProofStep 类 - 证明步骤表示
└── 证明策略函数 - assume, have, exact, apply, rfl, simp, prove
```

---

*本文档对应 lean4py 版本 1.34.0*