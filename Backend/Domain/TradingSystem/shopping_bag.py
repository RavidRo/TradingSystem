from datetime import datetime

from Backend.DataBase.Handlers.purchase_details_handler import PurchaseDetailsHandler
from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.product import Product
from Backend.response import Response, PrimitiveParsable
from Backend.Service.DataObjects.shopping_bag_data import ShoppingBagData
from Backend.Domain.TradingSystem.Interfaces.IShoppingBag import IShoppingBag
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails


class ShoppingBag(IShoppingBag):
    def __init__(self, store):
        from Backend.DataBase.Handlers.shopping_bag_handler import ShoppingBagHandler
        self.__store = store
        # self.store_id = store.get_id()
        self._products_to_quantity = dict()
        self.__pending_products_to_quantity = dict()
        self.__pending_price = 0
        self.__shopping_bag_handler = ShoppingBagHandler.get_instance()

    def parse(self):
        products_ids_to_quantities = {}
        self_prods_to_quantites = (
            self._products_to_quantity
            if self._products_to_quantity != {}
            else self.__pending_products_to_quantity
        )
        for product_id in self_prods_to_quantites:
            products_ids_to_quantities[product_id] = self_prods_to_quantites[product_id][1]
        return ShoppingBagData(
            self.__store.get_id(), self.__store.get_name(), products_ids_to_quantities
        )

    """checks need to be made:
       ----------------------
       1. quantity is a positive number
       2. product with product_id exists in store with specified quantity 
       3. product with product_id doesn't already exist in the bag """

    def get_store(self):
        return self.__store

    def get_products_to_quantity(self):
        return self._products_to_quantity

    def set_products(self, products_to_quantities: dict[str, tuple[Product, int]]):
        self._products_to_quantity = products_to_quantities

    def get_pending_products_to_quantity(self):
        return self.__pending_products_to_quantity

    def get_pending_price(self):
        return self.__pending_price

    def add_product(self, product_id: str, quantity: int, user_name: str = None) -> Response[None]:
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
            return self.change_product_quantity(product_id=product_id, new_amount=self._products_to_quantity[product_id][1] + quantity)
            # return Response(
            #     False, msg=f"A product with id: {product_id} already exists in the store's bag"
            # )

        if user_name is not None:
            self.__shopping_bag_handler.add_product_to_bag(self.get_store(), self.__store.get_product(product_id), user_name, quantity)
            res = self.__shopping_bag_handler.commit_changes()
            if not res.succeeded():
                return db_fail_response

        self._products_to_quantity.update(
            {product_id: (self.__store.get_product(product_id), quantity)}
        )
        return Response(True, msg=f"The product with id: {product_id} added successfully!")

    """checks need to be made:
       ----------------------
       1. product with product_id exists in bag 
                                            """

    def remove_product(self, product_id: str, user_name: str = None) -> Response[None]:

        if self._products_to_quantity.get(product_id) is None:
            return Response(
                False, msg=f"No such product in the bag of ths store{self.__store.get_name()}"
            )
        else:
            if user_name is not None:
                self.__shopping_bag_handler.remove_product_from_bag(self.get_store(), product_id, user_name)
                res = self.__shopping_bag_handler.commit_changes()
                if not res.succeeded():
                    return db_fail_response
            self._products_to_quantity.pop(product_id)
        return Response(True, msg="Successfully removed product with id: " + str(product_id))

    def get_product_from_bag(self, product_id, username):
        product = self.__store.get_product(product_id)
        if product is None:
            self.remove_product(product_id, None if username == "Guest" else username)
            return Response(True, None)
        return Response(True, self._products_to_quantity[product_id][0].parse_with_price(username))

    """checks need to be made:
       ----------------------
       1. check if products exist in the store with specified quantities
       2. check if purchase types are appropriate
                                            """

    # product info - list of tuples (product_id to purchase_type)
    def buy_products(
        self, user_age: int, products_info=None, username="Guest"
    ) -> Response[PrimitiveParsable[float]]:

        """first step - check if all of the products exist in the store and acquire"""
        if products_info is None:
            products_info = {}
        availability_response = self.__store.check_and_acquire_available_products(self._products_to_quantity)
        if not availability_response.success:
            return availability_response

        """second step - check if the purchase_types are appropriate"""
        # since there are no purchase types for now- this checking isn't relevant
        purchase_policy_check = self.purchase_types_checks(user_age, self._products_to_quantity)
        if not purchase_policy_check.succeeded():
            return purchase_policy_check

        """third step - check and apply the discount """
        self.discount_apply(user_age, username)
        return Response[PrimitiveParsable[float]](
            True,
            PrimitiveParsable(self.__pending_price),
            msg="All the details are good! here comes the price",
        )

    def purchase_types_checks(self, user_age: int, products_info=None):
        if products_info is None:
            products_info = {}
        purchase_types_check = self.__store.check_purchase(products_info, user_age)
        if not purchase_types_check.success:
            self.__store.send_back(self._products_to_quantity)
            return purchase_types_check

        return Response(True, msg="The cart passed the purchase policy check!")

    def discount_apply(self, user_age: int, username="Guest"):
        self.__pending_price = self.__store.apply_discounts(
            self._products_to_quantity, user_age, username
        )
        self.__pending_products_to_quantity = self._products_to_quantity.copy()
        self._products_to_quantity.clear()

    """checks need to be made:
       ----------------------
       1. new_amount is a positive number
       2. product with product_id exists in the bag 
                                                """

    def change_product_quantity(self, product_id: str, new_amount: int, user_name=None) -> Response[None]:
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")
        if self._products_to_quantity.get(product_id) is None:
            return Response(False, msg="No such product in the bag")
        if not self.__store.has_enough(product_id, new_amount):
            return Response(
                False,
                msg="A product with id: " + str(product_id) + " no in inventory enough",
            )
        if user_name is not None:
            self.__shopping_bag_handler.change_product_quantity_in_bag(self.get_store(), product_id, user_name, new_amount)
            res = self.__shopping_bag_handler.commit_changes()
            if not res.succeeded():
                return db_fail_response

        self._products_to_quantity[product_id] = (
            self._products_to_quantity.get(product_id)[0],
            new_amount,
        )
        return Response(True, msg="amount changed successfully")

    def create_purchase_details_after_purchase(self, user_name="guest"):
        product_names = [prod.get_name() for product_id, (prod, quantity) in
                         self.__pending_products_to_quantity.items()]
        purchase_details = PurchaseDetails(user_name, self.__store.get_name(), self.__store.get_id(), product_names,
                                           datetime.now(),
                                           self.__pending_price)
        if user_name != "guest":
            res = PurchaseDetailsHandler.get_instance().save(purchase_details)
            if not res.succeeded():
                return None
        return purchase_details

    def delete_products_after_purchase(self, purchase_details,  user_name="guest"):
        # for now this function will only return details, in the future there will be specific deletion
        product_ids = [product_id for product_id in self.__pending_products_to_quantity]
        founder_res = self.__store.get_founder()
        self.__store.clear_offers(product_ids, user_name)
        self.__store.update_store_history(purchase_details)
        founder_res.get_obj().get_user_state()
        self.__pending_products_to_quantity.clear()


    def send_back(self):
        self._products_to_quantity = self.__pending_products_to_quantity.copy()
        self.__pending_products_to_quantity.clear()
        self.__store.send_back(products_to_quantities=self._products_to_quantity)

    def get_store_ID(self) -> str:
        return self.__store.get_id()

