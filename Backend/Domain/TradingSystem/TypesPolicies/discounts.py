from abc import ABC

from Backend.Domain.TradingSystem.Interfaces.IDiscount import IDiscount
from Backend.response import Response


class SimpleDiscount(IDiscount):

    def add_child(self, child: IDiscount) -> Response[None]:
        return Response(False, msg="Cannot add new discount to simple discount")

    def __init__(self, discount_data, duration=None):  # Add duration in later milestones
        super().__init__(discount_data.get('condition'))
        self._multiplier = discount_data['percentage'] / 100.0
        self._parent = None
        self._context = discount_data['context']
        self.duration = duration

        def discount_func(products_to_quantities) -> float:
            if "product" in discount_data['context']:
                return sum(
                    [prod.get_price() * quantity * self._multiplier if prod_id == discount_data['context'][
                        "product"] else 0
                     for prod_id, (prod, quantity) in products_to_quantities.items()])
            if "category" in discount_data['context']:
                return sum([
                    prod.get_price() * quantity * self._multiplier if prod.get_category() == discount_data['context'][
                        "category"] else 0
                    for prod_id, (prod, quantity) in products_to_quantities.items()])
            if "store" in discount_data['context']:
                return sum([prod.get_price() * quantity * self._multiplier
                            for prod_id, (prod, quantity) in
                            products_to_quantities.items()])

            raise RuntimeError("This shouldn't happen!")

        self.discount_func = discount_func

    def get_discount_by_id(self, exist_id: str):
        if self._id == exist_id:
            return self
        return None

    def is_composite(self) -> bool:
        return False

    def parse(self):
        discount = dict()
        discount['percentage'] = self._multiplier * 100
        discount['condition'] = self._condition.parse()
        discount['context'] = self._context
        discount['id'] = self.get_id()
        return discount

    def edit_simple_discount(self, discount_id, percentage=None, condition=None, context=None, duration=None):
        if self.get_id() != discount_id:
            return Response(False, msg="The ID provided is not found!")

        if percentage is not None:
            self._multiplier = percentage / 100
        if condition is not None:
            # TODO: ask Sean to implement this (fit this call to his interface)

            # self._condition.edit_condition(condition)
            self._condition = condition
        if context is not None:
            self._context = context

        return Response(True)

    def edit_complex_discount(self, discount_id, complex_type=None, decision_rule=None):
        return Response(False, msg="The ID provided does not belong to complex type!")

    def remove_discount(self, discount_id: str) -> Response[None]:
        # assuming it has a parent
        if self._id == discount_id:
            self.get_parent().remove_discount(self._id)
            self.set_parent(None)  # kinda redundant
            return Response(True)
        return Response(False, msg="discount to remove not found!")


class CompositeDiscount(IDiscount, ABC):
    def __init__(self, children: list[IDiscount] = None, condition=None):
        super().__init__(condition)
        if children is None:
            children = []
        self._children = children
        for child in children:
            if child.get_parent() is not None:
                self.set_parent(
                    child.get_parent())  # Assuming at most 1 child has parent (when merging with existing discount)
                break
        [child.set_parent(self) for child in children]

    def add_child(self, child: IDiscount):
        self._children.append(child)
        child.set_parent(self)

    def remove_child(self, child):
        self._children.remove(child)
        child.set_parent(None)

    def is_composite(self) -> bool:
        return True

    def edit_simple_discount(self, discount_id, percentage=None, condition=None, context=None, duration=None):
        if self.get_id() == discount_id:
            return Response(False, msg="The ID provided is not belong to simple discount!")

        for child in self._children:
            if child.edit_simple_discount(discount_id, percentage, condition, context).succeeded():
                return Response(True)
        return Response(False, msg="The ID provided is not found!")

    complex_type_generator = {
        "max": lambda children, decision_rule: MaximumCompositeDiscount(children=children),
        "add": lambda children, decision_rule: AddCompositeDiscount(children=children),
        "xor": lambda children, decision_rule: XorCompositeDiscount(children=children, decision_rule=decision_rule),
        "or": lambda children, decision_rule: OrConditionDiscount(children=children),
        "and": lambda children, decision_rule: AndConditionDiscount(children=children)
    }

    def edit_complex_discount(self, discount_id: str, complex_type: str = None, decision_rule: str = None):
        if self.get_id() == discount_id:
            self.get_parent().add_child(CompositeDiscount.complex_type_generator.get(complex_type)(self._children, decision_rule))
            self.get_parent().remove_child(self.get_id())
            return Response(True)

        for child in self._children:
            if child.edit_complex_discount(discount_id, complex_type, decision_rule).succeeded():
                return Response(True)
        return Response(False, msg="The ID provided is not found!")

    def get_discount_by_id(self, exist_id: str):
        if self._id == exist_id:
            return self
        for child in self._children:
            if child.get_discount_by_id(exist_id) is not None:
                return child
        return None

    def remove_discount(self, discount_id: str) -> Response[None]:
        if self._id == discount_id:
            self.get_parent().remove_child(self)
            self.set_parent(None)  # kinda redundant
            return Response(True)
        for child in self._children:
            child_res = child.remove_discount(discount_id)
            if child_res.succeeded():
                return child_res
        return Response(False, msg="discount to remove not found")

    def parse(self):
        discounts = [child.parse() for child in self._children]
        return discounts


class MaximumCompositeDiscount(CompositeDiscount):

    def __init__(self, children: list[IDiscount] = None, condition=None):
        super().__init__(children, condition)

        def discount_func(products_to_quantities) -> float:
            if len(self._children) == 0:
                return 0.0
            return max([child.apply_discount(products_to_quantities) for child in self._children])

        self.discount_func = discount_func

    def parse(self):
        discounts = dict()
        discounts['discounts'] = super().parse()
        discounts['merger'] = "max"
        return discounts


class AddCompositeDiscount(CompositeDiscount):

    def __init__(self, children: list[IDiscount] = None, condition=None):
        super().__init__(children, condition)

        def discount_func(products_to_quantities) -> float:
            return sum([child.apply_discount(products_to_quantities) for child in self._children])

        self.discount_func = discount_func

    def parse(self):
        discounts = dict()
        discounts['discounts'] = super().parse()
        discounts['merger'] = "add"
        return discounts


class XorCompositeDiscount(CompositeDiscount):
    decision_dict = {"first": lambda prices: prices[0] if len(prices) > 0 else 0.0,
                     "max": lambda prices: max(prices) if len(prices) > 0 else 0.0,
                     "min": lambda prices: min(prices) if len(prices) > 0 else 0.0
                     }

    def __init__(self, decision_rule: str, children: list[IDiscount] = None, condition=None):
        super().__init__(children, condition)

        def discount_func(products_to_quantities) -> float:
            prices = [child.apply_discount(products_to_quantities) for child in self._children]
            return XorCompositeDiscount.decision_dict[decision_rule](prices)

        self.discount_func = discount_func

    def parse(self):
        discounts = dict()
        discounts['discounts'] = super().parse()
        discounts['merger'] = "xor"
        return discounts


class AndConditionDiscount(CompositeDiscount):

    def __init__(self, children: list[IDiscount] = None, condition=None):
        super().__init__(children, condition)

    def apply_discount(self, products_to_quantities: dict) -> float:
        if all([child._condition(products_to_quantities) for child in self._children]):
            return sum([child.discount_func(products_to_quantities) for child in self._children])
        return 0.0

    def parse(self):
        discounts = dict()
        discounts['discounts'] = super().parse()
        discounts['merger'] = "and"
        return discounts


class OrConditionDiscount(CompositeDiscount):

    def __init__(self, children: list[IDiscount] = None, condition=None):
        super().__init__(children, condition)

    def apply_discount(self, products_to_quantities: dict) -> float:
        if any([child._condition(products_to_quantities) for child in self._children]):
            return sum([child.discount_func(products_to_quantities) for child in self._children])
        return 0.0

    def parse(self):
        discounts = dict()
        discounts['discounts'] = super().parse()
        discounts['merger'] = "or"
        return discounts


"""

add(discount_data, parent_id)

discount_data:

{
    discount_type: simple / complex
    percentage: 1-100
    condition?: {...}
    context: {
        obj: product / category / store
        id?: <some_id>
        }
    }
    type: max / add / and / or / xor
    decision_rule?: first / max / min (for xor)
} 
 
get_discounts() -> 
{
    discount: {
        simple: {...}
        complex: {
            type:
            decision_rule:
            children: []
            }
    }
}

"""
