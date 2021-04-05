from dataclasses import dataclass

from Backend.Domain.TradingSystem import Store
from Backend.Domain.TradingSystem.Interfaces import IProduct
from Backend.Domain.TradingSystem.Interfaces.IShoppingBag import IShoppingBag
from Backend.Domain.TradingSystem.PurchaseDetails import PurchaseDetails
from Backend.response import Response, ParsableList, Parsable, PrimitiveParsable
from datetime import datetime


class ShoppingBag(IShoppingBag, Parsable):

    def __init__(self, store: Store):
        self.store = store
        self.product_ids_to_quantity = dict()
        self.pending_products_to_quantity = dict()
        self.pending_price = 0

    # using set for checking if element exists since it's O(1) instead of O(n)

    def parse(self):
        products_names_to_quantities = []
        for product_id, quantity in self.product_ids_to_quantity:
            product_name = self.store.get_prouct_name(product_id)
            products_names_to_quantities.append((product_name, quantity))
        return ShoppingBagDataObject(self.store.get_name(), products_names_to_quantities)

    def add_product(self, product_id: str, quantity: int) -> Response[None]:
        if self.product_in_bag(product_id):
            return Response(False,
                            msg="A product with id: " + str(product_id) + " already exists in the store's bag")
        self.product_ids_to_quantity.update(product_id, quantity)
        return Response(True,
                        msg=f"The product with id: {product_id} added successfully!")

    def remove_product(self, product_id: str) -> Response[None]:
        if self.product_ids_to_quantity.get(product_id) is None:
            return Response(False, msg="No such product in the bag")
        else:
            self.product_ids_to_quantity.pop(product_id)
        return Response(True, msg="Successfully removed product with id: " + str(product_id))

    # product info - list of tuples (product_id to purchase_type)
    def buy_products(self, user_info, products_info={}) -> Response[None]:

        """first step - check if all of the products exist in the store and acquire them"""
        availablility_response = self.store.check_available_products(self.product_ids_to_quantity)
        if not availablility_response.success:
            return availablility_response

        self.store.acquire_products(self.product_ids_to_quantity)

        """second step - check if the purchase_types are appropriate"""
        # since there are no purchase types for now- this checking isn't relevant
        if products_info:
            purchase_types_check = self.store.check_purchase_types(products_info, user_info)
            if not purchase_types_check.success:
                self.store.send_back(self.product_ids_to_quantity)
                return purchase_types_check

        """third step - check and apply the discount """
        self.pending_price = self.store.apply_discounts(self.product_ids_to_quantity, user_info)
        # for now it's a copy- all of the products purchased regularly so they all passed to pending
        self.pending_products_to_quantity = self.product_ids_to_quantity.copy()
        self.product_ids_to_quantity.clear()
        return Response[PrimitiveParsable](True, PrimitiveParsable(self.pending_price),
                                           msg="All the details are good! here comes the price")

    def change_product_qunatity(self, product_id: str, new_amount: int) -> Response[None]:
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")
        if self.product_ids_to_quantity.get(product_id) is None:
            return Response(False, msg="No such product in the bag")
        self.product_ids_to_quantity[product_id] = new_amount
        return Response(True, msg="amount changed successfully")

    def delete_products_after_purchase(self, user_name="guest") -> PurchaseDetails:
        # for now this function will only return details, in the future there will be specific deletion
        return PurchaseDetails(user_name, self.store.get_name(), self.pending_products_to_quantity.keys(),
                               datetime.now(), self.pending_price)

    def get_store_ID(self):
        return self.store.get_id()

    def product_in_bag(self, product_id: str):
        return not (self.product_ids_to_quantity.get(product_id) is None)


@dataclass
class ShoppingBagDataObject:
    store_name: str
    product_names_to_quantities: list
