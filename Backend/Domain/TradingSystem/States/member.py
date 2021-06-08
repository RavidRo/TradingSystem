import threading
from datetime import date
from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.Responsibilities.founder import Founder
from Backend.Domain.TradingSystem.store import Store

# from Backend.Domain.TradingSystem.States.user_state import UserState
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails

from .user_state import UserState


class Member(UserState):
    def get_username(self):
        return Response(
            True, obj=PrimitiveParsable(self._username), msg="got username successfully"
        )

    def add_responsibility(self, responsibility, store_id):
        self.__responsibilities[store_id] = responsibility

    def remove_responsibility(self, store_id):
        del self.__responsibilities[store_id]

    def get_purchase_details(self):
        return self.__purchase_details

    def get_responsibilities(self):
        return self.__responsibilities

    def load_cart(self):
        self._cart = self._member_handler.load_cart(self._username)

    def __init__(
            self, user, username, responsibilities=None, purchase_details=None, cart=None
    ):
        super().__init__(user, cart)
        if purchase_details is None:
            purchase_details = []
        if responsibilities is None:
            responsibilities = dict()
        self._username = username
        self.__responsibilities = responsibilities
        self.__purchase_details = purchase_details
        self.__notifications: list[str] = []
        self.notifications_lock = threading.Lock()

    def login(self, username, password):
        return Response(False, msg="Members cannot re-login")

    def register(self, username, password):
        return Response(False, msg="Members cannot re-register")

    def save_product_in_cart(self, store_id, product_id, quantity):
        response = self._cart.add_product(store_id, product_id, quantity, self._username)
        # update data in DB in later milestones
        return response

    def delete_from_cart(self, store_id, product_id):
        response = self._cart.remove_product(store_id, product_id, self._username)
        # update data in DB in later milestones
        return response

    def change_product_quantity_in_cart(self, store_id, product_id, new_quantity):
        response = self._cart.change_product_quantity(store_id, product_id, new_quantity, self._username)
        # update data in DB in later milestones
        return response

    def buy_cart(self, current_user):
        response = super().buy_cart(current_user)
        # update data in DB in later milestones
        return response

    def delete_products_after_purchase(self):
        response = self._cart.delete_products_after_purchase(self._username)
        if response.succeeded():
            # update data in DB in later milestones
            self.__purchase_details += response.object.values
        return response

    def open_store(self, store_name) -> Response:
        store = Store(store_name)
        store.set_responsibility(Founder(self, store, self._user))
        store.save()
        res = self._member_handler.commit_changes()
        if not res.succeeded():
            self.remove_responsibility(store.get_id())
            return Response(False, msg="DB Error")
        return Response[Store](True, obj=store, msg="Store opened successfully")

    def get_purchase_history(self):
        return Response[ParsableList[PurchaseDetails]](
            True,
            obj=ParsableList(self.__purchase_details),
            msg="Purchase history " "got successfully",
        )

    def add_new_product(
            self, store_id, product_name, category, product_price, quantity, keywords=None
    ):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].add_product(
            product_name, category, product_price, quantity, keywords
        )

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

    def edit_product_details(
            self, store_id, product_id, new_name, new_category, new_price, keywords=None
    ):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].edit_product_details(
            product_id, new_name, new_category, new_price, keywords
        )

    def add_discount(
            self, store_id: str, discount_data: dict, exist_id: str, condition_type: str = None
    ):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].add_discount(
            discount_data, exist_id, condition_type
        )

    def move_discount(self, store_id: str, src_id: str, dest_id: str):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].move_discount(src_id, dest_id)

    def get_discounts(self, store_id: str):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].get_discounts()

    def remove_discount(self, store_id: str, discount_id: str):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].remove_discount(discount_id)

    def edit_simple_discount(
            self,
            store_id: str,
            discount_id: str,
            percentage: float = None,
            context: dict = None,
            duration=None,
    ):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].edit_simple_discount(
            discount_id, percentage, context, duration
        )

    def edit_complex_discount(
            self, store_id: str, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        if store_id not in self.__responsibilities:
            return Response(False, msg=f"this member do not own/manage store {store_id}")
        return self.__responsibilities[store_id].edit_complex_discount(
            discount_id, complex_type, decision_rule
        )

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

    def get_my_appointments(self):
        return Response(True, ParsableList(list(self.__responsibilities.values())))

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

    # 4.2
    def add_purchase_rule(
            self, store_id: str, rule_details: dict, rule_type: str, parent_id: str, clause: str = None
    ):
        return self.__responsibilities[store_id].add_purchase_rule(
            rule_details, rule_type, parent_id, clause
        )

    # 4.2
    def remove_purchase_rule(self, store_id: str, rule_id: str):
        return self.__responsibilities[store_id].remove_purchase_rule(rule_id)

    # 4.2
    def edit_purchase_rule(self, store_id: str, rule_details: dict, rule_id: str, rule_type: str):
        return self.__responsibilities[store_id].edit_purchase_rule(
            rule_details, rule_id, rule_type
        )

    # 4.2
    def move_purchase_rule(self, store_id: str, rule_id: str, new_parent_id: str):
        return self.__responsibilities[store_id].move_purchase_rule(rule_id, new_parent_id)

    # 4.2
    def get_purchase_policy(self, store_id):
        return self.__responsibilities[store_id].get_purchase_policy()

    def add_purchase_rule_history(self, purchase):
        self.__purchase_details.append(purchase)
