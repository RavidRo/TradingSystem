import threading
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.response import Response, PrimitiveParsable

users = {}
register_lock = threading.Lock()


def register(username, password) -> Response[None]:
    # We don't want to register to users with the same username
    with register_lock:
        if username in users:
            return Response(False, msg="username already exists")

        __add_user_to_db(username, password)
        return Response(True, msg="registration succeeded")


# Fail if login failed and returns true if the user logged into is an admin
def login(username, password) -> Response[PrimitiveParsable[bool]]:
    if username not in users:
        return Response(False, msg="username doesn't exist in the system")

    if not __is_password_match(password, username):
        return Response(False, msg="password incorrect")

    # is_admin = self.__is_username_admin(username)
    return Response(True, msg="login succeeded")


def __add_user_to_db(username, password) -> None:
    users[username] = {
        "password": generate_password_hash(password, method="sha256")
    }


def __is_password_match(given_password, username) -> bool:
    return check_password_hash(users[username]["password"], given_password)
