from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response


class ProductStub(Product):

    def __init__(self, name: str) -> None:
        self.product_edited = False
        self.name = name

    def edit_product_details(self, product_name: str, price: float):
        self.product_edited = True
        return Response(True)

    def get_name(self):
        return "product"

    def get_id(self):
        return '0'

    def get_price(self):
        return 1.0
