from typing import Callable
import uuid
import json
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission, Responsibility
from Backend.Domain.TradingSystem.user import User


def at_least_one_admin():
    with open("config.json", "r") as read_file:
        data = json.load(read_file)
        if "admins" not in data or len(data["admins"]) <= 0:
            raise Exception(
                "At least one admin should be at the system. Check config.json to add admins."
            )


at_least_one_admin()


class UserManager:
    __cookie_user: dict[str, IUser] = {}
    __username_user: dict[str, IUser] = {}

    @staticmethod
    def __deligate_to_user(cookie, func):
        user = UserManager.__get_user_by_cookie(cookie)
        if not user:
            return Response(False, msg="No user is identified by the given cookie")
        return func(user)

    @staticmethod
    def __get_user_by_cookie(cookie) -> IUser or None:
        if cookie not in UserManager.__cookie_user:
            return None
        return UserManager.__cookie_user[cookie]

    @staticmethod
    def __get_user_by_username(username) -> IUser or None:
        if username not in UserManager.__username_user:
            return None
        return UserManager.__username_user[username]

    @staticmethod
    def __create_cookie() -> str:
        return str(uuid.uuid4())

    # 2.1
    # returns the guest newly created cookie
    @staticmethod
    def enter_system() -> str:
        cookie = UserManager.__create_cookie()
        UserManager.__cookie_user[cookie] = IUser.create_user()
        return cookie

    @staticmethod
    def connect(cookie: str, communicate: Callable[[list[str]], bool]) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.connect(communicate)
        return UserManager.__deligate_to_user(cookie, func)

    # 2.3
    @staticmethod
    def register(username: str, password: str, cookie: str) -> Response[None]:
        def func(user: User):
            response = user.register(username, password)
            if response.succeeded():
                newUser = User()
                newUser.login(username, password)
                UserManager.__username_user[username] = newUser
            return response

        return UserManager.__deligate_to_user(cookie, func)

    # 2.4
    @staticmethod
    def login(username: str, password: str, cookie: str) -> Response[None]:
        def func(user: User):
            response = user.login(username, password)

            # If response succeeded we want to connect the cookie to the username
            if response.succeeded():
                for old_username in UserManager.__username_user:
                    if old_username == username:
                        old_user = UserManager.__username_user[old_username]
                        UserManager.__cookie_user[cookie] = old_user
                        old_user.connect(user.get_communicate())
                # for user_cookie in UserManager.__cookie_user:
                #     old_user = UserManager.__cookie_user[user_cookie]
                #     response_username = old_user.get_username()
                #     if (
                #         response_username.succeeded()
                #         and old_user != user
                #         and response_username.get_obj().get_val() == username
                #     ):
                #         UserManager.__cookie_user[cookie] = old_user
                #         old_user.connect(user.get_communicate())
            # *This action will delete the current cart but will restore the old one and other user details

            return response

        return UserManager.__deligate_to_user(cookie, func)

    # 2.7
    @staticmethod
    def add_to_cart(cookie: str, store_id: str, product_id: str, quantity: int) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.add_to_cart(
            store_id, product_id, quantity
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 2.8
    @staticmethod
    def get_cart_details(cookie: str) -> Response[ShoppingCart]:
        func: Callable[[User], Response] = lambda user: user.get_cart_details()
        return UserManager.__deligate_to_user(cookie, func)

    # 2.8
    @staticmethod
    def remove_product_from_cart(cookie: str, store_id: str, product_id: str) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.remove_product_from_cart(
            store_id, product_id
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 2.8
    @staticmethod
    def change_product_quantity_in_cart(
        cookie: str, store_id, product_id, new_amount
    ) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.change_product_quantity_in_cart(
            store_id, product_id, new_amount
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 2.9
    @staticmethod
    def purchase_cart(cookie: str, user_age: int) -> Response[PrimitiveParsable[float]]:
        func: Callable[[User], Response] = lambda user: user.purchase_cart(user_age)
        return UserManager.__deligate_to_user(cookie, func)

    # 2.9
    @staticmethod
    def purchase_completed(cookie: str) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.purchase_completed()
        return UserManager.__deligate_to_user(cookie, func)

    # 2.9
    @staticmethod
    def get_cart_price(cookie: str) -> Response[PrimitiveParsable[float]]:
        func: Callable[[User], Response] = lambda user: user.get_cart_price()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def lock_cart(cookie):
        func: Callable = lambda user: user.lock_cart()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def release_cart(cookie):
        func: Callable = lambda user: user.release_cart()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def cancel_purchase(cookie):
        func: Callable = lambda user: user.cancel_purchase()
        return UserManager.__deligate_to_user(cookie, func)

    # Member
    # ===============================

    # 3.2
    @staticmethod
    def create_store(cookie: str, name: str) -> Response[Store]:
        func: Callable[[User], Response] = lambda user: user.create_store(name)
        return UserManager.__deligate_to_user(cookie, func)

    # 3.7
    @staticmethod
    def get_purchase_history(cookie: str) -> Response[ParsableList[PurchaseDetails]]:
        func: Callable[[User], Response] = lambda user: user.get_purchase_history()
        return UserManager.__deligate_to_user(cookie, func)

    # Owner and manager
    # =======================

    # 4.1
    # Creating a new product a the store and setting its quantity to 0
    @staticmethod
    def create_product(
        cookie: str,
        store_id: str,
        name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str] = None,
    ) -> Response[str]:
        func: Callable[[User], Response] = lambda user: user.create_product(
            store_id, name, category, price, quantity, keywords
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.1
    @staticmethod
    def remove_product_from_store(
        cookie: str, store_id: str, product_id: str
    ) -> Response[PrimitiveParsable[int]]:
        func: Callable[[User], Response] = lambda user: user.remove_product_from_store(
            store_id, product_id
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.1
    @staticmethod
    def change_product_quantity_in_store(
        cookie: str, store_id: str, product_id: str, quantity: int
    ) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.change_product_quantity_in_store(
            store_id, product_id, quantity
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.1
    @staticmethod
    def edit_product_details(
        cookie: str,
        store_id: str,
        product_id: str,
        new_name: str,
        new_category: str,
        new_price: float,
        keywords: list[str] = None,
    ) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.edit_product_details(
            store_id, product_id, new_name, new_category, new_price, keywords
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.2
    @staticmethod
    def add_discount(
        cookie: str, store_id: str, discount_data: dict, exist_id: str, condition_type: str = None
    ):
        func: Callable[[User], Response] = lambda user: user.add_discount(
            store_id, discount_data, exist_id, condition_type
        )
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def move_discount(cookie: str, store_id: str, src_id: str, dest_id: str):
        func: Callable[[User], Response] = lambda user: user.move_discount(
            store_id,
            src_id,
            dest_id,
        )
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def get_discounts(cookie: str, store_id: str):
        func: Callable[[User], Response] = lambda user: user.get_discounts(store_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def remove_discount(cookie: str, store_id: str, discount_id: str):
        func: Callable[[User], Response] = lambda user: user.remove_discount(store_id, discount_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def edit_simple_discount(
        cookie: str,
        store_id: str,
        discount_id: str,
        percentage: float = None,
        context: dict = None,
        duration=None,
    ):
        func: Callable[[User], Response] = lambda user: user.edit_simple_discount(
            store_id, discount_id, percentage, context, duration
        )
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def edit_complex_discount(
        cookie: str,
        store_id: str,
        discount_id: str,
        complex_type: str = None,
        decision_rule: str = None,
    ):
        func: Callable[[User], Response] = lambda user: user.edit_complex_discount(
            store_id, discount_id, complex_type, decision_rule
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.2
    @staticmethod
    def add_purchase_rule(
        cookie: str,
        store_id: str,
        rule_details: dict,
        rule_type: str,
        parent_id: str,
        clause: str = None,
    ):
        func: Callable[[User], Response] = lambda user: user.add_purchase_rule(
            store_id, rule_details, rule_type, parent_id, clause
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.2
    @staticmethod
    def remove_purchase_rule(cookie: str, store_id: str, rule_id: str):
        func: Callable[[User], Response] = lambda user: user.remove_purchase_rule(store_id, rule_id)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.2
    @staticmethod
    def edit_purchase_rule(
        cookie: str, store_id: str, rule_details: dict, rule_id: str, rule_type: str
    ):
        func: Callable[[User], Response] = lambda user: user.edit_purchase_rule(
            store_id, rule_details, rule_id, rule_type
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.2
    @staticmethod
    def move_purchase_rule(cookie: str, store_id: str, rule_id: str, new_parent_id: str):
        func: Callable[[User], Response] = lambda user: user.move_purchase_rule(
            store_id, rule_id, new_parent_id
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.2
    @staticmethod
    def get_purchase_policy(cookie: str, store_id: str):
        func: Callable[[User], Response] = lambda user: user.get_purchase_policy(store_id)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.3
    @staticmethod
    def appoint_owner(cookie: str, store_id: str, username: str) -> Response[None]:
        to_appoint = UserManager.__get_user_by_username(username)
        if not to_appoint:
            return Response(False, msg="Given username does not exists")
        func: Callable[[User], Response] = lambda user: user.appoint_owner(store_id, to_appoint)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.5
    @staticmethod
    def appoint_manager(cookie: str, store_id: str, username: str) -> Response[None]:
        to_appoint = UserManager.__get_user_by_username(username)
        if not to_appoint:
            return Response(False, msg="Given username does not exists")
        func: Callable[[User], Response] = lambda user: user.appoint_manager(store_id, to_appoint)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.6
    @staticmethod
    def add_manager_permission(
        cookie: str, store_id: str, username: str, permission: Permission
    ) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.add_manager_permission(
            store_id, username, permission
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 4.6
    @staticmethod
    def remove_manager_permission(
        cookie: str, store_id: str, username: str, permission: Permission
    ) -> Response[None]:
        func = lambda user: user.remove_manager_permission(store_id, username, permission)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.4, 4.7
    @staticmethod
    def remove_appointment(cookie: str, store_id: str, username: str) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.remove_appointment(store_id, username)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.9
    @staticmethod
    def get_store_appointments(cookie: str, store_id: str) -> Response[Responsibility]:
        func: Callable[[User], Response] = lambda user: user.get_store_appointments(store_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def get_my_appointments(cookie: str) -> Response[ParsableList[Responsibility]]:
        func: Callable[[User], Response] = lambda user: user.get_my_appointments()
        return UserManager.__deligate_to_user(cookie, func)

    # 4.11
    @staticmethod
    def get_store_purchase_history(
        cookie: str, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        func = lambda user: user.get_store_purchase_history(store_id)
        return UserManager.__deligate_to_user(cookie, func)

    # System Manager
    # ====================

    # 6.4
    @staticmethod
    def get_any_store_purchase_history_admin(
        cookie: str, store_id: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        func: Callable[[User], Response] = lambda user: user.get_any_store_purchase_history_admin(
            store_id
        )
        return UserManager.__deligate_to_user(cookie, func)

    # 6.4
    @staticmethod
    def get_any_user_purchase_history_admin(
        cookie: str, username: str
    ) -> Response[ParsableList[PurchaseDetails]]:
        func: Callable[[User], Response] = lambda user: user.get_any_user_purchase_history_admin(
            username
        )
        return UserManager.__deligate_to_user(cookie, func)

    # Inter component functions
    # ====================

    # 6.4
    @staticmethod
    def get_any_user_purchase_history(username: str) -> Response[ParsableList[PurchaseDetails]]:
        return UserManager.__get_user_by_username(username).get_purchase_history()

    # For test purposes
    # =====================
    @staticmethod
    def _get_cookie_user():
        return UserManager.__cookie_user

    @staticmethod
    def _get_username_user():
        return UserManager.__username_user

    @staticmethod
    def get_user_received_notifications(cookie: str) -> Response[ParsableList[PurchaseDetails]]:
        func: Callable[[User], Response] = lambda user: user.get_user_received_notifications()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def empty_notifications(cookie):
        func: Callable[[User], bool] = lambda user: user.empty_notifications()
        return UserManager.__deligate_to_user(cookie, func)
