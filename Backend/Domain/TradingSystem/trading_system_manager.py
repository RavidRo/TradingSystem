from Backend.Domain.TradingSystem.user_manager import UserManager


""""this class is the first class that is responsible to transfer all requests to domain layer"""

""" just fot debug the authentication import was made"""


class TradingSystemManager(object):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if TradingSystemManager.__instance is None:
            TradingSystemManager()
        return TradingSystemManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradingSystemManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TradingSystemManager.__instance = self
            self.user_manager = UserManager()

    def enter_system(self):
        return self.user_manager.enter_system()

    def get_any_store_purchase_history(self, store_id):
        return False

    def get_user_purchase_history(self, user_id):
        return False

    def register(self, cookie, username, password):
        return self.user_manager.register(cookie=cookie, username=username, password=password)

    def login(self, cookie, username, password):
        return self.user_manager.login(cookie=cookie, username=username, password=password)
