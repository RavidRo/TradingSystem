"""this class is the gateway from the domain layer to the DB layer
all the calls that need a DB authority will go through it"""

from Backend.DataBase.Users import users

users = users.users()

def register(username, password):
    return users.register(username=username,password=password)

def login(username, password):
    return users.login(username=username,password=password)




