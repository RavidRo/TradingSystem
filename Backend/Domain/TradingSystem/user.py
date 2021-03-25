from Backend.Domain.TradingSystem.user_states import Guest, Member, Admin


class User(object):

    def __init__(self, state=None):
        if state is None:
            self.current_state = Guest(self)
        else:
            self.current_state = state

    def login(self, username, password):
        return self.current_state.login(username, password)

    def register(self, username, password):
        return self.current_state.register(username, password)
