from Backend.Domain.TradingSystem.offer import Offer
from Backend.response import Response
import uuid

from Backend.Service.DataObjects.product_data import ProductData
from Backend.Domain.TradingSystem.Interfaces.IProduct import IProduct


class Product(IProduct):
    def __init__(self, product_name: str, category: str, price: float, keywords=None):
        if keywords is None:
            keywords = []
        self.__product_name = product_name
        self.__category = category
        self.__price = price
        self.__id = str(self.id_generator())
        self.__keywords = keywords
        self.__offers: dict[str, Offer] = {}

    def parse(self):
        return ProductData(
            self.__id, self.__product_name, self.__category, self.__price, self.__keywords
        )

    def parse_with_price(self, username):
        return ProductData(
            self.__id,
            self.__product_name,
            self.__category,
            self.get_offered_price(username),
            self.__keywords,
        )

    def set_product_name(self, new_name):
        self.__product_name = new_name

    def get_id(self):
        return self.__id

    def get_offered_price(self, username):
        for offer in self.__offers.values():
            if offer.get_username() == username and offer.is_approved():
                return offer.get_price()
        return self.__price

    def get_price(self):
        return self.__price

    def get_name(self):
        return self.__product_name

    def get_category(self):
        return self.__category

    def get_keywords(self):
        return self.__keywords

    def id_generator(self):
        return uuid.uuid4()

    def add_offer(self, offer: Offer) -> None:
        self.__offers[offer.get_id()] = offer

    def get_offers(self) -> list[Offer]:
        return list(self.__offers.values())

    def suggest_counter_offer(self, offer_id, price) -> Response[None]:
        if offer_id not in self.__offers:
            return Response(False, msg=f"The offer with id {offer_id} does not exist")

        return self.__offers[offer_id].suggest_counter_offer(price)

    def approve_user_offer(self, offer_id) -> Response[None]:
        if offer_id not in self.__offers:
            return Response(False, msg=f"The offer with id {offer_id} does not exist")

        return self.__offers[offer_id].approve_user_offer()

    def reject_user_offer(self, offer_id) -> Response[None]:
        if offer_id not in self.__offers:
            return Response(False, msg=f"The offer with id {offer_id} does not exist")

        return self.__offers[offer_id].reject_user_offer()

    def edit_product_details(
        self, product_name: str, category: str, price: float, keywords: list[str] = None
    ):
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

        return Response(True, msg=f"Successfully edited product with product id: {self.__id}")
