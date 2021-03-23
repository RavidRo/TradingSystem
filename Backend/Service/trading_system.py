""" this class is responsible to communicate with the trading system manager"""

from Backend.Domain.TradingSystem import TradingSystemManager

class TradingSystem(object):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TradingSystem.__instance == None:
            TradingSystem()
        return TradingSystem.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradingSystem.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TradingSystem.__instance = self
            self.trading_system_manager = TradingSystemManager.TradingSystemManager()


    def register(self,username,password):
        return self.trading_system_manager.register(username=username,password=password)

    def login(self,username, password):
        return self.trading_system_manager.login(username=username, password=password)




