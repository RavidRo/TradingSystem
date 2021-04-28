from Backend.response import Response

from ..Interfaces.IDiscount import IDiscount
from .discounts import MaximumCompositeDiscount, AddCompositeDiscount, SimpleDiscount, AndConditionDiscount, \
    OrConditionDiscount, XorCompositeDiscount


class DiscountPolicy:
    def __init__(self):
        pass


def make_discount(discount_data):
    if discount_data['context']['obj'] not in ('product', 'category', 'store'):
        return Response(False, msg="Discount context is not 'product', 'context', or 'store'!")
    discount = DefaultDiscountPolicy.discounts_generator[discount_data['discount_type']](discount_data)
    if discount is not None:
        return Response(True, discount)
    return Response(False, msg="Complex discount type should be 'max', 'add', 'and', 'or', or 'xor'!")


class DefaultDiscountPolicy(DiscountPolicy):
    discounts_generator = {'simple': lambda discount_data: SimpleDiscount(discount_data),
                           'complex': lambda discount_data:
                           MaximumCompositeDiscount([], discount_data.get('condition'))
                           if discount_data['type'] == 'max'
                           else AddCompositeDiscount([], discount_data.get('condition'))
                           if discount_data['type'] == 'add'
                           else AndConditionDiscount([], discount_data.get('condition'))
                           if discount_data['type'] == 'and'
                           else OrConditionDiscount([], discount_data.get('condition'))
                           if discount_data['type'] == 'or'
                           else XorCompositeDiscount(discount_data['decision_rule'], [], discount_data.get('condition'))
                           if discount_data['type'] == 'xor'
                           else None
                           }

    def __init__(self):
        super().__init__()
        self.__discount: IDiscount = AddCompositeDiscount([])  # retrieve from DB in later milestones

    def get_discounts(self) -> Response[IDiscount]:
        return Response[IDiscount](True, self.__discount)

    def add_discount(self, discount_data: dict, exist_id: str) -> Response[None]:
        discount_res = make_discount(discount_data)
        if not discount_res.succeeded():
            return discount_res

        exist_discount = self.__discount.get_discount_by_id(exist_id)
        if exist_discount is None:
            return Response(False, msg="Couldn't find the existing discount whose id was sent!")

        if not exist_discount.is_composite():
            return Response(False, msg="Tries to add child to simple discount! please create the composite discount "
                                       "first!")

        exist_discount.add_child(discount_res.get_obj())
        return Response(True)

    def move_discount(self, src_id, dest_id) -> Response[None]:
        src_discount = self.__discount.get_discount_by_id(src_id)
        if src_discount is None:
            return Response(False, msg="Source discount cannot be found!")

        if src_discount.get_discount_by_id(dest_id) is not None:
            return Response(False, msg="Cannot move discount to it's descendant!")

        dest_discount = self.__discount.get_discount_by_id(dest_id)
        if dest_discount is None:
            return Response(False, msg="Destination discount cannot be found")

        # TODO: check with Ravid if add src_discount as child of dest_discount or as it's sibling.
        if not dest_discount.is_composite():
            return Response(False, msg="Tries to add child to simple discount! please create the composite discount "
                                       "first!")

        src_discount.get_parent().remove_discount(src_id)
        dest_discount.add_child(src_discount)
        return Response(True)

    def remove_discount(self, discount_id: str) -> Response[None]:
        return self.__discount.remove_discount(discount_id)

    def edit_simple_discount(self, discount_id, percentage=None, condition=None, context=None, duration=None):
        return self.__discount.edit_simple_discount(discount_id, percentage, condition, context, duration)

    def edit_complex_discount(self, discount_id, complex_type=None, decision_rule=None):
        return self.__discount.edit_complex_discount(discount_id, complex_type, decision_rule)

    def applyDiscount(self, products_to_quantities: dict) -> float:
        return self.__discount.apply_discount(products_to_quantities)
