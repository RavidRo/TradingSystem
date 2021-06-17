import threading
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.DataBase.Handlers.member_handler import MemberHandler
from Backend.DataBase.database import db_fail_response
from Backend.response import Response, PrimitiveParsable

users = dict()
register_lock = threading.Lock()
member_handler = MemberHandler.get_instance()


def register(username, password) -> Response[None]:
    # We don't want to register to users with the same username
    with register_lock:
        if username in users:
            return Response(False, msg="username already exists")
        credentials = member_handler.load_credentials(username)
        if not credentials.succeeded():
            if credentials.get_obj() is not None:
                return db_fail_response
            res = __add_user_to_db(username, password)
            if not res:
                return db_fail_response
        else:
            users[username] = {'password': credentials.get_obj()[1]}
            return Response(False, msg="username already_exists")

        return Response(True, msg="registration succeeded")


# Fail if login failed and returns true if the user logged into is an admin
def login(username, password) -> Response[PrimitiveParsable[bool]]:
    if username not in users:
        credentials = member_handler.load_credentials(username)
        if not credentials.succeeded():
            if credentials.get_obj() is not None:
                return db_fail_response
            return Response(False, msg="username doesn't exist in the system")
        users[username] = {'password': credentials.get_obj()[1]}

    if not __is_password_match(password, username):
        return Response(False, msg="incorrect password")

    return Response(True, msg="login succeeded")


def remove_user_credrnials(username: str):
    users.pop(username)

def __add_user_to_db(username, password) -> bool:
    res = member_handler.save_user_credentials(username, generate_password_hash(password, method="sha256"))
    if res.succeeded():
        users[username] = {'password': generate_password_hash(password, method="sha256")}
        return True
    else:
        return False


def __is_password_match(given_password, username) -> bool:
    return check_password_hash(users[username]["password"], given_password)
