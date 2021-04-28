from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import List

from Backend.response import Response


class PurchaseRule(ABC):
    """
    The base Component class declares common operations for both simple and
    complex objects of a composition.
    """

    @property
    def id(self) -> str:
        return self._id

    @property
    def parent(self) -> CompositePurchaseRule:
        return self._parent

    @id.setter
    def id(self, id: str):
        self._id = id

    @parent.setter
    def parent(self, parent: CompositePurchaseRule):
        self._parent = parent

    def add(self, component: PurchaseRule, parent_id: str, clause: str = None) -> Response[None]:
        pass

    def remove(self, component_id: str) -> Response[None]:
        pass

    def get_rule(self, rule_id: str) -> Response[PurchaseRule]:
        pass

    def check_validity(self, new_parent_id: str) -> Response[None]:
        pass

    def edit_rule(self, rule_id: str, component: PurchaseRule) -> Response[None]:
        pass

    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        pass


class CompositePurchaseRule(PurchaseRule):
    """
    The Composite class represents the complex components that may have
    children. Usually, the Composite objects delegate the actual work to their
    children.
    """

    def __init__(self, identifier: str) -> None:
        self.id = identifier
        self._children: List[PurchaseRule] = []

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def children_operation(self, func: callable, id: str, component: PurchaseRule = None) -> Response[None]:
        for child in self._children:
            if child.is_composite():
                if component is None:
                    response = func(child, id)
                else:
                    response = func(child, component, id)
                if response.succeeded():
                    return response
        return Response(False, msg=f"Operation couldn't be performed! Wrong parent_id: {id}")

    def add(self, component: PurchaseRule, parent_id: str, clause: str = None) -> Response[None]:
        if self.id == parent_id:
            self._children.append(component)
            component.parent = self
            return Response(True, msg="Rule was added successfully!")

        return self.children_operation(lambda child, rule, relevant_id: child.add(rule, relevant_id), parent_id, component)

    def remove(self, component_id: str) -> Response[None]:
        if self.id == component_id:
            self.parent._children.remove(self)
            self.parent = None
            return Response(True, msg="Rule was removed successfully!")

        return self.children_operation(lambda next_child, relevant_id: next_child.remove(relevant_id), component_id)

    def edit_rule(self, rule_id: str, component: PurchaseRule) -> Response[None]:
        if self.id == rule_id:
            self.parent.children.remove(self)
            self.parent.children.append(component)
            component.parent = self.parent
            self.parent = None
            component.children = copy.deepcopy(self.children)
            return Response(True, msg="rule was edited successfully!")

        return self.children_operation(lambda child, rule, relevant_id: child.edit_rule(rule, relevant_id), rule_id, component)

    def get_rule(self, rule_id: str) -> Response[PurchaseRule]:
        if self.id == rule_id:
            return Response(True, obj=self, msg="Here is the rule")
        else:
            for child in self.children:
                response = child.get_rule(rule_id)
                if response.succeeded():
                    return response
            return Response(False, msg=f"No rule with id: {rule_id}")

    def is_composite(self) -> bool:
        return True

    def check_validity(self, new_parent_id: str) -> Response[None]:
        if self.id == new_parent_id:
            return Response(False, msg="Invalid move operation!")
        for child in self.children:
            response = child.check_validity(new_parent_id)
            if not response.succeeded():
                return response
        return Response(True, msg="Valid move")

    def parse(self):
        pass

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        pass
