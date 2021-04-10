from ...Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.response import Response, ParsableList, PrimitiveParsable


class CartStub(ShoppingCart):

    def __init__(self):
        self.save_product = False
        self.remove_product_delegated = False
        self.change_quantity = False
        self.buy_cart = False
        self.remove_after_purchase = False

    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        self.save_product = True
        return Response(True)

    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        self.remove_product_delegated = True
        return Response(True)

    def change_product_quantity(self, store_id, product_id, new_amount):
        self.change_quantity = True
        return Response(True)

    def buy_products(self, user, products_purchase_info={}) -> Response[PrimitiveParsable]:
        self.buy_cart = True
        return Response(True)

    def delete_products_after_purchase(self, user_name: str = "guest") -> Response[ParsableList]:
        self.remove_after_purchase = True
        return Response(True)
