"""Bayesian statistics module."""

from typing import List, Tuple, Callable, Optional
import math
from collections import Counter


class GaussianPrior:
    """Gaussian (Normal) prior distribution."""
    
    def __init__(self, mean: float, variance: float):
        self.mean = mean
        self.variance = variance
        self.std = math.sqrt(variance)
    
    def log_likelihood(self, x: float) -> float:
        """Log likelihood of observing x."""
        return -0.5 * math.log(2 * math.pi * self.variance) - \
               (x - self.mean) ** 2 / (2 * self.variance)


class BetaPrior:
    """Beta prior distribution for probabilities."""
    
    def __init__(self, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta
    
    def log_likelihood(self, p: float) -> float:
        """Log likelihood of probability p."""
        if p <= 0 or p >= 1:
            return -float('inf')
        return (self.alpha - 1) * math.log(p) + \
               (self.beta - 1) * math.log(1 - p)
    
    def mean(self) -> float:
        """Mean of Beta distribution."""
        return self.alpha / (self.alpha + self.beta)
    
    def variance(self) -> float:
        """Variance of Beta distribution."""
        total = self.alpha + self.beta
        return (self.alpha * self.beta) / (total ** 2 * (total + 1))


def posterior_update_normal(
    prior_mean: float,
    prior_variance: float,
    data: List[float],
    likelihood_variance: float
) -> Tuple[float, float]:
    """Update Gaussian prior with normal likelihood (conjugate prior).
    
    Args:
        prior_mean: Mean of prior Gaussian
        prior_variance: Variance of prior Gaussian
        data: Observed data points
        likelihood_variance: Known variance of likelihood
        
    Returns:
        (posterior_mean, posterior_variance)
    """
    if not data:
        return prior_mean, prior_variance
    
    n = len(data)
    data_mean = sum(data) / n
    
    # Posterior variance
    posterior_variance = 1.0 / (1.0 / prior_variance + n / likelihood_variance)
    
    # Posterior mean
    posterior_mean = posterior_variance * (
        prior_mean / prior_variance + n * data_mean / likelihood_variance
    )
    
    return posterior_mean, posterior_variance


def posterior_update_beta_binomial(
    prior_alpha: float,
    prior_beta: float,
    successes: int,
    trials: int
) -> Tuple[float, float]:
    """Update Beta prior with Binomial likelihood (conjugate prior).
    
    Args:
        prior_alpha: Alpha parameter of Beta prior
        prior_beta: Beta parameter of Beta prior
        successes: Number of successes observed
        trials: Total number of trials
        
    Returns:
        (posterior_alpha, posterior_beta)
    """
    posterior_alpha = prior_alpha + successes
    posterior_beta = prior_beta + (trials - successes)
    return posterior_alpha, posterior_beta


def metropolis_hastings(
    log_target: Callable[[float], float],
    initial: float,
    n_samples: int = 1000,
    proposal_std: float = 1.0
) -> List[float]:
    """Metropolis-Hastings MCMC sampler.
    
    Args:
        log_target: Log of target distribution (unnormalized)
        initial: Initial sample value
        n_samples: Number of samples to generate
        proposal_std: Standard deviation of proposal distribution
        
    Returns:
        List of samples
    """
    import random
    
    samples = []
    current = initial
    current_log_prob = log_target(current)
    
    for _ in range(n_samples):
        # Propose new value
        proposal = current + random.gauss(0, proposal_std)
        proposal_log_prob = log_target(proposal)
        
        # Acceptance ratio
        log_alpha = proposal_log_prob - current_log_prob
        
        # Accept or reject
        if math.log(random.random()) < log_alpha:
            current = proposal
            current_log_prob = proposal_log_prob
        
        samples.append(current)
    
    return samples


def bayesian_linear_regression(
    x: List[List[float]],
    y: List[float],
    prior_mean: Optional[List[float]] = None,
    prior_precision: Optional[List[List[float]]] = None,
    noise_variance: float = 1.0
) -> Tuple[List[float], List[List[float]]]:
    """Bayesian linear regression with Gaussian prior.
    
    Args:
        x: Input features (n_samples x n_features)
        y: Target values
        prior_mean: Prior mean of coefficients (default: zeros)
        prior_precision: Prior precision matrix (inverse covariance)
        noise_variance: Known noise variance
        
    Returns:
        (posterior_mean, posterior_covariance)
    """
    n = len(x)
    if n == 0:
        return [], []
    
    m = len(x[0])
    
    # Default prior: zero mean, identity precision
    if prior_mean is None:
        prior_mean = [0.0] * m
    if prior_precision is None:
        prior_precision = [[1.0 if i == j else 0.0 for j in range(m)] 
                           for i in range(m)]
    
    # Compute X^T X and X^T y
    xtx = [[0.0] * m for _ in range(m)]
    xty = [0.0] * m
    
    for k in range(n):
        for i in range(m):
            xty[i] += x[k][i] * y[k]
            for j in range(m):
                xtx[i][j] += x[k][i] * x[k][j]
    
    # Posterior precision = prior_precision + X^T X / noise_variance
    posterior_precision = [row[:] for row in prior_precision]
    for i in range(m):
        for j in range(m):
            posterior_precision[i][j] += xtx[i][j] / noise_variance
    
    # Invert to get covariance
    if m == 1:
        posterior_variance = [[1.0 / posterior_precision[0][0]]]
    else:
        # 2x2 matrix inversion
        a, b, c, d = posterior_precision[0][0], posterior_precision[0][1], \
                     posterior_precision[1][0], posterior_precision[1][1]
        det = a * d - b * c
        if det == 0:
            posterior_variance = [[1.0, 0.0], [0.0, 1.0]]
        else:
            posterior_variance = [[d/det, -b/det], [-c/det, a/det]]
    
    # Posterior mean = posterior_cov @ (prior_precision @ prior_mean + X^T y / noise_variance)
    # Compute temp = prior_precision @ prior_mean + X^T y / noise_variance
    temp = [0.0] * m
    for i in range(m):
        # prior_precision @ prior_mean
        for j in range(m):
            temp[i] += prior_precision[i][j] * prior_mean[j]
        # Add X^T y / noise_variance
        temp[i] += xty[i] / noise_variance
    
    # posterior_mean = posterior_cov @ temp
    posterior_mean = [0.0] * m
    for i in range(m):
        for j in range(m):
            posterior_mean[i] += posterior_variance[i][j] * temp[j]
    
    return posterior_mean, posterior_variance


def compute_bayes_factor(
    log_likelihood_1: List[float],
    log_likelihood_2: List[float]
) -> float:
    """Compute Bayes factor comparing two models.
    
    K = P(D|M1) / P(D|M2)
    
    Args:
        log_likelihood_1: Log likelihoods under model 1
        log_likelihood_2: Log likelihoods under model 2
        
    Returns:
        Log Bayes factor (log K)
    """
    if len(log_likelihood_1) != len(log_likelihood_2):
        return 0.0
    
    # Use log-sum-exp trick for numerical stability
    max_ll1 = max(log_likelihood_1)
    max_ll2 = max(log_likelihood_2)
    
    sum1 = sum(math.exp(ll - max_ll1) for ll in log_likelihood_1)
    sum2 = sum(math.exp(ll - max_ll2) for ll in log_likelihood_2)
    
    log_k = max_ll1 + math.log(sum1) - (max_ll2 + math.log(sum2))
    return log_k
