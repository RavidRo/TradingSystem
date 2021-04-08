import Backend.Domain.TradingSystem.discount_type
import Backend.Domain.TradingSystem.store
from Backend.response import Response, PrimitiveParsable


class DiscountPolicy:
    def __init__(self):
        pass


class DefaultDiscountPolicy(DiscountPolicy):
    def __init__(self):
        super().__init__()
        self.discount_type = Backend.DefaultDiscountType()

    # def checkPolicy(self) -> Backend.DiscountType:
    #     return self.discount_type

    def applyDiscount(self, user, store, products_to_quantities: dict) -> Response[PrimitiveParsable]:
        # discount_type = self.checkPolicy()
        # return discount_type.apply_discount(products_to_quantities)
        return self.discount_type.apply_discount(products_to_quantities)
