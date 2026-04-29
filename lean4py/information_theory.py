from typing import List
import math


def entropy(prob_dist: List[float]) -> float:
    """Shannon entropy H(X) = -Σ p_i log2(p_i)."""
    if not prob_dist:
        return 0.0
    total = sum(prob_dist)
    if abs(total - 1.0) > 1e-10:
        prob_dist = [p / total for p in prob_dist]
    h = 0.0
    for p in prob_dist:
        if p > 0:
            h -= p * math.log2(p)
    return h


def mutual_information(joint_dist: List[List[float]], x_marginal: List[float], y_marginal: List[float]) -> float:
    """Mutual information I(X;Y) = Σ p_xy log2(p_xy/(p_x p_y))."""
    if not joint_dist or not x_marginal or not y_marginal:
        return 0.0
    mi = 0.0
    for i in range(len(joint_dist)):
        for j in range(len(joint_dist[0])):
            p_xy = joint_dist[i][j]
            if p_xy > 0:
                p_x, p_y = x_marginal[i], y_marginal[j]
                if p_x > 0 and p_y > 0:
                    mi += p_xy * math.log2(p_xy / (p_x * p_y))
    return mi


def kl_divergence(p: List[float], q: List[float]) -> float:
    """KL divergence D_KL(P||Q) = Σ p_i log2(p_i/q_i)."""
    if len(p) != len(q):
        raise ValueError("p and q must have same length")
    kl = 0.0
    for p_i, q_i in zip(p, q):
        if p_i > 0:
            if q_i <= 0:
                return float('inf')
            kl += p_i * math.log2(p_i / q_i)
    return kl
