from Backend.Domain.TradingSystem.member import Member
from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager

class Admin(Member):

    def __init__(self, user):
        super().__init__(user)
        self.tranding_system_manager = TradingSystemManager.get_instance()

    def __init__(self, user, responsibilities):
        super().__init__(user, responsibilities)
        self.tranding_system_manager = TradingSystemManager.get_instance()

    def get_any_store_purchase_history(self, store_id):
        self.tranding_system_manager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        self.tranding_system_manager.get_user_purchase_history(user_id)