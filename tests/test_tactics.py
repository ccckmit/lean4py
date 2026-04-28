import pytest
from lean4py.tactics import (
    Tactic,
    tactic_rfl, tactic_exact, tactic_apply, tactic_simp,
    tactic_assume, tactic_have,
    intros, intros_tactic,
    by_contra, by_contra_tactic,
    cases, cases_tactic,
    induction, induction_tactic,
    rewrite, rewrite_tactic,
    split, split_tactic,
    left, left_tactic,
    right, right_tactic,
    use, use_tactic,
    show, show_tactic,
    by, by_tactic,
    sorry, sorry_tactic,
    calc, calc_tactic,
    intro, intro_tactic,
    apply_tactic,
    TacticProof,
    TacticState,
)
from lean4py.logic import Prop, ProofStep


class TestTactic:
    def test_tactic_init(self):
        t = Tactic("rfl")
        assert t.name == "rfl"
        assert t.args == ()

    def test_tactic_with_args(self):
        t = Tactic("exact", Prop('p'))
        assert t.name == "exact"
        assert len(t.args) == 1

    def test_tactic_repr_no_args(self):
        t = Tactic("rfl")
        assert repr(t) == "tactic.rfl"

    def test_tactic_repr_with_args(self):
        t = Tactic("exact", Prop('p'))
        r = repr(t)
        assert "tactic.exact" in r


class TestTacticFunctions:
    def test_tactic_rfl(self):
        t = tactic_rfl()
        assert t.name == "rfl"

    def test_tactic_exact(self):
        p = Prop('p')
        t = tactic_exact(p)
        assert t.name == "exact"
        assert t.args[0] == p

    def test_tactic_apply(self):
        t = tactic_apply("H1")
        assert t.name == "apply"
        assert t.args[0] == "H1"

    def test_tactic_simp(self):
        t = tactic_simp()
        assert t.name == "simp"

    def test_tactic_assume(self):
        t = tactic_assume("H")
        assert t.name == "assume"
        assert t.args[0] == "H"

    def test_tactic_have(self):
        t = tactic_have("H")
        assert t.name == "have"
        assert t.args[0] == "H"


class TestProofStepFunctions:
    def test_intros_single(self):
        step = intros("H")
        assert step.tactic == "intros"
        assert step.args[0] == ["H"]

    def test_intros_list(self):
        step = intros(["H1", "H2"])
        assert step.tactic == "intros"
        assert step.args[0] == ["H1", "H2"]

    def test_by_contra(self):
        p = Prop('p')
        step = by_contra("H", p)
        assert step.tactic == "by_contra"
        assert step.args[1] == p

    def test_cases(self):
        p1, p2 = Prop('p1'), Prop('p2')
        step = cases("H", [p1, p2])
        assert step.tactic == "cases"
        assert len(step.args[1]) == 2

    def test_split(self):
        step = split()
        assert step.tactic == "split"

    def test_left(self):
        step = left()
        assert step.tactic == "left"

    def test_right(self):
        step = right()
        assert step.tactic == "right"

    def test_sorry(self):
        step = sorry()
        assert step.tactic == "sorry"

    def test_calc(self):
        step = calc([tactic_rfl()])
        assert step.tactic == "calc"


class TestTacticProof:
    def test_proof_init(self):
        p = TacticProof()
        assert p.steps == []

    def test_proof_add(self):
        p = TacticProof()
        p.add(tactic_rfl())
        assert len(p.steps) == 1

    def test_proof_repr(self):
        p = TacticProof([tactic_rfl()])
        r = repr(p)
        assert "rfl" in r


class TestTacticState:
    def test_state_init(self):
        s = TacticState()
        assert s.goals == []
        assert s.hypotheses == {}

    def test_add_hypothesis(self):
        s = TacticState()
        p = Prop('p')
        s.add_hypothesis("H", p)
        assert "H" in s.hypotheses
        assert s.hypotheses["H"] == p

    def test_get_hypothesis(self):
        s = TacticState()
        p = Prop('p')
        s.add_hypothesis("H", p)
        assert s.get_hypothesis("H") == p

    def test_get_hypothesis_missing(self):
        s = TacticState()
        assert s.get_hypothesis("H") is None

    def test_pop_goal(self):
        s = TacticState(goals=[Prop('p'), Prop('q')])
        goal = s.pop_goal()
        assert goal == Prop('p')
        assert len(s.goals) == 1

    def test_pop_goal_empty(self):
        s = TacticState()
        assert s.pop_goal() is None

    def test_state_repr(self):
        s = TacticState(goals=[Prop('p')], hypotheses={"H": Prop('q')})
        r = repr(s)
        assert "goals" in r
        assert "H" in r


class TestIntrosTactic:
    def test_intros_tactic_single(self):
        t = intros_tactic("H")
        assert t.name == "intros"
        assert t.args[0] == ["H"]

    def test_intros_tactic_list(self):
        t = intros_tactic(["H1", "H2"])
        assert t.args[0] == ["H1", "H2"]


class TestByContraTactic:
    def test_by_contra_tactic(self):
        p = Prop('p')
        t = by_contra_tactic("H", p)
        assert t.name == "by_contra"
        assert t.args[1] == p


class TestCasesTactic:
    def test_cases_tactic(self):
        p1, p2 = Prop('p1'), Prop('p2')
        t = cases_tactic("H", [p1, p2])
        assert t.name == "cases"
        assert len(t.args[1]) == 2


class TestInductionTactic:
    def test_induction_tactic(self):
        base = [intros("H")]
        ind = [intros("IH")]
        t = induction_tactic("n", base, ind)
        assert t.name == "induction"
        assert t.args[0] == "n"


class TestRewriteTactic:
    def test_rewrite_tactic(self):
        t = rewrite_tactic("eq_H")
        assert t.name == "rewrite"
        assert t.args[0] == "eq_H"

    def test_rewrite_tactic_sym(self):
        t = rewrite_tactic("eq_H", sym=True)
        assert t.args[1] is True


class TestSplitTactic:
    def test_split_tactic(self):
        t = split_tactic()
        assert t.name == "split"


class TestLeftRightTactic:
    def test_left_tactic(self):
        t = left_tactic()
        assert t.name == "left"

    def test_right_tactic(self):
        t = right_tactic()
        assert t.name == "right"


class TestUseTactic:
    def test_use_tactic(self):
        t = use_tactic("witness")
        assert t.name == "use"
        assert t.args[0] == "witness"


class TestShowTactic:
    def test_show_tactic(self):
        p = Prop('p')
        t = show_tactic(p)
        assert t.name == "show"
        assert t.args[0] == p


class TestByTactic:
    def test_by_tactic(self):
        tactics_list = [tactic_rfl()]
        t = by_tactic(tactics_list)
        assert t.name == "by"
        assert len(t.args[0]) == 1


class TestSorryTactic:
    def test_sorry_tactic(self):
        t = sorry_tactic()
        assert t.name == "sorry"


class TestCalcTactic:
    def test_calc_tactic(self):
        tactics_list = [tactic_rfl()]
        t = calc_tactic(tactics_list)
        assert t.name == "calc"
        assert len(t.args[0]) == 1


class TestIntroTactic:
    def test_intro_tactic(self):
        t = intro_tactic("H")
        assert t.name == "intro"
        assert t.args[0] == "H"


class TestApplyTactic:
    def test_apply_tactic(self):
        t = apply_tactic("H")
        assert t.name == "apply"
        assert t.args[0] == "H"
