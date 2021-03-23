""" this class is responsible to communicate with the trading system manager"""

from Backend.Domain.TradingSystem import trading_system_manager


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

    def enter_system(self):
        return self.trading_system_manager.enter_system()

    def register(self, cookie, username, password):
        return self.trading_system_manager.register(cookie=cookie, username=username, password=password)

    def login(self, cookie, username, password):
        return self.trading_system_manager.login(cookie=cookie, username=username, password=password)
