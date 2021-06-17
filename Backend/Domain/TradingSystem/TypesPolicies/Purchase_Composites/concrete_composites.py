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
            res = self.can_add_clause(component._clause)
            if res.succeeded():
                return self.add_to_clause(component)
            else:
                return Response(False, msg=f"Can't add another rule with clause: {component._clause}")
        else:
            if self.children[0] is not None:
                response_test = self.children[0].add(component, parent_id)
                if response_test.succeeded():
                    return response_test
            elif self.children[1] is not None:
                return self.children[1].add(component, parent_id)

            else:
                return Response(False, msg=f"There is no exsiting parent with {parent_id}")

    def can_add_clause(self, clause):
        if len(self.children) == 0:
            return Response(True)

        elif len(self.children) == 1:
            if self.children[0]._clause != clause:
                return Response(True)

        if self.children[0] == None:
            if self.children[1]._clause != clause:
                return Response(True)
            else:
                return Response(False)
        if self.children[0]._clause == clause:
            return Response(False)
        if self.children[1] == None:
            return Response(True)
        return Response(False)

    def add_to_clause(self, component: PurchaseRule) -> Response[None]:
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler

        res_save = PurchaseRulesHandler.get_instance().save(component)
        if res_save.succeeded():
            res_commit = PurchaseRulesHandler.get_instance().commit_changes()
            if res_commit.succeeded():
                return Response(True, msg="Rule was added successfully!")
        else:
            return Response(False, msg="There is an existing if clause for the condition")

    def remove(self, component_id: str) -> Response[None]:
        from Backend.DataBase.database import db_fail_response
        from Backend.DataBase.Handlers.purchase_rules_handler import PurchaseRulesHandler
        if self.children[0] is not None:
            if self.children[0].get_id() == component_id:
                clause = self.children[0]._clause
                parent = self.children[0].parent
                res_remove = PurchaseRulesHandler.get_instance().remove_rule(self.children[0])
                if res_remove.succeeded():
                    and_rule = AndCompositePurchaseRule(parent)
                    and_rule.set_clause(clause)
                    res_save_and = self.add_to_clause(and_rule)
                    if res_save_and.succeeded():
                        return Response(True, msg="Rule was removed successfully!")
                return db_fail_response

        if self.children[1] is not None:
            if self.children[1].get_id() == component_id:
                clause = self.children[1]._clause
                parent = self.children[1].parent
                res_remove = PurchaseRulesHandler.get_instance().remove_rule(self.children[1])
                if res_remove.succeeded():
                    and_rule = AndCompositePurchaseRule(parent)
                    and_rule.set_clause(clause)
                    res_save_and = self.add_to_clause(and_rule)
                    if res_save_and.succeeded():
                        return Response(True, msg="Rule was removed successfully!")
                return db_fail_response

        return super().remove(component_id)

    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        test_clause = None
        then_clause = None
        if self.children[0]._clause == "test":
            test_clause = self.children[0]
            then_clause = self.children[1]
        else:
            then_clause = self.children[0]
            test_clause = self.children[1]
        if not test_clause.operation(products_to_quantities, user_age).succeeded():
            return Response(True, msg="Purchase is permitted!")
        return then_clause.operation(products_to_quantities, user_age)

    def parse(self):
        test_clause = None
        then_clause = None
        if self.children[0]._clause == "test":
            test_clause = self.children[0]
            then_clause = self.children[1]
        else:
            then_clause = self.children[0]
            test_clause = self.children[1]
        return {
            "id": self.get_id(),
            "operator": "conditional",
            "test": test_clause.parse()
            if test_clause is not None
            else None,
            "then": then_clause.parse()
            if then_clause is not None
            else None,
        }
