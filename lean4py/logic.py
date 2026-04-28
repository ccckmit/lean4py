from typing import Optional

class Prop:
    """A propositional logic variable or compound formula.

    Propositions are equal by name (Prop('p') == Prop('p') is True),
    but are distinct objects (Prop('p') is Prop('p') is False).
    Always use == for equality checks, not 'is'.
    """
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Prop({self.name!r})"

    def __eq__(self, other):
        return isinstance(other, Prop) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __rshift__(self, other):
        return implies(self, other)

    def __and__(self, other):
        return and_(self, other)

    def __or__(self, other):
        return or_(self, other)

    def __invert__(self):
        return not_(self)


def Prop_var(name: str) -> Prop:
    """Create a propositional variable.

    Shorthand for Prop(name). e.g., p = Prop_var('p')
    """
    return Prop(name)


def implies(a: Prop, b: Prop) -> Prop:
    """Logical implication: a → b."""
    return _PropBinOp("→", a, b)


def and_(a: Prop, b: Prop) -> Prop:
    """Logical conjunction: a ∧ b."""
    return _PropBinOp("∧", a, b)


def or_(a: Prop, b: Prop) -> Prop:
    """Logical disjunction: a ∨ b."""
    return _PropBinOp("∨", a, b)


def not_(a: Prop) -> Prop:
    """Logical negation: ¬a."""
    return _PropUnOp("¬", a)


def iff(a: Prop, b: Prop) -> Prop:
    """Logical biconditional: a ↔ b (implemented as (a→b)∧(b→a))."""
    return and_(implies(a, b), implies(b, a))


class _PropBinOp(Prop):
    def __init__(self, op: str, left: Prop, right: Prop):
        super().__init__(f"({left.name} {op} {right.name})")
        self.op = op
        self.left = left
        self.right = right


class _PropUnOp(Prop):
    def __init__(self, op: str, operand: Prop):
        super().__init__(f"{op}{operand.name}")
        self.op = op
        self.operand = operand


class Theorem:
    """A named theorem with a proposition and optional proof steps."""
    def __init__(self, name: str, prop: Prop, proof: Optional[list] = None):
        self.name = name
        self.prop = prop
        self.proof = proof or []

    def __repr__(self):
        return f"Theorem({self.name!r}, {self.prop!r})"


class ProofStep:
    """A single step in a proof, identified by a tactic name and arguments."""
    def __init__(self, tactic: str, *args):
        self.tactic = tactic
        self.args = args

    def __repr__(self):
        return f"ProofStep({self.tactic!r}, {self.args})"


def assume(name: str, prop: Prop) -> ProofStep:
    """Assume a proposition with a given name in a proof."""
    return ProofStep("assume", name, prop)


def have(name: str, prop: Prop, from_: Optional[str] = None) -> ProofStep:
    """Introduce a new proposition that can be derived from existing assumptions."""
    return ProofStep("have", name, prop, from_)


def exact(prop: Prop) -> ProofStep:
    """Use an exact proposition to close a proof goal."""
    return ProofStep("exact", prop)


def apply(h: str) -> ProofStep:
    """Apply a hypothesis or theorem in a proof."""
    return ProofStep("apply", h)


def rfl() -> ProofStep:
    """Reflexivity tactic: prove a goal of the form x = x."""
    return ProofStep("rfl")


def simp() -> ProofStep:
    """Simplification tactic."""
    return ProofStep("simp")


def prove(prop: Prop, tactics: list) -> Theorem:
    """Create a theorem with a proposition and a list of proof tactics."""
    return Theorem(f"proved_{id(prop)}", prop, tactics)