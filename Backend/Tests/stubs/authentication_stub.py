from Backend.response import Response


class AuthenticationStub:
    def __init__(self):
        self.registered = False
        self.logged_in = False

    def register(self, username, password):
        self.registered = True
        return Response(True)

    def login(self, username, password):
        self.logged_in = True
        return Response(True)
