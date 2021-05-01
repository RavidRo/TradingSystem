from datetime import datetime

from Backend.response import Response, PrimitiveParsable
from Backend.Service.DataObjects.shopping_bag_data import ShoppingBagData
from Backend.Domain.TradingSystem.Interfaces.IShoppingBag import IShoppingBag
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class ShoppingBag(IShoppingBag):
    def __init__(self, store):
        self.__store = store
        self._products_to_quantity = dict()
        self.__pending_products_to_quantity = dict()
        self.__pending_price = 0

    def parse(self):
        products_ids_to_quantities = {}
        self_prods_to_quantites = self._products_to_quantity if self._products_to_quantity != {} else self.__pending_products_to_quantity
        for product_id in self_prods_to_quantites:
            products_ids_to_quantities[product_id] = self_prods_to_quantites[product_id][1]
        return ShoppingBagData(self.__store.get_name(), products_ids_to_quantities)

    """checks need to be made:
       ----------------------
       1. quantity is a positive number
       2. product with product_id exists in store with specified quantity 
       3. product with product_id doesn't already exist in the bag """

    def get_store(self):
        return self.__store

    def get_products_to_quantity(self):
        return self._products_to_quantity

    def get_pending_products_to_quantity(self):
        return self.__pending_products_to_quantity

    def get_pending_price(self):
        return self.__pending_price

    def add_product(self, product_id: str, quantity: int) -> Response[None]:

        if quantity <= 0:
            return Response(False, msg="quantity must be a positive number!")

        if not self.__store.product_exists(product_id):
            return Response(
                False,
                msg="A product with id: " + str(product_id) + " doesn't exist in store's inventory",
            )

        if not self.__store.has_enough(product_id, quantity):
            return Response(
                False,
                msg="A product with id: " + str(product_id) + " no in inventory enough",
            )

        if self._products_to_quantity.get(product_id) is not None:
            return Response(
                False, msg=f"A product with id: {product_id} already exists in the store's bag"
            )

        self._products_to_quantity.update(
            {product_id: (self.__store.get_product(product_id), quantity)}
        )
        return Response(True, msg=f"The product with id: {product_id} added successfully!")

    """checks need to be made:
       ----------------------
       1. product with product_id exists in bag 
                                            """

    def remove_product(self, product_id: str) -> Response[None]:

        if self._products_to_quantity.get(product_id) is None:
            return Response(
                False, msg=f"No such product in the bag of ths store{self.__store.get_name()}"
            )
        else:
            self._products_to_quantity.pop(product_id)
        return Response(True, msg="Successfully removed product with id: " + str(product_id))

    """checks need to be made:
       ----------------------
       1. check if products exist in the store with specified quantities
       2. check if purchase types are appropriate
                                            """

    # product info - list of tuples (product_id to purchase_type)
    def buy_products(self, user_age: int, products_info=None) -> Response[PrimitiveParsable[float]]:

        """first step - check if all of the products exist in the store and acquire"""
        if products_info is None:
            products_info = {}
        availability_response = self.__store.check_and_acquire_available_products(self._products_to_quantity)
        if not availability_response.success:
            return availability_response

        """second step - check if the purchase_types are appropriate"""
        # since there are no purchase types for now- this checking isn't relevant
        if products_info:
            self.purchase_types_checks(user_age, products_info)

        """third step - check and apply the discount """
        self.discount_apply()
        return Response[PrimitiveParsable[float]](
            True,
            PrimitiveParsable(self.__pending_price),
            msg="All the details are good! here comes the price",
        )

    def purchase_types_checks(self, user_info, products_info=None):
        if products_info is None:
            products_info = {}
        purchase_types_check = self.__store.check_purchase(products_info, user_info)
        if not purchase_types_check.success:
            self.__store.send_back(self._products_to_quantity)
            return purchase_types_check

    def discount_apply(self):
        self.__pending_price = self.__store.apply_discounts(self._products_to_quantity)
        # for now it's a copy- all of the products purchased regularly so they all passed to pending
        if not bool(self._products_to_quantity):
            self.send_back()
        self.__pending_products_to_quantity = self._products_to_quantity.copy()
        self._products_to_quantity.clear()

    """checks need to be made:
       ----------------------
       1. new_amount is a positive number
       2. product with product_id exists in the bag 
                                                """

    def change_product_quantity(self, product_id: str, new_amount: int) -> Response[None]:
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")
        if self._products_to_quantity.get(product_id) is None:
            return Response(False, msg="No such product in the bag")
        if not self.__store.has_enough(product_id, new_amount):
            return Response(
                False,
                msg="A product with id: " + str(product_id) + " no in inventory enough",
            )
        self._products_to_quantity[product_id] = (
            self._products_to_quantity.get(product_id)[0],
            new_amount,
        )
        return Response(True, msg="amount changed successfully")

    def delete_products_after_purchase(self, user_name="guest") -> PurchaseDetails:
        # for now this function will only return details, in the future there will be specific deletion
        product_names = [
            prod.get_name() for product_id, (prod, quantity) in self.__pending_products_to_quantity.items()
        ]
        self.__pending_products_to_quantity.clear()
        purchase_details = PurchaseDetails(user_name, self.__store.get_name(), product_names, datetime.now(),
                                           self.__pending_price)
        self.__store.update_store_history(purchase_details)
        return purchase_details

    def send_back(self):
        self._products_to_quantity = self.__pending_products_to_quantity.copy()
        self.__pending_products_to_quantity.clear()
        self.__store.send_back(products_to_quantities=self._products_to_quantity)

    def get_store_ID(self) -> str:
        return self.__store.get_id()

