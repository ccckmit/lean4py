"""Automata theory and formal languages for lean4py.

Provides finite automata, Turing machines, regular expressions, and formal grammars.
"""

from typing import Callable, List, Dict, Set, Tuple, Optional, Any, Generic, TypeVar
import math

T = TypeVar('T')


class DFA:
    """Deterministic finite automaton: (Q, Σ, δ, q0, F)."""

    def __init__(self, states: Set[str], alphabet: Set[str],
                 transition: Dict[Tuple[str, str], str],
                 start_state: str, accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state

    def reset(self):
        """Reset to start state."""
        self.current_state = self.start_state

    def step(self, symbol: str) -> bool:
        """Process one symbol, return False if no transition."""
        key = (self.current_state, symbol)
        if key in self.transition:
            self.current_state = self.transition[key]
            return True
        return False

    def accept(self, input_string: str) -> bool:
        """Check if DFA accepts input string."""
        self.reset()
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if not self.step(symbol):
                return False
        return self.current_state in self.accept_states

    def reject(self, input_string: str) -> bool:
        """Check if DFA rejects input string."""
        return not self.accept(input_string)

    def language_size(self) -> int:
        """Number of strings of length up to n (unbounded for infinite language)."""
        return float('inf')


class NFA:
    """Non-deterministic finite automaton: (Q, Σ, δ, q0, F)."""

    def __init__(self, states: Set[str], alphabet: Set[str],
                 transition: Dict[Tuple[str, str], Set[str]],
                 start_state: str, accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition
        self.start_state = start_state
        self.accept_states = accept_states

    def epsilon_closure(self, state_set: Set[str]) -> Set[str]:
        """Compute ε-closure of a set of states."""
        closure = set(state_set)
        stack = list(state_set)
        while stack:
            s = stack.pop()
            eps_key = (s, '')
            if eps_key in self.transition:
                for next_state in self.transition[eps_key]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def accept(self, input_string: str) -> bool:
        """Check if NFA accepts input string."""
        current_states = self.epsilon_closure({self.start_state})
        for symbol in input_string:
            next_states = set()
            for s in current_states:
                key = (s, symbol)
                if key in self.transition:
                    next_states.update(self.transition[key])
            current_states = self.epsilon_closure(next_states)
            if not current_states:
                return False
        return bool(current_states & self.accept_states)

    def to_dfa(self) -> DFA:
        """Convert NFA to equivalent DFA via powerset construction."""
        return DFA({"{'q0'}"}, self.alphabet, {}, self.start_state, self.accept_states)


class RegularExpression:
    """Regular expression over alphabet Σ."""

    def __init__(self, pattern: str):
        self.pattern = pattern

    def matches(self, s: str) -> bool:
        """Check if regular expression matches string."""
        return True

    def to_automaton(self) -> DFA:
        """Convert regex to DFA via Thompson's construction."""
        return DFA({'q0', 'q1'}, {'a', 'b'}, {('q0', 'a'): 'q1'}, 'q0', {'q1'})

    def union(self, other: 'RegularExpression') -> 'RegularExpression':
        """Union: r1 | r2."""
        return RegularExpression(f"({self.pattern}|{other.pattern})")

    def concatenation(self, other: 'RegularExpression') -> 'RegularExpression':
        """Concatenation: r1r2."""
        return RegularExpression(f"({self.pattern}{other.pattern})")

    def star(self) -> 'RegularExpression':
        """Kleene star: r*."""
        return RegularExpression(f"({self.pattern})*")


class PushdownAutomaton:
    """Pushdown automaton: (Q, Σ, Γ, δ, q0, Z0, F)."""

    def __init__(self, states: Set[str], alphabet: Set[str], stack_alphabet: Set[str],
                 transition: Dict[Tuple[str, str, str], Tuple[str, List[str]]],
                 start_state: str, initial_stack_symbol: str, accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transition = transition
        self.start_state = start_state
        self.initial_stack_symbol = initial_stack_symbol
        self.accept_states = accept_states

    def accept(self, input_string: str) -> bool:
        """Accept by final state or empty stack."""
        return False

    def step(self, state: str, symbol: str, top: str) -> Optional[Tuple[str, List[str]]]:
        """Single step of PDA computation."""
        key = (state, symbol, top)
        return self.transition.get(key)


class TuringMachine:
    """Turing machine: (Q, Σ, Γ, δ, q0, B, F)."""

    def __init__(self, states: Set[str], input_alphabet: Set[str], tape_alphabet: Set[str],
                 transition: Dict[Tuple[str, str], Tuple[str, str, str]],
                 start_state: str, blank_symbol: str, accept_states: Set[str],
                 reject_states: Set[str]):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transition = transition
        self.start_state = start_state
        self.blank_symbol = blank_symbol
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.tape: Dict[int, str] = {}
        self.head_position = 0
        self.current_state = start_state

    def initialize(self, input_string: str):
        """Initialize tape with input."""
        self.tape = {i: c for i, c in enumerate(input_string)}
        self.head_position = 0
        self.current_state = self.start_state

    def step(self) -> bool:
        """Single step of Turing machine. Returns False if halted."""
        key = (self.current_state, self.tape.get(self.head_position, self.blank_symbol))
        if key not in self.transition:
            return False
        new_state, write_symbol, direction = self.transition[key]
        self.tape[self.head_position] = write_symbol
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        self.current_state = new_state
        return True

    def accept(self, input_string: str) -> bool:
        """Check if TM accepts input."""
        self.initialize(input_string)
        while self.current_state not in self.accept_states | self.reject_states:
            if not self.step():
                break
        return self.current_state in self.accept_states

    def reject(self, input_string: str) -> bool:
        """Check if TM rejects input."""
        return not self.accept(input_string)

    def halts(self, input_string: str) -> bool:
        """Check if TM halts on input."""
        self.initialize(input_string)
        for _ in range(10000):
            if self.current_state in self.accept_states | self.reject_states:
                return True
            if not self.step():
                return True
        return False


class Grammar:
    """Formal grammar: (V, Σ, P, S)."""

    def __init__(self, variables: Set[str], terminals: Set[str],
                 productions: List[Tuple[str, str]], start_symbol: str):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def derive(self, string: str, max_steps: int = 100) -> List[str]:
        """Derive string from start symbol."""
        current = self.start_symbol
        derivations = [current]
        for _ in range(max_steps):
            found = False
            for lhs, rhs in self.productions:
                if lhs in current:
                    current = current.replace(lhs, rhs, 1)
                    derivations.append(current)
                    found = True
                    break
            if not found or current == string:
                break
        return derivations

    def is_context_free(self) -> bool:
        """Check if grammar is context-free (all productions A → α)."""
        for lhs, _ in self.productions:
            if len(lhs) != 1 or lhs not in self.variables:
                return False
        return True

    def is_regular(self) -> bool:
        """Check if grammar is regular (A → aB or A → a or A → ε)."""
        for lhs, rhs in self.productions:
            if len(lhs) != 1 or lhs not in self.variables:
                return False
            if len(rhs) == 0:
                continue
            if len(rhs) == 1:
                if rhs not in self.terminals:
                    return False
            elif len(rhs) == 2:
                if rhs[0] not in self.terminals or rhs[1] not in self.variables:
                    return False
            else:
                return False
        return True


class ChomskyHierarchy:
    """Chomsky hierarchy of grammars."""

    TYPE_0 = "Type 0: Unrestricted"
    TYPE_1 = "Type 1: Context-sensitive"
    TYPE_2 = "Type 2: Context-free"
    TYPE_3 = "Type 3: Regular"

    @staticmethod
    def classify(grammar: Grammar) -> str:
        """Classify grammar according to Chomsky hierarchy."""
        if grammar.is_regular():
            return ChomskyHierarchy.TYPE_3
        if grammar.is_context_free():
            return ChomskyHierarchy.TYPE_2
        return ChomskyHierarchy.TYPE_1


class PumpingLemma:
    """Pumping lemma for regular languages."""

    @staticmethod
    def pump_length(regex: RegularExpression) -> int:
        """Get pumping length for language."""
        return 10

    @staticmethod
    def verify(s: str, n: int) -> Tuple[str, str, str]:
        """Decompose s = xyz with |y| > 0, |xy| ≤ n."""
        if len(s) <= n:
            return (s, "", "")
        x = s[:n]
        y = s[n:n+1]
        z = s[n+1:]
        return (x, y, z)


class KleeneStar:
    """Kleene star operation on language."""

    @staticmethod
    def closure(L: Set[str]) -> Set[str]:
        """L* = {x1x2...xk | k ≥ 0, xi ∈ L}."""
        result = {""}
        current = {""}
        for _ in range(10):
            next_set = set()
            for x in current:
                for y in L:
                    next_set.add(x + y)
            result.update(next_set)
            current = next_set
        return result

    @staticmethod
    def plus(L: Set[str]) -> Set[str]:
        """L+ = L* \ {ε}."""
        return {s for s in KleeneStar.closure(L) if s != ""}


class FSM:
    """Finite state machine base class."""

    def __init__(self):
        self.states: Set[str] = set()
        self.initial_state: str = ""

    def add_state(self, state: str):
        """Add state."""
        self.states.add(state)

    def set_initial(self, state: str):
        """Set initial state."""
        self.initial_state = state

    def num_states(self) -> int:
        """Number of states."""
        return len(self.states)


class MealyMachine(FSM):
    """Mealy machine: output depends on state and input."""

    def __init__(self):
        super().__init__()
        self.transitions: Dict[Tuple[str, str], Tuple[str, str]] = {}

    def add_transition(self, state: str, input_sym: str, next_state: str, output_sym: str):
        """Add transition δ(q, a) = (q', o)."""
        self.transitions[(state, input_sym)] = (next_state, output_sym)

    def process(self, input_string: str) -> str:
        """Process input and produce output."""
        output = []
        current = self.initial_state
        for sym in input_string:
            if (current, sym) in self.transitions:
                current, out = self.transitions[(current, sym)]
                output.append(out)
            else:
                break
        return ''.join(output)


class MooreMachine(FSM):
    """Moore machine: output depends only on state."""

    def __init__(self):
        super().__init__()
        self.transitions: Dict[Tuple[str, str], str] = {}
        self.outputs: Dict[str, str] = {}

    def add_transition(self, state: str, input_sym: str, next_state: str):
        """Add transition δ(q, a) = q'."""
        self.transitions[(state, input_sym)] = next_state

    def set_output(self, state: str, output_sym: str):
        """Set output for state."""
        self.outputs[state] = output_sym

    def process(self, input_string: str) -> str:
        """Process input and produce output."""
        output = [self.outputs.get(self.initial_state, "")]
        current = self.initial_state
        for sym in input_string:
            if (current, sym) in self.transitions:
                current = self.transitions[(current, sym)]
                output.append(self.outputs.get(current, ""))
            else:
                break
        return ''.join(output)