"""Statistics module: descriptive statistics and regression."""

from typing import List, Tuple, Optional
import math


def mean(data):
    return 0.0 if not data else sum(data) / len(data)


def median(data):
    if not data: return 0.0
    s = sorted(data); n = len(s)
    return s[n//2] if n%2==1 else (s[n//2-1]+s[n//2])/2


def mode(data):
    if not data: return []
    from collections import Counter
    counts = Counter(data);
    mx = max(counts.values())
    return [k for k,v in counts.items() if v==mx]


def variance(data, sample=True):
    if len(data)<2: return 0.0
    m = mean(data)
    ss = sum((x-m)**2 for x in data)
    n = len(data)-1 if sample else len(data)
    return ss / n


def std_dev(data, sample=True):
    return math.sqrt(variance(data, sample))


def covariance(x, y):
    if len(x)!=len(y) or len(x)<2: return 0.0
    n=len(x); mx,my=mean(x),mean(y)
    return sum((x[i]-mx)*(y[i]-my) for i in range(n)) / (n-1)


def correlation(x, y):
    if len(x)!=len(y) or len(x)<2: return 0.0
    c=covariance(x,y); sx=std_dev(x); sy=std_dev(y)
    return 0.0 if sx==0 or sy==0 else c/(sx*sy)


def linear_regression(x, y):
    if len(x)!=len(y) or len(x)<2: return (0.0,0.0)
    n=len(x); sx,sy=sum(x),sum(y)
    sxy=sum(x[i]*y[i] for i in range(n))
    sx2=sum(xi**2 for xi in x)
    denom=n*sx2-sx**2
    if denom==0: return (0.0,mean(y))
    slope=(n*sxy-sx*sy)/denom
    intercept=(sy-slope*sx)/n
    return (slope,intercept)


def skewness(data):
    if len(data)<3: return 0.0
    n=len(data); m=mean(data); s=std_dev(data)
    if s==0: return 0.0
    return (n/((n-1)*(n-2)))*sum(((x-m)/s)**3 for x in data)


def kurtosis(data):
    if len(data)<4: return 0.0
    n=len(data); m=mean(data); s=std_dev(data)
    if s==0: return 0.0
    return (n*(n+1)/((n-1)*(n-2)*(n-3)))*sum((x-m)**4 for x in data)/(s**4) - 3*(n-1)**2/((n-2)*(n-3))


def t_test_one_sample(data, mu0=0.0):
    n=len(data)
    if n<2: return (0.0,1.0)
    xb=mean(data); s=std_dev(data)
    if s==0: return (float('inf'),0.0) if xb!=mu0 else (0.0,1.0)
    t=(xb-mu0)/(s/(n**0.5))
    z=abs(t)/(2**0.5)
    p=2*(1-0.5*(1+math.erf(z)))
    return (t,p)


def confidence_interval_mean(data, confidence=0.95):
    n=len(data)
    if n<2: return (0.0,0.0)
    xb=mean(data); s=std_dev(data)
    zs={0.90:1.645,0.95:1.96,0.99:2.576}
    z=zs.get(confidence,1.96)
    m=z*s/(n**0.5)
    return (xb-m, xb+m)


def anova_one_way(groups):
    k=len(groups); nt=sum(len(g) for g in groups)
    if k<2 or nt<=k: return (0.0,1.0,0.0)
    gm=[mean(g) for g in groups]
    om=mean([x for g in groups for x in g])
    SSb=sum(len(groups[i])*(gm[i]-om)**2 for i in range(k))
    dfb=k-1
    SSw=sum(sum((x-gm[i])**2 for x in groups[i]) for i in range(k))
    dfw=nt-k
    if SSw==0: return (float('inf'),0.0,1.0)
    MSb=SSb/dfb; MSw=SSw/dfw
    F=MSb/MSw
    # P-value approximation
    z=(F-1)/(2**0.5)
    p=2*(1-0.5*(1+math.erf(z)))
    if p<1e-10: p=1e-10
    if p>1.0: p=1.0
    eta=SSb/(SSb+SSw)
    return (F,p,eta)


def chi_square_test(observed, expected=None):
    n=sum(observed); k=len(observed)
    if k==0: return (0.0,1.0)
    if expected is None: expected=[n/k]*k
    chi2=sum((observed[i]-expected[i])**2/expected[i] for i in range(k) if expected[i]>0)
    df=k-1
    z=(chi2-df)/(2*df)**0.5
    p=2*(1-0.5*(1+math.erf(abs(z)/(2**0.5))))
    return (chi2,p)


def mann_whitney_u(x, y):
    """Mann-Whitney U test."""
    n1, n2 = len(x), len(y)
    if n1==0 or n2==0: return (0.0,1.0)
    # Combine and rank
    combined = sorted([(val,0) for val in x] + [(val,1) for val in y])
    # Assign ranks
    ranks = [0.0] * (n1+n2)
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    # Sum of ranks for group x
    R1 = sum(ranks[i] for i in range(n1))
    U1 = R1 - n1*(n1+1)/2
    U2 = n1*n2 - U1
    U = min(U1, U2)
    # Normal approximation
    import math
    mu_U = n1*n2/2
    sigma_U = (n1*n2*(n1+n2+1)/12)**0.5
    if sigma_U == 0: return (U,1.0)
    z = (U - mu_U) / sigma_U
    p = 2*(1-0.5*(1+math.erf(abs(z)/(2**0.5))))
    return (U, p)


def kruskal_wallis(groups):
    """Kruskal-Wallis H test."""
    k = len(groups)
    if k < 2:
        return (0.0, 1.0)
    # Combine all observations
    all_vals = []
    group_idx = []
    for i, g in enumerate(groups):
        all_vals.extend(g)
        group_idx.extend([i] * len(g))
    n_total = len(all_vals)
    if n_total == 0:
        return (0.0, 1.0)
    # Rank all observations
    indexed = sorted(zip(all_vals, group_idx))
    ranks = [0.0] * n_total
    i = 0
    while i < len(indexed):
        j = i
        while j < len(indexed) and indexed[j][0] == indexed[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2
        for k_idx in range(i, j):
            ranks[k_idx] = avg_rank
        i = j
    # Sum of ranks per group
    R_i = [0.0] * k
    n_i = [0] * k
    for idx in range(n_total):
        g = indexed[idx][1]
        R_i[g] += ranks[idx]
        n_i[g] += 1
    # H statistic
    H = 12 / (n_total * (n_total + 1)) * sum(R_i[g]**2 / n_i[g] for g in range(k) if n_i[g] > 0) - 3 * (n_total + 1)
    # Chi-square approximation
    import math
    df = k - 1
    if df <= 0:
        return (H, 1.0)
    # Approximate p-value
    z = (H - df) / (2 * df) ** 0.5
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / (2 ** 0.5))))
    return (H, p)


def linear_regression_diagnostics(x: List[float], y: List[float]) -> dict:
    """Linear regression with diagnostics."""
    n = len(x)
    if n != len(y) or n < 2:
        return {}
    
    x_mean, y_mean = mean(x), mean(y)
    
    # Compute slope and intercept
    sxx = sum((xi - x_mean)**2 for xi in x)
    sxy = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    
    if sxx == 0:
        return {}
    
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    
    # Compute fitted values and residuals
    fitted = [intercept + slope * xi for xi in x]
    residuals = [y[i] - fitted[i] for i in range(n)]
    
    # R-squared
    ss_res = sum(r**2 for r in residuals)
    ss_tot = sum((yi - y_mean)**2 for yi in y)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'residuals': residuals,
        'fitted_values': fitted
    }


def mann_kendall(x: List[float]) -> Tuple[float, float]:
    """Mann-Kendall trend test.
    
    Tests for monotonic trend in time series.
    
    Args:
        x: Time series data
        
    Returns:
        (tau, p-value)
    """
    import math
    
    n = len(x)
    if n < 2:
        return 0.0, 1.0
    
    # Count concordant and discordant pairs
    S = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if x[j] > x[i]:
                S += 1
            elif x[j] < x[i]:
                S -= 1
    
    # Variance of S
    var_S = n * (n - 1) * (2 * n + 5) / 18
    if var_S == 0:
        return 0.0, 1.0
    
    # Standardized test statistic
    if S > 0:
        Z = (S - 1) / math.sqrt(var_S)
    elif S < 0:
        Z = (S + 1) / math.sqrt(var_S)
    else:
        Z = 0.0
    
    # Approximate p-value (two-tailed)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(Z) / math.sqrt(2))))
    
    # Kendall's tau
    tau = S / (n * (n - 1) / 2)
    
    return tau, p


def wilcoxon_signed_rank(x: List[float], mu: float = 0.0) -> Tuple[float, float]:
    """Wilcoxon signed-rank test for one sample.
    
    Tests whether median of differences from mu is zero.
    
    Args:
        x: Sample data
        mu: Hypothesized median (default 0)
        
    Returns:
        (W statistic, p-value)
    """
    import math
    
    # Compute differences
    diffs = [v - mu for v in x if v != mu]
    n = len(diffs)
    
    if n == 0:
        return 0.0, 1.0
    
    # Rank absolute differences
    abs_diffs = [abs(d) for d in diffs]
    ranked = sorted(range(n), key=lambda i: abs_diffs[i])
    
    # Assign ranks (average for ties)
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and abs_diffs[ranked[j]] == abs_diffs[ranked[j + 1]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1  # 1-indexed ranks
        for k in range(i, j + 1):
            ranks[ranked[k]] = avg_rank
        i = j + 1
    
    # Compute W+ (sum of ranks for positive differences)
    W_plus = sum(ranks[i] for i in range(n) if diffs[i] > 0)
    W_minus = sum(ranks[i] for i in range(n) if diffs[i] < 0)
    W = min(W_plus, W_minus)
    
    # Approximate p-value (normal approximation)
    mean_W = n * (n + 1) / 4
    var_W = n * (n + 1) * (2 * n + 1) / 24
    
    if var_W == 0:
        return W, 1.0
    
    Z = (W - mean_W) / math.sqrt(var_W)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(Z) / math.sqrt(2))))
    
    return W, p


def wilcoxon_rank_sum(x: List[float], y: List[float]) -> Tuple[float, float]:
    """Wilcoxon rank-sum test (Mann-Whitney U test alternative).
    
    Tests whether two samples come from same distribution.
    
    Args:
        x: First sample
        y: Second sample
        
    Returns:
        (U statistic, p-value)
    """
    import math
    
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return 0.0, 1.0
    
    # Combine and rank
    combined = [(v, 0) for v in x] + [(v, 1) for v in y]
    combined.sort(key=lambda p: p[0])
    
    # Assign ranks
    ranks = [0.0] * (n1 + n2)
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) - 1 and combined[j][0] == combined[j + 1][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[k] = avg_rank
        i = j + 1
    
    # Sum of ranks for first sample
    rank_sum = sum(ranks[i] for i in range(n1))
    
    # U statistic
    U1 = rank_sum - n1 * (n1 + 1) / 2
    U2 = n1 * n2 - U1
    U = min(U1, U2)
    
    # Normal approximation
    mean_U = n1 * n2 / 2
    var_U = n1 * n2 * (n1 + n2 + 1) / 12
    
    if var_U == 0:
        return U, 1.0
    
    Z = (U - mean_U) / math.sqrt(var_U)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(Z) / math.sqrt(2))))
    
    return U, p
