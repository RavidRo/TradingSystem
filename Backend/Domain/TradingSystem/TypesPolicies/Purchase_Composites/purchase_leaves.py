import json
import operator

from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseRule
from Backend.Domain.TradingSystem.user import User
from Backend.response import Response


class PurchaseLeaf(PurchaseRule):
    """leaf_details is a json of the format
        {context:
        {object: _
         object_identifier: _
         }
         comparator: _
         constraint: _
         }"""

    def __init__(self, leaf_details: dict, parent=None):
        super().__init__(parent)
        self._context_obj = leaf_details['context']['obj']
        self._context_id = leaf_details['context'].get('identifier')
        self._comparator = leaf_details['operator']
        self._constraint = leaf_details['target']

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        pass

    def edit_rule(self, rule_id: str, component: PurchaseRule):
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        if self.get_id() == rule_id:
            old_rule_clause = self._clause
            component.set_clause(old_rule_clause)
            res_remove = PurchaseRulesHandler.get_instance().remove_rule(self)
            if res_remove.succeeded():
                res_save = PurchaseRulesHandler.get_instance().save(component)
                if res_save.succeeded():
                    res_commit = PurchaseRulesHandler.get_instance().commit_changes()
                    if res_commit.succeeded():
                        return Response(True, msg="rule was edited successfully!")
                    return res_commit
                return res_save
            return res_remove
        return Response(False, msg=f"rule couldn't be edited with id:{rule_id}")

    def add(self, component: PurchaseRule, parent_id: str, clause: str = None):
        return Response(False, msg="Rule can't be added as a leaf's child!")

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
        return Response(False, msg=f"rule couldn't be removed with id:{component_id}")

    def get_rule(self, rule_id):
        if self.get_id() == rule_id:
            return Response(True, obj=self, msg="Here is the rule")
        else:
            return Response(False, msg=f"No rule with id: {rule_id}")

    def check_validity(self, new_parent_id: str) -> Response[None]:
        if self.get_id() == new_parent_id:
            return Response(False, msg="Invalid move operation!")
        return Response(True, msg="Valid move")

    def parse(self):
        return {"id": self.get_id(),
                "context": {"obj": self._context_obj, "identifier": self._context_id},
                "operator": self._comparator,
                "target": self._constraint}
