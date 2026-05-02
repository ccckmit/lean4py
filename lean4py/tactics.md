# 戰術證明 (Tactics) - 數學原理文檔

## 概述

本模組 `tactics.py` 實現了命題邏輯定理證明器中的戰術（tactics）系統。戰術是構建形式證明的核心工具，用於逐步消除目標（goals）並建立命題的真實性。

---

## 1. 戰術系統基礎

### 1.1 戰術的定義

**戰術 (Tactic)** 是一種將當前目標状态轉換為更簡單子目標的指令。每個戰術接受當前狀態並返回一個新的證明狀態。

```python
class Tactic:
    def __init__(self, name: str, *args):
        self.name = name
        self.args = args
```

### 1.2 戰術語義

| 戰術 | 語義 |
|------|------|
| `exact p` | 證明目標恰好為命題 `p` |
| `apply h` | 應用假設/定理 `h` |
| `intro x` | 引入變量，建立蕴含前提 |
| `split` | 將合取目標拆分為兩個子目標 |
| `left` / `right` | 選擇析取的一側 |
| `cases` | 對排中律進行分類討論 |

---

## 2. 核心戰術

### 2.1 引入與消去

| 戰術 | 數學含義 |
|------|---------|
| `intro` | 對蘊含 `A → B` 引入前提 `A` |
| `exact` | 直接給出與目標完全匹配的命題 |
| `apply` | 使用蘊含或定理前向推理 |
| `have` | 引入輔助命題 |

### 2.2 結構戰術

| 戰術 | 數學含義 |
|------|---------|
| `split` | 對 `A ∧ B` 拆分為 `A` 和 `B` |
| `left` | 對 `A ∨ B` 選擇左側 `A` |
| `right` | 對 `A ∨ B` 選擇右側 `B` |
| `cases` | 對選言命題或命題邏輯進行枚舉 |

### 2.3 否定與矛盾

| 戰術 | 數學含義 |
|------|---------|
| `by_contra` | 反證法：假設否定結論，推出矛盾 |
| `sorry` | 跳過證明（作為佔位符） |

---

## 3. 數學歸納法戰術

### 3.1 歸納原理

數學歸納法基於自然數的 Peano 公理：

```
P(0) 成立
∀n (P(n) → P(n+1)) 成立
─────────────────────────────────
∴ ∀n P(n) 成立
```

### 3.2 歸納戰術結構

```python
def induction(var: str, base: List[ProofStep], ind: List[ProofStep]) -> ProofStep:
    return ProofStep("induction", var, base, ind)
```

**參數**：
- `var`: 進行歸納的變量名
- `base`: 基本情況的證明步驟
- `ind`: 歸納步驟的證明步驟

### 3.3 歸納策略

```
目標: ∀n P(n)

1. 引入歸納變量 n
   intros n

2. 對 n 進行歸納
   induction n with
   | base => ...
   | ind n ih => ...
```

---

## 4. 改寫戰術

### 4.1 等式改寫

`rewrite` 戰術使用等式替換目標或假設中的項：

```python
def rewrite(eq: str, sym: bool = False) -> ProofStep:
    return ProofStep("rewrite", eq, sym)
```

| 參數 | 含義 |
|------|------|
| `eq` | 使用的等式名稱 |
| `sym` | 是否反向使用（置換對稱） |

### 4.2 改寫方向

- **前向**：從已知等式左側替換為右側
- **反向 (sym=True)**：從右側替換為左側

---

## 5. 計算戰術

### 5.1 計算型證明

`calc` 戰術用於逐步計算：

```python
def calc(tactics_list: List) -> ProofStep:
    return ProofStep("calc", tactics_list)
```

### 5.2 計算示例

```
calc
  a + b =  ...  (使用加法結合律)
       =  ...  (使用加法交換律)
       =  c    (目標達成)
```

---

## 6. 證明狀態管理

### 6.1 目標狀態

```python
class TacticState:
    def __init__(self, goals: List = None, hypotheses: Dict = None):
        self.goals = goals or []
        self.hypotheses = hypotheses or {}
```

**組成部分**：
- `goals`: 待證明的命題棧
- `hypotheses`: 已引入的假設字典

### 6.2 目標棧操作

- `pop_goal()`: 彈出首個目標
- `add_hypothesis()`: 添加新假設

---

## 7. 證明步驟追蹤

### 7.1 TacticProof 類

```python
class TacticProof:
    def __init__(self, steps: list = None):
        self.steps = steps or []
```

用於收集所有證明步驟，形成完整的證明腳本。

### 7.2 證明結構

```
證明 ::= 步驟₁
       ; 步驟₂
       ; ...
       ; 步驟ₙ

步驟 ::= intro | exact | apply | have | ...
```

---

## 8. 戰術合成

### 8.1 順序合成

多個戰術可以按順序執行，每個戰術消費前一個的輸出狀態。

### 8.2 束縛合成

使用 `by` 戰術將多個戰術組合成原子證明：

```python
def by(tactics_list: List) -> ProofStep:
    return ProofStep("by", tactics_list)
```

---

## 9. 與 `prover.py` 的關係

本模組與 `prover.py` 緊密相關：
- `Tactic` 對應 `ProofStep`
- 戰術用於構建 `TableauProver` 的證明策略
- 支持真值表法 (`truth_table`) 和 tableau 法 (`tableau`)

---

## 10. 使用範例

```python
from lean4py.tactics import intro, exact, by_tactic, apply_tactic
from lean4py.logic import Prop_var

# 證明: p → p
p = Prop_var('p')

proof = by_tactic([
    intro('p'),           # 引入前提 p，得到目標 p
    exact(p)              # 直接給出 p
])
```

---

## 模組結構

| 類/函數 | 功能 |
|--------|------|
| `Tactic` | 戰術表示類 |
| `TacticProof` | 證明步驟收集器 |
| `TacticState` | 目標狀態管理 |
| `tactic_*` 函數 | 創建對應戰術 |

---

*本檔案說明 `tactics.py` 中戰術系統的數學原理與實現對應*