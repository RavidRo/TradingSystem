""" this class is responsible to communicate with the trading system manager"""

from Backend.Domain.TradingSystem import TradingSystemManager

def register(username,password):
    return TradingSystemManager.register(username=username,password=password)

def login(username, password):
    return TradingSystemManager.login(username=username, password=password)




