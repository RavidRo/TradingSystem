""" this class is responsible to communicate with the trading system manager"""
from __future__ import annotations
import threading
from asgiref.sync import sync_to_async



from Backend.Service.DataObjects.shopping_cart_data import ShoppingCartData
import Backend.Service.logs as log
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager
import Backend.Domain.Payment.payment_manager as PaymentSystem


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

    # @logging

    @sync_to_async
    def enter_system(self):
        return TradingSystemManager.enter_system()

    @sync_to_async
    @log.loging(to_hide=[1, 3])
    def register(self, cookie, username, password):
        return TradingSystemManager.register(cookie=cookie, username=username, password=password)

    @sync_to_async
    @log.loging(to_hide=[1, 3])
    def login(self, cookie, username, password):
        return TradingSystemManager.login(cookie=cookie, username=username, password=password)

    @sync_to_async
    @log.loging()
    def get_stores_details(self):
        return TradingSystemManager.get_stores_details()

    @sync_to_async
    @log.loging()
    def get_products_by_store(self, store_id: str):
        return TradingSystemManager.get_products_by_store(store_id)

    @sync_to_async
    @log.loging()
    def get_store(self, store_id: str):
        return TradingSystemManager.get_store(store_id)

    # kwargs = You can search for a product by additional key words
    @sync_to_async
    @log.loging()
    def search_products(
        self, *keywords, product_name="", category=None, min_price=None, max_price=None
    ):
        return TradingSystemManager.search_products(
            product_name,
            category,
            min_price,
            max_price,
            *keywords,
        )

    @sync_to_async
    @log.loging(to_hide=[1])
    def save_product_in_cart(self, cookie, store_id, product_id, quantity=0):
        return TradingSystemManager.save_product_in_cart(cookie, store_id, product_id, quantity)

    @sync_to_async
    @log.loging(to_hide=[1])
    def get_cart_details(self, cookie: str):
        return TradingSystemManager.get_cart_details(cookie)

    @sync_to_async
    @log.loging(to_hide=[1])
    def remove_product_from_cart(self, cookie: str, store_id, product_id):
        return TradingSystemManager.remove_product_from_cart(cookie, store_id, product_id)

    @sync_to_async
    @log.loging(to_hide=[1])
    def change_product_quantity_in_cart(self, cookie, store_id, product_id, new_quantity):
        return TradingSystemManager.change_product_quantity_in_cart(
            cookie, store_id, product_id, new_quantity
        )

    @sync_to_async
    @log.loging(to_hide=[1])
    def purchase_cart(self, cookie: str):
        return TradingSystemManager.purchase_cart(cookie)

    @sync_to_async
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

        res = PaymentSystem.pay(price, payment_details, products_ids_to_quantity, address)
        if res.succeeded():
            TradingSystemManager.release_cart(cookie)
            return TradingSystemManager.purchase_completed(cookie)
        else:
            TradingSystemManager.release_cart(cookie)
            return res

    @sync_to_async
    @log.loging(to_hide=[1])
    def cancel_purchase(self, cookie: str):
        return TradingSystemManager.cancel_purchase(cookie)

    # Member
    # ===============================

    @sync_to_async
    @log.loging(to_hide=[1])
    def create_store(self, cookie: str, name: str):
        return TradingSystemManager.create_store(cookie, name)

    @sync_to_async
    @log.loging(to_hide=[1])
    def get_purchase_history(self, cookie: str):
        return TradingSystemManager.get_purchase_history(cookie)

    # Owner and manager
    # =======================

    @sync_to_async
    @log.loging(to_hide=[1])
    def create_product(self, cookie: str, store_id: str, name: str, price: float, quantity: int):
        return TradingSystemManager.create_product(cookie, store_id, name, price, quantity)

    @sync_to_async
    @log.loging(to_hide=[1])
    def remove_product_from_store(self, cookie: str, store_id: str, product_id: str):
        return TradingSystemManager.remove_product_from_store(cookie, store_id, product_id)

    @sync_to_async
    @log.loging(to_hide=[1])
    def change_product_quantity_in_store(
        self, cookie: str, store_id: str, product_id: str, quantity: int
    ):
        return TradingSystemManager.change_product_quantity_in_store(
            cookie, store_id, product_id, quantity
        )

    @sync_to_async
    @log.loging(to_hide=[1])
    def edit_product_details(
        self,
        cookie: str,
        store_id: str,
        product_id: str,
        new_name: str = None,
        new_price: float = None,
    ):
        return TradingSystemManager.edit_product_details(
            cookie, store_id, product_id, new_name, new_price
        )

    @sync_to_async
    @log.loging(to_hide=[1])
    def appoint_owner(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.appoint_owner(cookie, store_id, username)

    @sync_to_async
    @log.loging(to_hide=[1])
    def appoint_manager(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.appoint_manager(cookie, store_id, username)

    @sync_to_async
    @log.loging(to_hide=[1])
    def add_manager_permission(self, cookie: str, store_id: str, username: str, permission: str):
        return TradingSystemManager.add_manager_permission(cookie, store_id, username, permission)

    @sync_to_async
    @log.loging(to_hide=[1])
    def remove_manager_permission(self, cookie: str, store_id: str, username: str, permission: str):
        return TradingSystemManager.remove_manager_permission(
            cookie, store_id, username, permission
        )

    @sync_to_async
    @log.loging(to_hide=[1])
    def remove_appointment(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.remove_appointment(cookie, store_id, username)

    @sync_to_async
    @log.loging(to_hide=[1])
    def get_store_appointments(self, cookie: str, store_id: str):
        return TradingSystemManager.get_store_appointments(cookie, store_id)

    # 4.11
    @sync_to_async
    @log.loging(to_hide=[1])
    def get_store_purchase_history(self, cookie: str, store_id: str):
        return TradingSystemManager.get_store_purchase_history(cookie, store_id)

    # System Manager
    # ====================

    @sync_to_async
    @log.loging(to_hide=[1])
    def get_any_store_purchase_history(self, cookie: str, store_id: str):
        return TradingSystemManager.get_any_store_purchase_history_admin(cookie, store_id)

    @sync_to_async
    @log.loging(to_hide=[1])
    def get_user_purchase_history(self, cookie: str, username: str):
        return TradingSystemManager.get_any_user_purchase_history_admin(cookie, username)
