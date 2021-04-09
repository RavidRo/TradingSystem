from .member import Member
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager


class Admin(Member):
    def __init__(self, user, username, responsibilities=None):
        super().__init__(user, username, responsibilities)

    def get_any_store_purchase_history(self, store_id):
        return TradingSystemManager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, username):
        return TradingSystemManager.get_any_user_purchase_history(username)
