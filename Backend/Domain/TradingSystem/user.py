from __future__ import annotations
import threading
from typing import Callable

from Backend.response import Response, ParsableList, PrimitiveParsable

from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.Interfaces.IUserState import IUserState
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.States.user_state import UserState
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission, Responsibility


class User(IUser):
    def __init__(self):
        self.state: UserState = IUserState.create_guest(self)
        self.appointment_lock = threading.Lock()
        self.__notifications: list[str] = []
        self.__communicate: Callable[[list[str]], bool] = lambda msgs: False

    def __notify_self(self) -> bool:
        answer = self.__communicate(self.__notifications)
        if answer:
            self.__notifications = []
        return answer

    def get_communicate(self) -> Callable[[list[str]], bool]:
        return self.__communicate

    def connect(self, communicate: Callable[[list[str]], bool]) -> bool:
        self.__communicate = communicate
        return self.__notify_self()  # if the user has connected

    # 2.3
    def register(self, username: str, password: str) -> Response[None]:
        return self.state.register(username, password)

    # 2.4
    def login(self, username: str, password: str) -> Response[None]:
        return self.state.login(username, password)

    # 2.7
    def add_to_cart(self, store_id: str, product_id: str, quantity: int) -> Response[None]:
        return self.state.save_product_in_cart(store_id, product_id, quantity)

    # 2.8
    def get_cart_details(self) -> Response[ShoppingCart]:
        return self.state.show_cart()

    # 2.8
    def remove_product_from_cart(self, store_id: str, product_id: str) -> Response[None]:
        return self.state.delete_from_cart(store_id, product_id)

    # 2.8
    def change_product_quantity_in_cart(
        self, store_id: str, product_id: str, new_amount: int
    ) -> Response[None]:
        return self.state.change_product_quantity_in_cart(store_id, product_id, new_amount)

    def get_discounted_current_cart_price(self):
        return self.state.get_discounted_current_cart_price()

    # 2.9
    def purchase_cart(self, user_age: int) -> Response[PrimitiveParsable[float]]:
        return self.state.buy_cart(user_age)

    # 2.9
    def purchase_completed(self) -> Response[None]:
        return self.state.delete_products_after_purchase()

    # 2.9
    def get_cart_price(self) -> Response[PrimitiveParsable[float]]:
        return self.state.get_cart_price()

    # 2.9
    def lock_cart(self):
        return self.state.lock_cart()

    # 2.9
    def release_cart(self):
        return self.state.release_cart()

    # 2.9
    def cancel_purchase(self):
        return self.state.cancel_purchase()

    # Member
    # ===============================

    # 3.2
    def create_store(self, name: str) -> Response[Store]:
        return self.state.open_store(name)

    # 3.7
    def get_purchase_history(self) -> Response[ParsableList[PurchaseDetails]]:
        return self.state.get_purchase_history()

    # Owner and manager
    # =======================

    # 4.1
    # Creating a new product a the store and setting its quantity to 0
    def create_product(
        self,
        store_id: str,
        name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str] = None,
    ) -> Response[str]:
        return self.state.add_new_product(store_id, name, category, price, quantity, keywords)

    # 4.1
    def remove_product_from_store(
        self, store_id: str, product_id: str
    ) -> Response[PrimitiveParsable[int]]:
        return self.state.remove_product(store_id, product_id)

    # 4.1
    def change_product_quantity_in_store(
        self, store_id: str, product_id: str, new_quantity: int
    ) -> Response[None]:
        return self.state.change_product_quantity_in_store(store_id, product_id, new_quantity)

    # 4.1
    def edit_product_details(
        self,
        store_id: str,
        product_id: str,
        new_name: str,
        new_category: str,
        new_price: float,
        keywords: list[str] = None,
    ) -> Response[None]:
        return self.state.edit_product_details(
            store_id, product_id, new_name, new_category, new_price, keywords
        )

    # 4.2
    def add_discount(self, store_id: str, discount_data: dict, exist_id: str):
        return self.state.add_discount(store_id, discount_data, exist_id)

    def move_discount(self, store_id: str, src_id: str, dest_id: str):
        return self.state.move_discount(store_id, src_id, dest_id)

    def get_discounts(self, store_id: str):
        return self.state.get_discounts(store_id)

    def remove_discount(self, store_id: str, discount_id: str):
        return self.state.remove_discount(store_id, discount_id)

    def edit_simple_discount(
        self,
        store_id: str,
        discount_id: str,
        percentage: float = None,
        condition: dict = None,
        context: dict = None,
        duration=None,
    ):
        return self.state.edit_simple_discount(
            store_id, discount_id, percentage, condition, context, duration
        )

    def edit_complex_discount(
        self, store_id: str, discount_id: str, complex_type: str = None, decision_rule: str = None
    ):
        return self.state.edit_complex_discount(discount_id, complex_type, decision_rule)

    # 4.2
    def add_purchase_rule(
        self, store_id: str, rule_details: dict, rule_type: str, parent_id: str, clause: str = None
    ):
        return self.state.add_purchase_rule(rule_details, rule_type, parent_id, clause)

    # 4.2
    def remove_purchase_rule(self, store_id: str, rule_id: str):
        return self.state.remove_purchase_rule(store_id, rule_id)

    # 4.2
    def edit_purchase_rule(self, store_id: str, rule_details: dict, rule_id: str, rule_type: str):
        return self.state.edit_purchase_rule(store_id, rule_details, rule_id, rule_type)

    # 4.2
    def move_purchase_rule(self, store_id: str, rule_id: str, new_parent_id: str):
        return self.state.move_purchase_rule(store_id, rule_id, new_parent_id)

    # 4.2
    def get_purchase_policy(self, store_id: str):
        return self.state.get_purchase_policy(store_id)

    # 4.3
    def appoint_owner(self, store_id: str, user: IUser) -> Response[None]:
        return self.state.appoint_new_store_owner(store_id, user)

    # 4.5
    def appoint_manager(self, store_id: str, user: IUser) -> Response[None]:
        return self.state.appoint_new_store_manager(store_id, user)

    # 4.6
    def add_manager_permission(
        self, store_id: str, username: str, permission: Permission
    ) -> Response[None]:
        return self.state.add_manager_permission(store_id, username, permission)

    # 4.6
    def remove_manager_permission(
        self, store_id: str, username: str, permission: Permission
    ) -> Response[None]:
        return self.state.remove_manager_permission(store_id, username, permission)

    # 4.4, 4.7
    def remove_appointment(self, store_id: str, username: str) -> Response[None]:
        return self.state.remove_appointment(store_id, username)

    # 4.9
    def get_store_appointments(self, store_id: str) -> Response[Responsibility]:
        return self.state.get_store_personnel_info(store_id)

    def get_my_appointments(self) -> Response[ParsableList[Responsibility]]:
        return self.state.get_my_appointments()

    # 4.11
    def get_store_purchase_history(self, store_id: str) -> Response[ParsableList[PurchaseDetails]]:
        return self.state.get_store_purchase_history(store_id)

    # System Manager
    # ====================

    # 6.4
    def get_any_user_purchase_history_admin(
        self, username: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        return self.state.get_user_purchase_history_admin(username)

    # 6.4
    def get_any_store_purchase_history_admin(
        self, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        return self.state.get_any_store_purchase_history_admin(store_id)

    # Inter component functions
    # ====================

    def is_appointed(self, store_id: str) -> Response[bool]:
        return self.state.is_appointed(store_id)

    def get_username(self) -> Response[PrimitiveParsable[str]]:
        return self.state.get_username()

    def change_state(self, new_state: UserState) -> None:
        self.state = new_state

    def get_appointment_lock(self) -> threading.Lock():
        return self.appointment_lock

    def empty_notifications(self):
        return len(self.__notifications) == 0

    def notify(self, message: str) -> bool:
        self.__notifications.append(message)
        return self.__notify_self()
