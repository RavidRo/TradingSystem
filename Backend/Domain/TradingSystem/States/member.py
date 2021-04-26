from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.States.user_state import UserState
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails

from .user_state import UserState


class Member(UserState):
    def get_username(self):
        return Response(True, obj=PrimitiveParsable(self._username), msg="got username successfully")

    def add_responsibility(self, responsibility, store_id):
        self.__responsibilities[store_id] = responsibility

    def get_purchase_details(self):
        return self.__purchase_details

    def get_responsibilities(self):
        return self.__responsibilities

    def __init__(
        self, user, username, responsibilities=None, purchase_details=None, cart=None
    ):  # for DB
        # initialization
        super().__init__(user, cart)
        if purchase_details is None:
            purchase_details = []
        if responsibilities is None:
            responsibilities = dict()
        self._username = username
        self.__responsibilities = responsibilities
        self.__purchase_details = purchase_details
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

    def change_product_quantity_in_cart(self, store_id, product_id, new_quantity):
        response = super().change_product_quantity_in_cart(store_id, product_id, new_quantity)
        # update data in DB in later milestones
        return response

    def buy_cart(self, current_user):
        response = super().buy_cart(current_user)
        # update data in DB in later milestones
        return response

    def delete_products_after_purchase(self):
        response = self._cart.delete_products_after_purchase(self._username)
        # update data in DB in later milestones
        self.__purchase_details += response.object.values
        return response

    def open_store(self, store_name):
        store = Store(store_name)
        store.set_responsibility(Founder(self, store))
        return Response[Store](True, obj=store, msg="Store opened successfully")

    def get_purchase_history(self):
        return Response[ParsableList[PurchaseDetails]](
            True,
            obj=ParsableList(self.__purchase_details),
            msg="Purchase history " "got successfully",
        )

    def add_new_product(self, store_id, product_name, category, product_price, quantity):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].add_product(product_name, category, product_price, quantity)

    def remove_product(self, store_id, product_id):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].remove_product(product_id)

    def change_product_quantity_in_store(self, store_id, product_id, new_quantity):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].change_product_quantity_in_store(
            product_id, new_quantity
        )

    def edit_product_details(self, store_id, product_id, new_name, new_category, new_price):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].edit_product_details(product_id, new_name, new_category, new_price)

    def appoint_new_store_owner(self, store_id, new_owner):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].appoint_owner(new_owner)

    def dismiss_from_store(self, store_id):
        self.__responsibilities.pop(store_id)

    def appoint_new_store_manager(self, store_id, new_manager):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].appoint_manager(new_manager)

    def add_manager_permission(self, store_id, username, permission):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].add_manager_permission(username, permission)

    def remove_manager_permission(self, store_id, username, permission):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].remove_manager_permission(username, permission)

    def remove_appointment(self, store_id, username):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].remove_appointment(username)

    def get_store_personnel_info(self, store_id):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].get_store_appointments()

    def get_store_purchase_history(self, store_id):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].get_store_purchase_history()

    def get_any_store_purchase_history_admin(self, store_id):
        return Response(False, msg="Regular members cannot get any store's purchase history")

    def get_user_purchase_history_admin(self, username):
        return Response(False, msg="Regular members cannot get any user's purchase history")

    def is_appointed(self, store_id):
        return Response(True, store_id in self.__responsibilities)
