import uuid

from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct
from Backend.response import Response


class Product(IProduct):

    def __init__(self, product_name: str, price: float):
        self.product_name = product_name
        self.price = price
        self.id = str(self.id_generator())

    def show_product_data(self) -> Response:
        return Response[self](True, msg="Product's details")

    def edit_product_details(self, product_name: str, price: float):
        self.product_name = product_name
        self.price = price

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def id_generator(self):
        return uuid.uuid4()
