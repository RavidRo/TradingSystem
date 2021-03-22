"""this class is responsible for authentication of users in the system
all the register/login commands go here"""

from Backend.Domain import DBHandler

def register(username,password):
    return DBHandler.register(username=username,password=password)

def login(username, password):
    return DBHandler.login(username=username, password=password)




