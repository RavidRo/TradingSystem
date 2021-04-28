import json
import operator
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseRule
from Backend.Domain.TradingSystem.user import User
from Backend.response import Response

# region class data
ops = {'great-than': operator.gt,
       'less-than': operator.lt,
       'great-equals': operator.ge,
       'less-equals': operator.le,
       'equals': operator.eq}

objs_operations = {'product': lambda self, products_to_quantities: self.product_operation(products_to_quantities),
                   'user': lambda self, user_age: self.user_operation(user_age),
                   'category': lambda self, products_to_quantities: self.category_operation(products_to_quantities),
                   'bag': lambda self, products_to_quantities: self.bag_operation(products_to_quantities)}


# endregion

class PurchaseLeaf(PurchaseRule):
    """
    The Leaf class represents the end objects of a composition. A leaf can't
    have any children.

    Usually, it's the Leaf objects that do the actual work, whereas Composite
    objects only delegate to their sub-components.
    """

    def __init__(self, identifier: str):
        self.id = identifier

    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        pass

    def edit_rule(self, rule_id: str, component: PurchaseRule):
        pass

    def remove(self, component_id: str) -> Response[None]:
        pass


class ConcreteLeaf(PurchaseLeaf):
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

    # For now- there are 4 kinds - age/category/product/shopping-bag
    # For each kind there is one value on which there is a rule
    def operation(self, products_to_quantities: dict, user_age: int) -> Response[None]:
        if self._context['obj'] == 'user' and objs_operations[self._context['obj']](self, user_age):
            return Response(True, msg="Purchase is permitted!")

        elif objs_operations[self._context['obj']](self, products_to_quantities):
            return Response(True, msg="Purchase is permitted!")

        return Response(False, msg="Purchase doesn't stand with the rules!")

    # region operations
    def user_operation(self, user_age: int):
        return ops[self._comparator](user_age, self._constraint)

    def category_operation(self, products_to_quantities: dict):
        category = self._context['identifier']
        amount_of_category = 0
        for product_id, (product, quantity) in products_to_quantities:
            if product.get_category() == category:
                amount_of_category += quantity

        return ops[self._comparator](amount_of_category, self._constraint)

    def product_operation(self, products_to_quantities: dict):
        prod_id = self._context['identifier']
        amount_of_prod = products_to_quantities.get(prod_id)[1]
        return ops[self._comparator](amount_of_prod, self._constraint)

    # ~ price before discounts ~
    def bag_operation(self, products_to_quantities: dict):
        cart_price = 0
        for _, (product, quantity) in products_to_quantities:
            cart_price += quantity * product.get_price()
        return ops[self._comparator](cart_price, self._constraint)

    # endregion

    def remove(self, component_id: str) -> Response[None]:
        if self.id == component_id:
            self.parent.children.remove(self)
            self.parent = None
            return Response(True, msg="rule was removed successfully!")
        return Response(False, msg=f"rule couldn't be removed with id:{component_id}")

    def edit_rule(self, rule_id: str, component: PurchaseRule):
        if self.id == rule_id:
            self.parent.children.remove(self)
            self.parent.children.append(component)
            component.parent = self.parent
            self.parent = None
            return Response(True, msg="rule was edited successfully!")
        return Response(False, msg=f"rule couldn't be edited with id:{rule_id}")

    def check_validity(self, new_parent_id: str) -> Response[None]:
        if self.id == new_parent_id:
            return Response(False, msg="Invalid move operation!")
        return Response(True, msg="Valid move")

    def parse(self):
        return {"id": self.id,
                "context": self._context,
                "operator": self._comparator,
                "target": self._constraint}
