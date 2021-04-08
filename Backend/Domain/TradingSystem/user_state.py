from abc import ABC, abstractmethod
import Backend.Domain.TradingSystem.shopping_cart
from Backend.response import Response


class UserState(ABC):

    def __init__(self, user):
        self.cart = Backend.ShoppingCart()
        self.user = user

    @abstractmethod
    def get_username(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def login(self, username, password):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def register(self, username, password):
        return Response(False, msg="Abstract Method")

    def save_product_in_cart(self, store_id, product_id, quantity):
        return self.cart.add_product(store_id, product_id, quantity)

    def show_cart(self):
        return Response[ShoppingCart](True, obj=self.cart, msg="got cart successfully")

    def delete_from_cart(self, store_id, product_id):
        return self.cart.remove_product(store_id, product_id)

    def change_product_quantity(self, store_id, product_id, new_amount):
        return self.cart.change_product_qunatity(store_id, product_id, new_amount)

    def buy_cart(self, current_user):
        return self.cart.buy_products(current_user)

    def delete_products_after_purchase(self):
        return self.cart.delete_pruducts_after_purchase()

    @abstractmethod
    def open_store(self, store_name):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_purchase_history(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_new_product(self, store_id, product_name, product_price,
                        quantity):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_product(self, store_id, product_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def set_product_name(self, store_id, product_id,
                         new_name):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def set_product_price(self, store_id, product_id,
                          new_price):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def appoint_new_store_owner(self, store_id, new_owner):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def appoint_new_store_manager(self, store_id, new_manager):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def dismiss_manager(self, store_id, manager):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_personnel_info(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_store_purchase_history(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_any_store_purchase_history(self, store_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_user_purchase_history(self, user_id):
        return Response(False, msg="Abstract Method")
