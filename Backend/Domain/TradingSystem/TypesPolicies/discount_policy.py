import threading

from Backend.DataBase.database import db_fail_response
from Backend.response import Response

from ..Interfaces.IDiscount import IDiscount
from .discounts import (
    MaximumCompositeDiscount,
    AddCompositeDiscount,
    SimpleDiscount,
    AndConditionDiscount,
    OrConditionDiscount,
    XorCompositeDiscount,
)


class DiscountPolicy:
    def generate_id(self) -> str:
        with self.auto_id_lock:
            self.auto_id += 1
            return str(self.auto_id - 1)

    def __init__(self):
        self.auto_id_lock = threading.Lock()
        self.auto_id = 1


CONDITION_ROOT_ID = "1"


class DefaultDiscountPolicy(DiscountPolicy):
    def __init__(self, root_rule):
        super().__init__()
        from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
        self.__discounts_rules_handler = DiscountsHandler.get_instance()
        self.__discount: IDiscount = root_rule
        self.discounts_generator = {
            "simple": lambda discount_data, parent=None: SimpleDiscount(discount_data, parent),
            "complex": lambda discount_data, parent=None: MaximumCompositeDiscount(parent)
            if discount_data["type"] == "max"
            else AddCompositeDiscount(parent)
            if discount_data["type"] == "add"
            else AndConditionDiscount(parent)
            if discount_data["type"] == "and"
            else OrConditionDiscount(parent)
            if discount_data["type"] == "or"
            else XorCompositeDiscount(discount_data["decision_rule"], parent)
            if discount_data["type"] == "xor"
            else None,
        }

    def make_discount(self, discount_data, parent):
        if "discount_type" not in discount_data or discount_data["discount_type"] not in (
            "simple",
            "complex",
        ):
            return Response(
                False, msg="discount must have discount_type from ('simple', 'complex')"
            )
        if discount_data["discount_type"] == "simple":
            if discount_data["context"]["obj"] not in ("product", "category", "store"):
                return Response(
                    False, msg="Discount context is not 'product', 'context', or 'store'!"
                )
            if "percentage" not in discount_data or (
                discount_data["percentage"] < 0.0 or discount_data["percentage"] > 100.0
            ):
                return Response(False, msg="Percentage of discount must be between 0 and 100")
        else:
            if "type" in discount_data and discount_data["type"] not in (
                "max",
                "add",
                "and",
                "or",
                "xor",
            ):
                return Response(False, msg="Invalid type value for complex discount")
            if (
                "type" in discount_data
                and discount_data["type"] == "xor"
                and "decision_rule" not in discount_data
            ):
                return Response(False, msg="Xor discount must have decision_rule")
        discount = self.discounts_generator[discount_data["discount_type"]](discount_data, parent)
        if discount is not None:
            return Response(True, discount)
        return Response(
            False, msg="Complex discount type should be 'max', 'add', 'and', 'or', or 'xor'!"
        )

    def get_discounts(self) -> Response[IDiscount]:
        return Response[IDiscount](True, self.__discount)

    def add_discount(self, discount_data: dict, exist_id: str, condition_type=None) -> Response[None]:
        exist_discount = self.__discount.get_discount_by_id(exist_id)

        if exist_discount is None:
            return Response(False, msg="Couldn't find the existing discount whose id was sent!")

        if not exist_discount.is_composite():
            exist_discount.wrlock.release_write()
            return Response(False, msg="Tries to add child to simple discount! please create the composite discount "
                                       "first!")

        discount_res = self.make_discount(discount_data, exist_discount)
        res_condition = discount_res.get_obj().create_purchase_rules_root()
        if not res_condition.succeeded():
            return db_fail_response

        if not discount_res.succeeded():
            return discount_res

        if "condition" in discount_data:
            condition_policy_res = discount_res.get_obj().get_conditions_policy()
            if not condition_policy_res.suceeded():
                return condition_policy_res
            res_add = condition_policy_res.get_obj().add_purchase_rule(discount_data["condition"], condition_type, CONDITION_ROOT_ID)
            if not res_add.succeded():
                return res_add

        exist_discount.wrlock.acquire_write()
        from Backend.DataBase.Handlers.discounts_handler import DiscountsHandler
        res_save = DiscountsHandler.get_instance().save(discount_res.get_obj())
        if res_save.succeeded():
            res_commit = DiscountsHandler.get_instance().commit_changes()
            if res_commit.succeeded():
                exist_discount.wrlock.release_write()
                return Response(True, msg="Discount was added successfully!")
        exist_discount.wrlock.release_write()
        return db_fail_response

    def move_discount(self, src_id, dest_id) -> Response[None]:
        if src_id == dest_id:
            return Response(False, msg="Cannot move discount to itself!")

        src_discount = self.__discount.get_discount_by_id(src_id)
        if src_discount is None:
            return Response(False, msg="Source discount cannot be found!")

        if src_discount.get_discount_by_id(dest_id) is not None:
            return Response(False, msg="Cannot move discount to it's descendant!")

        dest_discount = self.__discount.get_discount_by_id(dest_id)
        if dest_discount is None:
            return Response(False, msg="Destination discount cannot be found")

        # this is the top line that can acquire write since get_discount_by_id acquires all the branches read.
        src_discount.wrlock.acquire_write()
        dest_discount.wrlock.acquire_write()

        if not dest_discount.is_composite():
            dest_discount.wrlock.release_write()
            src_discount.wrlock.release_write()
            return Response(False, msg="Tries to add child to simple discount! please create the composite discount "
                                       "first!")

        src_discount.parent.remove_child(src_discount)
        dest_discount.add_child(src_discount)

        dest_discount.wrlock.release_write()
        src_discount.wrlock.release_write()
        return Response(True)

    def remove_discount(self, discount_id: str) -> Response[None]:
        return self.__discount.remove_discount(discount_id)

    def edit_simple_discount(self, discount_id, percentage=None, context=None, duration=None):
        return self.__discount.edit_simple_discount(discount_id, percentage, context, duration)

    def edit_complex_discount(self, discount_id, complex_type=None, decision_rule=None):
        return self.__discount.edit_complex_discount(
            discount_id, self.generate_id(), complex_type, decision_rule
        )

    def applyDiscount(self, products_to_quantities: dict, user_age: int, username) -> float:
        return self.__discount.apply_discount(products_to_quantities, user_age, username)

    def get_discount_by_id(self, discount_id):
        return self.__discount.get_discount_by_id(discount_id)

    def get_root_id(self):
        return self.__discount._id
