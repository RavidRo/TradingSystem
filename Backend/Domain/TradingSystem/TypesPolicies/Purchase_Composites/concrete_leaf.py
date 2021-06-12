import operator

from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.purchase_leaves import PurchaseLeaf
from Backend.response import Response

ops = {'great-than': operator.gt,
       'less-than': operator.lt,
       'great-equals': operator.ge,
       'less-equals': operator.le,
       'equals': operator.eq}


class UserLeafPurchaseRule(PurchaseLeaf):

    def __init__(self, leaf_details: dict):
        super().__init__(leaf_details)

    def operation(self, products_to_quantities: dict, user_age: int):
        if ops[self._comparator](user_age, self._constraint):
            return Response(True, msg="Purchase is permitted!")
        return Response(False,msg="Purchase is not permitted!")


class ProductLeafPurchaseRule(PurchaseLeaf):

    def __init__(self, leaf_details: dict):
        super().__init__(leaf_details)

    def operation(self, products_to_quantities: dict, user_age: int):
        prod_id = self._context['identifier']
        amount_of_prod = products_to_quantities.get(prod_id)[1]
        if ops[self._comparator](amount_of_prod, self._constraint):
            return Response(True, msg="Purchase is permitted!")
        return Response(False, msg="Purchase is not permitted!")


class CategoryLeafPurchaseRule(PurchaseLeaf):

    def __init__(self, leaf_details: dict):
        super().__init__(leaf_details)

    def operation(self, products_to_quantities: dict, user_age: int):
        category = self._context['identifier']
        amount_of_category = 0
        for product_id,(product, quantity) in products_to_quantities.items():
            if product.get_category() == category:
                amount_of_category += quantity

        if ops[self._comparator](amount_of_category, self._constraint):
            return Response(True, msg="Purchase is permitted!")
        return Response(False, msg="Purchase is not permitted!")


class BagLeafPurchaseRule(PurchaseLeaf):

    def __init__(self, leaf_details: dict):
        super().__init__(leaf_details)

    def operation(self, products_to_quantities: dict, user_age: int):
        cart_price = 0
        for _, (product, quantity) in products_to_quantities.items():
            cart_price += quantity * product.get_price()
        if ops[self._comparator](cart_price, self._constraint):
            return Response(True, msg="Purchase is permitted!")
        return Response(False, msg="Purchase is not permitted!")