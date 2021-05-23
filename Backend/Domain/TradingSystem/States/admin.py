from Backend.Domain.TradingSystem.States.member import Member


class Admin(Member):
    def __init__(self, user, username, responsibilities=None, purchase_details=None, cart=None):
        super().__init__(user, username, responsibilities, purchase_details, cart)

    def get_any_store_purchase_history_admin(self, store_id):
        from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager

        return TradingSystemManager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history_admin(self, username):
        from Backend.Domain.TradingSystem.trading_system_manager import TradingSystemManager

        return TradingSystemManager.get_any_user_purchase_history(username)
