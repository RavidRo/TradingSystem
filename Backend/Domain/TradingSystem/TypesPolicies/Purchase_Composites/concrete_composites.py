from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import \
    CompositePurchaseRule, PurchaseRule
from Backend.Domain.TradingSystem.user import User
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
        return {"id": self.id,
                "operator": "or",
                "children":
                    [child.parse() for child in self.children]}


class AndCompositePurchaseRule(CompositePurchaseRule):

    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        for child in self.children:
            if not child.operation(products_to_quantities, user_age).succeeded():
                return Response(False, msg="Purchase doesn't stand with the rules!")
        return Response(True, msg="Purchase is permitted!")

    def parse(self):
        return {"id": self.id,
                "operator": "and",
                "children":
                    [child.parse() for child in self.children]}


clauses = {'test': 0,
           'then': 1}


class ConditioningCompositePurchaseRule(CompositePurchaseRule):
    def __init__(self, identifier: str):
        super(ConditioningCompositePurchaseRule, self).__init__(identifier)
        self.children = [None, None]

    def add(self, component: PurchaseRule, parent_id: str, clause: str = None) -> Response[None]:
        if self.id == parent_id:
            if clause == 'test':
                return self.add_to_clause(clauses['test'], component)
            elif clause == 'then':
                return self.add_to_clause(clauses['then'], component)
            else:
                return Response(False, msg="There is an existing if clause for the condition")

        else:
            if self.children[0] is not None:
                response_test = self.children[0].add(component, parent_id, clause)
                if response_test.succeeded():
                    return response_test
            elif self.children[1] is not None:
                return self.children[1].add(component, parent_id, clause)

            else:
                return Response(False, msg=f"There is no exsiting parent with {parent_id}")


    def add_to_clause(self, index_of_clause: int, component: PurchaseRule) -> Response[None]:
        if self.children[index_of_clause] is None:
            self.children[index_of_clause] = component
            component.parent = self
            return Response(True, msg="Rule was added successfully!")
        else:
            return Response(False, msg="There is an existing if clause for the condition")

    def remove(self, component_id: str) -> Response[None]:
        if self.children[0] is not None:
            if self.children[0].id == component_id:
                self.children[0] = AndCompositePurchaseRule(self.children[0].id)
                return Response(True, msg="Rule was removed successfully!")

        if self.children[1] is not None:
            if self.children[1].id == component_id:
                self.children[1] = AndCompositePurchaseRule(self.children[1].id)
                return Response(True, msg="Rule was removed successfully!")

        return super().remove(component_id)

    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        if not self.children[clauses['test']].operation(products_to_quantities, user_age).succeeded():
            return Response(True, msg="Purchase is permitted!")
        return self.children[clauses['then']].operation(products_to_quantities, user_age)

    def parse(self):
        return {"id": self.id,
                "operator": "conditional",
                "test": self.children[clauses['test']].parse() if self.children[clauses['test']] is not None else None,
                "then": self.children[clauses['then']].parse()} if self.children[clauses['then']] is not None else None
