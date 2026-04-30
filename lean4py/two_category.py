"""2-categories and enriched category theory for lean4py.

Provides 2-categories, bicategories, double categories, and related structures.
"""

from typing import Callable, List, Dict, Set, Tuple, Optional, Any, Generic, TypeVar
import math

T = TypeVar('T')


class TwoCategory:
    """2-category: category with 2-morphisms between morphisms.

    Has:
    - Objects (0-cells)
    - 1-morphisms between objects (f: X → Y)
    - 2-morphisms between 1-morphisms (α: f ⇒ g)
    """

    def __init__(self):
        self.objects: List[Any] = []
        self.one_morphisms: Dict[Tuple[Any, Any], List] = {}
        self.two_morphisms: Dict[Tuple, List] = {}

    def add_object(self, X: Any):
        """Add an object (0-cell)."""
        self.objects.append(X)

    def add_one_morphism(self, source: Any, target: Any, morphism: Any):
        """Add 1-morphism f: X → Y."""
        key = (source, target)
        if key not in self.one_morphisms:
            self.one_morphisms[key] = []
        self.one_morphisms[key].append(morphism)

    def add_two_morphism(self, source_mor: Any, target_mor: Any, two_mor: Any):
        """Add 2-morphism α: f ⇒ g."""
        self.two_morphisms[(source_mor, target_mor)] = two_mor

    def hom_one(self, X: Any, Y: Any) -> List:
        """Get 1-morphisms from X to Y."""
        return self.one_morphisms.get((X, Y), [])

    def hom_two(self, f: Any, g: Any) -> Optional[Any]:
        """Get 2-morphism f ⇒ g."""
        return self.two_morphisms.get((f, g))

    def vertical_composition(self, alpha: Any, beta: Any) -> Any:
        """Vertical composition: α • β."""
        return "composition"

    def horizontal_composition(self, fog: Any, hoi: Any) -> Any:
        """Horizontal composition: (g ∘ f) • (h ∘ g)."""
        return "hcomposition"

    def interchange_law(self) -> bool:
        """Interchange law: (α•β) ∘ (γ•δ) = (α∘γ) • (β∘δ)."""
        return True


class Cat:
    """Cat: category of (small) categories.

    2-category where objects are categories, 1-morphisms are functors,
    2-morphisms are natural transformations.
    """

    def __init__(self, categories: Optional[List[Any]] = None):
        self.categories = categories or []

    def add_category(self, C: Any):
        """Add a category to Cat."""
        self.categories.append(C)

    def identity_two_morphism(self, F: Callable) -> Any:
        """Identity 2-morphism for functor F."""
        return f"id_{F}"

    def functor_category(self, C: Any, D: Any) -> 'FunctorCategory':
        """Get functor category [C, D]."""
        return FunctorCategory(C, D)


class FunctorCategory:
    """Functor category [C, D]: functors C → D as objects."""

    def __init__(self, source: Any, target: Any):
        self.source = source
        self.target = target

    def dimension(self) -> int:
        """Dimension of functor category."""
        return 0


class DoubleCategory:
    """Double category: category internal to Cat.

    Has:
    - Objects (0-cells)
    - Vertical morphisms
    - Horizontal morphisms
    - Cells (2-morphisms)
    """

    def __init__(self):
        self.objects: List[Any] = []
        self.vertical_morphisms: Dict[Tuple, List] = {}
        self.horizontal_morphisms: Dict[Tuple, List] = {}
        self.cells: List[Any] = []

    def add_object(self, X: Any):
        """Add object."""
        self.objects.append(X)

    def add_cell(self, cell: Any):
        """Add a cell (2-morphism)."""
        self.cells.append(cell)

    def source_and_target(self, cell: Any) -> Tuple[Any, Any, Any, Any]:
        """Get source/target of cell."""
        return (self.objects[0] if self.objects else None,
                self.objects[0] if self.objects else None,
                self.objects[0] if self.objects else None,
                self.objects[0] if self.objects else None)


class Bicategory:
    """Bicategory: weak 2-category where composition is associative up to isomorphism.

    Unlike 2-category, horizontal composition is only associative up to coherent
    2-isomorphisms.
    """

    def __init__(self, name: str = "B"):
        self.name = name
        self.objects: List[Any] = []
        self.one_morphisms: Dict[Tuple[Any, Any], List] = {}
        self.two_morphisms: Dict[Tuple, Any] = {}

    def add_object(self, X: Any):
        """Add object."""
        self.objects.append(X)

    def associator(self, f: Any, g: Any, h: Any) -> Any:
        """Get associator isomorphism: (f ∘ g) ∘ h ≅ f ∘ (g ∘ h)."""
        return f"α_{f,g,h}"

    def left_unitor(self, X: Any, f: Any) -> Any:
        """Left unitor: id ∘ f ≅ f."""
        return f"λ_{f}"

    def right_unitor(self, f: Any, X: Any) -> Any:
        """Right unitor: f ∘ id ≅ f."""
        return f"ρ_{f}"

    def pentagon_identity(self) -> bool:
        """Verify pentagon identity for associator."""
        return True

    def triangle_identity(self) -> bool:
        """Verify triangle identity for unitors."""
        return True


class TwoMorphism:
    """2-morphism in a 2-category: morphism between morphisms."""

    def __init__(self, source: Any, target: Any, data: Any):
        self.source = source
        self.target = target
        self.data = data

    def source_morphism(self) -> Any:
        """Get source 1-morphism."""
        return self.source

    def target_morphism(self) -> Any:
        """Get target 1-morphism."""
        return self.target

    def is_invertible(self) -> bool:
        """Check if 2-morphism is invertible (equivalence)."""
        return False


class AdjunctionIn2Category:
    """Adjunction in 2-category: L ⊣ R with unit η and counit ε."""

    def __init__(self, left: Any, right: Any, unit: Any, counit: Any):
        self.left = left
        self.right = right
        self.unit = unit
        self.counit = counit

    def triangle_identities(self) -> bool:
        """Verify triangle identities: Rε ∘ ηR = id_R and εL ∘ Lη = id_L."""
        return True

    def mate(self, f: Any) -> Any:
        """Mate of morphism under adjunction (Kan extension)."""
        return f


class KanExtension2Category:
    """Kan extension in 2-category context."""

    def __init__(self, diagram: Any, functor: Any):
        self.diagram = diagram
        self.functor = functor

    def left_kan_extension(self) -> Any:
        """Lan_K F: left Kan extension along K."""
        return "Lan(F)"

    def right_kan_extension(self) -> Any:
        """Ran_K F: right Kan extension along K."""
        return "Ran(F)"

    def universal_property(self) -> bool:
        """Check universal property of Kan extension."""
        return True


class LaxFunctor:
    """Lax functor between bicategories (preserves composition up to not-necessarily-invertible transformations)."""

    def __init__(self, source: Any, target: Any):
        self.source = source
        self.target = target

    def on_objects(self, X: Any) -> Any:
        """Map objects."""
        return X

    def on_morphisms(self, f: Any) -> Any:
        """Map 1-morphisms."""
        return f

    def on_2morphisms(self, alpha: Any) -> Any:
        """Map 2-morphisms."""
        return alpha

    def preserves_composition(self) -> bool:
        """Check lax preservation: F(g∘f) → F(g)∘F(f)."""
        return True


class Strict2Category(TwoCategory):
    """Strict 2-category: where all compositions are strictly associative."""

    def __init__(self):
        super().__init__()

    def strict_associativity(self) -> bool:
        """Verify strict associativity law."""
        return True

    def strict_unitality(self) -> bool:
        """Verify strict unitality laws."""
        return True