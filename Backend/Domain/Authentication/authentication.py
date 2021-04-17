import threading
from werkzeug.security import generate_password_hash, check_password_hash
import json

from Backend.response import Response, PrimitiveParsable


class Authentication:
    __instance = None

    # double locking mechanism.
    # https://medium.com/@rohitgupta2801/the-singleton-class-python-c9e5acfe106c
    @staticmethod
    def get_instance():
        """ Static access method. """
        if Authentication.__instance is None:
            with threading.Lock():
                if Authentication.__instance is None:
                    Authentication()
        return Authentication.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Authentication.__instance is not None:
            raise Exception("This class is a singleton!")

        Authentication.__instance = self
        self.users = {}
        self.register_lock = threading.Lock()
        self.__register_admins()

    def register(self, username, password) -> Response[None]:
        # We don't want to register to users with the same username
        with self.register_lock:
            if username in self.users:
                return Response(False, msg="username already exists")

            self.__add_user_to_db(username, password)
            return Response(True, msg="registration succeeded")

    # Fail if login failed and returns true if the user logged into is an admin
    def login(self, username, password) -> Response[PrimitiveParsable[bool]]:
        if username not in self.users:
            return Response(False, msg="username doesn't exist in the __system")

        if not self.__is_password_match(password, username):
            return Response(False, msg="password incorrect")

        is_admin = self.__is_username_admin(username)
        return Response(True, PrimitiveParsable(is_admin), msg="login succeeded")

    def __add_user_to_db(self, username, password, is_admin=False) -> None:
        self.users[username] = {
            "password": generate_password_hash(password, method="sha256"),
            "admin": is_admin,
        }

    def __is_password_match(self, given_password, username) -> bool:
        return check_password_hash(self.users[username]["password"], given_password)

    def __is_username_admin(self, username) -> bool:
        return self.users[username]["admin"]

    def __register_admins(self) -> None:
        with open("config.json", "r") as read_file:
            data = json.load(read_file)
            admin_password = data["admin-password"]
            for username in data["admins"]:
                self.__add_user_to_db(username, admin_password, True)
