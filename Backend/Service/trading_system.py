""" this class is responsible to communicate with the trading system manager"""


from Backend.Service.loggs import logging
from Backend.response import Response
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystem as trading_system_manager
from Backend.Domain.Payment.payment_manager import PaymentSystem


# TODO: import response object and the interface ItradingSystem


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
        return trading_system_manager.enter_system()

    @logging
    def register(self, cookie, username, password):
        return trading_system_manager.register(cookie=cookie, username=username, password=password)

    @logging
    def login(self, cookie, username, password):
        return trading_system_manager.login(cookie=cookie, username=username, password=password)

    @logging
    def get_stores_details(self):
        return trading_system_manager.get_stores_details()

    @logging
    def get_products_by_store(self, store_id: str):
        return trading_system_manager.get_products_by_store(store_id)

    @logging
    def search_products(self, product_name="", category=None, min_price=None, max_price=None, **kwargs):
        return trading_system_manager.search_products(product_name, category, min_price, max_price, **kwargs)

    @logging
    def save_product_in_cart(self, cookie, store_id, product_id, quantity):
        return trading_system_manager.save_product_in_cart(cookie, store_id, product_id, quantity)

    @logging
    def get_cart_details(self, cookie: str):
        return trading_system_manager.get_cart_details(cookie)

    @logging
    def remove_product_from_cart(self, cookie: str, product_id):
        return trading_system_manager.remove_product_from_cart(cookie, product_id)

    @logging
    def change_product_quantity_in_cart(self, cookie, store_id, product_id, new_quantity):
        return trading_system_manager.change_product_quantity_in_cart(cookie, store_id, product_id, new_quantity)

    @logging
    def purchase_cart(self, cookie: str):
        return trading_system_manager.purchase_cart(cookie)

    @logging
    def send_payment(self, cookie, payment_details):
        price = trading_system_manager.get_cart_price(cookie)
        res = PaymentSystem.pay(price, payment_details)
        if res.succeeded():
            return self.purchase_completed(cookie)
        else:
            return res.get_msg()

    @logging
    def purchase_completed(self, cookie: str):
        return trading_system_manager.purchase_completed(cookie)

    # Member
    # ===============================

    @logging
    def create_store(self, cookie: str, name: str):
        return trading_system_manager.create_store(cookie, name)

    @logging
    def get_purchase_history(self, cookie: str):
        return trading_system_manager.get_purchase_history(cookie)

    # Owner and manager
    # =======================

    @logging
    def create_product(self, cookie: str, store_id: str, name: str, price: float, quantity: int):
        return trading_system_manager.create_product(cookie, store_id, name, price, quantity)

    @logging
    def remove_products(self, cookie: str, store_id: str, product_id: str):
        return trading_system_manager.remove_products(cookie, store_id, product_id)

    @logging
    def change_product_quantity(cookie: str, store_id: str, product_id: str, quantity: int):
        return trading_system_manager.change_product_quantity(cookie, store_id, product_id, quantity)

    @logging
    def edit_product_details(cookie: str, store_id: str, product_id: str, new_name: str, new_price: float):
        return trading_system_manager.edit_product_details(cookie, store_id, product_id, new_name, new_price)

    @logging
    def appoint_owner(self, cookie: str, store_id: str, username: str):
        return trading_system_manager.appoint_owner(cookie, store_id, username)

    @logging
    def appoint_manager(self, cookie: str, store_id: str, username: str):
        return trading_system_manager.appoint_manager(cookie, store_id, username)

    @logging
    def add_manager_permission(self, cookie: str, store_id: str, username: str, permission_number: int):
        return trading_system_manager.add_manager_permission(cookie, store_id, username, permission_number)

    @logging
    def remove_manager_permission(self, cookie: str, store_id: str, username: str, permission_number: int):
        return trading_system_manager.remove_manager_permission(cookie, store_id, username, permission_number)

    @logging
    def remove_appointment(self, cookie: str, store_id: str, username: str):
        return trading_system_manager.remove_appointment(cookie, store_id, username)

    @logging
    def get_store_appointments(self, cookie: str, store_id: str):
        return trading_system_manager.get_store_appointments(cookie, store_id)

    # System Manager
    # ====================

    @logging
    def get_any_store_purchase_history(self, cookie: str, store_id: str):
        return trading_system_manager.get_any_store_purchase_history(cookie, store_id)

    @logging
    def get_user_purchase_history(self, cookie: str, username: str):
        return trading_system_manager.get_user_purchase_history(cookie, username)
