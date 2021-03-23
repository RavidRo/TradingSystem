"""this class is ment to be the gateway from the domain layer to the DB"""

from Backend.DataBase.Users import users

"""initializing mock DB"""
users = users.users()

def is_username_exists(username):
    return users.is_username_exists(username=username)

def is_password_match(given_password,username):
     return users.is_password_match(given_password=given_password,username=username)

def add_user_to_db(username,password):
    users.add_user_to_db(username=username,password=password)



