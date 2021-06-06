from Backend.DataBase.database import db_fail_response
from Backend.response import Response
import uuid

from Backend.Service.DataObjects.product_data import ProductData
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct


class Product(IProduct):
    def __init__(self, product_name: str, category: str, price: float, keywords=None):
        from Backend.DataBase.Handlers.product_handler import ProductHandler
        if keywords is None:
            keywords = []
        self.__product_name = product_name
        self.__category = category
        self.__price = price
        self.__id = str(self.id_generator())
        self.__keywords = keywords
        self.__product_handler = ProductHandler.get_instance()

    def parse(self):
        return ProductData(self.__id, self.__product_name, self.__category, self.__price, self.__keywords)

    def set_product_name(self, new_name):
        self.__product_name = new_name

    def get_id(self):
        return self.__id

    def get_price(self):
        return self.__price

    def get_name(self):
        return self.__product_name

    def get_category(self):
        return self.__category

    def get_keywords(self):
        return self.__keywords

    def set_keywords(self, keywords):
        self.__keywords = keywords

    def id_generator(self):
        return uuid.uuid4()

    def edit_product_details(self, product_name: str, category: str, price: float, keywords: list[str] = None):
        msg = ""
        if price is not None and price < 0:
            msg += "Product's price must pe none negative!\n"
        if product_name is not None and product_name == "":
            msg += "Product's name cannot be an empty string!\n"
        if category is not None and category == "":
            msg += "Category name cannot be an empty string!\n"

        if msg != "":
            return Response(False, msg=msg)

        if price is not None:
            self.__price = price

        if product_name is not None:
            self.__product_name = product_name

        if keywords is not None:
            self.__keywords = keywords

        if category is not None:
            self.__category = category

        res = self.__product_handler.commit_changes()
        if not res.succeeded():
            return db_fail_response

        return Response(True, msg=f"Successfully edited product with product id: {self.__id}")
