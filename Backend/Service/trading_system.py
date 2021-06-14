""" this class is responsible to communicate with the trading __system manager"""
from __future__ import annotations

import json
from typing import Callable
import threading

import sqlalchemy

from Backend.DataBase.Handlers.member_handler import MemberHandler
from Backend.DataBase.Handlers.offer_handler import OfferHandler
from Backend.DataBase.Handlers.product_handler import ProductHandler
from Backend.DataBase.Handlers.purchase_details_handler import PurchaseDetailsHandler
from Backend.DataBase.Handlers.responsibilities_handler import ResponsibilitiesHandler
from Backend.DataBase.Handlers.shopping_bag_handler import ShoppingBagHandler
from Backend.DataBase.Handlers.store_handler import StoreHandler
from Backend.DataBase.database import mapper_registry, engine, session
from Backend.Service import logs
from Backend.response import Response

import Backend.Service.logs as log
from Backend.Service.DataObjects.shopping_cart_data import ShoppingCartData
from Backend.Service.DataObjects.statistics_data import StatisticsData

from Backend.Domain.Payment.payment_manager import PaymentManager
from Backend.Domain.TradingSystem.offer import Offer
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager


class TradingSystem(object):
    __instance = None

    # https://medium.com/@rohitgupta2801/the-singleton-class-python-c9e5acfe106c
    # double locking mechanism
    @staticmethod
    def getInstance() -> TradingSystem:
        """Static access method."""
        if TradingSystem.__instance is None:
            with threading.Lock():
                if TradingSystem.__instance is None:
                    TradingSystem()
        return TradingSystem.__instance

    def __init__(self):

        stmt = sqlalchemy.sql.expression.text("CREATE EXTENSION IF NOT EXISTS ltree;")
        session.execute(stmt)
        session.commit()

        MemberHandler.get_instance()
        StoreHandler.get_instance()
        ResponsibilitiesHandler.get_instance()
        ShoppingBagHandler.get_instance()
        ProductHandler.get_instance()
        PurchaseDetailsHandler.get_instance()
        OfferHandler.get_instance()

        mapper_registry.metadata.drop_all(engine)
        mapper_registry.metadata.create_all(engine)

        cookies = []
        store_ids = []
        product_ids = []
        """Virtually private constructor."""
        if TradingSystem.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TradingSystem.__instance = self
            self.payment_manager = PaymentManager()
            try:
                read_file = open("state.json", "r")
            except:
                e = FileNotFoundError("state.json file is absent")
                logs.log_file_errors(e)
                return
            with read_file:
                data = json.load(read_file)
                actions = data["actions"]
                for action in actions:
                    func = action["function"]
                    args = action["args"]
                    new_args = []
                    for arg in args:
                        if isinstance(arg, str):
                            if arg.split('#')[0] == 'cookie':
                                new_args.append(cookies[int(arg.split('#')[1]) - 1])
                            elif arg.split('#')[0] == 'store_id':
                                new_args.append(store_ids[int(arg.split('#')[1]) - 1])
                            elif arg.split('#')[0] == 'product_id':
                                new_args.append(product_ids[int(arg.split('#')[1]) - 1])
                            else:
                                new_args.append(arg)
                        else:
                            new_args.append(arg)
                    result = self.__getattribute__(func)(*new_args)
                    if func == "enter_system":
                        cookies.append(result)
                    elif func == "create_store":
                        if not result.succeeded():
                            raise Exception(f"initializing using state.json failed on function - {func}, args - {new_args}: {result.get_msg()}")
                        store_ids.append(result.get_obj())
                    elif func == "create_product":
                        if not result.succeeded():
                            raise Exception(f"initializing using state.json failed on function - {func}, args - {new_args}: {result.get_msg()}")
                        product_ids.append(result.get_obj())
                    elif not result.succeeded():
                        raise Exception(f"initializing using state.json failed on function - {func}, args - {new_args}: {result.get_msg()}")

    def enter_system(self):
        return TradingSystemManager.enter_system()

    @staticmethod
    @log.loging(to_hide=[0])
    def connect(cookie: str, communicate: Callable[[list[str]], bool]) -> Response[None]:
        return TradingSystemManager.connect(cookie, communicate)

    @log.loging(to_hide=[1, 3])
    def register(self, cookie, username, password) -> Response[None]:
        return TradingSystemManager.register(cookie=cookie, username=username, password=password)

    @log.loging(to_hide=[1, 3])
    def login(self, cookie, username, password):
        return TradingSystemManager.login(cookie=cookie, username=username, password=password)

    @log.loging()
    def get_stores_details(self):
        return TradingSystemManager.get_stores_details()

    @log.loging()
    def get_products_by_store(self, store_id: str):
        return TradingSystemManager.get_products_by_store(store_id)

    @log.loging()
    def get_store(self, store_id: str):
        return TradingSystemManager.get_store(store_id)

    # kwargs = You can search for a product by additional key words
    @log.loging()
    def search_products(
        self,
        product_name: str = None,
        product_category: str = None,
        min_price=None,
        max_price=None,
        keywords=None,
    ):
        return TradingSystemManager.search_products(
            product_name,
            product_category,
            min_price,
            max_price,
            keywords,
        )

    @log.loging(to_hide=[1])
    def save_product_in_cart(self, cookie, store_id, product_id, quantity=0):
        return TradingSystemManager.save_product_in_cart(cookie, store_id, product_id, quantity)

    @log.loging(to_hide=[1])
    def get_cart_details(self, cookie: str):
        return TradingSystemManager.get_cart_details(cookie)

    @log.loging(to_hide=[1])
    def remove_product_from_cart(self, cookie: str, store_id, product_id):
        return TradingSystemManager.remove_product_from_cart(cookie, store_id, product_id)

    @log.loging(to_hide=[1])
    def change_product_quantity_in_cart(self, cookie, store_id, product_id, new_quantity):
        return TradingSystemManager.change_product_quantity_in_cart(
            cookie, store_id, product_id, new_quantity
        )

    @log.loging(to_hide=[1])
    def purchase_cart(self, cookie: str, user_age: int):
        return TradingSystemManager.purchase_cart(cookie, user_age)

    @log.loging(to_hide=[1])
    def get_discounted_current_cart_price(self, cookie: str):
        return TradingSystemManager.get_discounted_current_cart_price(cookie)

    @log.loging(to_hide=[1])
    def send_payment(self, cookie, payment_details, address):
        TradingSystemManager.lock_cart(cookie)
        price = TradingSystemManager.get_cart_price(cookie)  # check cart price is None
        if not price.succeeded():
            TradingSystemManager.release_cart(cookie)
            return price
        cart: ShoppingCartData = TradingSystemManager.get_cart_details(cookie).get_obj()
        products_ids_to_quantity = {}
        for bag in cart.bags:
            products_ids_to_quantity |= bag.product_ids_to_quantities

        res = self.payment_manager.pay(
            price.get_obj(), payment_details, products_ids_to_quantity, address
        )
        if res.succeeded():
            TradingSystemManager.release_cart(cookie)
            delete_res = TradingSystemManager.purchase_completed(cookie)
            if not delete_res.succeeded():
                print(delete_res.get_msg())
                self.payment_manager.rollback(*res.get_obj())
            return delete_res
        else:
            TradingSystemManager.release_cart(cookie)
            return res

    @log.loging(to_hide=[1])
    def cancel_purchase(self, cookie: str):
        return TradingSystemManager.cancel_purchase(cookie)

    # Member
    # ===============================

    @log.loging(to_hide=[1])
    def create_store(self, cookie: str, name: str):
        return TradingSystemManager.create_store(cookie, name)

    @log.loging(to_hide=[1])
    def get_purchase_history(self, cookie: str):
        return TradingSystemManager.get_purchase_history(cookie)

    # Owner and manager
    # =======================

    @log.loging(to_hide=[1])
    def create_product(
        self,
        cookie: str,
        store_id: str,
        name: str,
        category: str,
        price: float,
        quantity: int,
        keywords: list[str] = None,
    ):
        return TradingSystemManager.create_product(
            cookie, store_id, name, category, price, quantity, keywords
        )

    @log.loging(to_hide=[1])
    def remove_product_from_store(self, cookie: str, store_id: str, product_id: str):
        return TradingSystemManager.remove_product_from_store(cookie, store_id, product_id)

    @log.loging(to_hide=[1])
    def change_product_quantity_in_store(
        self, cookie: str, store_id: str, product_id: str, quantity: int
    ):
        return TradingSystemManager.change_product_quantity_in_store(
            cookie, store_id, product_id, quantity
        )

    @log.loging(to_hide=[1])
    def edit_product_details(
        self,
        cookie: str,
        store_id: str,
        product_id: str,
        new_name: str = None,
        new_category: str = None,
        new_price: float = None,
        keywords: list[str] = None,
    ):
        return TradingSystemManager.edit_product_details(
            cookie, store_id, product_id, new_name, new_category, new_price, keywords
        )

    @log.loging()
    def get_product(self, store_id: str, product_id: str, username="Guest"):
        return TradingSystemManager.get_product(store_id, product_id, username)

    @log.loging()
    def get_product_from_bag(self, cookie: str, store_id: str, product_id: str, username=None):
        return TradingSystemManager.get_product_from_bag(cookie, store_id, product_id, username)

    @log.loging(to_hide=[1])
    def add_discount(
        self,
        cookie: str,
        store_id: str,
        discount_data: dict,
        exist_id: str,
        condition_type: str = None,
    ):
        return TradingSystemManager.add_discount(
            cookie, store_id, discount_data, exist_id, condition_type
        )

    @log.loging(to_hide=[1])
    def move_discount(self, cookie: str, store_id: str, src_id: str, dest_id: str):
        return TradingSystemManager.move_discount(cookie, store_id, src_id, dest_id)

    @log.loging(to_hide=[1])
    def get_discounts(self, cookie: str, store_id: str):
        return TradingSystemManager.get_discounts(cookie, store_id)

    @log.loging(to_hide=[1])
    def remove_discount(self, cookie: str, store_id: str, discount_id: str):
        return TradingSystemManager.remove_discount(cookie, store_id, discount_id)

    @log.loging(to_hide=[1])
    def edit_simple_discount(
        self,
        cookie: str,
        store_id: str,
        discount_id: str,
        percentage: float = None,
        context: dict = None,
        duration=None,
    ):
        return TradingSystemManager.edit_simple_discount(
            cookie, store_id, discount_id, percentage, context, duration
        )

    @log.loging(to_hide=[1])
    def edit_complex_discount(
        self,
        cookie: str,
        store_id: str,
        discount_id: str,
        complex_type: str = None,
        decision_rule: str = None,
    ):
        return TradingSystemManager.edit_complex_discount(
            cookie, store_id, discount_id, complex_type, decision_rule
        )

    @log.loging(to_hide=[1])
    def appoint_owner(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.appoint_owner(cookie, store_id, username)

    @log.loging(to_hide=[1])
    def appoint_manager(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.appoint_manager(cookie, store_id, username)

    @log.loging(to_hide=[1])
    def add_manager_permission(self, cookie: str, store_id: str, username: str, permission: str):
        return TradingSystemManager.add_manager_permission(cookie, store_id, username, permission)

    @log.loging(to_hide=[1])
    def remove_manager_permission(self, cookie: str, store_id: str, username: str, permission: str):
        return TradingSystemManager.remove_manager_permission(
            cookie, store_id, username, permission
        )

    @log.loging(to_hide=[1])
    def remove_appointment(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.remove_appointment(cookie, store_id, username)

    @log.loging(to_hide=[1])
    def get_store_appointments(self, cookie: str, store_id: str):
        return TradingSystemManager.get_store_appointments(cookie, store_id)

    @log.loging(to_hide=[1])
    def get_my_appointments(self, cookie: str):
        return TradingSystemManager.get_my_appointments(cookie)

    # 4.2
    @log.loging(to_hide=[1])
    def add_purchase_rule(
        self,
        cookie: str,
        store_id: str,
        rule_details: dict,
        rule_type: str,
        parent_id: str,
        clause: str = None,
    ):
        return TradingSystemManager.add_purchase_rule(
            cookie, store_id, rule_details, rule_type, parent_id, clause
        )

    # 4.2
    @log.loging(to_hide=[1])
    def remove_purchase_rule(self, cookie: str, store_id: str, rule_id: str):
        return TradingSystemManager.remove_purchase_rule(cookie, store_id, rule_id)

    # 4.2
    @log.loging(to_hide=[1])
    def edit_purchase_rule(
        self, cookie: str, store_id: str, rule_details: dict, rule_id: str, rule_type: str
    ):
        return TradingSystemManager.edit_purchase_rule(
            cookie, store_id, rule_details, rule_id, rule_type
        )

    # 4.2
    @log.loging(to_hide=[1])
    def move_purchase_rule(self, cookie: str, store_id: str, rule_id: str, new_parent_id: str):
        return TradingSystemManager.move_purchase_rule(cookie, store_id, rule_id, new_parent_id)

    # 4.11
    @log.loging(to_hide=[1])
    def get_store_purchase_history(self, cookie: str, store_id: str):
        return TradingSystemManager.get_store_purchase_history(cookie, store_id)

    # System Manager
    # ====================

    @log.loging(to_hide=[1])
    def get_any_store_purchase_history(self, cookie: str, store_id: str):
        return TradingSystemManager.get_any_store_purchase_history_admin(cookie, store_id)

    @log.loging(to_hide=[1])
    def get_user_purchase_history(self, cookie: str, username: str):
        return TradingSystemManager.get_any_user_purchase_history_admin(cookie, username)

    @log.loging(to_hide=[1])
    def empty_notifications(self, cookie: str):
        return TradingSystemManager.empty_notifications(cookie)

    @log.loging(to_hide=[1])
    def get_purchase_policy(self, cookie, store_id):
        return TradingSystemManager.get_purchase_policy(cookie, store_id)

    # Offers
    # ==================

    @log.loging(to_hide=[1])
    def get_user_offers(self, cookie) -> Response[list[Offer]]:
        return TradingSystemManager.get_user_offers(cookie)

    @log.loging(to_hide=[1])
    def get_store_offers(self, cookie, store_id) -> Response[list[Offer]]:
        return TradingSystemManager.get_store_offers(cookie, store_id)

    @log.loging(to_hide=[1])
    def create_offer(self, cookie, store_id, product_id) -> Response[str]:
        return TradingSystemManager.create_offer(cookie, store_id, product_id)

    @log.loging(to_hide=[1])
    def declare_price(self, cookie, offer_id, price) -> Response[None]:
        return TradingSystemManager.declare_price(cookie, offer_id, price)

    @log.loging(to_hide=[1])
    def suggest_counter_offer(
        self, cookie, store_id, product_id, offer_id, price
    ) -> Response[None]:
        return TradingSystemManager.suggest_counter_offer(
            cookie, store_id, product_id, offer_id, price
        )

    @log.loging(to_hide=[1])
    def approve_manager_offer(self, cookie, offer_id) -> Response[None]:
        return TradingSystemManager.approve_manager_offer(cookie, offer_id)

    @log.loging(to_hide=[1])
    def approve_user_offer(self, cookie, store_id, product_id, offer_id) -> Response[None]:
        return TradingSystemManager.approve_user_offer(cookie, store_id, product_id, offer_id)

    @log.loging(to_hide=[1])
    def reject_user_offer(self, cookie, store_id, product_id, offer_id) -> Response[None]:
        return TradingSystemManager.reject_user_offer(cookie, store_id, product_id, offer_id)

    @log.loging(to_hide=[1])
    def cancel_offer(self, cookie, offer_id) -> Response[None]:
        return TradingSystemManager.cancel_offer(cookie, offer_id)

    @log.loging(to_hide=[1])
    def get_users_statistics(self, cookie) -> Response[StatisticsData]:
        return TradingSystemManager.get_users_statistics(cookie)
