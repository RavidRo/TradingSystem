

from Backend.Domain import DBHandler

def register(username, password):
    if DBHandler.is_username_exists(username=username):
        return "username already exists"
    else:
        DBHandler.add_user_to_db(username=username,password=password)
        return "registration succeeded"

def login(username, password):
    if not DBHandler.is_username_exists(username=username):
        return "username doesn't exist in the system"
    else:
        if not DBHandler.is_password_match(given_password=password,username=username):
            return "password incorrect"
        else:
            return "login succeeded"



