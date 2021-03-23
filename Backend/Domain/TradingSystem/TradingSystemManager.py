""""this class is the first class that is responsible to transfer all requests to domain layer"""

""" just fot debug the authentication import was made"""
from Backend.Domain.Authentication import authentication

def register(username,password):
    return authentication.register(username=username,password=password)

def login(username, password):
    return authentication.login(username=username,password=password)




