from abc import ABC, abstractmethod
from typing import Union

from Backend.Domain.TradingSystem.Interfaces.IDiscount import IDiscount
from Backend.response import Response


class Discounter(ABC):
    def __init__(self, id, percentage):
        self._id = id
        self.multiplier = percentage / 100.0

    @abstractmethod
    def discount_func(self, products_to_quantities, username):
        raise NotImplementedError

    def set_id(self, id):
        self._id = id


class ProductDiscountStrategy(Discounter):
    def __init__(self, id, percentage):
        super().__init__(id, percentage)

    def discount_func(self, products_to_quantities, username):
        return sum(
            [
                prod.get_offered_price(username) * quantity * self.multiplier
                if prod_id == self._id
                else 0
                for prod_id, (prod, quantity) in products_to_quantities.items()
            ]
        )


class CategoryDiscountStrategy(Discounter):
    def __init__(self, id, percentage):
        super().__init__(id, percentage)

    def discount_func(self, products_to_quantities, username):
        return sum(
            [
                prod.get_offered_price(username) * quantity * self.multiplier
                if prod.get_category() == self._id
                else 0
                for _, (prod, quantity) in products_to_quantities.items()
            ]
        )


class StoreDiscountStrategy(Discounter):
    def __init__(self, percentage):
        super().__init__(None, percentage)

    def discount_func(self, products_to_quantities, username):
        return sum(
            [
                prod.get_offered_price(username) * quantity * self.multiplier
                for _, (prod, quantity) in products_to_quantities.items()
            ]
        )


class SimpleDiscount(IDiscount):
    strategy_generator = {
        "product": lambda id, percentage: ProductDiscountStrategy(id, percentage),
        "category": lambda id, percentage: CategoryDiscountStrategy(id, percentage),
        "store": lambda id, percentage: StoreDiscountStrategy(percentage),
    }

    def get_context(self):
        return self._context

    def __init__(self, discount_data, id, duration=None):  # Add duration in later milestones
        super().__init__(id)
        self._parent = None
        self._context = discount_data["context"]
        self._discount_strategy = SimpleDiscount.strategy_generator[
            discount_data["context"]["obj"]
        ](discount_data["context"].get("id"), discount_data["percentage"])
        self._duration = duration

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        if self._conditions_policy.checkPolicy(products_to_quantities, user_age):
            return self._discount_strategy.discount_func(products_to_quantities, username)
        return 0.0

    def get_discount_by_id(self, exist_id: str):
        if self._id == exist_id:
            return self
        return None

    def is_composite(self) -> bool:
        return False

    def parse(self):
        discount = super().parse()
        discount["percentage"] = self._discount_strategy.multiplier * 100
        discount["context"] = self._context
        discount["discount_type"] = "simple"
        return discount

    def edit_simple_discount(self, discount_id, percentage=None, context=None, duration=None):
        if self.get_id() != discount_id:
            return Response(False, msg="The ID provided is not found!")

        msg = ""

        if percentage is not None and (percentage < 0 or percentage > 100):
            msg += "Percentage parameter must be at range 0-100\n"

        if context is not None:
            if "obj" not in context:
                msg += "context must include 'obj' key\n"
            else:
                if context["obj"] not in ("product", "category", "store"):
                    msg += "context object must be one of the following: 'product', 'category', 'store'\n"
            if context["obj"] != "store" and ("id" not in context):
                msg += "context must include 'id' key\n"

        # add conditions on duration in later milestones

        if msg != "":
            return Response(False, msg=msg)

        if context is not None:
            if self._context["obj"] == context["obj"]:
                self._context["id"] = context.get("id")
                self._discount_strategy.set_id(context.get("id"))
            else:
                self._discount_strategy = SimpleDiscount.strategy_generator[context["obj"]](
                    context.get("id"),
                    percentage
                    if percentage is not None
                    else self._discount_strategy.multiplier * 100,
                )
                self._context = context

        if percentage is not None:
            self._discount_strategy.multiplier = percentage / 100

        if duration is not None:
            self._duration = duration

        return Response(True)

    def edit_complex_discount(self, discount_id, new_id, complex_type=None, decision_rule=None):
        return Response(False, msg="The ID provided does not belong to complex type!")

    def remove_discount(self, discount_id: str) -> Response[None]:
        # assuming it has a parent
        if self._id == discount_id:
            self.get_parent().remove_child(self)
            self.set_parent(None)  # kinda redundant
            return Response(True)
        return Response(False, msg="discount to remove not found!")

    def get_children(self) -> Union[list[IDiscount], None]:
        return None

    def get_parent(self) -> IDiscount:
        return self._parent

    def add_child(self, child: IDiscount) -> Response[None]:
        return Response(False, msg="Cannot add new discount to simple discount")

    def remove_child(self, child: IDiscount):
        return Response(False, msg="Cannot remove discount to simple discount")


class CompositeDiscount(IDiscount, ABC):
    def __init__(self, children: list[IDiscount] = None, id="1"):
        super().__init__(id)
        if children is None:
            children = []
        self._children = children
        for child in children:
            if child.get_parent() is not None:
                self.set_parent(
                    child.get_parent()
                )  # Assuming at most 1 child has parent (when merging with existing discount)
                break
        [child.set_parent(self) for child in children]

    def get_context(self):
        return None

    def add_child(self, child: IDiscount):
        self._children.append(child)
        child.set_parent(self)
        return Response(True)

    def remove_child(self, child: IDiscount):
        self._children.remove(child)
        child.set_parent(None)
        return Response(True)

    def get_children(self) -> list[IDiscount]:
        return self._children

    def is_composite(self) -> bool:
        return True

    def edit_simple_discount(self, discount_id, percentage=None, context=None, duration=None):
        if self.get_id() == discount_id:
            return Response(False, msg="The ID provided is not belong to simple discount!")

        for child in self._children:
            if child.edit_simple_discount(discount_id, percentage, context).succeeded():
                return Response(True)
        return Response(False, msg="The ID provided is not found!")

    complex_type_generator = {
        "max": lambda children, decision_rule, new_id: MaximumCompositeDiscount(
            children=children, new_id=new_id
        ),
        "add": lambda children, decision_rule, new_id: AddCompositeDiscount(
            children=children, new_id=new_id
        ),
        "xor": lambda children, decision_rule, new_id: XorCompositeDiscount(
            children=children, decision_rule=decision_rule, new_id=new_id
        ),
        "or": lambda children, decision_rule, new_id: OrConditionDiscount(
            children=children, new_id=new_id
        ),
        "and": lambda children, decision_rule, new_id: AndConditionDiscount(
            children=children, new_id=new_id
        ),
    }

    def edit_complex_discount(
        self, discount_id: str, new_id: str, complex_type: str = None, decision_rule: str = None
    ):

        if self.get_id() == discount_id:
            msg = ""
            if complex_type is not None and complex_type not in ("max", "add", "xor", "and", "or"):
                msg += (
                    "complex_type must be one of the following: 'max', 'add', 'xor', 'and', 'or'\n"
                )
            if self.get_parent() is None:
                msg += "Cannot edit root discount!\n"
            if (
                complex_type == "xor"
                and decision_rule is None
                and not isinstance(self, XorCompositeDiscount)
            ):
                msg += "When editing to xor discount, one must supply decision_rule"

            if msg != "":
                return Response(False, msg=msg)
            parent_children = self.get_parent().get_children()
            parent_children[
                parent_children.index(self)
            ] = CompositeDiscount.complex_type_generator.get(complex_type)(
                self._children, decision_rule, new_id
            )
            self._id = discount_id
            return Response(True)

        for child in self._children:
            if child.edit_complex_discount(
                discount_id, new_id, complex_type, decision_rule
            ).succeeded():
                return Response(True)
        return Response(False, msg="The ID provided is not found!")

    def get_discount_by_id(self, exist_id: str):
        if self._id == exist_id:
            return self
        for child in self._children:
            found_discount = child.get_discount_by_id(exist_id)
            if found_discount is not None:
                return found_discount
        return None

    def remove_discount(self, discount_id: str) -> Response[None]:
        if self._id == discount_id:
            if self.get_parent() is None:
                return Response(False, msg="Tries to remove hidden root!")
            self.get_parent().remove_child(self)
            self.set_parent(None)  # kinda redundant
            return Response(True)
        for child in self._children:
            child_res = child.remove_discount(discount_id)
            if child_res.succeeded():
                return child_res
        return Response(False, msg="discount to remove not found")

    def parse(self):
        discounts = super().parse()
        discounts["discounts"] = [child.parse() for child in self._children]
        discounts["discount_type"] = "complex"
        return discounts


class MaximumCompositeDiscount(CompositeDiscount):
    def __init__(self, children: list[IDiscount] = None, new_id="1"):
        super().__init__(children, new_id)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        if len(self._children) == 0:
            return 0.0
        return max(
            [
                child.apply_discount(products_to_quantities, user_age, username)
                for child in self._children
            ]
        )

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "max"
        return discounts


class AddCompositeDiscount(CompositeDiscount):
    def __init__(self, children: list[IDiscount] = None, new_id="1"):
        super().__init__(children, new_id)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        return sum(
            [
                child.apply_discount(products_to_quantities, user_age, username)
                for child in self._children
            ]
        )

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "add"
        return discounts


class XorCompositeDiscount(CompositeDiscount):
    decision_dict = {
        "first": lambda prices: prices[0] if len(prices) > 0 else 0.0,
        "max": lambda prices: max(prices) if len(prices) > 0 else 0.0,
        "min": lambda prices: min(prices) if len(prices) > 0 else 0.0,
    }

    def __init__(self, decision_rule: str, children: list[IDiscount] = None, new_id="1"):
        super().__init__(children, new_id)
        self.__desicion_rule = decision_rule

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        prices = [
            child.apply_discount(products_to_quantities, user_age, username)
            for child in self._children
        ]
        return XorCompositeDiscount.decision_dict[self.__desicion_rule](prices)

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "xor"
        discounts["decision_rule"] = self.__desicion_rule
        return discounts


class AndConditionDiscount(CompositeDiscount):
    def __init__(self, children: list[IDiscount] = None, new_id="1"):
        super().__init__(children, new_id)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        if all(
            [
                child._conditions_policy.checkPolicy(products_to_quantities, user_age)
                for child in self._children
            ]
        ):
            return sum(
                [child.discount_func(products_to_quantities, username) for child in self._children]
            )
        return 0.0

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "and"
        return discounts


class OrConditionDiscount(CompositeDiscount):
    def __init__(self, children: list[IDiscount] = None, new_id="1"):
        super().__init__(children, new_id)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        if any(
            [
                child._conditions_policy.checkPolicy(products_to_quantities, user_age)
                for child in self._children
            ]
        ):
            return sum(
                [child.discount_func(products_to_quantities, username) for child in self._children]
            )
        return 0.0

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "or"
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
