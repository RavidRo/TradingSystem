"""this class is ment to be the gateway from the domain layer to the DB"""

from Backend.DataBase.Users import users


class DBHandler(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DBHandler.__instance is None:
            DBHandler()
        return DBHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DBHandler.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DBHandler.__instance = self
            self.users_db = users.Users()

    def is_username_exists(self, username):
        return self.users_db.is_username_exists(username=username)

    def is_password_match(self, given_password, username):
        return self.users_db.is_password_match(given_password=given_password, username=username)

    def add_user_to_db(self, username, password):
        self.users_db.add_user_to_db(username=username, password=password)
