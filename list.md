# lean4py 數學領域總覽

> 本專案包含 110 個 Python 模組，涵蓋從基礎邏輯到高等幾何的各大數學領域。

---

## 1. 基礎邏輯與形式系統 (Foundation & Logic)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `logic.py` | 命題邏輯 (Propositional Logic) | 命題、蘊含、聯結詞、定理證明結構 |
| `prover.py` | 定理證明 (Theorem Proving) | Tableau 證明法、命題邏輯反駁系統 |
| `nat.py` | 皮亞諾算術 (Peano Arithmetic) | 自然數結構、數學歸納法 |
| `sets.py` | 集合論 (Set Theory) | 集合操作、關係、函數 |
| `type_theory_advanced.py` | 類型論 (Type Theory) | 依值類型、依存類型、項歸納 |
| `proof_theory.py` | 證明論 (Proof Theory) | 推理系統、可證性邏輯 |
| `model_theory.py` | 模型論 (Model Theory) | 結構、理論、普遍性 |

---

## 2. 代數結構 (Algebraic Structures)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `algebra.py` | 抽象代數 (Abstract Algebra) | Magma、Semigroup、Monoid、Group、Ring、Field |
| `algebraic_structures.py` | 代數結構擴展 | 模、理想、格、向量空間 |
| `commutative_algebra_advanced.py` | 交換代數 (Commutative Algebra) | 局部化、諾etterian 環、維數理論 |
| `lie_algebra.py` | 李代數 (Lie Algebra) | 李括積、Jacobson 結構 |
| `lie_algebra_classification.py` | 李代數分類 | 半單李代數、根系、Dynkin 圖 |
| `hopf_algebra.py` | Hopf 代數 | 餘代數、餘乘法、龐加萊-伯克霍夫-維特定理 |

---

## 3. 線性代數與矩陣論

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `linear_algebra.py` | 線性代數 (Linear Algebra) | 向量、矩陣、特徵值、奇異值分解、PCA |

---

## 4. 實分析與複分析 (Analysis)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `real_analysis.py` | 實分析 (Real Analysis) | 極限、導數、積分、ODE 數值解 |
| `complex_analysis.py` | 複分析 (Complex Analysis) | 全純函數、柯西積分、留數定理、、保角映射 |
| `fourier_analysis.py` | 傅立葉分析 (Fourier Analysis) | 傅立葉級數、變換、頻譜分析 |
| `functional_analysis.py` | 泛函分析 (Functional Analysis) | 巴拿赫空間、希爾伯特空間、算子理論 |
| `integration.py` | 積分理論 (Integration Theory) | 黎曼/勒貝格積分、累次積分 |
| `measure_theory.py` | 測度論 (Measure Theory) | 測度空間、可測函數、LP 空間 |
| `calculus_of_variations.py` | 變分法 (Calculus of Variations) | 歐拉-拉格朗日方程、泛函極值 |

---

## 5. 數論 (Number Theory)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `number_theory.py` | 數論 (Number Theory) | 質數、同餘、迪菲-赫爾曼密碼系統 |
| `elliptic_curves.py` | 橢圓曲線 (Elliptic Curves) | 群結構、密碼學應用、BSD 猜想 |
| `l_functions.py` | L 函數 (L-Functions) | 黎曼 ζ 函數、狄利克雷 L 函數、函數方程 |
| `p_adic_numbers.py` | p 進數 (p-adic Numbers) | p 進賦值、亨澤爾引理、局部互反律 |
| `adeles.py` | 阿代數 (Adeles) | 局部緊群、整體域的自我對偶性 |
| `local_fields.py` | 局部域 (Local Fields) | 完備離散賦值域、伽羅瓦表示 |

---

## 6. 幾何與拓撲 (Geometry & Topology)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `topology.py` | 拓撲學 (Topology) | 開集、連續性、緊性、连通性 |
| `algebraic_topology.py` | 代數拓撲 (Algebraic Topology) | 同倫、同調、流形 |
| `algebraic_topology_advanced.py` | 高級代數拓撲 | 譜序列、光滑流形、纖維化 |
| `differential_geometry.py` | 微分幾何 (Differential Geometry) | 流形、切空間、余切叢 |
| `differential_geometry_enhanced.py` | 高等微分幾何 | 黎曼幾何、曲率、測地線 |
| `differential_geometry_advanced.py` | 進階微分幾何 | 幾何微分、陳類、主叢 |
| `kahler_geometry.py` | 凱勒幾何 (Kähler Geometry) | 凱勒流形、凱勒度量、霍奇理論 |
| `symplectic_geometry.py` | 辛幾何 (Symplectic Geometry) | 辛流形、哈密頓系統、莫尔斯理論 |
| `lie_groups.py` | 李群 (Lie Groups) | 連續變換群、指數映射、伴隨表示 |
| `symplectic_geometry.py` | 辛幾何 | 辛結構、哈密頓動力學 |

---

## 7. 圖論與組合數學 (Graph Theory & Combinatorics)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `graph_theory.py` | 圖論 (Graph Theory) | 圖遍歷、最短路徑、歐拉/漢密爾頓路徑、圖著色 |
| `graph_algorithms.py` | 圖算法 (Graph Algorithms) | 圖論算法的工程實現 |
| `combinatorics.py` | 組合數學 (Combinatorics) | 排列組合、分區、生成函數 |

---

## 8. 概率與統計 (Probability & Statistics)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `probability.py` | 概率論 (Probability Theory) | 概率空間、隨機變量、分佈、假設檢定 |
| `probability_enhanced.py` | 高等概率論 | 布朗運動、鞅、停時定理 |
| `statistics.py` | 統計學 (Statistics) | 描述統計、推論統計、迴歸分析 |
| `bayesian.py` | 貝葉斯統計 (Bayesian Statistics) | 貝葉斯推論、先驗/後驗分佈 |

---

## 9. 隨機過程 (Stochastic Processes)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `markov_chains.py` | 馬可夫鏈 (Markov Chains) | 離散/連續時間馬可夫鏈、平穩分佈 |
| `hmm.py` | 隱馬可夫模型 (Hidden Markov Models) | 前向-後向算法、維特比算法 |
| `kalman_filter.py` | 卡爾曼濾波 (Kalman Filtering) | 線性動力系統的最優估計 |
| `gaussian_process.py` | 高斯過程 (Gaussian Processes) | 貝葉斯非參數回歸、協方差函數 |

---

## 10. 機器學習與優化 (Machine Learning & Optimization)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `optimization.py` | 優化理論 (Optimization) | 梯度下降、牛頓法、限制優化 |
| `optimization_theory.py` | 優化理論擴展 | 凸優化、對偶理論、拉格朗日乘數 |
| `neural_network.py` | 神經網絡 (Neural Networks) | 前饋網絡、梯度下降、反向傳播 |
| `ml_basics.py` | 機器學習基礎 | 感知機、邏輯回歸、決策樹 |
| `reinforcement_learning.py` | 強化學習 (Reinforcement Learning) | 馬可夫決策過程、Q 學習、政策梯度 |
| `manifold_learning.py` | 流形學習 (Manifold Learning) | Isomap、LLE、t-SNE |
| `gnn.py` | 圖神經網絡 (Graph Neural Networks) | 圖卷積、消息傳遞、圖注意力 |
| `sparse_coding.py` | 稀疏編碼 (Sparse Coding) | 字典學習、OMP、壓縮感知 |
| `variational_inference.py` | 變分推斷 (Variational Inference) | 變分貝葉斯、ELBO、平均場近似 |

---

## 11. 代數幾何 (Algebraic Geometry)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `algebraic_geometry.py` | 代數幾何 (Algebraic Geometry) | 仿射/射影簇、扎里斯基拓撲、奇點 |
| `algebraic_geometry_advanced.py` | 高等代數幾何 | 概型、層、層 cohomology |
| `scheme_theory.py` | 概型理論 (Scheme Theory) | 局部環空間、層的截面、Serre 對偶 |

---

## 12. 表示論 (Representation Theory)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `representation_theory.py` | 表示論 (Representation Theory) | 群表示、指標、特征標理論 |
| `representation_theory_v127.py` | 表示論 (v1.27) | 同步發布版本 |
| `galois_representations.py` | 伽羅瓦表示 (Galois Representations) | 局部表示、ℓ-adic 表示、德拉塞雷猜想 |

---

## 13. 範疇論 (Category Theory)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `category_theory_advanced.py` | 範疇論 (Category Theory) | 函子、自然變換、極限 |
| `higher_category_theory.py` | 高階範疇論 (Higher Category Theory) | ∞-範疇、弱 Kan 復形 |
| `monoidal_categories.py` | 張量範疇 (Monoidal Categories) | 張量積、霍赫schild 同調 |
| `two_category.py` | 二範疇 (2-Categories) | 範疇的範疇、雙函子 |
| `derived_categories.py` | 導出範疇 (Derived Categories) | 三角範疇、導出函子、譜序列 |
| `sheaf.py` | 層理論基礎 | 預層、層、層化 |
| `sheaf_theory.py` | 層論 (Sheaf Theory) | 層 cohomology、 Čech cohomology、拓撲斯的莖 |
| `stacks.py` | 疊理論 (Stack Theory) | 疊、Artin 疊、DM 疊 |
| `model_category.py` | 模型範疇 (Model Categories) | Quillen 模型結構、同倫極限 |
| `spectral_sequence.py` | 譜序列 (Spectral Sequences) | 過濾的鏈複形、收斂性 |
| `adjunction_representation.py` | 伴隨表示 (Adjunction Representation) | 伴隨函子、伴隨表現 |

---

## 14. 同調代數 (Homological Algebra)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `homological_algebra_advanced.py` | 同調代數 (Homological Algebra) | 鏈複形、Ext、Tor、投射分解 |

---

## 15. 伽羅瓦理論 (Galois Theory)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `galois_theory.py` | 伽羅瓦理論 (Galois Theory) | 域擴張、可解群、尺規作圖 |

---

## 16. 自動機與計算理論 (Automata & Computability)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `automata_theory.py` | 自動機理論 (Automata Theory) | 有限狀態機、正規語言、下推自動機 |
| `automata_theory_v134.py` | 自動機理論 (v1.34) | 同步發布版本 |
| `computational_complexity_v134.py` | 計算複雜性 (Computational Complexity) | P/NP 問題、複雜性類別 |
| `formal_languages.py` | 形式語言 (Formal Languages) | 喬姆斯基層級、正規表達式、上下文無關語法 |
| `lambda_calculus.py` | λ 演算 (Lambda Calculus) | 匿名函數、閉包、Church 編碼 |

---

## 17. 微分方程與控制理論 (Differential Equations & Control)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `differential_equations.py` | 常微分方程 (ODEs) | 解的存在性、Euler/Runge-Kutta 數值解 |
| `pde.py` | 偏微分方程 (PDEs) | 熱方程、波方程、Green 函數 |
| `control_theory.py` | 控制理論 (Control Theory) | 狀態空間、可控性、最優控制 |

---

## 18. 非交換幾何與算子代數 (Noncommutative Geometry & Operator Algebras)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `noncommutative_geometry.py` | 非交換幾何 (Noncommutative Geometry) | 柯爾莫戈洛夫積分、遍歷理論 |
| `operator_algebras.py` | 算子代數 (Operator Algebras) | C*-代數、馮·諾伊曼代數、KK-理論 |
| `free_operator_algebras.py` | 自由算子代數 | 自由概率、自由獨立性 |
| `free_probability.py` | 自由概率論 (Free Probability) | 自由卷積、Rand 園子、Voiculescu 結構 |

---

## 19. K-理論與遍歷理論 (K-Theory & Ergodic Theory)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `k_theory.py` | K-理論 (K-Theory) | 矢量叢、Atiyah-Singer 指數定理 |
| `ergodic_theory.py` | 遍歷理論 (Ergodic Theory) | 保測變換、遍歷定理、熵 |

---

## 20. 自守形式 (Automorphic Forms)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `automorphic_forms.py` | 自守形式 (Automorphic Forms) | 模形式、艾森斯坦級數、朗蘭茲對應 |

---

## 21. 信息論與編碼理論 (Information & Coding Theory)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `information_theory.py` | 信息論 (Information Theory) | 熵、互信息、信道容量 |
| `coding_theory.py` | 編碼理論 (Coding Theory) | 線性碼、漢明碼、里德-所羅門碼 |

---

## 22. 信號處理與時間序列 (Signal Processing & Time Series)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `signal_processing.py` | 信號處理 (Signal Processing) | 濾波、FFT、頻譜估計 |
| `time_series.py` | 時間序列分析 (Time Series) | ARMA 模型、平穩性、預測 |

---

## 23. 數值分析 (Numerical Methods)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `numerical_methods.py` | 數值分析 (Numerical Analysis) | 數值積分、數值線性代數、方程求解 |

---

## 24. 符號計算 (Symbolic Computation)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `symbolic.py` | 符號計算 (Symbolic Computation) | 符號表達式、形式求導、方程化簡 |

---

## 25. 工具模組 (Utilities)

| 檔案 | 數學領域 | 說明 |
|------|---------|------|
| `__init__.py` | 模組導出 | 統一導出所有 63 個數學模組 |
| `exceptions.py` | 異常定義 | 自定義數學異常類型 |

---

## 數學領域分類統計

```
基礎邏輯與形式系統     :  7 個模組
代數結構               :  6 個模組
線性代數               :  1 個模組
分析學                 :  7 個模組
數論                   :  6 個模組
幾何與拓撲             :  9 個模組
圖論與組合數學         :  3 個模組
概率與統計             :  4 個模組
隨機過程               :  4 個模組
機器學習與優化         :  9 個模組
代數幾何               :  3 個模組
表示論                 :  3 個模組
範疇論                 : 11 個模組
同調代數               :  1 個模組
伽羅瓦理論             :  1 個模組
自動機與計算理論       :  5 個模組
微分方程與控制         :  3 個模組
非交換幾何與算子代數   :  4 個模組
K-理論與遍歷理論       :  2 個模組
自守形式               :  1 個模組
信息論與編碼           :  2 個模組
信號處理與時間序列     :  2 個模組
數值分析               :  1 個模組
符號計算               :  1 個模組
工具模組               :  2 個模組
─────────────────────────────────
總計                   : 93 個數學模組
另有版本迭代模組       :  v1.27, v1.34 等
```

---

## 版本對照表 (Version Map)

| 版本 | 模組 |
|------|------|
| v1.27 | `representation_theory_v127.py` |
| v1.34 | `automata_theory_v134.py`, `computational_complexity_v134.py` |

---

## 依賴關係圖（簡化）

```
邏輯/集合
    ↓
代數結構 → 線性代數 → 拓撲/幾何
    ↓                ↓
數論          代數拓撲
    ↓                ↓
代數幾何 ←── 表示論
    ↓
    範疇論 ←── 同調代數
              ↓
         層論/疊
```

---

*本檔案由 code-doc_generator 技能自動生成*