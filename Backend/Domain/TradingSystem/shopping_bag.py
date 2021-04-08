from dataclasses import dataclass
from Backend.Domain.TradingSystem.Interfaces.IShoppingBag import IShoppingBag
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.response import Response, PrimitiveParsable
from datetime import datetime


class ShoppingBag(IShoppingBag):
    from Backend.Domain.TradingSystem.store import Store

    def __init__(self, store: Store):
        self.store = store
        self.products_to_quantity = dict()
        self.pending_products_to_quantity = dict()
        self.pending_price = 0

    def parse(self):
        products_names_to_quantities = []
        for product_id, quantity in self.products_to_quantity:
            product_name = self.store.get_product_name(product_id)
            products_names_to_quantities.append((product_name, quantity))
        return ShoppingBagDataObject(self.store.get_name(), products_names_to_quantities)

    """checks need to be made:
       ----------------------
       1. quantity is a positive number
       2. product with product_id exists in store with specified quantity 
       3. product with product_id doesn't already exist in the bag """
    def add_product(self, product_id: str, quantity: int) -> Response[None]:

        if quantity <= 0:
            return Response(False, msg="quantity must be a positive number!")

        if not self.store.product_exists(product_id, quantity):
            return Response(False, msg="A product with id: " + str(product_id) + " doesn't exist in store's inventory")

        if self.products_to_quantity.get(product_id) is not None:
            return Response(False, msg=f"A product with id: {product_id} already exists in the store's bag")

        self.products_to_quantity.update({product_id: (self.store.get_product(product_id), quantity)})
        return Response(True, msg=f"The product with id: {product_id} added successfully!")

    """checks need to be made:
       ----------------------
       1. product with product_id exists in bag 
                                            """
    def remove_product(self, product_id: str) -> Response[None]:

        if self.products_to_quantity.get(product_id) is None:
            return Response(False, msg=f"No such product in the bag of ths store{self.store.get_name()}")
        else:
            self.products_to_quantity.pop(product_id)
        return Response(True, msg="Successfully removed product with id: " + str(product_id))

    """checks need to be made:
       ----------------------
       1. check if products exist in the store with specified quantities
       2. check if purchase types are appropriate
                                            """
    # product info - list of tuples (product_id to purchase_type)
    def buy_products(self, user_info, products_info={}) -> Response[None]:

        """first step - check if all of the products exist in the store"""
        availability_response = self.store.check_available_products(self.products_to_quantity)
        if not availability_response.success:
            return availability_response

        """second step - acquire the products"""
        self.store.acquire_products(self.products_to_quantity)

        """third step - check if the purchase_types are appropriate"""
        # since there are no purchase types for now- this checking isn't relevant
        if products_info:
            self.purchase_types_checks(user_info, products_info)

        """fourth step - check and apply the discount """
        self.discount_apply(user_info)
        return Response[PrimitiveParsable](True, PrimitiveParsable(self.pending_price),
                                           msg="All the details are good! here comes the price")

    def purchase_types_checks(self, user_info, products_info ={}):
        purchase_types_check = self.store.check_purchase_types(products_info, user_info)
        if not purchase_types_check.success:
            self.store.send_back(self.products_to_quantity)
            return purchase_types_check

    def discount_apply(self, user_info):
        self.pending_price = self.store.apply_discounts(user_info, self.products_to_quantity)
        # for now it's a copy- all of the products purchased regularly so they all passed to pending
        if not bool(self.products_to_quantity):
            self.send_back()
        self.pending_products_to_quantity = self.products_to_quantity.copy()
        self.products_to_quantity.clear()

    """checks need to be made:
       ----------------------
       1. new_amount is a positive number
       2. product with product_id exists in the bag 
                                                """
    def change_product_qunatity(self, product_id: str, new_amount: int) -> Response[None]:
        if new_amount <= 0:
            return Response(False, msg="Amount can't be negative!")
        if self.products_to_quantity.get(product_id) is None:
            return Response(False, msg="No such product in the bag")
        self.products_to_quantity[product_id][1] = new_amount
        return Response(True, msg="amount changed successfully")

    def delete_products_after_purchase(self, user_name="guest") -> PurchaseDetails:
        # for now this function will only return details, in the future there will be specific deletion
        product_names = [prod.get_name() for product_id, (prod, quantity) in self.products_to_quantity.items()]
        self.pending_products_to_quantity.clear()
        return PurchaseDetails(user_name, self.store.get_name(), product_names,
                               datetime.now(), self.pending_price)

    def send_back(self):
        self.store.send_back(products_to_quantities=self.pending_products_to_quantity)

    def get_store_ID(self) -> str:
        return self.store.get_id()


@dataclass
class ShoppingBagDataObject:
    store_name: str
    product_names_to_quantities: list
