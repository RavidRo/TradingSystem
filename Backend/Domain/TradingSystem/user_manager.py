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
            self.load_users()

    def load_users(self):                        # from DB in later milestones (according to cookie)
        self.users[1] = User('tali', Member())
        self.users[2] = User('ravid', Member())
        self.users[3] = User('sean', Member())
        self.users[4] = User('inon', Member())
        self.users[5] = User('omer', Member())

    def login(self, cookie, username, password):
        if cookie not in self.users:
            self.users[cookie] = User(username)
        msg = self.users[cookie].login(username, password)
        return msg

    def register(self, cookie, username, password):
        if cookie not in self.users:
            self.users[cookie] = User(username)
        msg = self.users[cookie].register(username, password)
        return msg



