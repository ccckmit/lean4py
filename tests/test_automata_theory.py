"""Tests for automata_theory module (v1.20)."""
import pytest
from lean4py.automata_theory import (
    DFA, NFA, RegularExpression, PushdownAutomaton, TuringMachine,
    Grammar, ChomskyHierarchy, PumpingLemma, KleeneStar,
    MealyMachine, MooreMachine, FSM
)


class TestDFA:
    def test_creation(self):
        dfa = DFA({'q0', 'q1'}, {'0', '1'}, {('q0', '0'): 'q0', ('q0', '1'): 'q1'}, 'q0', {'q1'})
        assert 'q0' in dfa.states

    def test_reset(self):
        dfa = DFA({'q0', 'q1'}, {'0', '1'}, {}, 'q0', {'q1'})
        dfa.current_state = 'q1'
        dfa.reset()
        assert dfa.current_state == 'q0'

    def test_step(self):
        dfa = DFA({'q0', 'q1'}, {'0', '1'}, {('q0', '0'): 'q0', ('q0', '1'): 'q1'}, 'q0', {'q1'})
        result = dfa.step('1')
        assert result is True
        assert dfa.current_state == 'q1'

    def test_step_no_transition(self):
        dfa = DFA({'q0'}, {'0'}, {}, 'q0', {'q0'})
        result = dfa.step('1')
        assert result is False

    def test_accept(self):
        dfa = DFA({'q0', 'q1'}, {'0', '1'}, {('q0', '0'): 'q0', ('q0', '1'): 'q1'}, 'q0', {'q1'})
        assert dfa.accept('1') is True
        assert dfa.accept('0') is False

    def test_reject(self):
        dfa = DFA({'q0', 'q1'}, {'0', '1'}, {}, 'q0', {'q1'})
        assert dfa.reject('0') is True


class TestNFA:
    def test_creation(self):
        nfa = NFA({'q0', 'q1'}, {'a', 'b'}, {('q0', 'a'): {'q1'}}, 'q0', {'q1'})
        assert 'q0' in nfa.states

    def test_accept(self):
        nfa = NFA({'q0', 'q1'}, {'a'}, {('q0', 'a'): {'q1'}}, 'q0', {'q1'})
        assert nfa.accept('a') is True
        assert nfa.accept('b') is False

    def test_to_dfa(self):
        nfa = NFA({'q0'}, {'a'}, {}, 'q0', {'q0'})
        dfa = nfa.to_dfa()
        assert isinstance(dfa, DFA)


class TestRegularExpression:
    def test_creation(self):
        re = RegularExpression("a*b")
        assert re.pattern == "a*b"

    def test_matches(self):
        re = RegularExpression("ab")
        assert re.matches("ab") is True

    def test_to_automaton(self):
        re = RegularExpression("a")
        dfa = re.to_automaton()
        assert isinstance(dfa, DFA)

    def test_union(self):
        re1 = RegularExpression("a")
        re2 = RegularExpression("b")
        result = re1.union(re2)
        assert "|" in result.pattern

    def test_star(self):
        re = RegularExpression("a")
        result = re.star()
        assert "*" in result.pattern


class TestPushdownAutomaton:
    def test_creation(self):
        pda = PushdownAutomaton(
            {'q0', 'q1'}, {'a', 'b'}, {'Z0'},
            {}, 'q0', 'Z0', {'q1'}
        )
        assert 'q0' in pda.states

    def test_step(self):
        pda = PushdownAutomaton(
            {'q0', 'q1'}, {'a', 'b'}, {'Z0'},
            {}, 'q0', 'Z0', {'q1'}
        )
        result = pda.step('q0', 'a', 'Z0')
        assert result is None


class TestTuringMachine:
    def test_creation(self):
        tm = TuringMachine(
            {'q0', 'qaccept', 'qreject'}, {'0', '1'}, {'0', '1', 'B'},
            {}, 'q0', 'B', {'qaccept'}, {'qreject'}
        )
        assert 'q0' in tm.states

    def test_initialize(self):
        tm = TuringMachine(
            {'q0'}, {'a'}, {'a', 'B'}, {}, 'q0', 'B', set(), set()
        )
        tm.initialize('aaa')
        assert tm.head_position == 0
        assert tm.current_state == 'q0'

    def test_accept(self):
        tm = TuringMachine(
            {'q0', 'q1', 'qaccept', 'qreject'}, {'a'}, {'a', 'B'},
            {('q0', 'a'): ('q1', 'a', 'R')}, 'q0', 'B', {'qaccept'}, {'qreject'}
        )
        assert tm.accept('a') is False

    def test_halts(self):
        tm = TuringMachine(
            {'q0'}, {'a'}, {'a', 'B'}, {}, 'q0', 'B', set(), set()
        )
        assert tm.halts('') is True


class TestGrammar:
    def test_creation(self):
        g = Grammar({'S'}, {'a', 'b'}, [('S', 'aS'), ('S', 'b')], 'S')
        assert 'S' in g.variables

    def test_derive(self):
        g = Grammar({'S'}, {'a', 'b'}, [('S', 'b'), ('S', 'aS')], 'S')
        result = g.derive('b', max_steps=5)
        assert 'b' in result

    def test_is_context_free(self):
        g = Grammar({'S'}, {'a', 'b'}, [('S', 'aSbS'), ('S', '')], 'S')
        assert g.is_context_free() is True

    def test_is_regular(self):
        g = Grammar({'S', 'A'}, {'a', 'b'}, [('S', 'aS'), ('S', 'bA'), ('A', '')], 'S')
        assert g.is_regular() is True


class TestChomskyHierarchy:
    def test_classify_regular(self):
        g = Grammar({'S'}, {'a'}, [('S', 'aS'), ('S', '')], 'S')
        result = ChomskyHierarchy.classify(g)
        assert result == ChomskyHierarchy.TYPE_3

    def test_classify_context_free(self):
        g = Grammar({'S'}, {'a', 'b'}, [('S', 'aSbS'), ('S', '')], 'S')
        result = ChomskyHierarchy.classify(g)
        assert result == ChomskyHierarchy.TYPE_2


class TestPumpingLemma:
    def test_pump_length(self):
        re = RegularExpression("a*b")
        n = PumpingLemma.pump_length(re)
        assert n == 10

    def test_verify(self):
        result = PumpingLemma.verify("abcde", 3)
        assert len(result) == 3


class TestKleeneStar:
    def test_closure(self):
        L = {"a", "b"}
        result = KleeneStar.closure(L)
        assert "" in result
        assert "a" in result

    def test_plus(self):
        L = {"a"}
        result = KleeneStar.plus(L)
        assert "" not in result
        assert "a" in result


class TestFSM:
    def test_creation(self):
        fsm = FSM()
        assert fsm.states == set()

    def test_add_state(self):
        fsm = FSM()
        fsm.add_state('q0')
        assert 'q0' in fsm.states

    def test_set_initial(self):
        fsm = FSM()
        fsm.add_state('q0')
        fsm.set_initial('q0')
        assert fsm.initial_state == 'q0'

    def test_num_states(self):
        fsm = FSM()
        fsm.add_state('q0')
        fsm.add_state('q1')
        assert fsm.num_states() == 2


class TestMealyMachine:
    def test_creation(self):
        mm = MealyMachine()
        assert mm.states == set()

    def test_add_transition(self):
        mm = MealyMachine()
        mm.add_state('q0')
        mm.add_transition('q0', '0', 'q1', '1')
        assert ('q0', '0') in mm.transitions

    def test_process(self):
        mm = MealyMachine()
        mm.add_state('q0')
        mm.add_state('q1')
        mm.set_initial('q0')
        mm.add_transition('q0', '0', 'q1', '1')
        result = mm.process('0')
        assert result == '1'


class TestMooreMachine:
    def test_creation(self):
        mm = MooreMachine()
        assert mm.states == set()

    def test_add_transition(self):
        mm = MooreMachine()
        mm.add_state('q0')
        mm.add_transition('q0', '0', 'q1')
        assert ('q0', '0') in mm.transitions

    def test_set_output(self):
        mm = MooreMachine()
        mm.add_state('q0')
        mm.set_output('q0', '1')
        assert mm.outputs['q0'] == '1'

    def test_process(self):
        mm = MooreMachine()
        mm.add_state('q0')
        mm.add_state('q1')
        mm.set_initial('q0')
        mm.add_transition('q0', '0', 'q1')
        mm.set_output('q0', '0')
        mm.set_output('q1', '1')
        result = mm.process('0')
        assert result == '01'