# 控制理論 (Control Theory)

本文件說明 `lean4py/control_theory.py` 模組的數學原理。該模組涵蓋線性系統控制的核心概念，從狀態空間表達式到最優控制理論。

---

## 1. 狀態空間表示法 (State-Space Representation)

### 數學形式

連續時間線性系統的狀態空間表示為：

```
ẋ(t) = Ax(t) + Bu(t)
y(t) = Cx(t) + Du(t)
```

其中：
- **x(t)** ∈ ℝⁿ：狀態向量
- **u(t)** ∈ ℝᵐ：輸入（控制）向量
- **y(t)** ∈ ℝᵖ：輸出向量
- **A** ∈ ℝⁿˣⁿ：系統矩陣（狀態變換矩陣）
- **B** ∈ ℝⁿˣᵐ：輸入矩陣
- **C** ∈ ℝᵖˣⁿ：輸出矩陣
- **D** ∈ ℝᵖˣᵐ：前饋矩陣（通常為零）

### 離散時間形式

離散時間系統（採樣週期 T）：

```
x(k+1) = Ad·x(k) + Bd·u(k)
y(k) = C·x(k) + D·u(k)
```

其中 Ad = e^(AT) 為離散化後的狀態轉換矩陣。

### lean4py 實作

```python
class StateSpaceRepresentation:
    """狀態空間表示: dx/dt = Ax + Bu, y = Cx + Du"""
    
    def __init__(self, A, B, C=None, D=None):
        self.A = A  # 系統矩陣
        self.B = B  # 輸入矩陣
        self.C = C if C else [[1.0]]  # 輸出矩陣
        self.D = D if D else [[0.0]]  # 前饋矩陣
```

---

## 2. 可控性與卡爾曼秩條件 (Controllability)

### 可控性定義

系統 (A, B) 為**可控**若對於任意初始狀態 x₀ 和任意目標狀態 x₁，存在有限時間 T > 0 和控制輸入 u(t)，使得 x(0) = x₀ 可推到 x(T) = x₁。

### 可控性矩陣

可控性矩陣（Controllability Matrix）定義為：

```
𝒞 = [B, AB, A²B, ..., Aⁿ⁻¹B]  ∈ ℝⁿˣⁿᵐ
```

### 卡爾曼秩條件

系統 (A, B) **完全可控**的充要條件：

```
rank(𝒞) = n
```

即可控性矩陣的秩等於狀態維度 n。

### lean4py 實作

```python
class Controllability:
    @staticmethod
    def controllability_matrix(A, B):
        """建構可控性矩陣 [B, AB, A²B, ..., A^(n-1)B]"""
        n = len(A)
        # 計算 Cn = [B, AB, A²B, ..., A^(n-1)B]
        # 實務上需計算矩陣乘冪
        ...
    
    @staticmethod
    def is_controllable(A, B):
        """檢查可控性：rank(𝒞) = n"""
        return rank(controllability_matrix(A, B)) == len(A)
```

---

## 3. 可觀測性與可觀測性矩陣 (Observability)

### 可觀測性定義

系統 (A, C) 為**可觀測**若對於任意時間 T，根據有限時間內的輸出 y(t) 和已知輸入 u(t)，可以唯一確定初始狀態 x(0)。

### 可觀測性矩陣

可觀測性矩陣（Observability Matrix）定義為：

```
𝒪 = [C; CA; CA²; ...; CAⁿ⁻¹]ᵀ  ∈ ℝⁿᵖˣⁿ
```

或寫成行形式：

```
𝒪 = [C, CᵀA, CᵀA², ..., CᵀAⁿ⁻¹]ᵀ  ∈ ℝⁿᵖˣⁿ
```

### 可觀測性條件

系統 (A, C) **完全可觀測**的充要條件：

```
rank(𝒪) = n
```

### 對偶原理

可控性與可觀測性存在對偶關係：

- 系統 (A, B) 可控 ⟺ 系統 (Aᵀ, Bᵀ) 可觀測
- 此性質常用於將可觀測性問題轉化為可控性問題處理

### lean4py 實作

```python
class Observability:
    @staticmethod
    def observability_matrix(A, C):
        """建構可觀測性矩陣 [C; CA; CA²; ...; CA^(n-1)]"""
        n = len(A)
        # 計算 O = [C; CA; CA²; ...; CA^(n-1)]
        ...
    
    @staticmethod
    def is_observable(A, C):
        """檢查可觀測性：rank(𝒪) = n"""
        return rank(observability_matrix(A, C)) == len(A)
```

---

## 4. 極點配置與狀態反饋 (Pole Placement)

### 狀態反饋控制律

採用狀態反饋 u = -Kx + r，其中 K ∈ ℝᵐˣⁿ 為反饋增益矩陣：

```
ẋ = (A - BK)x + Br
```

閉環系統矩陣為 A_cl = A - BK。

### 極點配置原理

通過選擇合适的 K，可將閉環極點（A - BK 的特徵值）放置到任意位置（前提：系統可控）。

**極點位置的系統特性關係**：
- 極點實部 < 0 → 穩定
- 極點實部 = 0 → 邊界穩定
- 極點實部 > 0 → 不穩定
- 極點越靠左 → 響應越快（但需考慮控制能量約束）

### 阿克曼公式 (Ackermann's Formula)

對於單輸入系統 (m=1)，K 可由下式計算：

```
K = [0, 0, ..., 1] · 𝒞⁻¹ · φ(A)
```

其中 φ(λ) 為期望特徵多項式，A 為期望極點構成的矩陣。

### 狀態觀測器

由於完整狀態通常不可直接測量，需設計狀態觀測器：

```
ė = A·x̂ + Bu + L(y - C·x̂ - Du)
```

誤差動態 ė = (A - LC)x̂，選擇 L 使 A - LC 穩定。

---

## 5. 李雅普諾夫穩定性 (Lyapunov Stability)

### 穩定性定義

**李雅普諾夫意義下的穩定**：若對於任意 ε > 0，存在 δ(ε) > 0，使得 ||x(0)|| < δ ⇒ ||x(t)|| < ε 對所有 t ≥ 0 成立。

**漸進穩定**：系統穩定且 lim(t→∞) x(t) = 0。

**指數穩定**：存在常數 α > 0, β > 0 使得 ||x(t)|| ≤ β||x(0)||e^(-αt)。

### 李雅普諾夫直接法

對於系統 ẋ = f(x)，找尋正定函數 V(x)：

```
V(x) > 0, ∀x ≠ 0
V(0) = 0
```

**穩定判據**：
- V̇(x) ≤ 0 ⇒ 穩定
- V̇(x) < 0, ∀x ≠ 0 ⇒ 漸進穩定

### 線性系統的李雅普諾夫方程

對於線性系統 ẋ = Ax，系統漸進穩定的充要條件是存在正定矩陣 P > 0 使得：

```
AᵀP + PA < 0
```

此為**連續時間李雅普諾夫方程**。

離散時間系統 x(k+1) = Ax(k) 的條件為：

```
AᵀPA - P < 0
```

### lean4py 實作

```python
class LyapunovStability:
    @staticmethod
    def lyapunov_function(y):
        """建構簡單的李雅普諾夫函數 V(y) = ||y||²"""
        if isinstance(y, (int, float)):
            return y * y
        return sum(y_i ** 2 for y_i in y)
    
    @staticmethod
    def is_stable(lyapunov_func, dV_dt):
        """檢查李雅普諾夫穩定性：V 正定，dV/dt 負定"""
        # V > 0 且 dV/dt < 0
        ...
    
    @staticmethod
    def is_asymptotically_stable(lyapunov_func, dV_dt):
        """漸進穩定：V > 0 且 dV/dt < 0（對 y ≠ 0）"""
        ...
```

---

## 6. 線性二次型調節器 (Linear Quadratic Regulator, LQR)

### LQR 問題定義

尋求最優控制 u*(t) 使得以下性能指標最小化：

```
J = ∫₀^∞ [xᵀQx + uᵀRu] dt
```

約束條件為系統 dynamics：ẋ = Ax + Bu。

其中：
- **Q** ∈ ℝⁿˣⁿ：狀態加權矩陣（半正定）
- **R** ∈ ℝᵐˣᵐ：控制加權矩陣（正定）

### 數學推導

構造漢密爾頓函數：

```
H = xᵀQx + uᵀRu + λᵀ(Ax + Bu)
```

最優性條件：
```
∂H/∂u = 2R u + Bᵀλ = 0  ⇒  u* = -½R⁻¹Bᵀλ
∂H/∂x = -λ̇ = Qx + Aᵀλ
```

假設 λ = Px（正定矩陣），代入可得**代數李卡提方程 (ARE)**：

```
AᵀP + PA - PBR⁻¹BᵀP + Q = 0
```

最優反饋律為：

```
K = R⁻¹BᵀP
u* = -Kx
```

### lean4py 實作

```python
class OptimalControl:
    @staticmethod
    def hamiltonian(state, control, costate, dynamics):
        """H = λᵀ · f(x, u)，漢密爾頓函數"""
        return sum(c_i * d_i for c_i, d_i in zip(costate, dynamics(state, control)))
    
    @staticmethod
    def optimal_control(hamiltonian, control_space):
        """找尋最小化 H 的 u*"""
        # 求解漢密爾頓-雅可比-貝爾曼方程
        ...
```

---

## 7. 代數黎卡提方程 (Riccati Equations)

### 連續時間代數黎卡提方程 (CARE)

```
AᵀP + PA + Q - PBR⁻¹BᵀP = 0
```

或寫成：

```
AᵀP + PA - PBR⁻¹BᵀP + Q = 0
```

### 離散時間代數黎卡提方程 (DARE)

```
P = AᵀPA - AᵀPB(R + BᵀPB)⁻¹BᵀPA + Q
```

### 黎卡提方程的性質

1. **存在唯一正定解**：若 (A, B) 可控且 (A, Q½) 可觀測，則存在唯一正定解 P > 0
2. **閉環穩定性**：A - BR⁻¹BᵀP 為穩定矩陣
3. **最優性**：P 為最優價值函數的梯度矩陣

### 數值求解方法

1. **Schur 分解法**：將 Hamiltonian 矩陣進行 Schur 分解
2. **迭代法**：利用 Riccati 迭代
3. **牛頓法**：針對黎卡提方程的牛頓迭代

### 與 LQR 的關係

LQR 問題的最優解 P 就是 CARE 的正定解。控制增益 K 和閉環系統 A_cl 分別為：

```
K = R⁻¹BᵀP
A_cl = A - BK
```

---

## 8. 觀測器設計與卡爾曼濾波 (Observer & Kalman Filter)

### 狀態觀測器（龍伯格觀測器）

全階狀態觀測器動態方程：

```
ė = A·x̂ + Bu + L(y - C·x̂)
  = (A - LC)x̂ + Bu + Ly
```

誤差動態 ė = x - x̂：

```
ė = (A - LC)x̂ ⟹ ė = (A - LC)e
```

選擇觀測器增益 L 使 A - LC 穩定（需 (A, C) 可觀測）。

### 卡爾曼濾波器

卡爾曼濾波器是最優估計理論的核心，適用於帶噪聲的線性系統：

```
x(k+1) = A·x(k) + B·u(k) + w(k)    （過程噪聲）
z(k)   = H·x(k) + v(k)              （測量噪聲）
```

假設：
- w(k) ~ N(0, Q)：過程噪聲
- v(k) ~ N(0, R)：測量噪聲

### 預測步驟 (Prediction)

```
x̂⁻(k) = A·x̂(k-1) + B·u(k-1)
P⁻(k) = A·P(k-1)·Aᵀ + Q
```

### 更新步驟 (Update)

```
K(k) = P⁻(k)·Hᵀ·(H·P⁻(k)·Hᵀ + R)⁻¹    （卡爾曼增益）
x̂(k) = x̂⁻(k) + K(k)·(z(k) - H·x̂⁻(k))
P(k) = (I - K(k)·H)·P⁻(k)
```

其中：
- **K(k)**：卡爾曼增益
- **P(k)**：估計誤差協方差矩陣
- **z(k) - H·x̂⁻(k)**：創新向量（測量殘差）

### lean4py 實作

```python
class KalmanFilter:
    @staticmethod
    def predict(state, A, Q):
        """預測步驟: x̂⁻ = A·x̂, P⁻ = A·P·Aᵀ + Q"""
        # 狀態預測
        x_hat_minus = A @ state
        # 協方差預測
        P_minus = A @ P @ A.T + Q
        return x_hat_minus, P_minus
    
    @staticmethod
    def update(state, P, measurement, H, R):
        """更新步驟: K = P·Hᵀ(HPHᵀ + R)⁻¹, x̂ = x̂ + K(z - Hx̂)"""
        # 計算卡爾曼增益
        K = P @ H.T @ np.linalg.inv(H @ P @ H.T + R)
        # 狀態更新
        innovation = measurement - H @ state
        x_hat = state + K @ innovation
        # 協方差更新（Joseph form，數值穩定）
        P = (I - K @ H) @ P
        return x_hat, P
```

### 卡爾曼濾波的收斂性

當系統滿足以下條件時，估計誤差收斂到零：
1. (A, Q½) 可觀測
2. (A, Q½) 可控
3. R > 0（正定）

穩態卡爾曼增益 K∞ 和協方差 P∞ 滿足：

```
P∞ = A·P∞·Aᵀ - A·P∞·Hᵀ(H·P∞·Hᵀ + R)⁻¹·H·P∞·Aᵀ + Q
K∞ = P∞·Hᵀ(H·P∞·Hᵀ + R)⁻¹
```

---

## 模組結構總覽

| 類別 | 功能 | 核心方法 |
|------|------|----------|
| `LyapunovStability` | 李雅普諾夫穩定性分析 | `lyapunov_function`, `is_stable` |
| `StateSpaceRepresentation` | 狀態空間模型 | `system_dim`, `input_dim`, `output_dim` |
| `Controllability` | 可控性分析 | `controllability_matrix`, `is_controllable` |
| `Observability` | 可觀測性分析 | `observability_matrix`, `is_observable` |
| `OptimalControl` | 最優控制理論 | `hamiltonian`, `optimal_control` |
| `KalmanFilter` | 卡爾曼濾波 | `predict`, `update` |

---

## 數學符號表

| 符號 | 意義 |
|------|------|
| ẋ | 狀態向量對時間的導數 |
| A, B, C, D | 系統矩陣、輸入矩陣、輸出矩陣、前饋矩陣 |
| 𝒞 | 可控性矩陣 |
| 𝒪 | 可觀測性矩陣 |
| P | 李雅普諾夫矩陣 / 黎卡提方程解 |
| Q, R | LQR 加權矩陣 |
| K | 反饋增益矩陣 |
| L | 觀測器增益矩陣 |
| H | 測量矩陣 |
| P⁻, P | 預測協方差、估計協方差 |
| K | 卡爾曼增益 |

---

*本文件基於 `lean4py/control_theory.py` v1.34.0*