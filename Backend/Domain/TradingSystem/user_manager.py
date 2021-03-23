from Backend.Domain.TradingSystem.user import User
from Backend.Domain.TradingSystem.member import Member


class UserManager(object):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if UserManager.__instance is None:
            UserManager()
        return UserManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if UserManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UserManager.__instance = self
            self.users = dict()
            self.cookie_generator = 1

    def enter_system(self):
        self.users[self.cookie_generator] = User()
        self.cookie_generator += 1
        return self.cookie_generator - 1

    def login(self, cookie, username, password):
        if cookie not in self.users:
            raise RuntimeError("Connection is not defined")
        msg = self.users[cookie].login(username, password)
        return msg

    def register(self, cookie, username, password):
        if cookie not in self.users:
            raise RuntimeError("Connection is not defined")
        msg = self.users[cookie].register(username, password)
        return msg
