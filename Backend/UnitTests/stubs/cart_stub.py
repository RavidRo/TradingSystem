from ...Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.response import Response, ParsableList, PrimitiveParsable


class CartStub(ShoppingCart):

    def remove_product(self, store_id: str, product_id: str) -> Response[None]:
        return super().remove_product(store_id, product_id)

    def add_product(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        return super().add_product(store_id, product_id, quantity)

    def buy_products(self, user, products_purchase_info={}) -> Response[PrimitiveParsable]:
        return super().buy_products(user, products_purchase_info)

    def delete_products_after_purchase(self, user_name: str = "guest") -> Response[ParsableList]:
        return super().delete_products_after_purchase(user_name)

    def __init__(self):
        self.save_product = False
        self.remove_product = False
        self.change_quantity = False
        self.buy_cart = False
        self.remove_after_purchase = False

    def save_product_in_cart(self, store_id, product_id, quantity):
        self.save_product = True
        return Response(True)

    def delete_from_cart(self, store_id, product_id):
        self.remove_product = True
        return Response(True)

    def change_product_quantity(self, store_id, product_id, new_amount):
        self.change_quantity = True
        return Response(True)

    def buy_cart(self, current_user):
        self.buy_cart = False
        return Response(True)

    def remove_after_purchase(self, username):
        self.remove_after_purchase = True
        return Response(True)
