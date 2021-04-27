from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import CompositePurchaseRule, PurchaseRule


class OrCompositePurchaseRule(CompositePurchaseRule):

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        for child in self.children:
            if child.operation(products_to_quantities, user_age):
                return True
        return False


class AndCompositePurchaseRule(CompositePurchaseRule):

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        for child in self.children:
            if not child.operation(products_to_quantities, user_age):
                return False
        return True


class ConditioningCompositePurchaseRule(CompositePurchaseRule):
    def __init__(self, identifier: str):
        super().__init__(identifier)
        self._if_clause: PurchaseRule = True
        self._then_clause: PurchaseRule = True

    def add_if_clause(self, if_component: PurchaseRule):
        self._if_clause = if_component

    def add_then_clause(self, then_component: PurchaseRule):
        self._then_clause = then_component

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        if not self._if_clause.operation(products_to_quantities, user_age):
            return True
        return self._then_clause.operation(products_to_quantities,user_age)