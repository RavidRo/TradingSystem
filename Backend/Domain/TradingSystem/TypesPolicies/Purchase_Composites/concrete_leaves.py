import operator

from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseLeaf

ops = {'>': operator.gt,
       '<': operator.lt,
       '>=': operator.ge,
       '<=': operator.le,
       '=': operator.eq}


class ConcreteLeaf(PurchaseLeaf):

    """leaf_details is a json of the format
        {context:
        {object: _
         object_identifier: _
         }
         comparator: _
         constraint: _
         }"""
    def __init__(self, leaf_details: dict):
        self._object = leaf_details['context']['object']
        self._object_id = leaf_details['context']['object_identifier']
        self._comparator = leaf_details['comparator']
        self._constraint = leaf_details['constraint']

    # For now- there are 4 kinds - age/category/product/shopping-bag
    # For each kind there is one value on which there is a rule
    def operation(self, products_to_quantities: dict, user_age: int) -> bool:
        if self._object == 'age':
            return ops[self._comparator](user_age, self._constraint)

        elif self._object == 'category':
            category = self._object_id
            amount_of_category = 0
            for product_id, (product, quantity) in products_to_quantities:
                if product.get_category() == category:
                    amount_of_category += quantity

            return ops[self._comparator](amount_of_category, self._constraint)

        elif self._object == 'product':
            prod_id = self._object_id
            amount_of_prod = products_to_quantities.get(prod_id)[1]
            return ops[self._comparator](amount_of_prod, self._constraint)

        # ~ price before discounts ~
        elif self._object == 'shopping_bag':
            cart_price = 0
            for _, (product, quantity) in products_to_quantities:
                cart_price += quantity * product.get_price()
            return ops[self._comparator](cart_price, self._constraint)

