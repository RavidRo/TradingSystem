from Backend.Domain.TradingSystem.shopping_bag import ShoppingBag
from Backend.response import Response, PrimitiveParsable


class ShoppingBagStub(ShoppingBag):

    def __init__(self) -> None:
        self.dummy_product_price = 5
        self.products_to_quantity = {}

    def add_product(self, product_id : str, quantity: int):
        return Response(True)

    def remove_product(self, product_id: str) -> Response[None]:
        return Response(True)

    def change_product_quantity(self, product_id: str, new_amount: int) -> Response[None]:
        return Response(True)

    def buy_products(self, user_info, products_info={}) -> Response[None]:
        return Response(True, obj=PrimitiveParsable(self.dummy_product_price))