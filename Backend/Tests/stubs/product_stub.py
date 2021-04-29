from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response


class ProductStub(Product):

    def __init__(self, name: str, id: str = '0') -> None:
        self.product_edited = False
        self.name = name
        self.id = id

    def edit_product_details(self, product_name: str, category: str, price: float):
        self.product_edited = True
        return Response(True)

    def get_name(self):
        return "product"

    def get_id(self):
        return self.id

    def get_price(self):
        return 1.0
