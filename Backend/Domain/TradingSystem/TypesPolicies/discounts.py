from Backend.DataBase.Handlers import discounts_handler
from abc import ABC, abstractmethod
from typing import Union, List

from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.Interfaces.IDiscount import IDiscount
from Backend.response import Response


class Discounter(ABC):
    def __init__(self, identifier, percentage):
        self._identifier = identifier
        self.multiplier = percentage / 100.0

    @abstractmethod
    def discount_func(self, products_to_quantities, username):
        raise NotImplementedError

    def set_id(self, id):
        self._id = id


class ProductDiscountStrategy(Discounter):
    def __init__(self, identifier, percentage):
        super().__init__(identifier, percentage)

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
    def __init__(self, identifier, percentage):
        super().__init__(identifier, percentage)

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
        "product": lambda identifier, percentage: ProductDiscountStrategy(identifier, percentage),
        "category": lambda identifier, percentage: CategoryDiscountStrategy(identifier, percentage),
        "store": lambda identifier, percentage: StoreDiscountStrategy(percentage),
    }

    def create_condition_policy(self):
        from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import \
            AndCompositePurchaseRule
        from Backend.Domain.TradingSystem.TypesPolicies.purchase_policy import DefaultPurchasePolicy
        from Backend.DataBase.Handlers.store_handler import StoreHandler
        root_rule = AndCompositePurchaseRule()
        res = StoreHandler.get_instance().save_purchase_rule(root_rule)
        if not res.succeeded():
            return db_fail_response
        self._conditions_policy = DefaultPurchasePolicy(root_rule)
        self._conditions_policy_root_id = self._conditions_policy.get_root_id()
        return Response(True)


    def get_context(self):
        return self._context

    def __init__(self, discount_data, parent):  # Add duration in later milestones
        super().__init__(parent)
        self._parent = None
        self._context = discount_data["context"]
        self._discount_strategy = SimpleDiscount.strategy_generator[discount_data["context"]["obj"]](discount_data["context"].get("id"), discount_data["percentage"])
        self._discounter_data = {"obj": discount_data["context"]["obj"],
                                 "identifier": discount_data["context"].get("id"),
                                 "percentage": discount_data["percentage"]}

    def get_discount_strategy(self):
        if self._discount_strategy is None:
            self._discount_strategy = SimpleDiscount.strategy_generator[self._discounter_data["obj"]](self._discounter_data["identifier"], float(self._discounter_data["percentage"]))
        return self._discount_strategy

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        self.wrlock.acquire_read()
        if self._conditions_policy.checkPolicy(products_to_quantities, user_age).succeeded():
            discount = self.get_discount_strategy().discount_func(products_to_quantities, username)
        else:
            discount = 0.0
        self.wrlock.release_read()
        return discount

    def discount_func(self, products_to_quantities: dict, username) -> float:
        self.wrlock.acquire_read()
        discount = self._discount_strategy.discount_func(products_to_quantities, username)
        self.wrlock.release_read()
        return discount

    def get_discount_by_id(self, exist_id: str):
        if self.get_id() == exist_id:
            return self
        res = discounts_handler.DiscountsHandler.get_instance().load(exist_id)
        if res.succeeded():
            return res.get_obj()
        return None

    def is_composite(self) -> bool:
        return False

    def parse(self):
        self.wrlock.acquire_read()
        discount = super().parse()
        discount["percentage"] = self.get_discount_strategy().multiplier * 100
        discount["context"] = self._context
        self.wrlock.release_read()
        discount["discount_type"] = "simple"
        return discount

    def edit_simple_discount(self, discount_id, percentage=None, context=None):
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

        self.wrlock.acquire_write()
        self._context = context
        self._discounter_data = {"obj": context["obj"],
                                 "identifier": context.get("id"),
                                 "percentage": percentage}
        self._discount_strategy = SimpleDiscount.strategy_generator[context["obj"]](context.get("id"), percentage)
        from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
        res_commit = DiscountsHandler.get_instance().commit_changes()
        self.wrlock.release_write()
        if not res_commit.succeeded():
            return db_fail_response

        return Response(True)

    def edit_complex_discount(self, discount_id, complex_type=None, decision_rule=None):
        return Response(False, msg="The ID provided does not belong to complex type!")

    def remove_discount(self, discount_id: str) -> Response[None]:
        # assuming it has a parent
        if self.get_id() == discount_id:
            self.wrlock.acquire_write()
            from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
            res_remove = DiscountsHandler.get_instance().remove_rule(self)
            if res_remove.succeeded():
                res_commit = DiscountsHandler.get_instance().commit_changes()
                if res_commit.succeeded():
                    self.wrlock.release_write()
                    return Response(True, msg="Discount was removed successfully!")
                else:
                    self.wrlock.release_write()
                    return db_fail_response
            self.wrlock.release_write()
            return db_fail_response
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self._children: List[IDiscount] = []

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

        self.wrlock.acquire_write()
        for child in self._children:
            if child.edit_simple_discount(discount_id, percentage, context).succeeded():
                self.wrlock.release_write()
                return Response(True)
        self.wrlock.release_write()
        return Response(False, msg="The ID provided is not found!")

    complex_type_generator = {
        "max": lambda decision_rule, parent: MaximumCompositeDiscount(
            parent=parent
        ),
        "add": lambda decision_rule, parent: AddCompositeDiscount(
            parent=parent
        ),
        "xor": lambda decision_rule, parent: XorCompositeDiscount( decision_rule=decision_rule, parent=parent),
        "or": lambda decision_rule, parent: OrConditionDiscount(
            parent=parent
        ),
        "and": lambda decision_rule, parent: AndConditionDiscount(
            parent=parent
        ),
    }

    def edit_complex_discount(
        self, discount_id: str, complex_type: str = None, decision_rule: str = None):

        if self.get_id() == discount_id:
            msg = ""
            if complex_type is not None and complex_type not in ("max", "add", "xor", "and", "or"):
                msg += (
                    "complex_type must be one of the following: 'max', 'add', 'xor', 'and', 'or'\n"
                )
            if self.parent is None:
                msg += "Cannot edit root discount!\n"
            if (
                complex_type == "xor"
                and decision_rule is None
                and not isinstance(self, XorCompositeDiscount)
            ):
                msg += "When editing to xor discount, one must supply decision_rule"

            if msg != "":
                return Response(False, msg=msg)

            self.wrlock.acquire_write()
            parent = self.parent
            edited_discount = CompositeDiscount.complex_type_generator.get(complex_type)(decision_rule, parent)
            root_id = self._conditions_policy_root_id
            edited_discount._conditions_policy_root_id = root_id
            from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
            res_edit = DiscountsHandler.get_instance().edit_rule(self, edited_discount)
            if res_edit.succeeded():
                res_commit = DiscountsHandler.get_instance().commit_changes()
                self.wrlock.release_write()
                if res_commit.succeeded():
                    self.wrlock.release_write()
                    return Response(True)
            self.wrlock.release_write()
            return db_fail_response


        self.wrlock.acquire_write()
        for child in self._children:
            if child.edit_complex_discount(discount_id,complex_type, decision_rule).succeeded():
                self.wrlock.release_write()
                return Response(True)

        self.wrlock.release_write()
        return Response(False, msg="The ID provided is not found!")

    def get_discount_by_id(self, exist_id: str):
        if self.get_id() == exist_id:
            return self

        self.wrlock.acquire_read()
        for child in self._children:
            found_discount = child.get_discount_by_id(exist_id)
            if found_discount is not None:
                self.wrlock.release_read()
                return found_discount

        self.wrlock.release_read()

        from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
        res = DiscountsHandler.get_instance().load(exist_id)
        if not res.succeeded():
            return None

        return res.get_obj()

    def remove_discount(self, discount_id: str) -> Response[None]:
        self.wrlock.acquire_write()
        if self.get_id() == discount_id:
            if self.parent is None:
                self.wrlock.release_write()
                return Response(False, msg="Tries to remove hidden root!")
            from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
            res_remove = DiscountsHandler.get_instance().remove_rule(self)
            if res_remove.succeeded():
                res_commit = DiscountsHandler.get_instance().commit_changes()
                if res_commit.succeeded():
                    self.wrlock.release_write()
                    return Response(True, msg="Rule was removed successfully!")
                else:
                    self.wrlock.release_write()
                    return db_fail_response
            self.wrlock.release_write()
            return db_fail_response

        for child in self._children:
            child_res = child.remove_discount(discount_id)
            if child_res.succeeded():
                self.wrlock.release_write()
                return child_res

        self.wrlock.release_write()
        return Response(False, msg="discount to remove not found")

    def parse(self):
        discounts = super().parse()
        self.wrlock.acquire_read()
        discounts["discounts"] = [child.parse() for child in self._children]
        self.wrlock.release_read()
        discounts["discount_type"] = "complex"
        return discounts


class MaximumCompositeDiscount(CompositeDiscount):
    def __init__(self, parent=None):
        super().__init__(parent)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        self.wrlock.acquire_read()
        if len(self._children) == 0:
            self.wrlock.release_read()
            return 0.0
        discount = max(
            [child.apply_discount(products_to_quantities, user_age, username) for child in self._children]
        )
        self.wrlock.release_read()
        return discount

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "max"
        return discounts

    def discount_func(self, products_to_quantities: dict, username) -> float:
        self.wrlock.acquire_read()
        if len(self._children) == 0:
            discount = 0.0
        else:
            discount = max(
                [
                    child.discount_func(products_to_quantities, username)
                    for child in self._children
                ]
            )
        self.wrlock.release_read()
        return discount


class AddCompositeDiscount(CompositeDiscount):

    def __init__(self, parent=None):
        super().__init__(parent)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        self.wrlock.acquire_read()
        discount = sum(
            [child.apply_discount(products_to_quantities, user_age, username) for child in self._children]
        )
        self.wrlock.release_read()
        return discount

    def discount_func(self, products_to_quantities: dict, username) -> float:
        self.wrlock.acquire_read()
        discount = sum(
            [child.discount_func(products_to_quantities, username) for child in self._children]
        )
        self.wrlock.release_read()
        return discount

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

    def __init__(self, decision_rule: str, parent=None):
        super().__init__(parent)
        self.__desicion_rule = decision_rule

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        self.wrlock.acquire_read()
        prices = [
            child.apply_discount(products_to_quantities, user_age, username) for child in self._children
        ]
        discount = XorCompositeDiscount.decision_dict[self.__desicion_rule](prices)
        self.wrlock.release_read()
        return discount

    def discount_func(self, products_to_quantities: dict, username):
        self.wrlock.acquire_read()
        prices = [
            child.discount_func(products_to_quantities, username)
            for child in self._children
        ]
        discount = XorCompositeDiscount.decision_dict[self.__desicion_rule](prices)
        self.wrlock.release_read()
        return discount

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "xor"
        discounts["decision_rule"] = self.__desicion_rule
        return discounts


class AndConditionDiscount(CompositeDiscount):
    def __init__(self, parent=None):
        super().__init__(parent)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        self.wrlock.acquire_read()
        if all(
            [
                child._conditions_policy.checkPolicy(products_to_quantities, user_age).succeeded()
                for child in self._children
            ]
        ):
            discount = sum([child.discount_func(products_to_quantities, username) for child in self._children])
        else:
            discount = 0.0

        self.wrlock.release_read()
        return discount

    def discount_func(self, products_to_quantities: dict, username) -> float:
        self.wrlock.acquire_read()
        discount = sum(
                [child.discount_func(products_to_quantities, username) for child in self._children]
            )
        self.wrlock.release_read()
        return discount

    def parse(self):
        discounts = super().parse()
        discounts["type"] = "and"
        return discounts


class OrConditionDiscount(CompositeDiscount):
    def __init__(self, parent=None):
        super().__init__(parent)

    def apply_discount(self, products_to_quantities: dict, user_age: int, username) -> float:
        self.wrlock.acquire_read()
        if any(
            [
                child._conditions_policy.checkPolicy(products_to_quantities, user_age).succeeded()
                for child in self._children
            ]
        ):
            discount = sum([child.discount_func(products_to_quantities, username) for child in self._children])
        else:
            discount = 0.0

        self.wrlock.release_read()
        return discount

    def discount_func(self, products_to_quantities: dict, username) -> float:
        self.wrlock.acquire_read()
        discount = sum(
                [child.discount_func(products_to_quantities, username) for child in self._children]
            )
        self.wrlock.release_read()
        return discount

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
