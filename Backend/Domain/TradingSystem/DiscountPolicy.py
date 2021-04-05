from Backend.Domain.TradingSystem import Store
from Backend.Domain.TradingSystem.DiscountType import DefaultDiscountType, DiscountType
from Backend.Domain.TradingSystem.Interfaces import IDiscountPolicy, IDiscountType
from Backend.response import Response, PrimitiveParsable


class DiscountPolicy(IDiscountPolicy):
    def __init__(self):
        pass


class DefaultDiscountPolicy(DiscountPolicy):
    def __init__(self):
        self.discount_type = DefaultDiscountType()

    def checkPolicy(self) -> DiscountType:
        return self.discount_type

    def applyDiscount(self, user, store: Store, products_to_quantities:dict) -> Response[PrimitiveParsable]:
        discount_type = self.checkPolicy()
        return discount_type.applyDiscount(products_to_quantities)
