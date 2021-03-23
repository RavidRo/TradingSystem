from Backend.Domain.TradingSystem.guest import Guest
from Backend.Domain.TradingSystem.member import Member


class User(object):

    def __init__(self, username, state=Guest()):
        self.current_state = state
        self.username = username
        self.member_state = Member(self)

    def change_state(self, state):
        self.current_state = state

    def login(self, username, password):
        msg = self.current_state.login(username, password)
        if type(msg) == int:
            # Assumption: User holds the function change_state and the different states of the user.
            self.change_state(self.member_state)
        return msg

    def register(self, username, password):
        return self.current_state.register(username, password)
