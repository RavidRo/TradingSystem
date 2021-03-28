from Backend.Domain.TradingSystem.DiscountPolicy import DefaultDiscountPolicy
from Backend.Domain.TradingSystem.Interfaces import IPurchaseDetails, IStore
from Backend.Domain.TradingSystem import Product, PurchaseDetails
import uuid
from Backend.Domain.TradingSystem.PurchasePolicy import DefaultPurchasePolicy
from Backend.Domain.TradingSystem.Responsibilities import Responsibility
from Backend.response import Response, ParsableList


class Store(IStore):

    def __init__(self, store_name: str):
        """Create a new store with it's specified info"""
        self.id = str(self.id_generator())
        self.name = store_name
        self.products = []
        self.responsibility = None
        # These fields will be changed in the future versions
        self.discount_policy = DefaultDiscountPolicy()
        self.purchase_policy = DefaultPurchasePolicy()
        self.purchase_history = []

    def show_store_data(self) -> Response:
        # in the future other field will be checked too
        if self.responsibility is None:
            return Response(False, msg="Store's responsibilities aren't set yet")

        return Response[self](True, msg="Store's details are complete")

    def add_product(self, product_name: str, price: float, quantity: int) -> Response[None]:
        if quantity <= 0:
            # actually it's non-negative but adding 0 amount is redundant
            return Response(False, msg="Product's qunatity must be positive!")

        if price <= 0:
            return Response(False, msg="Product's price must pe positive!")

        if self.check_existing_product(product_name):
            return Response(False, msg="This product is already in the store's inventory")

        product = Product(self.id_generator(), product_name, price, quantity)
        self.products.append(product)
        return Response(True, msg="product" + str(product_name) + "successfully added")

    def remove_product(self, product_id: str) -> Response[None]:
        for prod in self.products:
            if prod.getID() == product_id:
                self.products.remove(prod)
                return Response(True, msg="Succesfully removed product " + str(prod.get_name()))
        return Response(False, msg="The product with id: " + str(product_id) + " is already not in the inventory!")

    def change_product_qunatity(self, product_id: str, quantity: int) -> Response[None]:
        for prod in self.products:
            if prod.getID() == product_id:
                prod.set_qunatity(quantity)
                return Response(True, msg="Succesfully updated product " + str(prod.get_name()) + "'s quantity")
        return Response(False, msg="The product with id: " + str(product_id) + " isn't in the inventory!")

    def edit_product_details(self, product_id: str, product_name: str, price: float) -> Response[None]:
        for prod in self.products:
            if prod.getID() == product_id:
                prod.change_details(product_name, price)
                return Response(True, msg="Succesfully updated product " + str(prod.get_name()) + "'s details")
        return Response(False, msg="The product with id: " + str(product_id) + " isn't in the inventory!")

    def get_personnel_info(self) -> Response[Responsibility]:
        if self.responsibility is None:
            return Response(False, msg="The store doesn't have assigned personnel")
        return Response[self.responsibility](True, msg="Personnel info")

    def get_purchases_history(self) -> Response[ParsableList[IPurchaseDetails]]:
        return Response[ParsableList(self.purchase_history)](True, msg="Purchase history")

    def update_store_history(self, purchase_details: PurchaseDetails):
        self.purchase_history.append(purchase_details)

    def id_generator(self) -> str:
        return uuid.uuid4()

    def get_id(self) -> str:
        return self.id

    def set_responsibility(self, responsibility: Responsibility):
        self.responsibility = responsibility

    def check_existing_product(self, product_name: str):
        for prod in self.products:
            if prod.get_name() == product_name:
                return True
        return False
