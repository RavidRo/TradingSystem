import json
import operator
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

    def __init__(self, leaf_details: dict, identifier: str):
        super().__init__(identifier)
        self._context = leaf_details['context']
        self._comparator = leaf_details['operator']
        self._constraint = leaf_details['target']

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        pass

    def edit_rule(self, rule_id: str, component: PurchaseRule):
        if self.id == rule_id:
            self.parent.children.remove(self)
            self.parent.children.append(component)
            return Response(True, msg="rule was edited successfully!")
        return Response(False, msg=f"rule couldn't be edited with id:{rule_id}")

    def add(self, component: PurchaseRule, parent_id: str, clause: str = None):
        return Response(False, msg="Rule can't be added as a leaf's child!")

    def remove(self, component_id: str) -> Response[None]:
        if self.id == component_id:
            self.parent.children.remove(self)
            self.parent = None
            return Response(True, msg="rule was removed successfully!")
        return Response(False, msg=f"rule couldn't be removed with id:{component_id}")

    def get_rule(self, rule_id):
        if self.id == rule_id:
            return Response(True, obj=self, msg="Here is the rule")
        else:
            return Response(False, msg=f"No rule with id: {rule_id}")

    def check_validity(self, new_parent_id: str) -> Response[None]:
        if self.id == new_parent_id:
            return Response(False, msg="Invalid move operation!")
        return Response(True, msg="Valid move")

    def parse(self):
        return {"id": self.id,
                "context": self._context,
                "operator": self._comparator,
                "target": self._constraint}
