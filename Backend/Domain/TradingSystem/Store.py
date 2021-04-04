from Backend.Domain.TradingSystem.DiscountPolicy import DefaultDiscountPolicy
from Backend.Domain.TradingSystem.Interfaces import IPurchaseDetails, IStore
from Backend.Domain.TradingSystem import Product, PurchaseDetails
import uuid
from Backend.Domain.TradingSystem.PurchasePolicy import DefaultPurchasePolicy
from Backend.Domain.TradingSystem.Responsibilities import Responsibility
from Backend.response import Response, ParsableList, Parsable


class Store(IStore, Parsable):

    def __init__(self, store_name: str):
        """Create a new store with it's specified info"""
        self.id = str(self.id_generator())
        self.name = store_name
        self.products_to_quantities = dict()
        self.responsibility = None
        # These fields will be changed in the future versions
        self.discount_policy = DefaultDiscountPolicy()
        self.purchase_policy = DefaultPurchasePolicy()
        self.purchase_history = []

    def parse(self):
        pass

    def show_store_data(self) -> Response:
        # in the future other field will be checked too
        if self.responsibility is None:
            return Response(False, msg="Store's responsibilities aren't set yet")

        return Response[Store](True, self, msg="Store's details are complete")

    def get_name(self) -> str:
        return self.name

    def add_product(self, product_name: str, price: float, quantity: int) -> Response[None]:
        if quantity <= 0:
            # actually it's non-negative but adding 0 amount is redundant
            return Response(False, msg="Product's qunatity must be positive!")

        if price <= 0:
            return Response(False, msg="Product's price must pe positive!")

        if self.check_existing_product(product_name):
            return Response(False, msg="This product is already in the store's inventory")

        product_id = self.id_generator()
        product = Product(product_id, product_name, price)
        self.products_to_quantities.update({product_id, (product, quantity)})
        return Response(True, msg="product" + str(product_name) + "successfully added")

    def remove_product(self, product_id: str) -> Response[None]:
        result = self.products_to_quantities.pop(product_id, None)
        if result is None:
            return Response(False, msg="The product " + str(result[0].get_name()) + " is already not in the inventory!")
        return Response(True, msg="Successfully removed product with product id: " + str(product_id))

    def change_product_quantity(self, product_id: str, quantity: int) -> Response[None]:
        if product_id in self.products_to_quantities:
            self.products_to_quantities[product_id][1] = quantity
            return Response(True, msg="Successfully updated product " +
                                      str(self.products_to_quantities[product_id][0].get_name()) + "'s quantity")
        return Response(False, msg="The product with id: " + str(product_id) + " isn't in the inventory!")

    def edit_product_details(self, product_id: str, product_name: str, price: float) -> Response[None]:
        if product_id in self.products_to_quantities:
            self.products_to_quantities[product_id][0].edit_product_details(product_name, price)
            return Response(True, msg="Succesfully updated product " + self.products_to_quantities[product_id][0].get_name() + "'s details")
        return Response(False, msg="The product with id: " + str(product_id) + " isn't in the inventory!")

    def get_personnel_info(self) -> Response[Responsibility]:
        if self.responsibility is None:
            return Response(False, msg="The store doesn't have assigned personnel")
        return Response[Responsibility](True, self.responsibility, msg="Personnel info")

    def get_purchases_history(self) -> Response[ParsableList[IPurchaseDetails]]:
        return Response[ParsableList](True, ParsableList(self.purchase_history), msg="Purchase history")

    def update_store_history(self, purchase_details: PurchaseDetails):
        self.purchase_history.append(purchase_details)

    def id_generator(self) -> str:
        return uuid.uuid4()

    def get_id(self) -> str:
        return self.id

    def set_responsibility(self, responsibility: Responsibility):
        self.responsibility = responsibility

    def check_existing_product(self, product_name: str):
        for (prod, quantity) in self.products_to_quantities.values():
            if prod.get_name() == product_name:
                return True
        return False

    def send_back(self, products_to_quantities: dict):
        for prod_id, quantity in products_to_quantities.items():
            if self.products_to_quantities.get(prod_id) is None:
                self.products_to_quantities.update({prod_id, quantity})
            else:
                self.products_to_quantities[prod_id,] += quantity

    # This function checks for available products and catches them
    def check_available_products(self, products_ids_to_quantities: dict):
        checked_products = dict()
        for prod_id, quantity in products_ids_to_quantities.items():
            current_quantity = products_ids_to_quantities.get(prod_id)
            if current_quantity is None:
                self.send_back(checked_products)
                return Response(False, msg="The product with id: " + prod_id + "doesn't exist in the inventory of the store")
            elif current_quantity < quantity:
                self.send_back(checked_products)
                return Response(False, msg="The store has less than" + str(quantity) + "of the product with id: " + prod_id + "left")
            else:
                # acquire the product with specified quantity
                if current_quantity == quantity:
                    products_ids_to_quantities.pop(prod_id)
                else:
                    products_ids_to_quantities.update({prod_id, current_quantity - quantity})
                checked_products.update({prod_id, quantity})
        # ask about dict as an object to add here!
        return Response(True, checked_products, msg="All products are available")

    # this will be added in the future - maybe I will apply Default Policy for now
    def check_purchase_types(self, products_info, user_info):
        return Response(True, msg="all purchase types arew available")

