from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import List
from sqlalchemy_utils import Ltree
from Backend.DataBase.database import engine, db_fail_response
from Backend.response import Response


class PurchaseRule(ABC):
    """
    The base Component class declares common operations for both simple and
    complex objects of a composition.
    """

    def __init__(self, parent=None):
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        from Backend.DataBase.Handlers.purchase_rules_handler import rules_id_seq
        _id = engine.execute(rules_id_seq)
        self._id = _id
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id
        self._clause = None

    def get_id(self):
        return str(self._id)

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

    def set_clause(self, clause_str):
        self._clause = clause_str

    def add(self, component: PurchaseRule, parent_id: str) -> Response[None]:
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
    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        pass

    def parse(self):
        pass


class CompositePurchaseRule(PurchaseRule):
    """
    The Composite class represents the complex components that may have
    children. Usually, the Composite objects delegate the actual work to their
    children.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._children: List[PurchaseRule] = []

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def children_operation(self, func: callable, id: str, component: PurchaseRule = None, clause: str = None) -> Response[None]:
        for child in self._children:
            if child is not None:
                if component is None:
                    response = func(child, id)
                else:
                    if clause is None:
                        response = func(child, component, id)
                    else:
                        response = func(child, component, id, clause)
                if response.succeeded():
                    return response
        return Response(False, msg=f"Operation couldn't be performed! Wrong parent_id: {id}")

    def add(self, component: PurchaseRule, parent_id: str) -> Response[None]:
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        if self.get_id() == parent_id:
            res_save = PurchaseRulesHandler.get_instance().save(component)
            if res_save.succeeded():
                res_commit = PurchaseRulesHandler.get_instance().commit_changes()
                if res_commit.succeeded():
                    return Response(True, msg="Rule was added successfully!")
        if self.is_composite():
            return self.children_operation(lambda child, rule, relevant_id: child.add(rule, relevant_id), parent_id, component)
        else:
            return Response(False, msg=f"Operation couldn't be performed! Wrong parent_id: {id}")

    def remove(self, component_id: str) -> Response[None]:
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        if self.get_id() == component_id:
            if self.parent is None:
                return Response(False, msg="Root can't be removed!")
            res_remove = PurchaseRulesHandler.get_instance().remove_rule(self)
            if res_remove.succeeded():
                res_commit = PurchaseRulesHandler.get_instance().commit_changes()
                if res_commit.succeeded():
                    return Response(True, msg="Rule was removed successfully!")
                else:
                    return db_fail_response
            else:
                return res_remove
        return self.children_operation(lambda next_child, relevant_id: next_child.remove(relevant_id), component_id)

    def edit_rule(self, rule_id: str, component: PurchaseRule) -> Response[None]:
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        if str(self.get_id()) == rule_id:
            res_edit = PurchaseRulesHandler.get_instance().edit_rule(self, component)
            if res_edit.succeeded():
                res_commit = PurchaseRulesHandler.get_instance().commit_changes()
                if res_commit.succeeded():
                    return Response(True, msg="rule was edited successfully!")
                return db_fail_response
            return res_edit
        return self.children_operation(lambda child, relevant_id, rule: child.edit_rule(rule, relevant_id), rule_id, component)

    def get_rule(self, rule_id: str) -> Response[PurchaseRule]:
        if str(self.get_id()) == rule_id:
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
        if str(self.get_id()) == new_parent_id:
            return Response(False, msg="Invalid move operation!")
        for child in self.children:
            response = child.check_validity(new_parent_id)
            if not response.succeeded():
                return response
        return Response(True, msg="Valid move")

    def parse(self):
        pass

    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        pass
