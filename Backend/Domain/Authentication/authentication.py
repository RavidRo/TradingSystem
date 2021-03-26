from Backend.Domain import DBHandler
from abc import ABC, abstractmethod
from Backend import response

class IAuthentication(metaclass=ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'register') and
                callable(subclass.register) and
                hasattr(subclass, 'login') and
                callable(subclass.login))

class Authentication(IAuthentication):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Authentication.__instance is None:
            Authentication()
        return Authentication.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Authentication.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Authentication.__instance = self
            self.db_handler = DBHandler.DBHandler()

    def register(self, username, password):
        if self.db_handler.is_username_exists(username=username):
            # return "username already exists"
            return response.PrimitiveParsable(value="username already exists")

        else:
            self.db_handler.add_user_to_db(username=username, password=password)
            # return "registration succeeded"
            return response.PrimitiveParsable(value="registration succeeded")

    def login(self, username, password):
        if not self.db_handler.is_username_exists(username=username):
            # return "username doesn't exist in the system"
            return response.PrimitiveParsable(value="username doesn't exist in the system")

        else:
            if not self.db_handler.is_password_match(given_password=password, username=username):
                # return "password incorrect"
                return response.PrimitiveParsable(value="password incorrect")

            else:
                # return "login succeeded"
                return response.PrimitiveParsable(value="login succeeded")


