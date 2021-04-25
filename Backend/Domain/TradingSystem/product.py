from Backend.response import Response
import uuid

from Backend.Service.DataObjects.product_data import ProductData
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct


class Product(IProduct):
    def __init__(self, product_name: str, price: float):
        self.__product_name = product_name
        self.__price = price
        self.__id = str(self.id_generator())

    def parse(self):
        return ProductData(self.__id, self.__product_name, self.__price)

    def set_product_name(self, new_name):
        self.__product_name = new_name

    def get_id(self):
        return self.__id

    def get_price(self):
        return self.__price

    def get_name(self):
        return self.__product_name

    def id_generator(self):
        return uuid.uuid4()

    def edit_product_details(self, product_name: str, price: float):
        if price is not None:
            if price < 0:
                return Response(False, msg="Product's price must pe none negative!")
            self.__price = price

        if product_name is not None:
            if product_name == "":
                return Response(False, msg="Product's name can be an empty string!")
            self.__product_name = product_name

        return Response(True, msg=f"Successfully edited product with product id: {self.__id}")
