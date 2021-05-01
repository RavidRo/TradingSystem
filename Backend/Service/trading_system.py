""" this class is responsible to communicate with the trading __system manager"""
from __future__ import annotations
import threading
from typing import Callable

from Backend.Domain.Payment.payment_manager import PaymentManager
from Backend.Service.DataObjects.shopping_cart_data import ShoppingCartData
import Backend.Service.logs as log
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager
from Backend.response import Response


class TradingSystem(object):
    __instance = None

    # https://medium.com/@rohitgupta2801/the-singleton-class-python-c9e5acfe106c
    # double locking mechanism
    @staticmethod
    def getInstance() -> TradingSystem:
        """ Static access method. """
        if TradingSystem.__instance is None:
            with threading.Lock():
                if TradingSystem.__instance is None:
                    TradingSystem()
        return TradingSystem.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradingSystem.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TradingSystem.__instance = self
            self.payment_manager = PaymentManager()

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
    def purchase_cart(self, cookie: str):
        return TradingSystemManager.purchase_cart(cookie)

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
            return TradingSystemManager.purchase_completed(cookie)
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
    def get_my_appointees(self, cookie: str, store_id: str):
        return TradingSystemManager.get_my_appointees(cookie, store_id)

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
