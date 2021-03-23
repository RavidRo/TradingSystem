from Backend.Domain.TradingSystem.guest import Guest
from Backend.Domain.TradingSystem.member import Member
from Backend.Domain.TradingSystem.admin import Admin

class User:

    def __init__(self, state):
        self.current_state = state

    def __init__(self):
        self.current_state = Guest(self)

    def change_state(state):
        self.state = state

if __name__ == '__main__':
    user = User()
    user.current_state.login("inon", "guy")

    