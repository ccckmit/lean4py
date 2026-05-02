# test_formal_languages.py 测试文档

## 概述

本测试文件验证 `lean4py/formal_languages.py` 模块的形式语言理论实现，对应 mathlib4 的 `Mathlib.Computability.Language`。

---

## 1. 测试验证内容

测试套件验证以下核心功能：

| 类 | 测试方法 | 验证内容 |
|------|---------|---------|
| `RegularLanguage` | `test_from_regex`, `test_is_regular`, `test_pumping_lemma` | 正则语言的正则表达式构造、判定、泵浦引理 |
| `ContextFreeGrammar` | `test_creation`, `test_is_context_free`, `test_generates` | 上下文无关文法的创建、判定、字符串生成 |
| `ChomskyHierarchy` | `test_level`, `test_is_strict_subset` | 乔姆斯基层级分类与包含关系 |
| `PumpingLemma` | `test_for_regular`, `test_for_context_free` | 正则/上下文无关语言的泵浦引理 |

---

## 2. 正则语言测试 (Regular Language Tests)

### 数学原理

正则语言是形式语言理论中最简单的语言类，具有以下等价定义：

- **有限自动机 (DFA/NFA)**：可被确定/非确定有限自动机识别的语言
- **正则表达式**：可用正则表达式描述的语言
- **正则文法**：3 型文法 (左线性或右线性) 生成的语言

### 测试用例分析

```python
test_from_regex()     # 验证 from_regex("a*b") 返回 {language, is_regular}
test_is_regular()     # 验证 is_regular("L") 返回 True
test_pumping_lemma()  # 验证泵浦引理性质
```

**泵浦引理 (Pumping Lemma)**：若 $L$ 为正则语言，则存在常数 $n$（泵浦长度），使得任意 $w \in L$ 且 $|w| \geq n$ 可分解为 $w = xyz$ 满足：
1. $|y| \geq 1$
2. $|xy| \leq n$
3. 对所有 $i \geq 0$，$xy^iz \in L$

---

## 3. 上下文无关文法测试 (CFG Tests)

### 数学原理

上下文无关文法 (CFG) 为四元组 $G = (V, \Sigma, R, S)$：

- $V$：非终结符（变量）集合
- $\Sigma$：终结符集合
- $R$：产生式规则集合，形如 $A \rightarrow \alpha$
- $S$：起始符号

### 测试用例分析

```python
G = ContextFreeGrammar(["S"], ["a"], {"S": ["aS", ""]}, "S")
test_generates("aaa")  # 验证 S → aS → aaS → aaa
```

此文法生成语言 $L = \{a^n \mid n \geq 0\}$（即所有由单个字符组成的字符串）。

---

## 4. 乔姆斯基层级测试 (Chomsky Hierarchy Tests)

### 数学原理

乔姆斯基层级是形式语言的分类体系：

| 层级 | 语言类 | 文法类型 | 自动机模型 |
|------|--------|----------|-----------|
| 0 | 递归可枚举语言 | 0 型（短语结构文法） | 图灵机 |
| 1 | 上下文相关语言 | 1 型 | 线性界限自动机 |
| 2 | 上下文无关语言 | 2 型 | 下推自动机 |
| 3 | 正则语言 | 3 型 | 有限自动机 |

关系：$L_3 \subset L_2 \subset L_1 \subset L_0$

### 测试用例分析

```python
test_level()              # 验证返回整数层级 (0-3)
test_is_strict_subset()   # 验证层级包含关系 (level1 > level2 表示 level1 ⊂ level2)
```

---

## 5. 泵浦引理测试 (Pumping Lemma Tests)

### 两种泵浦引理对比

| 性质 | 正则语言 | 上下文无关语言 |
|------|---------|---------------|
| 分解形式 | $w = xyz$ | $w = uvxyz$ |
| 限制条件 | $\|xy\| \leq n$ | $\|vxz\| \leq n$ |
| 泵浦位置 | $y$ | $v$ 和 $x$ 可同时泵浦 |

### 测试用例分析

```python
test_for_regular()     # 验证正则语言满足泵浦引理
test_for_context_free()  # 验证上下文无关语言满足泵浦引理
```

注意：泵浦引理是**必要条件**，而非充分条件（可用于证明非正则/非 CF）。

---

## 版本信息

- 测试文件版本：v1.34
- 对应实现：`lean4py/formal_languages.py`
- 参考标准：mathlib4 `Mathlib.Computability.Language`