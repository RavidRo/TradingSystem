from Backend.response import Response, PrimitiveParsable


class DiscountType:
    def __init__(self):
        pass

    def apply_discount(self, products: list) -> Response[PrimitiveParsable[float]]:
        raise NotImplementedError


class DefaultDiscountType(DiscountType):
    def __init__(self):
        super().__init__()

    def apply_discount(self, products_to_quantities: dict) -> float:
        products_prices = [
            prod.price * quantity for prod_id, (prod, quantity) in products_to_quantities.items()
        ]
        return sum(products_prices)
