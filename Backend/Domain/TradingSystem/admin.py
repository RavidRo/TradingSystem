from Backend.Domain.TradingSystem.member import Member
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager


class Admin(Member):

    def __init__(self, responsibilities=dict()):
        super().__init__(responsibilities)
        self.tranding_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        self.tranding_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        self.tranding_system_manager.get_user_purchase_history(user_id)
