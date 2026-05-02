# 測試策略文檔

本文檔說明 `test_tactics.py` 中測試用例的數學原理。

## 1. 測試驗證的內容

這些測試驗證了 lean4py 策略系統的核心功能：

- **策略對象创建**：Tactic 類的初始化和表示
- **策略函數工廠**：各類策略創建函數的正確性
- **證明步驟封裝**：ProofStep 對證明步驟的封裝
- **策略證明組合**：TacticProof 組合多個策略
- **證明狀態管理**：TacticState 管理目標和假設

## 2. 基本策略測試

### 2.1 Tactic 類別測試

`TestTactic` 類測試 Tactic 對象的基本行為：

```python
def test_tactic_init(self):
    t = Tactic("rfl")
    assert t.name == "rfl"
    assert t.args == ()
```

**數學原理**：策略是 Lean 證明語言的基本構建模塊。每個策略包含：
- `name`：策略名稱（如 `rfl`、`exact`、`apply`）
- `args`：策略參數（元組形式）

### 2.2 策略函數工廠測試

`TestTacticFunctions` 類測試各種策略創建函數：

| 策略 | 數學含義 |
|------|----------|
| `tactic_rfl()` |  reflexivity（反射性）：`a = a` |
| `tactic_exact(p)` |  exact（精確）：直接使用命題 `p` 作為證據 |
| `tactic_apply("H")` |  apply（應用）：應用假設 `H` |
| `tactic_simp()` |  simplification（簡化）：應用簡化規則 |
| `tactic_assume("H")` |  assume（假設）：引入新假設 |
| `tactic_have("H")` |  have（擁有）：引入輔助命題 |

## 3. 策略組合測試

### 3.1 ProofStep 函數測試

`TestProofStepFunctions` 類測試證明步驟的創建：

**intros 策略** - 引入假設：
```python
intros("H")      # 引入單個假設 H
intros(["H1", "H2"])  # 引入多個假設
```

**by_contra 策略** - 反證法：
```python
by_contra("H", p)  # 假設 ¬p，推出矛盾
```

**cases 策略** - 分情況討論：
```python
cases("H", [p1, p2])  # 對假設 H 分別討論 p1 和 p2 情況
```

**split/left/right 策略** - 命題邏輯拆分：
```python
split()  # 拆分 ∧ 目標為兩個子目標
left()   # 選擇 ∨ 的左側
right()  # 選擇 ∨ 的右側
```

### 3.2 策略變體測試

各策略都有對應的 `*_tactic` 變體，返回 Tactic 對象而非 ProofStep：

| 函數 | 返回類型 | 用途 |
|------|----------|------|
| `intros_tactic("H")` | Tactic | 引入假設的策略對象 |
| `by_contra_tactic("H", p)` | Tactic | 反證法策略對象 |
| `cases_tactic("H", [p1,p2])` | Tactic | 分情況策略對象 |
| `induction_tactic("n", base, ind)` | Tactic | 數學歸納法策略對象 |
| `rewrite_tactic("eq_H")` | Tactic | 重寫策略對象 |
| `by_tactic([t1, t2])` | Tactic | 組合多個策略 |

**數學原理**：
- `induction_tactic`：數學歸納法，將命題拆分為 base case 和 inductive step
- `rewrite_tactic`：使用等式進行替換，支持 `sym=True` 反向重寫
- `by_tactic`：策略組合，並列執行多個策略

### 3.3 計算策略測試

`calc` 策略用於構建階梯式等式證明：
```python
calc([tactic_rfl()])  # 計算塊，包含多個等式步驟
```

## 4. 證明狀態管理測試

### 4.1 TacticState 類測試

`TestTacticState` 類測試證明狀態管理：

**數學含義**：
- `goals`：待證明的命題棧（stack）
- `hypotheses`：已引入的假設字典

```python
s = TacticState(goals=[Prop('p'), Prop('q')], hypotheses={"H": Prop('q')})
```

**狀態操作**：
| 方法 | 數學含義 |
|------|----------|
| `add_hypothesis(name, p)` |  在上下文中添加新假設 |
| `get_hypothesis(name)` |  獲取指定名稱的假設 |
| `pop_goal()` |  彈出並返回當前目標 |

### 4.2 TacticProof 類測試

`TestTacticProof` 類測試策略證明的組合：

```python
p = TacticProof()
p.add(tactic_rfl())
```

**數學原理**：
- 證明是多個策略步驟的有序序列
- 每個步驟將當前狀態轉換為新狀態
- 最終狀態應無剩餘目標

### 4.3 狀態轉換示意

```
初始狀態:
  goals: [p → q, p]
  hypotheses: {}

執行 intros("H"):
  goals: [q]
  hypotheses: {H: p → q}

執行 apply("H"):
  goals: [q, p]
  hypotheses: {H: p → q}

執行 assumption (或 exact):
  goals: []
  hypotheses: {H: p → q}
```

## 5. 測試類別總覽

| 測試類別 | 測試內容 |
|----------|----------|
| `TestTactic` | Tactic 對象基本功能 |
| `TestTacticFunctions` | 策略創建函數 |
| `TestProofStepFunctions` | 證明步驟函數 |
| `TestTacticProof` | 策略證明組合 |
| `TestTacticState` | 證明狀態管理 |
| `TestIntrosTactic` | 引入假設策略 |
| `TestByContraTactic` | 反證法策略 |
| `TestCasesTactic` | 分情況策略 |
| `TestInductionTactic` | 數學歸納法策略 |
| `TestRewriteTactic` | 重寫策略 |
| `TestSplitTactic` | 拆分策略 |
| `TestLeftRightTactic` | 選擇策略 |
| `TestUseTactic` | 使用策略 |
| `TestShowTactic` | 顯示目標策略 |
| `TestByTactic` | 策略組合 |
| `TestSorryTactic` | 暫時佔位策略 |
| `TestCalcTactic` | 計算證明策略 |
| `TestIntroTactic` | 單個引入策略 |
| `TestApplyTactic` | 應用策略 |

## 6. 命題邏輯策略對照表

| 邏輯符號 | 策略 | 說明 |
|----------|------|------|
| `∧` (合取) | `split` | 拆分為兩個子目標 |
| `∨` (析取) | `left` / `right` | 選擇左側或右側 |
| `→` (蘊含) | `apply` | 應用蘊含式 |
| `¬` (否定) | `by_contra` | 反證法 |
| `∀` (全稱) | `intros` | 引入任意元素 |
| `∃` (存在) | `use` | 使用見證 |
| `↔` (雙蘊含) | `split` + `apply` | 雙向證明 |