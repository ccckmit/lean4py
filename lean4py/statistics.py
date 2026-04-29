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
