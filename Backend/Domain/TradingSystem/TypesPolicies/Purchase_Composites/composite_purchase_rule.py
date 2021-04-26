from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class PurchaseRule(ABC):
    """
    The base Component class declares common operations for both simple and
    complex objects of a composition.
    """

    @property
    def parent(self) -> PurchaseRule:
        return self._parent

    @parent.setter
    def parent(self, parent: PurchaseRule):
        """
        Optionally, the base Component can declare an interface for setting and
        accessing a parent of the component in a tree structure. It can also
        provide some default implementation for these methods.
        """

        self._parent = parent

    """
    In some cases, it would be beneficial to define the child-management
    operations right in the base Component class. This way, you won't need to
    expose any concrete component classes to the client code, even during the
    object tree assembly. The downside is that these methods will be empty for
    the leaf-level components.
    """

    def add(self, component: PurchaseRule) -> None:
        pass

    def remove(self, component: PurchaseRule) -> None:
        pass

    def is_composite(self) -> bool:
        """
        You can provide a method that lets the client code figure out whether a
        component can bear children.
        """

        return False

    @abstractmethod
    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        """
        The base Component may implement some default behavior or leave it to
        concrete classes (by declaring the method containing the behavior as
        "abstract").
        """

        pass


class PurchaseLeaf(PurchaseRule):
    """
    The Leaf class represents the end objects of a composition. A leaf can't
    have any children.

    Usually, it's the Leaf objects that do the actual work, whereas Composite
    objects only delegate to their sub-components.
    """

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        pass


class CompositePurchaseRule(PurchaseRule):
    """
    The Composite class represents the complex components that may have
    children. Usually, the Composite objects delegate the actual work to their
    children and then "sum-up" the result.
    """

    def __init__(self) -> None:
        self._children: List[PurchaseRule] = []

    """
    A composite object can add or remove other components (both simple or
    complex) to or from its child list.
    """

    @property
    def children(self):
        return self._children

    def add(self, component: PurchaseRule) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: PurchaseRule) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        """
        The Composite executes its primary logic in a particular way. It
        traverses recursively through all its children, collecting and summing
        their results. Since the composite's children pass these calls to their
        children and so forth, the whole object tree is traversed as a result.
        """

        pass