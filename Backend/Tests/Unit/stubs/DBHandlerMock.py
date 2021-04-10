"""this class is ment to be the gateway from the domain layer to the DB"""

from Backend.DataBase.Users import users
from werkzeug.security import generate_password_hash, check_password_hash


class DBHandlerMock(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DBHandlerMock.__instance is None:
            DBHandlerMock()
        return DBHandlerMock.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DBHandlerMock.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DBHandlerMock.__instance = self
            self.users = {
                "Tali": {
                    "password": generate_password_hash("puppy", method="sha256"),
                    "is_admin": "True",
                },
                "Ravid": {
                    "password": generate_password_hash("dasi", method="sha256"),
                    "is_admin": "True",
                },
                "Inon": {
                    "password": generate_password_hash("guy", method="sha256"),
                    "is_admin": "",
                },
                "Sean": {
                    "password": generate_password_hash("Messi", method="sha256"),
                    "is_admin": "",
                },
                "Omer": {
                    "password": generate_password_hash("cool", method="sha256"),
                    "is_admin": "",
                },
            }

    def is_username_exists(self, username):
        return username in self.users

    def is_password_match(self, given_password, username):
        return check_password_hash(self.users[username]["password"], given_password)

    def add_user_to_db(self, username, password):
        self.users[username] = {
            "password": generate_password_hash(password, method="sha256"),
            "is_admin": "",
        }

    def is_username_admin(self, username):
        return bool(self.users[username]["is_admin"])
