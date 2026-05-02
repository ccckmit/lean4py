"""Tests for Bayesian statistics module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.bayesian import (
    GaussianPrior, BetaPrior,
    posterior_update_normal, posterior_update_beta_binomial,
    metropolis_hastings, bayesian_linear_regression,
    compute_bayes_factor
)
import math


class TestGaussianPrior:
    """Tests for Gaussian prior."""
    
    def test_initialization(self):
        """Test GaussianPrior initializes correctly."""
        prior = GaussianPrior(mean=0.0, variance=1.0)
        
        assert prior.mean == 0.0
        assert prior.variance == 1.0
        assert prior.std == 1.0
    
    def test_log_likelihood(self):
        """Test log likelihood computation."""
        prior = GaussianPrior(mean=0.0, variance=1.0)
        
        ll_at_mean = prior.log_likelihood(0.0)
        ll_away = prior.log_likelihood(1.0)
        
        assert ll_at_mean > ll_away  # Higher likelihood at mean
        assert ll_at_mean < 0  # Log likelihood is negative
    
    def test_likelihood_at_mean(self):
        """Test likelihood is maximum at prior mean."""
        prior = GaussianPrior(mean=5.0, variance=2.0)
        
        ll_mean = prior.log_likelihood(5.0)
        ll_other = prior.log_likelihood(0.0)
        
        assert ll_mean > ll_other


class TestBetaPrior:
    """Tests for Beta prior."""
    
    def test_initialization(self):
        """Test BetaPrior initializes correctly."""
        prior = BetaPrior(alpha=2.0, beta=5.0)
        
        assert prior.alpha == 2.0
        assert prior.beta == 5.0
    
    def test_mean_variance(self):
        """Test mean and variance computation."""
        prior = BetaPrior(alpha=2.0, beta=2.0)
        
        assert prior.mean() == 0.5
        assert prior.variance() > 0
    
    def test_log_likelihood_valid(self):
        """Test log likelihood for valid probabilities."""
        prior = BetaPrior(alpha=1.0, beta=1.0)  # Uniform
        
        ll = prior.log_likelihood(0.5)
        assert not math.isinf(ll)
        
        ll2 = prior.log_likelihood(0.0)
        assert math.isinf(ll2)  # Should be -inf for p=0 with alpha=1
    
    def test_invalid_probability(self):
        """Test log likelihood for invalid probabilities."""
        prior = BetaPrior(alpha=1.0, beta=1.0)
        
        ll_neg = prior.log_likelihood(-0.1)
        ll_high = prior.log_likelihood(1.1)
        
        assert math.isinf(ll_neg)
        assert math.isinf(ll_high)


class TestPosteriorUpdateNormal:
    """Tests for normal-normal conjugate update."""
    
    def test_perfect_prior(self):
        """Test when prior matches data exactly."""
        prior_mean = 5.0
        prior_var = 1.0
        data = [5.0, 5.0, 5.0]
        likelihood_var = 1.0
        
        post_mean, post_var = posterior_update_normal(
            prior_mean, prior_var, data, likelihood_var
        )
        
        # Posterior mean should be close to 5.0
        assert abs(post_mean - 5.0) < 0.1
        # Posterior variance should decrease
        assert post_var < prior_var
    
    def test_empty_data(self):
        """Test with no data returns prior."""
        prior_mean = 0.0
        prior_var = 1.0
        
        post_mean, post_var = posterior_update_normal(
            prior_mean, prior_var, [], 1.0
        )
        
        assert post_mean == prior_mean
        assert post_var == prior_var
    
    def test_uncertain_prior(self):
        """Test with very uncertain prior."""
        prior_mean = 0.0
        prior_var = 100.0  # Very uncertain
        data = [1.0, 2.0, 3.0]
        likelihood_var = 1.0
        
        post_mean, post_var = posterior_update_normal(
            prior_mean, prior_var, data, likelihood_var
        )
        
        # Posterior should be closer to data mean (2.0)
        assert 1.5 < post_mean < 2.5
        assert post_var < prior_var


class TestPosteriorUpdateBetaBinomial:
    """Tests for Beta-Binomial conjugate update."""
    
    def test_uniform_prior(self):
        """Test with uniform prior (Beta(1,1))."""
        prior_alpha = 1.0
        prior_beta = 1.0
        successes = 7
        trials = 10
        
        post_alpha, post_beta = posterior_update_beta_binomial(
            prior_alpha, prior_beta, successes, trials
        )
        
        assert post_alpha == 1.0 + 7.0
        assert post_beta == 1.0 + 3.0
    
    def test_strong_prior(self):
        """Test with strong prior."""
        prior_alpha = 50.0
        prior_beta = 50.0  # Expect p ≈ 0.5
        successes = 9
        trials = 10  # Observed p = 0.9
        
        post_alpha, post_beta = posterior_update_beta_binomial(
            prior_alpha, prior_beta, successes, trials
        )
        
        # Posterior should be between prior (0.5) and data (0.9)
        post_mean = post_alpha / (post_alpha + post_beta)
        assert 0.5 < post_mean < 0.9


class TestMetropolisHastings:
    """Tests for MCMC sampling."""

    def test_sample_normal_target(self):
        """Test sampling from a normal-like target."""
        # Target: log N(0, 1)
        def log_target(x):
            return -0.5 * x**2

        samples = metropolis_hastings(
            log_target, initial=0.0,
            n_samples=5000, proposal_std=1.0
        )

        assert len(samples) == 5000
        # Mean should be close to 0
        sample_mean = sum(samples) / len(samples)
        assert abs(sample_mean) < 0.2
    
    def test_samples_vary(self):
        """Test that samples are not all identical."""
        def log_target(x):
            return -0.5 * (x - 5)**2  # N(5, 1)
        
        samples = metropolis_hastings(
            log_target, initial=0.0,
            n_samples=500, proposal_std=2.0
        )
        
        # Samples should vary
        assert max(samples) - min(samples) > 1.0


class TestBayesianLinearRegression:
    """Tests for Bayesian linear regression."""
    
    def test_simple_case(self):
        """Test simple linear regression."""
        # y = 2*x + 1 with noise
        x = [[1.0], [2.0], [3.0], [4.0]]
        y = [3.0, 5.0, 7.0, 9.0]  # Perfect: 2*x + 1
        
        post_mean, post_cov = bayesian_linear_regression(x, y)
        
        assert len(post_mean) == 1
        assert len(post_cov) == 1
        # Coefficient should be close to 2
        assert 1.5 < post_mean[0] < 2.5
    
    def test_empty_data(self):
        """Test with empty data."""
        post_mean, post_cov = bayesian_linear_regression([], [])
        
        assert post_mean == []
        assert post_cov == []
    
    def test_with_prior(self):
        """Test with informative prior."""
        x = [[1.0], [2.0]]
        y = [2.0, 4.0]  # y = 2*x
        
        prior_mean = [10.0]  # Strong prior that coeff is 10
        prior_precision = [[1.0]]  # Moderate precision
        
        post_mean, _ = bayesian_linear_regression(
            x, y, prior_mean=prior_mean, 
            prior_precision=prior_precision
        )
        
        # Posterior should be between prior (10) and MLE (2)
        assert 2.0 < post_mean[0] < 10.0


class TestBayesFactor:
    """Tests for Bayes factor computation."""
    
    def test_equal_models(self):
        """Test when both models fit equally well."""
        # Same log likelihoods
        ll1 = [-1.0, -2.0, -1.5]
        ll2 = [-1.0, -2.0, -1.5]
        
        log_k = compute_bayes_factor(ll1, ll2)
        assert abs(log_k) < 0.1  # log K ≈ 0, so K ≈ 1
    
    def test_model_1_better(self):
        """Test when model 1 fits better."""
        ll1 = [-1.0, -1.0, -1.0]  # Better fit
        ll2 = [-5.0, -5.0, -5.0]  # Worse fit
        
        log_k = compute_bayes_factor(ll1, ll2)
        assert log_k > 0  # Positive log K means model 1 is better
    
    def test_mismatch_length(self):
        """Test with mismatched lengths."""
        log_k = compute_bayes_factor([1.0], [1.0, 2.0])
        assert log_k == 0.0
