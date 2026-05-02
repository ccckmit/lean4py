# test_prover.py 测试文档

本文档说明 `tests/test_prover.py` 中测试用例的数学原理。

## 1. 测试验证的定理证明功能

本测试文件验证命题逻辑定理证明系统的核心功能，包括：
- 命题公式的有效性判定
- 可满足性判定
- 反例查找
- 表列法（Tableau Method）证明
- 证明器（Prover）类的基本操作

---

## 2. 真理表法测试 (TestTruthTableProve)

### 测试原理

真理表法通过枚举命题变元的所有可能取值组合，检验公式在每种情况下的真值。若公式在所有赋值下都为真，则该公式是**重言式（永真式）**。

### 关键测试用例

| 测试 | 公式 | 期望结果 | 说明 |
|------|------|----------|------|
| `test_valid_p_implies_p` | P → P | True | 同一律（Identity Law） |
| `test_valid_excluded_middle` | P ∨ ¬P | True | 排中律（Law of Excluded Middle） |
| `test_valid_double_neg` | ¬¬P → P | True | 双重否定消去 |
| `test_valid_modus_ponens_form` | (P ∧ (P → Q)) → Q | True | 肯定前件式（Modus Ponens） |
| `test_invalid_p_implies_q` | P → Q | False | 条件式不是永真式 |
| `test_invalid_contradiction` | P ∧ ¬P | False | 矛盾式永假 |
| `test_valid_and_commute` | (P ∧ Q) ↔ (Q ∧ P) | True | 合取交换律 |
| `test_valid_or_commute` | (P ∨ Q) ↔ (Q ∨ P) | True | 析取交换律 |
| `test_valid_de_morgan_1` | ¬(P ∧ Q) ↔ (¬P ∨ ¬Q) | True | 德·摩根律 |
| `test_valid_de_morgan_2` | ¬(P ∨ Q) ↔ (¬P ∧ ¬Q) | True | 德·摩根律 |

---

## 3. is_valid() 与 is_satisfiable() 测试

### is_valid() - 有效性判定

`is_valid()` 判断公式是否对所有赋值都为真（重言式）。

```python
# 测试：P → P 是有效式
is_valid(implies(p, p))  # True

# 测试：P → Q 不是有效式
is_valid(implies(p, q))  # False
```

### is_satisfiable() - 可满足性判定

`is_satisfiable()` 判断公式是否存在至少一种使之为真的赋值。

| 测试 | 公式 | 结果 | 说明 |
|------|------|------|------|
| `test_satisfiable_atom` | P | True | 单原子命题可满足 |
| `test_unsatisfiable_contradiction` | P ∧ ¬P | False | 矛盾式不可满足 |
| `test_satisfiable_conjunction` | P ∧ Q | True | 合取可满足 |
| `test_satisfiable_or` | P ∨ Q | True | 析取可满足 |

**关系**：`is_valid(φ)` 等价于 `¬is_satisfiable(¬φ)`

---

## 4. 反例查找测试 (TestFindCounterexample)

### 测试原理

反例是使公式为假的特定赋值。`find_counterexample()` 通过搜索找出这样的赋值。

```python
# P → Q 的反例：P = True, Q = False
find_counterexample(implies(p, q))  # 返回反例

# 有效式没有反例
find_counterexample(implies(p, p))  # None
```

---

## 5. 表列法测试 (TestTableauProve)

### 测试原理

表列法（Tableau Method）是一种反证法证明技术：

1. 将待证公式的否定加入表
2. 按照规则分解公式，展开分支
3. 若所有分支都出现互补对（如 P 和 ¬P），则原公式有效
4. 若存在分支不闭合，则找到反例

### 关键规则

| 公式类型 | 展开方式 |
|----------|----------|
| ¬(A → B) | 展开为 [A, ¬B]（α规则） |
| A → B | 展开为 [¬A, B] |
| ¬¬A | 展开为 [A] |
| A ∧ B | 展开为 [A, B] |
| A ∨ B | 分支展开为 [A] 和 [B] |
| ¬(A ∧ B) | 展开为 [¬A, ¬B] |
| ¬(A ∨ B) | 展开为 [¬A] 和 [¬B] |

### 测试用例

| 测试 | 公式 | 期望结果 |
|------|------|----------|
| `test_tableau_valid_p_implies_p` | P → P | True |
| `test_tableau_valid_excluded_middle` | P ∨ ¬P | True |
| `test_tableau_invalid` | P → Q | False |

---

## 6. Prover 类测试 (TestProver)

### 测试功能

| 测试 | 功能 | 说明 |
|------|------|------|
| `test_prover_init` | 初始化 | 创建空证明器 |
| `test_prover_add_theorem` | 添加定理 | 命名并存储定理 |
| `test_prover_prove_truth_table` | 证明 | 使用真理表法证明 |
| `test_prover_prove_invalid` | 无效证明 | 返回 None |
| `test_prove_with_steps` | 分步证明 | 返回结果和反例 |

### API 示例

```python
prover = Prover()
p = Prop('p')

# 添加定理
t = prover.add_theorem('id', implies(p, p))

# 证明
result = prover.prove(implies(p, p), method='truth_table')

# 分步证明
result, counterexample = prover.prove_with_steps(implies(p, p))
```

---

## 7. 战术系统测试 (TestNewTactics, TestTacticState)

### 基础战术

| 战术 | 作用 |
|------|------|
| `intro` / `intros` | 引入假设变量 |
| `split` | 拆分合取目标 |
| `left` / `right` | 处理析取分支 |
| `use` | 使用假设 |
| `show` | 设置证明目标 |
| `by` | 调用子证明 |
| `sorry` | 占位符 |
| `rewrite` | 重写（可逆向） |
| `induction` | 数学归纳法 |
| `calc` | 计算证明 |

### 反证法战术

```python
by_contra('h', not_(p))  # 引入反设假设 h: ¬p
```

### 案例分析

```python
cases('h', [p, q])  # 对假设 h 分类讨论
```

---

## 8. 数学基础总结

### 核心算法

1. **真理表法**：时间复杂度 O(2^n)，n 为命题变元数量
2. **表列法**：最坏情况指数级，但实际通常更快
3. **有效性 ↔ 可满足性**：`valid(φ) ≡ ¬satisfiable(¬φ)`

### 关键性质

- **可靠性**（Soundness）：证明器只证明有效公式
- **完备性**（Completeness）：所有有效公式都能被证明
- **判定性**：命题逻辑是可判定的