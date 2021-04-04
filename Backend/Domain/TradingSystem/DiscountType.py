from Backend.Domain.TradingSystem import Product
from Backend.Domain.TradingSystem.Interfaces import IDiscountType
from Backend.response import Response, PrimitiveParsable


class DiscountType(IDiscountType):
    def __init__(self):
        pass

    def apply_discount(self, products: list) -> Response[None]:
        raise NotImplementedError


class DefaultDiscountType(DiscountType):
    def __init__(self):
        pass

    def apply_discount(self, products: Product, ) -> Response[None]:
        products_prices = [prod.price for prod in products]
        return Response()[PrimitiveParsable](True, PrimitiveParsable(sum(products_prices)), msg="Discount applied")
