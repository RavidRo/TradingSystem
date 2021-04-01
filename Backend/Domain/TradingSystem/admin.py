from Backend.Domain.TradingSystem.member import Member


class Admin(Member):

    def __init__(self, user, username, responsibilities=None):
        super().__init__(user, username, responsibilities)

    def get_any_store_purchase_history(self, store_id):
        return TradingSystemManager.get_any_store_purchase_history(store_id)

    def get_user_purchase_history(self, user_id):
        return TradingSystemManager.get_user_purchase_history(user_id)
