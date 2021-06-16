from Backend.Domain.TradingSystem.statistics import Statistics
from Backend.Service.DataObjects.statistics_data import StatisticsData
import threading

from Backend.DataBase.database import db_fail_response
from Backend.Domain.TradingSystem.offer import Offer
from typing import Callable
import uuid
import json

from Backend.DataBase.Handlers.member_handler import MemberHandler
from Backend.Domain.TradingSystem.States.member import Member
from Backend.response import Response, ParsableList, PrimitiveParsable
from Backend.Domain.TradingSystem.Interfaces.IUser import IUser
from Backend.Domain.TradingSystem.store import Store
from Backend.Domain.TradingSystem.shopping_cart import ShoppingCart
from Backend.Domain.TradingSystem.purchase_details import PurchaseDetails
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Permission, Responsibility
from Backend.Domain.TradingSystem.user import User
from Backend.settings import Settings


class UserManager:
    _cookie_user: dict[str, IUser] = {}
    _username_user: dict[str, User] = {}

    @staticmethod
    def __deligate_to_user(cookie, func):
        user = UserManager.__get_user_by_cookie(cookie)
        if not user:
            return Response(False, msg="No user is identified by the given cookie")
        return func(user)

    @staticmethod
    def __get_user_by_cookie(cookie) -> IUser or None:
        if cookie not in UserManager._cookie_user:
            return None
        return UserManager._cookie_user[cookie]

    @staticmethod
    def _get_user_by_username(username, store_id=None) -> IUser or None:
        if username not in UserManager._username_user:
            user_res = MemberHandler.get_instance().load(username)
            if not user_res.succeeded():
                return None
            member = user_res.get_obj()
            member.load_cart()
            user = IUser.create_user()
            user.change_state(member)
            member.set_user(user)
            member._responsibilities = dict()
            if store_id is not None:
                member.get_responsibility(store_id)
            member.notifications_lock = threading.Lock()
            member._member_handler = MemberHandler.get_instance()
            UserManager._username_user[username] = user
        return UserManager._username_user[username]

    @staticmethod
    def _add_user_to_username(username, user):
        UserManager._username_user[username] = user

    @staticmethod
    def __create_cookie() -> str:
        return str(uuid.uuid4())

    # 2.1
    # returns the guest newly created cookie
    @staticmethod
    def enter_system(register=True) -> str:
        cookie = UserManager.__create_cookie()
        UserManager._cookie_user[cookie] = IUser.create_user()
        if register:
            UserManager._cookie_user[cookie].register_statistics()
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
                newUser = IUser.create_user()
                newUser.change_state(response.get_obj())
                UserManager._username_user[username] = newUser
            return response

        return UserManager.__deligate_to_user(cookie, func)

    # 2.4
    @staticmethod
    def login(username: str, password: str, cookie: str) -> Response[None]:
        def func(user: User):
            response = user.login(username, password)

            # If response succeeded we want to connect the cookie to the username
            if response.succeeded():
                for old_username in UserManager._username_user:
                    if old_username == username:
                        old_user = UserManager._username_user[old_username]
                        UserManager._cookie_user[cookie] = old_user
                        old_user.connect(user.get_communicate())
                        return response
                member_res = MemberHandler.get_instance().load(username)
                if not member_res.succeeded():
                    return member_res
                member = member_res.get_obj()
                res = member.load_cart()
                if res.succeeded():
                    member._responsibilities = dict()
                    member.notifications_lock = threading.Lock()
                    member._member_handler = MemberHandler.get_instance()
                    res_commit = MemberHandler.get_instance().commit_changes()
                    if res_commit.succeeded():
                        member.set_user(user)
                        user.change_state(member)
                        UserManager._username_user[username] = user
                    return res_commit
                return res

                # for user_cookie in UserManager.__cookie_user:
                #     old_user = UserManager.__cookie_user[user_cookie]
                #     response_username = old_user.get_username()
                #     if (
                #         response_username.succeeded()i
                #         and response_username.get_obj().get_val() == username
                #     ):
                #         UserManager.__cookie_user[cookie] = old_user
                #         old_user.connect(user.get_communicate())
            # *This action will delete the current cart but will restore the old one and other user details
            UserManager._cookie_user[cookie].register_statistics()
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

    @staticmethod
    def get_product_from_bag(cookie, store_id, product_id, username):
        func: Callable[[User], Response] = lambda user: user.get_product_from_bag(
            store_id, product_id, username
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
        to_appoint = UserManager._get_user_by_username(username, store_id)
        if not to_appoint:
            return Response(False, msg="Given username does not exists")
        func: Callable[[User], Response] = lambda user: user.appoint_owner(store_id, to_appoint)
        return UserManager.__deligate_to_user(cookie, func)

    # 4.5
    @staticmethod
    def appoint_manager(cookie: str, store_id: str, username: str) -> Response[None]:
        to_appoint = UserManager._get_user_by_username(username, store_id)
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
        user = UserManager._get_user_by_username(username)
        if not user:
            return Response(False, msg="Given username does not exists")
        return user.get_purchase_history()

    # For test purposes
    # =====================
    @staticmethod
    def _get_cookie_user():
        return UserManager._cookie_user

    @staticmethod
    def _get_username_user():
        return UserManager._username_user

    @staticmethod
    def get_user_received_notifications(cookie: str) -> Response[ParsableList[PurchaseDetails]]:
        func: Callable[[User], Response] = lambda user: user.get_user_received_notifications()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def empty_notifications(cookie):
        func: Callable[[User], bool] = lambda user: user.empty_notifications()
        return UserManager.__deligate_to_user(cookie, func)

    # Offers
    # ==================

    @staticmethod
    def get_user_offers(cookie) -> Response[ParsableList[Offer]]:
        func: Callable[[User], Response] = lambda user: user.get_user_offers()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def get_store_offers(cookie, store_id) -> Response[ParsableList[Offer]]:
        func: Callable[[User], Response] = lambda user: user.get_store_offers(store_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def create_offer(cookie, store_id, product_id) -> Response[str]:
        func: Callable[[User], Response] = lambda user: user.create_offer(store_id, product_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def declare_price(cookie, offer_id, price) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.declare_price(offer_id, price)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def suggest_counter_offer(cookie, store_id, product_id, offer_id, price) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.suggest_counter_offer(
            store_id, product_id, offer_id, price
        )
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def approve_manager_offer(cookie, offer_id) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.approve_manager_offer(offer_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def approve_user_offer(cookie, store_id, product_id, offer_id) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.approve_user_offer(
            store_id, product_id, offer_id
        )
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def reject_user_offer(cookie, store_id, product_id, offer_id) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.reject_user_offer(
            store_id, product_id, offer_id
        )
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def cancel_offer(cookie, offer_id) -> Response[None]:
        func: Callable[[User], Response] = lambda user: user.cancel_offer(offer_id)
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def get_users_statistics(cookie) -> Response[StatisticsData]:
        func: Callable[[User], Response] = lambda user: user.get_users_statistics()
        return UserManager.__deligate_to_user(cookie, func)

    @staticmethod
    def get_member(res_id):
        for user in UserManager._username_user.values():
            if user.state.has_res_id(res_id):
                return Response(True, obj=user.state)

        member_res = MemberHandler.get_instance().load_user_with_res(res_id)
        if member_res.succeeded():
            member_res.get_obj().load_cart()
            user = IUser.create_user()
            user.change_state(member_res.get_obj())
            member_res.get_obj().set_user(user)
            UserManager._username_user[member_res.get_obj().get_username().get_obj().get_val()] = user
            return member_res

        return db_fail_response


def register_admins() -> None:
    settings = Settings.get_instance(False)
    admins = settings.get_admins()
    if len(admins) <= 0:
        raise Exception(
            "At least one admin should be at the system. Check config.json to add admins."
        )
    for admin in admins:
        cookie = UserManager.enter_system(False)
        UserManager.register(admin, settings.get_password(), cookie)
        Statistics.getInstance().subscribe(UserManager._get_user_by_username(admin))
