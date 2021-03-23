from Backend.Domain.TradingSystem.user_states import Guest, Member, Admin


class User(object):

    def __init__(self, state=Guest()):
        self.current_state = state
        self.member_state = Member(self)        # should take the state from DB

    def change_state(self, state):
        self.current_state = state

    def login(self, username, password):
        msg = self.current_state.login(username, password)
        if msg == "login succeeded":
            # Assumption: User holds the function change_state and the different states of the user.
            self.change_state(self.member_state)
        return msg

    def register(self, username, password):
        return self.current_state.register(username, password)
