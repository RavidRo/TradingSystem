from Backend.Domain.TradingSystem.Interfaces import IProduct
from Backend.Domain.TradingSystem.Interfaces.IShoppingBag import IShoppingBag
from Backend.response import Response, ParsableList


class ShoppingBag(IShoppingBag):
    # using set for checking if element exists since it's O(1) instead of O(n)

    def add_product(self, product_id: str, quantity: int) -> Response[None]:
        pass

    def remove_product(self, product_id: str) -> Response[None]:
        pass

    def show_bag(self) -> Response:
        pass

    def buy_products(self, products_info, user_info) -> Response[None]:
        pass

    def change_product_qunatity(self, product_id: str, new_amount: int) -> Response[None]:
        pass

    def delete_products_after_purchase(self) -> Response[ParsableList[IProduct]]:
        pass