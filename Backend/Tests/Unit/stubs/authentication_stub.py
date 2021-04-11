from Backend.Domain.Authentication.authentication import Authentication
from Backend.response import Response, PrimitiveParsable


class AuthenticationStub:
    def __init__(self):
        self.registered = False
        self.logged_in = False

    def register(self, username, password):
        self.registered = True
        return Response(True)

    def login(self, username, password):
        self.logged_in = True
        if username == "admin":
            return Response(True, PrimitiveParsable(True))
        return Response(True, PrimitiveParsable(False))
