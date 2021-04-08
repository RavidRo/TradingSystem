
import Backend.Domain.TradingSystem.discount_type
from Backend.Domain.TradingSystem.Interfaces import IDiscountPolicy
import Backend.Domain.TradingSystem.store
from Backend.response import Response, PrimitiveParsable


class DiscountPolicy(IDiscountPolicy):
    def __init__(self):
        pass


class DefaultDiscountPolicy(DiscountPolicy):
    def __init__(self):
        super().__init__()
        self.discount_type = Backend.DefaultDiscountType()

    def checkPolicy(self) -> Backend.DiscountType:
        return self.discount_type

    def applyDiscount(self, user, store: Backend.Store, products_to_quantities: dict) -> Response[PrimitiveParsable]:
        discount_type = self.checkPolicy()
        return discount_type.apply_discount(products_to_quantities)
