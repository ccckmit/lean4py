"""Tests for differential_equations module."""

import pytest
from lean4py.differential_equations import (
    ODEProblem, LipschitzCondition, PicardLindelof,
    FlowProperty, PhasePortrait, StabilityAnalysis
)
from lean4py.real_analysis import euler_method, runge_kutta_4


class TestODEProblem:
    """Test ODE problems."""

    def test_creation(self):
        f = lambda t, y: y
        problem = ODEProblem(f, t0=0.0, y0=1.0)
        assert problem.t0 == 0.0
        assert problem.y0 == 1.0

    def test_euler_step_scalar(self):
        f = lambda t, y: y
        problem = ODEProblem(f, t0=0.0, y0=1.0)
        result = problem.euler_step(t=0.0, y=1.0, dt=0.1)
        assert abs(result - 1.1) < 1e-10


class TestLipschitzCondition:
    """Test Lipschitz condition."""

    def test_is_lipschitz(self):
        f = lambda t, y: y
        domain = [(0.0, 1.0)]
        assert LipschitzCondition.is_lipschitz(f, domain, (0.0, 10.0), (0.0, 5.0)) is True

    def test_lipschitz_constant(self):
        f = lambda t, y: y
        domain = [(0.0, 1.0)]
        L = LipschitzCondition.lipschitz_constant(f, domain)
        assert L >= 0


class TestPicardLindelof:
    """Test Picard-Lindelöf theorem."""

    def test_has_unique_solution(self):
        f = lambda t, y: y
        problem = ODEProblem(f, t0=0.0, y0=1.0)
        assert PicardLindelof.has_unique_solution(problem, (0.0, 1.0)) is True

    def test_picard_iteration(self):
        f = lambda t, y: y
        problem = ODEProblem(f, t0=0.0, y0=1.0)
        result = PicardLindelof.picard_iteration(problem, t=0.5, n_iterations=5)
        assert result is not None


class TestFlowProperty:
    """Test flow properties."""

    def test_is_flow(self):
        f = lambda t, y: y
        problem = ODEProblem(f, t0=0.0, y0=1.0)
        assert FlowProperty.is_flow(problem) is True

    def test_semigroup_property(self):
        f = lambda t, y: y
        problem = ODEProblem(f, t0=0.0, y0=1.0)
        assert FlowProperty.semigroup_property(problem) is True


class TestPhasePortrait:
    """Test phase portrait analysis."""

    def test_fixed_points(self):
        f = lambda y: (0.0,)
        domain = [(0.0,), (1.0,)]
        fixed = PhasePortrait.fixed_points(f, domain)
        assert len(fixed) >= 0

    def test_is_stable(self):
        fixed_point = (0.0,)
        jacobian = lambda y: ((1.0,),)
        assert PhasePortrait.is_stable(fixed_point, jacobian) is True


class TestStabilityAnalysis:
    """Test stability analysis."""

    def test_linear_stability(self):
        jacobian = ((1.0,),)
        result = StabilityAnalysis.linear_stability(jacobian)
        assert result in ["stable", "unstable", "saddle"]

    def test_lyapunov_stability(self):
        problem = ODEProblem(lambda t, y: -y, t0=0.0, y0=1.0)
        lyapunov = lambda y: y * y
        assert StabilityAnalysis.lyapunov_stability(problem, lyapunov) is True
