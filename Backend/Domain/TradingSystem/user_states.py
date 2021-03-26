from abc import ABC, abstractmethod
from Backend.Domain.Authentication.authentication import Authentication
from Backend.Domain.TradingSystem.responsibility import Responsibility
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.store import Store
from Backend.response import Response, ParsableList
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from typing import List


# TODO: Change return types to Response

class UserState(ABC):

    def __init__(self, user):
        self.cart = ShoppingCart()
        self.user = user

    @abstractmethod
    def login(self, username, password):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def register(self, username, password):
        return Response(False, msg="Abstract Method")

    def save_product_in_cart(self, store_id, product_id, quantity):
        return self.cart.add_product(store_id, product_id, quantity)

    def show_cart(self):
        return self.cart.show_cart()

    def delete_from_cart(self, store_id, product_id):
        return self.cart.remove_product(store_id, product_id)

    def change_product_quantity(self, store_id, product_id, new_amount):
        return self.cart.change_product_qunatity(store_id, product_id, new_amount)

    def buy_cart(self, product_purchase_info, current_user):
        return self.cart.buy_products(product_purchase_info, current_user)

    def delete_products_after_purchase(self):
        return self.cart.delete_pruducts_after_purchase()

    @abstractmethod
    def open_store(self, store_id, store_parameters):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def get_purchase_history(self):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def add_new_product(self, store_id, product_information,
                        quantity):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def remove_product(self, store_id, product_id):
        return Response(False, msg="Abstract Method")

    @abstractmethod
    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
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


class Guest(UserState):

    def __init__(self, user):
        super().__init__(user)
        self.authentication = Authentication.get_instance()

    def login(self, username, password):
        response = self.authentication.login(username, password)
        if response.success:
            self.user.change_state(Member(username))  # in later milestones, fetch data from DB
        # TODO: need to induce if an admin was logged in - ask Sunshine
        return response

    def register(self, username, password):
        return self.authentication.register(username, password)

    def open_store(self, store_id, store_parameters):
        return Response(False, msg="A store cannot be opened by a guest")

    def get_purchase_history(self):
        return Response(False, msg="Guests don't have purchase history")

    def add_new_product(self, store_id, product_information, quantity):
        return Response(False, msg="Guests cannot add products to stores")

    def remove_product(self, store_id, product_id):
        return Response(False, msg="Guests cannot remove products from stores")

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        return Response(False, msg="Guests cannot change store product's quantity")

    def set_product_price(self, store_id, product_id, new_price):
        return Response(False, msg="Guests cannot edit store product's details")

    def appoint_new_store_owner(self, store_id, new_owner):
        return Response(False, msg="Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager):
        return Response(False, msg="Guests cannot appoint new store managers")

    def add_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Guests cannot edit a stores manager's responsibilities")

    def remove_manager_permission(self, store_id, username, permission):
        return Response(False, msg="Guests cannot edit a stores manager's responsibilities")

    def dismiss_manager(self, store_id, manager):
        return Response(False, msg="Guests cannot dismiss managers")

    def get_store_personnel_info(self, store_id):
        return Response(False, msg="Guests cannot get store personnel information")

    def get_store_purchase_history(self, store_id):
        return Response(False, msg="Guests cannot get store's purchase history")

    def get_any_store_purchase_history(self, store_id):
        return Response(False, msg="Guests cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        return Response(False, msg="Guests cannot get any user's purchase history")


class Member(UserState):

    def __init__(self, user, username, responsibilities=None, purchase_details=[]):  # for DB initialization
        super().__init__(user)
        if responsibilities is None:
            responsibilities = dict()
        self.username = username
        self.responsibilities = responsibilities
        self.purchase_details = purchase_details
        # get cart data from DB

    def login(self, username, password):
        return Response(False, msg="Members cannot re-login")

    def register(self, username, password):
        return Response(False, msg="Members cannot re-register")

    def save_product_in_cart(self, store_id, product_id, quantity):
        response = super().save_product_in_cart(store_id, product_id, quantity)
        # update data in DB in later milestones
        return response

    def delete_from_cart(self, store_id, product_id):
        response = super().delete_from_cart(store_id, product_id)
        # update data in DB in later milestones
        return response

    def change_product_quantity(self, store_id, product_id, new_quantity):
        response = super().change_product_quantity(store_id, product_id, new_quantity)
        # update data in DB in later milestones
        return response

    def buy_cart(self, user, product_purchase_info):
        response = super().buy_cart(user, product_purchase_info)
        # update data in DB in later milestones
        return response

    def delete_products_after_purchase(self):
        response = super().delete_products_after_purchase()
        # update data in DB in later milestones
        self.purchase_details.append(response.object)
        return response

    def open_store(self, store_id, store_parameters):
        if store_id in self.responsibilities:
            return Response(False, msg="Store cannot be re-opened")
        store = Store(store_id, store_parameters)
        self.responsibilities[store_id] = Responsibility(self,
                                                         store)
        return Response[store](True, obj=store, msg="Store opened successfully")

    def get_purchase_history(self):
        return Response[List[PurchaseDetails]](True, obj=ParsableList(self.purchase_details), msg="Purchase history "
                                                                                                  "got successfully")

    def add_new_product(self, store_id, product_id, quantity):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].add_product(product_id, quantity)

    def remove_product(self, store_id, product_id):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_product(product_id)

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].change_product_quantity(product_id, new_quantity)

    def set_product_price(self, store_id, product_id,
                          new_price):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].set_product_price(product_id, new_price)

    def appoint_new_store_owner(self, store_id, new_owner):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].appoint_owner(new_owner)

    def appoint_new_store_manager(self, store_id, new_manager):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].appoint_manager(new_manager)

    def add_manager_permission(self, store_id, username, permission):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].add_manager_permission(username, permission)

    def remove_manager_permission(self, store_id, username, permission):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_manager_permission(username, permission)

    def dismiss_manager(self, store_id, manager):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].remove_appointment(manager)

    def get_store_personnel_info(self, store_id):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].get_store_appointments()

    def get_store_purchase_history(self, store_id):
        if store_id not in self.responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.responsibilities[store_id].get_store_purchases_history()

    def get_any_store_purchase_history(self, store_id):
        return Response(False, msg="Members cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        return Response(False, msg="Members cannot get any user's purchase history")


class Admin(Member):

    def __init__(self, user, username, responsibilities=None):
        super().__init__(user, username, responsibilities)
        self.trading_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        return self.trading_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        return self.trading_system_manager.get_user_purchase_history(user_id)
