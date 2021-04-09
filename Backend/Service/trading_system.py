""" this class is responsible to communicate with the trading system manager"""


from Backend.Service.logs import logging
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager
from Backend.Domain.Payment.payment_manager import PaymentSystem


class TradingSystem(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TradingSystem.__instance is None:
            TradingSystem()
        return TradingSystem.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradingSystem.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TradingSystem.__instance = self
            # self.trading_system_manager = trading_system_manager.TradingSystemManager()

    @logging
    def enter_system(self):
        return TradingSystemManager.enter_system()

    @logging
    def register(self, cookie, username, password):
        return TradingSystemManager.register(cookie=cookie, username=username, password=password)

    @logging
    def login(self, cookie, username, password):
        return TradingSystemManager.login(cookie=cookie, username=username, password=password)

    @logging
    def get_stores_details(self):
        return TradingSystemManager.get_stores_details()

    @logging
    def get_products_by_store(self, store_id: str):
        return TradingSystemManager.get_products_by_store(store_id)

    # kwargs = You can search for a product by additional key words
    @logging
    def search_products(
        self, *keywords, product_name="", category=None, min_price=None, max_price=None
    ):
        return TradingSystemManager.search_products(
            *keywords,
            product_name,
            category,
            min_price,
            max_price,
        )

    @logging
    def save_product_in_cart(self, cookie, store_id, product_id, quantity=1):
        return TradingSystemManager.save_product_in_cart(cookie, store_id, product_id, quantity)

    @logging
    def get_cart_details(self, cookie: str):
        return TradingSystemManager.get_cart_details(cookie)

    @logging
    def remove_product_from_cart(self, cookie: str, product_id):
        return TradingSystemManager.remove_product_from_cart(cookie, product_id)

    @logging
    def change_product_quantity_in_cart(self, cookie, store_id, product_id, new_quantity):
        return TradingSystemManager.change_product_quantity_in_cart(
            cookie, store_id, product_id, new_quantity
        )

    @logging
    def purchase_cart(self, cookie: str):
        return TradingSystemManager.purchase_cart(cookie)

    @logging
    def send_payment(self, cookie, payment_details):
        price = TradingSystemManager.get_cart_price(cookie)
        res = PaymentSystem.pay(price, payment_details)
        if res.succeeded():
            return self.purchase_completed(cookie)
        else:
            return res.get_msg()

    @logging
    def purchase_completed(self, cookie: str):
        return TradingSystemManager.purchase_completed(cookie)

    # Member
    # ===============================

    @logging
    def create_store(self, cookie: str, name: str):
        return TradingSystemManager.create_store(cookie, name)

    @logging
    def get_purchase_history(self, cookie: str):
        return TradingSystemManager.get_purchase_history(cookie)

    # Owner and manager
    # =======================

    @logging
    def create_product(self, cookie: str, store_id: str, name: str, price: float, quantity: int):
        return TradingSystemManager.create_product(cookie, store_id, name, price, quantity)

    @logging
    def remove_products(self, cookie: str, store_id: str, product_id: str):
        return TradingSystemManager.remove_products(cookie, store_id, product_id)

    @logging
    def change_product_quantity(cookie: str, store_id: str, product_id: str, quantity: int):
        return TradingSystemManager.change_product_quantity(cookie, store_id, product_id, quantity)

    @logging
    def edit_product_details(
        cookie: str, store_id: str, product_id: str, new_name: str, new_price: float
    ):
        return TradingSystemManager.edit_product_details(
            cookie, store_id, product_id, new_name, new_price
        )

    @logging
    def appoint_owner(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.appoint_owner(cookie, store_id, username)

    @logging
    def appoint_manager(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.appoint_manager(cookie, store_id, username)

    @logging
    def add_manager_permission(
        self, cookie: str, store_id: str, username: str, permission_number: int
    ):
        return TradingSystemManager.add_manager_permission(
            cookie, store_id, username, permission_number
        )

    @logging
    def remove_manager_permission(
        self, cookie: str, store_id: str, username: str, permission_number: int
    ):
        return TradingSystemManager.remove_manager_permission(
            cookie, store_id, username, permission_number
        )

    @logging
    def remove_appointment(self, cookie: str, store_id: str, username: str):
        return TradingSystemManager.remove_appointment(cookie, store_id, username)

    @logging
    def get_store_appointments(self, cookie: str, store_id: str):
        return TradingSystemManager.get_store_appointments(cookie, store_id)

    # System Manager
    # ====================

    @logging
    def get_any_store_purchase_history(self, cookie: str, store_id: str):
        return TradingSystemManager.get_any_store_purchase_history(cookie, store_id)

    @logging
    def get_user_purchase_history(self, cookie: str, username: str):
        return TradingSystemManager.get_user_purchase_history(cookie, username)
