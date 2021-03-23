""""this class is the first class that is responsible to transfer all requests to domain layer"""

""" just fot debug the authentication import was made"""
from Backend.Domain.Authentication import authentication

class TradingSystemManager(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TradingSystemManager.__instance == None:
            TradingSystemManager()
        return TradingSystemManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradingSystemManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TradingSystemManager.__instance = self
            self.authentication = authentication.Authentication()


    def register(self,username,password):
        return self.authentication.register(username=username,password=password)

    def login(self,username, password):
        return self.authentication.login(username=username,password=password)




