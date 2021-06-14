from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import (
    CompositePurchaseRule,
    PurchaseRule,
)
from Backend.response import Response


class OrCompositePurchaseRule(CompositePurchaseRule):
    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        if len(self.children) == 0:
            return Response(True, msg="Purchase is permitted!")

        for child in self.children:
            if child.operation(products_to_quantities, user_age).succeeded():
                return Response(True, msg="Purchase is permitted!")
        return Response(False, msg="Purchase doesn't stand with the rules!")

    def parse(self):
        return {
            "id": self.get_id(),
            "operator": "or",
            "children": [child.parse() for child in self.children],
        }


class AndCompositePurchaseRule(CompositePurchaseRule):
    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        for child in self.children:
            if not child.operation(products_to_quantities, user_age).succeeded():
                return Response(False, msg="Purchase doesn't stand with the rules!")
        return Response(True, msg="Purchase is permitted!")

    def parse(self):
        return {
            "id": self.get_id(),
            "operator": "and",
            "children": [child.parse() for child in self.children],
        }


class ConditioningCompositePurchaseRule(CompositePurchaseRule):
    def __init__(self, parent):
        super(ConditioningCompositePurchaseRule, self).__init__(parent)

    def add(self, component: PurchaseRule, parent_id: str) -> Response[None]:
        if self.get_id() == parent_id:
            return self.add_to_clause(component)

        else:
            if self.children[0] is not None:
                response_test = self.children[0].add(component, parent_id)
                if response_test.succeeded():
                    return response_test
            elif self.children[1] is not None:
                return self.children[1].add(component, parent_id)

            else:
                return Response(False, msg=f"There is no exsiting parent with {parent_id}")

    # def can_add_clause(self, clause):
    #     if self.children[0] is None and (self.children[1] is None or self.children[1]._clause != clause):
    #         return Response(True, obj=0)
    #     if self.children[1] is None and (self.children[0] is None or self.children[0]._clause!= clause):
    #         return Response(True, obj=1)
    #     return Response(False)

    def add_to_clause(self, component: PurchaseRule) -> Response[None]:
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler

        res = self.can_add_clause(component._clause)
        if res.succeeded():
            res_save = PurchaseRulesHandler.get_instance().save(component)
            if res_save.succeeded():
                res_commit = PurchaseRulesHandler.get_instance().commit_changes()
                if res_commit.succeeded():
                    return Response(True, msg="Rule was added successfully!")
        else:
            return Response(False, msg="There is an existing if clause for the condition")

    def remove(self, component_id: str) -> Response[None]:
        if self.children[0] is not None:
            if self.children[0].get_id() == component_id:
                self.children[0] = AndCompositePurchaseRule()
                return Response(True, msg="Rule was removed successfully!")

        if self.children[1] is not None:
            if self.children[1].get_id() == component_id:
                self.children[1] = AndCompositePurchaseRule()
                return Response(True, msg="Rule was removed successfully!")

        return super().remove(component_id)

    # def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
    #     test_clause = self.children[0]
    #     if (
    #         not self.children[clauses["test"]]
    #         .operation(products_to_quantities, user_age)
    #         .succeeded()
    #     ):
    #         return Response(True, msg="Purchase is permitted!")
    #     return self.children[clauses["then"]].operation(products_to_quantities, user_age)
    #
    # def parse(self):
    #     return {
    #         "id": self.get_id(),
    #         "operator": "conditional",
    #         "test": self.children[clauses["test"]].parse()
    #         if self.children[clauses["test"]] is not None
    #         else None,
    #         "then": self.children[clauses["then"]].parse()
    #         if self.children[clauses["then"]] is not None
    #         else None,
    #     }
