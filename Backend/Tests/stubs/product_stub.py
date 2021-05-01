from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response


class ProductStub(Product):

    def __init__(self, name: str) -> None:
        self.product_edited = False
        self.name = name

    def edit_product_details(self, product_name: str, category: str, price: float, keywords: list[str] = None):
        self.product_edited = True
        return Response(True)

    def get_name(self):
        return "product"

    def get_id(self):
        return '0'

    def get_price(self):
        return 1.0

    def get_category(self):
        return "A"

    def get_keywords(self):
        return ["white"]
