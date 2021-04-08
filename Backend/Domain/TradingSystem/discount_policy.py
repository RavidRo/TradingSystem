from Backend.Domain.TradingSystem import store
from Backend.Domain.TradingSystem.discount_type import DefaultDiscountType, DiscountType
from Backend.Domain.TradingSystem.Interfaces import IDiscountPolicy, IDiscountType
from Backend.response import Response, PrimitiveParsable


class DiscountPolicy(IDiscountPolicy):
    def __init__(self):
        pass


class DefaultDiscountPolicy(DiscountPolicy):
    def __init__(self):
        super().__init__()
        self.discount_type = DefaultDiscountType()

    def checkPolicy(self) -> DiscountType:
        return self.discount_type

    def applyDiscount(self, user, store: store, products_to_quantities: dict) -> Response[PrimitiveParsable]:
        discount_type = self.checkPolicy()
        return discount_type.apply_discount(products_to_quantities)
