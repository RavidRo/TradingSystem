""" this class is responsible to communicate with the trading system manager"""

from Backend.Domain.TradingSystem import trading_system_manager
from Backend.Domain.Payment import PaymentManager



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
            self.trading_system_manager = trading_system_manager.TradingSystemManager()
            self.payment_manager = PaymentManager.PaymentManager()

    def enter_system(self):
        return self.trading_system_manager.enter_system()

    def register(self, cookie, username, password):
        return self.trading_system_manager.register(cookie=cookie, username=username, password=password)

    def login(self, cookie, username, password):
        return self.trading_system_manager.login(cookie=cookie, username=username, password=password)

    def get_stores_details(self):
        return self.trading_system_manager.get_stores_details()

    def get_products_by_store(self, store_id: str):
        return self.trading_system_manager.get_products_by_store(store_id)

    def search_products(self, product_name="", category=None, min_price=None, max_price=None, **kwargs):
        return self.trading_system_manager.search_products(product_name, category, min_price, max_price, **kwargs)

    def add_to_cart(self, cookie: str, product_id: str, quantity=1):
        return self.trading_system_manager.search_products(cookie, product_id, quantity)

    def get_cart_details(self, cookie: str) :
        return self.trading_system_manager.get_cart_details(cookie)

    def remove_product_from_cart(self, cookie: str, product_id: str, quantity=1):
        return self.trading_system_manager.remove_product_from_cart(cookie, product_id, quantity)

    def purchase_cart(self, cookie: str):
        return self.trading_system_manager.purchase_cart(cookie)

    def purchase_completed(self, cookie: str):
        return self.trading_system_manager.purchase_completed(cookie)

    # Member
    # ===============================

    def create_store(self, cookie: str, name: str):
        return self.trading_system_manager.create_store(cookie, name)

    def ger_purchase_history(self, cookie: str):
        return self.trading_system_manager.ger_purchase_history(cookie)

    # Owner and manager
    # =======================

    def create_product(self, cookie: str, store_id: str, name: str, price: float) :
        return self.trading_system_manager.create_product(cookie, store_id, name, price)

    def add_products(self, cookie: str, store_id: str, product_id: str, quantity: int) :
        return self.trading_system_manager.add_products(cookie, store_id, product_id, quantity)

    def remove_products(self, cookie: str, store_id: str, product_id: str, quantity: int):
        return self.trading_system_manager.remove_products(cookie, store_id, product_id, quantity)

    def set_product_price(self, cookie: str, store_id: str, product_id: str, new_price: float):
        return self.trading_system_manager.set_product_price(cookie, store_id, product_id, new_price)

    def appoint_owner(self, cookie: str, store_id: str, username: str):
        return self.trading_system_manager.appoint_owner(cookie, store_id, username)

    def appoint_manager(self, cookie: str, store_id: str, username: str):
        return self.trading_system_manager.appoint_manager(cookie, store_id, username)

    def add_manager_permission(self, cookie: str, store_id: str, username: str, permission_number: int):
        return self.trading_system_manager.add_manager_permission(cookie, store_id, username, permission_number)

    def remove_manager_permission(self, cookie: str, store_id: str, username: str, permission_number: int) :
        return self.trading_system_manager.remove_manager_permission(cookie, store_id, username, permission_number)

    def remove_appointment(self, cookie: str, store_id: str, username: str):
        return self.trading_system_manager.remove_appointment(cookie, store_id, username)

    def get_store_appointments(self, cookie: str, store_id: str) :
        return self.trading_system_manager.get_store_appointments(cookie, store_id)

    def get_store_purchases_history(self, cookie: str, store_id: str):
        return self.trading_system_manager.get_store_purchases_history(cookie, store_id)

    # System Manager
    # ====================

    def get_user_purchase_history(self, cookie: str, username: str):
        return self.trading_system_manager.get_user_purchase_history(cookie, username)
