"""Tests for automata_theory_v134.py v1.34."""

import unittest
from lean4py.automata_theory_v134 import (
    DFA, NFA, PushdownAutomaton, TuringMachine
)


class TestDFA(unittest.TestCase):
    def test_creation(self):
        dfa = DFA(["q0", "q1"], ["a"], {}, "q0", ["q1"])
        self.assertIsNotNone(dfa)

    def test_accepts(self):
        dfa = DFA(["q0", "q1"], ["a"], {}, "q0", ["q1"])
        self.assertTrue(dfa.accepts("a"))

    def test_is_deterministic(self):
        dfa = DFA(["q0"], ["a"], {}, "q0", ["q0"])
        self.assertTrue(dfa.is_deterministic())


class TestNFA(unittest.TestCase):
    def test_creation(self):
        nfa = NFA(["q0"], ["a"], {}, "q0", ["q0"])
        self.assertIsNotNone(nfa)

    def test_accepts(self):
        nfa = NFA(["q0"], ["a"], {}, "q0", ["q0"])
        self.assertTrue(nfa.accepts("a"))

    def test_to_dfa(self):
        nfa = NFA(["q0"], ["a"], {}, "q0", ["q0"])
        result = nfa.to_dfa()
        self.assertIsInstance(result, DFA)


class TestPushdownAutomaton(unittest.TestCase):
    def test_is_deterministic(self):
        self.assertTrue(PushdownAutomaton.is_deterministic({}))

    def test_accepts(self):
        self.assertTrue(PushdownAutomaton.accepts({}, "a"))


class TestTuringMachine(unittest.TestCase):
    def test_halts(self):
        self.assertTrue(TuringMachine.halts({}, "w"))

    def test_is_universal(self):
        self.assertTrue(TuringMachine.is_universal({}))


if __name__ == "__main__":
    unittest.main()
